"""Continuity regressions: authored reports are not real engine experiments."""
import json,shutil,unittest
from pathlib import Path
from tests.test_autonomy import make_root
from tests import test_project as fixtures
from agent.project_work import Project,preparation_archive
from agent.lab_store import LabStore

class ContinuityTests(unittest.TestCase):
 def setUp(self):
  self.root=make_root();self.addCleanup(shutil.rmtree,self.root)
  shutil.copytree(Path(__file__).parent/'fixtures/project',self.root/'project');self.project=Project(self.root)
 def publish_only(self):
  fixtures.ProjectTests.seed(self)
  card=self.project.synthesize('collisions')
  (self.root/'project/prepared.json').write_text(json.dumps(preparation_archive([card])),encoding='utf-8')
  # A separate clone has the publication but no original receipt or private card.
  clone=make_root();self.addCleanup(shutil.rmtree,clone);shutil.copytree(self.root/'project',clone/'project')
  self.root=clone;self.project=Project(clone);return card
 def failure(self):
  lab=LabStore(self.root);r=lab.create('Authored unrelated title','fixture failed method','unknown',{'project_task':'collisions'},{'engine':'Python','project_task':'collisions'})
  lab.transition(r['id'],'PLANNED');lab.transition(r['id'],'RUNNING')
  return lab.record_result(r['id'],'FAILED',{},['AUTHORED SOFTWARE TEST; no Roblox execution'],errors=['fixture blocked path'])
 def test_archive_brief_abstains_without_originals(self):
  self.publish_only();brief=self.project.brief('collisions')
  self.assertTrue(brief['abstained_from_established_facts']);self.assertFalse(brief['facts'])
 def test_archive_parameters_are_candidates_until_originals_revalidated(self):
  self.publish_only();card=self.project.latest('collisions')
  self.assertFalse(card['parameters']);self.assertTrue(card['archived_parameter_candidates'])
 def test_archive_does_not_hide_new_local_failure(self):
  self.publish_only();self.failure()
  self.assertTrue(self.project.latest('collisions')['inputs_obsolete'])
  brief=self.project.brief('collisions')['project']
  self.assertEqual(brief['readiness'],'BLOCKED');self.assertFalse(brief['implementation'])
 def test_unsaved_refresh_has_a_working_read_only_detail_route(self):
  fixtures.ProjectTests.seed(self);old=self.project.synthesize('collisions',True);self.failure()
  brief=self.project.brief('collisions')
  self.assertNotEqual(brief['key'],old['key']);self.assertFalse(self.project.has_card(brief['key']))
  self.assertEqual(brief['detail_tool'],'synthesize_technical')
  from agent.project_api import ProjectAPI
  detail=ProjectAPI(self.root).synthesize_technical('collisions')
  self.assertTrue(detail['project_card']['quality']['failures']);self.assertEqual(detail['project_card']['key'],brief['key'])
  self.assertEqual(self.project.index()['collisions'],old['key'])
