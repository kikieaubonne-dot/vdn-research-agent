"""Trusted-copy visual bake and independent import probe. No downloaded code.

The controller owns paths, budgets and processes. This script never saves input.
"""
import argparse
import gzip
import json
import sys
from pathlib import Path
import bpy


def samples(arm,start,end):
    scene=bpy.context.scene
    meshes=[o for o in scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==arm for m in o.modifiers)]
    if not meshes or len(meshes)>32 or len(arm.pose.bones)>128:raise ValueError('bounded skinned actor required')
    result=[]
    for i in range(25):
        fraction=i/24;frame=start+(end-start)*fraction;scene.frame_set(int(frame),subframe=frame-int(frame));deps=bpy.context.evaluated_depsgraph_get()
        bones={p.name:{'head':list(arm.matrix_world@p.head),'tail':list(arm.matrix_world@p.tail),'skin_matrix':[v for row in ((arm.matrix_world@p.matrix)@(arm.matrix_world@p.bone.matrix_local).inverted()) for v in row]} for p in arm.pose.bones}
        shapes={}
        for obj in meshes:
            ev=obj.evaluated_get(deps);mesh=ev.to_mesh()
            try:
                mesh.calc_loop_triangles()
                if len(mesh.loop_triangles)>20000:raise ValueError('geometry cap')
                points=[ev.matrix_world@v.co for v in mesh.vertices];area=0;centroid=[0.,0.,0.]
                for t in mesh.loop_triangles:
                    a,b,c=[points[k] for k in t.vertices];w=(b-a).cross(c-a).length/2;area+=w
                    for axis in range(3):centroid[axis]+=w*(a[axis]+b[axis]+c[axis])/3
                if not area:raise ValueError('nonzero surface required')
                shapes[obj.name]={'triangles':len(mesh.loop_triangles),'min':[min(p[a] for p in points) for a in range(3)],'max':[max(p[a] for p in points) for a in range(3)],'surface_centroid':[c/area for c in centroid]}
            finally:ev.to_mesh_clear()
        result.append({'fraction':fraction,'bones':bones,'meshes':shapes})
    return {'schema':'vdn.animation-samples/1','actor':arm.name,'blender':bpy.app.version_string,'fps':scene.render.fps/scene.render.fps_base,'start_frame':start,'end_frame':end,'duration_s':(end-start)/(scene.render.fps/scene.render.fps_base),'samples':result,'Roblox':'NOT_TESTED'}


def save(path,value,compressed=False):
    if compressed:path=path.with_suffix(path.suffix+'.gz')
    if path.exists():raise ValueError('retain previous evidence')
    raw=(json.dumps(value,allow_nan=False,separators=(',',':'))+'\n').encode('utf-8')
    path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)


def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['bake','probe','reference'],required=True);p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--actor',required=True);p.add_argument('--format',choices=['glb','fbx'],default='glb');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root=Path.cwd().resolve();source=(root/a.input).resolve();out=(root/a.output).resolve()
    if not source.is_relative_to(root/'lab/inbox/learning') or not out.is_relative_to(root/'lab/inbox/learning') or not out.is_dir():raise ValueError('staged laboratory paths required')
    if a.phase in ('bake','reference'):bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if a.format=='glb':bpy.ops.import_scene.gltf(filepath=str(source))
        else:bpy.ops.import_scene.fbx(filepath=str(source))
    arm=bpy.data.objects.get(a.actor)
    if arm is None or arm.type!='ARMATURE' or not arm.animation_data or not arm.animation_data.action:raise ValueError('exact actor with active action required')
    action=arm.animation_data.action;start,end=action.frame_range
    if not 0<end-start<=240:raise ValueError('bounded animation range required')
    if a.phase=='probe':save(out/'imported.json',samples(arm,start,end),True);return
    save(out/'native.json',samples(arm,start,end),True)
    if a.phase=='reference':return
    diagnostics={'active_action':action.name,'nla_tracks':len(arm.animation_data.nla_tracks),'fcurves':[c.data_path for c in action.fcurves],'constraints':{b.name:[c.type for c in b.constraints] for b in arm.pose.bones if b.constraints},'method':'visual pose bake at each integer source frame; remove constraints only on loaded copy','source_saved':False}
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='POSE');bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.nla.bake(frame_start=int(start),frame_end=int(end),step=1,only_selected=True,visual_keying=True,clear_constraints=True,clear_parents=False,use_current_action=False,clean_curves=False,bake_types={'POSE'})
    bpy.ops.object.mode_set(mode='OBJECT')
    for curve in arm.animation_data.action.fcurves:
        for point in curve.keyframe_points:point.interpolation='LINEAR'
    save(out/'baked.json',samples(arm,start,end),True);save(out/'diagnostic.json',diagnostics)
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==arm for m in o.modifiers)]
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [arm]+meshes:obj.select_set(True)
    bpy.context.view_layer.objects.active=arm
    if a.format=='glb':bpy.ops.export_scene.gltf(filepath=str(out/'baked.glb'),export_format='GLB',use_selection=True,export_animations=True,export_force_sampling=True,export_animation_mode='ACTIVE_ACTIONS')
    else:bpy.ops.export_scene.fbx(filepath=str(out/'baked.fbx'),use_selection=True,object_types={'ARMATURE','MESH'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0)
    # Save only this copied actor; retain all other actors in the source file.
    for obj in list(bpy.context.scene.objects):
        if obj not in [arm]+meshes:bpy.data.objects.remove(obj,do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'baked.blend'),compress=True)


if __name__=='__main__':main()
