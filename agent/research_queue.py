"""V5.5 - file de recherche persistante (output/queue.json).

- Priorites, historique (output/queue_history.jsonl), deduplication par sens de la requete.
- Reprise apres interruption : un element reste "running" si le processus est coupe ; au chargement
  suivant, il repasse "pending" (sans compter une tentative de plus).
- Garde-fous : taille maximale, profondeur maximale des relances, nombre de tentatives, sujets autorises
  (config/topics.json) et termes exclus (config/autonomy.json).
- Ecriture atomique (fichier temporaire puis remplacement) : une coupure ne corrompt pas la file.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import time
from pathlib import Path

from agent.text import fold, tokens

ROOT = Path(__file__).resolve().parents[1]
STATUSES = ("pending", "running", "done", "failed", "skipped")

DEFAULTS = {
    "cycle": {"max_items": 4, "time_budget_s": 1500, "per_source": 4, "max_fetch_per_item": 8, "pause_s": 1.0},
    "daily": {"max_items": 40, "max_fetch": 300},
    "queue": {"max_size": 400, "max_depth": 2, "max_children_per_note": 3, "max_attempts": 3,
              "requery_after_days": 14, "stale_running_after_s": 7200},
    "lock": {"stale_after_s": 7200},
    "excluded_terms": [],
}


def load_config(root: Path = ROOT) -> dict:
    path = Path(root) / "config" / "autonomy.json"
    cfg = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    out = {}
    for k, v in DEFAULTS.items():
        out[k] = {**v, **cfg.get(k, {})} if isinstance(v, dict) else cfg.get(k, v)
    return out


def now_ts() -> float:
    return time.time()


def iso(ts: float | None = None) -> str:
    return dt.datetime.fromtimestamp(ts if ts is not None else now_ts(), dt.timezone.utc).isoformat(timespec="seconds")


def today(ts: float | None = None) -> str:
    return iso(ts)[:10]


def item_key(topic_id: str, query: str) -> str:
    """Meme sens = meme cle : ordre des mots, casse, accents et pluriels ignores.

    La cle ne depend pas du sujet : une meme recherche n'est jamais lancee deux fois sous deux sujets.
    (``topic_id`` est garde dans la signature pour compatibilite.)"""
    norm = " ".join(sorted(set(tokens(query)))) or fold(query).strip()
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def excluded_term(query: str, terms: list[str]) -> str | None:
    q = " " + re.sub(r"[^a-z0-9]+", " ", fold(query)) + " "
    for t in terms:
        if " " + re.sub(r"[^a-z0-9]+", " ", fold(t)).strip() + " " in q:
            return t
    return None


class ResearchQueue:
    def __init__(self, root: Path = ROOT, config: dict | None = None, topics: list[dict] | None = None):
        self.root = Path(root)
        self.cfg = config or load_config(self.root)
        self.path = self.root / "output" / "queue.json"
        self.history_path = self.root / "output" / "queue_history.jsonl"
        if topics is None:
            topics = json.loads((self.root / "config" / "topics.json").read_text(encoding="utf-8"))["topics"]
        self.topics = {t["id"]: t for t in topics}
        self.data = {"schema": "vdn.queue/1", "items": {}, "daily": {"date": "", "items": 0, "fetch": 0}}
        self.recovered = 0
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except ValueError:
                broken = self.path.with_suffix(".corrupt.json")
                self.path.replace(broken)
                self.log("queue_corrupt", {"moved_to": broken.name})
        self.data.setdefault("items", {})
        self.data.setdefault("daily", {"date": "", "items": 0, "fetch": 0})
        self._recover()

    # ------------------------------------------------------------------ persistance
    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.path)

    def log(self, event: str, payload: dict):
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with self.history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"utc": iso(), "event": event, **payload}, ensure_ascii=False) + "\n")

    def _recover(self):
        stale = self.cfg["queue"]["stale_running_after_s"]
        for it in self.data["items"].values():
            if it["status"] == "running":
                # Processus coupe : on reprend l'element. Au-dela du delai, on le compte comme un echec.
                if now_ts() - it.get("started_ts", 0) > stale:
                    it["attempts"] = it.get("attempts", 0) + 1
                it["status"] = "pending" if it.get("attempts", 0) < self.cfg["queue"]["max_attempts"] else "failed"
                self.recovered += 1
                self.log("recovered", {"key": it["key"], "query": it["query"], "status": it["status"]})

    # ------------------------------------------------------------------ ajout
    def add(self, topic_id: str, query: str, priority: float, origin: str = "seed", depth: int = 0,
            parent: str | None = None, reason: str = "") -> tuple[bool, str]:
        """Ajoute une recherche. Retourne (ajoutee, raison). Ne leve jamais d'exception pour une requete refusee."""
        q = re.sub(r"\s+", " ", query or "").strip()
        qc = self.cfg["queue"]
        if not q or not tokens(q):
            return False, "requete vide"
        if topic_id not in self.topics:
            return False, f"sujet non autorise : {topic_id}"
        bad = excluded_term(q, self.cfg.get("excluded_terms", []))
        if bad:
            self.log("excluded", {"query": q, "topic": topic_id, "term": bad})
            return False, f"terme exclu : {bad}"
        if depth > qc["max_depth"]:
            return False, f"profondeur {depth} > {qc['max_depth']}"
        key = item_key(topic_id, q)
        old = self.data["items"].get(key)
        if old:
            fresh = now_ts() - old.get("finished_ts", 0) < qc["requery_after_days"] * 86400
            if old["status"] in ("pending", "running") or (old["status"] == "done" and fresh) or old["status"] == "failed":
                return False, f"doublon ({old['status']})"
            # recherche ancienne terminee : on la remet en file (connaissances a rafraichir)
            old.update(status="pending", priority=priority, origin=origin, updated=iso())
            self.log("requeued", {"key": key, "query": q})
            return True, "remise en file"
        if self.pending_count() >= qc["max_size"]:
            return False, "file pleine"
        self.data["items"][key] = {
            "key": key, "topic": topic_id, "query": q, "priority": float(priority), "origin": origin,
            "depth": int(depth), "parent": parent, "reason": reason, "status": "pending", "attempts": 0,
            "created": iso(), "updated": iso(), "result": None,
        }
        self.log("added", {"key": key, "query": q, "topic": topic_id, "origin": origin, "depth": depth, "parent": parent})
        return True, "ajoutee"

    def best_topic(self, query: str, default: str) -> str:
        """Sujet autorise dont le vocabulaire (titre, sous-sujets, requetes) recouvre le plus la requete.
        Egalite : le sujet d'origine, puis le plus prioritaire. Aucun recouvrement : le sujet d'origine."""
        qt = set(tokens(query))
        scored = []
        for t in self.topics.values():
            vocab = set(tokens(" ".join([t.get("title", "")] + t.get("subtopics", []) + t.get("queries", []))))
            sc = len(qt & vocab)
            if sc:
                scored.append((sc, t["id"] == default, float(t.get("priority", 5)), t["id"]))
        return max(scored)[3] if scored else default

    def seed_from_topics(self) -> int:
        """Ajoute les requetes de base des sujets autorises qui ne sont ni en file, ni faites recemment."""
        n = 0
        for t in self.topics.values():
            for q in t.get("queries", []):
                ok, _ = self.add(t["id"], q, priority=float(t.get("priority", 5)), origin="seed", reason="requete de base du sujet")
                n += ok
        return n

    # ------------------------------------------------------------------ selection
    def pending_count(self) -> int:
        return sum(1 for it in self.data["items"].values() if it["status"] == "pending")

    def next_batch(self, n: int) -> list[dict]:
        """Plus haute priorite d'abord ; a priorite egale, les relances les plus profondes (approfondir).
        Un seul element par sujet tant que d'autres sujets attendent (variete)."""
        pend = sorted((it for it in self.data["items"].values() if it["status"] == "pending"),
                      key=lambda it: (-it["priority"], -it["depth"], it["created"], it["key"]))
        out, used = [], set()
        for it in pend:
            if len(out) >= n:
                break
            if it["topic"] not in used:
                out.append(it); used.add(it["topic"])
        for it in pend:
            if len(out) >= n:
                break
            if it not in out:
                out.append(it)
        return out

    # ------------------------------------------------------------------ cycle de vie
    def mark_running(self, it: dict):
        it.update(status="running", started_ts=now_ts(), updated=iso())
        self.save()
        self.log("started", {"key": it["key"], "query": it["query"]})

    def mark_done(self, it: dict, result: dict):
        it.update(status="done", finished_ts=now_ts(), updated=iso(), result=result)
        self.save()
        self.log("done", {"key": it["key"], "query": it["query"], "result": result})

    def mark_failed(self, it: dict, error: str):
        it["attempts"] = it.get("attempts", 0) + 1
        it.update(status="pending" if it["attempts"] < self.cfg["queue"]["max_attempts"] else "failed",
                  updated=iso(), last_error=error[:300])
        self.save()
        self.log("failed", {"key": it["key"], "query": it["query"], "error": error[:300], "attempts": it["attempts"]})

    # ------------------------------------------------------------------ quota quotidien
    def daily(self) -> dict:
        d = self.data["daily"]
        if d.get("date") != today():
            d.update(date=today(), items=0, fetch=0)
        return d

    def summary(self) -> dict:
        counts = {s: 0 for s in STATUSES}
        for it in self.data["items"].values():
            counts[it["status"]] = counts.get(it["status"], 0) + 1
        return {"counts": counts, "daily": dict(self.daily()),
                "next": [{"query": it["query"], "topic": it["topic"], "priority": it["priority"], "depth": it["depth"],
                          "origin": it["origin"]} for it in self.next_batch(5)]}
