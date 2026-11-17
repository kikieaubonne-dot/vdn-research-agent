"""Starter boundaries and runtime continuity; no Windows/Studio validation."""
import hashlib,importlib.util,json,shutil,sqlite3,tempfile,unittest
from pathlib import Path
from tests.test_autonomy import make_root

REPO=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('starter_windows_setup',REPO/'PROLOGUE_START_NOW/WINDOWS/setup.py')
SETUP=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(SETUP)


class StartNowChecks(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.source=self.root/'Eponge/source';self.source.mkdir(parents=True);self.file=self.source/'original.py';self.file.write_text('ORIGINAL source')
 def manifest(self,files):
  value={'files':{p.relative_to(self.root).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}};(self.root/'MANIFEST.json').write_text(json.dumps(value))
 def test_original_source_mutation_and_missing_file_fail(self):
  self.manifest([self.file]);self.assertEqual(SETUP.verify(self.root)['state'],'PASS');self.file.write_text('changed');self.assertEqual(SETUP.verify(self.root)['state'],'FAIL');self.file.unlink();self.assertEqual(SETUP.verify(self.root)['state'],'FAIL')
 def test_derived_index_change_is_explicit_and_never_waives_source_changes(self):
  p=self.root/'Eponge/runtime/output/knowledge.db';p.parent.mkdir(parents=True)
  with sqlite3.connect(p) as db:db.execute('CREATE TABLE fixture (value TEXT)')
  self.manifest([self.file,p])
  with sqlite3.connect(p) as db:db.execute("INSERT INTO fixture VALUES ('changed derived cache')")
  r=SETUP.verify(self.root);self.assertEqual(r['state'],'PASS');self.assertEqual(r['derived_cache_changes'],['Eponge/runtime/output/knowledge.db'])
  self.file.write_text('changed source');self.assertEqual(SETUP.verify(self.root)['state'],'FAIL')
 def test_corrupt_cache_and_traversal_are_not_accepted(self):
  p=self.root/'Eponge/runtime/output/knowledge.db';p.parent.mkdir(parents=True);p.write_bytes(b'fixture before');self.manifest([p]);p.write_bytes(b'corrupt after');self.assertEqual(SETUP.verify(self.root)['state'],'FAIL')
  (self.root/'MANIFEST.json').write_text(json.dumps({'files':{'../../private':{'sha256':'x'}}}))
  with self.assertRaises(ValueError):SETUP.verify(self.root)
 def test_symlink_manifest_and_parent_are_refused(self):
  target=self.root/'real';target.mkdir();file=target/'f';file.write_text('owned fixture');link=self.root/'linked'
  try:link.symlink_to(target,target_is_directory=True)
  except (OSError,NotImplementedError):self.skipTest('OS denies symlink creation; no claim for this platform')
  (self.root/'MANIFEST.json').write_text(json.dumps({'files':{'linked/f':{'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}}}))
  with self.assertRaises(ValueError):SETUP.verify(self.root)
  (self.root/'MANIFEST.json').unlink();(self.root/'MANIFEST.json').symlink_to(file)
  with self.assertRaises(ValueError):SETUP.verify(self.root)
 def test_non_windows_configuration_does_not_invent_a_windows_path(self):
  from unittest.mock import patch
  with patch.object(SETUP.sys,'platform','linux'):self.assertEqual(SETUP.config_candidate(self.root)['state'],'BLOCKED')
  self.assertFalse(list(self.root.glob('*config*.json')))
 def test_mcp_launch_refuses_modified_bundle_before_spawning(self):
  from unittest.mock import patch
  server=self.source/'vdn_mcp.py';server.write_text('OWNED fixture, never executed')
  data=self.root/'Eponge/runtime/project/prologue.json';data.parent.mkdir(parents=True);data.write_text('{}')
  self.manifest([self.file,server,data]);server.write_text('CORRUPTED fixture')
  with patch.object(SETUP.subprocess,'run',side_effect=AssertionError('must not execute corrupt source')):
   with self.assertRaisesRegex(ValueError,'bundle integrity'):SETUP.test_mcp(self.root)


class SeedContinuity(unittest.TestCase):
 def test_new_mission_keeps_existing_learning_receipts_and_staged_artifacts(self):
  from agent.mission import initialize
  root=make_root();self.addCleanup(shutil.rmtree,root)
  shutil.copytree(REPO/'agent',root/'agent',ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(REPO/'scripts',root/'scripts',ignore=shutil.ignore_patterns('__pycache__'))
  for name in ('eponge.py','vdn_mcp.py'):shutil.copyfile(REPO/name,root/name)
  shutil.copytree(REPO/'project',root/'project');(root/'knowledge').mkdir();(root/'output').mkdir()
  import datetime as dt
  (root/'output/queue.json').write_text(json.dumps({'version':2,'daily':{'date':dt.datetime.now(dt.timezone.utc).date().isoformat(),'items':0,'fetch':5,'http_calls':9},'items':{}}))
  seed=make_root();self.addCleanup(shutil.rmtree,seed);(seed/'output').mkdir();shutil.copyfile(root/'output/queue.json',seed/'output/queue.json')
  files=['lab/learning/animation/fixture/result.json','lab/inbox/learning/fixture/baked.blend']
  for name in files:
   p=seed/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('OWNED fixture '+name)
  source_only=root/'lab/learning/source-only.json';source_only.parent.mkdir(parents=True,exist_ok=True);source_only.write_text('OWNED source fixture')
  compute=seed/'lab/ocean/intelligence/compute.json';compute.parent.mkdir(parents=True);compute.write_text(json.dumps({'date':dt.datetime.now(dt.timezone.utc).date().isoformat(),'reserved_s':77.058}))
  destination=self.root_if_unused(root)
  result=initialize(destination,root,seed);self.assertEqual(result['state'],'PREPARED_DISABLED')
  for name in files:self.assertEqual((destination/'runtime'/name).read_bytes(),(seed/name).read_bytes())
  self.assertEqual((destination/'runtime/lab/learning/source-only.json').read_bytes(),source_only.read_bytes())
  self.assertEqual((destination/'runtime/lab/ocean/intelligence/compute.json').read_bytes(),compute.read_bytes())
 @staticmethod
 def root_if_unused(source):return source/'sandbox-mission'
