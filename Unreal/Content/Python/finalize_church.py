from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'patch_final_geometry.py').read_text(),str(P/'patch_final_geometry.py'),'exec'))
exec(compile((P/'review_scene.py').read_text(),str(P/'review_scene.py'),'exec'))
# Keep a roof camera for inspection of all four towers and intersecting roof.
loc=u.Vector(6000,0,5500);target=u.Vector(1000,-4440,1800)
roof=ae.spawn_actor_from_class(u.CameraActor,loc,u.MathLibrary.find_look_at_rotation(loc,target));roof.set_actor_label('11_Taköversikt');roof.set_folder_path('Review cameras');roof.camera_component.set_field_of_view(65)
actors=ae.get_all_level_actors();level.save_current_level()
shots=[['04_Domkyrkan','13_Unreal_Church_Detail.png'],['08_Kyrkoportal','14_Unreal_Portal_Detail.png'],['09_Altardetalj','15_Unreal_Altar_Detail.png'],['10_Orgel_Läktare','16_Unreal_Organ_Detail.png'],['11_Taköversikt','17_Unreal_Roof_Detail.png'],['05_Interiör_Altare','09_Unreal_Interior.png'],['06_Interiör_Orgel','10_Unreal_Organ.png'],['01_Stortorget','04_Unreal_Stortorget.png']]
(R/'previews/review-request.json').write_text(json.dumps({'shots':shots}))
checks={}
for name,start,end,expect in [('doorway',(1010,-2200,300),(1010,-3100,300),False),('aisle',(-800,-4440,280),(2100,-4440,280),False),('floor',(1010,-4440,300),(1010,-4440,0),True)]:
 hit=u.SystemLibrary.line_trace_single(world,u.Vector(*start),u.Vector(*end),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],u.DrawDebugTrace.NONE,True)
 checks[name]=(hit is not None)==expect
checks['status']='passed' if all(checks.values()) else 'failed'
(R/'previews/unreal-final-collision-check.json').write_text(json.dumps(checks,indent=2))
