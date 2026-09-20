import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem)
report={'transforms':[],'rays':[]}
# This world-space structural chunk was displaced 8.3 m from the saved Blender layout.
# Its original location is retained in pulpit-pier-diagnostic.json and the map backup.
for a in ae.get_all_level_actors():
 if a.get_actor_label()=='Domkyrka_Interior_Architecture_Part56':
  loc=a.get_actor_location()
  if abs(loc.x-830)<.01 and abs(loc.y)<.01 and abs(loc.z)<.01:
   a.set_actor_location(u.Vector(0,0,0),False,False)
   report['restored_structural_chunk']={'name':a.get_actor_label(),'from_cm':[830,0,0],'to_cm':[0,0,0]}
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()

for a in ae.get_all_level_actors():
 if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh and a.static_mesh_component.static_mesh.get_name().startswith('SM_Domkyrka_Interior_Architecture'):
  loc=a.get_actor_location();rot=a.get_actor_rotation();sc=a.get_actor_scale3d()
  report['transforms'].append({'name':a.get_actor_label(),'location':[loc.x,loc.y,loc.z],'rotation':[rot.pitch,rot.yaw,rot.roll],'scale':[sc.x,sc.y,sc.z]})
ignore=[a for a in ae.get_all_level_actors() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh and not a.static_mesh_component.static_mesh.get_name().startswith('SM_Domkyrka_Interior_Architecture')]
for y in [-5230,-5170,-5280]:
 hit=u.SystemLibrary.line_trace_single(ue.get_editor_world(),u.Vector(1750,y,640),u.Vector(2400,y,640),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
 report['rays'].append({'y':y,'hit':str(hit)})
(R/'previews/pulpit-pier-restored.json').write_text(json.dumps(report,indent=2))
path=R/'Unreal/Content/Python/repair_exterior_uv.py';exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
path=R/'Unreal/Content/Python/review_hero.py';exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['16_Predikstol_Infästning','36_Unreal_Pulpit_Mounted.png'],['17_Psalmtavla_Infästning','37_Unreal_Hymn_Boards_Mounted.png'],['04_Domkyrkan','38_Unreal_Exterior_Pass6.png'],['19_Tornhuv','39_Unreal_Tower_Pass6.png']]}))
