"""Measure targeted followup retention on any checkout, without network.

python bench/evaluate_v7.py --repo .
python bench/evaluate_v7.py --repo /path/to/baseline
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo.resolve()))
    from agent.recursive_gaps import propose
    from agent.planner import variants
    cases = json.loads(Path(__file__).with_name('v7_gap_cases.json').read_text(encoding='utf-8'))['cases']
    details = []
    for case in cases:
        candidates = propose(case['query'], [case['candidate']], 2)
        planned = [variants(c['query'])['terms'] for c in candidates]
        details.append({'query': case['query'], 'expected_facet': case['facet'], 'planned': planned,
                        'retained': any(case['facet'] in q.split() for q in planned)})
    print(json.dumps({'cases': len(cases), 'retained': sum(c['retained'] for c in details),
                      'fraction': sum(c['retained'] for c in details) / len(cases), 'details': details}, indent=2))


if __name__ == '__main__':
    main()
