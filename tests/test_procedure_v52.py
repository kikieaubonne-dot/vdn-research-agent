import unittest
from agent.procedure import actionable_excerpts
from agent.knowledge import decide_status

class ProcedureV52Tests(unittest.TestCase):
    def test_cut_off_at_to(self):
        self.assertEqual(actionable_excerpts(['built-in material, or set in the BasePart.MaterialVariant property to']), [])
    def test_cut_off_at_of(self):
        self.assertEqual(actionable_excerpts(['Set the MaterialVariant property of']), [])
    def test_complete_setting(self):
        s = 'Set the SurfaceAppearance AlphaMode property to Transparency for foliage cards.'
        self.assertEqual(actionable_excerpts([s]), [s])
    def test_recommendation_use(self):
        s = 'Try to use materials whenever possible in order to conserve memory budget for textures.'
        self.assertEqual(actionable_excerpts([s]), [s])
    def test_headings_not_actions(self):
        self.assertEqual(actionable_excerpts(['### Property: MaterialVariant.BaseMaterial', 'UV Mapping']), [])
    def test_truncated_does_not_document(self):
        a = {'accepted': True, 'excerpts': ['Set the MaterialVariant property to', 'The ColorMapContent property supports textures.']}
        self.assertEqual(decide_status(a, 1, True)[0], 'candidat')
    def test_complete_instruction_documents_source_not_tutorial(self):
        a = {'accepted': True, 'excerpts': ['Set the SurfaceAppearance AlphaMode property to Transparency.', 'The ColorMap provides a texture.']}
        self.assertEqual(decide_status(a, 1, True)[0], 'documente')
