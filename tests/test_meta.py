import unittest
from agent import meta
class MetaTests(unittest.TestCase):
    def test_irrelevant_spruce(self):
        item={'title':'super-smart-idea-im-about-to-have','excerpt':'funny project'}
        self.assertLess(meta.relevance(item,'Roblox spruce foliage alpha transparency','spruce'),0.4)
    def test_relevant_spruce(self):
        item={'title':'Roblox foliage transparency alpha issue','excerpt':'spruce foliage SurfaceAppearance rendering alpha'}
        self.assertGreaterEqual(meta.relevance(item,'Roblox spruce foliage alpha transparency','spruce'),0.4)
    def test_explore_before_exploit(self):
        s={}; choices=[]
        for _ in range(3):
            c=meta.choose(s,'devforum','spruce');choices.append(c);meta.record(s,'devforum','spruce',c,[0.7])
        self.assertEqual(set(choices),set(meta.STRATEGIES))
    def test_empty_does_not_reward(self):
        s={};meta.record(s,'github','forest','baseline',[])
        self.assertEqual(s['arms']['github:forest']['baseline']['reward'],0)
if __name__=='__main__':unittest.main()
