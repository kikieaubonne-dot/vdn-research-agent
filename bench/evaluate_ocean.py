"""Same corpus V10 facade vs V11 concepts, plus mechanical candidate rubric.

No network, model or new game performance measurement. This is development data.
"""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
import time
import tracemalloc
from agent.engine import KnowledgeEngine
from agent.ocean_api import OceanAPI
from agent import ocean_knowledge


def evaluate(source):
    source=Path(source).resolve();cases=json.loads((source/'bench/ocean_queries.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        for folder in ('knowledge','config'):shutil.copytree(source/folder,root/folder)
        old=KnowledgeEngine(root);new=OceanAPI(root);cards=ocean_knowledge.cards(root)
        targets={c['id'] for c in cards if c['facet']=='collision'}
        if not targets:raise ValueError('evaluation requires a collision candidate; prepare a grounded fixture or use the delivered live candidate')
        details=[];ranks={'V10':[],'V11':[]};outside=[];timings={'V10':[],'V11':[]}
        tracemalloc.start()
        for case in cases['cases']:
            start=time.perf_counter();a=old.search_knowledge(case['q'],5,3000);timings['V10'].append(time.perf_counter()-start)
            start=time.perf_counter();b=new.search_ocean(case['q'],5);brief=new.get_ocean_brief(case['q'],1000);timings['V11'].append(time.perf_counter()-start)
            ids={'V10':[h['id'] for h in a['results']],'V11':[h['id'] for h in b['results']]}
            r={name:next((i+1 for i,k in enumerate(values) if k in targets),None) for name,values in ids.items()}
            if case.get('expect_collision'):
                for name in ranks:ranks[name].append(r[name])
            if case.get('expect_abstention'):outside.append(brief['abstained'])
            details.append({**case,'ranks':r,'ids':ids,'ocean_brief_abstained':brief['abstained'],'truth_verified':brief['truth_verified'],
                            'version_constraints_exposed':bool(brief['candidates'] and brief['candidates'][0]['uncertainties'])})
        peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
        measurements={}
        for name,values in ranks.items():
            measurements[name]={'retrieval_cases':len(values),'hit_at_3':sum(r is not None and r<=3 for r in values)/len(values),
                                'mrr':sum(1/r if r else 0 for r in values)/len(values),
                                'mean_elapsed_s':sum(timings[name])/len(timings[name])}
        rubric=[]
        for c in cards:
            rubric.append({'id':c['id'],'literal_claims':len(c['claims']),'source_urls':len(c['sources']),
                           'proposed_steps':len(c['procedure']),'project_context_present':bool(c['context']),
                           'validation_protocol_items':len(c['validation']),'unknowns_explicit':bool(c['uncertainties']),
                           'human_usefulness_review':'not performed','truth_verified':False})
        return {'schema':'vdn.ocean-evaluation/11','protocol':cases['protocol'],'same_corpus':True,
                'source_markdown_count':len(list((root/'knowledge').rglob('*.md'))),'measurements':measurements,
                'outside_brief_abstention':sum(outside)/len(outside),'structural_rubric':rubric,'details':details,
                'python_tracemalloc_peak_bytes':peak,'vram_peak':'not measured','model_calls':0,'http_calls':0,
                'api_spend_usd':0,'semantic_embedding_quality':'not tested with a real model',
                'caveat':'Small development set and reference-identity relevance. Timing includes different APIs; no speed, truth or productivity gain inferred.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=evaluate(a.root);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('details','structural_rubric')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
