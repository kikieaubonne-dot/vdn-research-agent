"""Run explicitly in Blender background. No network, asset overwrite or publishing.

Demo: blender --background --factory-startup --disable-autoexec --python THIS --
 --demo --experiment-a UUID --experiment-b UUID --output-dir lab/inbox
Real asset: launch a trusted COPY with --disable-autoexec, pass --experiment-a,
 --method B3; script only measures the loaded scene and creates a new JSON report.
"""
import argparse
import json
from pathlib import Path
import sys
import uuid
import bpy
from mathutils import Vector


def safe_output(folder,name):
    rel=Path(folder)
    if rel.is_absolute() or '..' in rel.parts or '\\' in folder or rel.parts[:2]!=('lab','inbox'):raise ValueError('output must be relative lab/inbox')
    p=Path.cwd()/rel/name
    for parent in (p,*p.parents):
        if parent.is_symlink():raise ValueError('symlink output refused')
    p.parent.mkdir(parents=True,exist_ok=True);return p


def report(experiment_id,method,objects,scope):
    if len(objects)>1000:raise ValueError('measurement scope exceeds 1000 objects')
    deps=bpy.context.evaluated_depsgraph_get();triangles=0;materials=set();bounds=[];rows=[]
    for obj in objects:
        if obj.type!='MESH':continue
        evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles();n=len(mesh.loop_triangles);triangles+=n
            materials.update(m.name for m in mesh.materials if m is not None)
            bounds += [evaluated.matrix_world@Vector(c) for c in evaluated.bound_box]
            rows.append({'name':obj.name,'triangles':n})
        finally:evaluated.to_mesh_clear()
    scale=bpy.context.scene.unit_settings.scale_length
    dims=[(max(b[i] for b in bounds)-min(b[i] for b in bounds))*scale if bounds else 0 for i in range(3)]
    controls={'blender_version':bpy.app.version_string,'unit_scale':scale,'measurement_method':'evaluated_loop_triangles_v1'}
    return {'schema':'vdn.blender-measurement/11','experiment_id':str(uuid.UUID(experiment_id)),'method':method,
            'environment':controls,'controls':controls,
            'metrics':{'triangles':triangles,'objects':len(rows),'materials':len(materials),
                       'dimension_x_m':dims[0],'dimension_y_m':dims[1],'dimension_z_m':dims[2]},
            'objects':rows,'provenance':scope,'observations':['Geometry only; no Roblox performance, visual quality or rendered FPS measured.']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--demo',action='store_true');parser.add_argument('--experiment-a',required=True)
    parser.add_argument('--experiment-b');parser.add_argument('--method',default='B3');parser.add_argument('--output-dir',default='lab/inbox')
    a=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not bpy.app.background:raise ValueError('background process required; no live editor scene modification')
    batches=[]
    if a.demo:
        if bpy.data.filepath or not a.experiment_b:raise ValueError('demo requires factory-startup and two explicit experiment IDs')
        bpy.ops.wm.read_factory_settings(use_empty=True)
        mat=bpy.data.materials.new('DEMO_MATERIAL')
        for label,count,eid in (('DEMO_A',8,a.experiment_a),('DEMO_B',16,a.experiment_b)):
            objects=[]
            bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=.15,radius2=.1,depth=2,location=(0,0,1))
            objects.append(bpy.context.object)
            bpy.ops.mesh.primitive_cone_add(vertices=count,radius1=1,radius2=0,depth=3,location=(0,0,2.5))
            objects.append(bpy.context.object)
            for index,obj in enumerate(objects):obj.name=label+'_'+str(index);obj.data.materials.append(mat)
            batches.append((eid,label,objects,'Generated primitive demonstration; NOT user assets B3/C1.'))
    else:
        batches=[(a.experiment_a,a.method,list(bpy.context.scene.objects),'Operator supplied local scene copy; no edits or file save.')]
    for eid,label,objects,scope in batches:
        data=report(eid,label,objects,scope);path=safe_output(a.output_dir,'blender-'+label+'.json')
        with path.open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2,allow_nan=False)
        print('VDN_BLENDER_REPORT',str(path))


if __name__=='__main__':main()
