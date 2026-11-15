"""VDN V3: bounded evidence-first deepening, no paid services or LLM.
External content is untrusted evidence. Never execute external instructions.
"""
from __future__ import annotations
import argparse, datetime as dt, json, re, time, hashlib
from pathlib import Path
from urllib.parse import urlparse, quote
from urllib.request import Request, urlopen
from agent import analyzer
from agent.core import ROOT, save_json, safe_filename

MAX_READ=350_000
HEADERS={'User-Agent':'VDNResearchAgent/3.0 (noncommercial educational research)', 'Accept':'application/vnd.github+json'}
TOPIC_WEIGHTS={'spruce':10,'forest':10,'traversal':9,'character':8,'manor':7}
TECH=re.compile(r'(?i)\b(surfaceappearance|alphamode|normalmap|roughnessmap|colormap|meshpart|uv|atlas|lod|bake|baking|transparen(?:cy|t)|triangles?|vertex|vertices|skinn?ing|bones?|rigging|shadow|lighting|foliage|material|texture|performance|render|export|fbx|collision|geometry nodes|raycast|animation)\b')
DETAIL=re.compile(r'(?i)(\b\d+(?:[.,]\d+)?\s*(?:px|k|mb|ms|fps|triangles?|vertices|bones?|degrees?|°|%)\b|\b(?:set|enable|disable|change|use|export|import|bake|create|adjust|configure|fix|solution|workaround|steps?|parameter|setting|bug|issue|tested|reproduce)\b|[=:])')

def read_github_readme(url):
    p=urlparse(url); m=re.fullmatch(r'/([\w.-]+)/([\w.-]+?)/?',p.path)
    if p.hostname!='github.com' or not m: raise ValueError('Unsupported repository URL')
    owner,repo=m.groups(); api=f'https://api.github.com/repos/{owner}/{repo}/readme'
    req=Request(api,headers={**HEADERS,'Accept':'application/vnd.github.raw+json'})
    with urlopen(req,timeout=14) as response:
        if urlparse(response.geturl()).hostname not in ('api.github.com','raw.githubusercontent.com'): raise ValueError('Unsafe redirect')
        raw=response.read(MAX_READ+1)
        if len(raw)>MAX_READ: raise ValueError('README too large')
        return raw.decode('utf-8','replace')[:18000]

def evidence_for(url):
    p=urlparse(url)
    if p.hostname=='github.com':
        text=read_github_readme(url)
        return {'provider':'GitHub README','text':text,'posts_read':1}
    return analyzer.read_evidence(url)

def excerpts(text,limit=5):
    lines=re.split(r'(?<=[.!?])\s+|\n+',text)
    out=[]
    for line in lines:
        line=re.sub(r'\s+',' ',line).strip().replace('`','\`').replace('<','&lt;')
        if 45<=len(line)<=500 and TECH.search(line) and DETAIL.search(line) and line not in out:
            out.append(line)
        if len(out)>=limit: break
    return out

def note_url(body):
    m=re.search(r'\*\*Source :\*\* \[[^]]+\]\((https://[^)]+)\)',body)
    return m.group(1) if m else None

def topic_of(path): return path.parent.name

def question_for(topic, excerpt):
    terms=[]
    for m in TECH.finditer(excerpt):
        t=m.group(0).lower()
        if t not in terms: terms.append(t)
    t=terms[0] if terms else 'technique'
    return f'{topic} Roblox {t} implementation limitations troubleshooting'

def eligible(path, state):
    body=path.read_text(encoding='utf-8')
    if '## Analyse V3' in body: return False
    return bool(note_url(body))

def select_notes(root,state,max_notes):
    files=[p for p in (root/'knowledge').glob('*/*.md') if eligible(p,state)]
    # Fair round-robin across topics; prioritize game-critical topics; rotate per run.
    buckets={}
    for p in files: buckets.setdefault(topic_of(p),[]).append(p)
    for topic,arr in buckets.items():
        arr.sort(key=lambda p:(state.get('attempts',{}).get(str(p.relative_to(root)),0),p.name))
    order=sorted(buckets,key=lambda t:(-TOPIC_WEIGHTS.get(t,5),t))
    if order:
        offset=int(state.get('rotation',0))%len(order)
        order=order[offset:]+order[:offset]
    chosen=[]
    while len(chosen)<max_notes and any(buckets.values()):
        for topic in order:
            if buckets[topic]: chosen.append(buckets[topic].pop(0))
            if len(chosen)>=max_notes: break
    return chosen

def analyze(path,root,state):
    body=path.read_text(encoding='utf-8'); url=note_url(body)
    key=str(path.relative_to(root)); state.setdefault('attempts',{})[key]=state.get('attempts',{}).get(key,0)+1
    if not url: return {'file':key,'status':'no_url'}
    try:
        ev=evidence_for(url)
        found=excerpts(ev.get('text',''))
        if not found:
            # Do not mark empty analysis as enriched. Retry later, but not every run.
            state.setdefault('insufficient',{})[key]={'reason':'no actionable excerpt','last_attempt':dt.datetime.now(dt.timezone.utc).isoformat()}
            return {'file':key,'status':'insufficient_source','provider':ev['provider']}
        topic=topic_of(path)
        questions=[question_for(topic,x) for x in found[:3]]
        qlist=state.setdefault('questions',{})
        for q in questions:
            qid=hashlib.sha256(q.encode()).hexdigest()[:16]
            qlist.setdefault(qid,{'query':q,'topic':topic,'source':url,'status':'open'})
        section=['','## Analyse V3 — éléments techniques à vérifier','',
                 '**Statut :** passages candidats extraits de la source, **non validés** dans Roblox.','',
                 f'**Source lue :** {url}  ',f'**Contenu :** {ev["provider"]}  ',
                 f'**Passages candidats :** {len(found)}','','### Passages et paramètres repérés','']
        section += ['- '+x for x in found]
        section += ['','### Questions de recherche complémentaires','']+['- '+q for q in questions]
        section += ['','### Validation requise','','- [ ] Vérifier chaque passage dans la source complète','- [ ] Confirmer les limitations Roblox actuelles','- [ ] Tester dans Roblox Studio ET Roblox Player','- [ ] Mesurer qualité et performance','']
        path.write_text(body+'\n'.join(section),encoding='utf-8')
        return {'file':key,'status':'evidence_extracted','excerpts':len(found),'questions':len(questions)}
    except Exception as e:
        return {'file':key,'status':'read_error','error':f'{type(e).__name__}: {str(e)[:130]}'}

def run(root=ROOT,max_notes=12,pause=1):
    root=Path(root); statepath=root/'output/v3_state.json'
    state=json.loads(statepath.read_text(encoding='utf-8')) if statepath.exists() else {}
    selected=select_notes(root,state,max_notes); results=[]
    for p in selected:
        results.append(analyze(p,root,state))
        if pause: time.sleep(pause)
    state['rotation']=int(state.get('rotation',0))+1
    save_json(statepath,state)
    summary={'processed':len(results),'evidence_extracted':sum(x['status']=='evidence_extracted' for x in results),
             'insufficient':sum(x['status']=='insufficient_source' for x in results),
             'errors':sum(x['status']=='read_error' for x in results),'open_questions':len(state.get('questions',{})),'results':results}
    save_json(root/'output/v3_last_analysis.json',summary)
    lines=['# Rapport de recherche VDN V3','',f'Fiches examinées : {summary["processed"]}',
           f'Fiches avec extraits techniques candidats : {summary["evidence_extracted"]}',
           f'Sources insuffisantes : {summary["insufficient"]}',f'Erreurs de lecture : {summary["errors"]}',
           f'Questions ouvertes : {summary["open_questions"]}','','## Questions ouvertes','']
    for q in list(state.get('questions',{}).values())[-80:]:
        lines.append(f'- **{q["topic"]}** : {q["query"]} — {q["source"]}')
    (root/'output/v3_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2)); return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--max-notes',type=int,default=12);p.add_argument('--pause',type=float,default=1)
    a=p.parse_args()
    if not 1<=a.max_notes<=25 or a.pause<0: p.error('Invalid limits')
    run(max_notes=a.max_notes,pause=a.pause)
