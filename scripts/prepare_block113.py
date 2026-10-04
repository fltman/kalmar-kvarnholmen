"""Pass 113: the last generic pass-17 volumes near a street, scattered round the island.
Photographed (heights from Google panoramas, see references/block113-notes.md):
- 90977144 (Ölandskajen): the long white one-storey magasin under a grey sheet saddle roof; split
  where the outline steps out 4.2 m to the west (y -221.9) and where the narrow north end with the
  slanting east side begins (y -193.3);
- 91915629 (Skeppsbron): the low light-grey flat-roofed hall; the dark grey north end (5.5 m,
  measured on the west front) is its own zone;
- 91846927 (north shore): the red boarded pavilion under a deep-eaved metal hipped roof;
- 1049819215 (Stationsgatan): the glazed pavilion with the dark flat roof and the P sign.
Not photographed (plain sheds at estimated heights, matching their neighbours):
149000062, 90859836, 90859884, 90859852, 93238185, 93192417, 92204195, 1549543685.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block113.py
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
IDS=['90977144','91915629','91846927','1049819215','149000062','90859836','90859884','90859852','93238185','93192417','92204195','1549543685']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i];assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# 90977144: south range below the step line, the north range, the narrow north end (tip).
P=PG['90977144'];ms=P.intersection(half((-501.79,-221.86),(-485.13,-221.57),False));rest=P.difference(ms)
mt=rest.intersection(half((-502.64,-193.30),(-485.50,-193.23),True));mn=rest.difference(mt)
# 91915629: the dark north end, 5.5 m deep from the north wall.
P=PG['91915629'];sd=P.intersection(half((88.07,-273.51),(105.66,-273.92),True));sl=P.difference(sd)
GEO={'ms':ms,'mn':mn,'mt':mt,'sd':sd,'sl':sl,'pv':PG['91846927'],'bp':PG['1049819215'],
 's062':PG['149000062'],'r836':PG['90859836'],'r884':PG['90859884'],'r852':PG['90859852'],
 'w185':PG['93238185'],'y417':PG['93192417'],'r195':PG['92204195'],'s685':PG['1549543685']}
# Heights (m) above the ground: eaves 'height', ridge or roof top 'top'. est=True: not measured.
# roof: 'saddle' (ridge along the long side), 'hip' (inset hip), 'flat'.
spec={
 'ms':dict(height=4.80,top=9.30,roof='saddle',osm='90977144'),
 'mn':dict(height=4.80,top=8.40,roof='saddle',osm='90977144'),
 'mt':dict(height=4.80,top=6.50,roof='hip',osm='90977144',est=True),
 'sd':dict(height=4.50,top=4.50,roof='flat',osm='91915629'),
 'sl':dict(height=5.00,top=5.00,roof='flat',osm='91915629'),
 'pv':dict(height=3.00,top=5.80,roof='hip',osm='91846927'),
 'bp':dict(height=3.00,top=3.00,roof='flat',osm='1049819215'),
 's062':dict(height=2.80,top=3.30,roof='saddle',osm='149000062',est=True),
 'r836':dict(height=3.20,top=5.80,roof='saddle',osm='90859836',est=True),
 'r884':dict(height=3.20,top=5.80,roof='saddle',osm='90859884',est=True),
 'r852':dict(height=3.20,top=5.80,roof='saddle',osm='90859852',est=True),
 'w185':dict(height=2.80,top=2.80,roof='flat',osm='93238185',est=True),
 'y417':dict(height=2.90,top=4.70,roof='saddle',osm='93192417',est=True),
 'r195':dict(height=3.00,top=3.00,roof='flat',osm='92204195',est=True),
 's685':dict(height=2.40,top=3.40,roof='saddle',osm='1549543685',est=True),
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
(R/'source/block113.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block113-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK113_ZONES_OK' if ok else 'BLOCK113_ZONES_REVIEW')
