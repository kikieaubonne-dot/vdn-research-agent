"""Acceptance rules on authored fixtures, never a real Blender/Internet claim."""
import importlib.util,sys,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from agent.forest_mission import judge


class SnowMissionRules(unittest.TestCase):
 def test_oversized_session_is_blocked_before_starting_collection(self):
  import shutil
  from tests.test_autonomy import make_root
  from agent.forest_mission import ForestWorker
  root=make_root();self.addCleanup(shutil.rmtree,root)
  # The normal12-call configuration cannot fit this one-off8-call grant.
  worker=SimpleNamespace(root=root,cfg={'allow_network':True,'max_http_calls':8})
  result=ForestWorker.research(worker)
  self.assertEqual(result['state'],'SESSION_DOES_NOT_FIT_MISSION_BUDGET');self.assertEqual(result['http_calls'],0);self.assertFalse((root/'lab').exists())
 def test_production_catalog_exposes_independent_snow_and_material_branches(self):
  import json,shutil
  from tests.test_autonomy import make_root
  from agent.research_roots import Roots
  root=make_root();self.addCleanup(shutil.rmtree,root)
  shutil.copytree(Path(__file__).resolve().parents[1]/'project',root/'project')
  tree=Roots(root)
  for branch in ('trunk','branches','snow','materials'):
   name='forest/spruce/'+branch
   self.assertEqual(tree.resolve('tree:'+name),name);self.assertEqual(tree.nodes[name]['parent'],'forest/spruce');self.assertEqual(tree.nodes[name]['status'],'PROPOSED')
  self.assertEqual(tree.resolve('tree:forest/wind'),'forest/wind')
 def inputs(self):
  generated={'rows':[]};imported={'rows':[]}
  for profile in ('primary','transfer'):
   for method in ('caps','procedural'):
    n=100 if method=='caps' else 60;generated['rows'].append({'profile':profile,'method':method,'triangles':n,'glb_bytes':500,'native_reference':{'white_faces':10,'green_faces':10}})
    imported['rows'].append({'profile':profile,'method':method,'triangles':n,'white_material_factor':method=='caps','needle_green_material_factor':True,'textures':[]})
  return generated,imported
 def test_cheaper_candidate_is_rejected_when_export_loses_snow(self):
  r=judge(*self.inputs());self.assertTrue(all(s['selected_for_next_engine_test']=='caps' for s in r['selection']));self.assertFalse(r['human_approved']);self.assertEqual(r['Roblox'],'NOT_TESTED');self.assertEqual(r['realism'],'INCONCLUSIVE')
 def test_failed_fallback_does_not_create_a_winner(self):
  a,b=self.inputs()
  for r in b['rows']:r['triangles']+=1
  r=judge(a,b);self.assertTrue(all(s['selected_for_next_engine_test'] is None for s in r['selection']))
 def test_unknown_texture_semantics_require_review(self):
  a,b=self.inputs()
  for r in b['rows']:r['textures']=['authored fixture']
  self.assertTrue(all(s['selected_for_next_engine_test'] is None for s in judge(a,b)['selection']))
 def test_snow_faces_point_up_for_normal_mask_comparison(self):
  spec=importlib.util.spec_from_file_location('snow_script_fixture',Path(__file__).resolve().parents[1]/'scripts/blender_snow_portability.py');module=importlib.util.module_from_spec(spec)
  with patch.dict(sys.modules,{'bpy':SimpleNamespace(),'mathutils':SimpleNamespace(Vector=object)}):spec.loader.exec_module(module)
  vertices=[(0,-1,0),(0,1,0),(1,-.5,-.2),(1,.5,-.2)];indices=module.ribbon_face(0);a,b,c=[vertices[i] for i in indices[:3]];u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)];normal_z=u[0]*v[1]-u[1]*v[0];self.assertGreater(normal_z,0)
 def test_no_export_loss_inferred_when_native_reference_has_no_green(self):
  a,b=self.inputs()
  for row in a['rows']:
   if row['method']=='procedural':row['native_reference']['green_faces']=0
  result=judge(a,b)
  for row in result['rows']:
   if row['method']=='procedural':self.assertEqual(row['state'],'INVALID_NATIVE_COMPARISON')
