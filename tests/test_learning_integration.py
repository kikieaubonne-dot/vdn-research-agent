"""Authored software cases; real Blender/video evidence is reported separately."""
import copy,json,math,shutil,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_autonomy import make_root
from agent.learning_assets import compare_poses
from agent.learning_discovery import evaluate,record
from agent.learning_store import receipt,sha
from agent.project_api import ProjectAPI


class LearningIntegration(unittest.TestCase):
 def setUp(self):
  self.root=make_root();self.addCleanup(shutil.rmtree,self.root)
  self.key='d'*64;self.folder='lab/learning/media/'+self.key;(self.root/self.folder).mkdir(parents=True)
  receipt(self.root,self.folder,{'key':self.key,'state':'PARTIAL','spec':{},'frames':[],'vision':{'state':'NOT_TESTED'},'truth_verified':False})
 def test_read_only_existing_tools_do_not_call_model_or_write(self):
  q='learning:media:'+self.key;api=ProjectAPI(self.root,True)
  before={str(p):sha(p) for p in self.root.rglob('*') if p.is_file()}
  with patch('agent.intelligence_models.operation',side_effect=AssertionError('read must not consume compute')):
   r=api.synthesize_technical(q);b=api.get_intelligence_brief(q,500)
  self.assertFalse(r['facts']);self.assertFalse(r['truth_verified']);self.assertTrue(b['read_only']);self.assertTrue(b['omitted_detail'])
  self.assertLessEqual(len(json.dumps(b,ensure_ascii=False)),2000)
  self.assertEqual(before,{str(p):sha(p) for p in self.root.rglob('*') if p.is_file()})
  for args in ({'apply':True},{'allow_model':True}):
   with self.assertRaises(PermissionError):api.synthesize_technical(q,**args)
 def test_bad_identity_and_corruption_are_not_silent_fallbacks(self):
  api=ProjectAPI(self.root)
  for q in ('learning:media:../../private','learning:unknown:'+self.key,'learning:media:'+self.key.upper()):
   with self.assertRaises(ValueError):api.synthesize_technical(q)
  (self.root/self.folder/'result.json').write_text('{}')
  with self.assertRaises((KeyError,ValueError)):api.get_intelligence_brief('learning:media:'+self.key)
 def test_actual_stdio_process_preserves_27_tools_and_reads_evidence(self):
  from agent.mcp_v8 import Server
  q='learning:media:'+self.key
  messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'learning-test','version':'1'}}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'}]
  calls=[('get_intelligence_brief',{'question':q,'token_budget':500}),('synthesize_technical',{'question':q}),('synthesize_technical',{'question':q,'apply':True})]
  messages += [{'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':n,'arguments':a}} for i,(n,a) in enumerate(calls,3)]
  repo=Path(__file__).resolve().parents[1]
  p=subprocess.run([sys.executable,str(repo/'vdn_mcp.py'),'--root',str(self.root),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,encoding='utf-8',capture_output=True,timeout=30,cwd=self.root)
  self.assertEqual(p.returncode,0,p.stderr);out=[json.loads(x) for x in p.stdout.splitlines()]
  self.assertEqual(len(out[1]['result']['tools']),27);self.assertEqual(out[1]['result']['tools'],Server(self.root,v111=True).tools)
  self.assertFalse(out[2]['result'].get('isError'));self.assertFalse(out[3]['result'].get('isError'));self.assertTrue(out[4]['result']['isError'])
  self.assertFalse(out[2]['result']['structuredContent']['truth_verified'])
 def test_pose_gate_detects_lost_constraint_despite_existing_animation(self):
  def report(y):return {'inspection':{'pose_samples':[{'fraction':f,'rigs':[{'name':'actor','bones':[{'name':'hand','head':[0,y if f==.5 else 0,0]}]}]} for f in (0,.5,1)]}}
  r=compare_poses(report(.28),report(0),'actor','hand',1e-5)
  self.assertEqual(r['state'],'FAIL');self.assertIn('pose_changed_at_0.5',r['issues'])
  self.assertEqual(compare_poses(report(.28),report(.28),'actor','hand',1e-5)['state'],'PASS')
  self.assertFalse(r['human_approved'])
 def test_missing_and_nonfinite_pose_cannot_pass(self):
  empty={'inspection':{'pose_samples':[]}}
  self.assertEqual(compare_poses(empty,empty,'actor','hand',0)['state'],'FAIL')
  with self.assertRaises(ValueError):compare_poses(empty,empty,'actor','hand',math.nan)
 def test_discovery_requires_transfer_and_preserves_regression(self):
  c={'metric':'bytes','direction':'min','minimum_gain':1,'maximum_candidate':None}
  t={'case':'first','baseline':100,'candidate':40,'scope':'primary'}
  self.assertEqual(evaluate([t],c)['state'],'PARTIAL')
  self.assertEqual(evaluate([t,{**t,'scope':'transfer'}],c)['state'],'ADOPTED_IN_LAB')
  self.assertEqual(evaluate([t,{**t,'scope':'transfer','candidate':101}],c)['state'],'REJECTED_IN_LAB')
  with self.assertRaises(ValueError):evaluate([{**t,'candidate':math.nan}],c)
 def test_immutable_discovery_reuse_and_evidence_invalidation(self):
  path='lab/inbox/learning/observation.json';p=self.root/path;p.parent.mkdir(parents=True);p.write_text('{"observed":true}')
  methods=[{'id':str(i),'method':'authored fixture','tool':'fixture','version':'1','license':'OWN_CREATED','dependencies':[],'cost':'unknown','safety':'data only','status':'TESTED_FIXTURE'} for i in (0,1)]
  args=(self.root,'objective','precise gap',methods,[{'case':'primary','baseline':100,'candidate':50,'scope':'primary'}],{'metric':'bytes','direction':'min','minimum_gain':1,'maximum_candidate':None},[path],['Not a real tool test'])
  r=record(*args);self.assertFalse(r['verified']);self.assertFalse(r['automatic_tool_search']);self.assertTrue(record(*args)['cache_hit'])
  api=ProjectAPI(self.root);q='learning:discovery:'+r['key'];self.assertFalse(api.synthesize_technical(q)['laboratory_evidence']['inputs_obsolete'])
  p.write_text('{"observed":false}');self.assertTrue(api.synthesize_technical(q)['laboratory_evidence']['inputs_obsolete'])
 def test_asset_consultation_retains_failed_comparison_even_in_small_brief(self):
  from agent.learning_store import save
  name='lab/inbox/learning/actor.glb';p=self.root/name;p.parent.mkdir(parents=True);p.write_bytes(b'authored GLB fixture')
  key='a'*64;folder='lab/learning/assets/'+key;(self.root/folder).mkdir(parents=True)
  save(self.root,folder+'/inspection.json',{'blender_version':'FIXTURE','triangles':10})
  receipt(self.root,folder,{'key':key,'state':'PARTIAL','inspection_file':'inspection.json','spec':{'input':name,'input_sha256':sha(p)}})
  methods=[{'id':str(i),'method':'fixture','tool':'fixture','version':'1','license':'OWN_CREATED','dependencies':[],'cost':'fixture','safety':'data only','status':'FIXTURE'} for i in (0,1)]
  record(self.root,'goal','gap',methods,[{'case':'fixture','baseline':0,'candidate':.4,'scope':'primary'}],{'metric':'pose error','direction':'min','minimum_gain':0,'maximum_candidate':1e-5},[name],['FIXTURE, not engine evidence'])
  api=ProjectAPI(self.root);q='learning:asset:'+key
  r=api.synthesize_technical(q)['laboratory_evidence'];self.assertEqual(r['related_method_comparisons'][0]['state'],'REJECTED_IN_LAB')
  b=api.get_intelligence_brief(q,500);self.assertIn('REJECTED_IN_LAB',json.dumps(b));self.assertLessEqual(len(json.dumps(b,ensure_ascii=False)),2000)
 def test_isolated_obsidian_export_idempotence_and_rollback(self):
  from agent.obsidian import sync,rollback
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   pages={'knowledge/_VDN-learning/media.md':'# Laboratory PARTIAL\nNo observed UI action; original media only.\n'}
   self.assertEqual(sync(self.root,d,extra_pages=pages)['state'],'simulation')
   result=sync(self.root,d,apply=True,extra_pages=pages);self.assertEqual(result['state'],'committed')
   self.assertEqual(sync(self.root,d,apply=True,extra_pages=pages)['state'],'unchanged')
   self.assertEqual(rollback(d,result['transaction'],apply=True)['state'],'rolled_back')
   self.assertFalse((Path(d)/'knowledge/_VDN-learning/media.md').exists())
