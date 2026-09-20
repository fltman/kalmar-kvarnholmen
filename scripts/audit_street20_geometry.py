"""Check deterministic geometry across repeated scoped rebuilds."""
import bpy,json,hashlib,struct
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
names=json.loads((R/'previews/street20-build.json').read_text())['changed'];result={}
for name in names:
 me=bpy.data.objects[name].data;h=hashlib.sha256()
 for v in me.vertices:h.update(struct.pack('<3f',*v.co))
 for p in me.polygons:
  h.update(struct.pack('<II',len(p.vertices),p.material_index));h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
 for uv in me.uv_layers.active.data:h.update(struct.pack('<2f',*uv.uv))
 for m in me.materials:h.update(m.name.encode()+b'\0')
 result[name]={'sha256_geometry_uv_materials':h.hexdigest(),'vertices':len(me.vertices),'polygons':len(me.polygons)}
p=R/'previews/street20-repeatability.json';previous=json.loads(p.read_text()) if p.exists() else None
report={'status':'passed','compared_to_previous':bool(previous),'meshes':result}
if previous:assert previous['meshes']==result,'Scoped rebuild changed geometry on replay'
p.write_text(json.dumps(report,indent=2));print('STREET20_GEOMETRY_OK',bool(previous))
