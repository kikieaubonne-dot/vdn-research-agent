"""Read-only staged-asset inspection. No save, render, script or Web execution."""
import argparse,json,sys,math
from pathlib import Path
import bpy


def display_helpers(scene):
    helpers={}
    for rig in scene.objects:
        if rig.type!='ARMATURE':continue
        for bone in rig.pose.bones:
            shape=bone.custom_shape
            if shape is not None and shape.type=='MESH' and shape.hide_render:
                helpers.setdefault(shape.name,[]).append(rig.name+'/'+bone.name)
    return helpers


def inspect_scene():
    scene=bpy.context.scene
    if len(scene.objects)>128:raise ValueError('object cap')
    objects=[];armatures=[];triangles=0;raw_triangles=0;helper_refs=display_helpers(scene);helpers=[]
    for obj in scene.objects:
        if obj.type=='MESH':
            m=obj.data;m.calc_loop_triangles();n=len(m.loop_triangles);raw_triangles+=n
            if raw_triangles>200000 or len(m.vertices)>100000:raise ValueError('geometry cap')
            if obj.name in helper_refs:
                helpers.append({'name':obj.name,'triangles':n,'reason':'hidden-render bone custom shape','bone_references':helper_refs[obj.name]});continue
            triangles+=n
            groups={g.index:g.name for g in obj.vertex_groups};weights=[sum(g.weight for g in v.groups if g.group in groups) for v in m.vertices]
            objects.append({'name':obj.name[:120],'triangles':n,'vertices':len(m.vertices),'dimensions':list(obj.dimensions),'matrix_world':[list(row) for row in obj.matrix_world],'uv_layers':len(m.uv_layers),'custom_normals':getattr(m,'has_custom_normals',None),'max_influences':max((len(v.groups) for v in m.vertices),default=0),'unweighted_vertices':sum(w<1e-6 for w in weights),'weight_sum_min':min(weights,default=0),'weight_sum_max':max(weights,default=0),'armature_modifiers':sum(x.type=='ARMATURE' for x in obj.modifiers),'negative_determinant':obj.matrix_world.determinant()<0})
        elif obj.type=='ARMATURE':
            if len(obj.data.bones)>128:raise ValueError('bone cap')
            armatures.append({'name':obj.name,'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(b.head_local),'tail':list(b.tail_local)} for b in obj.data.bones]})
    materials=[]
    for m in bpy.data.materials:
        nodes=m.node_tree.nodes if m.use_nodes else [];images=[n.image for n in nodes if n.type=='TEX_IMAGE' and n.image]
        materials.append({'name':m.name[:120],'diffuse_rgba':list(m.diffuse_color),'surface_render_method':getattr(m,'surface_render_method','UNKNOWN'),'textures':[{'name':im.name,'file':im.filepath[:300],'packed':bool(im.packed_file),'size':list(im.size)} for im in images]})
    actions=[{'name':a.name,'frame_range':list(a.frame_range),'fcurves':len(a.fcurves) if hasattr(a,'fcurves') else None} for a in bpy.data.actions]
    ranges=[a.frame_range for a in bpy.data.actions];start=min((v[0] for v in ranges),default=scene.frame_start);end=max((v[1] for v in ranges),default=scene.frame_end);samples=[]
    for fraction in (0,.5,1):
        frame=start+(end-start)*fraction;scene.frame_set(int(frame),subframe=frame-int(frame));deps=bpy.context.evaluated_depsgraph_get();meshes=[];rigs=[]
        for obj in scene.objects:
            if obj.type=='MESH' and obj.name not in helper_refs:
                evaluated=obj.evaluated_get(deps);m=evaluated.to_mesh()
                try:
                    points=[evaluated.matrix_world@v.co for v in m.vertices]
                    if points:meshes.append({'name':obj.name,'world_min':[min(v[i] for v in points) for i in range(3)],'world_max':[max(v[i] for v in points) for i in range(3)],'centroid':[sum(v[i] for v in points)/len(points) for i in range(3)]})
                finally:evaluated.to_mesh_clear()
            elif obj.type=='ARMATURE':rigs.append({'name':obj.name,'bones':[{'name':p.name,'head':list(obj.matrix_world@p.head),'tail':list(obj.matrix_world@p.tail)} for p in obj.pose.bones]})
        samples.append({'fraction':fraction,'frame':frame,'meshes':meshes,'rigs':rigs})
    return {'schema':'vdn.asset-inspection/1','blender_version':bpy.app.version_string,'objects':objects,'armatures':armatures,'materials':materials,'actions':actions,'pose_samples':samples,'triangles':triangles,'scene_mesh_triangles':raw_triangles,'display_helpers':helpers,'units':{'system':scene.unit_settings.system,'scale_length':scene.unit_settings.scale_length},'dependencies':{'libraries':[l.filepath for l in bpy.data.libraries],'images':[im.filepath for im in bpy.data.images if im.filepath]},'Roblox_compatibility':'NOT_TESTED','untrusted_data':True,'input_saved':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root=Path.cwd().resolve();source=(root/a.input).resolve();output=(root/a.output).resolve()
    if not source.resolve().is_relative_to(root/'lab/inbox') or not output.resolve().is_relative_to(root/'lab/learning'):raise ValueError('staged sandbox paths required')
    if output.exists():raise ValueError('new report only')
    suffix=source.suffix.lower()
    if suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source.resolve()),load_ui=False,use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if suffix=='.obj':bpy.ops.wm.obj_import(filepath=str(source.resolve()))
        elif suffix=='.fbx':bpy.ops.import_scene.fbx(filepath=str(source.resolve()))
        elif suffix in ('.gltf','.glb'):bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        else:raise ValueError('unsupported asset')
    output.write_text(json.dumps(inspect_scene(),allow_nan=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
