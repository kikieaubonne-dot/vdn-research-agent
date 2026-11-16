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
import uuid
from pathlib import Path

from agent.text import fold, tokens
from agent.storage import atomic_write
from agent.priority import explain

ROOT = Path(__file__).resolve().parents[1]
STATUSES = ("pending", "running", "done", "failed", "skipped")

DEFAULTS = {
    "cycle": {"max_items": 4, "time_budget_s": 1200, "per_source": 4, "max_fetch_per_item": 8, "pause_s": 1.0,
              "max_http_calls": 100},
    "daily": {"max_items": 40, "max_fetch": 300, "max_http_calls": 600},
    "queue": {"max_size": 400, "max_depth": 2, "max_children_per_note": 3, "max_attempts": 3,
              "requery_after_days": 14, "stale_running_after_s": 7200,
              "max_children_per_item": 6, "stagnation_limit": 2, 'max_plan_nodes': 12},
    "lock": {"stale_after_s": 7200},
    "excluded_terms": [],
}


def load_config(root: Path = ROOT) -> dict:
    path = Path(root) / "config" / "autonomy.json"
    cfg = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    out = {}
    for k, v in DEFAULTS.items():
        out[k] = {**v, **cfg.get(k, {})} if isinstance(v, dict) else cfg.get(k, v)
    # Reject invalid configuration before any quota-controlled work.
    import math
    for section in ('cycle', 'daily', 'queue', 'lock'):
        for name, value in out[section].items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f'limite invalide : {section}.{name}')
            if not name.endswith('_s') and not name.endswith('_days') and int(value) != value:
                raise ValueError(f'limite entiere requise : {section}.{name}')
    if out['lock']['stale_after_s'] <= out['cycle']['time_budget_s']:
        raise ValueError('expiration du verrou doit depasser le budget du cycle')
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
    # Keep research facets previously lost as stopwords (e.g. limitations).
    facets = set(re.findall(r'\b(?:limitations|implementation|troubleshooting)\b', fold(query)))
    norm = " ".join(sorted(set(tokens(query)) | facets)) or fold(query).strip()
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def excluded_term(query: str, terms: list[str]) -> str | None:
    q = " " + re.sub(r"[^a-z0-9]+", " ", fold(query)) + " "
    for t in terms:
        if " " + re.sub(r"[^a-z0-9]+", " ", fold(t)).strip() + " " in q:
            return t
    return None


class ResearchQueue:
    def __init__(self, root: Path = ROOT, config: dict | None = None, topics: list[dict] | None = None,
                 recover: bool = True, state_dir: Path | None = None):
        self.root = Path(root)
        self.cfg = config or load_config(self.root)
        folder=Path(state_dir) if state_dir is not None else self.root/'output'
        if state_dir is not None:
            from agent.obsidian import safe_path
            if not folder.absolute().is_relative_to(self.root.resolve()/'lab'):
                raise ValueError('isolated queue must be under lab/')
            folder=safe_path(self.root,folder.absolute().relative_to(self.root.resolve()).as_posix())
        self.path = folder / "queue.json"
        self.history_path = folder / "queue_history.jsonl"
        if state_dir is not None:
            self.path=safe_path(self.root,self.path.relative_to(self.root).as_posix())
            self.history_path=safe_path(self.root,self.history_path.relative_to(self.root).as_posix())
        if topics is None:
            topics = json.loads((self.root / "config" / "topics.json").read_text(encoding="utf-8"))["topics"]
        self.topics = {t["id"]: t for t in topics}
        self.data = {"schema": "vdn.queue/1", "items": {}, "daily": {"date": "", "items": 0, "fetch": 0}}
        self.recovered = 0
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
                if state_dir is not None:
                    if not isinstance(self.data,dict) or self.data.get('schema')!='vdn.queue/1' or not isinstance(self.data.get('items'),dict) or not isinstance(self.data.get('daily'),dict):raise ValueError('invalid isolated queue structure')
                    for key,item in self.data['items'].items():
                        if not isinstance(item,dict) or item.get('key')!=key or item.get('status') not in STATUSES or not isinstance(item.get('query'),str) or type(item.get('depth')) is not int:raise ValueError('invalid isolated queue item')
            except ValueError:
                if state_dir is not None:raise ValueError('isolated queue corrupt; manual recovery required')
                if not recover:
                    raise ValueError('queue illisible ; inspection sans modification')
                broken = self.path.with_suffix(".corrupt.json")
                if broken.exists():
                    broken = self.path.with_name(f'queue.corrupt.{uuid.uuid4().hex}.json')
                self.path.replace(broken)
                self.log("queue_corrupt", {"moved_to": broken.name})
        self.data.setdefault("items", {})
        self.data.setdefault("daily", {"date": "", "items": 0, "fetch": 0})
        if recover:
            self._recover()

    # ------------------------------------------------------------------ persistance
    def save(self):
        atomic_write(self.path, json.dumps(self.data, ensure_ascii=False, indent=2) + "\n")

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
            parent: str | None = None, reason: str = "", dependencies: list[str] | None = None,
            research_signals: dict | None = None) -> tuple[bool, str]:
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
        dependencies = list(dict.fromkeys(dependencies or []))
        if any(d == key or d not in self.data['items'] for d in dependencies):
            return False, 'prerequis inexistant ou cyclique'
        # Legacy keys remain stable, including references from existing history.
        old = self.data["items"].get(key) or next((it for it in self.data['items'].values()
                    if item_key('', it['query']) == key), None)
        if old:
            fresh = now_ts() - old.get("finished_ts", 0) < qc["requery_after_days"] * 86400
            if old["status"] in ("pending", "running", "skipped") or (old["status"] == "done" and fresh) or old["status"] == "failed":
                return False, f"doublon ({old['status']})"
            # recherche ancienne terminee : on la remet en file (connaissances a rafraichir)
            old.update(status="pending", priority=priority, origin=origin, updated=iso())
            self.log("requeued", {"key": key, "query": q})
            return True, "remise en file"
        if self.pending_count() >= qc["max_size"]:
            return False, "file pleine"
        if parent in self.data['items']:
            if depth <= self.data['items'][parent]['depth']:
                return False, 'profondeur enfant doit depasser celle du parent'
            cap = qc['max_children_per_item'] if origin != 'decomposition' else qc['max_plan_nodes']
            if sum(it.get('parent') == parent for it in self.data['items'].values()) >= cap:
                return False, 'plafond enfants du parent atteint'
        self.data["items"][key] = {
            "key": key, "topic": topic_id, "query": q, "priority": float(priority), "origin": origin,
            "depth": int(depth), "parent": parent, "reason": reason, "status": "pending", "attempts": 0,
            "created": iso(), "updated": iso(), "result": None,
            'dependencies': dependencies, 'research_signals': research_signals or {},
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
        """Explainable live ranking, prerequisite gating, then topic diversity."""
        items = list(self.data['items'].values())
        evaluations = self._evaluations()
        pend = [it for it in items if it['status'] == 'pending' and not self.blocked_by(it)]
        ranks = {it['key']: explain(it, items, evaluations) for it in pend}
        pend.sort(key=lambda it: (ranks[it['key']]['rank'], -it['depth'], it['created'], it['key']))
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

    def blocked_by(self, it):
        blocked = []
        for dep in it.get('dependencies', []):
            parent = self.data['items'].get(dep, {})
            result = parent.get('result') or {}
            if parent.get('status') != 'done' or not result.get('knowledge_available', bool(result.get('created'))):
                blocked.append(dep)
        return blocked

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
            d.update(date=today(), items=0, fetch=0, http_calls=0)
        d.setdefault('http_calls', 0)
        return d

    def summary(self) -> dict:
        counts = {s: 0 for s in STATUSES}
        for it in self.data["items"].values():
            counts[it["status"]] = counts.get(it["status"], 0) + 1
        return {"counts": counts, "daily": dict(self.daily()),
                'blocked': [{'key': it['key'], 'dependencies': self.blocked_by(it)} for it in self.data['items'].values()
                            if it['status'] == 'pending' and self.blocked_by(it)],
                "next": [{"query": it["query"], "topic": it["topic"], "priority": it["priority"], "depth": it["depth"],
                          "origin": it["origin"], 'ranking': explain(it, list(self.data['items'].values()),
                              self._evaluations())} for it in self.next_batch(5)]}

    def _evaluations(self):
        path = self.root / 'output' / 'knowledge_evaluation.json'
        return json.loads(path.read_text(encoding='utf-8'))['notes'] if path.exists() else []
