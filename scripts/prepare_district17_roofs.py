import sys,json,math
from pathlib import Path

from shapely.geometry import Polygon,box
from shapely import constrained_delaunay_triangles
from shapely.ops import transform
R=Path(__file__).resolve().parents[1];p=R/'source/district17.json';d=json.loads(p.read_text());bs={b['id']:b for b in json.loads((R/'source/kvarnholmen.json').read_text())['buildings']}
for bid,H,depth,street in [('93238156',10.4,10.0,'Norra Långgatan'),('90859847',7.9,10.8,'Fiskaregatan'),('91926329',6.15,8.4,'Norra Långgatan'),('92379265',6.8,10.0,'Fiskaregatan'),('92412873',7.65,10.8,'Ölandsgatan')]:
 r=d['buildings']['SM_Kvarnholmen_House_'+bid];w=max([w for w in r['walls'] if w['frontage'] and w['street']==street and w['exposed']],key=lambda w:w['length']);p0,q=w['p'],w['q'];a=math.atan2(q[1]-p0[1],q[0]-p0[0]);co,si=math.cos(a),math.sin(a)
 def local(x,y,z=None):return ((x-p0[0])*co+(y-p0[1])*si,-(x-p0[0])*si+(y-p0[1])*co)
 def world(x,y,z):return (p0[0]+x*co-y*si,p0[1]+x*si+y*co,z)
 cuts=[(-1000,0),(0,0),(depth/2,3.2),(depth,0),(1000,0)]
 if bid=='91926329':cuts=[(-1000,0),(0,0),(depth*.22,2.35),(depth/2,3.1),(depth*.78,2.35),(depth,0),(1000,0)]
 faces=[]
 for po in bs[bid]['polygons']:
  poly=transform(local,Polygon(po['outer'],po['holes']))
  for (v,z),(vv,zz) in zip(cuts,cuts[1:]):
   g=poly.intersection(box(-2000,v,2000,vv))
   for tri in constrained_delaunay_triangles(g).geoms:
    vs=[world(x,y,H+z+(zz-z)*(y-v)/(vv-v)+.025) for x,y in list(tri.exterior.coords)[:3]];faces.append(vs)
  # Closed gables/ends only along true exterior, with splits at pitch breaks.
  for ring in [poly.exterior]+list(poly.interiors):
   cs=list(ring.coords)
   for P,Q in zip(cs,cs[1:]):
    ts=[0,1]+[(v-P[1])/(Q[1]-P[1]) for v,z in cuts[1:-1] if abs(Q[1]-P[1])>1e-6 and 0<(v-P[1])/(Q[1]-P[1])<1]
    for t,tt in zip(sorted(ts),sorted(ts)[1:]):
     pts=[(P[0]+(Q[0]-P[0])*f,P[1]+(Q[1]-P[1])*f) for f in [t,tt]]
     zs=[]
     for x,y in pts:
      for (v,z),(vv,zz) in zip(cuts,cuts[1:]):
       if v-1e-6<=y<=vv+1e-6:zs.append(z+(zz-z)*(y-v)/(vv-v));break
     if max(zs)>.05:faces.append([world(*pts[0],H),world(*pts[1],H),world(*pts[1],H+zs[1]+.025),world(*pts[0],H+zs[0]+.025)])
 r['authored_roof_faces']=faces
p.write_text(json.dumps(d,indent=2,ensure_ascii=False));print('PHOTO_ROOFS',5)
