"""Mocked Ollama contract only; no actual vision model is evaluated here."""
import io,json,shutil,threading,unittest
from unittest.mock import patch
from agent import intelligence_models as im
from agent.learning_store import receipt,sha
from agent.learning_vision import analyze,validate
from tests.test_autonomy import make_root


class VisionContract(unittest.TestCase):
 def setUp(self):
  self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.key='b'*64;self.folder='lab/learning/media/'+self.key;p=self.root/self.folder;p.mkdir(parents=True);image=p/'frame.png';image.write_bytes(b'\x89PNG\r\n\x1a\nAUTHORED fixture, not real model input');self.frame=sha(image)
  receipt(self.root,self.folder,{'spec':{},'frames':[{'asset':'frame.png','sha256':self.frame,'observed_pts_s':1.25}]})
  self.requests=[]
 def enable(self):
  (self.root/'config/intelligence.json').write_text(json.dumps({**im.DEFAULT,'enabled':True,'compact_model':'fixture:vision'}));p=self.root/'config/v10.json';v=json.loads(p.read_text());v['models']['local'].update(enabled=True,vision=True,model='fixture:vision');p.write_text(json.dumps(v))
 def opener(self,req,**kwargs):
  self.requests.append(req.full_url);path=req.full_url.rsplit('/',1)[-1]
  if path=='tags':r={'models':[{'name':'fixture:vision','digest':'AUTHORED-DIGEST'}]}
  elif path=='show':r={'capabilities':['vision']}
  elif path=='version':r={'version':'MOCK-SERVICE'}
  elif path=='generate':
   data=json.loads(req.data);self.assertFalse(data['stream']);self.assertEqual(data['keep_alive'],0);self.assertEqual(data['options']['num_gpu'],0);self.assertEqual(len(data['images']),1)
   r={'done':True,'response':json.dumps({'observations':[],'uncertainties':['Authored abstention fixture, no visual inference performed.']}),'eval_count':10}
  else:raise AssertionError(path)
  class Response(io.BytesIO):
   def __enter__(self):return self
   def __exit__(self,*args):self.close()
  return Response(json.dumps(r).encode())
 def call(self,**kwargs):return analyze(self.root,self.key,self.frame,'fixture:vision',**kwargs)
 def test_plan_and_unconfigured_fallback_never_open_socket(self):
  self.assertEqual(self.call(opener=self.opener)['state'],'PLANNED');self.assertFalse(self.requests)
  self.assertEqual(self.call(apply=True,allow_model=True,opener=self.opener)['state'],'BLOCKED_NOT_CONFIGURED');self.assertFalse(self.requests)
 def test_mock_installed_capability_and_json_are_not_truth(self):
  self.enable();r=self.call(apply=True,allow_model=True,opener=self.opener)
  self.assertEqual(r['state'],'MODEL_PERCEPTION_UNVERIFIED');self.assertFalse(r['truth_verified']);self.assertFalse(r['human_approved']);self.assertFalse(r['source_supported_claims']);self.assertEqual(r['observed_pts_s'],1.25);self.assertEqual(len(self.requests),4)
  next=self.call(apply=True,allow_model=True,opener=self.opener);self.assertTrue(next['cache_hit']);self.assertEqual(next['model_calls_this_run'],0);self.assertEqual(sum(x.endswith('/generate') for x in self.requests),1)
 def test_missing_service_and_cancellation_fall_back_without_success(self):
  self.enable()
  with patch('agent.learning_vision.im.Ollama.inventory',side_effect=OSError('authored unavailable')):r=self.call(apply=True,allow_model=True)
  self.assertEqual(r['state'],'DETERMINISTIC_FALLBACK');self.assertFalse(r['observations'])
  flag=threading.Event();flag.set();r=self.call(apply=True,allow_model=True,opener=self.opener,cancel=flag);self.assertEqual(r['reason_type'],'InterruptedError');self.assertFalse(self.requests)
 def test_model_not_installed_or_not_vision_does_not_generate(self):
  self.enable()
  with patch('agent.learning_vision.im.Ollama.inventory',return_value=[]):self.assertEqual(self.call(apply=True,allow_model=True)['state'],'DETERMINISTIC_FALLBACK')
  with patch('agent.learning_vision.im.Ollama.request',return_value={'capabilities':[]}),patch('agent.learning_vision.im.Ollama.inventory',return_value=[{'name':'fixture:vision','digest':'d'}]):self.assertEqual(self.call(apply=True,allow_model=True)['state'],'DETERMINISTIC_FALLBACK')
 def test_model_cannot_add_commands_approvals_or_unbounded_claims(self):
  for data in ({'observations':[],'uncertainties':['unknown'],'tools':['execute']},{'observations':[],'uncertainties':[]},{'observations':[{'description':'x','screen_parameters':[{'label':'parameter','literal_value':'50','verified':True}]}],'uncertainties':['unknown']}):
   with self.assertRaises(ValueError):validate(data)
 def test_rights_permission_path_and_edited_evidence_fail_before_model(self):
  with self.assertRaises(PermissionError):self.call(apply=True)
  with self.assertRaises(ValueError):analyze(self.root,'../../private',self.frame,'fixture:vision')
  (self.root/self.folder/'frame.png').write_bytes(b'changed')
  with self.assertRaises(ValueError):self.call(apply=True,allow_model=True,opener=self.opener)
