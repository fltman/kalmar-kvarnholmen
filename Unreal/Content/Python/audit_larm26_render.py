"""Read actual render buffers for the imported district and record any bad frames."""
import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];result={}
names=json.loads((R/'previews/larm26-build.json').read_text())['changed']
for name in names:
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name);c={'vertices':0,'zero_tangents':0,'zero_normals':0,'nonfinite_vectors':0,'nonunit_vectors':0}
 for i in range(mesh.get_num_sections(0)):
  vs,tris,ns,uvs,ts=u.ProceduralMeshLibrary.get_section_from_static_mesh(mesh,0,i)
  vectors=list(ns)+[t.tangent_x for t in ts]
  lengths=[v.x*v.x+v.y*v.y+v.z*v.z for v in vectors]
  c['nonfinite_vectors']+=sum(not math.isfinite(q) for q in lengths)
  c['nonunit_vectors']+=sum(math.isfinite(q) and abs(q-1)>.05 for q in lengths)
  c['vertices']+=len(vs);c['zero_tangents']+=sum(t.tangent_x.x**2+t.tangent_x.y**2+t.tangent_x.z**2<1e-8 for t in ts);c['zero_normals']+=sum(n.x*n.x+n.y*n.y+n.z*n.z<1e-8 for n in ns)
 result[name]=c
report={'status':'passed' if all(v['vertices']>0 and v['zero_tangents']==0 and v['zero_normals']==0 and v['nonfinite_vectors']==0 and v['nonunit_vectors']==0 for v in result.values()) else 'review_required','meshes':result}
(R/'previews/larm26-render-audit.json').write_text(json.dumps(report,indent=2))
