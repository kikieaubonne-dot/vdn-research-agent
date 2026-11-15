import unittest
from agent import meta
class DiagnosticsTests(unittest.TestCase):
    def test_empty_session_counted(self):
        s={}; meta.record(s,'github','spruce','baseline',[])
        arm=s['arms']['github:spruce']['baseline']
        self.assertEqual(arm['empty'],1)
        self.assertEqual(arm['returned'],0)
    def test_nonempty_session_counted(self):
        s={}; meta.record(s,'github','spruce','baseline',[0.5,0.7])
        arm=s['arms']['github:spruce']['baseline']
        self.assertEqual(arm['empty'],0)
        self.assertEqual(arm['returned'],2)
        self.assertAlmostEqual(arm['reward'],0.6)
    def test_metrics_distinguish_no_results(self):
        m=meta.trial_metrics([],[])
        self.assertIsNone(m['avg_relevance'])
        self.assertEqual(m['returned'],0)
    def test_metrics_distinguish_rejected(self):
        m=meta.trial_metrics([{'relevance':0.1}],[])
        self.assertEqual(m['rejected'],1)
        self.assertEqual(m['avg_relevance'],0.1)
if __name__=='__main__':unittest.main()
