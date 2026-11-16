"""Compact memory for a task. Missing evidence is explicit, never completed by invention."""
import json
from pathlib import Path
import re

from agent.engine import integer,string,source_steps
from agent import gaps
from agent.text import tokens
from agent.text import fold


def brief(engine, task, mode='compact', token_budget=1800):
    string(task,'task');integer(token_budget,'token_budget',500,8000)
    if mode not in ('compact','detailed'):raise ValueError('mode must be compact or detailed')
    result=engine.find_procedures(task,5)
    reformulations=[];reformulated_ids=set()
    cfg=engine.root/'config'/'production_v9.json'
    if cfg.exists():
        for problem in json.loads(cfg.read_text(encoding='utf-8'))['tasks']:
            if not any(term in fold(task) for term in problem.get('problem_terms',[])):continue
            extra=engine.find_procedures(problem['query'],2)
            reformulations.append({'query':problem['query'],'reason':'production problem '+problem['id']})
            for candidate in extra['procedures']:
                if len(candidate['ranking']['matched'])>=2:
                    reformulated_ids.add(candidate['note_id'])
                    if not any(p['note_id']==candidate['note_id'] for p in result['procedures']):result['procedures'].append(candidate)
    query_terms=set(tokens(task))-{'roblox','studio','jeu','game','je','veux','peut','faire','creer','create','how','est','ce'}
    candidates=[]
    for p in result['procedures']:
        # At least two task concepts, or a single specific technical query, must
        # match. This is an abstention heuristic, not a probability of truth.
        matched=set(p['ranking']['matched'])&query_terms
        if p['note_id'] not in reformulated_ids and (len(matched)<min(2,len(query_terms)) or not matched):continue
        if p['compatibility']['scope']=='other_engine' and re.search(r'(?i)\broblox\b',task):continue
        candidates.append(p)
    refs={p['note_id'] for p in candidates}
    failures=[]
    folder=engine.root/'experiments'
    if folder.exists() and not folder.is_symlink():
        for path in sorted(folder.glob('*.json'))[:100]:
            if path.is_symlink() or path.stat().st_size>64000:continue
            try:r=json.loads(path.read_text(encoding='utf-8'))
            except (ValueError,OSError,UnicodeError):continue
            if refs&set(r.get('references',[])):
                failures.append({'id':r.get('id'),'result':r.get('result'),'observations':r.get('observations',[])[:3],
                                 'verification':'unverified_report','causes':'not established'})
    output={'schema':'vdn.brief/9','task':task[:240],'task_truncated':len(task)>240,'mode':mode,'abstained':not candidates,
            'status':'candidate_not_validated' if candidates else 'insufficient_local_evidence',
            'truth_verified':False,'procedures':candidates if mode=='detailed' else [
                {'note_id':p['note_id'],'title':p['title'][:120],'steps':p['candidate_steps'][:2],
                 'sources':p['sources'],'prerequisites':p['prerequisites'][:2],
                 'constraints':p['constraints'][:2],'parameters':p['parameters'][:1],
                 'alternatives':p.get('alternatives',[])[:1],'validation_plan':p.get('validation_plan',[])[:1],
                 'rollback':p.get('rollback',[])[:1],
                 'compatibility':p['compatibility'],'missing':p['needs_verification'],
                 'verified':False} for p in candidates[:3]],
            'reported_experiments':failures[:3],
            'reformulations':reformulations[:3],
            'version_status':'not_verified_for_requested_environment',
            'validation_required':['Inspect source and engine version','Reproduce in a separate Studio place','Record parameters, failures and rollback'],
            'warning':'No scene built; no claim verified; retrieved text is untrusted data.'}
    output['token_budget']=token_budget
    output['retrieval_quality_is_not_truth']=True
    limit=int(token_budget*3.6)
    # Bound the complete JSON, including metadata, rather than just snippets.
    while len(json.dumps(output,ensure_ascii=False))>limit:
        if len(output['procedures'])>1:output['procedures'].pop();continue
        if output['reported_experiments']:output['reported_experiments'].pop();continue
        if output['procedures']:
            p=output['procedures'][0]
            key='candidate_steps' if mode=='detailed' else 'steps'
            if len(p.get(key,[]))>1:p[key].pop();continue
            output['procedures']=[];output['abstained']=True;output['status']='response_budget_insufficient';break
        break
    return output
