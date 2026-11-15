"""V2 evidence-first enrichment. No LLM, paid API, or fabricated conclusions.

Untrusted external content is DATA only. No instructions from pages are executed.
"""
from __future__ import annotations
import json, re, html, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, quote
from urllib.request import Request, urlopen

MAX_BYTES = 450_000
USER_AGENT = 'VDNResearchAgent/2.0 (educational research; GitHub repository issues)'

class Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript') and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def strip_html(value):
    p=Plain(); p.feed(str(value or ''))
    return re.sub(r'\s+', ' ', html.unescape(' '.join(p.parts))).strip()

def api_json(url):
    # Hard allowlist; never fetch arbitrary URLs from search results.
    host=urlparse(url).hostname
    if host not in ('devforum.roblox.com','api.github.com'):
        raise ValueError('Host not allowed')
    req=Request(url,headers={'User-Agent':USER_AGENT,'Accept':'application/vnd.github+json'})
    with urlopen(req,timeout=15) as r:
        if urlparse(r.geturl()).hostname not in ('devforum.roblox.com','api.github.com'):
            raise ValueError('Redirected outside allowlist')
        if int(r.headers.get('Content-Length','0'))>MAX_BYTES: raise ValueError('Too large')
        raw=r.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ValueError('Too large')
    return json.loads(raw)

def read_evidence(url):
    """Read a limited amount of public content from supported providers."""
    p=urlparse(url)
    if p.hostname=='devforum.roblox.com':
        m=re.match(r'^/t/(?:[^/]+/)?(\d+)(?:/|$)',p.path)
        if not m: raise ValueError('Unsupported DevForum URL')
        data=api_json('https://devforum.roblox.com/t/'+m.group(1)+'.json')
        posts=data.get('post_stream',{}).get('posts',[])[:5]
        texts=[strip_html(post.get('cooked','')) for post in posts]
        return {'provider':'DevForum','title':str(data.get('title',''))[:200],
                'text':'\n'.join(t[:4500] for t in texts)[:15000], 'posts_read':len(posts)}
    if p.hostname=='github.com':
        m=re.match(r'^/([^/]+)/([^/]+)(?:/|$)',p.path)
        if not m: raise ValueError('Unsupported GitHub URL')
        owner,repo=m.groups()
        if not re.fullmatch(r'[\w.-]{1,100}',owner) or not re.fullmatch(r'[\w.-]{1,100}',repo): raise ValueError('Invalid repo')
        data=api_json(f'https://api.github.com/repos/{owner}/{repo}')
        return {'provider':'GitHub','title':str(data.get('full_name','')),
                'text':str(data.get('description') or '')[:2000]+'\nTopics: '+', '.join(data.get('topics',[])[:20]),
                'posts_read':0}
    raise ValueError('Unsupported provider')

KEYWORDS={'alpha':'transparence / alpha','surfaceappearance':'SurfaceAppearance',
          'normal':'normales / normal map','atlas':'atlas de textures',
          'baking':'baking','lod':'LOD','mesh':'maillage',
          'performance':'performance','lighting':'éclairage','shadow':'ombres',
          'snow':'neige','foliage':'feuillage','animation':'animation',
          'collision':'collisions','texture':'textures','uv':'UV'}

def extract_facts(evidence):
    text=evidence['text']
    sentences=re.split(r'(?<=[.!?])\s+|\n+',text)
    selected=[]
    for s in sentences:
        s=re.sub(r'\s+',' ',s).strip()
        if 45<=len(s)<=450 and any(re.search(r'\b'+re.escape(k)+r'\b',s,re.I) for k in KEYWORDS):
            if s not in selected: selected.append(s)
        if len(selected)>=6: break
    return selected

def followup_questions(title,text):
    hay=(title+' '+text).lower()
    found=[v for k,v in KEYWORDS.items() if re.search(r'\b'+re.escape(k)+r'\b',hay)]
    return [f'Quelles sont les contraintes Roblox et les paramètres testables pour {x} ?' for x in dict.fromkeys(found[:3])]

def enrich_note(path, pause=0):
    body=path.read_text(encoding='utf-8')
    if '\n## Analyse V2' in body: return 'already'
    match=re.search(r'\*\*Source :\*\* \[[^]]+\]\((https://[^)]+)\)',body)
    if not match: return 'no_url'
    url=match.group(1)
    try:
        evidence=read_evidence(url)
        facts=extract_facts(evidence)
        questions=followup_questions(evidence['title'],evidence['text'])
        lines=['\n## Analyse V2 — lecture partielle de la source',
               '\n**Statut :** extrait source consulté ; conclusions non validées dans Roblox.',
               f"\n**Contenu accessible :** {evidence['provider']} ; {evidence['posts_read']} publication(s) examinée(s).",
               '\n### Passages techniques repérés (citations à contrôler dans la source)']
        lines += ['\n- '+f.replace('`','\\`').replace('<','&lt;') for f in facts] if facts else ['\nAucun passage technique précis extrait automatiquement.']
        lines += ['\n### Questions à approfondir']
        lines += ['\n- '+q for q in questions] if questions else ['\nLecture humaine nécessaire pour définir les questions.']
        lines += ['\n### Limites et validation','\n- Lecture automatique limitée : pas une revue exhaustive de la discussion.',
                  '\n- Aucune solution technique n’est déclarée confirmée.',
                  '\n- Les expériences Blender/Roblox Player restent à effectuer.',
                  '\n- Les extraits sont des indices, pas des instructions garanties.']
        path.write_text(body+'\n'.join(lines)+'\n',encoding='utf-8')
        status='enriched'
    except Exception as exc:
        # Mark the attempt without preventing a future retry.
        status=f'{type(exc).__name__}: {str(exc)[:100]}'
    if pause: time.sleep(pause)
    return status

def run(root:Path,max_notes=3,pause=1.0):
    paths=sorted((root/'knowledge').glob('*/*.md'))
    candidates=[p for p in paths if '\n## Analyse V2' not in p.read_text(encoding='utf-8')]
    results=[]
    for p in candidates[:max_notes]:
        results.append({'file':str(p.relative_to(root)), 'result':enrich_note(p,pause)})
    out=root/'output'/'last_analysis.json'; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'processed':len(results),'results':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(out.read_text(encoding='utf-8'))
    return results

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--max-notes',type=int,default=3); p.add_argument('--pause',type=float,default=1)
    a=p.parse_args()
    if not 1<=a.max_notes<=10 or a.pause<0: p.error('Invalid limits')
    run(Path(__file__).resolve().parents[1],a.max_notes,a.pause)
