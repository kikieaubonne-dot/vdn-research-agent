"""Preregistered geometry acceptance; fixtures never count as Blender execution."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent.forest_lab import specification,evaluate,run


class ForestAcceptanceTests(unittest.TestCase):
    def fixture(self):
        plan=specification('4.3.2');g={'phase':'generate','blender_version':'4.3.2','rows':[]};r={'phase':'verify','blender_version':'4.3.2','rows':[]}
        for asset,triangles in (('spruce',816),('shrub',688)):
            for variant,depth in (('A',0),('B',.2)):
                g['rows'].append({'asset':asset,'variant':variant,'capture_exists':True,'metrics':{'triangles':triangles,'branch_count':48 if asset=='spruce' else 40,'mean_branch_depth_m':depth}})
                r['rows'].append({'asset':asset,'variant':variant,'reopened':{'triangles':triangles},'obj_imported':{'triangles':triangles}})
        return plan,g,r

    def test_success_of_geometry_never_means_artistic_or_game_success(self):
        p,g,r=self.fixture();v=evaluate(p,g,r)
        self.assertEqual(v['geometry_conclusion'],'PASS')
        self.assertEqual(v['artistic_conclusion'],'INCONCLUSIVE')
        self.assertEqual(v['Roblox_conclusion'],'BLOCKED')
        self.assertNotIn('winner',v)

    def test_extra_geometry_fails_fixed_budget_hypothesis(self):
        p,g,r=self.fixture();g['rows'][1]['metrics']['triangles']+=20
        self.assertEqual(evaluate(p,g,r)['geometry_conclusion'],'FAIL')

    def test_export_or_reload_loss_is_a_failure(self):
        p,g,r=self.fixture();r['rows'][2]['obj_imported']['triangles']-=1
        self.assertEqual(evaluate(p,g,r)['geometry_conclusion'],'FAIL')

    def test_no_new_depth_is_negative_result(self):
        p,g,r=self.fixture();g['rows'][1]['metrics']['mean_branch_depth_m']=0
        self.assertEqual(evaluate(p,g,r)['rows'][0]['conclusion'],'FAIL')

    def test_missing_capture_cannot_validate_the_run(self):
        p,g,r=self.fixture();g['rows'][1]['capture_exists']=False
        self.assertEqual(evaluate(p,g,r)['geometry_conclusion'],'FAIL')

    def test_missing_transfer_arm_or_version_conflict_is_rejected(self):
        p,g,r=self.fixture()
        with self.assertRaises(ValueError):evaluate(p,g,{**r,'rows':r['rows'][:-1]})
        with self.assertRaises(ValueError):evaluate(p,g,{**r,'blender_version':'5.2'})

    def test_explicit_capability_required_before_any_engine_probe(self):
        with tempfile.TemporaryDirectory() as d,patch('agent.forest_lab.subprocess.run') as probe:
            with self.assertRaises(PermissionError):run(Path(d))
            probe.assert_not_called()

    def test_render_configuration_disables_unavailable_optional_denoiser(self):
        import importlib.util
        import sys
        from types import SimpleNamespace as NS
        script=Path(__file__).resolve().parents[1]/'scripts/blender_forest_ab.py'
        spec=importlib.util.spec_from_file_location('forest_driver_fixture',script)
        module=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,{'bpy':NS(),'mathutils':NS(Vector=object)}):spec.loader.exec_module(module)
        layer=NS(cycles=NS(use_denoising=True))
        scene=NS(cycles=NS(device='GPU',samples=999,use_denoising=True),render=NS(image_settings=NS()),view_layers=[layer])
        module.configure_render(scene,specification('4.3.2')['controls'])
        self.assertFalse(scene.cycles.use_denoising)
        self.assertFalse(layer.cycles.use_denoising)
        self.assertEqual(scene.cycles.device,'CPU')
        self.assertEqual(scene.render.threads,1)
