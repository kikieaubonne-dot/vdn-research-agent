"""Seven task handoffs, same corpus, exact V11.1 checkout versus project mode.

This measures explicit structural criteria, not Claude's coding performance,
semantic truth or quota savings. No model or Internet call is requested.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tracemalloc
from agent.project_work import Project

CASES=[('collisions','Corriger les collisions des sapins Roblox'),
       ('lighting','Améliorer la lampe torche Roblox'),
       ('performance','Optimiser les performances de la forêt Roblox'),
       ('materials','Corriger la texture du sapin Roblox'),
       ('animation','Préparer une animation Roblox'),
       ('interactions','Créer une interaction de porte Roblox'),
       ('export','Résoudre un problème d’export Blender 5.2 vers Roblox')]


def evaluate(root,baseline,token_budget=1800):
    root=Path(root).resolve();baseline=Path(baseline).resolve();project=Project(root);rows=[]
    tracemalloc.start()
    for expected,question in CASES:
        env=dict(os.environ);env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
        start=time.perf_counter()
        r=subprocess.run([sys.executable,'-m','agent.v111','--root',str(root),'brief',question,'--token-budget',str(token_budget)],
                         cwd=baseline,env=env,text=True,capture_output=True,timeout=30)
        elapsed=time.perf_counter()-start
        if r.returncode:raise ValueError('baseline failed; preserve stderr privately and do not claim comparison success')
        old=json.loads(r.stdout);start=time.perf_counter();new=project.brief(question,token_budget);current_elapsed=time.perf_counter()-start
        handoff=new.get('project',{});card=project.latest(expected) or project.synthesize(expected)
        def size(value):return len(json.dumps(value,ensure_ascii=False))
        def known_fields(value):
            s=json.dumps(value,ensure_ascii=False).lower()
            return {'game_named':'voisin de noël' in s,'target_engine':'roblox' in s,
                    'unknown_device_explicit':'unknown' in s or 'appareil' in s,
                    'rollback_present':'rollback' in s or 'restaurer' in s,
                    'test_protocol_present':bool(value.get('experiments') or value.get('tests')),
                    'steps_with_components':bool(value.get('implementation'))}
        rows.append({'task':expected,'question':question,'expected_task_annotation':expected,
            'A_V111':{'elapsed_with_process_startup_s':elapsed,'characters':size(old),'estimated_tokens':round(size(old)/3.6,1),
                      'criteria':known_fields(old),'raw_brief':old},
            'B_project':{'elapsed_in_process_s':current_elapsed,'characters':size(new),'estimated_tokens':round(size(new)/3.6,1),
                         'criteria':known_fields(handoff),'matched_task':handoff.get('task_id'),
                         'correct_task':handoff.get('task_id')==expected,'raw_brief':new},
            'source_attribution':{'scope':'mechanical capture metadata, not truth or platform validation',
                'source_count':len(card['sources']),'all_source_urls_present':all(s.get('url','').startswith('https://') for s in card['sources']),
                'live_link_check':'not performed by benchmark'},
            'readiness':card.get('current_readiness',card['quality']['readiness']),
            'human_usefulness_review':'not performed'})
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    return {'schema':'vdn.project-evaluation/11.2','cases':len(rows),'baseline_commit':'d23aafa6a190ff69d951730dd39566ed3e33f7a0',
        'same_corpus':True,'bible_hash':project.bible.fingerprint,'task_identity_correct':sum(r['B_project']['correct_task'] for r in rows),
        'context_budget':token_budget,'python_tracemalloc_peak_bytes':peak,'model_calls':0,'HTTP_calls':0,'api_cost_usd':0,
        'rows':rows,'limitations':['structural criteria and explicit task identity only; not blind semantic annotation',
            'baseline timing includes interpreter startup; project timing does not, so no speed gain inferred',
            'no Claude invocation or quota savings measured','sources captured from real pages must be distinguished from fixture tests',
            'no engine experiment or visual comparison performed']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--private-output',type=Path)
    a=p.parse_args();r=evaluate(a.root,a.baseline);a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.private_output:
        a.private_output.parent.mkdir(parents=True,exist_ok=True);a.private_output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    public=copy.deepcopy(r);public['publication_scope']='Source quotations redacted; metrics computed on full outputs. Original documents and raw outputs remain private.'
    for row in public['rows']:
        for mode in ('A_V111','B_project'):
            for field in ('facts','inferences'):
                for claim in row[mode]['raw_brief'].get(field,[]):
                    if 'text' in claim:claim['text_sha256']=hashlib.sha256(claim['text'].encode()).hexdigest();claim['text']='[source excerpt withheld; consult source and detailed analysis]'
    a.output.write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':r['cases'],'correct_task_identity':r['task_identity_correct'],'model_calls':0,'HTTP_calls':0}))


if __name__=='__main__':main()
