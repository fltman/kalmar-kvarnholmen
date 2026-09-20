"""Isolated Blender roof/entrance check without modifying the saved scene."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
for o in list(bpy.data.objects):
 if o.type=='MESH' and o.name!='SM_Kvarnholmen_House_92204184':bpy.data.objects.remove(o,do_unlink=True)
 elif o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.camera=bpy.data.objects['106_KaggensCorner22'];s.world=bpy.data.worlds.new('Corner study');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.40,.50,.66,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.7
bpy.ops.object.light_add(type='SUN');o=bpy.context.object;o.data.energy=3;o.rotation_euler=(math.radians(25),math.radians(-35),math.radians(-25));o.data.angle=math.radians(3)
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1200;s.render.resolution_y=750;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(R/'previews/street22-corner-blender.png');bpy.ops.render.render(write_still=True)
