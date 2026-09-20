"""Split large disconnected architectural assemblies into compact Lumen meshes.
Preserves every vertex, material, smooth flag and UV loop. No visible simplification.
"""
from collections import defaultdict
partition_report=[]
for source_name in ['SM_Kalmar_Domkyrka','SM_Domkyrka_Interior_Architecture','SM_Domkyrka_Pews','SM_Domkyrka_Galleries','SM_Domkyrka_Ionic_Details']:
 obj=bpy.data.objects.get(source_name)
 if not obj:continue
 me=obj.data;parent=list(range(len(me.vertices)))
 def root(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for e in me.edges:
  a,b=map(root,e.vertices)
  if a!=b:parent[b]=a
 islands=defaultdict(list)
 for f in me.polygons:islands[root(f.vertices[0])].append(f.index)
 groups=defaultdict(list)
 for faces in islands.values():
  ids={v for fi in faces for v in me.polygons[fi].vertices}
  coords=[me.vertices[i].co for i in ids]
  lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
  center=[(a+b)/2 for a,b in zip(lo,hi)]
  level='Ground' if hi[2]<1.5 else ('High' if lo[2]>13 else 'Lower')
  if source_name=='SM_Domkyrka_Interior_Architecture' and hi[2]-lo[2]>8 and hi[0]-lo[0]>8 and hi[1]-lo[1]>8:
   key=('Vault',len(groups),0)
  else:key=(level,math.floor(center[0]/10),math.floor(center[1]/10))
  groups[key].extend(faces)
 for index,(key,faces) in enumerate(sorted(groups.items())):
  ids=sorted({v for fi in faces for v in me.polygons[fi].vertices});remap={v:i for i,v in enumerate(ids)}
  data=bpy.data.meshes.new(source_name+f'_Part{index:02d}')
  data.from_pydata([me.vertices[i].co for i in ids],[],[tuple(remap[v] for v in me.polygons[fi].vertices) for fi in faces]);data.update()
  for ma in me.materials:data.materials.append(ma)
  uv=data.uv_layers.new(name='UVMap')
  for new,old_id in zip(data.polygons,faces):
   old=me.polygons[old_id];new.material_index=old.material_index;new.use_smooth=old.use_smooth
   for ni,oi in zip(new.loop_indices,old.loop_indices):uv.data[ni].uv=me.uv_layers.active.data[oi].uv
  part=bpy.data.objects.new(source_name+f'_Part{index:02d}',data);bpy.context.collection.objects.link(part);part['category']=obj['category'];part['lumen_partition']=True
 partition_report.append({'source':source_name,'parts':len(groups),'vertices_before':len(me.vertices)})
 bpy.data.objects.remove(obj,do_unlink=True)
(R/'exports/lumen-partitions.json').write_text(json.dumps(partition_report,indent=2))
