"""Pass 115: the houses of Stadsparken and Slottsvägen on the mainland west of Kvarnholmen. Pass 98
built them as plain volumes inside its combined chunk meshes; this pass splits fourteen of its
outlines (source/block98.json, OSM, ODbL) into zones with eaves, ridge and roof kind:
- Stadsparken: Kalmar konstmuseum (91931339), Byttan (91222116) and two small park buildings
  (91222187, 874870421);
- Slottsvägen: Slottshotellet with its green boarded west wing (93332243), the villa at
  Västerlånggatan 1 (93332252), the red-brick house with the glazed veranda (93306354), the green
  low house and the shed beside it (387312779, 387312778), the cream villa with the pediment
  (91970278), the white mansard pavilion (91970355), the cream house with the rooftop storey
  (91970390), the Söderport pavilion (91970274) and the KIKAIN kiosk (564958332).
Heights (metres above the ground, which pass 98 lays at model z 0.30) from Google Street View
panoramas, resected on the OSM outlines; see references/block115-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings'];BY={b['id']:b for b in B98}
IDS=['91931339','91222116','91222187','874870421','93332243','93332252','93306354','387312778','387312779','91970278','91970355','91970390','91970274','564958332']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>.8]
OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
def rect(a,b,s0,s1,t0,t1):
 # The rectangle s0..s1 along a->b, t0..t1 to the left of it, in model coordinates.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,t0),(s1,t0),(s1,t1),(s0,t1))])
V=lambda i,k:tuple(BY[i]['outer'][k])
# Fronts (a, b): the edge the zone's roof and openings are framed on, the inside to the left of a->b.
SH_SE=(V('93332243',15),V('93332243',16))          # Slottshotellet, the main range's south-east front
SH_GW=(V('93332243',13),V('93332243',14))          # its green west wing, the south-east side
RB_NW=(V('93306354',1),V('93306354',2))            # the red-brick house, its north-west wall (inside to the left)
VI_SE=(V('91970278',2),V('91970278',3))            # the cream villa, its south-east front on Slottsvägen
SO_LS=(V('91970274',1),V('91970274',2))            # the Söderport pavilion, the long south-east side
# Zones: (name, osm id, seed geometry, spec). Heights above the ground; 'top' is the ridge or roof top.
seeds=[
 ('mu','91931339',OUT['91931339'],dict(height=17.5,top=17.5,roof='flat',wall='Black')),
 ('by','91222116',OUT['91222116'],dict(height=3.9,top=4.6,roof='low',wall='White',upper=dict(inset=4.6,height=7.0,top=7.4))),
 ('pa','91222187',OUT['91222187'],dict(height=3.0,top=5.6,roof='hip',wall='Cream')),
 ('pb','874870421',OUT['874870421'],dict(height=2.8,top=3.6,roof='low',wall='Cream')),
 ('shg','93332243',OUT['93332243'].intersection(rect(*SH_GW,-0.5,9.9,-0.2,8.9)),dict(height=3.3,top=7.0,roof='saddle',wall='Green')),
 ('shm','93332243',OUT['93332243'].intersection(rect(*SH_SE,-0.5,16.6,0,9.9)),dict(height=7.6,top=12.6,roof='hip',wall='Red')),
 ('shn','93332243',OUT['93332243'],dict(height=7.2,top=11.0,roof='low',wall='Red')),
 ('vl','93332252',OUT['93332252'],dict(height=3.7,top=8.4,roof='saddle',wall='Salmon')),
 ('rb','93306354',OUT['93306354'].intersection(rect(*RB_NW,-0.5,18.5,0,7.8)),dict(height=4.6,top=8.0,roof='saddle',wall='Brick')),
 ('rv','93306354',OUT['93306354'],dict(height=3.5,top=3.7,roof='flat',wall='Veranda')),
 ('gs','387312778',OUT['387312778'],dict(height=2.6,top=2.8,roof='flat',wall='DarkGreen')),
 ('gl','387312779',OUT['387312779'],dict(height=3.4,top=3.6,roof='flat',wall='DarkGreen')),
 ('vi','91970278',OUT['91970278'].intersection(rect(*VI_SE,0,16.55,0,11.55)),dict(height=8.7,top=12.0,roof='saddle',wall='Cream')),
 ('vs','91970278',OUT['91970278'].intersection(rect(*VI_SE,16.55,20,0,11.55)),dict(height=1.0,top=1.0,roof='flat',wall='Stone')),
 ('vr','91970278',OUT['91970278'],dict(height=6.6,top=7.4,roof='low',wall='Cream')),
 ('mp','91970355',OUT['91970355'],dict(height=3.7,top=7.0,roof='mansard',wall='White')),
 ('rt','91970390',OUT['91970390'],dict(height=7.8,top=8.1,roof='flat',wall='Cream',upper=dict(inset=1.6,height=10.2,top=10.4))),
 ('so','91970274',OUT['91970274'].intersection(rect(*SO_LS,-0.5,22.5,0,11.8)),dict(height=4.4,top=7.8,roof='saddle',wall='Cream')),
 ('sw','91970274',OUT['91970274'],dict(height=3.0,top=3.3,roof='flat',wall='Grey')),
 ('ki','564958332',OUT['564958332'],dict(height=2.8,top=4.3,roof='cone',wall='White')),
]
# The front each zone's roof and openings are framed on (a, b), inside to the left of a->b.
FRONT={'shg':SH_GW,'shm':SH_SE,'shn':SH_SE,'rb':RB_NW,'vi':VI_SE,'so':SO_LS,'vl':(V('93332252',0),V('93332252',1)),
 'mp':(V('91970355',0),V('91970355',3)),'pa':(V('91222187',0),V('91222187',3)),'rt':(V('91970390',1),V('91970390',2)),'by':(V('91222116',0),V('91222116',1))}
taken={};zones={}
for name,osm,seed,spec in seeds:
 ps=parts(seed.difference(taken.get(osm,Polygon())));zones[name]=(osm,ps,spec);taken[osm]=unary_union([taken.get(osm,Polygon())]+ps)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0))-.30,b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
out={};report={}
for name,(osm,ps,spec) in zones.items():
 H=spec['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(osm,Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 fr=FRONT.get(name)
 out[name]=dict(spec,osm=osm,mesh='SM_Slott115_'+osm,polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls,
  front=[list(fr[0]),list(fr[1])] if fr else None)
 report[name]={'osm':osm,'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block115.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block115-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK115_ZONES_OK' if ok else 'BLOCK115_ZONES_REVIEW')
