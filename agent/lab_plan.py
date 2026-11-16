"""Reproducible plans and conditional memory. Never executes a game or model."""
import json
import uuid
from agent.lab_store import LabStore,clean_json
from agent.knowledge import dump_frontmatter

METRICS=('triangles','materials','textures','asset_bytes','night_readability_rating','artifact_count','frame_time_ms')
ZONES=('Forêt et végétation','Éclairage','Matériaux','Personnages','Vêtements','Animations','Gameplay et IA','Importation','Performances')
CONTROLS=('studio_version','device','graphics_quality','resolution','camera','lighting','tree_count','warmup_s','sample_s')


def spruce(root,apply=False,batch='snowy-spruce-v10'):
    if not isinstance(batch,str) or not 1<=len(batch)<=120:raise ValueError('invalid batch')
    namespace=uuid.uuid5(uuid.NAMESPACE_URL,'vdn:'+batch)
    shared={'batch':batch,'zone':ZONES[0],'controls':{k:None for k in CONTROLS},
            'procedure':['Créer un place privé VDN — Laboratoire et définir Workspace.VDNLab=true.',
                         'Créer deux modèles isolés avec la même silhouette et les mêmes dimensions cibles.',
                         'A : tronc, branches et aiguilles en géométrie simplifiée ; B : même tronc avec cartes de feuillage et atlas.',
                         'Exporter des copies distinctes ; consigner versions Blender/Studio, options FBX et identifiants des assets.',
                         'Fixer caméra, lumière nocturne, appareil, qualité et résolution identiques ; documenter tous les contrôles.',
                         'Mesurer chaque méthode seule, après préchauffage, puis répéter trois fois en alternant A/B.',
                         'Compter triangles dans Blender ; mesurer octets des exports locaux ; capturer les mêmes vues de nuit.',
                         'Consigner textures, matériaux, artefacts, MicroProfiler et durée des trames ; conserver captures et journaux.'],
            'validation':['Aucun paramètre comparatif inconnu ; trois répétitions documentées et données brutes jointes.',
                          'Comparer silhouette et lisibilité par annotation humaine ; l’échelle 1–5 est subjective.',
                          'Définir les seuils de performance et de qualité pour l’appareil cible avant le test.',
                          'Examiner les différences et limites avant toute recommandation conditionnelle.'],
            'rollback':'Supprimer les copies du laboratoire ; aucun changement au jeu principal.',
            'metrics_template':{k:None for k in METRICS},'not_executed':True}
    experiments=[];lab=LabStore(root)
    for method,technique in (('A','Géométrie simplifiée'),('B','Cartes de feuillage')):
        spec={'problem':'Sapin enneigé Roblox : qualité nocturne et coût de rendu', 'technique':technique,
              'hypothesis':'Comparer qualité et coût sous les mêmes conditions, sans supposer une méthode gagnante.',
              'parameters':{'method':method,'assets':[]},'environment':{},'protocol':shared,
              'experiment_id':str(uuid.uuid5(namespace,method))}
        record=lab.create(**spec) if apply else {**spec,'id':spec['experiment_id'],'status':'PLANNED_PREVIEW'}
        if apply and record['status']=='HYPOTHESIS':record=lab.transition(record['id'],'PLANNED')
        experiments.append(record)
    return {'state':'planned' if apply else 'simulation','zones':list(ZONES),'experiments':experiments,
            'game_executed':False,'comparison':'pending external measurements','winner':None}


def compare(root,first,second):
    lab=LabStore(root);records=[lab.get(first),lab.get(second)]
    if any(r.get('error') for r in records):raise ValueError('unknown comparison experiment')
    controls=[r['protocol'].get('controls',{}) for r in records]
    reasons=[]
    if not all(c and all(c.get(k) is not None for k in CONTROLS) for c in controls):reasons.append('missing controls')
    if controls[0]!=controls[1] or records[0]['environment']!=records[1]['environment']:reasons.append('conditions differ')
    if not all(r['results'] for r in records):reasons.append('missing results')
    if any(r['status'] not in ('FAILED','PARTIAL_SUCCESS','SUCCESS','VERIFIED') for r in records):reasons.append('latest run not complete')
    rows=[]
    for metric in METRICS:
        values=[r['results'][-1]['metrics'].get(metric) if r['results'] else None for r in records]
        rows.append({'metric':metric,'A':values[0],'B':values[1],
                     'B_minus_A':values[1]-values[0] if not reasons and all(v is not None for v in values) else None,
                     'kind':'subjective_annotation' if metric=='night_readability_rating' else 'reported_measurement'})
    return {'ids':[first,second],'comparable':not reasons,'reasons':reasons,'metrics':rows,'winner':None,
            'verification':[r['verification'] for r in records],
            'warning':'Raw reports do not establish causality or a universal winner; inspect repetitions, artifacts and conditions.'}


def summary(record,outcome=None):
    outcomes=[r for r in record['results'] if outcome is None or r['status']==outcome]
    last=outcomes[-1] if outcomes else None
    return {k:record[k] for k in ('id','status','revision','verification')} | {
        'reuse_conditions':[s[:200] for s in record['reuse_conditions'][:3]],
        'problem':record['problem'][:240],'technique':record['technique'][:160],
        'outcome_status':last['status'] if last else None,
        'last_errors':[s[:180] for s in last['errors'][:2]] if last else [],
        'limitations':[s[:180] for s in last['limits'][:2]] if last else ['not executed']}


def context(root,problem='',status=None,limit=5,detailed=False):
    result=LabStore(root).find(problem,status,limit)
    records=result['experiments']
    result['experiments']=records if detailed else [summary(r) for r in records]
    result['failed_methods']=[summary(r,'FAILED') for r in LabStore(root).find(problem,limit=min(2,limit),outcome='FAILED')['experiments']] if status in (None,'FAILED') else []
    result['reviewed_candidates']=[summary(r) for r in LabStore(root).find(problem,'VERIFIED',min(2,limit))['experiments']] if status in (None,'VERIFIED') else []
    result['best_technique']=None # Conditions and objectives must be compared by the caller.
    result['scope']='bounded lexical matches, not exhaustive recommendation or truth ranking'
    return result


def pages(root):
    lab=LabStore(root);folder=lab.path('experiments');result={};links=[]
    paths=sorted(folder.iterdir()) if folder.exists() else []
    if len(paths)>1000:raise ValueError('experiment count limit exceeded')
    for path in paths:
        r=lab.get(path.name)
        if r.get('error'):continue
        name='_VDN-Experience-'+r['id'];links.append('[['+name+']] — '+r['status'])
        meta={'id':r['id'],'type':'experiment','status':r['status'],'verification':r['verification'],
              'revision':r['revision'],'event_sha256':r['event_sha256'],'created':r['created_at'],'updated':r['updated_at']}
        result['knowledge/'+name+'.md']=dump_frontmatter(meta)+'\n# '+r['problem']+'\n\n'+\
            '[[ _VDN-Experiences ]]'.replace(' ','')+'\n\nDonnées rapportées ; les conditions de réutilisation restent obligatoires.\n\n'+\
            '```json\n'+clean_json(r)+'\n```\n'
    result['knowledge/_VDN-Experiences.md']='# 07 — Expériences\n\nMémoire séparée des sources. Échecs conservés ; revue humaine explicite pour VERIFIED.\n\n'+'\n'.join(links)+'\n'
    return result
