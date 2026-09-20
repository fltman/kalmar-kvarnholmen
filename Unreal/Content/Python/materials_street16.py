"""Assign dedicated fine plaster to nine street meshes, leaving shared materials intact."""
import unreal as u,json,ast
from pathlib import Path
ROOT=R=Path(__file__).resolve().parents[3];BASE='/Game/Kalmar'
MAN=json.loads((R/'exports/manifest.json').read_text());assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'setp','import_task','scalar','material'}];exec(compile(tree,'material_helpers','exec'))
report={}
for name,spec in MAN['materials'].items():
 if not name.startswith('M_Street16_'):continue
 ma=material(name,spec);ma.set_editor_property('two_sided',True);ma.set_editor_property('used_with_nanite',True);u.MaterialEditingLibrary.recompile_material(ma);library.save_loaded_asset(ma)
 normal=u.MaterialEditingLibrary.get_material_property_input_node(ma,u.MaterialProperty.MP_NORMAL);rough=u.MaterialEditingLibrary.get_material_property_input_node(ma,u.MaterialProperty.MP_ROUGHNESS)
 report[name]={'normal':isinstance(normal,u.MaterialExpressionTextureSample),'roughness':isinstance(rough,u.MaterialExpressionTextureSample),'linear_normal':not normal.texture.get_editor_property('srgb'),'flip_green':normal.texture.get_editor_property('flip_green_channel')}
for s in MAN['assets']:
 if not s.get('material_overrides'):continue
 mesh=u.load_asset(BASE+'/Meshes/'+s['name'])
 for idx,slot in enumerate(mesh.static_materials):
  old=str(slot.get_editor_property('imported_material_slot_name'));new=s['material_overrides'].get(old,old);ma=u.load_asset(BASE+'/Materials/'+new)
  if ma and mesh.get_material(idx)!=ma:mesh.set_material(idx,ma)
 library.save_loaded_asset(mesh)
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
assert report and all(all(x.values()) for x in report.values())
(R/'previews/street16-materials.json').write_text(json.dumps({'status':'passed','materials':report},indent=2))
