import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from agent.v3 import excerpts, analyze, select_notes

class V3Tests(unittest.TestCase):
    def test_excerpts(self):
        self.assertEqual(len(excerpts('Some nice game screenshots.')),0)
        self.assertEqual(len(excerpts('Set SurfaceAppearance AlphaMode = Transparency when using foliage texture cards.')),1)
    def test_no_empty_enrichment(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'knowledge/spruce/example.md';p.parent.mkdir(parents=True)
            p.write_text('**Source :** [GitHub](https://github.com/a/b)\n',encoding='utf-8')
            with patch('agent.v3.evidence_for',return_value={'provider':'GitHub','text':'Nothing useful','posts_read':1}):
                self.assertEqual(analyze(p,root,{})['status'],'insufficient_source')
            self.assertNotIn('Analyse V3',p.read_text())
    def test_real_extraction(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'knowledge/spruce/example.md';p.parent.mkdir(parents=True)
            p.write_text('**Source :** [GitHub](https://github.com/a/b)\n',encoding='utf-8');state={}
            with patch('agent.v3.evidence_for',return_value={'provider':'GitHub','text':'Set SurfaceAppearance AlphaMode = Transparency when using foliage texture cards.','posts_read':1}):
                self.assertEqual(analyze(p,root,state)['status'],'evidence_extracted')
            self.assertIn('Analyse V3',p.read_text());self.assertTrue(state['questions'])

if __name__=='__main__':unittest.main()
