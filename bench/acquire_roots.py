"""Explicit bounded isolated source study; never changes repository runtime/config.

The operator provides a previous authorized runtime, including proxy policy and
persistent counters. Existing sources/robots/ledgers are copied unchanged first.
Only a new session's HTTP ceiling is reduced, never a historical counter reset.
"""
import argparse,json,shutil,hashlib,platform,subprocess
from pathlib import Path
from agent.research_roots import Roots
from agent.intelligence_evidence import documents,passages
from agent.research_session import ResearchSessions


def main():
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,default=Path.cwd());p.add_argument('--runtime',type=Path,required=True);p.add_argument('--workspace',type=Path,required=True);p.add_argument('--allow-network',action='store_true');a=p.parse_args()
 if not a.allow_network:raise PermissionError('explicit --allow-network required')
 repo=a.repository.resolve();old=a.runtime.resolve();root=a.workspace.resolve()
 if root.is_relative_to(repo) or repo.is_relative_to(root) or root.is_relative_to(old) or old.is_relative_to(root):raise ValueError('separate new workspace required')
 root.mkdir(exist_ok=False)
 for f in ('knowledge','project','config'):shutil.copytree(repo/f,root/f)
 # Preserve existing policy/host permissions. Do not invent an alternate route
 # or turn on a provider which the supplied runtime did not authorize.
 shutil.copyfile(old/'config/ocean.json',root/'config/ocean.json')
 if not json.loads((old/'config/v10.json').read_text(encoding='utf-8'))['network_enabled']:raise PermissionError('supplied runtime did not enable acquisition')
 cfg=json.loads((root/'config/v10.json').read_text(encoding='utf-8'));cfg['network_enabled']=True
 cfg['research']['max_http_calls']=min(2,cfg['research']['max_http_calls']);cfg['research']['http_per_tick']=min(2,cfg['research']['http_per_tick']);(root/'config/v10.json').write_text(json.dumps(cfg),encoding='utf-8')
 (root/'output').mkdir();shutil.copyfile(old/'output/queue.json',root/'output/queue.json')
 for f in ('sources','robots'):shutil.copytree(old/('lab/ocean/'+f),root/('lab/ocean/'+f))
 before=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))['daily'];originals=documents(root);initial={d['id'] for d in originals}
 key='forest/spruce/foliage/cards';tree=Roots(root);g=tree.prepare(key,max_depth=0,apply=True)
 if 'id' not in g:raise ValueError('no acquisition selected; do not fetch redundantly')
 result=tree.run(g['id'],True,True);after=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))['daily'];now=documents(root);new=[d for d in now if d['id'] not in initial];assessment=tree.assess(key)
 relevant={p['document_id']:p for p in assessment['sources'] if p['original']};receipts=[]
 for d in new:
  ref=relevant.get(d['id']);excerpt=d['text'][ref['start']:ref['end']] if ref else ''
  receipts.append({'url':d['url'],'document_id':d['id'],'sha256':d['sha256'],'accessed':d['accessed'],'version':d['version'],'truncated':d['truncated'],'conditions':d['conditions'],'matching_passage':ref,'excerpt':excerpt[:500],'sha_valid':hashlib.sha256(d['text'].encode()).hexdigest()==d['sha256']})
 # Reassessing/replanning the isolated micro-branch requires no more HTTP.
 again=Roots(root).plan(key,max_depth=0);check=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))['daily']
 assert check==after
 trace=[json.loads(l) for l in (root/'lab/ocean/web-trace.jsonl').read_text(encoding='utf-8').splitlines()] if (root/'lab/ocean/web-trace.jsonl').exists() else []
 s=ResearchSessions(root).get(g['id'])
 report={'schema':'vdn.roots-network-study/11.2','base_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'os':platform.system(),'branch':key,'session_id':g['id'],'state':result['state'],'acquisition_state':result.get('acquisition_state'),'limits':s['limits'],'daily_before':before,'daily_after':after,'session_http_calls':s['http_calls'],'fetch_attempts':s['fetch_attempts'],'cache_hits':sum(t['kind']=='cache_hit' for t in trace),'http_attempts':[{'url':t['url'],'purpose':t['purpose']} for t in trace if t['kind']=='http_attempt'],'errors':result.get('errors',[]),'initial_original_documents':len(originals),'new_original_documents':len(new),'new_documents_matching_branch_context':sum(d['id'] in relevant for d in new),'new_receipts':receipts,'assessment':assessment,'second_plan_no_http':True,'research_candidates_after':again['research_candidates'],'model_calls':0,'game_executed':False,'limits_of_evidence':'Actual permitted web acquisition, mechanical subject-context matching only; no independent truth, full-thread completeness, applicable Studio build or B3/C1 result inferred.'}
 (root/'study-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
