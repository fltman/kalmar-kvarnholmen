"""Move the pass-79 review cameras to their manifest transforms (no mesh import)."""
import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];MAN=json.loads((R/'exports/manifest.json').read_text())
actors=u.get_editor_subsystem(u.EditorActorSubsystem);existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
import ast
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'vec','look'}];exec(compile(tree,'camera_helpers','exec'))
for s in MAN['cameras']:
 if not s['name'].startswith(tuple(str(i)+'_' for i in range(390,396))):continue
 cam=existing.get(s['name']) or actors.spawn_actor_from_class(u.CameraActor,vec(s['location']),look(s['location'],s['target']))
 cam.set_actor_label(s['name']);cam.set_folder_path('Review cameras');cam.set_actor_location(vec(s['location']),False,False);cam.set_actor_rotation(look(s['location'],s['target']),False);cam.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*s['lens']))))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
