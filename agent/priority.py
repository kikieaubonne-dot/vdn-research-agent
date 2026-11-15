"""Lexicographic research policy, independent of engineering P0/P1 priorities.

No fitted or arbitrary weighted sum: project utility first, prerequisite leverage
second, then evidence gaps, novelty, source prior, uncertainty and estimated cost.
The queue keeps topic diversity after ranking. Unknown inputs remain explicit.
"""
from agent.text import fold

ORDER = ('project_utility', 'unblocks', 'gap_importance', 'novelty', 'source_quality',
         'uncertainty', 'cost', 'duplication_risk')


def explain(item, items, evaluations=()):
    matched = [n for n in evaluations if fold(item['query']) in {fold(q) for q in n.get('queries', [])}]
    signals = item.get('research_signals', {})
    gaps = max((len(n.get('gaps', [])) for n in matched), default=signals.get('gap_importance', 1))
    tiers = [n['source_tier'] for n in matched if isinstance(n.get('source_tier'), (int, float))]
    failures = item.get('attempts', 0)
    observed_costs = [(i.get('result') or {})['http_calls'] for i in items if i.get('topic') == item.get('topic')
                      and (i.get('result') or {}).get('http_calls', 0) > 0]
    estimated_cost = signals.get('estimated_cost', sum(observed_costs) / len(observed_costs) if observed_costs else 1)
    criteria = {
        'project_utility': item['priority'],
        'unblocks': sum(i.get('status') == 'pending' and item['key'] in i.get('dependencies', []) for i in items),
        'gap_importance': gaps,
        'novelty': 1 / (1 + len(matched)),
        'source_quality': 1 / min(tiers) if tiers else signals.get('source_quality', 0),
        'uncertainty': gaps / 7,
        'cost': estimated_cost * (1 + failures),
        'duplication_risk': len(matched) / (1 + len(matched)),
    }
    rank = tuple(-criteria[k] if k not in ('cost', 'duplication_risk') else criteria[k] for k in ORDER)
    return {'policy': 'lexicographic/1', 'order': list(ORDER), 'criteria': criteria,
            'rank': rank, 'evidence_notes': [n.get('id') for n in matched],
            'cost_basis': 'observed mean HTTP attempts for topic' if observed_costs else 'neutral prior (no observation)',
            'unknown': (['source_quality'] if not tiers and 'source_quality' not in signals else []) +
                       (['cost'] if not observed_costs and 'estimated_cost' not in signals else [])}
