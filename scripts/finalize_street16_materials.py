"""Update Blender material assignments without changing the validated mesh geometry."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
text=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()"
exec(compile(text[:text.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
exec(compile((R/'scripts/street16_materials.py').read_text(),'street16_materials.py','exec'))
names=json.loads((R/'previews/street16-build.json').read_text())['changed']
for item in manifest['assets']:
 if item['name'] not in names:continue
 obj=bpy.data.objects[item['name']]
 for idx,ma in enumerate(obj.data.materials):
  if ma.name in street16_material_map:obj.data.materials[idx]=materials[street16_material_map[ma.name]]
 item['material_overrides']=street16_material_map
 item['materials']=[m.name for m in obj.data.materials]
manifest['materials']=specs
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
print('STREET16_MATERIAL_SOURCE_SAVED')
