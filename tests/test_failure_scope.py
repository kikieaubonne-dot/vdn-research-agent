"""Failure scope is not universal disproof. No engine or game is executed here."""
from pathlib import Path
import unittest
from unittest.mock import patch

from agent.lab_store import LabStore
from agent.project import Bible
from agent.project_work import Project
from agent.research_roots import Roots
from tests import test_operations as previous


class FailureScopeTests(unittest.TestCase):
    setUp=previous.RecoveryTests.setUp

    def record_failure(self,assets):
        lab=LabStore(self.root)
        r=lab.create('AUTHORED failing renderer fixture','same branch geometry fixture','rendering engine might lack an optional capability',parameters={'project_task':'trees','research_branch':'forest/spruce'},environment={'engine':'Blender','blender_version':'4.3.2','asset_ids':assets},protocol={})
        lab.transition(r['id'],'PLANNED');lab.transition(r['id'],'RUNNING')
        return lab.record_result(r['id'],'FAILED',{},['AUTHORED isolated renderer unavailable'],errors=['Optional denoiser unavailable'])

    def test_known_other_assets_do_not_block_all_B3_C1_preparation(self):
        baseline=Project(self.root).synthesize('trees')['quality']['readiness']
        failed=self.record_failure(['generated-fixture-spruce'])
        q=Project(self.root).synthesize('trees')['quality']
        self.assertEqual(q['readiness'],baseline)
        self.assertNotEqual(q['readiness'],'READY')
        self.assertFalse(q['failures'])
        self.assertIn(failed['id'],[r['id'] for r in q['other_context_failures']])
        gap=Roots(self.root).assess('forest/spruce')
        self.assertNotIn(failed['id'],gap['failures'])
        self.assertIn(failed['id'],gap['other_context_failures'])
        self.assertEqual(LabStore(self.root).get(failed['id'])['status'],'FAILED')

    def test_missing_asset_context_remains_conservatively_blocked(self):
        self.record_failure([])
        self.assertEqual(Project(self.root).synthesize('trees')['quality']['readiness'],'BLOCKED')

    def test_failure_on_target_assets_still_blocks(self):
        self.record_failure(Bible(self.root).task('trees')['assets'])
        self.assertEqual(Project(self.root).synthesize('trees')['quality']['readiness'],'BLOCKED')

    def test_other_asset_failure_still_forbids_identical_failed_method_retry(self):
        from agent.project_api import ProjectAPI
        record=self.record_failure(['generated-fixture-spruce'])
        with self.assertRaises(ValueError):
            ProjectAPI(self.root,allow_experiments=True).prepare_experiment(record['problem'],record['technique'],record['hypothesis'],parameters=record['parameters'],environment=record['environment'],protocol=record['protocol'])

    def test_quality_code_version_invalidates_previous_card_cache(self):
        p=Project(self.root);card=p.synthesize('trees',True)
        with patch('agent.project_work.VERSION','future-reviewed-quality-version'):
            self.assertTrue(p.get(card['key'])['inputs_obsolete'])

    def test_uncertain_or_noncanonical_asset_labels_cannot_hide_a_failure(self):
        from agent.project_quality import failure_applies_to_assets
        task={'assets':['B3','C1']}
        for assets in (['Unknown'],[' UNKNOWN '],['inconnu'],[' N/A '],[' b3 '],['c1']):
            with self.subTest(assets=assets):
                record={'environment':{'asset_ids':assets}}
                self.assertTrue(failure_applies_to_assets(record,task))
        self.assertFalse(failure_applies_to_assets({'environment':{'asset_ids':['generated-shrub']}},task))
