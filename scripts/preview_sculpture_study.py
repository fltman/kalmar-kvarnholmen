"""Isolated before/after study; leaves the production scene and exports untouched."""
import bpy,bmesh,math,ast,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
cx=cy=0;GOLD='Study_Gold';IVORY='Study_Ivory';materials={}
for name,color,metal in [(GOLD,(.62,.39,.12),1),(IVORY,(.65,.64,.60),0)]:
 ma=bpy.data.materials.new(name);ma.use_nodes=True;p=ma.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.36;materials[name]=ma
for filename,names in [('build_blender.py',{'Mesh'}),('build_interior.py',{'curve','sphere'})]:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
 exec(compile(tree,filename,'exec'))
for label,file,y in [('Before',R/'source/backups/detail-pass-3/sculpture_helpers.py',-1.15),('After',R/'scripts/sculpture_helpers.py',1.15)]:
 exec(compile(file.read_text(),str(file),'exec'))
 m=Mesh('Study_'+label,'Study');figure(m,0,y,0,2.32,GOLD,'chalice');m.finish()
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,y,-.055));ob=bpy.context.object;ob.scale=(.7,.85,.1);ob.data.materials.append(materials[IVORY])
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.location.z=-.12;bpy.context.object.data.materials.append(materials[IVORY])
world=bpy.data.worlds.new('Study');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.36,.4,1);world.node_tree.nodes['Background'].inputs[1].default_value=.65;bpy.context.scene.world=world
for loc,power,size in [((-3,-4,5),900,5),((2,1,4),1300,3),((-2,4,3),650,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.data.energy=power;ob.data.shape='DISK';ob.data.size=size;ob.rotation_euler=(Vector((0,0,1))-ob.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-7.2,0,2.8));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.16))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=6;s.render.resolution_x=1400;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath=str(R/'previews/28_Sculpture_Study.png')
(R/'source/studies').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/studies/Sculpture_Proportions.blend'))
bpy.ops.render.render(write_still=True)
