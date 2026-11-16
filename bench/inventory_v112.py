"""Read-only, typed continuity inventory; no network or model calls."""
import argparse,ast,collections,hashlib,json,re,subprocess
from pathlib import Path
from agent.corpus import scan_notes
from agent.intelligence_evidence import documents,passages
from agent.mcp_v8 import Server

def run(root,runtime=None):
 root=Path(root).resolve();notes=scan_notes(root);byid=collections.defaultdict(list)
 for n in notes:byid[n['id']].append(n.get('_path',n.get('path','UNKNOWN')))
 registry=json.loads((root/'output/registry.json').read_text(encoding='utf-8'));bib=json.loads((root/'project/bible.json').read_text(encoding='utf-8'));prepared=json.loads((root/'project/prepared.json').read_text(encoding='utf-8'))
 docs=documents(root);ps=passages(docs);tools=Server(root,v112=True).tools
 tools=tools if isinstance(tools,list) else list(tools.values())
 modules=[]
 for p in sorted((root/'agent').glob('*.py')):
  tree=ast.parse(p.read_text(encoding='utf-8-sig'))
  modules.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'responsibility':ast.get_docstring(tree),'definitions':[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))],
   'imports':sorted({n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names})})
 missing=[];registry_ids=[]
 for url,r in registry['urls'].items():
  registry_ids.append(r['id']);p=root/r['path']
  if not p.is_file() or r['id'] not in byid:missing.append({'kind':'registry_note','id':r['id'],'path':r['path'],'missing_path':not p.is_file(),'missing_note_id':r['id'] not in byid})
 refs=['main','codex/autonomy-v7','codex/knowledge-engine-v8','codex/knowledge-factory-v9','codex/research-lab-v10','codex/eponge-ocean-v11','d23aafa','72f1b9c']
 history=[];last=None
 for ref in refs:
  resolved=None
  for candidate in (ref,'origin/'+ref):
   check=subprocess.run(['git','rev-parse','--verify',candidate],cwd=root,text=True,capture_output=True)
   if check.returncode==0:resolved=candidate;sha=check.stdout.strip();break
  if resolved is None:
   history.append({'ref':ref,'state':'not_available_in_local_git_refs'});continue
  files=subprocess.check_output(['git','ls-tree','-r','--name-only',resolved,'knowledge'],cwd=root,text=True).splitlines();md=[f for f in files if f.endswith('.md')]
  found=subprocess.run(['git','grep','-h','-E','^id:',resolved,'--','knowledge'],cwd=root,text=True,capture_output=True)
  ids=[s.split(':',1)[1].strip().strip('"\'') for s in found.stdout.splitlines()];unique=set(ids)
  history.append({'ref':ref,'sha':sha,'markdown':len(md),'id_occurrences':len(ids),'unique_note_ids':len(unique),'duplicate_ids':[k for k,v in collections.Counter(ids).items() if v>1],
   'added_vs_previous_listed_ref':sorted(unique-last) if last is not None else None,'removed_vs_previous_listed_ref':sorted(last-unique) if last is not None else None});last=unique
 links=[];allnames={p.stem for p in (root/'knowledge').rglob('*.md')}
 for p in (root/'knowledge').rglob('*.md'):
  for target in re.findall(r'\[\[([^\]]+)\]\]',p.read_text(encoding='utf-8-sig')):
   name=target.split('|')[0].split('#')[0]
   if name and Path(name).stem not in allnames:links.append({'from':p.relative_to(root).as_posix(),'target':name,'kind':'unresolved_wikilink_in_repository_scope'})
 categories={}
 def cat(name,ids,scope,duplicates=False):
  ids=list(ids);c=collections.Counter(ids);categories[name]={'unique':len(c),'occurrences':len(ids),'ids':sorted(c),'scope':scope,'repeated_ids':{k:v for k,v in c.items() if v>1},'repetition_is_corruption':duplicates}
 cat('knowledge_note',byid,'definitions in admitted Markdown notes',True)
 cat('registry_note_reference',registry_ids,'references, not additional notes')
 cat('registry_content_fingerprint',registry['fingerprints'],'historical fingerprints, not source documents')
 cat('source_url_in_notes',(u for n in notes for u in n.get('sources',[])),'URL references; not visited or independent sources')
 cat('secondary_document',(d['id'] for d in docs if not d['independent']),'derived quotations admitted for retrieval; never primary sources')
 cat('secondary_passage',(p['id'] for p in ps if not p['independent']),'derived local passages')
 cat('original_snapshot_document',(d['id'] for d in docs if d['independent']),'original receipts present in repository runtime')
 for name in ('items','questions','tasks','visual_references','deferred','groups'):cat('bible_'+name,(i['id'] for i in bib[name]),'Bible namespace '+name)
 cat('prepared_card',(i['key'] for i in prepared['cards']),'secondary published preparations')
 cat('prepared_analysis_reference',(i['card']['analysis_key'] for i in prepared['cards']),'private analysis references; not shipped primary evidence')
 cat('prepared_document_reference',(s['document_id'] for i in prepared['cards'] for s in i['card']['sources']),'metadata references only')
 cat('prepared_passage_reference',(s['id'] for i in prepared['cards'] for s in i['card']['sources']),'metadata references only')
 cat('prepared_claim_reference',(c['id'] for i in prepared['cards'] for c in i['card']['quality']['facts']),'archived attribution metadata, not current facts')
 cat('mcp_tool',(t['name'] for t in tools),'V11.2 tool definitions')
 queue=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))
 cat('queue_item',queue['items'],'persistent global research queue; not session IDs')
 cat('v5_seen_source',json.loads((root/'output/state.json').read_text())['seen'],'legacy seen registry')
 # Enumerate every scalar ID/key in JSON/JSONL, preserving its file + pointer.
 # Generic occurrences are not promoted to definitions or summed with typed IDs.
 occurrences=[];errors=[]
 def walk(v,pointer,path):
  if isinstance(v,dict):
   for k,x in v.items():
    at=pointer+'/'+str(k)
    if isinstance(x,str) and (k in ('id','key','fingerprint','session_id','experiment_id','run_id','note_id','document_id','analysis_key','task_id','parent') or k.endswith('_id')):occurrences.append({'file':path,'pointer':at,'field':k,'value':x})
    walk(x,at,path)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,pointer+'/'+str(i),path)
 for folder in ('config','output','project','lab','tests/fixtures','bench','docs'):
  for p in sorted((root/folder).rglob('*')) if (root/folder).exists() else []:
   if p.is_symlink() or not p.is_file() or p.suffix not in ('.json','.jsonl') or p.is_relative_to(root/'docs/v112/continuity'):continue
   if p.stat().st_size>2_000_000:errors.append({'path':p.relative_to(root).as_posix(),'error':'oversized; not scanned'});continue
   try:
    text=p.read_text(encoding='utf-8-sig');v=json.loads(text) if p.suffix=='.json' else [json.loads(l) for l in text.splitlines() if l.strip()];walk(v,'',p.relative_to(root).as_posix())
   except (ValueError,OSError) as e:errors.append({'path':p.relative_to(root).as_posix(),'error':type(e).__name__})
 runtime_counts={}
 for scope,base in [('repository',root)]+([('previous_isolated_lab',Path(runtime).resolve())] if runtime else []):
  from agent.lab_store import LabStore
  d=documents(base);records=[]
  exp=base/'lab/experiments'
  if exp.exists():records=[LabStore(base).get(p.name) for p in exp.iterdir() if p.is_dir() and not p.is_symlink()]
  sessions=[]
  for p in sorted((base/'lab/research').glob('*/session.json')) if (base/'lab/research').exists() else []:sessions.append(json.loads(p.read_text())['id'])
  # ResearchSessions stores one directory per UUID; locate real files explicitly.
  for p in sorted((base/'lab/research').glob('*/state.json')) if (base/'lab/research').exists() else []:
   value=json.loads(p.read_text());sessions.append(value['id'])
  direct=[]
  for p in (base/'lab/research').glob('*.json') if (base/'lab/research').exists() else []:
   v=json.loads(p.read_text());
   if 'id' in v:direct.append(v['id'])
  runtime_counts[scope]={'original_documents':len([x for x in d if x['independent']]),'secondary_documents':len([x for x in d if not x['independent']]),
   'original_passages':len([p for p in passages(d) if p['independent']]),'source_cache_files':len(list((base/'lab/ocean/sources').glob('*.json'))),
   'experiment_ids':[r['id'] for r in records if 'id' in r],'session_ids':sorted(set(sessions+direct)),
   'project_cards_files':len(list((base/'lab/ocean/project/cards').glob('*.json'))),'analysis_files':len(list((base/'lab/ocean/intelligence/results').glob('*.json')))}
 return {'schema':'vdn.continuity-inventory/11.2','snapshot_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'scope':'repository files and explicitly named isolated previous lab; counts never pooled','knowledge_markdown_files':len(list((root/'knowledge').rglob('*.md'))),
 'note_statuses':dict(collections.Counter(n.get('status','UNKNOWN') for n in notes)),'categories':categories,'note_duplicate_definitions':{k:v for k,v in byid.items() if len(v)>1},
 'registry_broken_references':missing,'unresolved_wikilinks':links,'json_identifier_occurrences':occurrences,'scan_diagnostics':errors,'historical_snapshots':history,'modules':modules,'runtime_scopes':runtime_counts,
 'not_proven':['historical discussion meaning of approximately 150 IDs','remote URL availability','semantic truth or technical applicability','private desktop assets outside authorized paths']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--runtime',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 r=run(a.root,a.runtime);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'notes':r['categories']['knowledge_note']['unique'],'registry_broken':len(r['registry_broken_references']),'unresolved_wikilinks':len(r['unresolved_wikilinks']),'runtime':r['runtime_scopes']},ensure_ascii=False))
