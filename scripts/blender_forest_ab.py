"""Trusted, fixed procedural foliage experiment. No external assets or Web code.

Run only through agent.forest_lab's explicit local Blender capability.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

import bpy
from mathutils import Vector


def write(path, value):
    if path.exists():raise ValueError('retain prior experiment output')
    path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def asset_objects():
    return [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('eponge_asset')]


def counts(objects):
    triangles=0
    for o in objects:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
    return {'triangles':triangles,'objects':len(objects)}


def material(name, color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1);bsdf.inputs['Roughness'].default_value=.8
    return m


def mesh(name,verts,faces,mat):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['eponge_asset']=True;return o


def configure_render(scene,controls):
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=controls['samples']
    # Some packaged Blender builds lack OpenImageDenoise. This experiment does
    # not need denoising; apply identical raw settings to both arms explicitly.
    scene.cycles.use_denoising=False
    for layer in scene.view_layers:layer.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=1
    scene.render.resolution_x=controls['resolution'];scene.render.resolution_y=controls['resolution'];scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'


def build(asset, amplitude, spec):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    random.seed(spec['controls']['seed'])
    p=spec['assets'][asset];tiers=p['tiers'];branches=p['branches'];height=p['height_m'];radius=p['radius_m'];verts=[];faces=[];depths=[]
    for tier in range(tiers):
        z=.55+((height-.8)*tier/max(1,tiers-1));length=radius*(1-.78*tier/tiers)
        for branch in range(branches):
            angle=2*math.pi*branch/branches+.31*tier+random.uniform(-.08,.08);start=len(verts);zs=[]
            for step in range(5):
                t=step/4;dist=length*(.12+.88*t);width=length*.18*(1-.75*t);cz=z-amplitude*length*t*t;zs.append(cz)
                for sign in (-1,1):verts.append((math.cos(angle)*dist-math.sin(angle)*width*sign,math.sin(angle)*dist+math.cos(angle)*width*sign,cz))
            for step in range(4):
                a=start+step*2;faces.append((a,a+1,a+3,a+2))
            depths.append(max(zs)-min(zs))
    mesh('foliage',verts,faces,material('needles',(.025,.085,.04)))
    snow=[(x*.96,y*.96,z+.018) for x,y,z in verts]
    mesh('snow_caps',snow,faces,material('snow',(.72,.78,.86)))
    bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=.11,radius2=.035,depth=height,location=(0,0,height/2))
    trunk=bpy.context.object;trunk.name='trunk';trunk['eponge_asset']=True;trunk.data.materials.append(material('bark',(.1,.06,.025)))
    scene=bpy.context.scene;configure_render(scene,spec['controls']);scene.world=bpy.data.worlds.new('night');scene.world.color=(.008,.012,.025)
    scene.view_settings.view_transform='Standard'
    bpy.ops.object.camera_add(location=spec['controls']['camera']);cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.2;scene.camera=cam
    bpy.ops.object.light_add(type='SPOT',location=spec['controls']['spot_position']);lamp=bpy.context.object;lamp.rotation_euler=(Vector((0,0,1.7))-lamp.location).to_track_quat('-Z','Y').to_euler();lamp.data.energy=spec['controls']['spot_power_W'];lamp.data.spot_size=math.radians(70);lamp.data.spot_blend=.3
    return {**counts(asset_objects()),'mean_branch_depth_m':sum(depths)/len(depths),'branch_count':len(depths),'amplitude':amplitude}


def main():
    argv=sys.argv[sys.argv.index('--')+1:];p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--phase',choices=['generate','verify'],required=True);a=p.parse_args(argv)
    out=Path(a.output).resolve();root=Path.cwd().resolve()
    if not out.is_relative_to(root/'lab/inbox/forest') or any(q.is_symlink() for q in (Path(a.output),*Path(a.output).parents)):raise ValueError('isolated generated laboratory required')
    spec=json.loads((out/'spec.json').read_text(encoding='utf-8'));start=time.monotonic();rows=[]
    if spec['schema']!='vdn.forest-ab/1' or spec['controls']['blender_version']!=bpy.app.version_string:raise ValueError('version or plan mismatch')
    for asset in ('spruce','shrub'):
        for variant in ('A','B'):
            key=asset+'-'+variant
            if a.phase=='generate':
                metrics=build(asset,spec['variants'][variant]['camber_ratio'],spec)
                for o in bpy.context.scene.objects:o.select_set(bool(o.get('eponge_asset')))
                bpy.context.view_layer.objects.active=asset_objects()[0]
                bpy.ops.wm.obj_export(filepath=str(out/(key+'.obj')),export_selected_objects=True,export_materials=False,export_triangulated_mesh=True)
                bpy.ops.wm.save_as_mainfile(filepath=str(out/(key+'.blend')),check_existing=False)
                bpy.context.scene.render.filepath=str(out/(key+'.png'));bpy.ops.render.render(write_still=True)
                image=bpy.data.images.get('Render Result')
                rows.append({'asset':asset,'variant':variant,'metrics':metrics,'capture_exists':(out/(key+'.png')).stat().st_size>100,'blend':key+'.blend','obj':key+'.obj','capture':key+'.png'})
            else:
                bpy.ops.wm.open_mainfile(filepath=str(out/(key+'.blend')),load_ui=False,use_scripts=False)
                reopened=counts(asset_objects());bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
                bpy.ops.wm.obj_import(filepath=str(out/(key+'.obj')));imported=counts([o for o in bpy.context.scene.objects if o.type=='MESH'])
                rows.append({'asset':asset,'variant':variant,'reopened':reopened,'obj_imported':imported})
    write(out/(a.phase+'.json'),{'schema':'vdn.forest-blender-result/1','phase':a.phase,'blender_version':bpy.app.version_string,'duration_s':time.monotonic()-start,'rows':rows,'Roblox_executed':False,'human_aesthetic_review':'NOT_TESTED'})


if __name__=='__main__':main()
