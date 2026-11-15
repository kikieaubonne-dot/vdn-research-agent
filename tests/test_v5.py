"""Tests V5 : fournisseurs (réponses factices au format réel), filtre, fiches, migration, RAG, MCP, Ollama, méta, bout en bout.
Aucun accès réseau : tout passe par un « getter » factice qui sert les fichiers de tests/fixtures."""
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent import knowledge, llm, mcp_server, meta, planner, providers, rag, relevance, run as runner
from agent.text import tokens, expand, BM25, approx_tokens

FIX = Path(__file__).parent / "fixtures"
REPO = Path(__file__).resolve().parents[1]


def fake_getter(url, accept="*/*", max_bytes=0, retries=0, extra_headers=None, allow_extra_hosts=()):
    from urllib.parse import urlparse
    p = urlparse(url)
    if p.hostname == "devforum.roblox.com" and not providers.DEVFORUM_ALLOWED.match(p.path):
        raise providers.FetchError("chemin DevForum non autorisé")
    table = {
        "https://create.roblox.com/docs/llms.txt": "llms.txt",
        "https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md": "surface-appearance.md",
        "https://create.roblox.com/docs/en-us/reference/engine/classes/SurfaceAppearance.md": "class-surfaceappearance.md",
        "https://devforum.roblox.com/sitemap.xml": "devforum_sitemap.xml",
        "https://devforum.roblox.com/sitemap_1.xml": "devforum_sitemap_1.xml",
        "https://devforum.roblox.com/sitemap_recent.xml": "devforum_sitemap_recent.xml",
        "https://devforum.roblox.com/t/4525371.json": "devforum_topic.json",
        "https://api.github.com/repos/someone/roblox-foliage-tools": "github_repo_foliage.json",
        "https://api.github.com/repos/someone/roblox-foliage-tools/readme": "github_readme_foliage.md",
        "https://api.github.com/repos/other/pet-simulator": "github_repo_pet.json",
        "https://api.github.com/repos/other/pet-simulator/readme": "github_readme_pet.md",
    }
    if url.startswith("https://api.github.com/search/repositories"):
        return (FIX / "github_search.json").read_text(encoding="utf-8")
    if url in table:
        return (FIX / table[url]).read_text(encoding="utf-8")
    raise providers.FetchError(f"HTTP 404 sur {p.hostname}")


def make_root():
    d = Path(tempfile.mkdtemp())
    (d / "config").mkdir()
    shutil.copy(REPO / "config" / "vocabulary.json", d / "config" / "vocabulary.json")
    (d / "config" / "topics.json").write_text(json.dumps({"topics": [
        {"id": "spruce", "domain": "vegetation", "title": "Épicéa", "priority": 10, "queries": ["foliage SurfaceAppearance transparency"],
         "subtopics": ["foliage cards"]}]}), encoding="utf-8")
    (d / "knowledge").mkdir()
    (d / "output").mkdir()
    return d


class TextTests(unittest.TestCase):
    def test_tokens_fold_and_stem(self):
        self.assertEqual(tokens("Les Arbres enneigés"), ["arbre", "enneige"])

    def test_french_synonyms(self):
        self.assertIn("foliage", expand("feuillage"))

    def test_bm25_orders(self):
        b = BM25([tokens("snow terrain"), tokens("foliage cards alpha"), tokens("foliage")])
        self.assertEqual(b.top(tokens("foliage alpha"), 1)[0][0], 1)


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()

    def test_canonical_url(self):
        self.assertEqual(providers.canonical_url("https://devforum.roblox.com/t/some-slug/4525371/7?u=x"),
                         "https://devforum.roblox.com/t/4525371")
        self.assertEqual(providers.canonical_url("https://GitHub.com/Owner/Repo.git/"), "https://github.com/owner/repo")
        self.assertEqual(providers.canonical_url("https://create.roblox.com/docs/en-us/art/x.md"),
                         providers.canonical_url("https://create.roblox.com/docs/art/x"))

    def test_devforum_search_is_refused(self):
        with self.assertRaises(providers.FetchError):
            providers.http_get("https://devforum.roblox.com/search.json?q=foliage")

    def test_unknown_host_refused(self):
        with self.assertRaises(providers.FetchError):
            providers.http_get("https://example.com/")

    def test_docs_index_and_search(self):
        docs = providers.RobloxDocs(self.root, fake_getter)
        self.assertRaises(providers.FetchError, docs.refresh)  # < 50 entrées : index suspect, refusé
        entries = providers.parse_llms_index((FIX / "llms.txt").read_text(encoding="utf-8"))
        self.assertEqual(len(entries), 6)
        docs.path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
        res = docs.search("surface appearance alpha", 3)
        self.assertTrue(res and "surface-appearance" in res[0]["url"])
        page = docs.fetch(res[0]["url"])
        self.assertTrue(page["official"])
        self.assertIn("AlphaMode", page["text"])

    def test_devforum_sitemap_and_topic(self):
        df = providers.DevForum(self.root, fake_getter, pause=0)
        r = df.refresh(max_pages=5)
        self.assertEqual(r["topics_indexed"], 2)  # le sujet « pet simulator » n'est pas gardé
        res = df.search("foliage transparent distance", 3)
        self.assertEqual(res[0]["url"].rsplit("/", 1)[-1], "4525371")
        doc = df.fetch(res[0]["url"])
        self.assertTrue(doc["official"])
        self.assertTrue(doc["meta"]["accepted_answer"])
        self.assertIn("[PERSONNEL ROBLOX]", doc["text"])

    def test_github_short_query(self):
        seen = {}

        def g(url, **kw):
            seen["url"] = url
            return fake_getter(url, **kw)
        gh = providers.GitHub(self.root, g)
        gh.search("Roblox realistic spruce foliage alpha cards normals implementation limitations troubleshooting", 3)
        q = seen["url"].split("q=")[1].split("&")[0]
        self.assertLessEqual(len(q.split("%20")), 5)


class RelevanceTests(unittest.TestCase):
    def test_accepts_technical_roblox_source(self):
        text = (FIX / "surface-appearance.md").read_text(encoding="utf-8")
        a = relevance.assess("foliage SurfaceAppearance transparency", "Surface appearance", text, "roblox_docs")
        self.assertTrue(a["accepted"], a["reasons"])
        self.assertGreaterEqual(len(a["excerpts"]), 2)

    def test_rejects_noise_with_reason(self):
        a = relevance.assess("foliage transparency", "My Portfolio (Commissions Open)", "Hello I build foliage transparency stuff for Roblox", "devforum")
        self.assertFalse(a["accepted"])
        self.assertTrue(any("portfolio" in r for r in a["reasons"]))

    def test_rejects_off_topic(self):
        a = relevance.assess("foliage transparency", "pet simulator", "A fun pet simulator with eggs and rebirths for Roblox.", "github")
        self.assertFalse(a["accepted"])

    def test_query_text_cannot_make_itself_relevant(self):
        # régression du bug de migration : la requête recopiée dans la fiche ne doit pas compter
        body = ("# zqh7y/RollPetsRNG\n\n**Question de recherche :** Roblox snowy forest terrain optimization\n\n"
                "## Extrait de découverte (non vérifié)\n\nA pets RNG game.\n")
        ev = knowledge.legacy_evidence(body)
        self.assertNotIn("snowy", ev)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()
        self.topic = {"id": "spruce", "domain": "vegetation", "title": "Épicéa"}
        self.text = (FIX / "surface-appearance.md").read_text(encoding="utf-8")

    def _write(self, url="https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md", query="foliage SurfaceAppearance transparency"):
        reg = knowledge.Registry(self.root)
        a = relevance.assess(query, "Surface appearance", self.text, "roblox_docs")
        r = knowledge.write_note(self.root, reg, self.topic, query, {"url": url, "provider": "roblox_docs", "tier": 1},
                                 {"title": "Surface appearance", "text": self.text, "official": True}, a)
        reg.save()
        return r

    def test_note_schema_and_never_validated(self):
        r = self._write()
        self.assertEqual(r["action"], "created")
        meta, body = knowledge.parse_note((self.root / r["path"]).read_text(encoding="utf-8"))
        for k in ("id", "title", "domain", "subdomain", "status", "tested_in_studio", "confidence", "confidence_reason",
                  "sources", "accessed", "engine_version"):
            self.assertIn(k, meta)
        self.assertEqual(meta["tested_in_studio"], "non")
        self.assertIn(meta["status"], ("candidat", "documente"))
        for s in knowledge.SECTIONS:
            self.assertIn("## " + s, body)
        self.assertIn("1024", body)  # paramètre chiffré repris d'un extrait sourcé

    def test_dedup_by_canonical_url(self):
        first = self._write()
        second = self._write(url="https://create.roblox.com/docs/art/modeling/surface-appearance", query="foliage cards alpha")
        self.assertEqual(second["action"], "updated")
        self.assertEqual(second["id"], first["id"])
        self.assertEqual(len(list((self.root / "knowledge").rglob("*.md"))), 1)

    def test_frontmatter_roundtrip(self):
        meta = {"id": "vdn-1", "title": 'Titre "guillemets" : deux-points', "sources": ["https://a", "https://b"], "official": True, "tier": 2}
        m2, body = knowledge.parse_note(knowledge.dump_frontmatter(meta) + "\nCorps")
        self.assertEqual(m2, meta)
        self.assertEqual(body.strip(), "Corps")

    def test_migration_keeps_every_file(self):
        src = REPO / "knowledge"
        dst = self.root / "knowledge"
        shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("_index.md"))
        before = sorted(p.name for p in dst.rglob("*.md"))
        # remet les fiches dans leur état V4 si elles ont déjà été migrées (le dépôt peut l'être)
        for p in dst.rglob("*.md"):
            meta, body = knowledge.parse_note(p.read_text(encoding="utf-8"))
            if meta.get("id"):
                legacy = body.split("\n\n", 2)[-1] if body.startswith(">") else body
                p.write_text("---\nstatus: a_verifier\ntopic: \"" + p.parent.name + "\"\n---\n\n" + legacy, encoding="utf-8")
        shutil.copy(REPO / "config" / "topics.json", self.root / "config" / "topics.json")
        rep = knowledge.migrate_legacy(self.root)
        after = sorted(p.name for p in dst.rglob("*.md"))
        self.assertEqual(before, after)
        self.assertEqual(rep["migrated"], len(before))
        again = knowledge.migrate_legacy(self.root)
        self.assertEqual(again["migrated"], 0)  # idempotent

    def test_migration_loses_no_field_and_no_line(self):
        d = self.root / "knowledge" / "spruce"
        d.mkdir(parents=True, exist_ok=True)
        old_meta = ('---\nstatus: a_verifier\nsource_type: "GitHub repositories"\ntopic: "spruce"\n'
                    'score_heuristique: 35\ncollected_utc: "2026-11-15T12:15:20+00:00"\n---\n')
        old_body = ("\n# Foliage cards\n\n**Source :** [x](https://github.com/a/b)\n\n"
                    "**Question de recherche :** spruce foliage\n\nLigne historique unique 42.\n")
        p = d / "legacy-test.md"
        p.write_text(old_meta + old_body, encoding="utf-8")
        shutil.copy(REPO / "config" / "topics.json", self.root / "config" / "topics.json")
        knowledge.migrate_legacy(self.root)
        meta, body = knowledge.parse_note(p.read_text(encoding="utf-8"))
        self.assertEqual(meta["legacy_source_type"], "GitHub repositories")
        self.assertEqual(meta["legacy_collected_utc"], "2026-11-15T12:15:20+00:00")
        self.assertEqual(str(meta["legacy_score_heuristique"]), "35")
        self.assertEqual(meta["legacy_status"], "a_verifier")
        self.assertEqual(meta["legacy_topic"], "spruce")
        for line in old_body.strip().splitlines():
            self.assertIn(line, body)


class RagTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()
        k = KnowledgeTests()
        k.root, k.topic, k.text = self.root, {"id": "spruce", "domain": "vegetation", "title": "Épicéa"}, (FIX / "surface-appearance.md").read_text(encoding="utf-8")
        k._write()
        knowledge.build_indexes(self.root)

    def test_search_budget_and_french(self):
        rag.update_index(self.root)
        res = rag.search_knowledge("transparence du feuillage", top_k=3, token_budget=300, root=self.root)
        self.assertTrue(res["results"])
        self.assertLessEqual(res["tokens_estimated"], 300)

    def test_incremental_update(self):
        first = rag.update_index(self.root)
        second = rag.update_index(self.root)
        self.assertEqual(first["added"], 1)
        self.assertEqual(second["added"] + second["changed"], 0)

    def test_read_and_index(self):
        rag.update_index(self.root)
        nid = rag.search_knowledge("AlphaMode", root=self.root)["results"][0]["note_id"]
        self.assertIn("body", rag.read_knowledge(nid, 200, root=self.root))
        self.assertIn("index", rag.get_topic_index("vegetation", root=self.root))
        self.assertIn("error", rag.get_topic_index("../../etc", root=self.root))


class McpTests(unittest.TestCase):
    def test_protocol(self):
        init = mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
        self.assertEqual(init["result"]["protocolVersion"], "2025-06-18")
        self.assertIsNone(mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        tools = mcp_server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"search_knowledge", "read_knowledge", "get_topic_index"})
        bad = mcp_server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "delete_everything", "arguments": {}}})
        self.assertIn("error", bad)

    def test_tool_call_readonly(self):
        root = make_root()
        with patch.object(mcp_server, "ROOT", root):
            out = mcp_server.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                                     "params": {"name": "search_knowledge", "arguments": {"query": "foliage"}}})
        self.assertEqual(out["result"]["content"][0]["type"], "text")


class LlmGroundingTests(unittest.TestCase):
    def test_drops_unsupported_numbers_and_bad_refs(self):
        ex = ["Set AlphaMode to Transparency; max texture 1024 px.", "Keep trees under 4000 triangles."]
        answer = {"parametres": [{"nom": "taille", "valeur": "1024 px", "e": 1}, {"nom": "taille", "valeur": "2048 px", "e": 1},
                                 {"nom": "x", "valeur": "y", "e": 9}],
                  "limites": [{"texte": "moins de 4000 triangles", "e": 2}], "questions": ["Et sur mobile ?"]}
        kept, total, dropped = llm.ground(answer, ex)
        self.assertEqual(total, 4)
        self.assertEqual(dropped, 2)
        self.assertEqual(kept["parametres"][0]["valeur"], "1024 px")

    def test_enrich_writes_section_only_from_grounded(self):
        root = make_root()
        k = KnowledgeTests()
        k.root, k.topic, k.text = root, {"id": "spruce", "domain": "vegetation", "title": "Épicéa"}, (FIX / "surface-appearance.md").read_text(encoding="utf-8")
        r = k._write()
        fake = json.dumps({"parametres": [{"nom": "résolution max", "valeur": "1024x1024", "e": 2}],
                           "limites": [{"texte": "tri incorrect si beaucoup de surfaces transparentes", "e": 3}],
                           "description": [{"texte": "invention 9999 studs", "e": 1}]})
        out = llm.enrich_note(root / r["path"], generate=lambda p: fake)
        self.assertEqual(out["status"], "enriched")
        body = (root / r["path"]).read_text(encoding="utf-8")
        self.assertIn("non vérifiée", body)
        self.assertNotIn("9999", body)

    def test_unavailable_means_no_analysis(self):
        with patch("agent.llm.available", return_value=False):
            out = runner.enrich(make_root(), 3)
        self.assertIn("aucune analyse", out["status"])


class PlannerMetaTests(unittest.TestCase):
    def test_variants_are_short(self):
        for v in planner.variants("Roblox realistic spruce foliage alpha cards normals").values():
            self.assertTrue(2 <= len(v.split()) <= 4, v)

    def test_followups_capped(self):
        root = make_root()
        f = [{"query": f"foliage question {i}", "topic": "spruce"} for i in range(10)]
        chosen = planner.plan({}, root, 8, f)
        self.assertLessEqual(sum(1 for _, _, o in chosen if o == "suivi"), 2)

    def test_regression_fallback(self):
        s, j = {}, []
        for strat in meta.STRATEGIES:
            meta.record_trial(s, "github", "spruce", strat, {"returned": 4, "new": 4, "technical_mean": 1.0})
        arm = s["arms"]["github:spruce"]["synonyms"]
        arm.update({"n": 10, "reward": 8.0, "best_mean": 0.8, "recent": [0, 0, 0, 0, 0]})
        s["arms"]["github:spruce"]["terms"].update({"n": 10, "reward": 1.0})
        s["arms"]["github:spruce"]["facet"].update({"n": 10, "reward": 1.0})
        self.assertNotEqual(meta.choose(s, "github", "spruce", j), "synonyms")
        self.assertEqual(j[0]["event"], "regression")

    def test_reward_explicable(self):
        self.assertEqual(meta.reward_of({"returned": 0}), 0.0)
        self.assertEqual(meta.reward_of({"returned": 4, "error": "HTTP 403"}), 0.0)
        self.assertGreater(meta.reward_of({"returned": 4, "new": 2, "technical_mean": 0.5}),
                           meta.reward_of({"returned": 4, "new": 2, "technical_mean": 0.5, "offtopic": 2}))


class EndToEndTests(unittest.TestCase):
    """Recherche -> Source -> Extraction -> Vérification -> Markdown -> Index -> Récupération (sans Roblox Studio)."""

    def test_full_chain(self):
        root = make_root()
        provs = {"roblox_docs": providers.RobloxDocs(root, fake_getter), "devforum": providers.DevForum(root, fake_getter, pause=0),
                 "github": providers.GitHub(root, fake_getter)}
        provs["roblox_docs"].path.write_text(json.dumps({"entries": providers.parse_llms_index((FIX / "llms.txt").read_text(encoding="utf-8"))}))
        provs["devforum"].refresh(5)
        st = runner.research(root, max_queries=1, per_source=3, max_fetch=10, pause=0, provs=provs)
        self.assertEqual(st["queries"], 1)
        self.assertEqual(st["trials"], 3)
        self.assertGreaterEqual(st["created"], 2)
        self.assertGreaterEqual(st["rejected"], 1)  # le « pet simulator » de GitHub
        self.assertEqual(st["errors"], [])
        notes = knowledge.load_notes(root)
        self.assertTrue(all(n["status"] in ("candidat", "documente") for n in notes))
        self.assertTrue(any(n.get("official") for n in notes))
        res = rag.search_knowledge("feuillage transparent de loin", root=root)
        self.assertTrue(res["results"])
        # second passage : aucune nouvelle fiche (déduplication), stats explicables
        st2 = runner.research(root, max_queries=1, per_source=3, max_fetch=10, pause=0, provs=provs)
        self.assertEqual(st2["created"], 0)
        self.assertGreaterEqual(st2["updated"] + st2["duplicates"], 1)
        self.assertTrue((root / "output" / "meta_report.md").exists())
        self.assertTrue((root / "knowledge" / "_index.md").exists())

    def test_provider_error_is_reported_not_hidden(self):
        root = make_root()

        class Broken:
            name, tier = "github", 3

            def search(self, q, n):
                raise providers.FetchError("HTTP 403 sur api.github.com")
        st = runner.research(root, max_queries=1, per_source=2, max_fetch=5, pause=0, provs={"github": Broken()})
        self.assertEqual(len(st["errors"]), 1)
        self.assertEqual(st["created"], 0)
        state = json.loads((root / "output" / "meta_state.json").read_text())
        arm = next(iter(state["arms"]["github:spruce"].values()))
        self.assertEqual(arm["errors"], 1)


if __name__ == "__main__":
    unittest.main()
