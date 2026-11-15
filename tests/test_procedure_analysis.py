import unittest

from agent.procedure_analysis import analyze_procedures


class ProcedureAnalysisTests(unittest.TestCase):

    def test_extract_action_and_object(self):
        results = analyze_procedures([
            "Set the SurfaceAppearance AlphaMode property to Transparency."
        ])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["action"].lower(), "set")
        self.assertEqual(results[0]["object"].lower(), "surfaceappearance")
        self.assertEqual(results[0]["status"], "candidate_instruction")
        self.assertFalse(results[0]["tested"])

    def test_reject_outline(self):
        results = analyze_procedures([
            "UV Mapping",
            "Texture Atlases",
            "Optimization"
        ])

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
