import unittest
from agent.procedure import actionable_excerpts
from agent.knowledge import decide_status, build_body

class ProcedureQualityTests(unittest.TestCase):
    def test_toc_not_procedure(self):
        self.assertEqual(actionable_excerpts(['Texture Atlases', 'UV Mapping', 'Optimization']), [])
    def test_explicit_instruction(self):
        line='Set the SurfaceAppearance AlphaMode property to Transparency for foliage cards.'
        self.assertEqual(actionable_excerpts([line]), [line])
    def test_no_documented_status_for_outline(self):
        a={'accepted': True, 'excerpts': ['UV mapping and foliage atlas overview', 'PBR materials and transparency details']}
        self.assertEqual(decide_status(a, 1, True)[0], 'candidat')
    def test_documented_with_action_evidence(self):
        a={'accepted': True, 'excerpts': ['Set the SurfaceAppearance AlphaMode property to Transparency.', 'The mesh material supports a color map.']}
        self.assertEqual(decide_status(a, 1, True)[0], 'documente')
    def test_not_claiming_tutorial(self):
        body=build_body('Test','snow branch mesh',{'id':'spruce'}, {'excerpts':['UV Mapping'], 'topical':1, 'technical':0.3}, {'url':'https://create.roblox.com/docs/test','provider':'roblox_docs'}, '2026-11-15','candidat')
        self.assertIn('Ne pas présenter cette fiche comme un tutoriel', body)

if __name__=='__main__': unittest.main()
