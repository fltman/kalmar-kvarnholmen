from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'review_scene.py').read_text(),str(P/'review_scene.py'),'exec'))
cam=next(a for a in actors if a.get_actor_label()=='13_Predikstol')
loc=u.Vector(1000,-4100,410);target=u.Vector(1820,-5070,640)
cam.set_actor_location(loc,False,False);cam.set_actor_rotation(u.MathLibrary.find_look_at_rotation(loc,target),False)
import math
cam.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*28))))
level.save_current_level()
(R/'previews/review-request.json').write_text(json.dumps({'shots':[['09_Altardetalj','18_Unreal_Altar_Detail2.png'],['10_Orgel_Läktare','19_Unreal_Gallery_Detail2.png'],['12_Altarskulptur','20_Unreal_Sculpture_Detail2.png'],['13_Predikstol','21_Unreal_Pulpit_Detail2.png'],['05_Interiör_Altare','22_Unreal_Interior_Detail2.png']]}))
