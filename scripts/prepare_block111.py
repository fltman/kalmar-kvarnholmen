"""Pass 111: the last street-facing generic pass-17 volumes scattered round the island:
- 91926352 (50 Storgatan): the 1940s grey-beige rendered block; the four-storey range on the
  street corner (front x 111.4-125.15) and the three-storey wing set back 2.4 m to the east,
  split at the step in the outline (x 125.15);
- 91926324 (Storgatan): the light-grey 1.5-storey house under a red tile saddle roof, one zone;
- 91926325 (Storgatan): the green board gate, the low grey one-storey wing, the white two-storey
  part behind it and the yard behind a white wall with an iron gate; split at the gate's east post
  (x 159.0), the wing's east end (x 163.1, measured) and the back of the wing (y 4.5, estimated);
- 91846953 (1 Proviantgatan): the sage-green two-storey house with the pediment; the front range
  (x >= 164.5, y >= -112.25) and the unseen wing to the south-west;
- 91846937 (30 Ölandsgatan): the small yellow boarded house under a red hip roof, one zone;
- 91931337 (Stationsgatan): the grill kiosk, one zone;
- 149000060 (Ölandskajen): the white corrugated shed, split where the roofline steps down at
  s 17.4 from the east end (measured);
- 91072716 (Larmtorget): Gamla vattentornet, the round tower and its small annex on the east side.
Heights from resected Google panoramas (see references/block111-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block111.py
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
IDS=['91926352','91926324','91926325','91846953','91846937','91931337','149000060','91072716']
MESH={i:('SM_Building_'+i if i=='91926352' else 'SM_Kvarnholmen_House_'+i) for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i];assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# 91926352: the step in the outline at x 125.15 (four-storey range west, wing east).
P=PG['91926352'];m352=P.intersection(half((125.16,1.25),(125.07,31.83),True));w352=P.difference(m352)
# 91926325: gate to x 159.0, wing to x 163.1 and y 4.5, the two-storey part behind, the yard east.
P=PG['91926325'];yd=P.intersection(half((163.1,0),(163.1,20),False));rest=P.difference(yd)
gw=rest.intersection(half((159.0,0),(159.0,20),True)).intersection(half((150,4.5),(170,4.5),False))
lw=rest.difference(half((159.0,0),(159.0,20),True)).intersection(half((150,4.5),(170,4.5),False))
bk=rest.difference(gw).difference(lw)
# 91846953: the front range east of x 164.5 and north of the south wall line; the wing the rest.
P=PG['91846953'];f953=P.intersection(half((164.5,-130),(164.5,-80),False)).intersection(half((150,-112.25),(190,-112.25),True));w953=P.difference(f953)
# 149000060: the roofline steps down 17.4 m from the east end.
E,W=(-404.55,-265.87),(-435.0,-270.69);L=math.dist(E,W);t=((W[0]-E[0])/L,(W[1]-E[1])/L);c=(E[0]+t[0]*17.4,E[1]+t[1]*17.4)
P=PG['149000060'];e060=P.intersection(half(c,(c[0]-t[1],c[1]+t[0]),True));w060=P.difference(e060)
# 91072716: the round tower and the small annex on its east side.
T=PG['91072716'];cx,cy=-331.3,122.45
t716=T.intersection(Point(cx,cy).buffer(7.2,64));a716=T.difference(t716)
GEO={'m352':m352,'w352':w352,'h324':PG['91926324'],'gw325':gw,'lw325':lw,'bk325':bk,'yd325':yd,'f953':f953,'w953':w953,
 'y937':PG['91846937'],'k337':PG['91931337'],'e060':e060,'w060':w060,'t716':t716,'a716':a716}
# Heights (m) above the pavement: eaves 'height', ridge or roof top 'top'. est=True: not measured.
# roof: 'flat', 'hip', 'saddle', 'curved' (the shed's upswept end), 'tower', 'open' (yard, wall only).
spec={
 'm352':dict(height=14.50,top=14.50,roof='flat',osm='91926352'),
 'w352':dict(height=11.00,top=11.00,roof='flat',osm='91926352'),
 'h324':dict(height=4.30,top=9.40,roof='saddle',osm='91926324'),
 'gw325':dict(height=3.00,top=3.00,roof='open',osm='91926325'),
 'lw325':dict(height=3.20,top=4.10,roof='saddle',osm='91926325'),
 'bk325':dict(height=6.40,top=8.20,roof='saddle',osm='91926325',est=True),
 'yd325':dict(height=2.00,top=2.00,roof='open',osm='91926325'),
 'f953':dict(height=8.40,top=10.60,roof='hip',osm='91846953'),
 'w953':dict(height=7.20,top=9.20,roof='hip',osm='91846953',est=True),
 'y937':dict(height=4.20,top=7.20,roof='hip',osm='91846937'),
 'k337':dict(height=3.40,top=5.00,roof='hip',osm='91931337'),
 'e060':dict(height=3.00,top=3.35,roof='flat',osm='149000060'),
 'w060':dict(height=2.60,top=3.60,roof='curved',osm='149000060'),
 't716':dict(height=53.00,top=54.50,roof='tower',osm='91072716'),
 'a716':dict(height=4.00,top=4.00,roof='flat',osm='91072716',est=True),
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
    t_=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+wx*Lw*t_+nx*.3,p[1]+wy*Lw*t_+ny*.3))
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
(R/'source/block111.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block111-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK111_ZONES_OK' if ok else 'BLOCK111_ZONES_REVIEW')
