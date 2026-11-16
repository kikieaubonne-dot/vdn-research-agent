import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch,MagicMock
from agent import budget,intelligence_evidence as ev,intelligence_models as im,intelligence_semantic as semantic
from agent.intelligence import Intelligence,validate_model,prompt_for
from agent.intelligence_api import IntelligenceAPI
from agent.lab_store import LabStore
from agent.mcp_v8 import Server
from agent.ocean_web import OceanWeb
from bench.evaluate_intelligence import corpus,contract
from tests.test_autonomy import make_root

REPO=Path(__file__).resolve().parents[1]


class Response(io.BytesIO):
    def __enter__(self):return self
    def __exit__(self,*args):self.close()


class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.data,self.docs=corpus();self.brain=Intelligence(self.root)
    def cfg(self,**values):
        cfg={**im.DEFAULT,**values};(self.root/'config/intelligence.json').write_text(json.dumps(cfg),encoding='utf-8');return cfg
    def seed(self,document='collision'):
        d=next(d for d in self.docs if d['id']==document)
        # Explicit authored transport fixture, not an actual Internet source.
        record={'url':'https://create.roblox.com/fixture/'+d['id'],'text':d['text'],'provider':'roblox',
                'text_sha256':d['sha256'],'raw_text_sha256':d['sha256'],'version':d['version'],'at':__import__('time').time(),
                'accessed':'2026-11-16','published':d['published'],'truncated':False,'conditions':d['conditions']}
        folder=self.root/'lab/ocean/sources';folder.mkdir(parents=True,exist_ok=True)
        p=folder/(document+'.json');p.write_text(json.dumps(record),encoding='utf-8');return p
    def payload(self):return {'diagnosis':'Le comportement reste à tester.','claims':[],'procedures':[],'uncertainties':['Version du projet inconnue.'],'priorities':['Consigner le parcours témoin.']}
    def opener(self,req,**kwargs):
        if req.full_url.endswith('/api/tags'):r={'models':[{'name':'fixture:compact','digest':'test-digest','size':100,'details':{'quantization_level':'TEST'}}]}
        elif req.full_url.endswith('/api/version'):r={'version':'FIXTURE-VERSION'}
        elif req.full_url.endswith('/api/ps'):r={'models':[]}
        elif req.full_url.endswith('/api/show'):r={'license':'AUTHORED TEST LICENSE','details':{},'model_info':{}}
        elif req.full_url.endswith('/api/generate'):
            return Response((json.dumps({'response':json.dumps(self.payload()),'done':True,'eval_count':10,'prompt_eval_count':20,'eval_duration':1000000000})+'\n').encode())
        else:raise AssertionError(req.full_url)
        return Response(json.dumps(r).encode())
    def test_annotated_quality_contracts(self):
        self.assertGreaterEqual(len(self.data['cases']),30)
        for case in self.data['cases']:
            with self.subTest(case=case['id']):self.assertEqual(contract(case,self.docs,self.root),case['expected'])
    def test_multi_problem_diagnostic_and_controlled_experiments(self):
        r=self.brain.run('Forêt Roblox : arbres artificiels, collisions gênantes, rendu de nuit',documents=self.docs)
        self.assertEqual(r['intent']['problems'],['collision','appearance','lighting'])
        for p in r['experiments']:
            self.assertTrue(all(p[k] for k in ('hypothesis','initial_conditions','changed_variable','controlled_variables','steps','measures','success_criteria','risks','rollback')))
            self.assertFalse(p['executed']);self.assertFalse(p['truth_verified'])
    def test_preview_pure_and_fixture_memory_forbidden(self):
        self.brain.run('Roblox collisions',documents=self.docs)
        self.assertFalse((self.root/'lab').exists())
        with self.assertRaises(ValueError):self.brain.run('Roblox collisions',apply=True,documents=self.docs)
    def test_warning_is_kept_with_instruction_and_exact_offset(self):
        d=next(d for d in self.docs if d['id']=='collision');p=next(p for p in ev.passages([d]) if 'determines' in p['text'])
        self.assertIn('Warning:',p['text']);self.assertEqual(d['text'][p['start']:p['end']],p['text'])
    def test_numeric_unknown_does_not_use_unrelated_version_or_count(self):
        r=self.brain.run('Quel FPS exact donne B3 dans Roblox ?',documents=self.docs)
        self.assertTrue(r['requested_value_unknown']);self.assertTrue(r['abstained'])
    def test_strict_model_schema_rejects_extra_tools(self):
        with self.assertRaises(ValueError):validate_model({**self.payload(),'tools':[{'cmd':'bad'}]},[],[],ev.analyze('Roblox'))
    def test_model_fake_numbers_and_wrong_source_are_not_facts(self):
        ps=ev.retrieve('Roblox collision',self.docs);p=next(p for p in ps if p['document_id']=='collision')
        data=self.payload();data['claims']=[{'text':'The tree reaches 900 FPS.','passage_ids':[p['id']],'kind':'SOURCE_SUPPORTED','engine':'Roblox','version':'unknown'},
                                           {'text':'CanCollide is definitely optimal.','passage_ids':['missing'],'kind':'SOURCE_SUPPORTED','engine':'Roblox','version':'unknown'}]
        r=validate_model(data,ps,self.docs,ev.analyze('Roblox collision'))
        self.assertTrue(all(c['support']=='UNSUPPORTED' for c in r['claims']));self.assertEqual(len(r['critique']),2)
        d={**self.docs[0],'text':'An authored fixture records a measured count of 900 triangles.'}
        import hashlib
        d['sha256']=hashlib.sha256(d['text'].encode()).hexdigest();p=ev.passages([d])[0]
        c=ev.verify({'text':'The measured count is 90 triangles.','kind':'SOURCE_SUPPORTED','passage_ids':[p['id']],'engine':'Roblox','version':'unknown'},[p],[d],ev.analyze('Roblox collision'))
        self.assertIn('unsupported_number',c['issues'])
        c=ev.verify({'text':'Set Range to 900.','kind':'SOURCE_SUPPORTED','passage_ids':[p['id']],'engine':'Roblox','version':'unknown'},[p],[d],ev.analyze('Roblox collision'))
        self.assertIn('numeric_relation_not_literal',c['issues']);self.assertEqual(c['support'],'UNSUPPORTED')
    def test_hostile_document_never_executes_or_changes_goals(self):
        before=self.cfg()
        with patch('subprocess.run',side_effect=AssertionError('source executed')):
            r=self.brain.run('Roblox collision',documents=self.docs)
        self.assertFalse(any(p['hostile'] for p in r['passages']));self.assertEqual(im.settings(self.root),before)
    def test_cache_survives_restart_without_model_and_source_change_invalidates(self):
        p=self.seed();r=self.brain.run('Roblox collision',apply=True)
        again=Intelligence(self.root).run('Roblox collision',apply=True)
        self.assertTrue(again['cache_hit']);self.assertEqual(again['key'],r['key'])
        source=json.loads(p.read_text());source['conditions']={'changed':True};p.write_text(json.dumps(source))
        changed=self.brain.run('Roblox collision',apply=True);self.assertNotEqual(changed['key'],r['key'])
        self.assertTrue(self.brain.get(r['key']))
    def test_config_change_invalidates_and_corruption_isolated(self):
        self.seed();r=self.brain.run('Roblox collision',apply=True);self.cfg(economy=False)
        next_r=self.brain.run('Roblox collision',apply=True);self.assertNotEqual(r['key'],next_r['key'])
        path=self.brain.path('results/'+r['key']+'.json');before=path.read_text();path.write_text(before.replace('attribution_only','forged'))
        with self.assertRaises(ValueError):self.brain.get(r['key'])
        self.assertTrue(self.brain.search('Roblox')['diagnostics']);self.assertTrue(self.brain.get(next_r['key']))
    def test_missing_service_falls_back_with_journal_and_reservations(self):
        self.seed();self.cfg(enabled=True,compact_model='fixture:compact')
        def failure(*args,**kwargs):raise OSError('fixture unavailable')
        r=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=failure)
        self.assertEqual(r['state'],'deterministic_fallback');self.assertTrue(r['facts']);self.assertTrue(list(self.brain.path('runs').glob('*.json')))
    def test_real_stream_contract_is_fixture_not_model_quality(self):
        self.seed();self.cfg(enabled=True,compact_model='fixture:compact',context_tokens=4096)
        r=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=self.opener)
        self.assertIsNone(r['model_error'],r);self.assertEqual(r['model_metrics']['tokens_per_second'],10)
        self.assertEqual(r['model_metrics']['server_version'],'FIXTURE-VERSION');self.assertEqual(r['model_calls_this_run'],1)
        before=json.loads((self.root/'lab/ocean/model-budget.json').read_text())['calls']
        again=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=self.opener)
        self.assertTrue(again['cache_hit']);self.assertEqual(json.loads((self.root/'lab/ocean/model-budget.json').read_text())['calls'],before)
    def test_shared_model_budget_failure_preserves_evidence(self):
        self.seed();self.cfg(enabled=True,compact_model='fixture:compact',context_tokens=4096)
        im.reserve_model(self.root)
        r=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=self.opener)
        self.assertEqual(r['model_stop_details']['resource'],'model_calls');self.assertEqual(r['model_calls_this_run'],0);self.assertTrue(r['facts'])
    def test_model_failure_is_retriable_and_no_success_cache(self):
        self.seed();self.cfg(enabled=True,compact_model='fixture:compact',context_tokens=4096)
        def bad(req,**kw):
            if req.full_url.endswith('/api/generate'):return Response(b'{"done":true,"response":"not json"}\n')
            return self.opener(req,**kw)
        r=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=bad)
        self.assertEqual(r['state'],'deterministic_fallback');self.assertFalse(self.brain.path('results/'+r['key']+'.json').exists())
        self.assertTrue(Intelligence(self.root).get(r['key'])['journal_only'])
        self.assertTrue(self.brain.search('Roblox')['incomplete_or_failed_runs'])
    def test_ollama_endpoint_no_proxy_redirect_or_download(self):
        for url in ('https://example.com','http://localhost:11434','http://127.0.0.1/a','http://user:pass@127.0.0.1:11434'):
            with self.assertRaises(ValueError):im.endpoint(url)
        with patch('agent.intelligence_models.build_opener') as builder:im.Ollama(im.DEFAULT)
        self.assertEqual(builder.call_args.args[1].proxies,{})
    def test_cancel_closes_stream_and_never_spawns_background_worker(self):
        event=threading.Event();event.set();client=im.Ollama(im.DEFAULT,self.opener,event)
        with self.assertRaises(InterruptedError):client.inventory()
    def test_context_limit_fails_before_wire(self):
        client=im.Ollama(im.DEFAULT,lambda *a,**k:(_ for _ in ()).throw(AssertionError('wire call')))
        with self.assertRaises(ValueError):client.generate({'name':'fixture:compact'},'x'*10000)
    def test_truncated_or_oversized_generation_is_rejected(self):
        for raw in (b'{"response":"{}","done":false}\n',b'x'*65537):
            client=im.Ollama(im.DEFAULT,lambda *a,**kw:Response(raw))
            with self.assertRaises(ValueError):client.generate({'name':'fixture:compact'},'short')
    def test_inventory_and_diagnostic_preserve_exact_digest_license(self):
        r=im.diagnose(self.root,True,'fixture:compact',self.opener)
        self.assertEqual(r['service'],'available');self.assertEqual(r['models'][0]['digest'],'test-digest');self.assertEqual(r['selected_metadata']['license'],'AUTHORED TEST LICENSE')
    def test_router_economy_and_unknown_model_do_not_recommend(self):
        cfg=self.cfg(compact_model='small',capable_model='large',economy=False);models=[{'name':'small','digest':'s'},{'name':'large','digest':'l'}]
        intent=ev.analyze('Roblox collisions et rendu artificiel de nuit')
        self.assertEqual(im.route(intent,cfg,models,{'memory_pressure':'high'})['selected']['name'],'small')
        self.assertEqual(im.route(intent,cfg,models,{'memory_pressure':'unknown'})['selected']['name'],'large')
        self.assertIsNone(im.route(intent,cfg,[],{'memory_pressure':'unknown'})['recommended_default'])
    def test_no_semantic_index_graceful_and_model_digest_change_invalidates(self):
        ps=ev.retrieve('Roblox',self.docs);selected,state=semantic.retrieve(self.root,'Roblox',self.docs,'hybrid',ps,5,self.opener)
        self.assertEqual(state,'missing_index_lexical_fallback')
        p=self.brain.path('embeddings.json');p.parent.mkdir(parents=True);p.write_text(json.dumps({'model':{'name':'other','digest':'old'},'vectors':{}}))
        with patch('agent.intelligence_semantic.identity',return_value={'name':'other','digest':'new'}):
            _,state=semantic.retrieve(self.root,'Roblox',self.docs,'semantic',ps,5,self.opener)
        self.assertEqual(state,'unavailable_embeddings_lexical_fallback')
    def test_mcp_old_contracts_and_permissions(self):
        self.assertEqual(len(Server(self.root,v11=True).tools),22);server=Server(self.root,v111=True)
        self.assertEqual(len(server.tools),27)
        with self.assertRaises(PermissionError):server.dispatch('synthesize_technical',{'question':'Roblox','apply':True})
        r=server.dispatch('get_intelligence_brief',{'question':'Roblox','token_budget':500});self.assertFalse(r['truth_verified'])
    def test_stdio_real_process_and_bounded_brief(self):
        self.seed();r=self.brain.run('Roblox collision',apply=True)
        brief=self.brain.brief('Roblox collision',500,r['key']);self.assertLessEqual(len(json.dumps(brief,ensure_ascii=False)),1800)
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'test','version':'1'}}},
                  {'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'},
                  {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'get_intelligence_brief','arguments':{'question':'Roblox collision','token_budget':500}}}]
        p=subprocess.run([sys.executable,str(REPO/'vdn_mcp.py'),'--root',str(self.root),'--v111'],cwd=self.root,input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,0,p.stderr);rs=[json.loads(s) for s in p.stdout.splitlines()];self.assertEqual(len(rs[1]['result']['tools']),27)
        self.assertEqual(rs[0]['result']['serverInfo']['version'],'11.1.0');self.assertFalse(rs[2]['result']['structuredContent']['truth_verified'])
    def test_path_escape_and_symlink_refused(self):
        with self.assertRaises(ValueError):self.brain.get('../../escape')
        outside=Path(tempfile.mkdtemp());self.addCleanup(shutil.rmtree,outside)
        folder=self.root/'lab/ocean';folder.mkdir(parents=True)
        try:(folder/'intelligence').symlink_to(outside,target_is_directory=True)
        except OSError:self.skipTest('symlinks unavailable')
        with self.assertRaises(ValueError):self.brain.path('result.json')
    def test_failed_experiment_reappears_without_verification_promotion(self):
        lab=LabStore(self.root);r=lab.create('Roblox collisions','fixture failed proxy','unknown',{},{});r=lab.transition(r['id'],'PLANNED');r=lab.transition(r['id'],'RUNNING')
        lab.record_result(r['id'],'FAILED',{},['Authored failure fixture'],errors=['blocked path'])
        result=self.brain.run('Roblox collisions')
        self.assertTrue(result['experiment_memory']['failed_methods']);self.assertFalse(result['truth_verified'])
    def test_compute_cap_reserved_and_not_reset_by_retry(self):
        import datetime as dt
        p=self.brain.path('compute.json');p.parent.mkdir(parents=True);p.write_text(json.dumps({'date':dt.datetime.now(dt.timezone.utc).date().isoformat(),'reserved_s':60}))
        with self.assertRaises(budget.BudgetExhausted):im.operation(self.root,lambda:None)
        self.assertEqual(json.loads(p.read_text())['reserved_s'],60)
    def test_remote_private_inputs_never_route_and_zero_cost_blocks_before_call(self):
        cfg=self.cfg(remote_allowed=True);self.assertIsNone(im.remote_candidate(self.root,cfg))
        with self.assertRaises(budget.BudgetExhausted):im.reserve_model(self.root,True)
        self.assertFalse((self.root/'lab/ocean/model-budget.json').exists())
    def test_explicit_public_remote_reuses_existing_adapter_and_cost_ledger(self):
        self.seed();self.cfg(enabled=True,remote_allowed=True,sensitivity='public',context_tokens=4096)
        p=self.root/'config/v10.json';c=json.loads(p.read_text());c['network_enabled']=True;c['models']['remote'].update(enabled=True,model='fixture-remote',endpoint='https://fixture.invalid');p.write_text(json.dumps(c))
        p=self.root/'config/ocean.json';c=json.loads(p.read_text());c.update(model_backend='remote',max_cost_usd=1,remote_reservation_usd=.1);p.write_text(json.dumps(c))
        with patch('agent.models.infer',return_value={'state':'model_claims','claims':self.payload()}):
            r=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=self.opener)
        self.assertEqual(r['route']['level'],3);self.assertIsNone(r['model_error']);self.assertIsNone(r['metrics']['api_cost_usd'])
        self.assertEqual(json.loads((self.root/'lab/ocean/model-budget.json').read_text())['reserved_cost_usd'],.1)
        p=self.root/'config/v10.json';c=json.loads(p.read_text());c['models']['remote']['endpoint']='https://user:pass@fixture.invalid';p.write_text(json.dumps(c))
        self.assertIsNone(im.remote_candidate(self.root,im.settings(self.root)))
    def test_cancel_during_stream_closes_response(self):
        event=threading.Event()
        class CancelResponse(Response):
            def readline(self,*a):event.set();return b'{"response":"{}","done":true}\n'
        response=CancelResponse(b'');client=im.Ollama(im.DEFAULT,lambda *a,**k:response,event)
        with self.assertRaises(InterruptedError):client.generate({'name':'fixture'},'short')
        self.assertTrue(response.closed)
    def test_crash_after_evidence_save_retains_journal_and_source(self):
        self.seed();original=self.brain.write
        def crash(path,value,create_only=False):original(path,value,create_only);raise KeyboardInterrupt()
        with patch.object(self.brain,'write',side_effect=crash):
            with self.assertRaises(KeyboardInterrupt):self.brain.run('Roblox collision',apply=True)
        self.assertEqual(json.loads(next(self.brain.path('runs').glob('*.json')).read_text())['state'],'EVIDENCE_READY')
        key=json.loads(next(self.brain.path('runs').glob('*.json')).read_text())['fingerprint']
        self.assertEqual(self.brain.brief('Roblox collision',500,key)['state'],'EVIDENCE_READY')
        self.assertTrue(Intelligence(self.root).run('Roblox collision',apply=True)['facts'])
    def test_model_digest_change_cannot_reuse_prior_success_or_reset_budget(self):
        self.seed();self.cfg(enabled=True,compact_model='fixture:compact',context_tokens=4096)
        first=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=self.opener)
        def changed(req,**kw):
            if req.full_url.endswith('/api/tags'):return Response(json.dumps({'models':[{'name':'fixture:compact','digest':'changed-test-digest'}]}).encode())
            return self.opener(req,**kw)
        second=self.brain.run('Roblox collision',apply=True,allow_model=True,opener=changed)
        self.assertNotEqual(first['key'],second['key']);self.assertFalse(second['cache_hit']);self.assertEqual(second['model_stop_details']['resource'],'model_calls')
    def test_v11_collector_opt_in_uses_one_pipeline_and_same_session_budget(self):
        from agent.ocean import Ocean
        from tests.test_ocean import Response as WebResponse,FIXTURE
        self.cfg(enabled=True);p=self.root/'config/v10.json';cfg=json.loads(p.read_text());cfg['network_enabled']=True;p.write_text(json.dumps(cfg))
        o=Ocean(self.root);g=o.prepare('Forêt Roblox avec collisions',apply=True)
        def web(req,**kw):return WebResponse(req.full_url,'User-agent: *\nAllow: /\n' if req.full_url.endswith('/robots.txt') else FIXTURE)
        with patch('agent.intelligence_models.Ollama.inventory',return_value=[]),patch('agent.ocean.Ocean._model',side_effect=AssertionError('duplicate legacy inference')):
            r=o.advance(g['id'],apply=True,allow_network=True,opener=web)
        self.assertTrue(list(self.brain.path('results').glob('*.json')));self.assertLessEqual(r['research']['session']['http_calls'],6)
        self.assertEqual(r['research']['queue']['counts']['running'],0)
    def test_embedding_index_semantic_and_hybrid_fixture_routes(self):
        self.seed();model={'name':'fixture:embed','digest':'fixture-digest'}
        def vectors(root,texts):return [[1.0,0.0] if 'collision' in s.lower() or 'CanCollide' in s else [0.0,1.0] for s in texts]
        with patch('agent.intelligence_semantic.identity',return_value=model),patch('agent.ocean_semantic.vectors',side_effect=vectors):
            indexed=semantic.index(self.root,True);self.assertEqual(indexed['state'],'indexed')
            docs=ev.documents(self.root);lex=ev.retrieve('collision',docs)
            for mode in ('semantic','hybrid'):
                selected,state=im.operation(self.root,lambda:semantic.retrieve(self.root,'collision',docs,mode,lex,5))
                self.assertTrue(selected);self.assertEqual(state,'real_local_embeddings_'+mode)
        # The adapter is mocked: result label is an execution path, not real quality evidence.
    def test_explicit_obsidian_memory_export_excludes_summaries_from_rag(self):
        from agent import obsidian
        from agent.corpus import scan_notes
        self.seed();self.brain.run('Roblox collision',apply=True)
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'vault';r=obsidian.sync(self.root,dest,apply=True,extra_pages=self.brain.pages())
            self.assertEqual(r['state'],'committed');self.assertTrue((dest/'knowledge/_VDN-Intelligence.md').exists());self.assertFalse(scan_notes(dest))


if __name__=='__main__':unittest.main()
