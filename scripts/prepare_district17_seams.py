import sys,json,math
from pathlib import Path

from shapely.geometry import Polygon,LineString
from shapely.ops import transform
R=Path(__file__).resolve().parents[1];p=R/'source/district17.json';d=json.loads(p.read_text());bs={b['id']:b for b in json.loads((R/'source/kvarnholmen.json').read_text())['buildings']}
for bid,H,depth,street in [('93238156',10.4,10,'Norra Långgatan'),('90859847',7.9,10.8,'Fiskaregatan'),('91926329',6.15,8.4,'Norra Långgatan'),('92412873',7.65,10.8,'Ölandsgatan')]:
 r=d['buildings']['SM_Kvarnholmen_House_'+bid];w=max([w for w in r['walls'] if w['frontage'] and w['street']==street and w['exposed']],key=lambda w:w['length']);p0,q=w['p'],w['q'];a=math.atan2(q[1]-p0[1],q[0]-p0[0]);co,si=math.cos(a),math.sin(a)
 def local(x,y,z=None):return ((x-p0[0])*co+(y-p0[1])*si,-(x-p0[0])*si+(y-p0[1])*co)
 def world(x,y,z):return (p0[0]+x*co-y*si,p0[1]+x*si+y*co,z)
 cuts=[(0,0),(depth/2,3.2),(depth,0)]
 if bid=='91926329':cuts=[(0,0),(depth*.22,2.35),(depth/2,3.1),(depth*.78,2.35),(depth,0)]
 seams=[]
 for po in bs[bid]['polygons']:
  poly=transform(local,Polygon(po['outer'],po['holes']))
  for i in range(math.ceil(poly.bounds[0]/.65),math.floor(poly.bounds[2]/.65)+1):
   x=i*.65
   for (y,z),(yy,zz) in zip(cuts,cuts[1:]):
    g=poly.intersection(LineString([(x,y),(x,yy)]));parts=[g] if g.geom_type=='LineString' else list(getattr(g,'geoms',[]))
    for seg in parts:
     if seg.geom_type!='LineString' or seg.length<.1:continue
     coords=list(seg.coords);seams.append([world(u,v,H+.045+z+(zz-z)*(v-y)/(yy-y)) for u,v in [coords[0],coords[-1]]])
 r['authored_roof_seams']=seams
p.write_text(json.dumps(d,indent=2,ensure_ascii=False))
