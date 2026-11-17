"""Policies and structural checks on authored inputs, no real Blender assertion."""
import gzip,json,shutil,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
from agent.learning_assets import gltf_dependencies,inspect,roundtrip
from agent.learning_compact import pack,compact
from agent.learning_store import receipt,get,sha
from tests.test_autonomy import make_root

class AssetPolicies(unittest.TestCase):
 def setUp(self):self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.input=self.root/'lab/inbox/fixture';self.input.mkdir(parents=True)
 def test_remote_and_traversal_gltf_dependencies_are_refused(self):
  p=self.input/'scene.gltf'
  for uri in ('https://example.com/secret.bin','../secret.bin','%2e%2e/secret.bin','file:///etc/passwd','C:\\private.bin'):
   p.write_text(json.dumps({'buffers':[{'uri':uri}]}))
   with self.assertRaises(ValueError):gltf_dependencies(p)
 def test_local_dependency_hash_and_cache_obsolescence(self):
  f=self.input/'mesh.bin';f.write_bytes(b'AUTHORED mesh');p=self.input/'scene.gltf';p.write_text(json.dumps({'buffers':[{'uri':'mesh.bin'}]}));self.assertEqual(gltf_dependencies(p)[0]['sha256'],sha(f))
  folder='lab/learning/assets/'+'e'*64;(self.root/folder).mkdir(parents=True);receipt(self.root,folder,{'spec':{'input':'lab/inbox/fixture/scene.gltf','input_sha256':sha(p),'extra_inputs':{'lab/inbox/fixture/mesh.bin':sha(f)}}});f.write_bytes(b'CHANGED');self.assertTrue(get(self.root,folder)['inputs_obsolete'])
 def test_untrusted_or_unlicensed_copy_never_reaches_blender(self):
  p=self.input/'a.blend';p.write_bytes(b'BLENDER authored')
  with self.assertRaises(PermissionError):inspect(self.root,'lab/inbox/fixture/a.blend','OWN_CREATED',True,False)
 def test_geometry_only_cannot_accept_missing_rig_animation(self):
  a={'inspection':{'objects':[{'name':'x','triangles':12}],'armatures':[{'name':'rig'}],'actions':[{'name':'gesture'}]}}
  b={'inspection':{'objects':[{'name':'x','triangles':12}],'armatures':[],'actions':[]}}
  r=roundtrip(a,b);self.assertEqual(r['state'],'FAIL');self.assertIn('rig_missing',r['issues']);self.assertIn('animation_missing',r['issues']);self.assertFalse(r['human_approved'])
 def test_compaction_reconstructs_every_original_byte(self):
  original=b'BLENDER'+b'AUTHORED REPEATED NATIVE CONTENT '*500
  compressed=pack(original);self.assertLess(len(compressed),len(original));self.assertEqual(gzip.decompress(compressed),original)
 def test_compaction_refuses_other_formats_and_nonowned_paths(self):
  with self.assertRaises(ValueError):pack(b'AUTHORED non-blend')
  with self.assertRaises(PermissionError):compact(self.root,'knowledge/private.blend',True)
  with self.assertRaises(PermissionError):compact(self.root,'lab/inbox/learning/a.blend',False)

 def test_local_tool_logs_preserve_existing_secret_redaction(self):
  import sys
  from agent.learning_store import run_tool
  run_tool(self.root,[sys.executable,'-c','print(\'{"token":"PRIVATE_LEARNING_LOG"}\')'],'lab/learning/test/log.txt',timeout=3)
  self.assertNotIn('PRIVATE_LEARNING_LOG',(self.root/'lab/learning/test/log.txt').read_text())

 def test_bone_display_helper_is_not_delivered_geometry_and_not_name_based(self):
  import importlib.util,sys
  from types import SimpleNamespace as NS
  script=Path(__file__).resolve().parents[1]/'scripts/blender_inspect_learning.py';spec=importlib.util.spec_from_file_location('asset_helper_fixture',script);module=importlib.util.module_from_spec(spec)
  with patch.dict(sys.modules,{'bpy':NS()}):spec.loader.exec_module(module)
  hidden=NS(name='arbitrary-rig-widget',type='MESH',hide_render=True);real=NS(name='Icosphere',type='MESH',hide_render=False)
  rig=NS(name='rig',type='ARMATURE',pose=NS(bones=[NS(name='joint',custom_shape=hidden)]))
  found=module.display_helpers(NS(objects=[rig,hidden,real]))
  self.assertIn('arbitrary-rig-widget',found);self.assertNotIn('Icosphere',found)
