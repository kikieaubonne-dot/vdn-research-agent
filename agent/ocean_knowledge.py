"""Source-grounded candidates. Quotes are evidence, project steps are proposals."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import time
from agent import knowledge
from agent.corpus import scan_notes,read_text,library_path
from agent.lab_store import clean_json
from agent.storage import atomic_write
from agent.text import tokens,fold
from agent.ocean_plan import FACETS,facet_for

STATES=('DISCOVERED','EXTRACTED','SYNTHESIZED','SOURCE_SUPPORTED','EXPERIMENTALLY_TESTED','HUMAN_REVIEWED','DISPUTED','OUTDATED')
PROJECT_METHODS={
 'cards':['Construire deux copies de même silhouette : géométrie et cartes de feuillage ; conserver les exports séparés.',
          'Consigner atlas, UV, normales et mode de transparence réellement disponibles ; vérifier chaque option dans la version Studio installée.',
          'Comparer contours, chevauchements, ombres et changements à distance sous la même lampe torche ; photographier les défauts.'],
 'geometry':['Comparer les silhouettes du tronc et des étages de branches depuis les vues de gameplay, avant les micro-détails.',
             'Mesurer les triangles et dimensions des copies avec Blender ; garder la même échelle et le même import.',
             'Tester le même parcours au pied des arbres ; distinguer défaut visuel et blocage physique.'],
 'materials':['Inventorier les cartes PBR effectivement fournies et les propriétés documentées ; signaler les textures manquantes.',
              'Comparer le même arbre avec un matériau témoin et les textures candidates, sans changer caméra ni lumière.',
              'Capturer les surfaces éclairées et à l’ombre ; examiner coutures, normales et transparence séparément.'],
 'snow':['Préparer deux copies de branche : neige comme géométrie et représentation alternative autorisée par les sources.',
         'Documenter les intersections neige/aiguilles et la continuité de silhouette ; aucune compatibilité de shader n’est présumée.',
         'Comparer la lecture de nuit et le coût mesuré ; conserver les cas où une méthode échoue.'],
 'ground':['Comparer un terrain et une petite surface mesh témoin, avec la même pente et le même chemin de déplacement.',
           'Tester les empreintes sur chaque représentation dans une copie ; relever persistance, répétition et défauts de raccord.',
           'Vérifier les contacts du joueur et la lisibilité au faisceau avant toute généralisation à la forêt.'],
 'night':['Fixer caméra et exposition de test ; conserver une scène témoin sans brouillard pour isoler son effet.',
          'Comparer la lecture des silhouettes et du manoir avec les réglages réellement disponibles ; ne pas copier un preset Unreal.',
          'Capturer les mêmes positions et les zones cachées par le brouillard ; traiter l’ambiance comme jugement humain.'],
 'flashlight':['Monter une lampe de test dans un lieu séparé et consigner les propriétés SpotLight documentées, sans valeur optimale supposée.',
               'Comparer les mêmes troncs, feuillages et sols avec ombres activées/désactivées seulement si l’option est disponible.',
               'Mesurer les trames sur l’appareil cible et photographier les bords du faisceau ; ne pas confondre Heartbeat et FPS rendu.'],
 'wind':['Conserver un arbre statique témoin et une variante animée dont le rig est documenté.',
         'Vérifier la séparation tronc/branches, les poids et la pose de repos dans les versions Blender et Studio réelles.',
         'Comparer mouvements, collisions et coût mesuré à plusieurs distances ; consigner tout défaut d’import ou de déformation.'],
 'performance':['Fixer un chemin de déplacement reproductible et consigner densité, instances, matériaux et réglages de streaming.',
                'Modifier un seul facteur par variante : densité, géométrie ou stratégie de distance ; conserver les autres contrôles.',
                'Utiliser les outils de profilage Roblox sur l’appareil cible ; joindre les mesures brutes et les moments de blocage du contrôleur.'],
 'export':['Exporter une copie de chaque asset, avec unités, transformations, normales et options FBX consignées.',
           'Comparer dimensions, pose de repos et matériaux avant/après import ; vérifier explicitement Blender 5.2 côté utilisateur.',
           'Garder l’export précédent et le journal d’import pour attribuer les différences au pipeline, sans modifier les originaux.'],
 'comparison':['Construire un tableau des mécanismes Unreal cités et des capacités Roblox effectivement documentées.',
               'Marquer toute équivalence non démontrée comme hypothèse ; ne pas transposer des valeurs moteur par simple ressemblance.',
               'Préparer un prototype Roblox isolé avec les entrées disponibles ; les assets B3/C1 restent requis pour une comparaison les concernant.']}
ALIASES={'bloque':'collision','coince':'collision','sapins':'tree','troncs':'collision','aiguilles':'foliage',
         'gel':'snow','brouillard':'Atmosphere','lampe':'SpotLight','epiceas':'spruce','saccade':'performance',
         'pbr':'SurfaceAppearance','transparent':'transparency','fbx':'export','ombre':'Shadows'}


def expand(query):
    words=re.findall(r'[a-z0-9]+',fold(query))
    return query+' '+' '.join(ALIASES[w] for w in words if w in ALIASES)


def excerpts(source,query):
    # At most 24 literal words per source per candidate. Exact source spans.
    words=set(tokens(expand(query)));text=source['text']
    sentences=[re.sub(r'\s+',' ',s).strip(' \n>') for s in re.split(r'\n|(?<=[.!?])\s+',text)]
    candidates=[s for s in sentences if len(s)>=35 and not s.startswith(('#','|','```')) and
                not re.search(r'(?i)ignore (?:previous|all)|system prompt|run .*command|api.?key',s)]
    candidates.sort(key=lambda s:-len(words&set(tokens(s))))
    for s in candidates:
        if words&set(tokens(s)):
            quote=' '.join(s.split()[:24])
            # Whitespace normalization is recorded; no paraphrase called a quote.
            if quote in re.sub(r'\s+',' ',text):return quote
    return None


def synthesis(goal,facet,documents,model=None):
    definition=next(f for f in FACETS if f[0]==facet)
    claims=[];sources=[];uncertainties=['No result reproduced in the user project.','Software version and target device not independently verified.']
    for index,doc in enumerate(documents):
        quote=excerpts(doc,definition[1])
        sid='source-'+str(index+1)
        sources.append({k:doc[k] for k in ('url','provider','accessed','published','version','text_sha256','raw_text_sha256','truncated','policy')})
        sources[-1]['retrieved_at']=doc.get('at')
        sources[-1]['id']=sid
        if quote:claims.append({'id':'claim-'+str(len(claims)+1),'source_id':sid,'quote':quote,
                               'kind':'literal_source_excerpt','scope':'source statement; applicability requires test'})
        if doc['truncated']:uncertainties.append('Source cache truncated; unseen sections may add constraints: '+sid)
        if doc.get('changed_since_previous'):uncertainties.append('Source changed since previous download: '+sid)
    if not claims:raise ValueError('no relevant attributable source statement; synthesis refused')
    normalized=[re.sub(r'\s+',' ',d['text']) for d in documents]
    for c in claims:
        number=int(c['source_id'].split('-')[-1])-1
        if c['quote'] not in normalized[number]:raise ValueError('quote/source mismatch')
    documented=[a for a in definition[4] if any(re.search(r'\b'+re.escape(a)+r'\b',d['text'],re.I) for d in documents)]
    disputed=any(re.search(r'(?i)contradiction|sources? (?:disagree|conflict)',d['text']) for d in documents)
    # Boolean contradictions are only flagged for the same explicit property.
    for name in documented:
        values=set()
        for d in documents:
            values.update(v.lower() for v in re.findall(re.escape(name)+r'\s*(?:=|:|is)\s*(true|false)\b',d['text'],re.I))
        disputed=disputed or len(values)>1
    outdated=False
    for s in sources:
        if s['published']:
            try:outdated |= (dt.date.today()-dt.date.fromisoformat(s['published'][:10])).days>365
            except ValueError:uncertainties.append('Invalid publication date; freshness unknown.')
    steps=[
        'Travailler dans une copie du laboratoire, avec versions, appareil, caméra et assets consignés.',
        'Inspecter les éléments documentés : '+(', '.join(documented) or 'aucun paramètre suffisamment documenté ; compléter la recherche')+'.',
        'Préparer deux variantes ne différant que par la méthode étudiée ; consigner les valeurs réellement choisies.',
        'Répéter le protocole sous les mêmes conditions et conserver mesures, captures et échecs.',
        'Comparer les limites observées avant réutilisation ; conserver la variante initiale pour rollback.']
    alternatives=[]
    if facet=='collision':
        steps[1]='Inspecter les troncs, branches, décor et MeshParts ; relever les propriétés documentées '+', '.join(documented)+', sans présumer de leur valeur optimale.'
        steps.insert(2,'Proposition à tester : séparer la géométrie visuelle des volumes de collision simples, en conservant le comportement initial pour comparaison.')
        steps.insert(3,'Tester le contrôleur réel entre les troncs, sur les pentes et près des branches ; consigner les blocages et paramètres de collision de chaque variante.')
        alternatives=['Proposition non validée : comparer collisions du mesh et proxies simples séparés ; mesurer le compromis précision/coût.',
                      'Ne pas désactiver une collision sur la seule base de cette fiche ; vérifier les besoins de gameplay.']
    elif facet=='comparison':
        uncertainties.append('Unreal techniques are references, not evidence of Roblox support.')
    if facet in PROJECT_METHODS:
        steps[2:2]=PROJECT_METHODS[facet]
        alternatives.append('Proposition de comparaison contrôlée ; aucun résultat ou compromis optimal n’est établi par cette fiche.')
    hypotheses=[];model_steps=[];model_state='not_used'
    if model:
        model_state=model.get('state','unavailable')
        if model_state=='model_claims':
            payload=model.get('claims',{})
            # Only a literal evidence selection may become a source-supported fact.
            evidence=payload.get('evidence',[]);questions=payload.get('questions',[])
            if not isinstance(evidence,list) or not isinstance(questions,list):
                uncertainties.append('Invalid model output schema; ignored.');evidence=[];questions=[]
            for chosen in evidence[:4]:
                if not isinstance(chosen,dict) or not any(chosen.get('source_id')==c['source_id'] and chosen.get('quote')==c['quote'] for c in claims):
                    uncertainties.append('Model evidence rejected: no exact source match.')
            for question in questions[:4]:
                if isinstance(question,str) and len(question)<=300 and not re.search(r'\d',question):hypotheses.append({'text':question,'kind':'unverified_model_question'})
            proposals=payload.get('proposals',[])
            if not isinstance(proposals,list):proposals=[]
            known_ids={s['id'] for s in sources}
            for proposal in proposals[:6]:
                if not isinstance(proposal,dict):continue
                text=proposal.get('text');ids=proposal.get('source_ids')
                if not isinstance(text,str) or not 1<=len(text)<=500 or not isinstance(ids,list) or not ids or not set(ids)<=known_ids:continue
                if re.search(r'\d|(?i:ignore previous|run .*command|powershell|subprocess|api.?key)',text):
                    uncertainties.append('Model procedure rejected: unsupported number or executable/instruction pattern.');continue
                model_steps.append({'text':text,'source_ids':ids,'origin':'model_proposal_not_entailed_by_quote','verified':False})
    flags=['DISCOVERED','EXTRACTED','SYNTHESIZED','SOURCE_SUPPORTED']
    if disputed:flags.append('DISPUTED');uncertainties.append('Potential or explicit contradiction flag; compare conditions and versions before choosing an interpretation.')
    if outdated:flags.append('OUTDATED')
    fingerprint=hashlib.sha256(clean_json({'facet':facet,'source_text_hashes':sorted(s['text_sha256'] for s in sources),'quotes':[c['quote'] for c in claims]}).encode('utf-8')).hexdigest()
    result={'schema':'vdn.knowledge/11','id':'vdn-ocean-'+fingerprint[:20],'facet':facet,
            'title':definition[1]+' — application à la forêt Roblox','problem':goal,'context':'VDN isolated forest laboratory',
            'summary':'Les sources citées documentent '+(', '.join(documented) or 'les extraits ci-dessous')+'. Pour la forêt Roblox, la décision à préparer concerne '+
                      ('les collisions des troncs et branches, les volumes simples séparés et le passage du contrôleur.' if facet=='collision' else facet+'.')+
                      ' La méthode proposée reste à comparer dans le laboratoire ; aucune valeur optimale ou compatibilité de version n’est déduite.',
            'states':flags,'sources':sources,'claims':claims,'documented_tokens':documented,
            'parameters':'Only literal source tokens are documented; no numeric recommendation inferred.',
            'procedure':[{'text':s,'origin':'engineering_proposal','verified':False} for s in steps],
            'alternatives':alternatives,'hypotheses':hypotheses,'uncertainties':list(dict.fromkeys(uncertainties)),
            'prerequisites':['isolated asset copies','recorded software versions','target device and controller'],
            'validation':['Fix comparison controls before running.','Repeat traversal and rendering checks; record raw measurements.',
                          'Compare movement blockages, collision accuracy and measured frame cost; no FPS assumed.'],
            'confidence_reason':'Literal attribution checked mechanically; engineering correctness and project applicability unverified.',
            'model_state':model_state,'model_proposed_steps':model_steps,'related_notes':[],'experiment_ids':[],'truth_verified':False}
    clean_json(result);return result


def render(card):
    meta={'id':card['id'],'title':card['title'],'domain':'ocean','subdomain':card['facet'],'status':'candidat',
          'schema':'vdn.knowledge/11','ocean_states':card['states'],'source_tier':1 if all(s['provider'] in ('roblox','blender','unreal') for s in card['sources']) else 4,
          'sources':[s['url'] for s in card['sources']],'accessed':max(s['accessed'] for s in card['sources']),
          'engine_version':'unknown','tested_in_studio':'non','review_status':'pending','tags':['vdn','ocean','candidate',card['facet']]}
    lines=['# '+card['title'],'','## Problème',card['problem'],'','## Contexte',card['context'],'',
           '## Résumé technique',card['summary'],'','## Extraits justificatifs']
    for claim in card['claims']:
        source=next(s for s in card['sources'] if s['id']==claim['source_id'])
        lines += ['', '> « '+claim['quote']+' »','> — [source]('+source['url']+'), consultée le '+source['accessed']]
    for title,key in (('Prérequis','prerequisites'),('Procédure candidate — propositions non validées','procedure'),('Alternatives et compromis','alternatives'),('Limites et incertitudes','uncertainties'),('Protocole de reproduction proposé, non exécuté','validation')):
        lines += ['','## '+title]+['- '+(s['text'] if isinstance(s,dict) else s) for s in card[key]]
    lines += ['','## Paramètres documentés',card['parameters'],'Tokens présents : '+', '.join(card['documented_tokens']),
              '','## Connaissances associées']
    lines += ['- [['+p+']]' for p in card.get('related_note_paths',[])] or ['Aucune relation supplémentaire confirmée.']
    lines += ['','## Expériences associées','Identifiants : '+(', '.join(card['experiment_ids']) or 'aucune expérience liée ; protocole proposé seulement'),
              '','## Retour arrière','Conserver et restaurer les copies initiales ; aucune édition du jeu de production.',
              '','## Données structurées Océan','```json',clean_json(card),'```','']
    return knowledge.dump_frontmatter(meta)+'\n'+'\n'.join(lines)


def write_card(root,card,web):
    root=Path(root).resolve()
    path=library_path(root,'knowledge/ocean/'+card['id']+'.md')
    if path.exists():
        if not any(c['id']==card['id'] for c in cards(root)):raise ValueError('existing candidate is corrupt; inspect/archive explicitly, never overwrite')
        return {'action':'duplicate','id':card['id'],'path':path.relative_to(root).as_posix()}
    related=set(card.get('related_notes',[]))
    card['related_note_paths']=[n['_path'].removeprefix('knowledge/').removesuffix('.md') for n in scan_notes(root) if n['id'] in related]
    text=render(card);web.storage_check(len(text.encode('utf-8')))
    atomic_write(path,text,create_only=True)
    return {'action':'created','id':card['id'],'path':path.relative_to(root).as_posix(),'status':'candidat'}


def cards(root,diagnostics=None):
    diagnostics=[] if diagnostics is None else diagnostics
    result=[]
    for n in scan_notes(root,diagnostics):
        if n.get('schema')!='vdn.knowledge/11':continue
        match=re.search(r'^## Données structurées Océan\s*\n```json\n(.*?)\n```\s*$',n['_body'],re.S|re.M)
        if not match:diagnostics.append({'path':n['_path'],'error':'missing Ocean JSON block'});continue
        try:
            value=json.loads(match.group(1));clean_json(value)
            if value.get('id')!=n['id'] or value.get('schema')!='vdn.knowledge/11':raise ValueError('Ocean note identity corrupt')
            if not isinstance(value['states'],list) or not set(value['states'])<=set(STATES):raise ValueError('invalid knowledge states')
            fingerprint=hashlib.sha256(clean_json({'facet':value['facet'],'source_text_hashes':sorted(s['text_sha256'] for s in value['sources']),
                                                  'quotes':[c['quote'] for c in value['claims']]}).encode('utf-8')).hexdigest()
            if value['id']!='vdn-ocean-'+fingerprint[:20]:raise ValueError('Ocean evidence identity mismatch')
            result.append({**value,'path':n['_path']})
        except (ValueError,KeyError,TypeError) as exc:
            # Isolate the corrupt candidate; never overwrite it or poison others.
            diagnostics.append({'path':n['_path'],'error':str(exc)[:200]})
            continue
    return result


def search(root,query,limit=5,diagnostics=None):
    from agent.engine import string,integer
    string(query,'query');integer(limit,'limit',1,10)
    words=set(tokens(expand(query)));ranked=[]
    for card in cards(root,diagnostics):
        corpus=card['title']+' '+card['facet']+' '+' '.join(c['quote'] for c in card['claims'])
        matched=words&set(tokens(corpus));score=len(matched)
        if not score:continue
        score-=int('OUTDATED' in card['states'])+int('DISPUTED' in card['states'])
        ranked.append((score,card))
    ranked.sort(key=lambda r:(-r[0],r[1]['id']))
    selected=[];remaining=[];seen_sources=set()
    for entry in ranked:
        urls={s['url'] for s in entry[1]['sources']}
        if urls-seen_sources:selected.append(entry);seen_sources|=urls
        else:remaining.append(entry)
    ranked=selected+remaining
    return [{'id':c['id'],'title':c['title'],'facet':c['facet'],'score':s,'states':c['states'],
             'sources':[v['url'] for v in c['sources']],'claims':c['claims'][:2],
             'uncertainties':c['uncertainties'][:3],'source_refresh_needed':refresh_needed(root,c),'truth_verified':False} for s,c in ranked[:limit]]


def fresh(root,card,ttl):
    from agent.obsidian import safe_path
    root=Path(root).resolve()
    latest={};folder=safe_path(root,'lab/ocean/sources')
    paths=list(folder.glob('*.json')) if folder.exists() else []
    if len(paths)>1000:raise ValueError('source cache count limit exceeded')
    for p in paths:
        safe_path(root,p.relative_to(Path(root).resolve()).as_posix())
        if p.stat().st_size>64000:raise ValueError('oversized source cache')
        data=json.loads(p.read_text(encoding='utf-8'));old=latest.get(data['url'])
        if old is None or data['at']>old['at']:latest[data['url']]=data
    for source in card['sources']:
        checked=latest.get(source['url'])
        if checked and checked['text_sha256']!=source['text_sha256']:return False
        stamp=checked['at'] if checked else source.get('retrieved_at')
        if stamp is None:
            try:stamp=dt.datetime.fromisoformat(source['accessed']).replace(tzinfo=dt.timezone.utc).timestamp()
            except ValueError:return False
        if time.time()-stamp>ttl:return False
    return True


def refresh_needed(root,card):
    from agent.ocean_web import settings
    try:
        ttl=settings(root)['cache_ttl_s'] if (Path(root)/'config/ocean.json').exists() else 86400
        return not fresh(root,card,ttl)
    except (ValueError,OSError,KeyError,TypeError):return None


def legacy_view(root):
    # Read-only compatibility view. No automatic experiment/human-review promotion.
    return [{'id':n['id'],'legacy_status':n.get('status'),'states':['DISPUTED'] if n.get('status')=='contestee' else ['OUTDATED'] if n.get('status')=='obsolete' else ['DISCOVERED'],
             'claimed_test':n.get('tested_in_studio'),'truth_verified':False,'path':n['_path']} for n in scan_notes(root) if n.get('schema')!='vdn.knowledge/11']
