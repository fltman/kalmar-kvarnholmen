import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
names=json.loads((R/'previews/town-pass9-scope.json').read_text())['changed'];report={}
for name in names:
 me=bpy.data.objects[name].data;me.calc_loop_triangles();uv=me.uv_layers.active.data;bad=[]
 for t in me.loop_triangles:
  a,b,c=[uv[i].uv for i in t.loops];v=b-a;w=c-a
  if abs(v.x*w.y-v.y*w.x)<1e-12:bad.append({'polygon':t.polygon_index,'area':t.area})
 report[name]={'zero_uv_triangles':len(bad),'examples':bad[:12]}
(R/'previews/town-pass9-uv.json').write_text(json.dumps(report,indent=2));print(report)
