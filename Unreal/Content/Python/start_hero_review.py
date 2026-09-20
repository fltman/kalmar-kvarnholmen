from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'configure_hero_scene.py').read_text(),str(P/'configure_hero_scene.py'),'exec'))
import unreal as u, json, math
R=P.parents[2]
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
checks={}
for name,start,end,expect in [('doorway',(1010,-2200,300),(1010,-3100,300),False),('aisle',(-800,-4440,280),(2100,-4440,280),False),('floor',(1010,-4440,300),(1010,-4440,0),True)]:
 hit=u.SystemLibrary.line_trace_single(world,u.Vector(*start),u.Vector(*end),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],u.DrawDebugTrace.NONE,True)
 checks[name]=(hit is not None)==expect
mesh=u.load_asset('/Game/Kalmar/Meshes/SM_Domkyrka_Altar_Carving')
box=mesh.get_bounding_box()
checks['sculpture_bounds_finite']=all(math.isfinite(getattr(v,k)) for v in [box.min,box.max] for k in ['x','y','z'])
checks['status']='passed' if all(checks.values()) else 'failed'
(R/'previews/hero-final-geometry-check.json').write_text(json.dumps(checks,indent=2))
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'))
