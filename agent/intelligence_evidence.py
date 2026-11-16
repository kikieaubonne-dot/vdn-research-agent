"""Problem analysis, local evidence retrieval and mechanical attribution.

An exact quote establishes attribution, not technical truth. Editorial notes
are secondary evidence even when they link to an official website.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit
from agent import budget, ocean_knowledge
from agent.corpus import scan_notes
from agent.engine import string
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.text import tokens, fold, BM25

VERSION = '11.2.5'
STATUSES = ('SOURCE_SUPPORTED','INFERRED','HYPOTHESIS','EXPERIMENT_PROPOSAL','UNSUPPORTED','CONTRADICTED','OUTDATED')
HOSTILE = re.compile(r'(?i)ignore (?:all|previous)|system prompt|reveal .*secret|api.?key|powershell|subprocess|delete .*files|execute .*command|curl\s|rm -rf')


def digest(value):
    return hashlib.sha256(clean_json(value,2_000_000).encode('utf-8')).hexdigest()


def analyze(question):
    string(question,'question');q=fold(question);problems=[]
    patterns=[('collision',r'bloqu|coinc|collision|stuck|branches.*joueur|can.?collide'),
              ('appearance',r'artific|realis|realism|silhouette|aiguille|foliage|hair.?card|apparence'),
              ('lighting',r'nuit|night|rendu|render|lampe|flashlight|fog|brouillard|eclair'),
              ('performance',r'perform|saccad|fps|optim|lod|stream'),
              ('export',r'export|fbx|rig|animation|blender')]
    for name,pattern in patterns:
        if re.search(pattern,q):problems.append(name)
    software=[s for s in ('Roblox','Blender','Unreal') if s.lower() in q]
    versions={m.group(1).title():m.group(2) for m in re.finditer(r'(?i)\b(Roblox|Blender|Unreal)\s+(\d+(?:\.\d+){1,2})\b',question)}
    return {'objective':question,'problems':problems,'software':software,'versions':versions,
            'context':'Le Voisin de Noël — laboratory copies only','symptoms':question,
            'constraints':['no production changes','no undocumented parameters','target hardware must be recorded'],
            'missing':['asset copies and current settings','software versions not supplied','reproducible baseline and device'],
            'hypotheses':[{'problem':p,'text':{'collision':'Les volumes de collision pourraient gêner le parcours du contrôleur.',
                'appearance':'La silhouette, les normales ou les matériaux pourraient contribuer au rendu artificiel.',
                'lighting':'L’éclairage et la lisibilité nocturne pourraient devoir être isolés du matériau.',
                'performance':'La densité, la géométrie ou le rendu pourraient contribuer au coût.',
                'export':'Les transformations ou la compatibilité du pipeline pourraient intervenir.'}[p],
                'status':'HYPOTHESIS'} for p in problems],
            'success_criteria':['same controlled scene and repeatable route','record movement defects and frame measurements','human review of appearance'],
            'method':'deterministic domain intent; hypotheses are not diagnoses'}


def engine_for(url,title=''):
    host=urlsplit(url).hostname or ''
    if host in ('create.roblox.com','devforum.roblox.com'):return 'Roblox'
    if host=='docs.blender.org':return 'Blender'
    if host=='dev.epicgames.com':return 'Unreal'
    return next((s for s in ('Roblox','Blender','Unreal') if s.lower() in title.lower()),'unknown')


def documents(root,diagnostics=None,*,include_rejected=False):
    """Read bounded existing V11 source caches and notes; never fetch a URL."""
    if type(include_rejected) is not bool:raise ValueError('include_rejected must be boolean')
    root=Path(root).resolve();out=[];diagnostics=[] if diagnostics is None else diagnostics
    folder=safe_path(root,'lab/ocean/sources')
    paths=sorted(folder.glob('*.json')) if folder.exists() else []
    if len(paths)>1000:raise ValueError('source snapshot limit exceeded')
    for path in paths:
        try:
            path=safe_path(root,path.relative_to(root).as_posix())
            if path.stat().st_size>200_000:raise ValueError('source too large')
            d=json.loads(path.read_text(encoding='utf-8'));clean_json(d,200_000)
            if not isinstance(d,dict) or not isinstance(d.get('text'),str) or not isinstance(d.get('url'),str):raise ValueError('invalid source snapshot types')
            if type(d.get('at',0)) not in (int,float) or not isinstance(d.get('version','unknown'),str) or not isinstance(d.get('conditions',{}),dict):raise ValueError('invalid source snapshot metadata')
            if hashlib.sha256(d['text'].encode('utf-8')).hexdigest()!=d['text_sha256']:raise ValueError('source hash mismatch')
            u=urlsplit(d['url'])
            if u.scheme!='https' or not u.hostname or u.username or u.password or u.query:raise ValueError('unsafe recorded source URL')
            # Receipt is a previously collected snapshot, not a new source visit.
            version=d.get('version','unknown');engine=engine_for(d['url'])
            literal_version=re.search(r'\bBlender (\d+\.\d+(?:\.\d+)?) Manual\b',d['text'][:1000])
            if engine=='Blender' and version=='unknown' and literal_version:version=literal_version.group(1)
            out.append({'id':'doc-'+digest([d['url'],d['text_sha256']])[:24],'url':d['url'],
                        'title':next((s.lstrip('# ') for s in d['text'].splitlines() if s.startswith('#')),d['text'].splitlines()[0][:200] if d['text'].splitlines() else 'Source snapshot'),
                        'text':d['text'],'sha256':d['text_sha256'],'source_type':'recorded_source_snapshot',
                        'engine':engine,'version':version,'published':d.get('published'),
                        'accessed':d.get('accessed'),'retrieved_at':d.get('at',0),'truncated':d.get('truncated',False),
                        'independent':True,'conditions':d.get('conditions',{})})
        except (ValueError,KeyError,TypeError,OSError) as exc:diagnostics.append({'path':path.name,'error':type(exc).__name__})
    for n in scan_notes(root,diagnostics):
        if n.get('status')=='rejete' and not include_rejected:continue
        body=n['_body'];urls=n.get('sources',[])
        # Restrict secondary retrieval to source quotation, never generated steps.
        for m in re.finditer(r'^>\s*(?:«\s*)?(.+?)(?:\s*»)?\s*$',body,re.M):
            text=m.group(1).strip()
            adjacent=re.match(r'\s*\n>\s*—\s*\[source\]\((https://[^)]+)\)',body[m.end():])
            url=adjacent.group(1) if adjacent and adjacent.group(1) in urls else urls[0] if len(urls)==1 else ''
            if text.startswith(('—','- [source]')) or len(text)<20:continue
            if len(out)>=2000:break
            out.append({'id':'doc-'+digest([n['id'],text])[:24],'url':url,'title':n.get('title',n['id']),
                        'text':text,'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),
                        'source_type':'secondary_recorded_excerpt','engine':engine_for(url,n.get('title','')),
                        'version':n.get('engine_version','unknown'),'published':None,'accessed':n.get('accessed'),
                        'retrieved_at':0,'truncated':False,'independent':False,'note_id':n['id'],'conditions':{}})
    # URL canonicalization may leave multiple cache filenames for the same
    # snapshot (for example extensionless/.md). Keep the freshest receipt, not
    # duplicate evidence or retrieval slots. Metadata variants remain distinct.
    unique={}
    for d in out:
        key=digest([d['url'],d['sha256'],d['version'],d['conditions'],d['source_type']])
        if key not in unique or d['retrieved_at']>unique[key]['retrieved_at']:unique[key]=d
    return list(unique.values())


def context_only(text):
    # Retain images in source snapshots, but never elevate their captions to
    # technical assertions. Plain-language captions without markup remain a limit.
    return bool(re.match(r'^\s*(?:>\s*)?!\[',text))


def passages(docs):
    result=[]
    for d in docs:
        budget.check();text=d['text'];section='document';blocks=list(re.finditer(r'\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*',text))
        for index,m in enumerate(blocks):
            if m.group().startswith('#'):
                section=m.group().splitlines()[0].lstrip('# ')
            start,end=m.span()
            # Preserve a following warning/condition; do not extract an isolated
            # imperative without the adjoining restriction.
            if index+1<len(blocks) and re.match(r'(?i)(?:warning|note|caution|limitation|attention|however|only|requires)\b',blocks[index+1].group()):end=blocks[index+1].end()
            full=text[start:end];cut=len(full)>1400
            if cut:
                # Long blocks use overlapping windows; mark them incomplete.
                windows=[(s,min(s+1400,end)) for s in range(start,end,1200)][:30]
            else:windows=[(start,end)]
            for a,b in windows:
                value=text[a:b]
                if len(value)<8:continue
                result.append({'id':'pass-'+digest([d['id'],a,b])[:24],'document_id':d['id'],'url':d['url'],'title':d['title'],
                    'section':section[:200],'start':a,'end':b,'line':text.count('\n',0,a)+1,'text':value,
                    'document_sha256':d['sha256'],'engine':d['engine'],'version':d['version'],'published':d['published'],
                    'accessed':d['accessed'],'source_type':d['source_type'],'independent':d['independent'],
                    'conditions':d['conditions'],'retrieved_at':d['retrieved_at'],'incomplete_context':cut or d['truncated'],
                    'hostile':bool(HOSTILE.search(value)),'context_only':context_only(value)})
    return result


QUERIES={'collision':'MeshPart CollisionFidelity CanCollide collision player controller',
         'appearance':'mesh geometry silhouette foliage cards SurfaceAppearance PBR normals',
         'lighting':'lighting Atmosphere fog SpotLight night Shadows',
         'performance':'performance geometry streaming LOD triangles',
         'export':'Blender FBX export rig animation transforms'}


def retrieve(question,docs,limit=8,queries=None,anchors=None):
    intent=analyze(question);ps=[p for p in passages(docs) if not p['context_only']]
    if anchors:
        terms=set(tokens(' '.join(anchors)))
        ps=[p for p in ps if terms & set(tokens(p['text']+' '+p['section']))]
    index=BM25([tokens(p['title']+' '+p['section']+' '+p['text']) for p in ps]);picked=[]
    scoped=queries is not None
    queries=queries if scoped else [QUERIES[p] for p in intent['problems']]+[ocean_knowledge.expand(question)]
    scores={}
    # Diversify by problem first, then fill by lexical score.
    for query in queries:
        ranked=index.top(tokens(query),len(ps))
        ranked=[(i,s*(1.6 if ps[i]['independent'] else .6)*(.75 if ps[i]['incomplete_context'] else 1)) for i,s in ranked]
        ranked.sort(key=lambda pair:(-pair[1],ps[pair[0]]['id']))
        for i,s in ranked:scores[i]=max(s,scores.get(i,0))
        best=next((i for i,s in ranked if not ps[i]['hostile'] and i not in picked),None)
        if best is not None:picked.append(best)
    if not scoped and set(intent['problems'])&{'appearance','export'} and not any(ps[i]['engine']=='Blender' for i in picked):
        modelling=[(i,s) for i,s in index.top(tokens('Blender mesh geometry normals export'),len(ps))
                   if ps[i]['engine']=='Blender' and ps[i]['independent'] and not ps[i]['hostile']]
        if modelling:
            i,s=modelling[0];scores[i]=s;picked.append(i)
    for i in sorted(scores,key=lambda i:(-scores[i],ps[i]['id'])):
        if i not in picked and not ps[i]['hostile']:picked.append(i)
    return [{**ps[i],'retrieval_score':scores[i]} for i in picked[:limit]]


def verify(claim,selected,docs,intent,now=None):
    now=now or dt.datetime.now(dt.timezone.utc).isoformat();issues=[]
    text=claim.get('text','');kind=claim.get('kind','INFERRED');ids=claim.get('passage_ids',[])
    if kind not in STATUSES:kind='UNSUPPORTED';issues.append('invalid_claim_kind')
    if not isinstance(text,str) or not 1<=len(text)<=600:text='Invalid model claim';kind='UNSUPPORTED';issues.append('invalid_text')
    if not isinstance(ids,list) or not all(isinstance(x,str) for x in ids):ids=[];issues.append('invalid_passage_ids')
    refs=[p for p in selected if p['id'] in ids];by_doc={d['id']:d for d in docs}
    if not ids or len(refs)!=len(set(ids)):issues.append('missing_passage')
    for p in refs:
        d=by_doc.get(p['document_id'])
        if not d or hashlib.sha256(d['text'].encode('utf-8')).hexdigest()!=p['document_sha256'] or d['text'][p['start']:p['end']]!=p['text']:issues.append('document_span_mismatch')
    joined=' '.join(p['text'] for p in refs);numbers=re.findall(r'(?<![\w])[-+]?\d+(?:[.,]\d+)*',text)
    source_numbers=set(re.findall(r'(?<![\w])[-+]?\d+(?:[.,]\d+)*',joined))
    if any(n not in source_numbers for n in numbers):issues.append('unsupported_number')
    version=claim.get('version','unknown');engine=claim.get('engine','unknown')
    if version!='unknown' and not any(p['version']==version for p in refs):issues.append('version_not_supported')
    if engine!='unknown' and refs and not any(p['engine'] in (engine,'unknown') for p in refs):issues.append('engine_mismatch')
    if intent['software'] and engine not in ('unknown',*intent['software']):issues.append('target_engine_requires_adaptation')
    if intent['software'] and any(p['engine'] not in ('unknown',*intent['software']) for p in refs):issues.append('source_engine_requires_adaptation')
    if any(p['version']!='unknown' and p['engine'] in intent['versions'] and p['version']!=intent['versions'][p['engine']] for p in refs):issues.append('requested_version_mismatch')
    if HOSTILE.search(text):issues.append('hostile_instruction')
    if context_only(text) or any(p.get('context_only') for p in refs):issues.append('image_caption_not_a_technical_assertion')
    literal=bool(refs) and any(re.sub(r'\s+',' ',text).strip() in re.sub(r'\s+',' ',p['text']) for p in refs)
    if numbers and not literal:issues.append('numeric_relation_not_literal')
    state=kind
    if issues:state='UNSUPPORTED'
    elif kind=='SOURCE_SUPPORTED':
        if not literal or len(text)<12:state='INFERRED';issues.append('paraphrase_not_mechanically_entailed')
        elif not all(p['independent'] for p in refs):state='INFERRED';issues.append('secondary_excerpt_requires_original')
        elif any(p['incomplete_context'] for p in refs):state='INFERRED';issues.append('incomplete_source_context')
    if state=='SOURCE_SUPPORTED' and any(p['published'] and str(p['published'])[:4].isdigit() and int(str(p['published'])[:4])<dt.date.today().year-1 for p in refs):
        state='OUTDATED';issues.append('publication_age_requires_review')
    if state=='SOURCE_SUPPORTED' and any(p['retrieved_at'] and time.time()-p['retrieved_at']>86400 for p in refs):
        state='OUTDATED';issues.append('snapshot_older_than_one_day_requires_refresh')
    return {'id':'claim-'+digest([text,sorted(ids),engine,version])[:24],'text':text,'passage_ids':ids,
            'source_ids':sorted({p['document_id'] for p in refs}),'version':version,'engine':engine,'kind':kind,
            'support':state,'verification':'attribution_only' if state=='SOURCE_SUPPORTED' else 'not_verified',
            'issues':issues,'contradictions':[],'last_evaluated':now,'truth_verified':False}


def contradictions(selected):
    values=[]
    for p in selected:
        for m in re.finditer(r'\b([A-Za-z][A-Za-z0-9_.]*)\s*(?:=|:|is)\s*(true|false)\b',p['text'],re.I):values.append((m.group(1).lower(),m.group(2).lower(),p))
    out=[]
    for i,(prop,value,p) in enumerate(values):
        for other,v,q in values[i+1:]:
            if prop!=other or value==v or p['document_id']==q['document_id'] or p['engine']!=q['engine']:continue
            same=p['version']==q['version'] and p['version']!='unknown' and bool(p['conditions']) and p['conditions']==q['conditions']
            out.append({'property':prop,'passage_ids':[p['id'],q['id']],
                        'kind':'explicit_conflict_same_declared_conditions' if same else 'possible_conflict_compare_versions_and_conditions',
                        'status':'CONTRADICTED' if same else 'needs_review','truth_verified':False})
    return out[:20]
