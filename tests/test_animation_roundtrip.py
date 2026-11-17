"""Fixture trajectories are software checks, not real Blender validation."""
import copy,json,shutil,unittest
from unittest.mock import patch
from agent.animation_roundtrip import compare,trial
from tests.test_autonomy import make_root


def trajectory():
 return {'duration_s':2.,'samples':[{'fraction':i/24,'bones':{'hand':{'head':[0,i/24,0],'tail':[0,i/24,.1],'skin_matrix':[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]}},'meshes':{'handmesh':{'triangles':12,'min':[0,0,0],'max':[.1,.1,.1],'surface_centroid':[.05,.05,.05]}}} for i in range(25)]}


class AnimationGate(unittest.TestCase):
 def test_all_joints_surfaces_and_duration_preserved(self):
  a=trajectory();r=compare(a,copy.deepcopy(a));self.assertEqual(r['state'],'PASS');self.assertEqual(r['samples_compared'],25);self.assertFalse(r['human_approved']);self.assertEqual(r['Roblox'],'NOT_TESTED')
 def test_loss_between_original_three_sample_times_is_rejected(self):
  a=trajectory();b=copy.deepcopy(a);b['samples'][5]['bones']['hand']['head'][0]=.2
  self.assertIn('joint_trajectory_changed',compare(a,b)['errors'])
 def test_skin_deformation_loss_is_rejected_even_if_bones_match(self):
  a=trajectory();b=copy.deepcopy(a);b['samples'][9]['meshes']['handmesh']['max'][0]=.4
  self.assertIn('deformation_changed',compare(a,b)['errors'])
 def test_duration_missing_bones_and_extra_mesh_are_rejected(self):
  a=trajectory();b=copy.deepcopy(a);b['duration_s']=3;b['samples'][0]['bones']={};b['samples'][2]['meshes']['extra']=b['samples'][2]['meshes']['handmesh']
  r=compare(a,b);self.assertEqual(r['state'],'FAIL');self.assertIn('duration_changed',r['errors']);self.assertIn('missing_or_extra_bones',r['errors']);self.assertIn('missing_or_extra_meshes',r['errors'])
 def test_wrong_time_nan_topology_and_empty_samples_cannot_pass(self):
  a=trajectory();b=copy.deepcopy(a);b['samples'][2]['fraction']=.8;b['samples'][3]['meshes']['handmesh']['triangles']=13
  r=compare(a,b);self.assertIn('sample_time_changed',r['errors']);self.assertIn('topology_changed',r['errors'])
  b=copy.deepcopy(a);b['samples'][0]['bones']['hand']['tail'][0]=float('nan')
  with self.assertRaises(ValueError):compare(a,b)
  self.assertEqual(compare({'duration_s':0,'samples':[]},{'duration_s':0,'samples':[]})['state'],'FAIL')
 def test_plan_has_no_writes_and_exhausted_budget_starts_no_process(self):
  root=make_root();self.addCleanup(shutil.rmtree,root);source=root/'lab/inbox/learning/source.blend';source.parent.mkdir(parents=True);source.write_bytes(b'BLENDER fixture')
  from agent.learning_store import sha
  before={str(p):sha(p) for p in root.rglob('*') if p.is_file()}
  with patch('agent.animation_roundtrip.shutil.which',return_value=__file__):
   plan=trial(root,'lab/inbox/learning/source.blend','actor',license='OWN_CREATED',attest=True,trusted_copy=True)
  self.assertEqual(plan['state'],'PLANNED');self.assertEqual(before,{str(p):sha(p) for p in root.rglob('*') if p.is_file()})
  p=root/'lab/ocean/intelligence/compute.json';p.parent.mkdir(parents=True,exist_ok=True)
  import datetime as dt
  p.write_text(json.dumps({'date':dt.datetime.now(dt.timezone.utc).date().isoformat(),'reserved_s':60}));ledger=p.read_bytes()
  with patch('agent.animation_roundtrip.shutil.which',return_value=__file__),patch('agent.animation_roundtrip.run_tool',side_effect=AssertionError('quota bypass')):
   r=trial(root,'lab/inbox/learning/source.blend','actor',apply=True,license='OWN_CREATED',attest=True,trusted_copy=True)
  self.assertEqual(r['state'],'BLOCKED');self.assertEqual(p.read_bytes(),ledger)
 def test_unsafe_identity_and_untrusted_copy_refused(self):
  with self.assertRaises(PermissionError):trial('.', '../private.blend','actor',license='OWN_CREATED',attest=True)
  with self.assertRaises(ValueError):trial('.', '../private.blend','../actor',license='OWN_CREATED',attest=True,trusted_copy=True)
 def test_display_tail_is_not_a_skinning_transform_but_actual_transform_loss_fails(self):
  a=trajectory();b=copy.deepcopy(a);b['samples'][3]['bones']['hand']['tail'][2]+=.1
  r=compare(a,b);self.assertEqual(r['state'],'PASS');self.assertGreater(r['max_display_tail_error'],.09)
  b['samples'][3]['bones']['hand']['skin_matrix'][0]=.9
  self.assertIn('skin_transform_changed',compare(a,b)['errors'])
  del b['samples'][3]['bones']['hand']['skin_matrix']
  self.assertIn('missing_skin_transform',compare(a,b)['errors'])
 def test_pose_evidence_expansion_is_bounded_and_original_remains(self):
  import gzip,tempfile
  from pathlib import Path
  from agent.animation_roundtrip import load_samples
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'oversized.gz';p.write_bytes(gzip.compress(b' '*1000001))
   with self.assertRaises(ValueError):load_samples(Path(d),'oversized.gz')
   self.assertTrue(p.exists())
 def test_failed_trial_receipt_also_reaches_blackbox(self):
  from agent.reliability import BlackBox
  root=make_root();self.addCleanup(shutil.rmtree,root);p=root/'lab/inbox/learning/actor.blend';p.parent.mkdir(parents=True);p.write_bytes(b'BLENDER fixture')
  a=trajectory();bad=copy.deepcopy(a);bad['samples'][6]['bones']['hand']['head'][0]=.3
  with patch('agent.animation_roundtrip.shutil.which',return_value=__file__),patch('agent.animation_roundtrip.load_samples',side_effect=[a,a,bad]),patch('agent.animation_roundtrip.run_tool',return_value={'exit_code':0,'elapsed_s':0}):
   r=trial(root,'lab/inbox/learning/actor.blend','hand',apply=True,license='OWN_CREATED',attest=True,trusted_copy=True)
  self.assertEqual(r['state'],'FAIL');self.assertTrue(BlackBox(root).incidents())
