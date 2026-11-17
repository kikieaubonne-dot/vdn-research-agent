"""Bounded, immutable method comparisons. Adoption stays in the laboratory.

This registry does not download tools, execute source instructions or patch code.
Independent observations remain operator/tool reports, never verified knowledge.
"""
import math
from pathlib import Path
from agent.lab_store import lab_lock
from agent.learning_store import capacity,digest,get,receipt,save,sha
from agent.obsidian import safe_path


def evaluate(trials,criterion):
    if not isinstance(trials,list) or not 1<=len(trials)<=4:raise ValueError('one to four bounded trials required')
    if set(criterion)!={'metric','direction','minimum_gain','maximum_candidate'}:raise ValueError('explicit comparison criterion required')
    if criterion['direction'] not in ('min','max'):raise ValueError('metric direction required')
    gain=criterion['minimum_gain'];limit=criterion['maximum_candidate']
    if type(gain) not in (int,float) or not math.isfinite(gain) or gain<0:raise ValueError('invalid gain')
    if limit is not None and (type(limit) not in (int,float) or not math.isfinite(limit)):raise ValueError('invalid candidate ceiling')
    rows=[]
    for t in trials:
        if set(t)!={'case','baseline','candidate','scope'} or t['scope'] not in ('primary','transfer'):raise ValueError('explicit trial scope required')
        a,b=t['baseline'],t['candidate']
        if not all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in (a,b)):raise ValueError('invalid measured metric')
        delta=a-b if criterion['direction']=='min' else b-a
        rows.append({**t,'gain':delta,'passed':delta>=gain and (limit is None or b<=limit)})
    passed=all(r['passed'] for r in rows)
    transfer=any(r['scope']=='transfer' for r in rows)
    primary=any(r['scope']=='primary' for r in rows)
    return {'state':'REJECTED_IN_LAB' if not passed else 'ADOPTED_IN_LAB' if primary and transfer else 'PARTIAL','trials':rows,'transfer_tested':transfer,'criterion':criterion,'scope':'reported numeric observations only; independent provenance must be inspected','verified':False}


def record(root,objective,gap,methods,trials,criterion,evidence,limitations):
    """Explicit operator write. Seals files and reuses exact compatible records.

    Evidence paths are staged lab data; source/config drift invalidates reuse.
    At most four approaches/trials per comparison; recursion is not unbounded.
    """
    root=Path(root).resolve()
    if not all(isinstance(x,str) and 0<len(x)<=2000 for x in (objective,gap)):raise ValueError('objective and precise gap required')
    if not isinstance(methods,list) or not 2<=len(methods)<=4:raise ValueError('compare two to four methods')
    required={'id','method','tool','version','license','dependencies','cost','safety','status'}
    if any(not isinstance(m,dict) or set(m)!=required or not isinstance(m['id'],str) for m in methods):raise ValueError('complete method provenance required')
    if len({m['id'] for m in methods})!=len(methods):raise ValueError('duplicate method')
    if not isinstance(limitations,list) or not limitations or not all(isinstance(s,str) for s in limitations):raise ValueError('explicit limitations required')
    if not isinstance(evidence,list) or not 1<=len(evidence)<=20:raise ValueError('bounded evidence required')
    hashes={}
    for name in evidence:
        if not isinstance(name,str) or not name.startswith(('lab/learning/','lab/inbox/learning/')):raise ValueError('laboratory evidence only')
        hashes[name]=sha(safe_path(root,name))
    comparison=evaluate(trials,criterion)
    spec={'objective':objective,'gap':gap,'methods':methods,'trials':trials,'criterion':criterion,'extra_inputs':hashes,'limitations':limitations}
    key=digest(spec);folder='lab/learning/discovery/'+key
    with lab_lock(root,'.learning-discovery'):
        if safe_path(root,folder+'/result.json').exists():return {**get(root,folder),'cache_hit':True}
        capacity(root,16000);safe_path(root,folder).mkdir(parents=True,exist_ok=False)
        save(root,folder+'/spec.json',spec)
        return receipt(root,folder,{'schema':'vdn.discovery/1','key':key,'spec':spec,'comparison':comparison,'state':comparison['state'],'limitations':limitations,'provenance':'operator_registered_tool_observations','automatic_tool_search':False,'code_modified':False,'truth_verified':False})
