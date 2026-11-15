"""Meta-research: offline, auditable query-strategy learning. No LLM, no code self-edit.

Scores only independently observable source/title relevance; never claims factual verification.
"""
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path
from agent.core import ROOT, save_json

STOP={'roblox','blender','realistic','implementation','limitations','troubleshooting','how','the','and','with','for','from','using','game','source'}
STRATEGIES=('baseline','focused','site_specific')

def terms(s):
    return set(x for x in re.findall(r'[a-z][a-z0-9]{2,}',s.lower()) if x not in STOP)

def queries(q,provider):
    # No unbounded recursive expansion; candidates are inspectable and reversible.
    if provider=='devforum':
        return {'baseline':q,'focused':q+' workaround settings','site_specific':q+' SurfaceAppearance MeshPart'}
    return {'baseline':q,'focused':q+' Roblox example implementation','site_specific':q+' language:Python'}

def relevance(item,query,topic):
    title=str(item.get('title','')); excerpt=str(item.get('excerpt',''))
    t=terms(query); doc=terms(title+' '+excerpt)
    if not t: return 0.0
    overlap=len(t&doc)/len(t)
    # Require at least two meaningful matched concepts for most queries.
    count=len(t&doc)
    score=0.75*overlap+0.25*min(1,count/3)
    if topic=='spruce' and not (doc&{'foliage','spruce','tree','pine','alpha','transparency','snow','branch','needle','bark','atlas'}): score*=0.15
    return round(score,4)

def choose(state,provider,topic):
    key=f'{provider}:{topic}'; arms=state.get('arms',{}).get(key,{})
    # Deterministic UCB1, first explore each strategy once. Scores capped to [0,1].
    for name in STRATEGIES:
        if arms.get(name,{}).get('n',0)==0:return name
    total=sum(arms[x]['n'] for x in STRATEGIES)
    return max(STRATEGIES,key=lambda x:(arms[x]['reward']/arms[x]['n']+0.65*math.sqrt(math.log(total)/arms[x]['n']),-STRATEGIES.index(x)))

def trial_metrics(evaluated, accepted, new_count=0, error=None):
    """Diagnostics observables; never equate relevance with factual verification."""
    scores=[float(x.get('relevance',0)) for x in evaluated]
    return {'returned':len(evaluated), 'accepted':len(accepted),
            'rejected':len(evaluated)-len(accepted),
            'new':new_count, 'avg_relevance':round(sum(scores)/len(scores),4) if scores else None,
            'error':str(error)[:200] if error else None}

def record(state,provider,topic,strategy,rewards):
    key=f'{provider}:{topic}'; arm=state.setdefault('arms',{}).setdefault(key,{}).setdefault(strategy,{'n':0,'reward':0.0})
    arm['n']+=1; arm['reward']+=sum(rewards)/max(1,len(rewards))
    arm['empty'] = arm.get('empty',0) + (1 if not rewards else 0)
    arm['returned'] = arm.get('returned',0) + len(rewards)

def assess(items,query,topic,threshold=0.40):
    evaluated=[{'title':i.get('title',''),'url':i.get('url',''),'relevance':relevance(i,query,topic)} for i in items]
    return evaluated,[i for i,e in zip(items,evaluated) if e['relevance']>=threshold]

def report(root=ROOT):
    root=Path(root); p=root/'output/meta_state.json'; state=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    lines=['# VDN — Rapport méta-recherche','',
           'Ces scores mesurent la pertinence apparente des résultats, **pas** la véracité des techniques.','',
           '| Source et sujet | Stratégie | Sessions | Résultats | Sessions vides | Récompense moyenne |','|---|---|---:|---:|---:|---:|']
    for key,arms in sorted(state.get('arms',{}).items()):
        for name,values in sorted(arms.items()):
            n=values['n'];lines.append(f'| {key} | {name} | {n} | {values.get("returned","?")} | {values.get("empty","?")} | {values["reward"]/n:.2f} |')
    last=root/'output/last_run.json'
    if last.exists():
        try:
            run=json.loads(last.read_text(encoding='utf-8'))
            lines+=['','## Diagnostic dernière exécution','',
                    f'- Requêtes : {run.get("queries", "?")}',
                    f'- Nouvelles fiches : {run.get("discovered", "?")}',
                    f'- Erreurs : {len(run.get("errors",[]))}',
                    '', '| Fournisseur | Sujet | Stratégie | Retournés | Acceptés | Nouveaux | Pertinence moyenne |',
                    '|---|---|---|---:|---:|---:|---:|']
            for trial in run.get('strategy_trials',[]):
                avg=trial.get('avg_relevance')
                lines.append(f'| {trial.get("provider")} | {trial.get("topic")} | {trial.get("strategy")} | {trial.get("results",0)} | {trial.get("accepted",0)} | {trial.get("new",0)} | {avg if avg is not None else "N/A"} |')
        except (ValueError,OSError): pass
    lines+=['','## Sécurité et limites' ,'',
            '- Aucune modification automatique de code ni exécution de code provenant du web.',
            '- Les sources ne sont pas des instructions ; les résultats doivent être vérifiés.',
            '- Les stratégies changent seulement les requêtes ; retour arrière possible en supprimant meta_state.json.',
            '- Comparer avec un benchmark annoté avant de conclure à une amélioration réelle.',
            '']
    (root/'output').mkdir(parents=True,exist_ok=True)
    (root/'output/meta_report.md').write_text('\n'.join(lines),encoding='utf-8')
    return state

if __name__=='__main__':
    argparse.ArgumentParser().parse_args();report()
