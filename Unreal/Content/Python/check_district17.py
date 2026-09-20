from pathlib import Path
import json,unreal as u
P=Path(__file__).resolve().parent;R=P.parents[2]
text=(P/'audit_polish15_render.py').read_text().replace('polish15-build.json','district17-build.json').replace('polish15-render-audit.json','district17-render-audit.json')
exec(compile(text,str(P/'audit_polish15_render.py'),'exec'),{'__file__':str(P/'audit_polish15_render.py')})
text=(P/'validate_kvarnholmen.py').read_text().replace('kvarnholmen-collision.json','district17-collision.json')
exec(compile(text,str(P/'validate_kvarnholmen.py'),'exec'),{'__file__':str(P/'validate_kvarnholmen.py')})
text=(P/'validate_storgatan.py').read_text().replace('storgatan-collision.json','district17-storgatan-collision.json')
exec(compile(text,str(P/'validate_storgatan.py'),'exec'),{'__file__':str(P/'validate_storgatan.py')})

# Verify actual component materials, not just non-null defaults after FBX reimport.
man=json.loads((R/'exports/manifest.json').read_text());names=set(json.loads((R/'previews/district17-build.json').read_text())['changed']);actors={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()};material_report={}
for spec in man['assets']:
 name=spec['name']
 if name not in names:continue
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name);actor=actors[name.removeprefix('SM_')];slots=[]
 for i,slot in enumerate(mesh.static_materials):
  imported=str(slot.get_editor_property('imported_material_slot_name'));expected=spec.get('material_overrides',{}).get(imported,imported);actual=actor.static_mesh_component.get_material(i)
  slots.append({'expected':expected,'actual':actual.get_name() if actual else None,'passed':bool(actual and actual.get_name()==expected)})
 material_report[name]=slots
(R/'previews/district17-bindings.json').write_text(json.dumps({'status':'passed' if len(material_report)==303 and all(q['passed'] for v in material_report.values() for q in v) else 'failed','meshes':material_report},indent=2))

exec(compile((P/'check_klapphuset17.py').read_text(),str(P/'check_klapphuset17.py'),'exec'),{'__file__':str(P/'check_klapphuset17.py')})
