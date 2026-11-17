"""Original normalized actor/gesture laboratory. No real father reference or UI claim."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector


def output_directory(value,root):
    root=Path(root).resolve();out=(root/Path(value)).resolve()
    if not out.is_relative_to(root/'lab/inbox/learning') or not out.is_dir():raise ValueError('new staged lab required')
    return out


def mat(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*color,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.7;return m


def part(name,loc,scale,bone,arm,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,location=loc);obj=bpy.context.object;obj.name=name;obj.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);obj.data.materials.append(material)
    obj.vertex_groups.new(name=bone).add(list(range(len(obj.data.vertices))),1,'REPLACE');mod=obj.modifiers.new('Rig','ARMATURE');mod.object=arm;obj['actor']=arm.name
    for p in obj.data.polygons:p.use_smooth=True
    return obj


def actor(name,width,method):
    data=bpy.data.armatures.new(name);arm=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(arm);bpy.context.view_layer.objects.active=arm;arm.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    bones={}
    def bone(n,head,tail,parent=None):
        b=data.edit_bones.new(n);b.head=head;b.tail=tail
        if parent:b.parent=bones[parent]
        bones[n]=b
    bone('root',(0,0,.05),(0,0,.48));bone('spine',(0,0,.48),(0,0,.78),'root');bone('neck',(0,0,.78),(0,0,.87),'spine');bone('head',(0,0,.87),(0,0,1),'neck')
    for side,sign in (('L',-1),('R',1)):
        x=sign*.18*width;bone('upper_arm.'+side,(x,0,.78),(x,0,.57),'spine');bone('forearm.'+side,(x,0,.57),(x,0,.36),'upper_arm.'+side);bone('hand.'+side,(x,0,.36),(x,-.02,.30),'forearm.'+side)
        x=sign*.085*width;bone('thigh.'+side,(x,0,.48),(x,0,.26),'root');bone('shin.'+side,(x,0,.26),(x,0,.06),'thigh.'+side);bone('foot.'+side,(x,0,.06),(x,-.08,.03),'shin.'+side)
    bpy.ops.object.mode_set(mode='OBJECT');arm.select_set(False)
    skin=mat(name+'-skin',(.42,.25,.16));cloth=mat(name+'-sweater',(.10,.15,.23));dark=mat(name+'-trousers',(.045,.05,.07))
    pieces=[part(name+'-torso',(0,0,.65),(.18*width,.085,.18),'spine',arm,cloth),part(name+'-head',(0,-.006,.925),(.072,.06,.085),'head',arm,skin)]
    for side,sign in (('L',-1),('R',1)):
        x=sign*.18*width;pieces += [part(name+'-upper_arm.'+side,(x,0,.675),(.038,.04,.12),'upper_arm.'+side,arm,cloth),part(name+'-forearm.'+side,(x,0,.465),(.029,.035,.115),'forearm.'+side,arm,cloth),part(name+'-hand.'+side,(x,-.006,.33),(.026,.025,.04),'hand.'+side,arm,skin)]
        x=sign*.085*width;pieces += [part(name+'-thigh.'+side,(x,0,.37),(.05,.065,.13),'thigh.'+side,arm,dark),part(name+'-shin.'+side,(x,0,.16),(.035,.04,.105),'shin.'+side,arm,dark),part(name+'-shoe.'+side,(x,-.03,.035),(.04,.075,.035),'foot.'+side,arm,dark)]
    target_pos=Vector((-.30*width,-.28,.64));bpy.ops.object.empty_add(location=target_pos);target=bpy.context.object;target.name=name+'-target'
    if method=='IK':
        constraint=arm.pose.bones['forearm.L'].constraints.new('IK');constraint.target=target;constraint.chain_count=2;constraint.use_stretch=False
        for frame,influence in ((1,0),(13,1),(25,0)):constraint.influence=influence;constraint.keyframe_insert('influence',frame=frame)
    else:
        for frame,value in ((1,0),(13,1),(25,0)):
            for n,angle in (('upper_arm.L',.85),('forearm.L',.6)):
                p=arm.pose.bones[n];p.rotation_mode='XYZ';p.rotation_euler.x=angle*value;p.keyframe_insert('rotation_euler',frame=frame)
    head=arm.pose.bones['head'];head.rotation_mode='XYZ'
    for frame,v in ((1,0),(13,.08),(25,0)):head.rotation_euler.z=v;head.keyframe_insert('rotation_euler',frame=frame)
    return arm,pieces,target


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root=Path.cwd().resolve();out=output_directory(a.output,root)
    spec=json.loads((out/'spec.json').read_text());bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=25;scene.render.fps=12
    actors=[]
    for profile,width in (('father_proxy',1),('transfer_proxy',.85)):
        for method in ('FK','IK'):actors.append((profile,method,*actor(profile+'-'+method,width,method)))
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=2;scene.cycles.use_denoising=False
    for layer in scene.view_layers:layer.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=1;scene.render.resolution_x=256;scene.render.resolution_y=256;scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('diagnostic-world');scene.world.color=(.12,.12,.12)
    bpy.ops.object.camera_add(location=(1.7,-3,1.3));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.53))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.3;scene.camera=cam
    bpy.ops.object.light_add(type='AREA',location=(1,-2,3));lamp=bpy.context.object;lamp.data.energy=250;lamp.data.size=3;lamp.rotation_euler=(Vector((0,0,.6))-lamp.location).to_track_quat('-Z','Y').to_euler()
    measurements=[]
    for profile,method,arm,pieces,target in actors:
        for _,_,other,meshes,_ in actors:
            for obj in meshes:obj.hide_render=other!=arm
        scene.frame_set(13);bpy.context.view_layer.update();wrist=arm.matrix_world@arm.pose.bones['forearm.L'].tail;error=(wrist-target.location).length
        feet=[]
        for f in (1,13,25):scene.frame_set(f);bpy.context.view_layer.update();feet.append(list(arm.matrix_world@arm.pose.bones['foot.L'].head))
        scene.frame_set(13);bpy.context.view_layer.update();scene.render.filepath=str(out/(arm.name+'.png'));bpy.ops.render.render(write_still=True)
        for obj in scene.objects:obj.select_set(obj==arm or obj in pieces)
        bpy.context.view_layer.objects.active=arm
        props=bpy.ops.export_scene.gltf.get_rna_type().properties
        kwargs={'filepath':str(out/(arm.name+'.glb')),'export_format':'GLB','use_selection':True,'export_animations':True,'export_force_sampling':True}
        if 'export_animation_mode' in props and 'ACTIVE_ACTIONS' in props['export_animation_mode'].enum_items.keys():kwargs['export_animation_mode']='ACTIVE_ACTIONS'
        bpy.ops.export_scene.gltf(**kwargs)
        triangles=0
        for obj in pieces:obj.data.calc_loop_triangles();triangles+=len(obj.data.loop_triangles)
        measurements.append({'profile':profile,'method':method,'actor':arm.name,'triangles':triangles,'hand_error_normalized':error,'target':list(target.location),'wrist_at_peak':list(wrist),'foot_positions':feet,'blender_version':bpy.app.version_string,'export_options':kwargs,'skeleton':len(arm.data.bones)})
    # One shared .blend avoids duplicating the entire base file for each variant.
    for _,_,_,pieces,_ in actors:
        for obj in pieces:obj.hide_render=False
    scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'prologue-proxies.blend'))
    (out/'measurements.json').write_text(json.dumps({'schema':'vdn.prologue-measures/1','rows':measurements,'controls':spec['controls'],'scope':'normalized engineering proxies, not actual father appearance/height or Roblox validation'},indent=2)+'\n')


if __name__=='__main__':main()
