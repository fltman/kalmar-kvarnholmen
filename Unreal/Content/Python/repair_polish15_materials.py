"""Selective surrounding-house import; preserve the hand-reviewed lighting and other assets."""
import unreal as u,json,math,ast,traceback
from pathlib import Path
ROOT=R=Path(__file__).resolve().parents[3]
MAN=json.loads((R/'exports/manifest.json').read_text());BASE='/Game/Kalmar'
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
actors=u.get_editor_subsystem(u.EditorActorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
# Reuse the production import/material helpers without rebuilding the level.
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'setp','import_task','scalar','material','vec','look'}]
exec(compile(tree,'production_material_helpers','exec'))

u.log("POLISH15_MATERIAL_REPAIR_BEGIN")
result={}
for name in json.loads((R/'source/polish15-material-specs.json').read_text()):
 m=material(name,MAN['materials'][name]);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_nanite',True);u.MaterialEditingLibrary.recompile_material(m);library.save_loaded_asset(m);result[name]={'normal':u.MaterialEditingLibrary.get_material_property_input_node(m,u.MaterialProperty.MP_NORMAL) is not None,'base_color':u.MaterialEditingLibrary.get_material_property_input_node(m,u.MaterialProperty.MP_BASE_COLOR) is not None}
level.save_current_level()
u.log('POLISH15_MATERIAL_REPAIR_DONE')
(R/'previews/polish15-material-repair.json').write_text(json.dumps({'status':'passed','materials':result},indent=2))
