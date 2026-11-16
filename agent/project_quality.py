"""Explainable task preparation. Readiness is a checklist, never a probability."""
import re
from agent.intelligence_evidence import digest
from agent.lab_store import LabStore
from agent.text import tokens

STATES=('SOURCE_DOCUMENTED','ENGINEERING_PROPOSAL','TESTED_IN_ISOLATION','TESTED_IN_BLENDER',
        'TESTED_IN_ROBLOX','HUMAN_APPROVED','FAILED','OBSOLETE')


def quality(bible,task,analysis,proposal,dependency_states=None,records=None):
    dependency_states={} if dependency_states is None else dependency_states
    selected={p['id']:p for p in analysis['passages']};issues=[];valid=[];seen=set();sources=[]
    for c in analysis['facts']:
        refs=[selected.get(i) for i in c['passage_ids']]
        if not refs or any(p is None for p in refs):issues.append('citation_missing_passage');continue
        if c['support']!='SOURCE_SUPPORTED' or any(not p['independent'] or p['incomplete_context'] for p in refs):issues.append('source_insufficient');continue
        if any(p['engine'] not in ('Roblox','Blender') for p in refs):issues.append('foreign_engine_not_applicable');continue
        if any(p['engine']=='Blender' and p['version']!=bible.value('blender_version') for p in refs):issues.append('blender_version_incompatible');continue
        if not set(tokens(' '.join(task['anchors']))) & set(tokens(c['text']+' '+' '.join(p['section'] for p in refs))):issues.append('correct_but_off_topic');continue
        valid.append(c)
        for p in refs:
            key=(p['url'],p['document_sha256'])
            if key not in seen:sources.append({k:p[k] for k in ('id','document_id','url','document_sha256','version','engine','source_type','section','start','end')});seen.add(key)
    for p in analysis['passages']:
        if p['engine']=='Blender' and p['version']!=bible.value('blender_version'):issues.append('blender_version_unverified_or_incompatible')
        if p['version'] in ('unknown','inconnue','UNKNOWN'):issues.append('software_version_unknown')
    for c in analysis['claims']:
        if c['support']=='OUTDATED':issues.append('source_obsolete')
        if c['support']=='UNSUPPORTED':issues.append('rejected_claim_not_a_fact')
    if analysis['contradictions']:issues.append('contradiction_requires_review')
    if analysis['source_diagnostics']:issues.append('source_or_index_diagnostic')
    structured=all(all(isinstance(s.get(k),str) and len(s[k])>=12 for k in ('input','action','expected_observation')) and s.get('component') for s in proposal['steps'])
    if not structured:issues.append('procedure_not_reproducible')
    if not sources:issues.append('no_sufficient_original_source')
    # Only explicitly task-bound reports can establish test scope. Lexical
    # similarity by itself is not evidence that B3/C1 or this project was tested.
    records=LabStore(bible.root).find(task['query'],limit=20)['experiments'] if records is None else records
    tests=[];approved=[];failures=[]
    for r in records:
        env=r['environment'];bound=env.get('project_task')==task['id'] or r['parameters'].get('project_task')==task['id']
        if not bound:continue
        if not r['results']:continue
        last=r['results'][-1];kind=env.get('engine')
        reviewed=bool(r['status']=='VERIFIED' and r['review'] and r['verification']=='operator_reviewed_under_stated_conditions')
        # A declared engine name, a Python test or an unreviewed client report
        # cannot establish an engine execution. Preserve that declaration apart.
        scope=('TESTED_IN_ROBLOX' if kind=='Roblox' else 'TESTED_IN_BLENDER') if reviewed and kind in ('Roblox','Blender') else 'TESTED_IN_ISOLATION'
        same_assets=set(task['assets'])<=set(env.get('asset_ids',[]))
        version=env.get('engine_version') if kind=='Roblox' else env.get('blender_version')
        target=bible.value('engine_version') if kind=='Roblox' else bible.value('blender_version')
        matches=kind in ('Roblox','Blender') and version==target and target not in ('UNKNOWN','unknown') and same_assets
        protocol_matches=r['protocol'].get('project_recipe_hash')==digest(proposal)
        tests.append({'id':r['id'],'scope':scope,'reported_outcome':last['status'],'conditions':last['conditions'],
                      'declared_engine':kind,'engine_execution_human_attested':reviewed,
                      'matches_proposed_protocol':protocol_matches,
                      'matches_task_assets_and_version':matches,'verification':r['verification'],'provenance':last['provenance']})
        if last['status']=='FAILED':failures.append(tests[-1])
        if reviewed and matches and not protocol_matches:issues.append('reviewed_experiment_does_not_bind_current_procedure')
        if matches and protocol_matches and kind=='Roblox' and reviewed:approved.append(r['id'])
    if failures:issues.append('bound_failure_requires_new_justification')
    questions=bible.questions(task)
    missing_dependencies=[d for d in task['requires'] if dependency_states.get(d)!='READY']
    checks={'original_sources_sufficient':bool(valid),'procedure_structured':structured,
            'blocking_decisions_resolved':not questions,'dependencies_ready':not missing_dependencies,
            'compatibility_and_assets_human_reviewed':bool(approved),
            'no_unresolved_conflict_or_failure':not analysis['contradictions'] and not failures}
    if questions or failures:readiness='BLOCKED'
    elif all(checks.values()):readiness='READY'
    elif analysis['passages'] or proposal['steps']:readiness='PARTIAL'
    else:readiness='UNKNOWN'
    statuses=['ENGINEERING_PROPOSAL']
    if valid:statuses.append('SOURCE_DOCUMENTED')
    statuses+=list(dict.fromkeys(t['scope'] for t in tests))
    if approved:statuses.append('HUMAN_APPROVED')
    if failures:statuses.append('FAILED')
    if 'source_obsolete' in issues:statuses.append('OBSOLETE')
    return {'readiness':readiness,'research_state':'PARTIAL' if analysis['passages'] else 'UNKNOWN',
        'checks':checks,'issues':list(dict.fromkeys(issues)),'facts':valid,'sources':sources,'evidence_states':statuses,
        'blocking_questions':[{'id':q['id'],'text':q['text']} for q in questions],
        'missing_dependencies':missing_dependencies,'experiments':tests,'failures':failures,
        'remote_links':'not live-checked by this offline control','meaning':'task preparation checklist; no probability or claim of engine success'}


def drift(bible,idea):
    q=idea.lower();outside=any(s in q for s in ('nanite','lumen','unreal shader','shader unreal','assistant universel'))
    narrative=any(s in q for s in ('maëlle sera','maelle sera','père noël sera','pere noel sera','sonia sera'))
    return {'coherence':'REQUIRES_REVIEW' if outside or narrative else 'UNKNOWN',
        'technical_transfer':'UNSUPPORTED_WITHOUT_ROBLOX_EVIDENCE' if outside else 'not established',
        'player_impact':'à expliciter','dependencies':'à documenter','cost':'unknown','P0_P1_risk':'do not expand mandatory scope',
        'can_defer':True,'decision':'human decision required' if outside or narrative else 'proposal only',
        'narrative_confirmed':False}
