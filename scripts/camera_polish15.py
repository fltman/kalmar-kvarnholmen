import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'));spec=next(c for c in json.loads((R/'exports/manifest.json').read_text())['cameras'] if c['name']=='49_Fiskaregatan');obj=bpy.data.objects[spec['name']];obj.location=spec['location'];obj.rotation_euler=(Vector(spec['target'])-obj.location).to_track_quat('-Z','Y').to_euler();bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'));print('CAMERA15_SAVED')
