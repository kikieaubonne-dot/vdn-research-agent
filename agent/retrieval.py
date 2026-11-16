"""Balanced bilingual query groups. Retrieval vocabulary is not proof metadata."""
import re
from agent.text import tokens, fold, expand

# Narrow technical equivalences avoid the acquisition vocabulary's wind/bone and
# general animation/rig ambiguity. No question-specific or note-ID exceptions.
EQUIVALENTS = (
    'rig rigging skeleton squelette armature',
    'bone bones os',
    'wind vent sway',
    'custom customised customized personnalise personnalisee personnalises personnalisees',
    'import importing imported importer importation importe',
    'export exporting exported exporter exportation exporte',
    'bug bugs glitch glitches buguent bugguent bugue erreur erreurs issues',
    'forest foret bois woodland',
    'snow neige snowy enneige enneigee enneigees enneiges',
    'performance performances optimization optimisation optimiser optimize',
    'lighting light eclairage lumiere nocturne night nuit',
    'atmosphere atmospheric atmospherique',
    'fog mist brouillard brume',
    'density densite',
    'haze',
)


def groups(query):
    result, seen = [], set()
    for word in dict.fromkeys(tokens(query)):
        if word in ('roblox', 'studio'):
            continue
        aliases = next((s.split() for s in EQUIVALENTS if word in tokens(s)), expand(word))
        terms = tuple(dict.fromkeys([word] + [fold(a) for a in aliases if ' ' not in a]))
        normalized = frozenset(tokens(' '.join(terms)))
        if normalized not in seen:
            result.append((word, terms, normalized))
            seen.add(normalized)
    return result


def expanded(query):
    return list(dict.fromkeys(t for _, aliases, _ in groups(query) for t in aliases[:12]))


def coverage(query_groups, title, text):
    tt, bt = set(tokens(title)), set(tokens(text))
    matched = [name for name, _, aliases in query_groups if aliases & (tt | bt)]
    title_matched = [name for name, _, aliases in query_groups if aliases & tt]
    return {'matched': matched, 'title_matched': title_matched,
            'coverage': len(matched) / max(1, len(query_groups)),
            'title_coverage': len(title_matched) / max(1, len(query_groups))}
