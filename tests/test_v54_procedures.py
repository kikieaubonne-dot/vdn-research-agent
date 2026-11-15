import unittest

from agent.knowledge import build_body


class V54ProcedureTests(unittest.TestCase):

    def make_body(self, excerpts):
        return build_body(
            title="Terrain test",
            query="snow terrain material",
            topic={"id": "snow", "title": "Snow"},
            assessment={"excerpts": excerpts},
            src={
                "provider": "roblox_docs",
                "url": "https://create.roblox.com/docs/test"
            },
            accessed="2026-11-15",
            status="documente"
        )

    def test_steps_in_main_section(self):
        body = self.make_body([
            "In the Properties window, set Expanded Terrain to Enabled.",
            "Click the plus icon to create a new terrain material."
        ])

        start = body.index("## " + chr(0xC9) + "tapes reproductibles")
        end = body.index("## Param" + chr(0xE8) + "tres", start)
        section = body[start:end]

        self.assertIn("Instructions extraites automatiquement", section)
        self.assertIn("Expanded Terrain", section)
        self.assertNotIn("## Indices de proc", body)

    def test_no_steps_not_a_tutorial(self):
        body = self.make_body(["UV Mapping"])

        self.assertIn(
            "Ne pas pr" + chr(0xE9) + "senter cette fiche comme un tutoriel",
            body
        )


if __name__ == "__main__":
    unittest.main()
