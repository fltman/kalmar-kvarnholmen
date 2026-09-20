import bpy,bmesh,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
report={}
for name in json.loads((R/'previews/larmtorget-facades-build.json').read_text())['changed']:
 me=bpy.data.objects[name].data.copy();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.calc_tangents()
 bad=[]
 for poly in me.polygons:
  for li in poly.loop_indices:
   loop=me.loops[li]
   if loop.tangent.length<.5 or loop.bitangent.length<.5:
    bad.append({'co':list(me.vertices[loop.vertex_index].co),'mat':me.materials[poly.material_index].name,'normal':list(loop.normal),'tangent':list(loop.tangent),'area':poly.area})
 report[name]={'bad_loops':len(bad),'examples':bad[:20]}
 bpy.data.meshes.remove(me)
(R/'previews/larmtorget-tangent-audit.json').write_text(json.dumps(report,indent=2))
