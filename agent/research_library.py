"""Non-destructive library tiers and scoped lexical fusion over existing RAG."""
import re
from agent import rag
from agent.corpus import scan_notes
from agent.engine import KnowledgeEngine,integer,string
from agent.intelligence_evidence import digest
from agent.text import fold


def tier(note):
 if note.get('status') in ('rejete','obsolete'):return 'ARCHIVE'
 if note.get('status') in ('documente','reproduit','valide') and note.get('sources') and re.search(r'^>\s',note['_body'],re.M):return 'MAIN'
 return 'RESERVE'

def canonical(text,version='unknown',conditions=None):
 # Exact normalized passage only. Different parameters, words, engine/version
 # or conditions remain distinct. This is not semantic paraphrase equivalence.
 return 'evidence-'+digest([re.sub(r'\s+',' ',text).strip(),version,conditions or {}])[:24]

class Library:
 def __init__(self,root):self.root=root;self.engine=KnowledgeEngine(root)
 def inventory(self):
  notes=scan_notes(self.root);groups={k:[] for k in ('MAIN','RESERVE','ARCHIVE')}
  for n in notes:groups[tier(n)].append(n['id'])
  return {'tiers':groups,'counts':{k:len(v) for k,v in groups.items()},'physical_moves':0,'deleted':0,'meaning':'note curation states, never independent engine verification'}
 def search(self,query,branch=None,limit=5):
  string(query,'query');integer(limit,'limit',1,10);notes={n['id']:n for n in scan_notes(self.root)}
  queries=[query]+([branch['query']] if branch and branch['query']!=query else []);scores={};hits={}
  self.engine._ensure_index()
  for q in queries[:2]:
   raw=rag.search_knowledge(q,10,8000,self.root)
   seen=set()
   for h in raw['results']:
    if h['note_id'] in seen:continue
    seen.add(h['note_id']);rank=len(seen);nid=h['note_id'];scores[nid]=scores.get(nid,0)+1/(60+rank)
    hits.setdefault(nid,h)
  groups={'MAIN':[],'RESERVE':[]};seen={};incompatible=[]
  for nid in sorted(scores,key=lambda n:(-scores[n],n)):
   n=notes[nid];t=tier(n)
   if t=='ARCHIVE':continue
   full=self.engine.get_knowledge(nid);scope=full['compatibility']['scope']
   if scope=='other_engine':incompatible.append(nid);continue
   h=hits[nid];key=canonical(n['_body'],str(n.get('engine_version','unknown')),{'scope':scope,'tier':t})
   if key in seen:
    seen[key]['aliases'].append(nid);seen[key]['sources']=list(dict.fromkeys(seen[key]['sources']+n.get('sources',[])));continue
   item={'note_id':nid,'title':n['title'],'tier':t,'canonical_evidence_id':key,'aliases':[nid],'sources':n.get('sources',[]),'excerpt':h['text'][:350],'version':n.get('engine_version','unknown'),'scope':scope,'rank_score':scores[nid],'independent_original':False,'verification':'note reference only; inspect original and applicability'}
   groups[t].append(item);seen[key]=item
  # Keep candidates visible even when there is no main-library result.
  ranked=sorted([x for g in groups.values() for x in g],key=lambda x:-x['rank_score'])[:limit]
  return {'query':query,'results':ranked,'main':groups['MAIN'][:limit],'reserve':groups['RESERVE'][:limit],'incompatible':incompatible,'duplicate_groups':sum(len(x['aliases'])-1 for x in seen.values()),'queries':queries,'abstained_from_verified_answer':True,'empty_reason':'no compatible traceable note; propose a bounded source search' if not ranked else None,'policy':'two-query reciprocal-rank fusion only for explicit branch scope; evidence levels kept separate'}
