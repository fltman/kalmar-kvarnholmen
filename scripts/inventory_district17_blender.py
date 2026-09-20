import bpy,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
out={}
for o in bpy.data.objects:
 if o.type!='MESH' or not (o.name.startswith(('SM_Building_','SM_Kvarnholmen_House_')) or o.get('category') in ['Landmarks','Kvarnholmen/Landmarks','Storgatan/Landmarks']):continue
 z=collections.Counter();m=collections.Counter()
 for p in o.data.polygons:
  ma=o.data.materials[p.material_index].name;m[ma]+=p.area
  if abs(p.normal.z)<.1:
   for i in p.vertices:z[round(o.data.vertices[i].co.z,2)]+=p.area/len(p.vertices)
 out[o.name]={'category':o.get('category'),'props':{k:str(v) for k,v in o.items()},'height_modes':z.most_common(12),'materials':m.most_common(),'bbox':[[min(v.co[i] for v in o.data.vertices),max(v.co[i] for v in o.data.vertices)] for i in range(3)],'vertices':len(o.data.vertices)}
(R/'previews/district17/inventory.json').write_text(json.dumps(out,indent=2));print('INVENTORY',len(out))
