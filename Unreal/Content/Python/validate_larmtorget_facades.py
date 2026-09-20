"""Facade-pass regression checks: walking clearance, floor and authored mesh settings."""
import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3]
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
vec=lambda x,y,z:u.Vector(x*100,-y*100,z*100)
paths=[('street_to_square',(-280,-2.8),(-307,-2.8)),('north_frontage',(-334,24),(-297,24)),('south_frontage',(-333,-26),(-298,-26)),('theatre_approach',(-305,12),(-341.5,12))]
report={'status':'testing','paths':[],'floor':[],'meshes':[]}
for label,start,end in paths:
 hit=u.SystemLibrary.capsule_trace_single(world,vec(*start,1.0),vec(*end,1.0),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 report['paths'].append({'name':label,'clear':hit is None})
 for p in [start,end]:
  hit=u.SystemLibrary.line_trace_single(world,vec(*p,.6),vec(*p,-.3),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  report['floor'].append({'point':p,'present':hit is not None})
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
for name in json.loads((R/'previews/larmtorget-facades-build.json').read_text())['changed']:
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name);settings=smes.get_lod_build_settings(mesh,0)
 matches=[a for a in actors if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==mesh]
 report['meshes'].append({'name':name,'actors':len(matches),'imported_tangents':not settings.recompute_tangents,'full_precision_uv':settings.use_full_precision_u_vs,'nanite':smes.get_nanite_settings(mesh).enabled})
report['status']='passed' if all(p['clear'] for p in report['paths']) and all(p['present'] for p in report['floor']) and all(m['actors']==1 and m['full_precision_uv'] and m['nanite'] for m in report['meshes']) else 'failed'
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
(R/'previews/larmtorget-facades-validation.json').write_text(json.dumps(report,indent=2))
