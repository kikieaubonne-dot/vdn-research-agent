"""Local knowledge facade. Source Markdown is untrusted data, never instructions.

Acquisition is deliberately absent from this API. Only report_experiment may
write user data, in its own directory, when explicitly enabled by the host.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import uuid

from agent import rag, knowledge, decomposition
from agent.corpus import read_text, scan_notes
from agent.evaluation import evaluate_note
from agent.procedure import actionable_excerpts
from agent.research_queue import load_config
from agent.storage import atomic_write
from urllib.parse import urlparse

LEVELS = ('documentee', 'a_verifier', 'testee_localement', 'preuve_externe_inspectee', 'contestee')


def string(value, name, limit=2000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'{name}: nonempty string, at most {limit} characters')
    return value


def integer(value, name, low=1, high=10):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{name}: integer in {low}..{high}')
    return value


def evidence(text):
    meta, body = knowledge.parse_note(text)
    assessed = evaluate_note(text)
    level = 'contestee' if assessed['conflict'] else ('documentee' if
            assessed['diagnostics']['source_traceability'] and assessed['diagnostics']['actionable_steps'] else 'a_verifier')
    claimed = {'reproduit': 'testee_localement', 'valide': 'preuve_externe_inspectee'}.get(meta.get('status'))
    return {'level': level, 'claimed_level': claimed, 'verified': False,
            'source_tier_prior': meta.get('source_tier'), 'source_reliability': 'not_independently_verified',
            'gaps': assessed['gaps'], 'warnings': assessed['warnings'],
            'technical_accuracy': assessed['technical_accuracy']}


def source_steps(text):
    meta, body = knowledge.parse_note(text)
    editorial=meta.get('editorial_steps',[])
    if meta.get('procedure_origin')=='source_based_editorial_candidate' and isinstance(editorial,list):
        return [s for s in editorial if isinstance(s,str) and len(s)<=1000][:12]
    excerpts = re.findall(r'^>\s*«\s*(.+?)\s*»\s*$', body, re.M)
    if not excerpts:
        # Legacy evidence is explicitly tagged as extracted, not independently verified.
        excerpts = [line.lstrip('- ').strip() for line in knowledge.legacy_evidence(body).splitlines()]
    return list(dict.fromkeys(actionable_excerpts(excerpts)))[:12]


def compatibility(text):
    meta,body=knowledge.parse_note(text)
    title=str(meta.get('title',''))
    quoted=' '.join(re.findall(r'^>\s*«\s*(.+?)\s*»\s*$',body,re.M)) or knowledge.legacy_evidence(body)
    source_text=title+' '+quoted
    if re.search(r'(?i)\b(babylon(?:\.js)?|unity|unreal|webgpu|webgl)\b',title):
        scope='other_engine';limitations=['Engine-specific technique: a Roblox port and compatibility test are required.']
    elif any(urlparse(u).hostname in ('create.roblox.com','devforum.roblox.com') for u in meta.get('sources',[])):
        scope='roblox_specific';limitations=['Roblox version, device and practical result still require testing.']
    elif re.search(r'(?i)\broblox\b',source_text):
        scope='roblox_mentioned';limitations=['Roblox is mentioned; engine compatibility is not independently verified.']
    elif re.search(r'(?i)\bblender\b',source_text):
        scope='blender_pipeline';limitations=['Blender workflow: Roblox import constraints remain to be checked.']
    else:
        scope='unknown';limitations=['Roblox compatibility is not established by the available source excerpts.']
    return {'scope':scope,'verified':False,'engine_version':meta.get('engine_version','unknown'),'limitations':limitations}


def meaningful_section(body, names):
    sec = knowledge.sections(body)
    values = [sec.get(name, '').strip() for name in names]
    return [v for v in values if v and not re.search(r'(?i)^\s*(?:[-*]\s*)?(à compléter|a completer|aucun|non identifi|—\s*$)', v)]


class KnowledgeEngine:
    def __init__(self, root: Path, *, allow_experiments=False):
        self.root = Path(root).resolve()
        self.allow_experiments = allow_experiments
        self._snapshot = None
        self.index = None

    def get_task_brief(self, task, mode='compact', token_budget=1800):
        from agent.operational import brief
        return brief(self,task,mode,token_budget)

    def _ensure_index(self):
        snapshot = tuple((p.relative_to(self.root).as_posix(), p.stat().st_mtime_ns, p.stat().st_size)
                         for p in sorted((self.root/'knowledge').rglob('*.md')) if not p.is_symlink())
        if snapshot != self._snapshot:
            self.index = rag.update_index(self.root)
            self._snapshot = snapshot
        return self.index or {}

    def get_knowledge(self, note_id):
        string(note_id, 'note_id', 120)
        if not re.fullmatch(r'[A-Za-z0-9_-]+', note_id):
            raise ValueError('invalid note_id')
        self._ensure_index()
        con = rag.connect(self.root)
        try:
            row = con.execute('SELECT path FROM notes WHERE id=?', (note_id,)).fetchone()
        finally:
            con.close()
        if not row:
            return {'error': 'unknown note_id', 'note_id': note_id}
        text = read_text(self.root, row[0])
        meta, body = knowledge.parse_note(text)
        if meta.get('id') != note_id:
            raise ValueError('index does not match source identity')
        return {'id': note_id, 'title': meta.get('title'), 'path': row[0], 'meta': meta,
                'body': body, 'content': text, 'truncated': False, 'sources': meta.get('sources', []),
                'updated': meta.get('updated'), 'engine_version': meta.get('engine_version'),
                'evidence': evidence(text), 'compatibility':compatibility(text), 'untrusted_data': True}

    def search_knowledge(self, query, top_k=5, token_budget=1500, domain=None, evidence_level=None):
        string(query, 'query')
        integer(top_k, 'top_k')
        integer(token_budget, 'token_budget', 200, 8000)
        if domain is not None and (not isinstance(domain, str) or not re.fullmatch(r'[a-z0-9_-]{1,80}', domain)):
            raise ValueError('invalid domain')
        if evidence_level is not None and evidence_level not in LEVELS:
            raise ValueError('invalid evidence_level')
        self._ensure_index()
        raw = rag.search_knowledge(query, 10, token_budget, self.root, domain=domain)
        out, seen = [], set()
        for hit in raw['results']:
            if hit['note_id'] in seen:
                continue
            note = self.get_knowledge(hit['note_id'])
            if note.get('error'):
                continue
            if evidence_level and note['evidence']['level'] != evidence_level:
                continue
            seen.add(hit['note_id'])
            out.append({'id': hit['note_id'], 'title': hit['title'], 'excerpt': hit['text'],
                        'heading': hit['heading'], 'relevance_score': hit['score'], 'ranking': hit['ranking'],
                        'path': hit['path'], 'domain': hit['domain'], 'sources': note['sources'],
                        'updated': note['updated'], 'engine_version': note['engine_version'], 'evidence': note['evidence'],
                        'compatibility':note['compatibility'],
                        'uncertainties': ['Technical accuracy has not been independently verified.'] + note['evidence']['warnings']})
        if re.search(r'(?i)\broblox\b',query):
            order={'roblox_specific':0,'roblox_mentioned':1,'blender_pipeline':2,'unknown':3,'other_engine':4}
            out.sort(key=lambda hit:order[hit['compatibility']['scope']])
        return {'schema': 'vdn.search/8', 'query': query, 'results': out[:top_k],
                'index_diagnostics': self.index.get('diagnostics', []),
                'selection_policy': 'explicit Roblox tasks prefer Roblox-scoped sources; then query coverage, title coverage, text BM25; evidence reported separately',
                'tokens_estimated_passages': raw['tokens_estimated'], 'untrusted_data': True}

    def find_procedures(self, task, top_k=5):
        string(task, 'task');integer(top_k, 'top_k')
        found = self.search_knowledge(task, top_k, 8000)
        procedures = []
        for hit in found['results']:
            note = self.get_knowledge(hit['id'])
            steps = source_steps(note['content'])
            procedures.append({'note_id': note['id'], 'title': note['title'], 'sources': note['sources'],
                'candidate_steps': [{'text': step, 'source_note': note['id'], 'source_urls': note['sources'],
                                     'verified': False,'origin':note['meta'].get('procedure_origin','source_excerpt')} for step in steps],
                'prerequisites': meaningful_section(note['body'], ('Prérequis','Prerequisites')),
                'constraints': meaningful_section(note['body'], ('Limites connues de Roblox','Constraints')),
                'parameters': meaningful_section(note['body'], ('Paramètres (sourcés)',)),
                'alternatives':meaningful_section(note['body'],('Alternatives',)),
                'validation_plan':meaningful_section(note['body'],('Protocole de reproduction proposé, non exécuté','Protocole de reproduction')),
                'rollback':meaningful_section(note['body'],('Retour arrière',)),
                'evidence': note['evidence'], 'order_verified': False,
                'compatibility':note['compatibility'],
                'procedure_status': 'requires_porting' if note['compatibility']['scope']=='other_engine' else
                                    'candidate_instructions' if steps else 'insufficient_evidence',
                'needs_verification': note['evidence']['gaps'] + ['sequence, engine version and reproduction in Studio'],
                'ranking': hit['ranking']})
        return {'schema':'vdn.procedures/8','task':task,'procedures':procedures,
                'complementary_sources': list(dict.fromkeys(u for p in procedures for u in p['sources'])),
                'warning':'Extracted instructions are candidates; sources are not an executable or validated end-to-end tutorial.'}

    def plan_research(self, question):
        string(question, 'question')
        preview = decomposition.describe(self.root, question)
        cfg = load_config(self.root)
        if preview['nodes'] and cfg['queue']['max_depth']<1:
            raise ValueError('decomposition disabled by max_depth')
        nodes = preview['nodes'] or [{'id':'question', 'query':question, 'requires':[], 'reason':'question utilisateur'}]
        if len(nodes) > cfg['queue']['max_plan_nodes']:
            raise ValueError('plan exceeds max_plan_nodes')
        out=[]
        for node in nodes:
            found=self.search_knowledge(node['query'],3,1000)
            # Relevance is not prerequisite completion; references remain candidates.
            refs=[r for r in found['results'] if r['ranking']['matched']]
            gaps=sorted(set(g for r in refs for g in r['evidence']['gaps'])) if refs else ['no_local_evidence']
            if refs and refs[0]['ranking']['coverage']<1:
                gaps.append('query_not_fully_matched')
            out.append({**node,'references':refs,'status':'candidate_references' if refs else 'needs_research',
                        'missing_prerequisites':[d for d in node.get('requires',[]) if not next((p['references'] for p in out if p['id']==d),[])],
                        'unverified_prerequisites':node.get('requires',[]), 'gaps':gaps,
                        'validated_procedure':False})
        return {'schema':'vdn.plan-preview/8','question':question,'profile':preview['profile'],
                'nodes':out,'construction_order':[n['id'] for n in nodes],
                'network_requests':0,'queue_modified':False,'built_scene':False,
                'limits':{'max_nodes':cfg['queue']['max_plan_nodes'],'max_depth':cfg['queue']['max_depth']}}

    def report_experiment(self, task, result, parameters, environment, observations, references, experiment_id=None):
        if not self.allow_experiments:
            raise PermissionError('experiment writes disabled; enable --allow-experiments explicitly')
        string(task,'task');string(result,'result')
        if not isinstance(parameters,dict) or not isinstance(environment,dict):
            raise ValueError('parameters and environment must be objects')
        if not isinstance(observations,list) or not observations or not all(isinstance(x,str) and len(x)<=4000 for x in observations):
            raise ValueError('observations must be a nonempty list of strings')
        if not isinstance(references,list) or not references or len(references)>20:
            raise ValueError('references must contain 1..20 note IDs')
        for reference in references:
            if self.get_knowledge(reference).get('error'):
                raise ValueError('unknown referenced note')
        if experiment_id is not None:
            string(experiment_id,'experiment_id',36)
        identity=str(uuid.UUID(experiment_id)) if experiment_id else str(uuid.uuid4())
        payload={'task':task,'result':result,'parameters':parameters,'environment':environment,
                 'observations':observations,'references':references}
        encoded=json.dumps(payload,ensure_ascii=False,sort_keys=True,allow_nan=False)
        if len(encoded.encode('utf-8'))>64000:
            raise ValueError('experiment exceeds 64 KB')
        digest=hashlib.sha256(encoded.encode('utf-8')).hexdigest()
        folder=self.root/'experiments'
        if folder.is_symlink():
            raise ValueError('symlink experiment directory refused')
        from agent.autonomy import Lock
        with Lock(self.root,load_config(self.root)['lock']['stale_after_s']):
            folder.mkdir(exist_ok=True)
            path=folder/(identity+'.json');journal=folder/'journal.jsonl'
            if path.is_symlink() or journal.is_symlink():
                raise ValueError('symlink experiment file refused')
            record={'schema':'vdn.experiment/8','id':identity,'reported_at':dt.datetime.now(dt.timezone.utc).isoformat(),
                    **payload,'content_sha256':digest,'reported_by':'client','verification':'unverified_report',
                    'truth_verified':False,'promotes_knowledge':False}
            if path.exists():
                record=json.loads(path.read_text(encoding='utf-8'))
                if record.get('content_sha256')!=digest:
                    raise ValueError('experiment_id already used for a different report')
            else:
                atomic_write(path,json.dumps(record,ensure_ascii=False,indent=2)+'\n',create_only=True)
            log=journal.read_text(encoding='utf-8') if journal.exists() else ''
            events=[json.loads(line) for line in log.splitlines() if line.strip()]
            if not any(e['id']==identity for e in events):
                atomic_write(journal,log+json.dumps({'event':'experiment_reported','id':identity,'verification':'unverified_report'})+'\n')
        return {'id':identity,'path':path.relative_to(self.root).as_posix(),'verification':'unverified_report',
                'truth_verified':False,'promotes_knowledge':False}
