import unittest
from urllib.parse import parse_qs, urlparse
from agent.providers import GitHub

class GitHubRankingTests(unittest.TestCase):

    def test_relevant_repo_first(self):
        def fake_get(url, **kwargs):
            import json
            return json.dumps({
                "items": [
                    {
                        "html_url": "https://github.com/test/blender-importer",
                        "full_name": "test/blender-importer",
                        "description": "Blender import tools",
                        "topics": []
                    },
                    {
                        "html_url": "https://github.com/test/snow-generator",
                        "full_name": "test/snow-generator",
                        "description": "Procedural snow for Blender",
                        "topics": []
                    }
                ]
            })

        results = GitHub(getter=fake_get).search(
            "snow procedural blender", 5
        )

        self.assertEqual(
            results[0]["url"],
            "https://github.com/test/snow-generator"
        )

    def test_specific_keyword_beats_generic_keyword(self):
        import json

        def fake_get(url, **kwargs):
            return json.dumps({
                "items": [
                    {
                        "html_url": "https://github.com/test/blender-tools",
                        "full_name": "test/blender-tools",
                        "description": "Blender tools and plugins",
                        "topics": []
                    },
                    {
                        "html_url": "https://github.com/test/snow-addon",
                        "full_name": "test/snow-addon",
                        "description": "Snow accumulation on 3D objects",
                        "topics": []
                    }
                ]
            })

        results = GitHub(getter=fake_get).search(
            "snow procedural blender", 5
        )

        self.assertEqual(
            results[0]["url"],
            "https://github.com/test/snow-addon"
        )

    def test_no_generic_roblox_fallback(self):
        queries = []

        def fake_get(url, **kwargs):
            import json
            q = parse_qs(urlparse(url).query)["q"][0]
            queries.append(q)
            return json.dumps({"items": []})

        GitHub(getter=fake_get).search(
            "roblox SurfaceAppearance", 5
        )

        self.assertNotIn("roblox", queries)

    def test_empty_description_preserved(self):
        def fake_get(url, **kwargs):
            import json
            return json.dumps({
                "items": [{
                    "html_url": "https://github.com/test/unknown",
                    "full_name": "test/unknown",
                    "description": None,
                    "topics": []
                }]
            })

        results = GitHub(getter=fake_get).search(
            "snow blender", 5
        )

        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
