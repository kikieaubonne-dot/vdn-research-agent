import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent.core import clean, score, valid_url, run

class CoreTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean('<b>Hello</b> &amp; world'), 'Hello & world')
    def test_url(self):
        self.assertTrue(valid_url('https://devforum.roblox.com/t/abc/123'))
        self.assertFalse(valid_url('javascript:alert(1)'))
    def test_score(self):
        self.assertGreater(score({'title':'Roblox foliage cards', 'excerpt':'baking'}, 'Roblox foliage cards', {'priority':8}), 20)
    def test_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'config').mkdir()
            (root/'config/topics.json').write_text('{"topics":[{"id":"tree","title":"Tree","priority":5,"queries":["Roblox tree"]}]}')
            example = [{'title':'Roblox tree foliage guide','url':'https://github.com/example/foliage','excerpt':'Roblox tree cards','source':'GitHub'}]
            with patch('agent.core.search_github', return_value=example), patch('agent.core.search_devforum', return_value=[]):
                first = run(root, max_queries=1, per_source=1, pause=0)
                second = run(root, max_queries=1, per_source=1, pause=0)
            self.assertEqual(first['discovered'], 1)
            self.assertEqual(second['discovered'], 0)

if __name__ == '__main__':
    unittest.main()
