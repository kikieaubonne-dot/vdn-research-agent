"""Frozen holdout protocol. --code-root can point at a clean V8 checkout.

The same questions, API budgets and corpus are used for both versions. No rules
are tuned by this evaluator; citation identity is not semantic correctness.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd())
    p.add_argument('--code-root',type=Path);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.code_root:sys.path.insert(0,str(args.code_root.resolve()))
    from agent.engine import KnowledgeEngine
    from agent.providers import canonical_url
    from agent import rag
    cases=json.loads((args.root/'bench'/'v9_holdout.json').read_text(encoding='utf-8'))['cases']
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for folder in ('knowledge','config'):shutil.copytree(args.root/folder,root/folder)
        t=time.perf_counter();index=rag.update_index(root);index_ms=(time.perf_counter()-t)*1000
        engine=KnowledgeEngine(root);details=[];ranks=[];latencies=[];abstentions=[];citations=0;total=0
        for case in cases:
            start=time.perf_counter();found=engine.search_knowledge(case['q'],5,5000)
            latencies.append((time.perf_counter()-start)*1000)
            expected=set(case.get('expected_ids',[]));urls={canonical_url(u) for u in case.get('expected_sources',[])}
            rank=next((i+1 for i,h in enumerate(found['results']) if h['id'] in expected or
                       urls & {canonical_url(u) for u in h['sources']}),None)
            if expected or urls:ranks.append(rank)
            for hit in found['results']:
                source=engine.get_knowledge(hit['id'])
                total+=len(hit['sources']);citations+=sum(u in source['sources'] for u in hit['sources'])
            brief=engine.get_task_brief(case['q'],token_budget=1800) if hasattr(engine,'get_task_brief') else None
            abstained=brief['abstained'] if brief else not found['results']
            if case.get('expect_abstention'):abstentions.append(abstained)
            all_expected=[h['id'] for h in found['results'] if h['id'] in expected]
            details.append({'category':case['category'],'q':case['q'],'rank':rank,'ids':[h['id'] for h in found['results']],
                            'abstained':abstained,'all_desired_sources_found':set(all_expected)>=expected if case.get('all_sources_desired') else None,
                            'brief_tokens_approx':len(json.dumps(brief,ensure_ascii=False))/3.6 if brief else None,
                            'version_uncertain':brief.get('version_status') if brief else 'not exposed by V8',
                            'truth_verified':brief.get('truth_verified') if brief else False})
        n=max(1,len(ranks));result={'schema':'vdn.holdout/9','implementation':str(args.code_root or 'V9 working tree'),
            'cases':len(cases),'retrieval_cases':len(ranks),**{f'hit_at_{k}':sum(r is not None and r<=k for r in ranks)/n for k in (1,3,5)},
            'mrr':sum(1/r if r else 0 for r in ranks)/n,'citation_identity_accuracy':citations/max(1,total),
            'citation_semantic_truth':'not measured','outside_abstention':sum(abstentions)/max(1,len(abstentions)),
            'abstention_protocol':'explicit briefing' if hasattr(engine,'get_task_brief') else 'empty-result proxy; V8 has no explicit abstention tool',
            'index_ms':index_ms,'latency_median_ms':sorted(latencies)[len(latencies)//2],
            'index_notes':index['notes'],'details':details}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
