import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];actors=u.get_editor_subsystem(u.EditorActorSubsystem)
existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
for s in json.loads((R/'exports/manifest.json').read_text())['cameras']:
 if not s['name'].startswith(('23_','24_','25_','26_','27_')):continue
 a=existing[s['name']];a.set_actor_location(vec(s['location']),False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(vec(s['location']),vec(s['target'])),False);a.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*s['lens']))))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
