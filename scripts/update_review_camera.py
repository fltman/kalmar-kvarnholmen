import bpy
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1]
cam=bpy.data.objects['06_Interiör_Orgel'];cam.location=(20,44.4,3.1);cam.rotation_euler=(Vector((-12,44.4,10))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(r/'source/Stortorget.blend'))
bpy.context.scene.camera=cam;bpy.context.scene.render.filepath=str(r/'previews/06_Interiör_Orgel.png');bpy.ops.render.render(write_still=True)
