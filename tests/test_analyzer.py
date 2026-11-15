import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from agent.analyzer import strip_html, read_evidence, extract_facts, enrich_note, followup_questions

class AnalyzerTests(unittest.TestCase):
    def test_html(self):
        self.assertEqual(strip_html('<p>Alpha <b>foliage</b></p>'),'Alpha foliage')
    def test_allowlist(self):
        with self.assertRaises(ValueError): read_evidence('https://example.com/x')
    def test_extract(self):
        facts=extract_facts({'text':'The SurfaceAppearance transparency changes how foliage renders at a distance.'})
        self.assertEqual(len(facts),1)
    def test_followup(self):
        self.assertTrue(followup_questions('Roblox alpha foliage',''))
    def test_enrich(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.md'
            p.write_text('**Source :** [Roblox DevForum](https://devforum.roblox.com/t/test/123)\n',encoding='utf-8')
            fake={'provider':'DevForum','title':'Alpha foliage','text':'The foliage transparency becomes different at a distance in the Roblox Player.','posts_read':1}
            with patch('agent.analyzer.read_evidence',return_value=fake):
                self.assertEqual(enrich_note(p),'enriched')
            self.assertIn('Analyse V2',p.read_text())
            self.assertEqual(enrich_note(p),'already')

if __name__=='__main__': unittest.main()
