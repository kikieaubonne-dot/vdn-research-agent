"""V5.5 - relances deterministes (sans IA, sans token) a partir d'une fiche creee.

Une fiche nouvelle peut produire au plus ``max_children`` questions complementaires :
- les API Roblox citees par la source (``Class.SpotLight.Angle|Angle`` -> "SpotLight Angle") ;
- les lacunes detectees dans la fiche : pas de parametre chiffre -> "<API> settings",
  pas de limite -> "<API> limitations", aucune etape -> "<API> tutorial".

Chaque relance porte sa raison, pour que le rapport explique pourquoi l'agent creuse.
La file applique ensuite profondeur maximale, exclusions et deduplication.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from agent.knowledge import parse_note
from agent.structure import extract_api_refs
from agent.text import tokens

GAP_MARKERS = (
    ("Aucun paramètre chiffré trouvé", "settings", "aucun parametre chiffre dans la source"),
    ("Aucune limite explicite trouvée", "limitations", "aucune limite Roblox citee"),
    ("Aucune instruction complete identifiee", "tutorial", "aucune etape exploitable"),
)


def _api_terms(body: str) -> list[tuple[str, str]]:
    """(classe, propriete) dans l'ordre de frequence, a partir des references Roblox de la fiche."""
    refs = [r for r in extract_api_refs(body) if r["kind"] in ("Class", "Enum")]
    counts = Counter()
    for r in extract_api_refs(body):
        if r["kind"] in ("Class", "Enum"):
            counts[r["name"]] += 1
    seen, out = set(), []
    for r in sorted(refs, key=lambda r: -counts[r["name"]]):
        parts = r["name"].split(".")[1:]
        if not parts:
            continue
        cls, prop = parts[0], (parts[1] if len(parts) > 1 else "")
        if (cls, prop) in seen:
            continue
        seen.add((cls, prop))
        out.append((cls, prop))
    return out


def missing_info(body: str) -> list[str]:
    return [why for marker, _, why in GAP_MARKERS if marker in body]


def followups_for_note(note_path: Path, parent_query: str, max_children: int = 3) -> list[dict]:
    """Questions complementaires pour une fiche. Retourne [{'query', 'reason'}] (au plus max_children)."""
    meta, body = parse_note(Path(note_path).read_text(encoding="utf-8"))
    if meta.get("status") not in ("documente", "candidat"):
        return []
    parent_tokens = set(tokens(parent_query))
    apis = _api_terms(body)
    main = apis[0][0] if apis else ""
    out: list[dict] = []

    def push(query: str, reason: str):
        q = " ".join(query.split())
        if not q or len(out) >= max_children:
            return
        if set(tokens(q)) <= parent_tokens:  # rien de nouveau par rapport a la requete d'origine
            return
        if any(set(tokens(q)) == set(tokens(o["query"])) for o in out):
            return
        out.append({"query": q, "reason": reason})

    # 1. lacunes de la fiche, sur l'API principale (ou la requete d'origine si la source n'en cite aucune)
    subject = main or " ".join(parent_query.split()[:3])
    for marker, facet, why in GAP_MARKERS:
        if marker in body:
            push(f"{subject} {facet}", f"lacune : {why} ({meta.get('id')})")
    # 2. proprietes Roblox citees par la source, a approfondir
    for cls, prop in apis:
        if prop:
            push(f"{cls} {prop}", f"API citee par la source : {cls}.{prop} ({meta.get('id')})")
    return out
