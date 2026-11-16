"""Passage embeddings derived from V11 local adapter, model digest bound."""
import json
import math
from agent import budget,intelligence_evidence as ev,intelligence_models as im,ocean_semantic
from agent.storage import atomic_write
from agent.ocean_web import OceanWeb,settings
from agent.obsidian import safe_path
from agent.lab_store import clean_json


def identity(root,opener=None):
    cfg=settings(root)['semantic']
    if not cfg['enabled'] or not cfg['model']:raise ValueError('embeddings disabled or model missing')
    local={**im.settings(root),'endpoint':cfg['endpoint']}
    installed=im.Ollama(local,opener).inventory()
    found=next((m for m in installed if m['name']==cfg['model']),None)
    if not found:raise ValueError('exact embedding model not installed')
    return {'endpoint':cfg['endpoint'],'name':found['name'],'digest':found['digest']}


def index(root,apply=False,max_items=10,opener=None):
    from agent.engine import integer
    integer(max_items,'max_items',1,10)
    ps=ev.passages(ev.documents(root));path=safe_path(root,'lab/ocean/intelligence/embeddings.json')
    if not apply:return {'state':'simulation','passages':len(ps),'automatic_download':False}
    def work():
        model=identity(root,opener);data=read(path) if path.exists() else {'model':model,'vectors':{}}
        if data['model']!=model:raise ValueError('embedding model changed; archive derived index explicitly')
        pending=[p for p in ps if not p['hostile'] and data['vectors'].get(p['id'],{}).get('sha256')!=ev.digest(p['text'])][:max_items]
        if not pending:return {'state':'unchanged','model':model}
        vectors=ocean_semantic.vectors(root,[p['text'] for p in pending])
        for p,v in zip(pending,vectors):data['vectors'][p['id']]={'sha256':ev.digest(p['text']),'vector':v}
        text=clean_json(data,1_000_000);OceanWeb(root).storage_check(len(text.encode('utf-8')));atomic_write(path,text)
        return {'state':'indexed','items':len(pending),'remaining':len(ps)-len(data['vectors']),'model':model,'quality':'not established'}
    return im.operation(root,work)


def read(path):
    if path.stat().st_size>1_000_000:raise ValueError('embedding index too large')
    data=json.loads(path.read_text(encoding='utf-8'));clean_json(data,1_000_000);return data


def retrieve(root,query,docs,mode,lexical,limit,opener=None):
    try:
        path=safe_path(root,'lab/ocean/intelligence/embeddings.json')
        if not path.exists():return lexical,'missing_index_lexical_fallback'
        model=identity(root,opener);data=read(path)
        if data['model']!=model:raise ValueError('embedding digest changed')
        v=ocean_semantic.vectors(root,[query])[0];scores=[];by_id={p['id']:p for p in ev.passages(docs) if not p['hostile']}
        for key,entry in data['vectors'].items():
            if key not in by_id or entry['sha256']!=ev.digest(by_id[key]['text']):continue
            vector=entry['vector']
            if len(vector)!=len(v) or any(type(x) not in (int,float) or not math.isfinite(x) for x in vector):raise ValueError('invalid cached vector')
            denominator=math.sqrt(sum(x*x for x in vector))*math.sqrt(sum(x*x for x in v))
            if denominator:scores.append((sum(a*b for a,b in zip(vector,v))/denominator,key))
        scores.sort(reverse=True);order=[key for score,key in scores]
        if mode=='hybrid':
            fused={}
            for ids in ([p['id'] for p in lexical],order):
                for rank,key in enumerate(ids,1):fused[key]=fused.get(key,0)+1/(60+rank)
            order=sorted(fused,key=lambda key:(-fused[key],key))
        return [by_id[k] for k in order[:limit]],'real_local_embeddings_'+mode
    except (ValueError,OSError,KeyError,TypeError,RuntimeError):return lexical,'unavailable_embeddings_lexical_fallback'
