"""Reimport repaired bevel UVs and retain fine profiles with full-precision UVs."""
import unreal as u,json,ast,traceback
from pathlib import Path
R=ROOT=Path(__file__).resolve().parents[3];BASE='/Game/Kalmar';assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='import_task'];exec(compile(tree,'import_helpers','exec'))
report={'status':'running','meshes':[]}
try:
 repaired={x['name'] for x in json.loads((R/'previews/exterior-uv-repaired.json').read_text())}
 for spec in json.loads((R/'exports/manifest.json').read_text())['assets']:
  name=spec['name']
  if not name.startswith('SM_Kalmar_Domkyrka'):continue
  mesh=u.load_asset(BASE+'/Meshes/'+name)
  if name in repaired:
   opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False
   opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
   data=opt.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False;data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False;data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
   mesh=import_task(R/'exports'/spec['file'],BASE+'/Meshes',name,opt)
   for i,slot in enumerate(mesh.static_materials):mesh.set_material(i,u.load_asset(BASE+'/Materials/'+str(slot.get_editor_property('imported_material_slot_name'))))
  build=smes.get_lod_build_settings(mesh,0)
  if not build.use_full_precision_u_vs:
   build.use_full_precision_u_vs=True;smes.set_lod_build_settings(mesh,0,build)
  library.save_loaded_asset(mesh)
  report['meshes'].append({'name':name,'reimported':name in repaired,'full_precision_uv':bool(smes.get_lod_build_settings(mesh,0).use_full_precision_u_vs)})
  (R/'previews/exterior-uv-unreal.json').write_text(json.dumps(report,indent=2))
 report['status']='passed';u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
except Exception:
 report['status']='failed';report['error']=traceback.format_exc();raise
finally:(R/'previews/exterior-uv-unreal.json').write_text(json.dumps(report,indent=2))
