from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'patch_final_geometry.py').read_text(),str(P/'patch_final_geometry.py'),'exec'))
exec(compile((P/'review_scene.py').read_text(),str(P/'review_scene.py'),'exec'))
(R/'previews/review-request.json').write_text(json.dumps({'shots':[['11_Taköversikt','17_Unreal_Roof_Detail.png'],['09_Altardetalj','15_Unreal_Altar_Detail.png'],['05_Interiör_Altare','09_Unreal_Interior.png']]}))
checks={}
for name,start,end,expect in [('doorway',(1010,-2200,300),(1010,-3100,300),False),('aisle',(-800,-4440,280),(2100,-4440,280),False),('floor',(1010,-4440,300),(1010,-4440,0),True)]:
 hit=u.SystemLibrary.line_trace_single(world,u.Vector(*start),u.Vector(*end),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],u.DrawDebugTrace.NONE,True)
 checks[name]=(hit is not None)==expect
checks['status']='passed' if all(checks.values()) else 'failed'
(R/'previews/unreal-final-collision-check.json').write_text(json.dumps(checks,indent=2))

start=time.monotonic()+15
