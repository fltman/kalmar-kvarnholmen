"""Pass 123: a correction of pass 115 for five of its Stadsparken and Slottsvägen houses. It re-zones
their pass-98 outlines (source/block98.json, OSM, ODbL) from new contributor photos:
- Slottshotellet (93332243): the red main range (2.5 storeys), the front risalit on the south-east
  side, the cross gable that projects into the courtyard on the north-west side, the polygonal
  glazed porch beside it, the green boarded west wing and the low link between them;
- Kalmar konstmuseum (91931339): the tall black tower, the lower core, the cantilevered front block
  and the low glazed entrance link towards Byttan;
- Byttan (91222116): one zone, with the set-back upper storey given as a rectangle in its frame;
- the grey boarded park pavilion (874870421): the main body under a saddle roof and its annex;
- 91222187, which no photo identifies (kept as pass 115's plain pavilion).
Heights are metres above the ground, which pass 98 lays at model z 0.30; see
references/block123-notes.md for what is measured and what is estimated.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings'];BY={b['id']:b for b in B98}
IDS=['93332243','91931339','91222116','874870421','91222187']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>.8]
OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
def rect(a,b,s0,s1,t0,t1):
 # The rectangle s0..s1 along a->b, t0..t1 to the left of it, in model coordinates.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,t0),(s1,t0),(s1,t1),(s0,t1))])
V=lambda i,k:tuple(BY[i]['outer'][k])
# Frames (a, b): s along a->b, t to the left (into the building).
HF=(V('93332243',15),V('93332243',16))   # Slottshotellet: the south-east front of the main range
HG=(V('93332243',13),V('93332243',14))   # its green west wing, the south-east side (pass 115's frame)
MF=(V('91931339',4),V('91931339',5))     # the museum: its south-east side
BF=(V('91222116',0),V('91222116',1))     # Byttan: its north-west front, from the museum end
PF=(V('874870421',3),V('874870421',4))   # the pavilion: its south side
SF=(V('91222187',2),V('91222187',3))     # 91222187: its south-east side
seeds=[
 # Slottshotellet. hm: the main range s 0..27.4, t 0..9.88 (2.5 storeys, hip with dormers);
 # hr: the front risalit (7.0 x 3.4) with its cross gable; hx: the courtyard cross gable (5.1 x 2.3);
 # hp: the polygonal glazed porch with the terrace on top; hg: the green wing; hl: the low link.
 ('hm','93332243',OUT['93332243'].intersection(rect(*HF,-0.5,27.6,-0.01,9.88)),dict(height=7.6,top=12.6,roof='hip',wall='Red')),
 ('hr','93332243',OUT['93332243'].intersection(rect(*HF,16.0,23.4,-3.6,0)),dict(height=7.6,top=11.1,roof='cross',wall='Red')),
 ('hx','93332243',OUT['93332243'].intersection(rect(*HF,1.9,7.3,9.88,12.4)),dict(height=7.6,top=10.2,roof='cross',wall='Red')),
 ('hp','93332243',OUT['93332243'].intersection(rect(*HF,16.0,23.3,9.88,14.6)),dict(height=3.6,top=3.8,roof='terrace',wall='White')),
 ('hg','93332243',OUT['93332243'].intersection(rect(*HG,-0.5,9.9,-0.2,8.9)),dict(height=3.3,top=7.0,roof='saddle',wall='Green')),
 ('hl','93332243',OUT['93332243'],dict(height=3.1,top=3.6,roof='lean',wall='Green')),
 # The museum. ml: the low glazed entrance link; mt: the tall tower; mf: the cantilevered front
 # block (its soffit is in the build); mc: the core.
 ('ml','91931339',OUT['91931339'].intersection(rect(*MF,-4.0,0.0,8.0,21.0)),dict(height=4.6,top=4.6,roof='flat',wall='Black')),
 ('mt','91931339',OUT['91931339'].intersection(rect(*MF,0.0,6.72,-0.5,23.5)),dict(height=18.5,top=18.5,roof='flat',wall='Black')),
 ('mf','91931339',OUT['91931339'].intersection(rect(*MF,6.72,12.31,17.33,22.5)),dict(height=14.0,top=14.0,roof='flat',wall='Black',soffit=[6.0,8.0])),
 ('mc','91931339',OUT['91931339'],dict(height=16.0,top=16.0,roof='flat',wall='Black')),
 # Byttan: the one-storey restaurant; the upper storey's rectangle in the BF frame.
 ('by','91222116',OUT['91222116'],dict(height=3.9,top=4.6,roof='low',wall='White',upper=dict(s0=3.6,s1=13.6,t0=3.5,t1=12.5,height=7.0,top=7.4))),
 # The pavilion: the main body (saddle along its south side), the annex behind it.
 ('pv','874870421',OUT['874870421'].intersection(rect(*PF,-0.1,10.6,-0.1,5.59)),dict(height=2.7,top=4.6,roof='saddle',wall='GreyBoard')),
 ('pn','874870421',OUT['874870421'],dict(height=2.6,top=3.4,roof='low',wall='GreyBoard')),
 # 91222187: no view identifies it (the open shelter in park_pav_b stands 25-40 degrees away from
 # its bearing); pass 115's plain cream pavilion under a red hip is kept.
 ('sh','91222187',OUT['91222187'],dict(height=3.0,top=5.6,roof='hip',wall='Cream')),
]
FRONT={'hm':HF,'hr':HF,'hx':HF,'hp':HF,'hg':HG,'hl':HF,'ml':MF,'mt':MF,'mf':MF,'mc':MF,'by':BF,'pv':PF,'pn':PF,'sh':SF}
taken={};zones={}
for name,osm,seed,spec in seeds:
 ps=parts(seed.difference(taken.get(osm,Polygon())));zones[name]=(osm,ps,spec);taken[osm]=unary_union([taken.get(osm,Polygon())]+ps)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0))-.30,b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for name,(o,ps,spec) in zones.items():
  if o!=osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
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
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'corrects_pass':115,'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS},
  'empty_zones':[n for n,(o,ps,s) in zones.items() if not ps]}}
(R/'source/block123.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values()) and not c['empty_zones']
(R/'previews/block123-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK123_ZONES_OK' if ok else 'BLOCK123_ZONES_REVIEW')
