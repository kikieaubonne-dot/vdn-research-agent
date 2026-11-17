"""Independent bounded supervisor and change gate. Standard library only.

Never installs a service, changes permissions or launches Web-supplied commands.
Only the child group created here may be terminated. The core can be unavailable.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import re
import threading
import time
import tempfile
import uuid


def safe(root,relative):
    root=Path(root).absolute();rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in str(relative):raise ValueError('unsafe guard path')
    p=root/rel
    if not p.resolve().is_relative_to(root.resolve()):raise ValueError('guard path escaped workspace')
    if any(q.is_symlink() for q in (p,*p.parents)):raise ValueError('guard symlink refused')
    return p


def read(root,name,limit=2_000_000):
    p=safe(root,name)
    if p.stat().st_size>limit:raise ValueError('guard input oversized')
    return json.loads(p.read_text(encoding='utf-8'))


def write(root,name,value):
    p=safe(root,name);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name('.'+p.name+'.'+uuid.uuid4().hex)
    try:
        with tmp.open('x',encoding='utf-8') as f:json.dump(value,f,allow_nan=False);f.flush();os.fsync(f.fileno())
        os.replace(tmp,p)
    finally:tmp.unlink(missing_ok=True)


def redact(value):
    text=str(value)
    # JSON/header quoting is not present in key=value logs. Cover both forms.
    text=re.sub(r'''(?ix)(["']?(?:api[_-]?key|token|access_token|password|secret|authorization)["']?\s*[:=]\s*)(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s,;]+)''',r'\1[REDACTED]',text)
    text=re.sub(r'(?i)(bearer\s+)[^\s,;"\']+',r'\1[REDACTED]',text)
    text=re.sub(r'(?:github_pat_|gh[pousr]_|sk-)[A-Za-z0-9_-]{15,}','[REDACTED]',text)
    text=re.sub(r'(?i)[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\n]+','<private-path>',text)
    text=re.sub(r'/(?:home|Users)/[^\s\n]+','<private-path>',text)
    return ''.join(c for c in text if c in '\n\t' or ord(c)>=32)


def emergency(root,component,exc):
    """One bounded fallback outside the primary tree, then minimal stderr.

    A different directory is not guaranteed to be a different physical disk.
    Failure of both locations is explicitly observable, never healthy.
    """
    record={'schema':'vdn.guard-emergency/1','state':'DIAGNOSTIC_UNAVAILABLE','component':component,'exception_type':type(exc).__name__,'message':redact(exc)[:1000],'primary_failed':False}
    try:
        name='guard-emergency-'+uuid.uuid4().hex+'.json';write(root,name,record);return safe(root,name)
    except (OSError,ValueError):record['primary_failed']=True
    try:
        folder=Path(tempfile.mkdtemp(prefix='eponge-emergency-',dir=tempfile.gettempdir()));p=folder/'incident.json'
        with p.open('x',encoding='utf-8') as stream:json.dump(record,stream);stream.flush();os.fsync(stream.fileno())
        return p
    except (OSError,ValueError):return None
    finally:
        try:sys.stderr.write(json.dumps({'state':'DIAGNOSTIC_UNAVAILABLE','component':component,'exception_type':type(exc).__name__,'primary_failed':True})+'\n');sys.stderr.flush()
        except (OSError,ValueError):pass


def exclusive(path):
    """Crash-released OS lock; no PID guessing or stale-lock deletion."""
    p=Path(path)
    if any(q.is_symlink() for q in (p,*p.parents)):raise ValueError('lock symlink refused')
    f=p.open('a+b')
    try:
        if os.name=='nt':
            import msvcrt
            if f.seek(0,2)==0:f.write(b'0');f.flush()
            f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BaseException:f.close();raise
    return f


def verify_code(root):
    m=read(root,'code-manifest.json')
    if m.get('schema')!='vdn.frozen-code/1' or not 1<=len(m['files'])<=1000:raise ValueError('invalid frozen code manifest')
    for name,h in m['files'].items():
        p=safe(root,'code/'+name)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('frozen code integrity failed')
    # No new executable file may hide outside the manifest.
    for folder in ('agent','scripts'):
        for p in safe(root,'code/'+folder).rglob('*.py'):
            if p.relative_to(safe(root,'code')).as_posix() not in m['files']:raise ValueError('unexpected executable code')
    return m


def gate(baseline,candidate):
    """Candidate data only. Code, tests, config, guard and reliable memory are denied."""
    baseline=Path(baseline);candidate=Path(candidate);changed=[]
    for p in candidate.rglob('*'):
        if p.is_symlink():raise ValueError('candidate symlink refused')
        if not p.is_file():continue
        name=p.relative_to(candidate).as_posix();old=safe(baseline,name)
        if old.exists() and hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(old.read_bytes()).digest():continue
        changed.append(name)
        if not name.startswith('lab/candidates/') or p.suffix not in ('.json','.md') or p.stat().st_size>64000:
            return {'state':'REJECTED','reason':'protected or non-allowlisted change','files':changed,'promoted':False}
    missing=[p.relative_to(baseline).as_posix() for p in baseline.rglob('*') if p.is_file() and not safe(candidate,p.relative_to(baseline).as_posix()).exists()]
    if missing:return {'state':'REJECTED','reason':'baseline file deleted','files':missing,'promoted':False}
    return {'state':'STAGED_REVIEW_REQUIRED','files':changed,'promoted':False,'reason':'data proposal only; no automated reliable-memory or code promotion'}


def terminate(child,grace=3):
    if child.poll() is not None:return
    if os.name=='nt':
        # Scoped to our still-live child; never enumerate or terminate other PIDs.
        subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],capture_output=True,timeout=5,shell=False)
    else:
        try:os.killpg(child.pid,signal.SIGTERM)
        except ProcessLookupError:return
    try:child.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        if os.name=='nt':child.kill()
        else:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        child.wait(timeout=3)


def drain(stream,output,failed):
    """Bounded redacted lines; drop oversized lines instead of leaking split secrets."""
    try:
        while True:
            line=stream.readline(8193)
            if not line:break
            if len(line)>8192:
                while line and not line.endswith(b'\n'):line=stream.readline(8193)
                text='[oversized child line omitted]\n'
            else:
                text=redact(line.decode('utf-8','replace'))
            output.write(text.encode('utf-8'));output.flush()
            if output.tell()>1_000_000:failed.set();return
    except (OSError,ValueError):failed.set()


def leased_worker(root,worker_id):
    """Transient companion owns the core child and observes the parent's pipe.

    EOF on supervisor death, a stalled pulse or a deadline stops only this child
    group. No service, reparented PID termination or automatic OS reboot restart.
    """
    root=Path(root);cfg=read(root,'mission.json',16000);verify_code(root)
    duration=cfg['duration_s'];timeout=cfg['heartbeat_timeout_s']
    if type(duration) is not int or not 1<=duration<=3600 or type(timeout) is not int or not 2<=timeout<=60:raise ValueError('invalid lease limits')
    lock=exclusive(safe(root,'worker.lock'));lost=threading.Event();pulse=[time.monotonic()];child=None;state='BLOCKED';born=time.monotonic()
    def watch_parent():
        try:
            # Raw descriptor read avoids a daemon holding BufferedReader's lock
            # during Python shutdown after a normally completed core.
            while os.read(sys.stdin.fileno(),1):pulse[0]=time.monotonic()
        finally:lost.set()
    def interrupted(*_):lost.set()
    signal.signal(signal.SIGTERM,interrupted)
    if hasattr(signal,'SIGINT'):signal.signal(signal.SIGINT,interrupted)
    threading.Thread(target=watch_parent,daemon=True).start()
    try:
        options={'start_new_session':True} if os.name!='nt' else {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP}
        child=subprocess.Popen([sys.executable,str(safe(root,'code/eponge.py')),'--workspace',str(root),'worker','--worker-id',worker_id],cwd=safe(root,'code'),stdin=subprocess.DEVNULL,shell=False,**options)
        write(root,'worker-lease.json',{'state':'RUNNING','wrapper_pid':os.getpid(),'worker_pid':child.pid,'worker_id':worker_id,'started_at':time.time()})
        while child.poll() is None:
            if lost.is_set() or time.monotonic()-pulse[0]>timeout:state='PARENT_LEASE_LOST';break
            if time.monotonic()-born>=duration:state='DEADLINE';break
            time.sleep(.05)
        if child.poll() is not None:state='STOPPED';return child.returncode
        return 2
    except BaseException as exc:
        emergency(root,'worker_lease',exc);raise
    finally:
        if child is not None:terminate(child,grace=1)
        try:write(root,'worker-lease.json',{'state':state,'worker_id':worker_id,'wrapper_pid':os.getpid(),'worker_pid':child.pid if child else None,'finished_at':time.time()})
        except (OSError,ValueError) as exc:emergency(root,'worker_lease_final',exc)
        lock.close()


def supervise(workspace):
    root=Path(workspace).absolute();cfg=read(root,'mission.json',16000)
    if cfg.get('schema')!='vdn.productive-mission/1' or cfg.get('enabled') is not True:raise PermissionError('mission not explicitly activated')
    duration=cfg['duration_s'];restart_limit=cfg['max_restarts'];heartbeat_timeout=cfg['heartbeat_timeout_s'];progress_timeout=cfg['progress_timeout_s']
    for value,lo,hi in ((duration,1,3600),(restart_limit,0,2),(heartbeat_timeout,2,60),(progress_timeout,5,600)):
        if type(value) is not int or not lo<=value<=hi:raise ValueError('invalid hard supervisor limit')
    guard=safe(root,'guard.lock');guard.parent.mkdir(parents=True,exist_ok=True)
    # OS releases this lock after a crash. Do not infer liveness from a PID file.
    try:f=exclusive(guard)
    except OSError:raise RuntimeError('a supervisor already owns this workspace')
    # Independent workspaces otherwise duplicate resource/HTTP allowances.
    # Serialize new supervised campaigns for this OS identity. This is not a
    # claim that copied sequential daily ledgers are globally reconciled.
    user=str(os.getuid()) if hasattr(os,'getuid') else os.environ.get('USERNAME','local-user')
    group=hashlib.sha256(user.encode()).hexdigest()[:16]
    try:shared=exclusive(Path(tempfile.gettempdir())/('eponge-supervisor-'+group+'.lock'))
    except (OSError,ValueError):
        f.close();raise RuntimeError('another supervised mission owns this OS user resource slot')
    started=time.time();deadline=time.monotonic()+duration;attempts=0;child=None;state='STOPPED';events=[]
    def event(kind,**values):
        row={'at':time.time(),'kind':kind,**values};events.append(row)
        try:write(root,'guard-events.json',{'schema':'vdn.guard-events/1','events':events[-200:]})
        except (OSError,ValueError) as exc:emergency(root,'supervisor_events',exc);raise
    try:
        while time.monotonic()<deadline:
            if attempts>restart_limit:event('CIRCUIT_OPEN');break
            verify_code(root);attempts+=1;worker_id=uuid.uuid4().hex
            env=dict(os.environ);env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1')
            log=safe(root,'guard-attempt-'+str(attempts)+'.log')
            with log.open('ab') as output:
                options={'start_new_session':True} if os.name!='nt' else {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP}
                child=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'leased-worker',str(root),worker_id],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=safe(root,'code'),env=env,shell=False,**options)
                logging_failed=threading.Event();reader=threading.Thread(target=drain,args=(child.stdout,output,logging_failed),daemon=True);reader.start()
                event('CHILD_STARTED',pid=child.pid,attempt=attempts);born=time.monotonic();last_integrity=born;state='RUNNING'
                while child.poll() is None:
                    try:child.stdin.write(b'.');child.stdin.flush()
                    except (BrokenPipeError,OSError):break
                    if time.monotonic()-last_integrity>5:verify_code(root);last_integrity=time.monotonic()
                    control=read(root,'control.json',2000).get('state')
                    if control=='STOPPED' or time.monotonic()>=deadline:state='STOPPED';terminate(child);break
                    try:
                        h=read(root,'reports/status.json',64000)
                        lease=read(root,'worker-lease.json',2000)
                        bound=h.get('worker_id')==worker_id and lease.get('worker_id')==worker_id and lease.get('wrapper_pid')==child.pid and h.get('worker_pid')==lease.get('worker_pid')
                        age=time.time()-h['last_heartbeat'] if bound else time.monotonic()-born
                        stuck=bound and time.time()-h['last_progress']>progress_timeout and h.get('activity')!='IDLE' and control!='PAUSED'
                        if bound and (age<0 or h['last_progress']>time.time()):age=heartbeat_timeout+1
                    except (OSError,ValueError,KeyError,TypeError):age=time.monotonic()-born;stuck=False
                    if age>heartbeat_timeout or stuck or logging_failed.is_set():
                        event('WATCHDOG_TIMEOUT',heartbeat_age_s=age,progress_stalled=stuck);terminate(child);state='STALE';break
                    write(root,'guard-status.json',{'schema':'vdn.guard-status/1','state':'PAUSED' if control=='PAUSED' else state,'guard_pid':os.getpid(),'worker_pid':child.pid,'worker_id':worker_id,'last_heartbeat':time.time(),'started_at':started,'attempts':attempts,'deadline_epoch':started+duration})
                    time.sleep(.2)
                reader.join(timeout=2)
                child.stdin.close()
            event('CHILD_EXIT',returncode=child.returncode,attempt=attempts)
            if child.returncode==0 or state=='STOPPED':break
            state='DEGRADED';time.sleep(min(2**(attempts-1),max(0,deadline-time.monotonic())))
        return 0 if state=='STOPPED' or child and child.returncode==0 else 1
    except BaseException as exc:
        # The independent journal remains usable even if the core/repair engine fails.
        state='BLOCKED';emergency(root,'supervisor',exc);event('GUARD_FAILURE',exception_type=type(exc).__name__);raise
    finally:
        if child is not None:terminate(child)
        try:write(root,'guard-status.json',{'schema':'vdn.guard-status/1','state':'STOPPED' if state not in ('BLOCKED','DEGRADED','STALE') else state,'last_heartbeat':time.time(),'guard_pid':os.getpid(),'started_at':started,'attempts':attempts,'finished_at':time.time()})
        except (OSError,ValueError) as exc:emergency(root,'supervisor_final',exc)
        finally:shared.close();f.close()


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True);q=s.add_parser('supervise');q.add_argument('workspace');q=s.add_parser('gate');q.add_argument('baseline');q.add_argument('candidate');q=s.add_parser('leased-worker');q.add_argument('workspace');q.add_argument('worker_id');a=p.parse_args()
    try:
        if a.command=='gate':
            r=gate(a.baseline,a.candidate);print(json.dumps(r));return 2 if r['state']=='REJECTED' else 0
        if a.command=='leased-worker':return leased_worker(a.workspace,a.worker_id)
        return supervise(a.workspace)
    except Exception as exc:
        print(json.dumps({'state':'BLOCKED','exception_type':type(exc).__name__,'operation':a.command}));return 2


if __name__=='__main__':raise SystemExit(main())
