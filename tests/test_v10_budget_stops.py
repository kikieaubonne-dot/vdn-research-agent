"""HTTP fixtures only: no real Internet or user's Windows session is accessed."""
import json
import shutil
import unittest
from unittest.mock import patch,MagicMock
from urllib.error import URLError,HTTPError

from agent import budget,providers
from agent.research_session import ResearchSessions
from agent.research_queue import ResearchQueue
from tests.test_autonomy import make_root


class SessionBudgetTests(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root)
        path=self.root/'config/v10.json';cfg=json.loads(path.read_text());cfg['network_enabled']=True
        path.write_text(json.dumps(cfg));self.sessions=ResearchSessions(self.root)
        self.state=self.sessions.prepare('foliage mesh export',apply=True)
        self.sid=self.state['id']
    def response(self):
        response=MagicMock();response.__enter__.return_value=response
        response.geturl.return_value='https://create.roblox.com/docs/fixture.md'
        response.headers={};response.read.return_value=b'fixture'
        return response
    def collect(self,*args,**kwargs):
        for index in range(7):
            if index<5:budget.fetch_attempt()
            providers.http_get('https://create.roblox.com/docs/fixture.md')
    def run_online(self,fn=None):
        return self.sessions.run(self.sid,apply=True,allow_network=True,research_fn=fn or self.collect)
    def test_observed_third_tick_six_http_five_fetches_and_resume_to_twelve(self):
        state=self.sessions.get(self.sid);state['ticks']=2;self.sessions.save(state)
        q=self.sessions.queue(state,False)
        for word in ('bark','needles','snow','uv','wind','alpha','atlas','normals','lighting'):
            q.add('spruce','foliage '+word,1)
        q.save()
        observed=[]
        def wire_response(*a,**k):
            observed.append(self.sessions.get(self.sid)['http_calls'])
            self.assertEqual(observed[-1],len(observed))
            self.assertEqual(ResearchQueue(self.root,recover=False).daily()['http_calls'],len(observed))
            return self.response()
        with patch('agent.providers.urlopen',side_effect=wire_response) as wire:
            first=self.run_online()
            self.assertEqual(first['state'],'BUDGET_STOP')
            self.assertEqual(first['session']['ticks'],3)
            self.assertEqual(first['session']['http_calls'],6)
            self.assertEqual(first['session']['fetch_attempts'],5)
            self.assertEqual(wire.call_count,6)
            self.assertEqual(first['queue']['counts']['running'],0)
            self.assertEqual(first['stop_details']['scope'],'tick')
            self.assertEqual(first['stop_details']['limit'],6)
            self.assertEqual(first['session']['last_tick']['session_http_remaining'],6)
            self.assertEqual(first['queue']['counts']['pending'],10)
            second=self.run_online()
            self.assertEqual(wire.call_count,12)
            self.assertEqual(second['stop_details']['scope'],'session')
            self.assertEqual(second['stop_details']['limit'],12)
            self.assertEqual(second['stop_details']['used'],12)
            self.assertEqual(second['session']['http_calls'],12)
            self.assertEqual(second['queue']['counts']['running'],0)
            before=self.sessions.get(self.sid)
            third=self.run_online()
            self.assertEqual(wire.call_count,12)
            self.assertEqual(third['session']['attempts'],before['attempts'])
            self.assertEqual(third['session']['ticks'],before['ticks'])
        self.assertEqual(first['session']['integration_failures'],0)
    def test_stop_returned_by_collector_keeps_scope_and_source_errors(self):
        def collect(*args,**kwargs):
            try:self.collect()
            except budget.BudgetExhausted as exc:
                return {'stop_reason':str(exc),'stop_details':exc.details(),'created':0,'errors':['fixture source unavailable']}
        with patch('agent.providers.urlopen',return_value=self.response()):r=self.run_online(collect)
        self.assertEqual(r['state'],'BUDGET_STOP');self.assertEqual(r['stop_details']['scope'],'tick')
        self.assertEqual(r['session']['last_collection']['errors'],['fixture source unavailable'])
    def test_source_error_is_not_a_budget_stop_and_cleans_queue(self):
        r=self.run_online(lambda *a,**k:{'errors':['fixture HTTP 403 on create.roblox.com'],'created':0})
        self.assertEqual(r['state'],'ERROR');self.assertEqual(r['session']['integration_failures'],1)
        self.assertEqual(r['queue']['counts']['running'],0)
        self.assertEqual(r['session']['last_collection']['errors'],['fixture HTTP 403 on create.roblox.com'])
    def test_successful_resume_removes_stale_stop_and_error(self):
        state=self.sessions.get(self.sid);state.update(stop_reason='old budget',stop_details={'scope':'tick'},error='old error')
        self.sessions.save(state)
        r=self.run_online(lambda *a,**k:{'created':0,'errors':[]})
        self.assertNotIn('stop_reason',r['session']);self.assertNotIn('error',r['session'])
        self.assertNotIn('stop_details',r['session'])
    def test_daily_http_limit_is_distinct(self):
        q=ResearchQueue(self.root,recover=False);q.daily()['http_calls']=q.cfg['daily']['max_http_calls'];q.save()
        with patch('agent.providers.urlopen') as wire:r=self.run_online()
        wire.assert_not_called();self.assertEqual(r['stop_details']['scope'],'daily')
        self.assertEqual(r['stop_details']['resource'],'http_calls')
        self.assertEqual(r['queue']['counts']['running'],0)
    def test_exhausted_session_preflight_persists_recovery_without_spending_attempt(self):
        state=self.sessions.get(self.sid);q=self.sessions.queue(state,False);item=next(iter(q.data['items'].values()))
        q.mark_running(item);state.update(http_calls=12,ticks=3,attempts={item['key']:1});self.sessions.save(state)
        before=q.path.read_bytes()
        self.assertEqual(self.sessions.run(self.sid)['queue']['counts']['running'],1)
        self.assertEqual(q.path.read_bytes(),before)
        with patch('agent.providers.urlopen') as wire:r=self.run_online()
        wire.assert_not_called();self.assertEqual(r['session']['ticks'],3)
        self.assertEqual(r['session']['attempts'][item['key']],1)
        self.assertEqual(self.sessions.queue(r['session'],False).summary()['counts']['pending'],1)
    def test_budget_stop_does_not_refund_attempts(self):
        with patch('agent.providers.urlopen',return_value=self.response()):
            self.run_online();r=self.run_online()
        self.assertEqual(max(r['session']['attempts'].values()),2)
        self.assertEqual(r['queue']['counts']['failed'],1)
        self.assertEqual(r['queue']['counts']['running'],0)
    def test_bootstrap_http_is_counted_and_stop_metadata_survives_setup(self):
        docs=MagicMock();docs.path=self.root/'missing-index.json'
        docs.refresh.side_effect=lambda:[providers.http_get('https://create.roblox.com/docs/llms.txt') for _ in range(7)]
        forum=MagicMock()
        with patch('agent.run.active_providers',return_value={'roblox_docs':docs,'devforum':forum}),patch('agent.providers.urlopen',return_value=self.response()) as wire:
            r=self.sessions.run(self.sid,apply=True,allow_network=True)
        self.assertEqual(r['state'],'BUDGET_STOP');self.assertEqual(wire.call_count,6)
        self.assertEqual(r['session']['fetch_attempts'],0)
        self.assertEqual(r['stop_details']['scope'],'tick')
        forum.refresh.assert_not_called()
    def test_partial_created_notes_remain_unverified_and_visible_after_stop(self):
        from tests.test_autonomy import FakeDocs
        class LaterProvider:
            name,tier='github',3
            def search(self,*args):
                for _ in range(7):providers.http_get('https://api.github.com/search/repositories?q=fixture')
        with patch('agent.providers.urlopen',return_value=self.response()):
            r=self.sessions.run(self.sid,apply=True,allow_network=True,provs={'roblox_docs':FakeDocs(),'github':LaterProvider()})
        self.assertEqual(r['state'],'BUDGET_STOP')
        self.assertEqual(r['session']['last_collection']['created'],1)
        self.assertEqual(len(r['session']['last_collection']['created_note_ids']),1)
        self.assertFalse(r['session']['last_collection']['truth_verified'])
        self.assertEqual(r['queue']['counts']['running'],0)
    def test_tick_deadline_and_daily_fetch_are_not_http_tick_limits(self):
        path=self.root/'config/v10.json';cfg=json.loads(path.read_text());cfg['research']['time_per_tick_s']=0;path.write_text(json.dumps(cfg))
        r=self.run_online();self.assertEqual(r['stop_details']['scope'],'tick');self.assertEqual(r['stop_details']['resource'],'compute_s')
        cfg['research']['time_per_tick_s']=20;path.write_text(json.dumps(cfg))
        q=ResearchQueue(self.root,recover=False);q.daily()['fetch']=q.cfg['daily']['max_fetch'];q.save()
        r=self.run_online();self.assertEqual(r['stop_details']['scope'],'daily');self.assertEqual(r['stop_details']['resource'],'fetch_attempts')
    def test_session_tick_and_compute_preflight_keep_scoped_diagnostics(self):
        state=self.sessions.get(self.sid);state['ticks']=state['limits']['max_ticks'];self.sessions.save(state)
        r=self.run_online();self.assertEqual(r['reason'],'max_ticks');self.assertEqual(r['stop_details']['scope'],'session')
        self.assertEqual(r['stop_details']['resource'],'ticks')
        state=self.sessions.get(self.sid);state['ticks']=0;state['compute_reserved_s']=state['limits']['compute_budget_s'];self.sessions.save(state)
        r=self.run_online();self.assertEqual(r['reason'],'compute_budget');self.assertEqual(r['stop_details']['resource'],'compute_s')
    def test_status_exposes_scoped_stop_without_reporting_integration_error(self):
        from agent.v10 import metrics
        with patch('agent.providers.urlopen',return_value=self.response()):self.run_online()
        status=metrics(self.root)['sessions'][0]
        self.assertIsNone(status['last_error']);self.assertEqual(status['integration_failures'],0)
        self.assertEqual(status['stop_details']['scope'],'tick')
        self.assertEqual(status['last_tick']['http_calls'],6)
        self.assertEqual(status['last_tick']['daily']['http_calls'],6)
    def test_collection_diagnostics_do_not_persist_recognizable_credentials(self):
        secret='ghp_'+'a'*40
        r=self.run_online(lambda *a,**k:{'errors':['fixture '+secret]})
        self.assertEqual(r['state'],'ERROR')
        self.assertNotIn(secret,self.sessions.session_path(self.sid).read_text(encoding='utf-8'))
        self.assertNotIn(secret,self.sessions.queue(r['session'],False).path.read_text(encoding='utf-8'))
    def test_real_research_result_propagates_budget_metadata(self):
        class Provider:
            name,tier='roblox_docs',1
            def search(self,*a):
                for _ in range(7):providers.http_get('https://create.roblox.com/docs/fixture.md')
        with patch('agent.providers.urlopen',return_value=self.response()):
            r=self.sessions.run(self.sid,apply=True,allow_network=True,provs={'roblox_docs':Provider()})
        self.assertEqual(r['state'],'BUDGET_STOP');self.assertEqual(r['stop_details']['scope'],'tick')
        self.assertEqual(r['session']['last_collection']['created'],0)


class TransportBudgetTests(unittest.TestCase):
    def response(self,url):
        r=MagicMock();r.__enter__.return_value=r;r.geturl.return_value=url;r.headers={};r.read.return_value=b'fixture';return r
    def test_robots_and_each_retry_share_the_http_budget(self):
        guard=budget.Budget(60,6)
        url='https://create.roblox.com/robots.txt'
        with budget.using(guard),patch('agent.providers.urlopen',side_effect=[self.response(url)]+[URLError('fixture')]*5) as wire,patch('agent.budget.time.sleep'):
            providers.http_get(url)
            with self.assertRaises(budget.BudgetExhausted):providers.http_get('https://create.roblox.com/docs/fixture.md',retries=10)
        self.assertEqual(wire.call_count,6);self.assertEqual(guard.http_calls,6)
    def test_retriable_status_attempts_are_counted_before_wire(self):
        guard=budget.Budget(60,2)
        with budget.using(guard),patch('agent.providers.urlopen',side_effect=HTTPError('https://api.github.com',503,'fixture',{},None)) as wire,patch('agent.budget.time.sleep'):
            with self.assertRaises(budget.BudgetExhausted):providers.http_get('https://api.github.com/search/repositories?q=fixture',retries=5)
        self.assertEqual(wire.call_count,2);self.assertEqual(guard.http_calls,2)
    def test_redirect_charged_before_follow_and_disallowed_target_not_charged(self):
        request=providers.Request('https://create.roblox.com/docs/first.md')
        guard=budget.Budget(60,2)
        with budget.using(guard):
            budget.request()
            redirected=providers.CheckedRedirect().redirect_request(request,None,302,'found',{},'https://create.roblox.com/docs/second.md')
            self.assertIsNotNone(redirected);self.assertEqual(guard.http_calls,2)
            with self.assertRaises(budget.BudgetExhausted):providers.CheckedRedirect().redirect_request(request,None,302,'found',{},'https://create.roblox.com/docs/third.md')
            with self.assertRaises(providers.FetchError):providers.CheckedRedirect().redirect_request(request,None,302,'found',{},'https://outside.invalid/private')
        self.assertEqual(guard.http_calls,2)


if __name__=='__main__':unittest.main()
