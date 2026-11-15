import unittest
from agent.recursive_gaps import propose

class GapTests(unittest.TestCase):
    def test_insufficient_technical_generates_specific_followup(self):
        r = propose('tree foliage cards', [{'topical': .8, 'technical': .04, 'roblox': True, 'noise': []}])
        self.assertEqual(len(r), 1)
        self.assertIn('tutorial', r[0]['query'])
    def test_irrelevant_or_noise_does_not_spawn(self):
        self.assertEqual(propose('tree foliage cards', [{'topical': .1, 'technical': 0, 'noise': []}]), [])
        self.assertEqual(propose('tree foliage cards', [{'topical': .8, 'technical': 0, 'noise': ['portfolio']}]), [])
    def test_depth_bounded_elsewhere_and_max_children(self):
        r = propose('flashlight shadows forest', [{'topical': .8, 'technical': 0, 'roblox': False, 'noise': []}], 1)
        self.assertEqual(len(r), 1)

class CycleIntegrationTests(unittest.TestCase):
    def test_rejected_results_enqueue_followups(self):
        import shutil
        from tests.test_autonomy import make_root
        from agent import autonomy
        from agent.research_queue import ResearchQueue
        root = make_root()
        try:
            def rejected_research(root, **kwargs):
                return {"fetched": 1, "created": 0, "rejected": 1, "duplicates": 0,
                        "created_notes": [], "errors": [],
                        "rejected_candidates": [{"topical": .8, "technical": .04, "roblox": True, "noise": []}]}
            result = autonomy.cycle(root, max_items=1, research_fn=rejected_research)
            self.assertEqual(result["created"], 0)
            self.assertGreater(result["followups_added"], 0)
            q = ResearchQueue(root)
            self.assertTrue(any(i["origin"] == "relance_lacune" for i in q.data["items"].values()))
        finally:
            shutil.rmtree(root, ignore_errors=True)
