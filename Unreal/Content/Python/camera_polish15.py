import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem);spec=next(c for c in json.loads((R/'exports/manifest.json').read_text())['cameras'] if c['name']=='49_Fiskaregatan');v=lambda p:u.Vector(p[0]*100,-p[1]*100,p[2]*100)
a=next(a for a in ae.get_all_level_actors() if a.get_actor_label()==spec['name']);a.set_actor_location(v(spec['location']),False,False);a.set_actor_rotation(u.MathLibrary.find_look_at_rotation(v(spec['location']),v(spec['target'])),False);u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
