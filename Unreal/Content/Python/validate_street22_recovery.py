"""Check the saved world after editor restart without reloading its map."""
import unreal as u,json,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem);actors=ae.get_all_level_actors();missing=[]
for a in actors:
 if isinstance(a,u.StaticMeshActor):
  mesh=a.static_mesh_component.static_mesh
  if not mesh:missing.append(a.get_actor_label())
  elif any(a.static_mesh_component.get_material(i) is None for i in range(len(mesh.static_materials))):missing.append(a.get_actor_label()+' material')
assert not missing,missing
assert any(a.get_actor_label()=='106_KaggensCorner22' for a in actors)
report={'status':'passed','actors':len(actors),'missing_meshes_or_materials':missing,'final_corner_camera_present':True,'time':datetime.datetime.now().isoformat()}
(R/'previews/street22-recovery-validation.json').write_text(json.dumps(report,indent=2))
print('STREET22_RECOVERY_VALIDATED')
