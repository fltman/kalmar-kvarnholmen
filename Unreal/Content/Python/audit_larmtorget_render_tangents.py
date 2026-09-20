import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];report={}
for name in json.loads((R/'previews/larmtorget-facades-build.json').read_text())['changed']:
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name);counts={'vertices':0,'zero_tangents':0,'zero_normals':0}
 for i in range(mesh.get_num_sections(0)):
  vs,tris,ns,uvs,ts=u.ProceduralMeshLibrary.get_section_from_static_mesh(mesh,0,i)
  counts['vertices']+=len(vs)
  counts['zero_tangents']+=sum(t.tangent_x.x**2+t.tangent_x.y**2+t.tangent_x.z**2<1e-8 for t in ts)
  counts['zero_normals']+=sum(n.x**2+n.y**2+n.z**2<1e-8 for n in ns)
 report[name]=counts
(R/'previews/larmtorget-render-tangent-audit.json').write_text(json.dumps(report,indent=2))
