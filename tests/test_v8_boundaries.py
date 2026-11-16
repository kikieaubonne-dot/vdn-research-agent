"""Safety defects reproduced independently against the V7 checkout."""
import shutil
import unittest
from unittest.mock import patch
from agent import rag, knowledge, mcp_server
from tests.test_autonomy import make_root


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()
        self.addCleanup(shutil.rmtree, self.root)

    def test_non_object_mcp_message_is_invalid_request(self):
        result = mcp_server.handle([])
        self.assertEqual(result['error']['code'], -32600)

    def test_bool_top_k_rejected_not_coerced(self):
        with patch.object(mcp_server, 'ROOT', self.root):
            result = mcp_server.handle({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                    'params': {'name': 'search_knowledge', 'arguments': {'query': 'tree', 'top_k': True}}})
        self.assertTrue(result.get('error') or result.get('result', {}).get('isError'))

    def test_general_index_symlink_cannot_escape(self):
        (self.root / 'knowledge').mkdir()
        private = self.root / 'outside.txt'
        private.write_text('OUTSIDE LIBRARY')
        try:
            (self.root / 'knowledge' / '_index.md').symlink_to(private)
        except (OSError,NotImplementedError):
            self.skipTest('symlinks unavailable for this Windows account/filesystem')
        result = rag.get_topic_index('index', root=self.root)
        self.assertIn('error', result)

    def test_first_passage_does_not_exceed_tiny_token_budget(self):
        p = self.root / 'knowledge' / 'note.md'
        p.parent.mkdir()
        p.write_text(knowledge.dump_frontmatter({'id': 'vdn-test', 'title': 'Mesh ' * 80,
                     'status': 'documente'}) + '\n## Evidence\nSet the MeshPart texture material.\n')
        rag.update_index(self.root)
        result = rag.search_knowledge('Mesh', token_budget=1, root=self.root)
        self.assertLessEqual(result['tokens_estimated'], 1)

    def test_partially_corrupt_library_is_indexed_with_diagnostics(self):
        p = self.root / 'knowledge' / 'note.md'
        p.parent.mkdir()
        p.write_text(knowledge.dump_frontmatter({'id': 'vdn-test', 'source_tier': 'bad'}) + '\n# Mesh')
        result = rag.update_index(self.root)
        self.assertTrue(result['diagnostics'])
