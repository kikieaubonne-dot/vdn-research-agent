"""Original snow-method benchmark. Fixed code, no downloaded assets/scripts.

Geometry caps vs Blender procedural color: portability, NOT artistic superiority.
"""
import argparse,json,math,random,sys
from pathlib import Path
import bpy
from mathutils import Vector


def material(name,color,procedural=False,threshold=.98):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes;links=m.node_tree.links;bsdf=n.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1);bsdf.inputs['Roughness'].default_value=.8
    if procedural:
        geometry=n.new('ShaderNodeNewGeometry');separate=n.new('ShaderNodeSeparateXYZ');test=n.new('ShaderNodeMath');test.operation='GREATER_THAN';test.inputs[1].default_value=threshold;mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(*color,1);mix.inputs[2].default_value=(.8,.85,.9,1);links.new(geometry.outputs['Normal'],separate.inputs[0]);links.new(separate.outputs['Z'],test.inputs[0]);links.new(test.outputs[0],mix.inputs[0]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
    return m


def mesh(name,vertices,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update();obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);obj.data.materials.append(mat);obj['benchmark_asset']=True;return obj


def ribbon_face(a):
    return (a,a+2,a+3,a+1)


def build(profile,method,spec):
    bpy.ops.wm.read_factory_settings(use_empty=True);random.seed(spec['seed']);height=3 if profile=='primary' else 1.8;radius=1.05 if profile=='primary' else .58;tiers=8 if profile=='primary' else 6;vertices=[];faces=[]
    for tier in range(tiers):
        z=.4+(height-.7)*tier/(tiers-1);length=radius*(1-.82*tier/tiers)
        for branch in range(7):
            angle=branch*math.tau/7+tier*.38+random.uniform(-.1,.1);start=len(vertices)
            # Two curved surfaces; common base geometry for both methods.
            for step in range(5):
                t=step/4;distance=length*(.1+.9*t);width=length*.19*(1-.8*t);cz=z-.22*length*t*t
                for side in (-1,1):vertices.append((math.cos(angle)*distance-math.sin(angle)*width*side,math.sin(angle)*distance+math.cos(angle)*width*side,cz))
            for step in range(4):
                a=start+step*2;faces.append(ribbon_face(a))
    needles=material('needles-'+method,(.025,.09,.04),method=='procedural',spec.get('snow_mask_threshold',.98));mesh('foliage',vertices,faces,needles)
    if method=='caps':mesh('snow_caps',[(x*.94,y*.94,z+.015) for x,y,z in vertices],faces,material('snow',(.8,.85,.9)))
    bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=.08,radius2=.02,depth=height,location=(0,0,height/2));trunk=bpy.context.object;trunk.name='trunk';trunk['benchmark_asset']=True;trunk.data.materials.append(material('bark',(.12,.065,.025)))
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=2;scene.cycles.use_denoising=False
    for layer in scene.view_layers:layer.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=1;scene.render.resolution_x=256;scene.render.resolution_y=256;scene.render.resolution_percentage=100;scene.world=bpy.data.worlds.new('controlled-night');scene.world.color=(.025,.03,.045)
    bpy.ops.object.camera_add(location=(3.7,-5.5,3));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,1.4))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=4.4;scene.camera=camera
    bpy.ops.object.light_add(type='AREA',location=(2,-3,4));light=bpy.context.object;light.data.energy=350;light.data.size=3;light.rotation_euler=(Vector((0,0,1.4))-light.location).to_track_quat('-Z','Y').to_euler()
    return [o for o in scene.objects if o.get('benchmark_asset')]


def metrics(objects):
    count=0
    for obj in objects:obj.data.calc_loop_triangles();count+=len(obj.data.loop_triangles)
    return {'triangles':count,'mesh_objects':len(objects)}


def native_reference(objects):
    white=green=0;thresholds=[]
    for obj in objects:
        for polygon in obj.data.polygons:
            m=obj.data.materials[polygon.material_index];tests=[n for n in m.node_tree.nodes if n.type=='MATH' and n.operation=='GREATER_THAN'] if m.use_nodes else []
            if tests:
                threshold=float(tests[0].inputs[1].default_value);thresholds.append(threshold);normal=(obj.matrix_world.to_3x3().inverted().transposed()@polygon.normal).normalized()
                if normal.z>threshold:white+=1
                else:green+=1
            else:
                c=m.diffuse_color
                if min(c[:3])>.65:white+=1
                if c[1]>c[0]+.025 and c[1]>c[2]+.025:green+=1
    return {'white_faces':white,'green_faces':green,'thresholds':sorted(set(thresholds)),'scope':'analytic source-normal support for this known owned shader, not visual/model perception'}


def imported_metrics():
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];colors=[];textures=[]
    for obj in objects:
        for slot in obj.material_slots:
            m=slot.material
            if not m:continue
            bsdf=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if m.use_nodes else None
            if bsdf:colors.append(list(bsdf.inputs['Base Color'].default_value)[:3]);textures += [n.image.name for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
    white=any(min(c)>.65 for c in colors);green=any(c[1]>c[0]+.025 and c[1]>c[2]+.025 for c in colors)
    return {**metrics(objects),'white_material_factor':white,'needle_green_material_factor':green,'textures':textures,'color_check_scope':'mechanical imported material-factor inspection; textures require separate visual review','Roblox':'NOT_TESTED'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['generate','inspect','reference'],required=True);p.add_argument('--folder',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root=Path.cwd().resolve();folder=(root/a.folder).resolve()
    if not folder.is_relative_to(root/'lab/inbox/learning') or not folder.is_dir():raise ValueError('owned staged folder required')
    spec=json.loads((folder/'spec.json').read_text());rows=[]
    for profile in ('primary','transfer'):
        for method in spec.get('methods',('caps','procedural')):
            name=profile+'-'+method
            if a.phase=='generate':
                objects=build(profile,method,spec);row={'profile':profile,'method':method,**metrics(objects),'native_reference':native_reference(objects)};bpy.context.scene.render.filepath=str(folder/(name+'.png'));bpy.ops.render.render(write_still=True);bpy.ops.object.select_all(action='DESELECT')
                for obj in objects:obj.select_set(True)
                bpy.context.view_layer.objects.active=objects[0];bpy.ops.export_scene.gltf(filepath=str(folder/(name+'.glb')),export_format='GLB',use_selection=True,export_animations=False)
                bpy.ops.wm.save_as_mainfile(filepath=str(folder/(name+'.blend')),compress=True);row['glb_bytes']=(folder/(name+'.glb')).stat().st_size
            elif a.phase=='inspect':
                bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(folder/(name+'.glb')));row={'profile':profile,'method':method,**imported_metrics()}
            else:
                bpy.ops.wm.open_mainfile(filepath=str(folder/(name+'.blend')),load_ui=False,use_scripts=False);objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];row={'profile':profile,'method':method,'native_reference':native_reference(objects)}
            rows.append(row)
    target=folder/('generated.json' if a.phase=='generate' else 'imported.json' if a.phase=='inspect' else 'native-reference.json')
    if target.exists():raise ValueError('previous evidence retained')
    target.write_text(json.dumps({'schema':'vdn.snow-portability/1','version':bpy.app.version_string,'rows':rows,'scope':'procedural research proxies, not photorealism/B3/C1/Studio'},indent=2)+'\n')


if __name__=='__main__':main()
