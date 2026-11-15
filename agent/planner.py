"""Planification des requêtes (inspirée de STORM : points de vue ; de GPT Researcher : sous-questions).

Corrections V4.1 :
- Les requêtes de suivi V3 (« <sujet> Roblox <terme> implementation limitations troubleshooting ») étaient triées
  AVANT les requêtes de base car jamais lancées (tri par nombre d'exécutions croissant) ; trop longues, elles ne
  renvoyaient presque rien. Ici : requêtes courtes (2 à 4 termes), suivis plafonnés à 25 % des requêtes d'une session,
  et équilibre entre sujets (tourniquet pondéré par la priorité).
"""
from __future__ import annotations
import json
from pathlib import Path

from agent.text import tokens, expand

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("terms", "synonyms", "facet")
FACETS = {"settings": "settings", "limits": "limit", "performance": "performance", "issue": "bug"}


def short(query: str, n: int = 4) -> str:
    words = [w for w in dict.fromkeys(query.split()) if w.lower() not in ("roblox", "studio")]
    meaningful = [w for w in words if tokens(w)]
    return " ".join(meaningful[:n])


def variants(query: str) -> dict[str, str]:
    """Trois formulations comparables (même longueur), pour la méta-recherche."""
    base = short(query)
    words = base.split()
    syn = base
    for i, w in enumerate(words):
        alts = [a for a in expand(w) if a.lower() != w.lower() and " " not in a]
        if alts:
            syn = " ".join(words[:i] + [alts[0]] + words[i + 1:])
            break
    facet_word = list(FACETS.values())[sum(map(ord, base)) % len(FACETS)]
    facet = " ".join((words[:3] + [facet_word]))
    return {"terms": base, "synonyms": syn, "facet": facet}


def load_topics(root: Path = ROOT) -> list[dict]:
    cfg = json.loads((Path(root) / "config" / "topics.json").read_text(encoding="utf-8"))
    return cfg["topics"]


def plan(state: dict, root: Path = ROOT, max_queries: int = 8, followups: list[dict] | None = None) -> list[tuple[dict, str, str]]:
    """Retourne [(topic, requête, origine)]. Équilibre : priorité, puis requêtes les moins lancées, sujets en tourniquet."""
    topics = load_topics(root)
    runs = state.setdefault("query_runs", {})
    buckets = []
    for t in sorted(topics, key=lambda t: -int(t.get("priority", 5))):
        qs = [(runs.get(q, 0), i, q) for i, q in enumerate(t.get("queries", []))]
        qs.sort()
        buckets.append((t, [q for _, _, q in qs]))
    chosen: list[tuple[dict, str, str]] = []
    max_follow = max(0, max_queries // 4)
    by_id = {t["id"]: t for t in topics}
    for f in (followups or [])[:max_follow]:
        if f.get("topic") in by_id:
            chosen.append((by_id[f["topic"]], short(f["query"]), "suivi"))
    rot = int(state.get("rotation", 0))
    if buckets:
        buckets = buckets[rot % len(buckets):] + buckets[:rot % len(buckets)]
    while len(chosen) < max_queries and any(b[1] for b in buckets):
        for t, qs in buckets:
            if qs and len(chosen) < max_queries:
                q = qs.pop(0)
                # un sujet prioritaire (≥ 9) peut prendre deux places par tour
                chosen.append((t, q, "base"))
                if int(t.get("priority", 5)) >= 9 and qs and len(chosen) < max_queries:
                    chosen.append((t, qs.pop(0), "base"))
    state["rotation"] = rot + 1
    return chosen
