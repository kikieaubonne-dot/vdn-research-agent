"""Operational gaps: separate evidence dimensions and explicit production priorities."""
import datetime as dt
import json
from pathlib import Path
import re

from agent.corpus import scan_notes
from agent.engine import evidence, compatibility, source_steps
from agent.knowledge import dump_frontmatter,legacy_evidence
from agent.text import tokens


def inventory(root, as_of=None):
    root=Path(root);as_of=as_of or dt.date.today()
    config=json.loads((root/'config'/'production_v9.json').read_text(encoding='utf-8'))
    diagnostics=[];notes=[]
    for note in scan_notes(root,diagnostics):
        text=dump_frontmatter({k:v for k,v in note.items() if not k.startswith('_')})+'\n'+note['_body']
        e=evidence(text);c=compatibility(text)
        try:age=(as_of-dt.date.fromisoformat(str(note.get('accessed',''))[:10])).days
        except ValueError:age=None
        proposed_protocol='## Protocole de reproduction proposé, non exécuté' in note['_body']
        dimensions={'relevance':'task-dependent','source_quality':{'tier_prior':note.get('source_tier'),'truth_verified':False},
                    'freshness':{'collection_age_days':age,'potentially_stale':age is not None and age>365,'source_version_verified':False},
                    'compatibility':c,'coverage':{'missing_fields':e['gaps']},
                    'reproducibility':'proposed_not_executed' if proposed_protocol else 'missing' if 'reproducibility' in e['gaps'] else 'protocol_present_not_executed',
                    'verifiability':'references_present' if note.get('sources') else 'missing_sources',
                    'operational_utility':'candidate_steps' if source_steps(text) else 'insufficient_steps',
                    'uncertainty':{'version_unknown':note.get('engine_version','inconnue') in ('inconnue','unknown',''),
                                   'contested':e['level']=='contestee','verification_required':True}}
        source_text=' '.join(re.findall(r'^>\s*«\s*(.+?)\s*»\s*$',note['_body'],re.M)) or legacy_evidence(note['_body'])
        notes.append({'id':note['id'],'path':note['_path'],'title':note.get('title',''),'sources':note.get('sources',[]),
                      'dimensions':dimensions,'_terms':set(tokens(str(note.get('title',''))+' '+source_text))})
    tasks=[]
    for task in config['tasks']:
        anchors=set(tokens(' '.join(task['anchors'])))
        matches=[n for n in notes if n['_terms']&anchors]
        gaps=[]
        if not matches:gaps.append('no_task_specific_reference')
        if not any(n['dimensions']['operational_utility']=='candidate_steps' for n in matches):gaps.append('no_candidate_instructions')
        for field in ('prerequisites','reproducibility','constraints'):
            absent=(not matches or all(n['dimensions']['reproducibility']=='missing' for n in matches)) if field=='reproducibility' else (not matches or all(field in n['dimensions']['coverage']['missing_fields'] for n in matches))
            if absent:gaps.append('missing_'+field)
        if not matches or all(n['dimensions']['uncertainty']['version_unknown'] for n in matches):gaps.append('version_unverified')
        gaps.append('not_reproduced_in_project')
        tasks.append({**task,'references':[n['id'] for n in matches],'gaps':gaps,
                      'targeted_query':task['query'],'ranking_reason':f"production P{task['priority']}, impact {task['impact']}; {len(gaps)} unresolved dimensions; no probability inferred"})
    tasks.sort(key=lambda t:(t['priority'],-len(t['gaps']),t['id']))
    for n in notes:n.pop('_terms')
    return {'schema':'vdn.gaps/9','as_of':as_of.isoformat(),'target_date':config['target_date'],
            'policy':'production priority first, then number of missing dimensions; engineering priorities separate',
            'notes':notes,'tasks':tasks,'diagnostics':diagnostics}


def pages(root, report=None):
    report=report or inventory(root)
    by_id={n['id']:n for n in report['notes']}
    def link(n):
        return '[['+str(Path(n['path']).relative_to('knowledge').with_suffix('')).replace('\\','/')+']]'
    home=['# Éponge — accueil opérationnel','','[[ _VDN-Lacunes | Recherches à faire ]]'.replace(' ','') ,'',
          'Les originaux sont conservés. Toutes les procédures restent candidates tant qu’aucune revue de preuve ne les valide.','']
    gaps=['# Lacunes prioritaires','','Classement de production, pas un score de vérité.','']
    for t in report['tasks']:
        home += [f"## P{t['priority']} — {t['need']}",'']
        gaps += [f"## P{t['priority']} — {t['need']}",f"- Recherche ciblée : `{t['targeted_query']}`",
                 '- Lacunes : '+', '.join(t['gaps']),'- Validation proposée, non exécutée : '+t['validation']]
        for nid in t['references']:
            if nid in by_id:
                relation=f"- Documenté par : {link(by_id[nid])}"
                home.append(relation);gaps.append(relation)
        home.append('');gaps.append('')
    return {'knowledge/_VDN-Accueil.md':'\n'.join(home)+'\n','knowledge/_VDN-Lacunes.md':'\n'.join(gaps)+'\n'}
