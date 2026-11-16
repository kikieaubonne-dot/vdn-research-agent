"""Offline retrieval experiment, preserving the input corpus and benchmark.

python -m bench.evaluate_v8 --root . --output work/metrics.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import statistics
import tempfile
import time

from agent import rag


def measure(root, cases, policy):
    ranks, latencies, details = [], [], []
    for case in cases['queries']:
        start = time.perf_counter()
        response = rag.search_knowledge(case['q'], 5, 8000, root, ranking=policy)
        latencies.append((time.perf_counter() - start) * 1000)
        ids = list(dict.fromkeys(r['note_id'] for r in response['results']))
        rank = next((i + 1 for i, nid in enumerate(ids) if nid in case['expected']), None)
        ranks.append(rank)
        details.append({'q': case['q'], 'rank': rank, 'ids': ids})
    n = max(1, len(ranks))
    negative_ok = all(not {r['note_id'] for r in rag.search_knowledge(c['q'], 5, 1500, root, ranking=policy)['results']}
                      .intersection(c['must_not_return']) for c in cases.get('negatives', []))
    return {'queries': len(ranks), **{f'hit_at_{k}': sum(r is not None and r <= k for r in ranks) / n for k in (1, 3, 5)},
            'mrr': sum(1/r if r else 0 for r in ranks)/n, 'latency_median_ms': statistics.median(latencies),
            'latency_p95_ms': sorted(latencies)[min(len(latencies)-1, int(len(latencies)*.95))],
            'negatives_clean': negative_ok, 'details': details}


def evaluate(source):
    source = Path(source)
    manifest = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((source/'knowledge').rglob('*')) if p.is_file()}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name in ('knowledge','config','bench'):
            shutil.copytree(source/name, root/name)
        start=time.perf_counter();index=rag.update_index(root);cold=(time.perf_counter()-start)*1000
        start=time.perf_counter();incremental=rag.update_index(root);warm=(time.perf_counter()-start)*1000
        result={'schema':'vdn.rag-experiment/8', 'corpus':manifest,'index':index,'index_cold_ms':cold,
                'index_incremental_ms':warm,'incremental':incremental,'policies':{}}
        for name in ('legacy','balanced','coverage','coverage_prior'):
            result['policies'][name]={}
            for split, filename in (('development','rag_development_v8.json'),('historical','rag_queries.json')):
                cases=json.loads((root/'bench'/filename).read_text(encoding='utf-8'))
                result['policies'][name][split]=measure(root,cases,name)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=evaluate(args.root)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name, splits in result['policies'].items():
        print(name,{split:{k:v for k,v in r.items() if k!='details'} for split,r in splits.items()})


if __name__=='__main__':
    main()
