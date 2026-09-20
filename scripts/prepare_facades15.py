"""Inventory blank masses and find genuinely exposed wall intervals, retaining mapped passages."""
from pathlib import Path
import json,math
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/kvarnholmen.json').read_text());M=json.loads((R/'exports/manifest.json').read_text())
candidates={a['name'].removeprefix('SM_Kvarnholmen_House_') for a in M['assets'] if a['category']=='Kvarnholmen/Building massing'}
# Retain inventory for repeatable rebuilds after categories have changed.
if not candidates and (R/'source/facades15.json').exists():candidates=set(json.loads((R/'source/facades15.json').read_text())['buildings'])
polys={b['id']:unary_union([Polygon(p['outer'],p['holes']) for p in b['polygons']]) for b in D['buildings']}
roads=unary_union([LineString(q['points']) for q in D['roads'] if len(q['points'])>1]);out={}
for b in D['buildings']:
 if b['id'] not in candidates:continue
 shape=polys[b['id']];neighbours=unary_union([p.buffer(.22) for bid,p in polys.items() if bid!=b['id'] and p.distance(shape)<.3]);walls=[]
 tiers=[(b['base_polygons'],-.1,min(3.4,b['height'])),(b['polygons'],3.4,b['height'])] if b['has_passage'] else [(b['polygons'],-.1,b['height'])]
 for tier,(ps,z0,z1) in enumerate(tiers):
  if z1<=z0:continue
  for po in ps:
   pg=orient(Polygon(po['outer'],po['holes']),sign=1)
   for ring in [pg.exterior]+list(pg.interiors):
    coords=list(ring.coords)
    for p,q in zip(coords,coords[1:]):
     ln=LineString([p,q]);L=ln.length
     if L<.08:continue
     diff=ln.difference(neighbours);parts=[diff] if diff.geom_type=='LineString' else list(getattr(diff,'geoms',[]));intervals=[]
     for seg in parts:
      if seg.geom_type!='LineString' or seg.length<1.4:continue
      a,c=sorted([ln.project(Point(seg.coords[0])),ln.project(Point(seg.coords[-1]))]);intervals.append([a,c])
     mid=ln.interpolate(.5,normalized=True);a=math.atan2(q[1]-p[1],q[0]-p[0]);probe=Point(mid.x+math.sin(a)*2,mid.y-math.cos(a)*2)
     walls.append(dict(p=p,q=q,length=L,z0=z0,z1=z1,exposed=intervals,road_distance=probe.distance(roads),tier=tier))
 possible=[i for i,w in enumerate(walls) if w['z0']<0 and any(v-u>2.2 for u,v in w['exposed'])]
 door=min(possible,key=lambda i:walls[i]['road_distance']) if possible else None
 out[b['id']]={'walls':walls,'entrance_wall':door,'name':b['tags'].get('name'),'style':'modern' if b['roof']=='flat' or b['tags'].get('building') in ['office','retail','commercial'] else ('timber' if b['height']<4.5 and int(b['id'])%4==0 else 'traditional'),'reference_status':'inferred from mapped footprint and estimated storeys; individual facade unverified'}
report={'buildings':out,'count':len(out),'exposed_wall_segments':sum(bool(w['exposed']) for b in out.values() for w in b['walls']),'preserves_mapped_passages':True}
(R/'source/facades15.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('FACADE_INVENTORY',report['count'],report['exposed_wall_segments'])
