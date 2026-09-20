"""Make the redistributable snapshot independent of the research-only altar photo."""
from pathlib import Path
import unreal as u,json,math
R=Path(__file__).resolve().parents[3]
ma=u.load_asset('/Game/Kalmar/Materials/M_Altarpiece_Photo')
u.MaterialEditingLibrary.delete_all_material_expressions(ma)
c=u.MaterialEditingLibrary.create_material_expression(ma,u.MaterialExpressionConstant3Vector,0,0);c.constant=u.LinearColor(.23,.17,.10,1)
u.MaterialEditingLibrary.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
r=u.MaterialEditingLibrary.create_material_expression(ma,u.MaterialExpressionConstant,0,140);r.r=.88
u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
ma.set_editor_property('two_sided',True);ma.set_editor_property('used_with_nanite',True);u.MaterialEditingLibrary.recompile_material(ma);u.EditorAssetLibrary.save_loaded_asset(ma)
u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/Kalmar/Maps/Stortorget')
ae=u.get_editor_subsystem(u.EditorActorSubsystem);actors=ae.get_all_level_actors()
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
missing=[]
for a in actors:
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh
  if not m:missing.append(a.get_actor_label())
  elif any(a.static_mesh_component.get_material(i) is None for i in range(len(m.static_materials))):missing.append(a.get_actor_label()+' material')
report={'status':'passed' if not missing else 'failed','actors':len(actors),'missing_meshes_or_materials':missing,'excluded_photo':True}
(R/'previews/public-unreal-validation.json').write_text(json.dumps(report,indent=2));assert not missing
print('PUBLIC_UNREAL_READY')
