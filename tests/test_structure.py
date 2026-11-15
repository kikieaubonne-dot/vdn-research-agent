"""V5.5 etape 1 : tests hors ligne du decoupage structurel (agent/structure.py)."""
import json
import unittest
from pathlib import Path

from agent import structure as st

FIXTURES = Path(__file__).parent / "fixtures"
URL = "https://create.roblox.com/docs/effects/light-sources"


def load_light_sources():
    text = (FIXTURES / "structure_light_sources.md").read_text(encoding="utf-8")
    return st.parse_markdown(text, url=URL, provider="roblox_docs")


def of_type(doc, btype):
    return [b for b in doc["blocks"] if b["type"] == btype]


class InlineCleaningTests(unittest.TestCase):
    def test_roblox_ref_with_label(self):
        self.assertEqual(st.clean_inline("adjust the `Class.SpotLight.Angle|Angle` value"), "adjust the Angle value")

    def test_roblox_ref_without_label_keeps_last_name(self):
        self.assertEqual(st.clean_inline("Insert a `Class.SpotLight`."), "Insert a SpotLight.")

    def test_api_refs_keep_full_name(self):
        refs = st.extract_api_refs("Set `Class.SpotLight.Range|Range` and `Enum.Material.Snow`.")
        self.assertEqual([r["name"] for r in refs], ["Class.SpotLight.Range", "Enum.Material.Snow"])
        self.assertEqual([r["label"] for r in refs], ["Range", "Snow"])
        self.assertEqual(refs[0]["kind"], "Class")

    def test_api_ref_without_backticks(self):
        refs = st.extract_api_refs("Class.SpotLight.Angle|Angle controls the cone.")
        self.assertEqual(refs[0]["name"], "Class.SpotLight.Angle")
        self.assertEqual(st.clean_inline("Class.SpotLight.Angle|Angle controls the cone."), "Angle controls the cone.")

    def test_links_and_emphasis(self):
        raw = "See [shared properties](#shared-properties) in the **Explorer**."
        self.assertEqual(st.clean_inline(raw), "See shared properties in the Explorer.")
        self.assertEqual(st.extract_links(raw), [{"text": "shared properties", "url": "#shared-properties"}])

    def test_slug(self):
        self.assertEqual(st.slug("Shared properties"), "shared-properties")
        self.assertEqual(st.slug("\u00c9clairage de nuit"), "eclairage-de-nuit")


class HeadingTests(unittest.TestCase):
    def test_nested_heading_paths(self):
        doc = load_light_sources()
        heads = of_type(doc, "heading")
        self.assertEqual([(h["level"], h["text"]) for h in heads],
                         [(1, "Light sources"), (2, "Shared properties"), (2, "Spotlights"), (3, "Flashlight setup")])
        flash_list = [b for b in of_type(doc, "list") if b["section"][-1] == "Flashlight setup"][0]
        self.assertEqual(flash_list["section"], ["Light sources", "Spotlights", "Flashlight setup"])

    def test_sibling_heading_resets_path(self):
        doc = st.parse_markdown("# A\n## B\ntext b\n## C\ntext c\n# D\ntext d")
        paras = of_type(doc, "paragraph")
        self.assertEqual([p["section"] for p in paras], [["A", "B"], ["A", "C"], ["D"]])

    def test_setext_headings(self):
        doc = st.parse_markdown("Title\n=====\n\nSub\n---\n\nbody")
        self.assertEqual([(h["level"], h["text"]) for h in of_type(doc, "heading")], [(1, "Title"), (2, "Sub")])

    def test_front_matter_title_not_a_block(self):
        doc = load_light_sources()
        self.assertEqual(doc["source"]["title"], "Light sources")
        self.assertEqual(doc["meta"]["title"], "Light sources")
        self.assertFalse(any("description:" in b["raw"] for b in doc["blocks"]))


class ListTests(unittest.TestCase):
    def test_numbered_list_order_and_numbers(self):
        doc = load_light_sources()
        steps = [b for b in of_type(doc, "list") if b["ordered"]][0]
        self.assertEqual(steps["start"], 1)
        self.assertEqual([it["number"] for it in steps["items"]], [1, 2, 3])
        self.assertEqual([it["position"] for it in steps["items"]], [1, 2, 3])
        self.assertTrue(steps["items"][2]["text"].startswith("Then adjust the Angle and Range"))
        self.assertEqual([r["name"] for r in steps["items"][2]["api_refs"]],
                         ["Class.SpotLight.Angle", "Class.SpotLight.Range"])

    def test_list_resumed_after_code_is_linked_not_renumbered(self):
        doc = load_light_sources()
        lists = [b for b in of_type(doc, "list") if b["ordered"]]
        self.assertEqual(len(lists), 2)
        self.assertEqual(lists[1]["start"], 4)
        self.assertEqual(lists[1]["continues"], lists[0]["id"])
        seq = st.sequence(doc, lists[0]["id"])
        self.assertEqual([it["number"] for it in seq], [1, 2, 3, 4])

    def test_no_continuation_across_headings(self):
        doc = st.parse_markdown("## A\n1. one\n2. two\n## B\n3. three")
        lists = of_type(doc, "list")
        self.assertNotIn("continues", lists[1])

    def test_lazy_one_numbering_kept_as_written(self):
        doc = st.parse_markdown("1. first\n1. second\n1. third")
        items = of_type(doc, "list")[0]["items"]
        self.assertEqual([it["number"] for it in items], [1, 1, 1])
        self.assertEqual([it["position"] for it in items], [1, 2, 3])

    def test_nested_bullets_depth_and_parent(self):
        doc = load_light_sources()
        bullets = [b for b in of_type(doc, "list") if not b["ordered"]][0]
        self.assertEqual([(it["depth"], it["parent"]) for it in bullets["items"]], [(0, None), (1, 1), (0, None)])
        self.assertEqual(bullets["items"][1]["text"], "Keep Shadows enabled.")

    def test_item_continuation_line(self):
        doc = st.parse_markdown("1. Select the part\n   in the Explorer.\n2. Set Anchored.")
        items = of_type(doc, "list")[0]["items"]
        self.assertEqual(items[0]["text"], "Select the part in the Explorer.")
        self.assertEqual(len(items), 2)

    def test_loose_list_with_blank_lines(self):
        doc = st.parse_markdown("1. one\n\n2. two\n\n3. three\n\nAfter.")
        self.assertEqual(len(of_type(doc, "list")), 1)
        self.assertEqual(len(of_type(doc, "list")[0]["items"]), 3)
        self.assertEqual(of_type(doc, "paragraph")[0]["text"], "After.")

    def test_item_reference_points_to_section(self):
        doc = load_light_sources()
        item = [b for b in of_type(doc, "list") if b["ordered"]][0]["items"][1]
        self.assertEqual(item["ref"]["url"], URL + "#spotlights")
        self.assertEqual(item["ref"]["section"], "Light sources > Spotlights")
        self.assertEqual(item["ref"]["item"], 2)

    def test_no_completeness_verdict(self):
        # L'etape 1 ne juge pas : aucune notion de procedure complete, quel que soit le nombre d'etapes.
        doc = st.parse_markdown("\n".join(f"{k}. Set Property{k}." for k in range(1, 9)))
        text = json.dumps(doc)
        for word in ("complete", "procedure", "tutorial", "valid"):
            self.assertNotIn(word, text.lower())


class CodeBlockTests(unittest.TestCase):
    def test_code_preserved_verbatim(self):
        doc = load_light_sources()
        code = of_type(doc, "code")[0]
        self.assertEqual(code["language"], "lua")
        self.assertIn("light.Angle = 45 -- `Class.SpotLight.Angle|Angle` reste intact dans le code", code["raw"])
        self.assertEqual(code["text"], code["raw"])
        self.assertEqual(code["api_refs"], [])
        self.assertTrue(code["closed"])

    def test_code_attached_to_preceding_list_item(self):
        doc = load_light_sources()
        lists = [b for b in of_type(doc, "list") if b["ordered"]]
        code = of_type(doc, "code")[0]
        self.assertEqual(code["after_list"], lists[0]["id"])
        self.assertEqual(code["after_item"], 3)

    def test_heading_like_line_inside_code_is_not_heading(self):
        doc = st.parse_markdown("# Real\n```\n# not a heading\n1. not a list\n```")
        self.assertEqual(len(of_type(doc, "heading")), 1)
        self.assertEqual(of_type(doc, "list"), [])
        self.assertEqual(of_type(doc, "code")[0]["raw"], "# not a heading\n1. not a list")

    def test_unclosed_fence_flagged(self):
        doc = st.parse_markdown("```lua\nprint(1)")
        self.assertFalse(of_type(doc, "code")[0]["closed"])

    def test_indented_fence_inside_list(self):
        doc = st.parse_markdown("1. Add a script:\n   ```lua\n   print('hi')\n   ```\n2. Run.")
        code = of_type(doc, "code")[0]
        self.assertEqual(code["raw"], "print('hi')")
        self.assertEqual(code["after_item"], 1)
        lists = of_type(doc, "list")
        self.assertEqual(lists[1]["continues"], lists[0]["id"])


class OtherBlockTests(unittest.TestCase):
    def test_table_cells_do_not_split_on_roblox_pipe(self):
        doc = load_light_sources()
        table = of_type(doc, "table")[0]
        self.assertEqual(table["header"], ["Property", "Description"])
        self.assertEqual(table["rows"][0], ["Brightness", "Intensity of the light."])
        self.assertEqual(table["api_refs"][0]["name"], "Class.Light.Brightness")

    def test_callout_quote(self):
        doc = load_light_sources()
        quote = of_type(doc, "quote")[0]
        self.assertEqual(quote["callout"], "info")
        self.assertEqual(quote["text"], "The LightingStyle property sets your game's lighting style.")

    def test_image_alt_kept(self):
        img = of_type(load_light_sources(), "image")[0]
        self.assertEqual(img["text"], "A street lamp spotlight with a 30 degree angle.")
        self.assertEqual(img["src"], "../assets/SpotLight-Angle-30.jpg")

    def test_paragraph_kept_whole_not_split_in_sentences(self):
        doc = st.parse_markdown("First sentence. Second sentence.\nSame paragraph.")
        self.assertEqual(len(of_type(doc, "paragraph")), 1)

    def test_html_tag_lines_skipped(self):
        doc = st.parse_markdown("<Alert severity='info'>\nText inside.\n</Alert>")
        self.assertEqual([b["type"] for b in doc["blocks"]], ["paragraph"])


class SchemaTests(unittest.TestCase):
    def test_schema_and_stable_keys(self):
        doc = load_light_sources()
        self.assertEqual(doc["schema"], "vdn.structure/1")
        self.assertEqual(set(doc), {"schema", "source", "meta", "blocks", "stats"})
        required = {"id", "index", "type", "section", "anchor", "line_start", "line_end",
                    "raw", "text", "api_refs", "links", "ref"}
        for blk in doc["blocks"]:
            self.assertTrue(required <= set(blk), blk["id"])
            self.assertIn(blk["type"], st.BLOCK_TYPES)
        self.assertEqual([b["index"] for b in doc["blocks"]], list(range(len(doc["blocks"]))))

    def test_order_follows_source_lines(self):
        doc = load_light_sources()
        starts = [b["line_start"] for b in doc["blocks"]]
        self.assertEqual(starts, sorted(starts))

    def test_json_round_trip(self):
        doc = load_light_sources()
        self.assertEqual(st.from_json(st.to_json(doc)), doc)

    def test_wrong_schema_rejected(self):
        with self.assertRaises(ValueError):
            st.from_json('{"schema": "autre/9"}')

    def test_nothing_invented(self):
        # Chaque mot du texte nettoye provient du texte brut du bloc.
        doc = load_light_sources()
        for blk in doc["blocks"]:
            if blk["type"] in ("code", "table"):
                continue
            for word in blk["text"].replace(".", " ").split():
                self.assertIn(word.strip(",:;()'\""), blk["raw"], blk["id"])

    def test_crlf_and_accents(self):
        doc = st.parse_markdown("# \u00c9clairage\r\n\r\n1. R\u00e9gler la port\u00e9e.\r\n2. Tester.\r\n")
        self.assertEqual(of_type(doc, "heading")[0]["text"], "\u00c9clairage")
        self.assertEqual([it["text"] for it in of_type(doc, "list")[0]["items"]],
                         ["R\u00e9gler la port\u00e9e.", "Tester."])

    def test_parse_text_for_forum(self):
        doc = st.parse("To fix it:\n1. Open Lighting\n2. Set Technology to Future", provider="devforum")
        self.assertEqual(doc["source"]["format"], "text")
        self.assertEqual(len(of_type(doc, "list")[0]["items"]), 2)

    def test_section_blocks(self):
        doc = load_light_sources()
        self.assertTrue(all("Spotlights" in b["section"] for b in st.section_blocks(doc, "Light sources", "Spotlights")))
        self.assertEqual(st.section_blocks(doc, "Nope"), [])

    def test_empty_input(self):
        doc = st.parse_markdown("")
        self.assertEqual(doc["blocks"], [])
        self.assertEqual(doc["stats"]["blocks"], 0)


if __name__ == "__main__":
    unittest.main()
