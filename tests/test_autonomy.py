"""V5.5 - tests hors ligne du moteur autonome (file, relances, verrou, quotas, rapport, reprise)."""
import json
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from agent import autonomy
from agent.followup_rules import followups_for_note
from agent.research_queue import ResearchQueue, item_key, load_config

REPO = Path(__file__).resolve().parents[1]


class FakeDocs:
    """Imite RobloxDocs : une page officielle par requete, avec des references Roblox."""
    name, tier = "roblox_docs", 1

    def __init__(self):
        self.searches = []
        self.path = Path("unused")

    def search(self, query, limit=4):
        self.searches.append(query)
        slug = "-".join(query.lower().split())
        return [{"url": f"https://create.roblox.com/docs/fake/{slug}", "title": f"Guide {query}", "provider": self.name, "tier": 1}]

    def fetch(self, url):
        topic = url.rsplit("/", 1)[-1].replace("-", " ")
        text = (f"# Guide {topic}\n\nThis page explains {topic} in Roblox Studio for first person horror games.\n\n"
                f"## Setup\n\n"
                f"1. Insert a `Class.SpotLight` into the flashlight part to light the {topic} scene.\n"
                f"2. Set the `Class.SpotLight.Brightness|Brightness` property to 2 so the {topic} stays readable at night.\n"
                f"3. Set the `Class.SpotLight.Range|Range` property to 40 studs and enable `Class.SpotLight.Shadows|Shadows`.\n\n"
                f"Use the `Class.Camera.FieldOfView|FieldOfView` property of the camera to adjust {topic} immersion.\n")
        return {"title": f"Guide {topic}", "text": text, "official": True, "meta": {"kind": "documentation officielle"}}


def make_root(**overrides):
    root = Path(tempfile.mkdtemp(prefix="vdn_auto_"))
    # Frozen test contract, independent of personal network/model/quota settings.
    shutil.copytree(Path(__file__).parent / "fixtures" / "config", root / "config")
    cfg = json.loads((root / "config" / "autonomy.json").read_text(encoding="utf-8"))
    cfg["cycle"]["pause_s"] = 0
    for section, values in overrides.items():
        cfg[section].update(values)
    (root / "config" / "autonomy.json").write_text(json.dumps(cfg), encoding="utf-8")
    return root


def run_cycle(root, **kw):
    return autonomy.cycle(root, provs={"roblox_docs": FakeDocs()}, **kw)


class CycleDemoTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_full_autonomous_cycle(self):
        """Demarre, choisit, cherche, filtre, sauvegarde, memorise, prepare la suite."""
        s = run_cycle(self.root, max_items=2)
        self.assertEqual(s["stop_reason"], "cycle termine")
        self.assertGreater(s["seeded"], 40)                       # demarre : file amorcee depuis les sujets
        self.assertEqual(len(s["items"]), 2)                      # choisit 2 sujets differents
        self.assertNotEqual(s["items"][0]["topic"], s["items"][1]["topic"])
        q0 = ResearchQueue(self.root)
        self.assertEqual(q0.topics[s["items"][0]["topic"]]["priority"], 10)  # priorite la plus haute en premier
        self.assertGreaterEqual(s["created"], 2)                  # cherche, filtre, sauvegarde
        notes = list((self.root / "knowledge").rglob("*.md"))
        self.assertTrue(any("tested_in_studio: \"non\"" in n.read_text(encoding="utf-8") for n in notes))
        self.assertGreater(s["followups_added"], 0)               # prepare des relances
        q = json.loads((self.root / "output" / "queue.json").read_text(encoding="utf-8"))
        done = [it for it in q["items"].values() if it["status"] == "done"]
        relances = [it for it in q["items"].values() if it["origin"] == "relance"]
        self.assertEqual(len(done), 2)                            # memorise
        self.assertTrue(all(r["depth"] == 1 and r["parent"] and r["reason"] for r in relances))
        history = (self.root / "output" / "queue_history.jsonl").read_text(encoding="utf-8")
        self.assertIn('"event": "started"', history)
        self.assertIn('"event": "done"', history)
        report = (self.root / s["report"]).read_text(encoding="utf-8")
        self.assertIn("Prochaines recherches", report)
        self.assertIn("relance", report)
        self.assertTrue((self.root / "output" / "last_cycle.json").exists())
        self.assertFalse((self.root / "output" / "vdn.lock").exists())

    def test_second_cycle_continues_without_repeating(self):
        s1 = run_cycle(self.root, max_items=2)
        s2 = run_cycle(self.root, max_items=2)
        first = {(i["topic"], i["query"]) for i in s1["items"]}
        second = {(i["topic"], i["query"]) for i in s2["items"]}
        self.assertFalse(first & second)
        self.assertEqual(s2["seeded"], 0)
        report = next((self.root / "output" / "reports").glob("*.md")).read_text(encoding="utf-8")
        self.assertEqual(report.count("## Cycle"), 2)             # le rapport du jour s'enrichit

    def test_existing_note_never_rewritten(self):
        run_cycle(self.root, max_items=1)
        note = next((self.root / "knowledge").rglob("*.md"))
        before = note.read_bytes()
        q = ResearchQueue(self.root)
        first = next(it for it in q.data["items"].values() if it["status"] == "done")
        # meme sujet, requete reformulee qui ramene la meme URL
        q.add(first["topic"], first["query"], priority=99, origin="test")
        q.data["items"][item_key(first["topic"], first["query"])]["status"] = "done"
        q.save()
        fake = FakeDocs()
        fake.search = lambda query, limit=4: [{"url": "https://create.roblox.com/docs/fake/" +
                                               "-".join(first["query"].lower().split()), "title": "x"}]
        autonomy.cycle(self.root, provs={"roblox_docs": fake}, max_items=1)
        self.assertEqual(note.read_bytes(), before)


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.root = make_root()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_excluded_topics_refused(self):
        q = ResearchQueue(self.root)
        for bad in ("brainrot simulator", "robux currency shop", "pet tycoon", "game pass marketing"):
            ok, why = q.add("lighting", bad, 9)
            self.assertFalse(ok, bad)
            self.assertIn("terme exclu", why)
        self.assertTrue(q.add("lighting", "flashlight shadows idle animation", 9)[0])

    def test_unknown_topic_refused(self):
        self.assertFalse(ResearchQueue(self.root).add("crypto", "token price", 9)[0])

    def test_depth_limit(self):
        q = ResearchQueue(self.root)
        self.assertFalse(q.add("lighting", "spotlight range", 5, depth=3)[0])
        self.assertTrue(q.add("lighting", "spotlight range", 5, depth=2)[0])

    def test_semantic_duplicate(self):
        q = ResearchQueue(self.root)
        self.assertTrue(q.add("lighting", "SpotLight Angle", 5)[0])
        ok, why = q.add("lighting", "angle  spotlights", 5)
        self.assertFalse(ok)
        self.assertIn("doublon", why)

    def test_same_query_never_queued_under_two_topics(self):
        q = ResearchQueue(self.root)
        self.assertTrue(q.add("lighting", "SpotLight Brightness", 5)[0])
        self.assertFalse(q.add("forest", "spotlight brightness", 5)[0])

    def test_followup_routed_to_best_topic(self):
        q = ResearchQueue(self.root)
        self.assertEqual(q.best_topic("SpotLight shadows", "spruce"), "lighting")
        self.assertEqual(q.best_topic("zzz qqq", "spruce"), "spruce")
        self.assertEqual(q.best_topic("Camera FieldOfView", "spruce"), "fps_camera")

    def test_queue_size_cap(self):
        root = make_root(queue={"max_size": 3})
        try:
            q = ResearchQueue(root)
            self.assertEqual(q.seed_from_topics(), 3)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_followups_stop_at_max_depth(self):
        root = make_root(queue={"max_depth": 0})
        try:
            s = run_cycle(root, max_items=2)
            self.assertGreater(s["created"], 0)
            self.assertEqual(s["followups_added"], 0)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_daily_quota(self):
        root = make_root(daily={"max_items": 1})
        try:
            self.assertEqual(len(run_cycle(root, max_items=4)["items"]), 1)
            s = run_cycle(root, max_items=4)
            self.assertEqual(s["items"], [])
            self.assertEqual(s["stop_reason"], "quota quotidien atteint")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_time_budget(self):
        s = run_cycle(self.root, max_items=4, time_budget_s=-1)
        self.assertEqual(s["items"], [])
        self.assertEqual(s["stop_reason"], "budget de temps atteint")

    def test_lock_blocks_concurrent_cycle(self):
        lock = self.root / "output" / "vdn.lock"
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text(json.dumps({"pid": 1, "started": "maintenant", "ts": time.time()}), encoding="utf-8")
        s = run_cycle(self.root, max_items=2)
        self.assertIn("deja en cours", s["stop_reason"])
        self.assertEqual(s["items"], [])
        self.assertTrue(lock.exists())                            # le verrou d'un autre cycle n'est pas supprime

    def test_stale_lock_taken_over(self):
        lock = self.root / "output" / "vdn.lock"
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text(json.dumps({"pid": 1, "started": "hier", "ts": time.time() - 99999}), encoding="utf-8")
        s = run_cycle(self.root, max_items=1)
        self.assertTrue(s["lock_taken_over"])
        self.assertEqual(len(s["items"]), 1)

    def test_error_logged_and_retried_not_fatal(self):
        calls = []

        def boom(*a, **k):
            calls.append(1)
            raise ConnectionError("reseau coupe")
        s = autonomy.cycle(self.root, provs={}, max_items=2, research_fn=boom)
        self.assertEqual(len(calls), 2)                           # le cycle continue apres une erreur
        self.assertEqual([i["status"] for i in s["items"]], ["echec", "echec"])
        errors = (self.root / "output" / "errors.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(errors), 2)
        self.assertIn("reseau coupe", errors[0])
        q = ResearchQueue(self.root)
        failed = [it for it in q.data["items"].values() if it.get("last_error")]
        self.assertTrue(all(it["status"] == "pending" and it["attempts"] == 1 for it in failed))

    def test_gives_up_after_max_attempts(self):
        q = ResearchQueue(self.root)
        q.add("lighting", "spotlight range", 5)
        it = q.data["items"][item_key("lighting", "spotlight range")]
        for _ in range(load_config(self.root)["queue"]["max_attempts"]):
            q.mark_failed(it, "erreur")
        self.assertEqual(it["status"], "failed")

    def test_resume_after_interruption(self):
        q = ResearchQueue(self.root)
        q.add("lighting", "spotlight range", 5)
        it = q.data["items"][item_key("lighting", "spotlight range")]
        q.mark_running(it)                                         # coupure ici (PC eteint, plantage...)
        q2 = ResearchQueue(self.root)
        self.assertEqual(q2.recovered, 1)
        self.assertEqual(q2.data["items"][it["key"]]["status"], "pending")
        self.assertEqual(q2.data["items"][it["key"]]["attempts"], 0)

    def test_corrupt_queue_file_kept_aside(self):
        p = self.root / "output" / "queue.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{pas du json", encoding="utf-8")
        q = ResearchQueue(self.root)
        self.assertEqual(q.data["items"], {})
        self.assertTrue((self.root / "output" / "queue.corrupt.json").exists())


class FollowupRuleTests(unittest.TestCase):
    def test_followups_from_note(self):
        root = make_root()
        try:
            s = run_cycle(root, max_items=1)
            note = root / s["items"][0]["notes"][0]["path"]
            fs = followups_for_note(note, s["items"][0]["query"], 3)
            self.assertLessEqual(len(fs), 3)
            self.assertTrue(all(f["reason"] for f in fs))
            self.assertTrue(any(f["query"].startswith("SpotLight") for f in fs))
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
