"""Manual-first image planning. No image synthesis, perceptual score or actions."""
import hashlib
import struct
from agent.lab_store import LabStore,clean_json
from agent.models import infer

FIELDS=('observations','hypotheses','uncertainties')


def annotations(value):
    if not isinstance(value,dict) or set(value)!=set(FIELDS):raise ValueError('supply observations, hypotheses and uncertainties')
    for field in FIELDS:
        items=value[field]
        if not isinstance(items,list) or len(items)>30 or not all(isinstance(i,str) and 1<=len(i)<=500 for i in items):raise ValueError('invalid visual annotations')
    clean_json(value);return value


def image_data(root,artifact_id):
    lab=LabStore(root);receipt=lab.artifact(artifact_id);path=lab.root/receipt['path'];data=path.read_bytes()
    # PNG only in V10 to keep MIME validation and dimension reading deterministic.
    if len(data)<24 or data[:8]!=b'\x89PNG\r\n\x1a\n' or data[12:16]!=b'IHDR':raise ValueError('V10 visual input requires a PNG artifact')
    width,height=struct.unpack('>II',data[16:24])
    if not width or not height or width*height>100_000_000:raise ValueError('invalid PNG dimensions')
    return data,{'sha256':receipt['sha256'],'file_bytes':len(data),'width_px':width,'height_px':height,
                 'measurement_scope':'PNG header only; no decoded pixels or calibrated scene dimensions'}


def plan(root,artifact_id,manual=None,backend='none'):
    data,objective=image_data(root,artifact_id)
    output={'state':'manual'} if manual is not None else infer(root,'Describe visible elements and spatial relations as short strings in observations, hypotheses, uncertainties arrays.',backend,[data])
    claims=manual if manual is not None else output.get('claims')
    if claims is None:return {'state':'manual_required','objective':objective,'template':{k:[] for k in FIELDS},'model':output}
    claims=annotations(claims)
    return {'state':'annotated','objective':objective,**claims,
            'topics':[{'question':'Comment reproduire et tester : '+x,'origin':'manual_observation' if manual is not None else 'unverified_model_observation'} for x in claims['observations']],
            'original_technique':'unknown','verified':False,'model':output if manual is None else {'state':'manual'}}


def compare(root,reference,result,corrections=None,backend='none'):
    a,ma=image_data(root,reference);b,mb=image_data(root,result)
    output={'state':'manual'} if corrections is not None else infer(root,'Compare target image first, result second. Return corrections array of objects with dimension (silhouette, proportions, colors, materials, lighting, missing, excessive), impact (high, medium, low), reason and action. No numeric scene measurements.',backend,[a,b])
    values=corrections if corrections is not None else (output.get('claims') or {}).get('corrections',[])
    if not isinstance(values,list) or len(values)>30:raise ValueError('invalid corrections')
    for v in values:
        if not isinstance(v,dict) or set(v)!=set(('dimension','impact','reason','action')):raise ValueError('invalid correction fields')
        if v['dimension'] not in ('silhouette','proportions','colors','materials','lighting','missing','excessive') or v['impact'] not in ('high','medium','low'):raise ValueError('invalid correction category')
        if not all(isinstance(v[k],str) and 1<=len(v[k])<=1000 for k in ('reason','action')):raise ValueError('invalid correction text')
    clean_json(values)
    return {'state':'annotated' if values else 'manual_required','objective':{'reference':ma,'result':mb,'byte_identical':ma['sha256']==mb['sha256']},
            'estimates':sorted(values,key=lambda v:('high','medium','low').index(v['impact'])),
            'estimate_origin':'manual' if corrections is not None else 'unverified_model','calibrated_score':None,'verified':False}
