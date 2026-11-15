"""Relances prudentes sur les sources rejetees : aucune IA, aucune invention de preuve.

Une relance est une QUESTION de recherche, jamais une fiche de connaissance.
Les pages manifestement hors sujet/bruitees ne produisent pas de relances.
"""
from __future__ import annotations


def propose(query: str, candidates: list[dict], max_children: int = 2) -> list[dict]:
    """Construit des recherches ciblees sur les lacunes des pages proches du sujet."""
    eligible = [c for c in candidates if c.get('topical', 0) >= 0.5 and not c.get('noise')]
    if not eligible or max_children <= 0:
        return []
    out = []
    def add(suffix, reason):
        if len(out) < max_children:
            out.append({'query': f'{query} {suffix}', 'reason': reason})
    if any(c.get('technical', 0) < 0.15 for c in eligible):
        add('step by step implementation tutorial code', 'sources pertinentes mais sans etapes techniques suffisantes')
    if any(not c.get('roblox') for c in eligible):
        add('Roblox Studio implementation compatibility', 'compatibilite Roblox non etablie')
    if not out:
        add('exact settings limitations examples', 'approfondir les details des sources rejetees')
    return out
