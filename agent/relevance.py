"""Évaluation d'une source en scores SÉPARÉS (jamais un score opaque unique).

- topical   : la source parle-t-elle du sujet demandé ? (concepts + termes de la requête, sur le CONTENU lu)
- roblox    : la source concerne-t-elle Roblox ou un outil de la chaîne (Blender…) ?
- noise     : signes d'une source hors sujet (portfolio, recrutement, vitrine de jeu…), avec la raison
- technical : densité de passages techniques exploitables (paramètres, réglages, limites)

Ces scores mesurent la PERTINENCE et l'UTILITÉ APPARENTE, pas la véracité ni la validation dans Roblox.
Correction V4.1 : V4 calculait la pertinence sur le seul titre « propriétaire/dépôt » d'un résultat GitHub, alors que
GitHub l'avait trouvé grâce au README -> pertinence 0,0 systématique. On évalue maintenant le contenu réellement lu.
"""
from __future__ import annotations
import re
from agent.text import tokens, concepts, vocabulary, fold, contains_phrase

ACCEPT = {"topical": 0.5, "technical": 0.15}

# Phrases techniques « exploitables » : réglage, valeur, procédure, limite.
DETAIL = re.compile(
    r"(?i)(\b\d+(?:[.,]\d+)?\s*(?:px|k|kb|mb|ms|fps|studs?|tris|triangles?|vertices|bones?|degrees?|°|%)\b"
    r"|\b(?:set|enable|disable|change|use|export|import|bake|create|adjust|configure|fix|solution|workaround|steps?"
    r"|parameter|setting|property|limit|maximum|minimum|max|min|must|cannot|can't|only|supports?|tested|reproduce"
    r"|régler|activer|désactiver|limite|maximum|propriété)\b|=)")


def tech_terms(text: str) -> list[str]:
    voc = vocabulary()
    found = []
    for t in voc.get("tech", []):
        if contains_phrase(text, t):
            found.append(t)
    return found


def noise_reasons(title: str, text: str = "") -> list[str]:
    """Raisons de rejet évidentes, cherchées surtout dans le titre (le corps peut citer « portfolio » par hasard)."""
    voc = vocabulary()
    reasons = []
    for phrase in voc.get("noise", []):
        if contains_phrase(title, phrase):
            reasons.append(f"titre : « {phrase} »")
    head = fold(text[:600])
    for phrase in ("looking for", "hiring", "commissions open", "commissions closed", "for hire", "my portfolio"):
        if phrase in head and f"titre : « {phrase} »" not in reasons:
            reasons.append(f"début du texte : « {phrase} »")
    return reasons


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p and p.strip()]


def technical_excerpts(text: str, limit: int = 8, min_len: int = 40, max_len: int = 420) -> list[str]:
    """Phrases contenant à la fois un terme technique et un détail actionnable. Citations courtes, dédupliquées."""
    out, seen = [], set()
    for s in sentences(text):
        if not (min_len <= len(s) <= max_len):
            continue
        if not DETAIL.search(s) or not tech_terms(s):
            continue
        key = fold(s)[:120]
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
        if len(out) >= limit:
            break
    return out


def assess(query: str, title: str, text: str, provider: str = "", topic_concepts: set | None = None) -> dict:
    """Retourne les scores séparés et la décision, avec les raisons (pour le diagnostic)."""
    voc = vocabulary()
    q_tokens = tokens(query)
    q_concepts = concepts(q_tokens) | set(topic_concepts or ())
    doc = f"{title}\n{text}"
    d_tokens = tokens(doc)
    d_set = set(d_tokens)
    d_concepts = concepts(d_tokens)
    # Couverture des termes de la requête (hors « roblox », trop fréquent) et des concepts.
    q_terms = [t for t in dict.fromkeys(q_tokens) if t not in ("roblox",)]
    term_cov = (sum(t in d_set for t in q_terms) / len(q_terms)) if q_terms else 0.0
    concept_cov = (len(q_concepts & d_concepts) / len(q_concepts)) if q_concepts else term_cov
    topical = round(0.5 * term_cov + 0.5 * concept_cov, 3)
    roblox = provider in ("roblox_docs", "devforum") or any(contains_phrase(doc[:20000], w) for w in voc.get("roblox_signal", []))
    reasons_noise = noise_reasons(title, text)
    excerpts = technical_excerpts(text)
    terms_found = tech_terms(text[:30000])
    technical = round(min(1.0, 0.12 * len(excerpts) + 0.04 * len(terms_found)), 3)
    reasons = []
    if topical < ACCEPT["topical"]:
        reasons.append(f"hors sujet (pertinence {topical} < {ACCEPT['topical']})")
    if not roblox:
        reasons.append("aucun lien avec Roblox ou la chaîne Blender")
    if reasons_noise:
        reasons.append("bruit : " + ", ".join(reasons_noise))
    if technical < ACCEPT["technical"]:
        reasons.append(f"pas assez de contenu technique ({technical})")
    return {
        "topical": topical, "term_coverage": round(term_cov, 3), "concept_coverage": round(concept_cov, 3),
        "roblox": roblox, "noise": reasons_noise, "technical": technical,
        "excerpts": excerpts, "tech_terms": terms_found[:15],
        "accepted": not reasons, "reasons": reasons,
    }
