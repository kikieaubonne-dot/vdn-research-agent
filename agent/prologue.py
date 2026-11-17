"""Project-specific production inventory and resumable prototype progression.

No Studio bridge or game execution. Narrative decisions come from project data.
"""
import argparse
import json
from pathlib import Path
import re
from agent.learning_store import digest,load,save
from agent.obsidian import safe_path
from agent.project import Bible


class Prologue:
    def __init__(self,root):
        self.root=Path(root).resolve();self.data=load(self.root,'project/prologue.json');self.bible=Bible(root)
        if self.data.get('schema')!='vdn.prologue-production/1':raise ValueError('invalid prologue schema')
        self.states={};self.resources={};scenes={s['id'] for s in self.data['scenes']}
        if len(scenes)!=6 or not 1<=len(self.data['resources'])<=60:raise ValueError('bounded complete scene inventory required')
        for state in self.data['states']:
            if state['id'] in self.states or state['scene'] not in scenes:raise ValueError('invalid state identity')
            if any(v not in ('walk','look','interact','sprint') for v in state['controls']) and state['scene']=='B':raise ValueError('first pursuit must not impose advanced movement')
            self.states[state['id']]=state
        for state in self.states.values():
            if state['next'] is not None and state['next'] not in self.states:raise ValueError('unknown next state')
        seen=set();current=self.data['initial']
        while current is not None:
            if current in seen or current not in self.states:raise ValueError('cyclic or unknown progression')
            seen.add(current);current=self.states[current]['next']
        if seen!=set(self.states):raise ValueError('unreachable progression state')
        required={'id','category','scenes','function','priority','dependencies','format','creation_method','license','estimated_cost','Roblox_compatibility','validation','files','tests','known_problems'}
        for resource in self.data['resources']:
            if set(resource)!=required or not re.fullmatch('[a-z0-9-]{1,64}',resource['id']) or resource['id'] in self.resources or not set(resource['scenes'])<=scenes or resource['priority'] not in ('P0','P1','P2','P3'):raise ValueError('invalid production resource')
            for file in resource['files']:safe_path(self.root,file)
            self.resources[resource['id']]=resource
        visited=set()
        def visit(key,chain):
            if key not in self.resources or key in chain:raise ValueError('invalid resource dependency or cycle')
            if key in visited:return
            for dep in self.resources[key]['dependencies']:visit(dep,chain+[key])
            visited.add(key)
        for key in self.resources:visit(key,[])
        if self.data['ending']['status']!='UNKNOWN' or any(x['status']!='PROPOSED' for x in self.data['ending']['options']):raise ValueError('ending must remain undecided')
        self.fingerprint=digest({'production':self.data,'bible':self.bible.fingerprint})
    def inventory(self):
        rows=[]
        for resource in self.resources.values():
            def present(p):
                if safe_path(self.root,p).is_file():return True
                # Catalog code references are repository-relative; a data-only
                # runtime must not falsely report its executing code absent.
                if p.startswith(('agent/','scripts/','roblox/','docs/v112/')):
                    return safe_path(Path(__file__).resolve().parents[1],p).is_file()
                return False
            missing=[p for p in resource['files'] if not present(p)]
            readiness='BLOCKED' if missing else 'PARTIAL' if resource['files'] else 'UNKNOWN'
            rows.append({**resource,'readiness':readiness,'missing_files':missing})
        return {'schema':'vdn.prologue-inventory/1','fingerprint':self.fingerprint,'resources':rows,'file_scope':'explicit data-root files or current code-repository references; no personal-folder discovery','production_days':self.data['production_days'],'design_hypotheses':self.data['design_hypotheses'],'ending':self.data['ending'],'engine_executed':False,'state':'PARTIAL','facts':[]}
    def brief(self,budget=1800):
        if type(budget) is not int or not 500<=budget<=8000:raise ValueError('context budget required')
        inv=self.inventory();out={'schema':'vdn.prologue-brief/1','state':'PARTIAL','objective':'Assemble the entire playable prologue A–E with proxies; stop before unapproved ending F.','constraints':self.data['confirmed_constraints'],'resources_count':len(inv['resources']),'available_code':[r['id'] for r in inv['resources'] if r['files'] and not r['missing_files']],'critical_missing':[r['id'] for r in inv['resources'] if r['priority']=='P0' and not r['files']],'ending':{'status':'UNKNOWN','detail':'No ending selected automatically.'},'engine_executed':False,'truth_verified':False,'detail_question':'prologue:resources','rollback':'Isolated copies only; retain original assets and checkpoints. No publication.'}
        while len(json.dumps(out,ensure_ascii=False))>budget*4 and out['critical_missing']:out['critical_missing'].pop();out['omitted_resources']=True
        return out
    def initial(self):return {'schema':'vdn.prologue-state/1','fingerprint':self.fingerprint,'state':self.data['initial'],'sequence':0,'last_event_id':None,'last_event':None,'seen_events':{},'engine_executed':False}
    def advance(self,state,event,event_id):
        if state.get('fingerprint')!=self.fingerprint or state.get('state') not in self.states:raise ValueError('obsolete/corrupt checkpoint')
        if not isinstance(event_id,str) or not re.fullmatch('[a-zA-Z0-9-]{1,64}',event_id):raise ValueError('bounded idempotency identity required')
        if not isinstance(state.get('seen_events'),dict) or len(state['seen_events'])>len(self.states) or state.get('sequence')!=len(state['seen_events']):raise ValueError('invalid event history')
        if event_id in state['seen_events']:
            if event!=state['seen_events'][event_id]:raise ValueError('idempotency identity conflict')
            return {**state,'duplicate':True}
        current=self.states[state['state']]
        if current['next'] is None:raise ValueError('ending requires a human decision; no automatic continuation')
        if event!=current['event']:raise ValueError('unexpected or out-of-order event')
        return {**state,'state':current['next'],'sequence':state['sequence']+1,'last_event_id':event_id,'last_event':event,'seen_events':{**state['seen_events'],event_id:event},'duplicate':False}
    def checkpoint(self,state,identity):
        if not re.fullmatch('[a-z0-9-]{1,64}',identity) or state.get('fingerprint')!=self.fingerprint:raise ValueError('invalid checkpoint')
        path='lab/learning/prologue/'+identity+'.json';save(self.root,path,{'payload':state,'sha256':digest(state)});return path
    def resume(self,identity):
        if not re.fullmatch('[a-z0-9-]{1,64}',identity):raise ValueError('invalid checkpoint identity')
        data=load(self.root,'lab/learning/prologue/'+identity+'.json');state=data['payload']
        if digest(state)!=data['sha256'] or state.get('fingerprint')!=self.fingerprint or state.get('state') not in self.states:raise ValueError('corrupt or stale checkpoint retained; review before restarting')
        return state
    def pages(self):
        return {'knowledge/_VDN-prologue/production.md':'# Prologue — PARTIAL, no Studio validation\n\n'+json.dumps(self.inventory(),ensure_ascii=False,indent=2)+'\n'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('command',choices=['inventory','brief','replay']);a=p.parse_args();work=Prologue(a.root)
    if a.command=='replay':
        state=work.initial();trace=[state]
        while work.states[state['state']]['next'] is not None:
            state=work.advance(state,work.states[state['state']]['event'],'step-'+str(state['sequence']+1));trace.append(state)
        out={'state':'SIMULATION_ONLY','trace':trace,'engine_executed':False,'note':'No player action, voice, Studio scene or gameplay timing executed.'}
    else:out=work.inventory() if a.command=='inventory' else work.brief()
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
