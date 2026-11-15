"""Regression cases reproduced on V6; all providers are local fakes."""
import json
import shutil
import time
import unittest
from unittest.mock import patch

from agent import autonomy, knowledge, run
from agent.research_queue import ResearchQueue, item_key
from tests.test_autonomy import make_root


class SafetyV7Tests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()
        self.addCleanup(shutil.rmtree, self.root)

    def test_remaining_daily_fetch_is_passed_to_research(self):
        q = ResearchQueue(self.root)
        q.daily()['fetch'] = q.cfg['daily']['max_fetch'] - 1
        q.save()
        seen = []
        def research(root, **kw):
            seen.append(kw['max_fetch'])
            return {'fetched': kw['max_fetch']}
        s = autonomy.cycle(self.root, max_items=1, research_fn=research)
        self.assertEqual(seen, [1])
        self.assertLessEqual(s['queue']['daily']['fetch'], q.cfg['daily']['max_fetch'])

    def test_failed_fetches_consume_fetch_budget(self):
        class Broken:
            name, tier = 'github', 3
            calls = 0
            def search(self, query, limit):
                return [{'url': f'https://github.com/a/repo{i}'} for i in range(4)]
            def fetch(self, url):
                self.calls += 1
                raise ConnectionError('offline')
        p = Broken()
        topic = {'id': 'spruce', 'title': 'Tree'}
        run.research(self.root, provs={'github': p}, planned=[(topic, 'tree mesh', 'test')],
                     max_fetch=1, pause=0, finalize=False)
        self.assertEqual(p.calls, 1)

    def test_attempt_charged_before_interrupted_research(self):
        def interrupted(root, **kw):
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            autonomy.cycle(self.root, max_items=1, research_fn=interrupted)
        q = ResearchQueue(self.root)
        self.assertEqual(q.daily()['items'], 1)

    def test_registry_reconstructed_after_note_committed_before_registry(self):
        path = self.root / 'knowledge' / 'manual.md'
        path.parent.mkdir(exist_ok=True)
        path.write_text(knowledge.dump_frontmatter({'id': 'vdn-manual',
                        'sources': ['https://github.com/a/tree']}) + '\n# User knowledge\n', encoding='utf-8')
        reg = knowledge.Registry(self.root)
        self.assertIsNotNone(reg.find('https://github.com/a/tree'))

    def test_partial_new_lock_is_busy(self):
        path = self.root / 'output' / 'vdn.lock'
        path.parent.mkdir(exist_ok=True)
        path.write_text('{', encoding='utf-8')
        with self.assertRaises(autonomy.Busy):
            with autonomy.Lock(self.root, 7200):
                pass
        self.assertEqual(path.read_text(), '{')

    def test_queue_status_is_read_only_during_active_cycle(self):
        q = ResearchQueue(self.root)
        q.add('lighting', 'SpotLight Angle', 8)
        it = q.data['items'][item_key('lighting', 'SpotLight Angle')]
        q.mark_running(it)
        before = q.history_path.read_bytes()
        status = autonomy.queue_status(self.root)
        self.assertEqual(status['counts']['running'], 1)
        self.assertEqual(before, q.history_path.read_bytes())

    def test_corrupt_archives_are_not_overwritten(self):
        path = self.root / 'output' / 'queue.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text('{first', encoding='utf-8')
        ResearchQueue(self.root)
        path.write_text('{second', encoding='utf-8')
        ResearchQueue(self.root)
        archived = [p.read_text() for p in path.parent.glob('queue.corrupt*.json')]
        self.assertCountEqual(archived, ['{first', '{second'])
