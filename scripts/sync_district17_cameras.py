import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
for c in json.loads((R/'source/district17-camera-overrides.json').read_text()).values():
 o=bpy.data.objects[c['name']];o.location=c['location'];o.rotation_euler=(Vector(c['target'])-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=c['lens']
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
