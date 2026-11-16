"""Optional local embeddings and hybrid ranking. No model download or paid API.

Vectors are derived data, never evidence. Missing service/index degrades to lexical.
"""
import hashlib
import json
import math
from pathlib import Path
import urllib.request
from urllib.parse import urlsplit
from agent import budget,ocean_knowledge,rag
from agent.models import NoRedirect
from agent.ocean_web import settings,OceanWeb
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.storage import atomic_write
from agent.autonomy import Lock
from agent.research_queue import ResearchQueue


def vectors(root,texts):
    cfg=settings(root)['semantic'];url=urlsplit(cfg['endpoint'])
    if not cfg['enabled'] or not cfg['model']:raise ValueError('local embedding model not configured')
    if url.scheme!='http' or url.hostname not in ('127.0.0.1','::1') or url.username or url.password or url.query or url.fragment:raise ValueError('embeddings require explicit loopback HTTP')
    payload={'model':cfg['model'],'input':[s[:12000] for s in texts]}
    request=urllib.request.Request(cfg['endpoint'].rstrip('/')+'/api/embed',json.dumps(payload).encode('utf-8'),{'Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect,urllib.request.ProxyHandler({})).open(request,timeout=budget.request(10)) as response:raw=response.read(1000001)
    if len(raw)>1000000:raise ValueError('embedding response too large')
    values=json.loads(raw)['embeddings']
    if not isinstance(values,list) or len(values)!=len(texts):raise ValueError('embedding shape mismatch')
    size=None
    for vector in values:
        if not isinstance(vector,list) or not 1<=len(vector)<=4096 or any(type(x) not in (int,float) or not math.isfinite(x) for x in vector):raise ValueError('invalid embedding vector')
        if size is not None and size!=len(vector):raise ValueError('inconsistent embedding dimensions')
        if not any(vector):raise ValueError('zero embedding vector')
        size=len(vector)
    return values


def operation(root,fn,max_calls):
    # Explicit local model traffic still shares the daily HTTP counter.
    with Lock(root,7200):
        q=ResearchQueue(root,recover=False);daily=q.daily();cfg=q.cfg
        def checkpoint(resource):
            if daily['http_calls']>=cfg['daily']['max_http_calls']:raise budget.BudgetExhausted('daily embedding HTTP limit',scope='daily',resource='http_calls',limit=cfg['daily']['max_http_calls'],used=daily['http_calls'])
            daily['http_calls']+=1;q.save()
        guard=budget.Budget(20,max_calls,checkpoint,http_scope='operation')
        with budget.using(guard):return fn()


def index(root,apply=False,max_items=4):
    from agent.engine import integer
    integer(max_items,'max_items',1,10)
    cards=ocean_knowledge.cards(root);path=safe_path(root,'lab/ocean/semantic.json');cfg=settings(root)['semantic']
    existing=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'model':cfg['model'],'vectors':{}}
    if existing['model']!=cfg['model']:raise ValueError('model changed; archive derived index explicitly before rebuilding')
    texts={c['id']:c['title']+' '+' '.join(x['quote'] for x in c['claims']) for c in cards}
    pending=[(k,t) for k,t in texts.items() if existing['vectors'].get(k,{}).get('sha256')!=hashlib.sha256(t.encode('utf-8')).hexdigest()][:max_items]
    if not apply:return {'state':'simulation','pending_ids':[k for k,t in pending],'model':cfg['model']}
    if not pending:return {'state':'unchanged','model':cfg['model']}
    result=operation(root,lambda:vectors(root,[t for k,t in pending]),1)
    for (key,text),v in zip(pending,result):existing['vectors'][key]={'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),'vector':v}
    text=clean_json(existing,1000000);OceanWeb(root).storage_check(len(text.encode('utf-8')));atomic_write(path,text)
    return {'state':'indexed','items':len(result),'model':cfg['model'],'semantic_quality':'not established by indexing'}


def hybrid(root,query,limit=5):
    lexical=ocean_knowledge.search(root,query,limit);path=safe_path(root,'lab/ocean/semantic.json')
    if not path.exists():return {'results':lexical,'semantic_state':'missing_index'}
    try:
        if path.stat().st_size>1000000:raise ValueError('oversized embedding index')
        data=json.loads(path.read_text(encoding='utf-8'));cfg=settings(root)['semantic']
        clean_json(data,1000000)
        if data['model']!=cfg['model']:raise ValueError('embedding model mismatch')
        query_v=operation(root,lambda:vectors(root,[query]),1)[0];ranked=[]
        cards={c['id']:c for c in ocean_knowledge.cards(root)}
        for key,entry in data['vectors'].items():
            if key not in cards or len(entry['vector'])!=len(query_v):continue
            c=cards[key];text=c['title']+' '+' '.join(x['quote'] for x in c['claims'])
            if entry['sha256']!=hashlib.sha256(text.encode('utf-8')).hexdigest():continue
            v=entry['vector']
            if any(type(x) not in (int,float) or not math.isfinite(x) for x in v):raise ValueError('invalid cached vector')
            norm=math.sqrt(sum(x*x for x in v))*math.sqrt(sum(x*x for x in query_v))
            if not norm:continue
            ranked.append((sum(a*b for a,b in zip(v,query_v))/norm,key))
        ranked.sort(reverse=True);scores={}
        # Reciprocal rank fusion; similarity is not a truth or confidence score.
        for sequence in ([x['id'] for x in lexical],[k for s,k in ranked]):
            for rank,key in enumerate(sequence,1):scores[key]=scores.get(key,0)+1/(60+rank)
        order=sorted(scores,key=lambda k:(-scores[k],k))[:limit]
        return {'results':[{'id':k,'title':cards[k]['title'],'sources':[s['url'] for s in cards[k]['sources']],'fusion_score':scores[k],'truth_verified':False} for k in order],
                'semantic_state':'local_model_vectors','semantic_quality':'requires evaluation with real model; vectors are not evidence'}
    except (ValueError,OSError,KeyError,TypeError,RuntimeError):return {'results':lexical,'semantic_state':'unavailable_lexical_fallback'}
