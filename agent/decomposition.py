"""Bounded, inspectable domain plans with prerequisites; no model or network."""
from __future__ import annotations

import json
from pathlib import Path

from agent import meta
from agent.research_queue import ResearchQueue, item_key, excluded_term
from agent.text import fold, tokens


def plan(root: Path, question: str, topic: str) -> dict:
    q = ResearchQueue(root)
    if topic not in q.topics:
        raise ValueError('sujet non autorise')
    path = Path(root) / 'config' / 'research_domains.json'
    profiles = json.loads(path.read_text(encoding='utf-8'))['profiles'] if path.exists() else []
    words = set(fold(question).replace('?', '').split())
    profile = next((p for p in profiles if words & set(p['triggers'])), None)
    # Simple questions retain the existing queue engine.
    nodes = profile['nodes'] if profile and len(words) >= 6 else []
    if nodes and (q.cfg['queue']['max_depth'] < 1 or len(nodes) > q.cfg['queue']['max_plan_nodes'] or
                  len(nodes) > q.cfg['queue']['max_size'] - q.pending_count()):
        raise ValueError('plan refuse : profondeur ou capacite de file insuffisante')
    seen = set()
    for node in nodes:
        if node['id'] in seen or any(d not in seen for d in node.get('requires', [])):
            raise ValueError('profil invalide : prerequis cycliques, inconnus ou ordre non topologique')
        if not tokens(node['query']) or excluded_term(node['query'], q.cfg['excluded_terms']):
            raise ValueError('profil invalide : requete vide ou exclue')
        seen.add(node['id'])
    # Buffer the journal until the entire plan has been accepted.
    events = []
    log = q.log
    q.log = lambda event, payload: events.append((event, payload))
    added, reason = q.add(topic, question, q.topics[topic].get('priority', 5), origin='question', reason='question utilisateur')
    if not added:
        return {'question': question, 'added': 0, 'reason': reason, 'nodes': []}
    parent = next(it for it in q.data['items'].values() if item_key('', it['query']) == item_key(topic, question))
    if nodes:
        parent.update(status='skipped', reason='question decomposee ; recherches dans les enfants')
    out = []
    keys = {}
    for node in nodes:
        dependencies = [keys[d] for d in node.get('requires', [])]
        target = q.best_topic(node['query'], topic)
        ok, why = q.add(target, node['query'], parent['priority'], origin='decomposition', depth=1,
                       parent=parent['key'], reason=node['reason'], dependencies=dependencies)
        key = next((it['key'] for it in q.data['items'].values() if item_key('', it['query']) == item_key('', node['query'])), None)
        if key is None:
            # No dangling prerequisites or partial persisted plans.
            raise ValueError(f"plan refuse : {node['id']} : {why}")
        keys[node['id']] = key
        out.append({**node, 'key': key, 'added': ok, 'decision': why})
    q.save()
    for event, payload in events:
        log(event, payload)
    result = {'schema': 'vdn.plan/1', 'question': question, 'root': parent['key'],
              'profile': profile['id'] if nodes else None, 'added': sum(n['added'] for n in out) if nodes else 1,
              'nodes': out, 'limits': q.cfg['queue']}
    meta.save_json(Path(root) / 'output' / 'research_plans' / (parent['key'] + '.json'), result)
    return result
