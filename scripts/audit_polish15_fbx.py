import json,math
from pathlib import Path
from io_scene_fbx import parse_fbx
R=Path(__file__).resolve().parents[1];result={}
def find(e,key):
 if e.id==key:yield e
 for c in e.elems:yield from find(c,key)
for name in json.loads((R/'previews/polish15-build.json').read_text())['changed']:
 root,version=parse_fbx.parse(str(R/'exports/meshes'/(name+'.fbx')))
 item={}
 for key in [b'Normals',b'Tangents',b'Binormals']:
  data=[v for e in find(root,key) for v in e.props[0]];lens=[sum(v*v for v in data[i:i+3])**.5 for i in range(0,len(data),3)]
  item[key.decode()]={'vectors':len(lens),'min_length':min(lens) if lens else None,'near_zero':sum(n<1e-4 for n in lens),'nonfinite':sum(not math.isfinite(n) for n in lens)}
 result[name]=item
(R/'previews/polish15-fbx-audit.json').write_text(json.dumps(result,indent=2))
