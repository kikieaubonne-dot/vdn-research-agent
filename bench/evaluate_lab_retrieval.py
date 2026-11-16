"""Same-corpus development retrieval measures, not engine truth or Claude savings."""
import argparse,hashlib,json,math,shutil,tempfile,time
from pathlib import Path
from agent import rag,intelligence_evidence as ev
from agent.corpus import scan_notes

def evaluate(repository):
 repository=Path(repository);cases=[]
 for filename in ('rag_queries.json','rag_development_v8.json'):
  data=json.loads((repository/'bench'/filename).read_text(encoding='utf-8'));cases += [{**c,'annotation_source':filename} for c in data['queries']]
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);shutil.copytree(repository/'knowledge',root/'knowledge');rag.update_index(root)
  notes=scan_notes(root);statuses={n['id']:n.get('status') for n in notes};docs=ev.documents(root)
  rows=[]
  for c in cases:
   row={'question':c['q'],'expected_ids':c['expected'],'annotation_source':c['annotation_source'],'strategies':{}}
   for strategy in ('BM25_text','coverage','intelligence_lexical'):
    start=time.perf_counter()
    if strategy=='intelligence_lexical':selected=ev.retrieve(c['q'],docs,8);ids=list(dict.fromkeys(p['document_id'] for p in selected));mapping={d['id']:d.get('note_id') for d in docs};ids=list(dict.fromkeys(mapping[i] for i in ids if mapping.get(i)))[:5]
    else:ids=list(dict.fromkeys(p['note_id'] for p in rag.search_knowledge(c['q'],5,2000,root,ranking='balanced' if strategy=='BM25_text' else 'coverage')['results']))[:5]
    wanted=set(c['expected']);hits=sum(i in wanted for i in ids);rank=next((i for i,k in enumerate(ids,1) if k in wanted),None)
    dcg=sum(1/math.log2(i+2) for i,k in enumerate(ids) if k in wanted);ideal=sum(1/math.log2(i+2) for i in range(min(5,len(wanted))))
    row['strategies'][strategy]={'ids':ids,'precision_against_listed_labels_at_5':hits/len(ids) if ids else 0,'recall_at_5':hits/len(wanted),'reciprocal_rank':1/rank if rank else 0,'ndcg_at_5':dcg/ideal if ideal else 0,'rejected_returned':sum(statuses[i]=='rejete' for i in ids),'latency_s':time.perf_counter()-start}
   rows.append(row)
  mean={s:{m:sum(r['strategies'][s][m] for r in rows)/len(rows) for m in ('precision_against_listed_labels_at_5','recall_at_5','reciprocal_rank','ndcg_at_5','rejected_returned','latency_s')} for s in rows[0]['strategies']}
  return {'schema':'vdn.lab-retrieval-evaluation/11.2','corpus_hash':ev.digest([(n['id'],hashlib.sha256(n['_body'].encode()).hexdigest()) for n in notes]),'questions':len(rows),'active_documents':len(docs),'rejected_documents':sum(statuses.get(d.get('note_id'))=='rejete' for d in docs),'means':mean,'rows':rows,'semantic_hybrid':{'state':'NOT_RUN','reason':'no real installed embedding model selected and validated'},'HTTP_calls':0,'model_calls':0,'limitations':['existing small development labels, not blind holdout','expected IDs are not exhaustive relevance judgments; precision is against listed labels only','citation attribution and real engine benefit not measured by retrieval IDs','timings depend on warm caches; no Claude calls or quota savings measured']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=evaluate(a.root);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'questions':r['questions'],'rejected_documents':r['rejected_documents'],'means':r['means']}))
