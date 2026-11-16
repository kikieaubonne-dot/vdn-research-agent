"""Bounded one-shot research and source-based candidate notes. Never self-deploys."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import math
from urllib.robotparser import RobotFileParser

from agent import budget, providers, knowledge
from agent.autonomy import Lock
from agent.corpus import scan_notes
from agent.research_queue import ResearchQueue, load_config
from agent.storage import atomic_write
from agent.procedure import actionable_excerpts
from agent.relevance import sentences


def config(root):
    cfg=json.loads((Path(root)/'config'/'factory_v9.json').read_text(encoding='utf-8'))
    for key in ('max_items','max_http_calls','max_attempts','stagnation_limit'):
        if type(cfg[key]) is not int or cfg[key]<0:raise ValueError('invalid factory limit: '+key)
    if not isinstance(cfg['time_budget_s'],(float,int)) or not math.isfinite(cfg['time_budget_s']) or cfg['time_budget_s']<0:
        raise ValueError('invalid factory time budget')
    return cfg


def known(root, url):
    canonical=providers.canonical_url(url)
    return next((n for n in scan_notes(root) if canonical in [providers.canonical_url(s) for s in n.get('sources',[])]),None)


def write_candidate(root, recipe, documents):
    root=Path(root)
    if not re.fullmatch(r'[a-z0-9_-]{1,60}',recipe['domain']):raise ValueError('unsafe knowledge domain')
    for url in recipe['urls']:providers.validate_url(url)
    canonical=providers.canonical_url(recipe['urls'][0])
    previous=known(root,canonical)
    if previous:return {'action':'duplicate','id':previous['id'],'path':previous['_path']}
    joined='\n'.join(documents[u] for u in recipe['urls'])
    if re.search(r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{30,}|(?:api_key|secret_key)\s*[:=]\s*[A-Za-z0-9_-]{24,}',joined,re.I):
        raise ValueError('possible credential in source; publication refused')
    if not all(a.lower() in joined.lower() for a in recipe['anchors']):
        raise ValueError('required source anchors absent; candidate not published')
    accessed=dt.datetime.now(dt.timezone.utc).date().isoformat()
    source_dates=[];hashes=[];quotes=[]
    for url in recipe['urls']:
        text=documents[url]
        if len(text.encode('utf-8'))>200000 or not re.search(r'^#\s+\S',text,re.M):
            raise ValueError('invalid or oversized Markdown source')
        meta,_=knowledge.parse_note(text)
        source_dates.append(str(meta.get('last_updated','unknown')))
        hashes.append(hashlib.sha256(text.encode()).hexdigest())
        # Publish at most 24 literal source words per page, never the full cache.
        short=[s for s in sentences(text) if 35<=len(s)<=240 and len(s.split())<=24 and not s.startswith(('#','|','```','---'))]
        selected=(actionable_excerpts(short) or short)[:1]
        quotes += [(q,url) for q in selected]
    nid=knowledge.note_id(canonical)
    meta={'id':nid,'title':recipe['title'],'domain':recipe['domain'],'subdomain':recipe['topic'],
          'status':'candidat','source_tier':1,'sources':[providers.canonical_url(u) for u in recipe['urls']],
          'provider':'roblox_docs','official':True,'accessed':accessed,'created':accessed,'updated':accessed,
          'engine_version':'inconnue','tested_in_studio':'non','confidence':'faible',
          'evidence_status':'a_verifier','compatibility_status':'non_verifie','procedure_status':'candidate',
          'review_status':'pending','source_dates':source_dates,'source_sha256':hashes,
          'queries':[recipe['task']+' '+ ' '.join(recipe['anchors'])],
          'editorial_steps':recipe['steps'],'procedure_origin':'source_based_editorial_candidate',
          'production_priority':recipe['priority'],'tags':['vdn','v9',recipe['task'],'a-verifier']}
    lines=[f"# {recipe['title']}",'','> Procédure éditoriale candidate issue des sources listées ; aucun test Studio ni revue externe.','',
           '## Problème','',recipe['task'],'','## Contexte','','Roblox ; version du projet et appareils à vérifier.','',
           '## Sources','']
    lines += [f'- [{i+1}] {u} — consulté le {accessed}' for i,u in enumerate(meta['sources'])]
    for heading,values in [('Prérequis',recipe['prerequisites']),('Méthode candidate',recipe['steps']),
                           ('Limites connues de Roblox',recipe['constraints']),('Alternatives',recipe['alternatives'])]:
        lines += ['',f'## {heading}','']+[f'- {s} '+('[proposition de conception non validée]' if 'Hypothèse' in s else '[source 1]') for s in values]
    lines += ['','## Paramètres (sourcés)','']+['- '+p+' [source 1]' for p in recipe.get('parameters',[])]
    lines += ['',
              '## Protocole de reproduction proposé, non exécuté','',recipe['validation'],'',
              '## Diagnostic','','Conserver erreurs, environnement, paramètres et observations. Les causes proposées restent des hypothèses.','',
              '## Retour arrière','',recipe['rollback'],'','## Extraits justificatifs','']
    for quote,url in quotes:lines += [f'> « {quote} »',f'> — [source]({providers.canonical_url(url)})','']
    lines += ['## Niveau de preuve','','Documentation officielle consultée ; exactitude de la procédure proposée et fonctionnement dans le jeu non vérifiés.','']
    path=root/'knowledge'/recipe['domain']/(nid[4:]+'-'+knowledge.slugify(recipe['title'],50)+'.md')
    atomic_write(path,knowledge.dump_frontmatter(meta)+'\n'+'\n'.join(lines),create_only=True)
    return {'action':'created','id':nid,'path':path.relative_to(root).as_posix(),'status':'candidat','sources':meta['sources']}


def import_evidence(root, folder, *, apply=False):
    if apply:
        with Lock(root,7200):return _import_evidence(root,folder,apply=True)
    return _import_evidence(root,folder,apply=False)


def _import_evidence(root, folder, *, apply=False):
    """Publish only configured source-based drafts from a previously recorded read."""
    folder=Path(folder).resolve();access=json.loads((folder/'access.json').read_text())
    documents={}
    for record in access['sources']:
        if record.get('status')!='read':continue
        path=(folder/record['path']).resolve()
        if not path.is_relative_to(folder) or path.is_symlink():raise ValueError('unsafe evidence path')
        if path.stat().st_size>200000:raise ValueError('source too large')
        providers.validate_url(record['url'])
        documents[record['url']]=path.read_text(encoding='utf-8')
    out=[]
    for recipe in sorted(config(root)['recipes'],key=lambda r:r['priority']):
        if not all(u in documents for u in recipe['urls']):
            out.append({'task':recipe['task'],'action':'missing_source'});continue
        if not apply:out.append({'task':recipe['task'],'action':'would_publish'});continue
        out.append({'task':recipe['task'],**write_candidate(root,recipe,documents)})
    return {'schema':'vdn.enrichment/9','http_calls_recorded':access['http_calls'],'items':out,
            'verification':'source_based_candidates_not_tested'}


def collect(root, *, apply=False, max_items=None, getter=None):
    """Explicit one-shot, existing transport/retries/budgets, shared daily counters."""
    root=Path(root);cfg=config(root);global_cfg=load_config(root)
    cap=min(cfg['max_items'],global_cfg['cycle']['max_items']) if max_items is None else max_items
    if type(cap) is not int or not 0<=cap<=min(cfg['max_items'],global_cfg['cycle']['max_items']):raise ValueError('invalid max_items')
    recipes=sorted(cfg['recipes'],key=lambda r:r['priority'])[:cap]
    if not apply:return {'state':'simulation','tasks':[r['task'] for r in recipes],'network_requests':0}
    getter=getter or providers.http_get
    result={'schema':'vdn.factory-cycle/9','items':[],'errors':[],'stop_reason':None}
    with Lock(root,global_cfg['lock']['stale_after_s']):
        q=ResearchQueue(root,recover=False);daily=q.daily()
        def checkpoint(resource):
            key='http_calls' if resource=='http_calls' else 'fetch'
            maximum=global_cfg['daily']['max_http_calls'] if key=='http_calls' else global_cfg['daily']['max_fetch']
            if daily[key]>=maximum:raise budget.BudgetExhausted('daily quota reached')
            daily[key]+=1;q.save()
        guard=budget.Budget(min(cfg['time_budget_s'],global_cfg['cycle']['time_budget_s']),
                            min(cfg['max_http_calls'],global_cfg['cycle']['max_http_calls'],max(0,global_cfg['daily']['max_http_calls']-daily['http_calls'])),checkpoint)
        state_path=root/'output'/'factory_state.json'
        state=json.loads(state_path.read_text()) if state_path.exists() else {'attempts':{}}
        documents={};stagnant=0;rules=None
        with budget.using(guard):
            for recipe in recipes:
                try:
                    guard.check()
                    existing=known(root,recipe['urls'][0])
                    if existing:
                        result['items'].append({'task':recipe['task'],'action':'duplicate','id':existing['id']});stagnant+=1
                        if stagnant>=cfg['stagnation_limit']:result['stop_reason']='stagnation';break
                        continue
                    if daily['items']>=global_cfg['daily']['max_items']:raise budget.BudgetExhausted('daily item quota reached')
                    daily['items']+=1;q.save()
                    if rules is None:
                        robots=getter('https://create.roblox.com/robots.txt',retries=0)
                        rules=RobotFileParser();rules.parse(robots.splitlines())
                    for url in recipe['urls']:
                        cache=root/'output'/'cache'/'factory_v9'/(hashlib.sha256(url.encode()).hexdigest()+'.md')
                        from agent.obsidian import safe_path
                        cache=safe_path(root,cache.relative_to(root).as_posix())
                        if cache.is_symlink():raise ValueError('symlink source cache refused')
                        if cache.exists():
                            if cache.stat().st_size>200000:raise ValueError('oversized cache')
                            documents[url]=cache.read_text(encoding='utf-8');continue
                        if state['attempts'].get(url,0)>=cfg['max_attempts']:raise ValueError('source attempt limit reached')
                        if not rules.can_fetch(providers.USER_AGENT,url):raise ValueError('robots policy refused source')
                        budget.fetch_attempt();state['attempts'][url]=state['attempts'].get(url,0)+1
                        atomic_write(state_path,json.dumps(state,indent=2)+'\n')
                        documents[url]=getter(url,accept='text/markdown,text/plain',retries=0)
                        if len(documents[url].encode('utf-8'))>200000:raise ValueError('source too large')
                        atomic_write(cache,documents[url])
                        budget.pause(.5)
                    note=write_candidate(root,recipe,documents)
                    result['items'].append({'task':recipe['task'],**note});stagnant=0
                except Exception as e:
                    result['errors'].append(f'{type(e).__name__}: {e}');result['stop_reason']='budget' if isinstance(e,budget.BudgetExhausted) else 'error'
                    break
        result['http_calls']=guard.http_calls
        result['stop_reason']=result['stop_reason'] or 'completed'
        atomic_write(root/'output'/'factory_last_run.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
