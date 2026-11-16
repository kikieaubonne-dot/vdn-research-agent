"""Annotated synthetic contracts and same-corpus V11/V11.1 evaluation.

Fixtures define test semantics, not Roblox truth. Actual LLM runs require an
explicit exact installed model and consume the unchanged shared daily budget.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time
import tracemalloc
from agent import intelligence_evidence as ev,intelligence_models as im,ocean_knowledge,ocean_plan,ocean_semantic,intelligence_semantic
from agent.intelligence import Intelligence,prompt_for,validate_model

DATA=Path(__file__).with_name('intelligence_cases.json')


def corpus():
    data=json.loads(DATA.read_text(encoding='utf-8'));out=[]
    for original in data['documents']:
        d={'url':'https://fixtures.invalid/'+original['id'],'source_type':'AUTHORED_FIXTURE','independent':True,
           'published':None,'accessed':None,'retrieved_at':time.time(),'truncated':False,'conditions':{},**original}
        d['sha256']=hashlib.sha256(d['text'].encode('utf-8')).hexdigest();out.append(d)
    return data,out


def contract(case,docs,root):
    if case['task']=='intent':return {'problems':ev.analyze(case['question'])['problems']}
    if case['task']=='claim':
        d=copy.deepcopy(next(d for d in docs if d['id']==case['document']));ps=ev.passages([d]);c=case['claim']
        p=next((p for p in ps if c['text'] in p['text']),next(p for p in ps if not p['text'].startswith('#')))
        if case['mutation']=='secondary':p['independent']=False
        if case['mutation']=='offset':p['start']+=1
        if case['mutation']=='hash':p['document_sha256']='0'*64
        if case['mutation']=='incomplete':p['incomplete_context']=True
        chosen=[p];ids=['missing'] if case['mutation']=='missing' else [p['id']]
        return {'support':ev.verify({**c,'passage_ids':ids},chosen,[d],ev.analyze(case['question']))['support']}
    if case['task']=='contradiction':
        cs=ev.contradictions(ev.passages([d for d in docs if d['id'] in case['documents']]))
        return {'status':cs[0]['status'] if cs else None}
    r=Intelligence(root).run(case['question'],documents=docs);return {'abstained':r['abstained']}


def retrieval_metrics(ids,relevant):
    selected=ids[:5];wanted=set(relevant)
    return {'precision_at_5':sum(i in wanted for i in selected)/len(selected) if selected else 0,
            'document_recall_at_5':len(set(selected)&wanted)/len(wanted) if wanted else None,
            'relevant_documents':relevant,'retrieved_documents':selected}


def evaluate(root,models=(),allow_model=False,max_cases=8,with_embeddings=False):
    data,docs=corpus();details=[];tracemalloc.start();start=time.perf_counter()
    for case in data['cases']:
        actual=contract(case,docs,root);details.append({'id':case['id'],'category':case['category'],'expected':case['expected'],'actual':actual,'pass':actual==case['expected']})
    questions=data['model_tasks'][:max_cases];comparison=[];cfg=im.settings(root)
    for case in questions:
        q=case['question'];t=time.perf_counter();before=[]
        facet=ocean_plan.facet_for(q)[0]
        # V11's existing deterministic synthesis on the identical source corpus.
        for d in docs:
            if not ocean_knowledge.excerpts(d,ocean_plan.facet_for(q)[1]):continue
            adapted={**d,'provider':'AUTHORED_FIXTURE','text_sha256':d['sha256'],'raw_text_sha256':d['sha256'],'policy':'authored fixture only'}
            try:before.append((d['id'],ocean_knowledge.synthesis(q,facet,[adapted])))
            except ValueError:pass
        a={'mode':'A_V11_deterministic','elapsed_s':time.perf_counter()-t,'candidate_count':len(before),
           'claim_registry':False,'source_span_offsets':False,'unverified':True,
           'retrieval':retrieval_metrics([doc_id for doc_id,_ in before],case['relevant_documents'])}
        b=Intelligence(root).run(q,documents=docs)
        comparison.append({'id':case['id'],'question':q,'A':a,'B_deterministic':{'elapsed_s':b['metrics']['elapsed_s'],
            'intent_problems':b['intent']['problems'],'facts':len(b['facts']),'unsupported':b['metrics']['unsupported_claims'],
            'claim_registry':True,'source_span_offsets':True,'abstained':b['abstained'],'structural_protocols':len(b['experiments']),
            'retrieval':retrieval_metrics([p['document_id'] for p in b['passages']],case['relevant_documents']),
            'raw_claim_registry':b['claims'],'model_calls':0,'api_cost_usd':0,
            'human_usefulness':'not reviewed'},'B_local':[],'C_hybrid':{'state':'not_run','reason':'requires explicitly configured real embeddings and indexed same corpus'}})
        if allow_model and models:
            if not cfg['enabled']:raise ValueError('enable intelligence explicitly before model benchmarking')
            for name in models:
                result={'name':name,'state':'unavailable','fixture_inputs':True}
                def work():
                    client=im.Ollama(cfg);installed=client.inventory();selected=next((m for m in installed if m['name']==name),None)
                    if not selected:raise ValueError('exact model not installed')
                    prompt,seen=prompt_for(b['intent'],b['passages'],cfg)
                    if not seen:raise ValueError('insufficient context')
                    im.reserve_model(root);payload,metrics=client.generate(selected,prompt)
                    reviewed=validate_model(payload,seen,docs,b['intent'])
                    return {'name':name,'state':'executed_real_model','fixture_inputs':True,'metrics':metrics,'raw_output':payload,
                            'reviewed':reviewed,'json_valid':True,'unsupported_claims':sum(c['support']=='UNSUPPORTED' for c in reviewed['claims'])}
                try:result=im.operation(root,work)
                except (OSError,ValueError,RuntimeError) as exc:
                    result['error_kind']=type(exc).__name__
                    if hasattr(exc,'details'):result['stop_details']=exc.details()
                comparison[-1]['B_local'].append(result)
    if with_embeddings:
        def embed_work():
            model=intelligence_semantic.identity(root)
            ps=[p for p in ev.passages(docs) if not p['hostile']][:64]
            vectors=ocean_semantic.vectors(root,[p['text'] for p in ps]);queries=ocean_semantic.vectors(root,[c['question'] for c in questions])
            import math
            results=[]
            for case,qv,row in zip(questions,queries,comparison):
                def cosine(v):
                    denominator=math.sqrt(sum(x*x for x in v))*math.sqrt(sum(x*x for x in qv))
                    return sum(a*b for a,b in zip(v,qv))/denominator if denominator else -1
                ranked=sorted(range(len(ps)),key=lambda i:-cosine(vectors[i]));scores={}
                lex=ev.retrieve(case['question'],docs,8);by_id={p['id']:p for p in ps}
                for ids in ([p['id'] for p in lex],[ps[i]['id'] for i in ranked]):
                    for rank,key in enumerate(ids,1):scores[key]=scores.get(key,0)+1/(60+rank)
                fused=sorted(scores,key=lambda k:-scores[k])
                results.append({'model':model,'semantic_only':retrieval_metrics([ps[i]['document_id'] for i in ranked],case['relevant_documents']),
                    'hybrid':retrieval_metrics([by_id[k]['document_id'] for k in fused if k in by_id],case['relevant_documents']),
                    'state':'real_local_embeddings_on_authored_fixtures','end_to_end_model_synthesis':'not_run; this measures retrieval only'})
            return results
        if not allow_model:raise ValueError('embedding benchmark requires explicit --allow-model')
        try:
            for row,result in zip(comparison,im.operation(root,embed_work)):row['C_hybrid']=result
        except (ValueError,OSError,RuntimeError,KeyError) as exc:
            for row in comparison:row['C_hybrid']={'state':'unavailable','error_kind':type(exc).__name__}
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    claim_results=[r for r in details if any(c['id']==r['id'] and c['task']=='claim' for c in data['cases'])]
    return {'schema':'vdn.intelligence-evaluation-results/11.1','provenance':data['provenance'],'pipeline_version':ev.VERSION,
            'cases':len(details),'passed':sum(d['pass'] for d in details),'failed':[d['id'] for d in details if not d['pass']],
            'claim_support_contract_accuracy':sum(d['pass'] for d in claim_results)/len(claim_results),
            'elapsed_s':time.perf_counter()-start,'python_tracemalloc_peak_bytes':peak,'vram':'not measured',
            'details':details,'same_corpus_comparison':comparison,'real_models_requested':list(models),
            'human_review':'not performed; structural completeness is not correctness or usefulness',
            'recommend_default_model':None,'limitations':['development fixtures, not blind holdout or real engine truth',
                'no semantic entailment proof','no gain inferred from structural fields','existing per-day model and HTTP quotas remain in force']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True)
    p.add_argument('--models',nargs='*',default=[]);p.add_argument('--allow-model',action='store_true');p.add_argument('--max-cases',type=int,default=8);p.add_argument('--with-embeddings',action='store_true')
    a=p.parse_args()
    if a.models and not a.allow_model:p.error('--models requires explicit --allow-model')
    if not 1<=a.max_cases<=12:p.error('--max-cases must be 1..12')
    r=evaluate(a.root,a.models,a.allow_model,a.max_cases,a.with_embeddings);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:r[k] for k in ('cases','passed','failed','claim_support_contract_accuracy','recommend_default_model')},ensure_ascii=False));return 0 if not r['failed'] else 1


if __name__=='__main__':raise SystemExit(main())
