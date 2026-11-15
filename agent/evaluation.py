"""Evidence diagnostics for Markdown, never an automatic technical truth score."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from agent.knowledge import parse_note, sections, _PARAM, _LIMIT
from agent.procedure import actionable_excerpts
from agent.text import fold

STATES = ('verifie', 'probable', 'hypothetique', 'non_resolu')
EMPTY = re.compile(r'(?i)(à compléter|a completer|aucun|non identifi|non etabli|non vérifi|non verifi|^—$)')


def evaluate_note(text: str) -> dict:
    meta, body = parse_note(text)
    sec = sections(body)
    excerpts = re.findall(r'^>\s*«\s*(.+?)\s*»\s*$', body, re.M)
    sources = [u for u in meta.get('sources', []) if isinstance(u, str) and
               urlparse(u).scheme == 'https' and urlparse(u).hostname and not urlparse(u).username]
    cited = [e for e in excerpts if re.search(
        r'^>\s*«\s*' + re.escape(e) + r'\s*»\s*\n>[^\n]*https://', body, re.M)]
    steps = actionable_excerpts(excerpts)

    def filled(*names):
        value = '\n'.join(sec.get(n, '') for n in names).strip()
        return bool(value and not EMPTY.search(value))

    # Values/constraints count only in source excerpts, not agent boilerplate.
    diagnostics = {
        'source_traceability': bool(sources and cited),
        'actionable_steps': bool(steps),
        'parameters': any(_PARAM.search(e) for e in excerpts),
        'constraints': any(_LIMIT.search(e) for e in excerpts),
        'prerequisites': filled('Prérequis', 'Prerequisites'),
        'alternatives': filled('Alternatives'),
        'reproducibility': filled('Protocole de reproduction', 'Reproduction protocol'),
    }
    warnings = []
    if not diagnostics['source_traceability']:
        warnings.append('affirmations sans extraits attribuables : non verifiees')
    if '## Analyse IA' in body:
        warnings.append('analyse IA : affirmation non verifiee meme si un extrait est cite')
    conflict = bool(re.search(r'(?i)contradic|sources?\s+(?:disagree|conflict)', body))
    if conflict:
        warnings.append('contradiction signalee : arbitrage externe requis')
    # A pre-existing validation label is reported, never promoted to proof.
    state = 'probable' if all(diagnostics[k] for k in ('source_traceability', 'actionable_steps')) else 'hypothetique'
    if not excerpts or conflict:
        state = 'non_resolu'
    if meta.get('status') in ('valide', 'reproduit') or fold(str(meta.get('tested_in_studio', ''))) == 'oui':
        warnings.append('validation declaree dans la fiche ; preuve non controlee automatiquement')
    return {'id': meta.get('id'), 'state': state, 'technical_accuracy': 'non_verifiee',
            'topic': meta.get('subdomain'),
            'source_tier': meta.get('source_tier'), 'source_reliability': 'a_evaluer',
            'diagnostics': diagnostics, 'gaps': [k for k, present in diagnostics.items() if not present],
            'warnings': warnings, 'excerpts': len(excerpts), 'attributed_excerpts': len(cited),
            'actionable_steps': len(steps), 'conflict': conflict,
            'queries': meta.get('queries', []), 'claimed_status': meta.get('status'),
            'truth_verified': False}


def evaluate_library(root: Path) -> dict:
    result = []
    for path in sorted((Path(root) / 'knowledge').rglob('*.md')):
        if not path.name.startswith('_'):
            result.append({'path': path.relative_to(root).as_posix(), **evaluate_note(path.read_text(encoding='utf-8'))})
    return {'schema': 'vdn.evaluation/1', 'method': 'structural evidence diagnostics; no truth score', 'notes': result}
