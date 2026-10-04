"""Pass 108: Kaggensgatan, the generic pass-17 volumes 92204167, 92379295, 92379291, 92204171 and
92379305:
- 92204167 (west side, north of Storgatan): the brown brick three-storey shop house (Klintheims
  Skor) over the southern ~16.3 m of the front; the outline is split at y 30.9 where the brick
  front ends in the contributor photo and a lighter, unseen facade begins (estimated joint);
- 92379295 (SM_Building_92379295, the corner of Storgatan, east side): the salmon rendered house
  with arched shop windows, cream pilasters and a red arched gate (contributor photo, scaled from
  the door), one zone;
- 92379291 (38 Kaggensgatan, corner of Strömgatan): the cream rendered house with two curved
  gables and red brick mansard ends; front range and the Strömgatan wing (unseen, estimated);
- 92204171 (west side, north of the gate at y 232-236): the modern white four-storey frame house
  with recessed glazed balconies over garage doors; the frame block over the southern 9.4 m of the
  front, the garage storey on to the north corner, both to the OSM vertex x -207.45; the rear
  part unseen and kept low;
- 92379305 (40c Kaggensgatan, corner of Strömgatan): the 1960s three-storey office in ribbed
  grey-beige concrete, one zone, flat roof.
Heights from the resected Google panoramas and the two contributor photos (see
references/block108-notes.md). Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block108.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['92204167','92379295','92379291','92204171','92379305']
MESH={i:('SM_Building_'+i if i=='92379295' else 'SM_Kvarnholmen_House_'+i) for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i];assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# Joints: 92204167 at y 30.9 (end of the brick front, estimated +-1.5 m); 92379291 at the OSM line
# x -168.9 (the wing corner); 92204171 at the OSM vertex x -207.45 on its north side.
P=PG['92204167'];b167=P.intersection(half((-192.2,30.9),(-220.6,30.9),True));n167=P.difference(b167)
P=PG['92379291'];c291=P.intersection(half((-168.92,175.77),(-168.77,197.47),True));w291=P.difference(c291)
P=PG['92204171'];f171=P.intersection(half((-207.45,230.0),(-207.45,250.0),False));r171=P.difference(f171)
# The frame block ends at y 245.66 (s 9.4 from the south corner, measured); only the garage storey
# runs on to the north corner.
w171=f171.intersection(half((-190.0,245.66),(-210.0,245.66),True));g171=f171.difference(w171)
GEO={'b167':b167,'n167':n167,'s295':PG['92379295'],'c291':c291,'w291':w291,'w171':w171,'g171':g171,'r171':r171,'o305':PG['92379305']}
# Heights (m) above the pavement: eaves 'height', ridge or roof top 'top'. est=True: not measured.
# roof: 'flat', 'hip', 'mansard' (steep ring and flat top).
spec={
 'b167':dict(height=11.50,top=11.50,roof='flat',osm='92204167'),
 'n167':dict(height=10.50,top=12.30,roof='hip',osm='92204167',est=True),
 's295':dict(height=13.30,top=15.80,roof='mansard',osm='92379295'),
 'c291':dict(height=7.90,top=11.00,roof='mansard',osm='92379291'),
 'w291':dict(height=7.90,top=11.00,roof='mansard',osm='92379291',est=True),
 'w171':dict(height=12.90,top=12.90,roof='flat',osm='92204171'),
 'g171':dict(height=3.10,top=3.10,roof='flat',osm='92204171'),
 'r171':dict(height=6.65,top=6.65,roof='flat',osm='92204171',est=True),
 'o305':dict(height=9.70,top=9.70,roof='flat',osm='92379305'),
}
for z in spec:spec[z]['mesh']=MESH[spec[z]['osm']]
taken=Polygon();zones={}
for name in spec:
 ps=parts(GEO[name].difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope=set(IDS)
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope and len(v['walls'])>=3]
def neighbour_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name,spec[name]['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
out={};report={}
for name,ps in zones.items():
 H=spec[name]['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
foot=unary_union(list(PG.values()));covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block108.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block108-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK108_ZONES_OK' if ok else 'BLOCK108_ZONES_REVIEW')
