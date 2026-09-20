"""Mapped green/parking polygons, with schematically marked bays and retained walkways."""
for row in D18['surfaces']:
 m=p18_new('SM_Kvarnholmen_Surface18_'+row['id'],'Kvarnholmen/Green areas' if row['kind']=='green' else 'Kvarnholmen/Parking')
 ma=P18['Grass'] if row['kind']=='green' else 'M_Kvarnholmen_Asphalt';z=.035 if row['kind']=='green' else .018
 for t in row['triangles']:
  v=[(x,y,z) for x,y in t]
  if (Vector(v[1])-Vector(v[0])).cross(Vector(v[2])-Vector(v[0])).z<0:v.reverse()
  m.faces(v,[(0,1,2)],ma)
 for p in row['polygons']:
  for ring in [p['outer']]+p['holes']:
   for p,q in zip(ring,ring[1:]+ring[:1]):
    if row['kind']=='green':m.faces([(*p,-.11),(*q,-.11),(*q,z),(*p,z)],[(0,1,2,3)],TS)
 for bay in row['bays']:
  cs=bay['corners']
  for k in range(4):
   if k==bay['open_side']:continue
   p,q=cs[k],cs[(k+1)%4];ang=math.atan2(q[1]-p[1],q[0]-p[0]);m.box(((p[0]+q[0])/2,(p[1]+q[1])/2,z+.004),(math.dist(p,q),.08,.007),P18['ParkingPaint'],ang)
 obj=p18_finish(m);obj['osm_landuse_id']=row['id'];obj['landuse_name']=row['name'];obj['bay_layout']='inferred from footprint, not regulatory survey'
# Existing earthwork tops get the same clearly green surface, geometry stays unchanged.
for name in ['SM_Kvarnholmen_Vall_Sodra','SM_Kvarnholmen_Vall_Regeringen','SM_Kvarnholmen_Vall_CarolusPhilippus']:
 obj=bpy.data.objects.get(name)
 if not obj:continue
 for i,ma in enumerate(obj.data.materials):
  if ma.name=='M_Landmark_Turf':obj.data.materials[i]=materials[P18['Grass']]
 pass18_names.append(name)
