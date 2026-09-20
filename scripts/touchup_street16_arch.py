"""Raise the belt course above arched glazing, keeping the rest of the mesh intact."""
import bpy,json,bmesh,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
name='SM_Building_92204194';obj=bpy.data.objects[name];me=obj.data
adj={v.index:set() for v in me.vertices}
for e in me.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();moved=0
for i in adj:
 if i in seen:continue
 component=set();stack=[i]
 while stack:
  k=stack.pop()
  if k in component:continue
  component.add(k);stack.extend(adj[k]-component)
 seen.update(component);vs=[me.vertices[k].co for k in component]
 z0=min(v.z for v in vs);z1=max(v.z for v in vs);width=max(v.x for v in vs)-min(v.x for v in vs)
 if abs((z0+z1)/2-3.45)<.005 and abs(z1-z0-.13)<.005 and width>12:
  for k in component:me.vertices[k].co.z+=.72
  moved+=len(component)
assert moved==8,moved
me.update();bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
exec(compile((R/'scripts/district_tangent_export.py').read_text(),'district_tangent_export.py','exec'));export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
(R/'previews/street16-arch-touchup.json').write_text(json.dumps({'status':'passed','vertices_moved':moved,'belt_height':4.17}))
