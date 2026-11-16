import contextlib
import io
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from agent import budget,ocean_knowledge,obsidian,lab_plan
from agent.ocean import Ocean
from agent.ocean_api import OceanAPI,pages
from agent.ocean_web import OceanWeb,public_addresses
from agent.research_session import ResearchSessions
from agent.lab_store import LabStore
from agent.mcp_v8 import Server
from agent.v11 import tick
from tests.test_autonomy import make_root

REPO=Path(__file__).resolve().parents[1]
FIXTURE='''# Synthetic Roblox documentation fixture
MeshPart CollisionFidelity describes collision geometry used by the physics engine.
CanCollide determines whether this part participates in physical collisions.
CollisionGroup is a documented property; test behavior with the actual player controller.
Foliage cards transparency and SurfaceAppearance textures need engine compatibility checks.
[Foliage cards](https://create.roblox.com/docs/foliage-cards.md)
[Collisions](https://create.roblox.com/docs/collisions.md)
'''


class Response:
    def __init__(self,url,body,status=200):self.url=url;self.body=body.encode('utf-8');self.headers={};self.status=status
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def geturl(self):return self.url
    def read(self,n):return self.body[:n]


class OceanTests(unittest.TestCase):
    def setUp(self):
        self.root=make_root();self.addCleanup(shutil.rmtree,self.root);self.ocean=Ocean(self.root);self.calls=[]
        p=self.root/'config/v10.json';cfg=json.loads(p.read_text());cfg['network_enabled']=True;p.write_text(json.dumps(cfg))
        p=self.root/'config/ocean.json';cfg=json.loads(p.read_text());cfg['providers']['roblox']['seeds']=['https://create.roblox.com/docs/collisions.md'];p.write_text(json.dumps(cfg))
    def opener(self,req,**kw):
        self.calls.append(req.full_url)
        return Response(req.full_url,'User-agent: *\nAllow: /\n' if req.full_url.endswith('robots.txt') else FIXTURE)
    def prepare(self):return self.ocean.prepare('Créer une forêt Roblox avec collisions et lampe torche',apply=True)
    def run_goal(self):
        g=self.prepare();r=self.ocean.advance(g['id'],apply=True,allow_network=True,opener=self.opener);return g,r
    def test_planner_is_pure_and_independent_research_does_not_block_on_trunk(self):
        r=self.ocean.prepare('Créer une forêt enneigée nocturne Roblox')
        self.assertEqual(len(r['plan']['nodes']),12);self.assertFalse((self.root/'lab').exists())
        self.assertTrue(all(not n['requires'] for n in r['plan']['nodes']))
        self.assertTrue(all(n['production_prerequisites'] for n in r['plan']['nodes']))
    def test_grounded_collision_candidate_is_useful_and_unverified(self):
        g,r=self.run_goal();cards=ocean_knowledge.cards(self.root)
        self.assertTrue(cards,r);collision=next(c for c in cards if c['facet']=='collision')
        self.assertIn('CanCollide',collision['documented_tokens']);self.assertIn('SOURCE_SUPPORTED',collision['states'])
        self.assertFalse(collision['truth_verified']);self.assertGreaterEqual(len(collision['procedure']),6)
        self.assertTrue(any('troncs' in s['text'] for s in collision['procedure']))
        self.assertTrue(all(c['quote'] in FIXTURE for c in collision['claims']))
        self.assertLessEqual(r['research']['session']['http_calls'],6)
        self.assertEqual(r['research']['queue']['counts']['running'],0)
    def test_second_goal_reuses_candidates_and_has_no_prepare_http(self):
        self.run_goal();count=len(self.calls);before=len(ocean_knowledge.cards(self.root))
        g=self.ocean.prepare('Optimiser les collisions dans ma forêt Roblox',apply=True)
        self.assertGreaterEqual(g['queries_avoided_lower_bound'],1);self.assertEqual(len(self.calls),count)
        self.ocean.advance(g['id'],apply=True,allow_network=True,opener=self.opener)
        self.assertEqual(len([c for c in ocean_knowledge.cards(self.root) if c['facet']=='collision']),1)
    def test_pause_stop_and_adoption_never_reset_counters(self):
        g=self.prepare();self.ocean.control(g['id'],'pause',apply=True)
        self.assertEqual(self.ocean.advance(g['id'],apply=True,allow_network=True,opener=self.opener)['state'],'PAUSED');self.assertFalse(self.calls)
        self.ocean.control(g['id'],'resume',apply=True);self.ocean.control(g['id'],'stop',apply=True)
        with self.assertRaises(ValueError):self.ocean.control(g['id'],'resume',apply=True)
        sid=ResearchSessions(self.root).prepare('forêt Roblox',apply=True)['id'];p=ResearchSessions(self.root).session_path(sid);before=p.read_bytes()
        self.ocean.adopt(sid,apply=True);self.assertEqual(p.read_bytes(),before)
    def test_interrupt_after_note_commit_resumes_without_duplicate_or_counter_reset(self):
        g=self.prepare();original=ocean_knowledge.write_card
        def interrupted(*args,**kw):original(*args,**kw);raise KeyboardInterrupt()
        with patch('agent.ocean_knowledge.write_card',side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):self.ocean.advance(g['id'],apply=True,allow_network=True,opener=self.opener)
        count=len(ocean_knowledge.cards(self.root));before=ResearchSessions(self.root).get(g['id'])['http_calls']
        r=self.ocean.advance(g['id'],apply=True,allow_network=True,opener=self.opener)
        self.assertGreaterEqual(r['research']['session']['http_calls'],before)
        self.assertEqual(len([c for c in ocean_knowledge.cards(self.root) if c['facet']=='collision']),1)
    def test_cache_and_robots_enforced_and_attempt_is_not_success(self):
        web=OceanWeb(self.root,self.opener);guard=budget.Budget(60,4)
        with budget.using(guard):
            doc=web.get('https://create.roblox.com/docs/collisions.md','roblox');web.get('https://create.roblox.com/docs/collisions.md','roblox')
        self.assertEqual(guard.http_calls,2);self.assertEqual(web.cache_hits,1)
        root2=make_root();self.addCleanup(shutil.rmtree,root2)
        blocked=OceanWeb(root2,lambda req,**kw:Response(req.full_url,'User-agent: *\nDisallow: /\n'))
        with budget.using(budget.Budget(60,3)):
            with self.assertRaises(Exception):blocked.get('https://create.roblox.com/docs/collisions.md','roblox')
    def test_robots_auth_denied_and_source_corruption_refused(self):
        def denied(req,**kw):raise HTTPError(req.full_url,403,'fixture denied',{},None)
        with budget.using(budget.Budget(60,3)):
            with self.assertRaises(Exception):OceanWeb(self.root,denied).get('https://create.roblox.com/docs/collisions.md','roblox')
        web=OceanWeb(self.root,self.opener)
        with budget.using(budget.Budget(60,3)):web.get('https://create.roblox.com/docs/collisions.md','roblox')
        p=next((self.root/'lab/ocean/sources').glob('*.json'));r=json.loads(p.read_text());r['text']='corrupt';p.write_text(json.dumps(r))
        with self.assertRaises(ValueError):web.get('https://create.roblox.com/docs/collisions.md','roblox')
    def test_public_dns_mixed_private_and_literal_ips_refused(self):
        for host in ('127.0.0.1','::1'):
            with self.assertRaises(ValueError):public_addresses(host)
        rows=[(socket.AF_INET,socket.SOCK_STREAM,6,'',('93.184.216.34',443)),(socket.AF_INET,socket.SOCK_STREAM,6,'',('127.0.0.1',443))]
        with patch('socket.getaddrinfo',return_value=rows):
            with self.assertRaises(ValueError):public_addresses('fixture.example')
        with patch('socket.getaddrinfo',return_value=rows[:1]):self.assertEqual(public_addresses('fixture.example'),['93.184.216.34'])
    def test_provider_permission_paths_and_storage(self):
        web=OceanWeb(self.root,self.opener)
        for url in ('http://create.roblox.com/docs/a','https://127.0.0.1/a','https://create.roblox.com:444/a','https://user:pass@create.roblox.com/a','https://create.roblox.com/a?token=x'):
            with self.assertRaises(Exception):web.get(url,'roblox')
        web.cfg['storage_bytes']=0
        with self.assertRaises(budget.BudgetExhausted):web.storage_check(1)
        with self.assertRaises(ValueError):web.path('../escape')
    def test_model_unmatched_claim_rejected_and_contradictions_are_flags(self):
        web=OceanWeb(self.root,self.opener)
        with budget.using(budget.Budget(60,3)):doc=web.get('https://create.roblox.com/docs/collisions.md','roblox')
        card=ocean_knowledge.synthesis('forest','collision',[doc],{'state':'model_claims','claims':{'evidence':[{'source_id':'source-1','quote':'invented 900 FPS'}],'questions':['What remains unknown?']}})
        self.assertTrue(any('rejected' in s for s in card['uncertainties']));self.assertFalse(any('900' in c['quote'] for c in card['claims']))
        other={**doc,'text':doc['text']+'\nSources disagree on the collision behavior.','published':'2000-01-01'}
        c=ocean_knowledge.synthesis('forest','collision',[other]);self.assertIn('DISPUTED',c['states']);self.assertIn('OUTDATED',c['states'])
    def test_mcp_stdio_and_permissions_and_bounded_brief(self):
        self.run_goal();api=OceanAPI(self.root)
        b=api.get_ocean_brief('Pourquoi mon personnage se bloque contre les sapins ?',500)
        self.assertLessEqual(len(json.dumps(b,ensure_ascii=False)),1800)
        self.assertFalse(b['truth_verified'])
        server=Server(self.root,v11=True)
        with self.assertRaises(PermissionError):server.dispatch('prepare_ocean',{'goal':'forêt Roblox','apply':True})
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'ocean-test','version':'1'}}},
                  {'jsonrpc':'2.0','method':'notifications/initialized'},
                  {'jsonrpc':'2.0','id':2,'method':'tools/list'},
                  {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'get_ocean_brief','arguments':{'goal':'collisions sapins'}}}]
        r=subprocess.run([sys.executable,str(REPO/'vdn_mcp.py'),'--root',str(self.root),'--v11'],input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,capture_output=True,cwd=self.root,timeout=20)
        self.assertEqual(r.returncode,0,r.stderr);responses=[json.loads(s) for s in r.stdout.splitlines()]
        self.assertEqual(len(responses),3);self.assertEqual(responses[0]['result']['serverInfo']['version'],'11.0.0')
        self.assertEqual(len(responses[1]['result']['tools']),22)
        self.assertFalse(responses[2]['result']['isError']);self.assertFalse(responses[2]['result']['structuredContent']['truth_verified'])
    def test_obsidian_idempotent_export_and_legacy_read_only(self):
        self.run_goal();before={p:p.read_bytes() for p in (self.root/'knowledge').rglob('*.md')}
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'bundle';extra={**lab_plan.pages(self.root),**pages(self.root)}
            self.assertEqual(obsidian.sync(self.root,dest,apply=True,extra_pages=extra)['state'],'committed')
            self.assertEqual(obsidian.sync(self.root,dest,apply=True,extra_pages=extra)['state'],'unchanged')
            from agent.corpus import scan_notes
            self.assertEqual(len(scan_notes(dest)),len(ocean_knowledge.cards(self.root)))
        ocean_knowledge.legacy_view(self.root)
        self.assertTrue(all(p.read_bytes()==data for p,data in before.items()))
    def test_scheduler_is_off_without_any_runtime_writes(self):
        self.assertEqual(tick(self.root,'scheduled',True)['state'],'disabled')
        self.assertFalse((self.root/'lab').exists())
    def test_fixture_configuration_ignores_personal_network_and_model_flags(self):
        from tests import test_autonomy
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d);shutil.copytree(REPO/'config',fake/'config')
            p=fake/'config/v10.json';cfg=json.loads(p.read_text());cfg['network_enabled']=True;p.write_text(json.dumps(cfg));before=p.read_bytes()
            with patch.object(test_autonomy,'REPO',fake):root=make_root()
            self.addCleanup(shutil.rmtree,root)
            self.assertFalse(json.loads((root/'config/v10.json').read_text())['network_enabled'])
            self.assertEqual(p.read_bytes(),before)


if __name__=='__main__':unittest.main()
