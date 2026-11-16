"""Authored software contracts; no Studio or model truth is fabricated."""
import json,shutil,unittest
from pathlib import Path
from agent import intelligence_evidence as ev
from agent.knowledge import dump_frontmatter
from tests.test_autonomy import make_root

class RejectedEvidenceTests(unittest.TestCase):
 def setUp(self):self.root=make_root();self.addCleanup(shutil.rmtree,self.root)
 def test_rejected_note_is_not_reintroduced_by_intelligence(self):
  p=self.root/'knowledge';p.mkdir();meta={'id':'rejected-fixture','title':'Roblox collision false lead','status':'rejete','sources':['https://create.roblox.com/docs/fixture'],'source_tier':4}
  (p/'rejected.md').write_text(dump_frontmatter(meta)+'\n> « This authored rejected collision technique must not enter active evidence. »\n',encoding='utf-8')
  self.assertFalse(ev.documents(self.root))
 def test_rejected_history_remains_explicitly_inspectable(self):
  p=self.root/'knowledge';p.mkdir();meta={'id':'rejected-fixture','title':'Roblox collision false lead','status':'rejete','sources':['https://create.roblox.com/docs/fixture'],'source_tier':4}
  (p/'rejected.md').write_text(dump_frontmatter(meta)+'\n> « This authored rejected collision technique is retained for diagnosis. »\n',encoding='utf-8')
  self.assertTrue(ev.documents(self.root,include_rejected=True))

class ChapterTests(unittest.TestCase):
 def setUp(self):
  self.root=make_root();self.addCleanup(shutil.rmtree,self.root)
  shutil.copytree(Path(__file__).parent/'fixtures/lab_project',self.root/'project')
 def catalog(self):
  from agent.chapters import Chapters
  return Chapters(self.root)
 def test_confirmed_characters_and_proposed_attic_are_separate(self):
  from agent.project import Bible
  items={i['id']:i for i in Bible(self.root).data['items']};self.assertEqual(items['leo']['status'],'CONFIRMED');self.assertEqual(items['maelle']['status'],'CONFIRMED')
  c=self.catalog();self.assertEqual(c.chapters['chapter2']['status'],'PROPOSED');self.assertEqual(c.scenes['chapter2-attic']['validation'],'NOT_TESTED')
 def test_next_chapter_is_prepared_without_auto_research(self):
  p=self.catalog().plan('chapter1');h={s['chapter']:s['horizon'] for s in p['scenes']}
  self.assertEqual(h['chapter1'],'A');self.assertEqual(h['chapter2'],'B');self.assertEqual(h['prologue'],'C');self.assertEqual(p['network_requests'],0)
  self.assertNotIn('dust',p['research_candidates'])
 def test_attic_decomposition_covers_real_subproblems(self):
  p=self.catalog().plan('chapitre 2');tasks={t['task'] for t in p['tasks'] if t['horizon']=='A'}
  self.assertTrue({'architecture','materials','lighting','dust','interactions','puzzles','guidance','audio'}<=tasks)
  self.assertNotIn('dust',p['research_candidates']);self.assertEqual(len(p['research_candidates']),len(set(p['research_candidates'])))
 def test_prologue_postit_is_reported_prototype_not_engine_proof(self):
  p=self.catalog().scenes['prologue-home'];self.assertEqual(p['existing'][0]['status'],'PROTOTYPE');self.assertEqual(p['development'],'UNKNOWN')
 def test_asymmetric_mode_remains_deferred(self):
  p=self.catalog().plan('lobby');self.assertTrue(any(i['id']=='asymmetric' for i in p['deferred']));self.assertNotIn('asymmetric',p['research_candidates'])
 def test_ambiguous_or_unknown_chapters_are_rejected(self):
  from agent.chapters import select_scope
  with self.assertRaises(ValueError):select_scope('chapitre 1 et chapitre 2')
  with self.assertRaises(ValueError):self.catalog().plan('chapter9')
 def test_unknown_task_in_catalog_is_not_silently_scheduled(self):
  p=self.root/'project/chapters.json';d=json.loads(p.read_text());d['scenes'][0]['features'][0]['task']='invented';p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):self.catalog()
 def test_read_only_plan_does_not_change_source_files(self):
  before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()};self.catalog().plan('prologue');self.catalog().brief('chapter2');self.catalog().prepare('chapter1')
  self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
 def test_compact_brief_never_claims_visual_or_engine_execution(self):
  for budget in (500,1800):
   p=self.catalog().brief('chapter2',budget);self.assertLessEqual(len(json.dumps(p,ensure_ascii=False)),budget*3.6);self.assertFalse(p['visual_analysis_performed']);self.assertFalse(p['engine_executed']);self.assertIn('rollback',p)
 def test_chapter_session_pause_and_revision_preserve_counters(self):
  from agent.project_research import ProjectResearch
  r=ProjectResearch(self.root);g=self.catalog().prepare('chapter2',True);before=r.sessions.get(g['id']);r.control(g['id'],'pause',True)
  self.assertEqual(r.run(g['id'],True,True)['state'],'PAUSED');r.control(g['id'],'resume',True)
  path=self.root/'project/chapters.json';d=json.loads(path.read_text());d['revision']+=1;path.write_text(json.dumps(d))
  self.assertEqual(r.run(g['id'],True,True)['state'],'PROJECT_CHANGED');self.assertEqual(before,r.sessions.get(g['id']))
 def test_mcp_contracts_and_research_permission_remain_explicit(self):
  from agent.mcp_v8 import Server
  old=Server(self.root,v111=True);new=Server(self.root,v112=True);self.assertEqual(old.tools,new.tools)
  self.assertEqual(new.dispatch('get_intelligence_brief',{'question':'chapitre 2'})['chapter']['id'],'chapter2')
  with self.assertRaises(PermissionError):new.dispatch('prepare_ocean',{'goal':'chapitre 2','apply':True})
 def test_actual_stdio_chapter_plan(self):
  import subprocess,sys
  repo=Path(__file__).resolve().parents[1];messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'chapter-test','version':'1'}}},{'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'plan_ocean','arguments':{'goal':'chapitre 2'}}}]
  p=subprocess.run([sys.executable,str(repo/'vdn_mcp.py'),'--root',str(self.root),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,encoding='utf-8',capture_output=True,timeout=30,cwd=self.root)
  self.assertEqual(p.returncode,0,p.stderr);out=[json.loads(l) for l in p.stdout.splitlines()];self.assertEqual(out[-1]['result']['structuredContent']['plan']['chapter']['id'],'chapter2')
 def test_chapter_pages_are_generated_and_excluded_from_rag(self):
  from agent.corpus import scan_notes
  pages=self.catalog().pages()
  for name,text in pages.items():
   p=self.root/name;p.parent.mkdir(exist_ok=True);p.write_text(text,encoding='utf-8')
  self.assertFalse(scan_notes(self.root));self.assertEqual(len(pages),4)
 def test_chapter_planning_does_not_implicitly_call_a_model(self):
  from agent.project_api import ProjectAPI
  api=ProjectAPI(self.root,True)
  with self.assertRaises(ValueError):api.synthesize_technical('chapitre 2',True,True)

class FailureLearningTests(unittest.TestCase):
 setUp=ChapterTests.setUp
 def api(self):
  from agent.project_api import ProjectAPI
  return ProjectAPI(self.root,allow_experiments=True)
 def failed(self):
  api=self.api();spec={'problem':'Authored failed tree trial, not real Roblox','technique':'fixture collision method','hypothesis':'test fixture','parameters':{'project_task':'collisions'},'environment':{'project_task':'collisions','engine':'Python'},'protocol':{'controls':'authored fixture'}}
  r=api.prepare_experiment(**spec);r=api.lab_api.start_experiment(r['id'],r['revision'])
  result=api.record_experiment_result(r['id'],'FAILED',{},['AUTHORED fixture only'],errors=['collision blocked path'])
  return spec,result
 def test_failed_report_returns_hypotheses_and_targeted_queries_without_actions(self):
  _,r=self.failed();d=r['diagnostic'];self.assertEqual(d['state'],'RESEARCH_PROPOSED');self.assertEqual(d['automatic_actions'],[]);self.assertTrue(d['targeted_queries']);self.assertFalse(d['verified'])
  self.assertTrue(all(h['status']=='HYPOTHESIS' for h in d['hypotheses']))
 def test_identical_failed_method_is_refused_before_new_record(self):
  spec,r=self.failed()
  with self.assertRaises(ValueError):self.api().prepare_experiment(**spec)
  self.assertEqual(self.api().lab_api.lab.get(r['id'])['status'],'FAILED')
 def test_changed_conditions_and_explicit_retry_are_possible(self):
  spec,_=self.failed();new={**spec,'parameters':{**spec['parameters'],'controlled_change':'new fixture collider'}}
  self.assertEqual(self.api().prepare_experiment(**new)['status'],'PLANNED')
  retry={**spec,'protocol':{**spec['protocol'],'retry_justification':'Repeat to measure a specific missing baseline observation.'}}
  self.assertEqual(self.api().prepare_experiment(**retry)['status'],'PLANNED')
 def test_failure_diagnostics_remain_available_after_restart(self):
  spec,r=self.failed();found=self.api().get_experiment_context('collision');self.assertTrue(found['failure_diagnostics']);self.assertEqual(found['failure_diagnostics'][0]['experiment_id'],r['id'])
 def test_missing_result_is_not_diagnosed_as_an_engine_failure(self):
  from agent.failure_learning import diagnose
  r=self.api().prepare_experiment('fixture waiting','fixture','unknown')
  self.assertEqual(diagnose(self.root,r['id'])['state'],'WAITING_EVIDENCE')


class LabRunnerTests(unittest.TestCase):
 setUp=ChapterTests.setUp
 def lab(self):
  from agent.lab_runner import LocalLab
  return LocalLab(self.root)
 def test_preview_has_no_process_or_write(self):
  before={p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()};r=self.lab().prepare();self.assertFalse(r['engine_executed']);self.assertEqual(before,{p:p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
 def test_execution_requires_an_explicit_operator_capability(self):
  r=self.lab().prepare(apply=True)
  with self.assertRaises(PermissionError):self.lab().run(r['id'])
 def test_shell_or_studio_capabilities_are_not_accepted(self):
  for capability in ('shell','studio','python','publish'):
   with self.assertRaises(ValueError):self.lab().prepare(capability=capability)
  self.assertEqual(self.lab().capabilities()['studio']['state'],'NOT_IMPLEMENTED')
 def test_external_or_parent_scene_paths_are_refused(self):
  for path in ('../asset.blend','C:\\asset.blend','/tmp/asset.blend'):
   with self.assertRaises(ValueError):self.lab().prepare('blender_copy_geometry',path,unit_scale=1)
 def test_changed_scene_after_preparation_is_refused(self):
  p=self.root/'lab/inbox/copy.blend';p.parent.mkdir(parents=True);p.write_bytes(b'AUTHORED NON-BLENDER fixture')
  r=self.lab().prepare('blender_copy_geometry','lab/inbox/copy.blend',unit_scale=1,apply=True);p.write_bytes(b'changed fixture')
  with self.assertRaises(ValueError):self.lab().run(r['id'],allow_blender=True)
 def test_job_tampering_is_refused(self):
  lab=self.lab();r=lab.prepare(apply=True);p=lab.path(r['id']);v=json.loads(p.read_text());v['spec']['script_sha256']='bad';p.write_text(json.dumps(v))
  with self.assertRaises(ValueError):lab.get(r['id'])
 def test_wrong_engine_version_is_blocked_without_geometry_execution(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  import sys
  r=self.lab().prepare(apply=True)
  with patch('agent.lab_runner.subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='Blender 4.3.2')) as run:
   result=self.lab().run(r['id'],executable=sys.executable,allow_blender=True)
  self.assertEqual(result['state'],'BLOCKED');self.assertFalse(result['engine_executed']);self.assertEqual(run.call_count,1)
 def test_unavailable_engine_does_not_fabricate_reports(self):
  r=self.lab().prepare(apply=True);result=self.lab().run(r['id'],executable=str(self.root/'missing-blender'),allow_blender=True)
  self.assertEqual(result['state'],'BLOCKED');self.assertFalse(result['reports'])

class VisualFallbackTests(unittest.TestCase):
 setUp=ChapterTests.setUp
 def data(self):return {'description':'Une forêt de sapins enneigés avec silhouettes irrégulières et une lampe.','observed':['Branches irrégulières rapportées par l’utilisateur'],'inferred':['La géométrie pourrait contribuer'],'unknown':['Aucun asset ni image inspecté'],'keep':['silhouette'],'avoid':['répétition'],'reference_hashes':[],'provenance':'operator_description'}
 def test_description_is_not_a_claim_of_image_analysis(self):
  from agent.visual_description import describe
  from agent.project_work import Project
  r=describe(Project(self.root),'trees',self.data());self.assertFalse(r['description']['visual_analysis_performed']);self.assertIn('trees',r['description']['candidate_tasks']);self.assertEqual(r['description']['inference_status'],'HYPOTHESIS')
 def test_missing_description_and_fake_image_reference_are_refused(self):
  from agent.visual_description import describe
  from agent.project_work import Project
  d=self.data();d['description']=''
  with self.assertRaises(ValueError):describe(Project(self.root),'trees',d)
  d=self.data();d['reference_hashes']=['0'*64]
  with self.assertRaises(ValueError):describe(Project(self.root),'trees',d)
 def test_description_revision_invalidates_cache_without_entering_primary_sources(self):
  from agent.visual_description import describe
  from agent.project_work import Project
  p=Project(self.root);first=p.synthesize('trees',True);describe(p,'trees',self.data(),True)
  self.assertTrue(p.get(first['key'])['inputs_obsolete']);self.assertFalse(ev.documents(self.root));self.assertNotEqual(first['key'],p.synthesize('trees')['key'])
 def test_unknown_model_provenance_is_not_accepted_as_real_vision(self):
  from agent.visual_description import describe
  from agent.project_work import Project
  d=self.data();d['provenance']='real_visual_model_executed'
  with self.assertRaises(ValueError):describe(Project(self.root),'trees',d)

class NarrativeHandoffRegression(unittest.TestCase):
 setUp=ChapterTests.setUp
 def test_confirmed_answers_are_not_lost_from_bible_handoff(self):
  from agent.project_work import Project
  result=Project(self.root).brief('Bible du jeu')['project'];answers={q['id']:q.get('answer') for q in result['questions']}
  self.assertIn('Léo',answers['playable'] or '');self.assertIn('policier',answers['playable'] or '')
  self.assertIn('omitted_items',result)

class MultisourceTests(unittest.TestCase):
 setUp=ChapterTests.setUp
 def test_candidate_sources_are_bounded_and_do_not_enable_a_provider(self):
  from agent.project import Bible
  from agent.ocean_web import settings
  b=Bible(self.root);task=b.task('collisions');self.assertEqual(task['source_candidates'][1]['provider'],'devforum');self.assertNotIn('devforum',settings(self.root)['providers'])
  p=self.root/'project/bible.json';d=json.loads(p.read_text());d['tasks'][0]['source_candidates']=[{'url':'https://example.invalid','provider':'anything','role':'candidate'}]*5;p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):Bible(self.root)
 def test_failure_then_configured_alternative_preserves_partial_source_progress(self):
  from unittest.mock import patch
  from agent.project_research import ProjectResearch,Collector
  from agent.providers import FetchError
  from agent import budget
  p=self.root/'config/ocean.json';c=json.loads(p.read_text());c['providers']['devforum']={'enabled':True,'hosts':['devforum.roblox.com'],'seeds':[],'policy':'authored fixture'};p.write_text(json.dumps(c))
  research=ProjectResearch(self.root);g=research.prepare(['collisions'],True);collector=Collector(research,g,False,None);calls=[]
  def get(web,url,provider,*a):
   calls.append(provider)
   if provider=='roblox':raise FetchError('authored unavailable official source')
   from tests import test_project as source_fixture
   source_fixture.ProjectTests.seed(self);return {'links':[]}
  with budget.using(budget.Budget(20,0)),patch('agent.ocean_web.OceanWeb.get',get):result=collector(self.root,[('forest',research.project.bible.task('collisions')['query'])],2)
  self.assertEqual(calls,['roblox','devforum']);self.assertEqual(result['fetch_attempts'],2);self.assertTrue(result['created_notes']);self.assertTrue(result['errors'])

class LocalRunnerBindingTests(unittest.TestCase):
 setUp=ChapterTests.setUp
 def test_experiment_redirection_is_rejected(self):
  from agent.lab_runner import LocalLab
  lab=LocalLab(self.root);r=lab.prepare(apply=True);p=lab.path(r['id']);d=json.loads(p.read_text());d['experiments'][0]['id']='00000000-0000-0000-0000-000000000000';p.write_text(json.dumps(d))
  with self.assertRaises(ValueError):lab.get(r['id'])
 def test_nonfinite_scene_units_are_refused_before_job_or_experiment(self):
  from agent.lab_runner import LocalLab
  p=self.root/'lab/inbox/fixture.blend';p.parent.mkdir(parents=True);p.write_bytes(b'NOT A REAL BLENDER FILE: validation fixture')
  for value in (float('nan'),float('inf'),True,0):
   with self.assertRaises(ValueError):LocalLab(self.root).prepare('blender_copy_geometry','lab/inbox/fixture.blend',apply=True,unit_scale=value)
  self.assertFalse((self.root/'lab/runner').exists());self.assertFalse((self.root/'lab/experiments').exists())

class CommunityExtractionRegression(unittest.TestCase):
 setUp=ChapterTests.setUp
 def test_public_topic_json_is_extracted_with_post_provenance(self):
  from agent.ocean_web import OceanWeb
  from tests.test_ocean import Response
  p=self.root/'config/ocean.json';cfg=json.loads(p.read_text());cfg['providers']['devforum']={'enabled':True,'hosts':['devforum.roblox.com'],'seeds':['https://devforum.roblox.com/t/123.json'],'policy':'authored fixture'};p.write_text(json.dumps(cfg))
  topic={'title':'Authored collision topic fixture','created_at':'2026-01-01T00:00:00Z','post_stream':{'posts':[{'id':123,'username':'fixture-author','cooked':'<p>This authored collision explanation must be extracted as text with its post attribution.</p>'}]}}
  def opener(req,**kw):return Response(req.full_url,'User-agent: *\nAllow: /\n' if req.full_url.endswith('/robots.txt') else json.dumps(topic))
  d=OceanWeb(self.root,opener).get('https://devforum.roblox.com/t/123.json','devforum')
  self.assertTrue(d['text'].startswith('# Authored collision topic fixture'));self.assertNotIn('<p>',d['text']);self.assertEqual(d['conditions']['post_ids'],[123]);self.assertEqual(d['conditions']['license'],'UNKNOWN')

class ChapterSourceGateRegression(unittest.TestCase):
 setUp=ChapterTests.setUp
 def test_foreign_engine_and_incompatible_blender_do_not_fill_chapter_brief(self):
  from agent.chapters import Chapters
  folder=self.root/'knowledge';folder.mkdir()
  for key,url,version in [('foreign','https://dev.epicgames.com/documentation/unreal-engine/lumen','unknown'),('old-blender','https://docs.blender.org/manual/en/5.3/render/materials.html','5.3')]:
   meta={'id':key,'title':'Roblox lighting material source fixture','status':'documente','source_tier':4,'engine_version':version,'sources':[url]}
   (folder/(key+'.md')).write_text(dump_frontmatter(meta)+'\n> « Roblox lighting shadow material texture reference is authored here only to test incompatible source rejection. »\n',encoding='utf-8')
  b=Chapters(self.root).brief('chapter2',8000)
  self.assertFalse([s for t in b['tasks'] for s in t['source_references']]);self.assertEqual(b['engine_version_filtered_documents'],2)
