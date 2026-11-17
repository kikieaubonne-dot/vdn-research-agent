"""Additional fault scenarios; local fixtures only, never the user's game."""
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from agent.reliability import BlackBox, redact
from scripts import eponge_guard as guard
from tests import test_operations as previous

REPO = Path(__file__).resolve().parents[1]


class ContinuationSafetyTests(unittest.TestCase):
    def test_quoted_json_and_headers_do_not_expose_credentials(self):
        raw = '{"api_key": "PRIVATE_JSON_KEY", "password": "PRIVATE_JSON_PASSWORD", "Authorization": "Bearer PRIVATE_HEADER"} token=PRIVATE_PLAIN'
        for render in (redact, guard.redact):
            text = render(raw)
            for secret in ('PRIVATE_JSON_KEY', 'PRIVATE_JSON_PASSWORD', 'PRIVATE_HEADER', 'PRIVATE_PLAIN'):
                self.assertNotIn(secret, text)
            self.assertIn('[REDACTED]', text)

    def test_independent_log_stream_redacts_quoted_json(self):
        output = io.BytesIO(); failed = threading.Event()
        guard.drain(io.BytesIO(b'{"token": "PRIVATE_STREAM"}\n'), output, failed)
        self.assertNotIn(b'PRIVATE_STREAM', output.getvalue())
        self.assertFalse(failed.is_set())

    def test_blackbox_primary_disk_failure_uses_separate_emergency_location(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as emergency:
            box = BlackBox(Path(d))
            import agent.reliability as reliability
            original = reliability.atomic_write
            def fail_primary(path, *args, **kwargs):
                if Path(path).is_relative_to(Path(d)):
                    raise OSError(28, 'AUTHORED full primary filesystem')
                return original(path, *args, **kwargs)
            with patch.object(reliability, 'atomic_write', side_effect=fail_primary), patch('tempfile.gettempdir', return_value=emergency), patch('sys.stderr', new_callable=io.StringIO):
                p = box.fallback('reporter', OSError(28, 'token=PRIVATE_DISK_FAILURE'))
            self.assertFalse(p.is_relative_to(Path(d)))
            report = json.loads(p.read_text())
            self.assertEqual(report['state'], 'DIAGNOSTIC_UNAVAILABLE')
            self.assertNotIn('PRIVATE_DISK_FAILURE', p.read_text())
            self.assertTrue(report['primary_failed'])

    def test_guard_fallback_without_core_imports_survives_primary_disk_failure(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as emergency:
            with patch.object(guard, 'write', side_effect=OSError(28, 'AUTHORED disk full')), patch('tempfile.gettempdir', return_value=emergency), patch('sys.stderr', new_callable=io.StringIO):
                p = guard.emergency(Path(d), 'supervisor', OSError(28, 'password=PRIVATE_GUARD_FAILURE'))
            self.assertTrue(p.is_file())
            self.assertEqual(json.loads(p.read_text())['state'], 'DIAGNOSTIC_UNAVAILABLE')
            self.assertNotIn('PRIVATE_GUARD_FAILURE', p.read_text())


class GuardParentLossTests(unittest.TestCase):
    setUp = previous.IndependentGuardTests.setUp
    fixture = previous.IndependentGuardTests.fixture
    run_guard = previous.IndependentGuardTests.run_guard

    @unittest.skipIf(os.name == 'nt', 'POSIX SIGKILL injection; Windows parent-loss test remains separate')
    def test_killed_supervisor_cannot_leave_worker_running_and_restart_reuses_effect(self):
        body = '''import json,os,sys,time
from pathlib import Path
root=Path(sys.argv[sys.argv.index('--workspace')+1]);wid=sys.argv[-1]
p=root/'effect.txt'
if not p.exists():p.write_text('one authorized fixture effect')
if (root/'complete-fixture').exists():raise SystemExit(0)
while True:
 h={'worker_id':wid,'worker_pid':os.getpid(),'last_heartbeat':time.time(),'last_progress':time.time(),'activity':'fixture'}
 p=root/'reports/status.json';q=p.with_suffix('.tmp');q.write_text(json.dumps(h));os.replace(q,p)
 time.sleep(.1)
'''
        self.fixture(body, duration=20)
        command = [sys.executable, str(REPO/'scripts/eponge_guard.py'), 'supervise', str(self.ws)]
        first = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=(os.name!='nt'))
        self.addCleanup(lambda: guard.terminate(first) if first.poll() is None else None)
        end = time.monotonic()+8
        while time.monotonic()<end:
            try:
                h=json.loads((self.ws/'reports/status.json').read_text())
                if h.get('activity')=='fixture':break
            except (OSError, ValueError):pass
            time.sleep(.05)
        else:self.fail('fixture worker did not start')
        worker_pid=h['worker_pid']
        def cleanup_owned_fixture():
            p=Path('/proc')/str(worker_pid)/'cmdline'
            if p.exists() and str(self.ws).encode() in p.read_bytes():
                try:os.killpg(worker_pid,signal.SIGTERM)
                except ProcessLookupError:pass
        self.addCleanup(cleanup_owned_fixture)
        first.kill();first.wait(timeout=3)
        def live(pid):
            p=Path('/proc')/str(pid)/'stat'
            return p.exists() and p.read_text().split()[2]!='Z'
        end=time.monotonic()+5
        while live(worker_pid) and time.monotonic()<end:time.sleep(.05)
        self.assertFalse(live(worker_pid),'worker outlived its dead supervisor')
        lease=json.loads((self.ws/'worker-lease.json').read_text())
        self.assertEqual(lease['state'],'PARENT_LEASE_LOST')
        before=(self.ws/'effect.txt').read_bytes()
        (self.ws/'complete-fixture').write_text('operator-authorized fixture resume')
        resumed=self.run_guard()
        self.assertEqual(resumed.returncode,0,resumed.stdout+resumed.stderr)
        self.assertEqual(before,(self.ws/'effect.txt').read_bytes())

    def test_future_heartbeat_cannot_disable_watchdog(self):
        body='''import json,os,sys,time
from pathlib import Path
r=Path(sys.argv[sys.argv.index('--workspace')+1])
h={'worker_id':sys.argv[-1],'worker_pid':os.getpid(),'last_heartbeat':time.time()+3600,'last_progress':time.time()+3600,'activity':'fixture'}
(r/'reports/status.json').write_text(json.dumps(h));time.sleep(15)
'''
        self.fixture(body,duration=8)
        started=time.monotonic();r=self.run_guard()
        self.assertNotEqual(r.returncode,0)
        self.assertLess(time.monotonic()-started,7)

class BudgetAccountingTests(unittest.TestCase):
    setUp = previous.RecoveryTests.setUp

    def test_fetch_attempt_is_not_an_http_call_in_intelligence_operation(self):
        from agent import budget, intelligence_models as im
        from agent.research_queue import ResearchQueue
        before=dict(ResearchQueue(self.root, recover=False).daily())
        im.operation(self.root, budget.fetch_attempt)
        after=ResearchQueue(self.root, recover=False).daily()
        self.assertEqual(after['http_calls'], before['http_calls'])
        self.assertEqual(after['fetch'], before['fetch']+1)

class IncidentEscalationTests(unittest.TestCase):
    setUp = previous.RecoveryTests.setUp

    def test_recurrence_cannot_downgrade_critical_or_remove_human_review(self):
        a=self.box.incident('fixture','same-operation','AUTHORED same failure','CRITICAL',requires_human=True)
        b=self.box.incident('fixture','same-operation','AUTHORED same failure','LOW',requires_human=False)
        self.assertEqual(a['incident_id'],b['incident_id'])
        self.assertEqual(b['severity'],'CRITICAL')
        self.assertTrue(b['requires_human'])
        with self.assertRaises(PermissionError):self.box.attempt(b['incident_id'],'retry_transient')

    def test_loss_of_all_journal_locations_remains_explicit(self):
        with patch('agent.reliability.atomic_write',side_effect=OSError(28,'AUTHORED disk full')),patch('sys.stderr',new_callable=io.StringIO) as console:
            r=self.box.fallback('reporter',OSError(28,'token=PRIVATE_ALL_DISKS'))
        self.assertIsNone(r)
        self.assertIn('DIAGNOSTIC_UNAVAILABLE',console.getvalue())
        self.assertNotIn('PRIVATE_ALL_DISKS',console.getvalue())

class SingleMissionTests(unittest.TestCase):
    setUp = previous.IndependentGuardTests.setUp
    fixture = previous.IndependentGuardTests.fixture
    run_guard = previous.IndependentGuardTests.run_guard

    def test_two_workspaces_cannot_run_concurrent_missions(self):
        body='''import json,os,sys,time
from pathlib import Path
r=Path(sys.argv[sys.argv.index('--workspace')+1]);(r/'fixture-started').write_text('owned fixture')
while True:
 h={'worker_id':sys.argv[-1],'worker_pid':os.getpid(),'last_heartbeat':time.time(),'last_progress':time.time(),'activity':'fixture'}
 p=r/'reports/status.json';q=p.with_suffix('.tmp');q.write_text(json.dumps(h));os.replace(q,p);time.sleep(.1)
'''
        self.fixture(body,duration=15)
        first=subprocess.Popen([sys.executable,str(REPO/'scripts/eponge_guard.py'),'supervise',str(self.ws)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=(os.name!='nt'))
        self.addCleanup(lambda:guard.terminate(first) if first.poll() is None else None)
        end=time.monotonic()+6
        while not (self.ws/'fixture-started').exists() and time.monotonic()<end:time.sleep(.05)
        self.assertTrue((self.ws/'fixture-started').exists())
        other=previous.IndependentGuardTests();other.setUp();self.addCleanup(other.doCleanups)
        other.fixture("print('SECOND SHOULD NOT RUN')\n")
        second=other.run_guard()
        self.assertNotEqual(second.returncode,0)
        events=json.loads((other.ws/'guard-events.json').read_text())['events'] if (other.ws/'guard-events.json').exists() else []
        self.assertFalse(any(e['kind']=='CHILD_STARTED' for e in events))
        self.assertFalse((other.ws/'worker-lease.json').exists())

class WindowsLauncherPinTests(unittest.TestCase):
    def test_windows_launchers_are_part_of_the_validation_baseline(self):
        from scripts.eponge_validate import inventory
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'scripts').mkdir();(root/'eponge.py').write_text('pass\n')
            launcher=root/'Eponge.cmd';launcher.write_text('@echo off\npython eponge.py\n')
            script=root/'scripts/local.ps1';script.write_text('Write-Output fixture\n')
            before=inventory(root)
            self.assertIn('Eponge.cmd',before)
            self.assertIn('scripts/local.ps1',before)
            launcher.write_text('@echo unvalidated alteration\n')
            self.assertNotEqual(before,inventory(root))
