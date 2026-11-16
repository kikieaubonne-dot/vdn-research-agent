import json
import shutil
import unittest
from unittest.mock import patch
import uuid
from agent import budget,lab_plan,visual
from agent.lab_store import LabStore
from agent.research_session import ResearchSessions
from agent.research_queue import ResearchQueue
from tests.test_autonomy import make_root


class LabTests(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.lab=LabStore(self.root)
    def create(self,**kw):return self.lab.create('foliage snow','cards','Check silhouette',**kw)
    def running(self,**kw):
        r=self.create(**kw);self.lab.transition(r['id'],'PLANNED');return self.lab.transition(r['id'],'RUNNING')
    def artifact(self,kind='self_generated'):
        path=self.root/'lab/inbox/test.txt';path.parent.mkdir(parents=True,exist_ok=True);path.write_text('fixture data, no Studio execution')
        return self.lab.import_artifact('lab/inbox/test.txt',kind)
    def test_lifecycle_failure_search_and_retry(self):
        r=self.running();r=self.lab.record_result(r['id'],'FAILED',{},['fixture failed'],errors=['alpha fringe'])
        self.assertEqual(lab_plan.context(self.root,'foliage')['failed_methods'][0]['id'],r['id'])
        self.lab.transition(r['id'],'PLANNED');self.lab.transition(r['id'],'RUNNING')
        r=self.lab.record_result(r['id'],'SUCCESS',{'triangles':None},['fixture success'])
        self.assertEqual(len(r['results']),2);self.assertEqual(r['verification'],'not_verified')
        self.assertEqual(lab_plan.context(self.root,'foliage')['failed_methods'][0]['outcome_status'],'FAILED')
    def test_no_direct_promotion_and_revision_guard(self):
        r=self.create()
        for state in ('VERIFIED','SUCCESS','FAILED','RUNNING'):
            with self.assertRaises(ValueError):self.lab.transition(r['id'],state)
        with self.assertRaises(ValueError):self.lab.transition(r['id'],'PLANNED',999)
        self.assertEqual(self.lab.get(r['id'])['revision'],1)
    def test_idempotent_create_and_result_replay(self):
        eid=str(uuid.uuid4());r=self.running(experiment_id=eid)
        self.assertEqual(self.create(experiment_id=eid)['revision'],r['revision'])
        rid=str(uuid.uuid4());kwargs=dict(metrics={},observations=['fixture'],request_id=rid)
        first=self.lab.record_result(eid,'SUCCESS',**kwargs)
        self.assertEqual(self.lab.record_result(eid,'SUCCESS',**kwargs),first)
        with self.assertRaises(ValueError):self.lab.record_result(eid,'FAILED',{},['different'],errors=['error'],request_id=rid)
    def test_self_generated_cannot_verify(self):
        r=self.running(environment={'studio':'fixture only'});a=self.artifact()
        self.lab.record_result(r['id'],'SUCCESS',{},['fixture'],artifacts=[a['id']])
        with self.assertRaises(ValueError):self.lab.review(r['id'],'fixture tester',['fixture only'],True)
    def test_operator_attestation_is_explicit_and_conditional(self):
        r=self.running(environment={'engine':'test fixture, not Roblox'});a=self.artifact('external_measurement')
        self.lab.record_result(r['id'],'SUCCESS',{},['fixture'],artifacts=[a['id']])
        with self.assertRaises(ValueError):self.lab.review(r['id'],'fixture tester',['fixture only'])
        r=self.lab.review(r['id'],'fixture tester',['fixture only'],True)
        self.assertEqual(r['status'],'VERIFIED');self.assertEqual(r['reuse_conditions'],['fixture only'])
        self.lab.transition(r['id'],'PLANNED');self.assertEqual(self.lab.get(r['id'])['verification'],'not_verified')
    def test_event_corruption_fails_closed(self):
        r=self.create();p=next((self.root/'lab/experiments'/r['id']/'events').glob('*.json'))
        event=json.loads(p.read_text());event['snapshot']['status']='VERIFIED';p.write_text(json.dumps(event))
        with self.assertRaises(ValueError):self.lab.get(r['id'])
        self.assertTrue(self.lab.find()['diagnostics'])
    def test_atomic_failure_preserves_previous_event(self):
        r=self.create()
        with patch('agent.lab_store.atomic_write',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):self.lab.transition(r['id'],'PLANNED')
        self.assertEqual(self.lab.get(r['id']),r)
    def test_wrong_json_types_report_corruption(self):
        r=self.create();p=next((self.root/'lab/experiments'/r['id']/'events').glob('*.json'));p.write_text('[]')
        with self.assertRaises(ValueError):self.lab.get(r['id'])
        self.assertEqual(len(self.lab.find()['diagnostics']),1)
    def test_artifact_integrity_and_receipt_identity(self):
        a=self.artifact('external_capture');p=self.root/'lab/artifacts'/ (a['id']+'.receipt.json')
        record=json.loads(p.read_text());record['kind']='self_generated';p.write_text(json.dumps(record))
        with self.assertRaises(ValueError):self.lab.artifact(a['id'])
        p.write_text(json.dumps(a));(self.root/a['path']).write_text('changed')
        with self.assertRaises(ValueError):self.lab.artifact(a['id'])
    def test_path_symlinks_secrets_and_nonfinite_refused(self):
        for name in ('../outside.txt','lab/inbox/../../../outside.txt','lab/inbox/code.py'):
            with self.assertRaises(ValueError):self.lab.import_artifact(name)
        with self.assertRaises(ValueError):self.create(parameters={'api_key':'do not persist'})
        r=self.running()
        with self.assertRaises(ValueError):self.lab.record_result(r['id'],'SUCCESS',{'time':float('nan')},['fixture'])
        target=self.root/'outside';target.mkdir()
        try:(self.root/'lab/inbox').symlink_to(target,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('symlinks unavailable for this account')
        with self.assertRaises(ValueError):self.lab.import_artifact('lab/inbox/test.txt')
    def test_reference_is_only_a_plan_and_idempotent(self):
        p=lab_plan.spruce(self.root);self.assertFalse((self.root/'lab').exists());self.assertIsNone(p['winner'])
        p=lab_plan.spruce(self.root,True);again=lab_plan.spruce(self.root,True)
        self.assertEqual(p,again);self.assertEqual(len(p['zones']),9)
        self.assertTrue(all(v is None for v in p['experiments'][0]['protocol']['metrics_template'].values()))
        c=lab_plan.compare(self.root,*[r['id'] for r in p['experiments']])
        self.assertFalse(c['comparable']);self.assertIsNone(c['winner'])


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.sessions=ResearchSessions(self.root)
    def cfg(self,**fields):
        path=self.root/'config/v10.json';cfg=json.loads(path.read_text());cfg.update(fields);path.write_text(json.dumps(cfg));return cfg
    def prepare(self):return self.sessions.prepare('foliage mesh export',apply=True)
    def test_dry_run_and_default_off_are_pure(self):
        self.sessions.prepare('foliage mesh export');self.assertEqual(self.sessions.tick(apply=True)['state'],'disabled')
        self.assertFalse((self.root/'lab').exists());self.assertFalse((self.root/'output').exists())
    def test_recursive_offline_bounded_and_persistent(self):
        s=self.prepare()
        for _ in range(12):self.sessions.run(s['id'],apply=True)
        state=self.sessions.get(s['id']);q=self.sessions.queue(state,False)
        self.assertGreaterEqual(max(i['depth'] for i in q.data['items'].values()),1)
        self.assertLessEqual(max(i['depth'] for i in q.data['items'].values()),2)
        self.assertLessEqual(len(q.data['items']),24);self.assertLessEqual(state['ticks'],12)
        self.assertEqual(state['http_calls'],0);self.assertTrue(all(not d['result']['truth_verified'] for d in state['decisions']))
    def test_profile_dependencies_and_branch_budget(self):
        question='Comment reproduire un sapin enneige photorealiste dans Roblox'
        r=self.sessions.prepare(question,apply=True)
        self.assertTrue(self.sessions.queue(r,False).data['items'])
        c=json.loads((self.root/'config/v10.json').read_text());c['research']['max_branches']=1;self.cfg(research=c['research'])
        with self.assertRaises(ValueError):self.sessions.prepare(question,apply=True)
    def test_http_budget_persisted_before_calls_and_retries(self):
        c=self.cfg(network_enabled=True);c['research']['max_http_calls']=1;self.cfg(research=c['research'])
        s=self.prepare();calls=[]
        def collect(*args,**kwargs):
            budget.request();calls.append('first');budget.request();calls.append('second')
        result=self.sessions.run(s['id'],apply=True,allow_network=True,research_fn=collect)
        self.assertEqual(calls,['first']);self.assertEqual(result['state'],'BUDGET_STOP')
        self.assertEqual(self.sessions.get(s['id'])['http_calls'],1)
        self.assertEqual(ResearchQueue(self.root,recover=False).daily()['http_calls'],1)
        self.sessions.run(s['id'],apply=True,allow_network=True,research_fn=collect);self.assertEqual(calls,['first'])
    def test_interruption_preserves_attempt_and_resumes(self):
        s=self.prepare()
        with patch('agent.research_session.KnowledgeEngine.find_procedures',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):self.sessions.run(s['id'],apply=True)
        old=self.sessions.get(s['id']);self.assertEqual(sum(old['attempts'].values()),1)
        result=self.sessions.run(s['id'],apply=True);self.assertNotEqual(result['state'],'ERROR')
        self.assertLessEqual(max(result['session']['attempts'].values()),2)
    def test_daily_quota_and_compute_stop(self):
        s=self.prepare();q=ResearchQueue(self.root,recover=False);q.daily()['items']=q.cfg['daily']['max_items'];q.save()
        result=self.sessions.run(s['id'],apply=True);self.assertEqual(result['state'],'BUDGET_STOP')
        c=self.cfg();c['research']['compute_budget_s']=0;self.cfg(research=c['research']);s=self.prepare()
        self.assertEqual(self.sessions.run(s['id'],apply=True)['reason'],'compute_budget')
    def test_network_flag_and_corrupt_queue_refused(self):
        s=self.prepare()
        with self.assertRaises(PermissionError):self.sessions.run(s['id'],apply=True,allow_network=True)
        (self.sessions.folder(s['id'])/'queue.json').write_text('broken')
        with self.assertRaises(ValueError):self.sessions.run(s['id'],apply=True)
    def test_schedule_allowlist_and_not_due(self):
        self.cfg(autonomous_enabled=True,schedule={'enabled':True,'interval_s':3600},allowed_goals=['saves'])
        result=self.sessions.tick('scheduled',apply=True)
        self.assertEqual(result['goal'],'saves');self.assertFalse(result['game_executed'])
        self.assertEqual(self.sessions.tick('scheduled',apply=True)['state'],'not_due')
        self.assertEqual(LabStore(self.root).get(result['planned_experiment_id'])['status'],'PLANNED')
    def test_session_id_idempotence(self):
        sid=str(uuid.uuid4());a=self.sessions.prepare('mesh foliage',session_id=sid,apply=True)
        self.assertEqual(self.sessions.prepare('mesh foliage',session_id=sid,apply=True),a)
        with self.assertRaises(ValueError):self.sessions.prepare('different mesh',session_id=sid,apply=True)

    def test_time_stop_before_lookup_and_attempt_cap(self):
        c=self.cfg();c['research']['time_per_tick_s']=0;self.cfg(research=c['research']);s=self.prepare()
        with patch('agent.research_session.KnowledgeEngine.find_procedures',side_effect=AssertionError('deadline must stop first')):
            self.assertEqual(self.sessions.run(s['id'],apply=True)['state'],'BUDGET_STOP')
        c['research']['time_per_tick_s']=20;self.cfg(research=c['research']);s=self.prepare()
        with patch('agent.research_session.KnowledgeEngine.find_procedures',side_effect=RuntimeError('fixture lookup failure')) as mock:
            for _ in range(4):self.sessions.run(s['id'],apply=True)
        self.assertEqual(mock.call_count,2)
        self.assertEqual(self.sessions.get(s['id'])['integration_failures'],2)
    def test_lowered_depth_and_terminal_do_not_repeat_work(self):
        s=self.prepare();self.sessions.run(s['id'],apply=True)
        c=self.cfg();c['research']['max_depth']=0;self.cfg(research=c['research'])
        self.sessions.run(s['id'],apply=True);old=self.sessions.get(s['id'])
        self.assertEqual(old['status'],'COMPLETE');self.assertEqual(old['limits']['max_depth'],0)
        self.sessions.run(s['id'],apply=True);self.assertEqual(self.sessions.get(s['id'])['ticks'],old['ticks'])
    def test_lab_lock_symlink_refused_without_external_write(self):
        target=self.root/'outside';target.mkdir();folder=self.root/'lab';folder.mkdir()
        try:(folder/'.research-control').symlink_to(target,target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('symlinks unavailable')
        with self.assertRaises(ValueError):self.prepare()
        self.assertEqual(list(target.iterdir()),[])
    def test_invalid_session_and_config_fail_closed(self):
        s=self.prepare();p=self.sessions.session_path(s['id']);obj=json.loads(p.read_text());obj['limits']['max_ticks']=-1;p.write_text(json.dumps(obj))
        with self.assertRaises(ValueError):self.sessions.run(s['id'],apply=True)
        c=self.cfg();c['research']['unknown_limit']=3;self.cfg(research=c['research'])
        with self.assertRaises(ValueError):self.prepare()


if __name__=='__main__':unittest.main()
