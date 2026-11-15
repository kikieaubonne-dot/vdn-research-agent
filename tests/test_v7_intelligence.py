"""Offline acceptance cases for evidence-aware recursive research."""
import json
import shutil
import unittest
import gzip
import io
import time
from unittest.mock import patch
from urllib.error import URLError
from urllib.request import Request

from agent import autonomy, budget, decomposition, evaluation, knowledge, meta, planner, priority, providers, run
from agent.research_queue import ResearchQueue, item_key, load_config
from agent.recursive_gaps import propose
from agent.storage import atomic_write
from tests.test_autonomy import make_root, FakeDocs


class V7Tests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()
        self.addCleanup(shutil.rmtree, self.root)

    def configure(self, section, **values):
        path = self.root / 'config' / 'autonomy.json'
        data = json.loads(path.read_text())
        data[section].update(values)
        path.write_text(json.dumps(data))

    def note(self, body, **fields):
        return knowledge.dump_frontmatter({'id': 'vdn-test', 'status': 'documente',
                    'sources': ['https://create.roblox.com/docs/test'], 'source_tier': 1, **fields}) + '\n' + body

    def test_simple_question_uses_existing_queue(self):
        p = decomposition.plan(self.root, 'SpotLight shadows', 'lighting')
        self.assertIsNone(p['profile'])
        self.assertEqual(p['added'], 1)
        self.assertEqual(len(ResearchQueue(self.root).next_batch(4)), 1)

    def test_complex_question_has_eleven_branches_and_prerequisites(self):
        p = decomposition.plan(self.root, 'Comment creer un sapin enneige realiste performant dans Roblox ?', 'spruce')
        self.assertEqual(len(p['nodes']), 11)
        self.assertEqual(p['added'], 11)
        q = ResearchQueue(self.root)
        ready = q.next_batch(12)
        self.assertEqual([it['query'] for it in ready], ['tree trunk geometry'])
        self.assertEqual(len(q.summary()['blocked']), 10)
        q.mark_done(ready[0], {'created': 1})
        self.assertEqual([it['query'] for it in q.next_batch(12)], ['tree branch structure'])
        self.assertTrue(all(2 <= len(n['query'].split()) <= 4 for n in p['nodes']))

    def test_unproductive_prerequisite_does_not_unlock_dependents(self):
        decomposition.plan(self.root, 'How to create a realistic snowy pine tree in Roblox?', 'spruce')
        q = ResearchQueue(self.root)
        q.mark_done(q.next_batch(1)[0], {'created': 0})
        self.assertEqual(q.next_batch(5), [])
        self.assertEqual(len(q.summary()['blocked']), 10)

    def test_already_planned_question_does_not_duplicate(self):
        question = 'How to create a realistic snowy pine tree in Roblox?'
        decomposition.plan(self.root, question, 'spruce')
        before = ResearchQueue(self.root).data
        self.assertEqual(decomposition.plan(self.root, question, 'spruce')['added'], 0)
        self.assertEqual(ResearchQueue(self.root).data, before)

    def test_plan_budget_refuses_before_writing_queue(self):
        self.configure('queue', max_plan_nodes=3)
        with self.assertRaises(ValueError):
            decomposition.plan(self.root, 'How to create a realistic snowy pine tree in Roblox?', 'spruce')
        self.assertFalse((self.root / 'output' / 'queue.json').exists())

    def test_invalid_dependencies_in_profile_refused(self):
        path = self.root / 'config' / 'research_domains.json'
        data = json.loads(path.read_text())
        data['profiles'][0]['nodes'][0]['requires'] = ['lighting']
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            decomposition.plan(self.root, 'How to create a realistic snowy pine tree in Roblox?', 'spruce')
        self.assertFalse((self.root / 'output' / 'queue.json').exists())

    def test_followup_facet_survives_planner_shortening(self):
        for f in propose('foliage alpha tree cards', [{'topical': .9, 'technical': 0, 'roblox': False}], 2):
            self.assertLessEqual(len(f['query'].split()), 4)
            self.assertEqual(planner.variants(f['query'])['terms'], f['query'])
        self.assertNotEqual(item_key('', 'SpotLight'), item_key('', 'SpotLight limitations'))

    def test_total_children_capped_across_many_notes_and_rejections(self):
        self.configure('queue', max_children_per_item=2)
        p = FakeDocs()
        original = p.search
        p.search = lambda query, limit: original(query, limit) + original(query + ' settings', limit)
        result = autonomy.cycle(self.root, provs={'roblox_docs': p}, max_items=1)
        q = ResearchQueue(self.root)
        parent = next(it for it in q.data['items'].values() if it['status'] == 'done')
        self.assertGreater(result['created'], 0)
        self.assertLessEqual(sum(it.get('parent') == parent['key'] for it in q.data['items'].values()), 2)

    def test_stagnation_stops_rejected_branch(self):
        self.configure('queue', max_depth=5, stagnation_limit=2)
        q = ResearchQueue(self.root)
        q.add('spruce', 'tree foliage cards', 10)
        q.save()
        def insufficient(root, **kwargs):
            return {'fetched': 1, 'rejected_candidates': [{'topical': .9, 'technical': .01, 'roblox': True}]}
        first = autonomy.cycle(self.root, max_items=1, research_fn=insufficient)
        self.assertEqual(first['followups_added'], 1)
        second = autonomy.cycle(self.root, max_items=1, research_fn=insufficient)
        self.assertEqual(second['followups_added'], 0)
        q = ResearchQueue(self.root)
        self.assertTrue(any((it.get('result') or {}).get('expansion_stop') == 'stagnation' for it in q.data['items'].values()))

    def test_priority_prerequisite_leverage_and_cost_are_explained(self):
        q = ResearchQueue(self.root)
        q.add('spruce', 'tree geometry', 10)
        a = q.data['items'][item_key('', 'tree geometry')]
        q.add('spruce', 'tree materials', 10)
        q.add('spruce', 'tree snow', 10, dependencies=[a['key']])
        self.assertEqual(q.next_batch(1)[0]['key'], a['key'])
        report = q.summary()['next'][0]['ranking']
        self.assertEqual(report['criteria']['unblocks'], 1)
        self.assertIn('source_quality', report['unknown'])
        low_cost = {**a, 'research_signals': {'estimated_cost': 1}}
        high_cost = {**a, 'research_signals': {'estimated_cost': 10}}
        self.assertLess(priority.explain(low_cost, [])['rank'], priority.explain(high_cost, [])['rank'])

    def test_priorities_reevaluated_when_evidence_arrives(self):
        q = ResearchQueue(self.root)
        for query in ('tree alpha', 'tree bark'):
            q.add('spruce', query, 10)
        old = q.next_batch(1)[0]
        meta.save_json(self.root / 'output' / 'knowledge_evaluation.json', {'notes': [
            {'id': 'new-evidence', 'queries': [old['query']], 'source_tier': 1, 'gaps': []}]})
        self.assertNotEqual(q.next_batch(1)[0]['key'], old['key'])

    def test_long_unsourced_note_is_not_evidence(self):
        result = evaluation.evaluate_note(self.note('# Guide\n' + 'A long generic tutorial. ' * 1000))
        self.assertEqual(result['state'], 'non_resolu')
        self.assertFalse(result['truth_verified'])
        self.assertFalse(result['diagnostics']['source_traceability'])
        self.assertIn('actionable_steps', result['gaps'])

    def test_cited_steps_are_probable_not_verified(self):
        body = ('## Extraits justificatifs\n\n'
                '> « Set the MeshPart transparency property to 0.5 for the foliage cards. »\n'
                '> — [source](https://create.roblox.com/docs/test)\n')
        r = evaluation.evaluate_note(self.note(body, tested_in_studio='oui', status='valide'))
        self.assertEqual(r['state'], 'probable')
        self.assertEqual(r['technical_accuracy'], 'non_verifiee')
        self.assertFalse(r['truth_verified'])
        self.assertTrue(r['warnings'])

    def test_explicit_source_contradiction_remains_unresolved(self):
        r = evaluation.evaluate_note(self.note('## Sources contradictoires\nSources disagree on the supported limit.'))
        self.assertTrue(r['conflict'])
        self.assertEqual(r['state'], 'non_resolu')

    def test_no_reliable_source_or_results_creates_no_claim(self):
        s = autonomy.cycle(self.root, max_items=1, research_fn=lambda *a, **k: {'returned': 0})
        self.assertEqual(s['created'], 0)
        self.assertEqual(s['followups_added'], 0)
        self.assertEqual(s['items'][0]['status'], 'done')

    def test_http_retries_respect_shared_call_budget(self):
        guard = budget.Budget(60, 2)
        with budget.using(guard), patch('agent.providers.urlopen', side_effect=URLError('offline')) as urlopen, patch('agent.budget.time.sleep'):
            with self.assertRaises(budget.BudgetExhausted):
                providers.http_get('https://create.roblox.com/docs/test.md', retries=5)
        self.assertEqual(urlopen.call_count, 2)
        self.assertEqual(guard.http_calls, 2)

    def test_deadline_stops_request_before_network(self):
        with patch('agent.budget.time.monotonic', return_value=10) as clock:
            guard = budget.Budget(2, 5)
            clock.return_value = 12
            with budget.using(guard), patch('agent.providers.urlopen') as urlopen:
                with self.assertRaises(budget.BudgetExhausted):
                    providers.http_get('https://create.roblox.com/docs/test.md')
            urlopen.assert_not_called()

    def test_http_budget_persisted_before_interrupt(self):
        def interrupted(root, **kwargs):
            budget.request()
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            autonomy.cycle(self.root, max_items=1, research_fn=interrupted)
        self.assertEqual(ResearchQueue(self.root).daily()['http_calls'], 1)

    def test_configured_item_cap_cannot_be_overridden(self):
        self.configure('cycle', max_items=1)
        s = autonomy.cycle(self.root, max_items=20, research_fn=lambda *a, **k: {})
        self.assertEqual(len(s['items']), 1)

    def test_invalid_configuration_fails_before_work(self):
        for value in (-1, float('nan'), float('inf'), True):
            self.configure('cycle', max_http_calls=value)
            with self.assertRaises(ValueError):
                load_config(self.root)

    def test_atomic_replacement_failure_preserves_original(self):
        path = self.root / 'user-note.md'
        path.write_text('user knowledge', encoding='utf-8')
        with patch('agent.storage.os.replace', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                atomic_write(path, 'new data')
        self.assertEqual(path.read_text(), 'user knowledge')
        self.assertEqual(list(self.root.glob('.*.tmp')), [])

    def test_create_only_never_overwrites_existing_note(self):
        path = self.root / 'user-note.md'
        path.write_text('user knowledge', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            atomic_write(path, 'new data', create_only=True)
        self.assertEqual(path.read_text(), 'user knowledge')

    def test_active_system_lock_cannot_be_stolen_when_metadata_is_stale(self):
        with autonomy.Lock(self.root, 7200) as lock:
            data = json.loads(lock.path.read_text())
            data['ts'] = time.time() - 99999
            lock.path.write_text(json.dumps(data))
            with self.assertRaises(autonomy.Busy):
                with autonomy.Lock(self.root, 7200):
                    pass

    def test_redirect_refused_before_contacting_untrusted_host(self):
        req = Request('https://api.github.com/test', headers={'Authorization': 'test-value'})
        with self.assertRaises(providers.FetchError):
            providers.CheckedRedirect().redirect_request(req, None, 302, 'Found', {}, 'https://example.org/stolen')

    def test_cross_host_redirect_strips_authorization_and_uses_budget(self):
        req = Request('https://api.github.com/test', headers={'Authorization': 'test-value'})
        guard = budget.Budget(60, 1)
        with budget.using(guard):
            redirected = providers.CheckedRedirect().redirect_request(req, None, 302, 'Found', {},
                                                                      'https://raw.githubusercontent.com/a/b')
        self.assertIsNone(redirected.get_header('Authorization'))
        self.assertEqual(guard.http_calls, 1)

    def test_decompression_size_bounded(self):
        class Response(io.BytesIO):
            headers = {'Content-Encoding': 'gzip'}
            def geturl(self):
                return 'https://create.roblox.com/docs/test.md'
        with patch('agent.providers.urlopen', return_value=Response(gzip.compress(b'x' * 10000))):
            with self.assertRaisesRegex(providers.FetchError, 'decompressee'):
                providers.http_get('https://create.roblox.com/docs/test.md', max_bytes=100)

    def test_invalid_source_never_creates_knowledge(self):
        with self.assertRaises(providers.FetchError):
            knowledge.write_note(self.root, knowledge.Registry(self.root), {'id': 'spruce'}, 'tree',
                                 {'url': 'javascript:alert(1)'}, {}, {})
        self.assertFalse((self.root / 'knowledge').exists())

    def test_shallow_old_note_enqueues_targeted_bounded_research_without_rewrite(self):
        path = self.root / 'knowledge' / 'old-note.md'
        path.parent.mkdir()
        path.write_text(self.note('# Old note\nUnresolved method.', subdomain='spruce', queries=['tree mesh geometry']))
        before = path.read_bytes()
        s = autonomy.cycle(self.root, max_items=0)
        self.assertGreater(s['reevaluations_added'], 0)
        self.assertLessEqual(s['reevaluations_added'], 6)
        self.assertEqual(path.read_bytes(), before)

    def test_legacy_query_key_remains_deduplicated_after_facet_fix(self):
        q = ResearchQueue(self.root)
        query = 'SpotLight limitations'
        q.add('lighting', query, 9)
        item = q.data['items'].pop(item_key('', query))
        item['key'] = 'legacy-key'
        q.data['items']['legacy-key'] = item
        self.assertFalse(q.add('lighting', query, 9)[0])

    def test_full_complex_plan_completes_across_bounded_cycles_with_local_sources(self):
        self.configure('queue', max_depth=1)
        decomposition.plan(self.root, 'How to create a realistic snowy pine tree in Roblox?', 'spruce')
        class DistinctDocs(FakeDocs):
            def fetch(self, url):
                subject = url.rsplit('/', 1)[-1].replace('-', ' ')
                # Distinct evidence for each prerequisite, rather than the shared
                # SpotLight excerpts in the general-purpose FakeDocs fixture.
                text = (f'# {subject}\n\n'
                        f'Set the MeshPart for {subject} transparency = 0.5 in Roblox Studio to inspect the texture.\n'
                        f'Export the {subject} mesh with Blender FBX and apply the material to the mesh.\n'
                        f'Test the {subject} mesh rendering with SurfaceAppearance and inspect draw calls.\n')
                return {'title': subject, 'text': text, 'official': True, 'meta': {}}
        for _ in range(3):
            s = autonomy.cycle(self.root, provs={'roblox_docs': DistinctDocs()})
            self.assertLessEqual(len(s['items']), 4)
        q = ResearchQueue(self.root)
        nodes = [it for it in q.data['items'].values() if it['origin'] == 'decomposition']
        self.assertEqual(len(nodes), 11)
        self.assertTrue(all(it['status'] == 'done' for it in nodes))
        self.assertEqual(q.daily()['items'], 11)

    def test_known_source_supplies_prerequisite_without_rewriting(self):
        p = FakeDocs()
        q = ResearchQueue(self.root)
        q.add('spruce', 'tree mesh', 10)
        q.save()
        first = autonomy.cycle(self.root, provs={'roblox_docs': p}, max_items=1)
        path = self.root / first['items'][0]['notes'][0]['path']
        before = path.read_bytes()
        q = ResearchQueue(self.root)
        q.add('spruce', 'tree geometry', 20)
        q.save()
        first_url = p.search('tree mesh')[0]['url']
        p.search = lambda query, limit: [{'url': first_url, 'title': 'Existing tree mesh'}]
        second = autonomy.cycle(self.root, provs={'roblox_docs': p}, max_items=1)
        self.assertEqual(second['items'][0]['duplicates'], 1)
        q = ResearchQueue(self.root)
        self.assertTrue(q.data['items'][item_key('', 'tree geometry')]['result']['knowledge_available'])
        self.assertEqual(path.read_bytes(), before)

    def test_cost_estimate_uses_actual_topic_http_history(self):
        item = {'key': 'a', 'query': 'tree mesh', 'topic': 'spruce', 'priority': 10}
        history = [{**item, 'key': 'b', 'result': {'http_calls': 6}},
                   {**item, 'key': 'c', 'result': {'http_calls': 2}}]
        ranked = priority.explain(item, history)
        self.assertEqual(ranked['criteria']['cost'], 4)
        self.assertNotIn('cost', ranked['unknown'])

    def test_daily_http_cap_includes_github_fallbacks_and_survives_restart(self):
        self.configure('daily', max_http_calls=2)
        class Response(io.BytesIO):
            headers = {}
            def geturl(self):
                return 'https://api.github.com/search/repositories'
        with patch('agent.providers.urlopen', side_effect=lambda *a, **k: Response(b'{"items": []}')) as remote:
            first = autonomy.cycle(self.root, provs={'github': providers.GitHub(self.root)}, max_items=1)
            second = autonomy.cycle(self.root, provs={'github': providers.GitHub(self.root)}, max_items=1)
        self.assertEqual(remote.call_count, 2)
        self.assertEqual(first['http_calls'], 2)
        self.assertEqual(second['http_calls'], 0)
        self.assertEqual(ResearchQueue(self.root).daily()['http_calls'], 2)
        self.assertEqual(first['stop_reason'], 'budget HTTP atteint')

    def test_fetch_attempt_counter_survives_interrupt(self):
        def interrupted(root, **kwargs):
            budget.fetch_attempt()
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            autonomy.cycle(self.root, research_fn=interrupted, max_items=1)
        self.assertEqual(ResearchQueue(self.root).daily()['fetch'], 1)

    def test_scheduled_refresh_shares_daily_http_quota(self):
        self.configure('daily', max_http_calls=0)
        with patch('agent.providers.urlopen') as remote:
            result = run.refresh(self.root)
        remote.assert_not_called()
        self.assertEqual(result['http_calls'], 0)
        self.assertEqual(result['stop_reason'], 'budget HTTP atteint')

    def test_note_cap_also_covers_evaluator_generated_followups(self):
        self.configure('queue', max_children_per_note=1)
        s = autonomy.cycle(self.root, provs={'roblox_docs': FakeDocs()}, max_items=1)
        self.assertEqual(s['created'], 1)
        self.assertLessEqual(s['followups_added'], 1)
