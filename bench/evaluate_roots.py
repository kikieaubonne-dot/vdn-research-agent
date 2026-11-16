"""Frozen source-subject retrieval comparison; not engine truth or blind evaluation."""
import argparse,json,math,shutil,tempfile,time,hashlib
from pathlib import Path
from agent import rag
from agent.research_roots import Roots
from agent.research_library import Library
from agent.corpus import scan_notes
from agent.intelligence_evidence import digest


def metrics(ids,wanted,elapsed):
 wanted=set(wanted);hits=sum(i in wanted for i in ids);rank=next((i for i,k in enumerate(ids,1) if k in wanted),None)
 ideal=sum(1/math.log2(i+2) for i in range(min(5,len(wanted))))
 return {'ids':ids,'recall_at_5':hits/len(wanted),'precision_against_listed_labels_at_5':hits/5,'reciprocal_rank':1/rank if rank else 0,'ndcg_at_5':sum(1/math.log2(i+2) for i,k in enumerate(ids) if k in wanted)/ideal,'coverage':int(hits>0),'empty':int(not ids),'duplicates':len(ids)-len(set(ids)),'latency_s':elapsed}


def evaluate(repository):
 repository=Path(repository);cases=json.loads((repository/'bench/roots_evaluation.json').read_text(encoding='utf-8'))
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp)
  for f in ('knowledge','project','config'):shutil.copytree(repository/f,root/f)
  rag.update_index(root);tree=Roots(root);lib=Library(root);lib.engine._ensure_index();rows=[]
  for c in cases['cases']:
   row={**c,'strategies':{}}
   start=time.perf_counter();ids=list(dict.fromkeys(h['note_id'] for h in rag.search_knowledge(c['question'],5,8000,root)['results']))[:5]
   row['strategies']['existing_coverage']=metrics(ids,c['expected'],time.perf_counter()-start)
   for strategy,oracle in (('inferred_branch_fusion',False),('explicit_branch_fusion',True)):
    start=time.perf_counter()
    try:key=c['branch'] if oracle else tree.resolve(c['question'])
    except ValueError:key=None
    result=lib.search(c['question'],tree.nodes[key] if key else None);ids=[h['note_id'] for h in result['results']]
    row['strategies'][strategy]={**metrics(ids,c['expected'],time.perf_counter()-start),'branch_used':key,'attributed_references':len(set(u for h in result['results'] for u in h['sources'])),'duplicate_groups':result['duplicate_groups']}
   rows.append(row)
  means={s:{m:sum(r['strategies'][s][m] for r in rows)/len(rows) for m in ('recall_at_5','precision_against_listed_labels_at_5','reciprocal_rank','ndcg_at_5','coverage','empty','duplicates','latency_s')} for s in rows[0]['strategies']}
  regressions={s:[r['id'] for r in rows if r['strategies'][s]['recall_at_5']<r['strategies']['existing_coverage']['recall_at_5'] or r['strategies'][s]['reciprocal_rank']<r['strategies']['existing_coverage']['reciprocal_rank']] for s in ('inferred_branch_fusion','explicit_branch_fusion')}
  return {'schema':'vdn.roots-retrieval/11.2','base_sha':'ad2fc6b6e211ccb686052273221cb35f26e30bf6','corpus_hash':digest([(n['id'],hashlib.sha256(n['_body'].encode()).hexdigest()) for n in scan_notes(root)]),'annotation_hash':digest(cases),'annotation_provenance':cases['provenance'],'questions':len(rows),'means':means,'regressions':regressions,'rows':rows,'network_calls':0,'model_calls':0,'semantic':'NOT_RUN; no real embedding backend','limits':['Small authored source-subject labels; incomplete relevance judgments; not blind engine ground truth.','Explicit-branch results assume user-provided branch and must not be conflated with inferred routing.','No statistical significance, semantic entailment, Claude quota reduction or engine technique validation demonstrated.','Latency includes Python facade/index checks; CPU, cache and corpus dependent.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=evaluate(a.root);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'questions':r['questions'],'means':r['means'],'regressions':r['regressions']}))
