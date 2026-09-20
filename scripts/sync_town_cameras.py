import bpy,ast,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
tree=ast.parse((R/'scripts/build_town_details.py').read_text())
cameras=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='town_cameras' for t in n.targets)))
manifest=json.loads((R/'exports/manifest.json').read_text())
for name,loc,target,lens in cameras:
 obj=bpy.data.objects[name];obj.location=loc;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();obj.data.lens=lens
 next(s for s in manifest['cameras'] if s['name']==name).update(location=loc,target=target,lens=lens)
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'));print('TOWN_CAMERAS_SYNCED')
