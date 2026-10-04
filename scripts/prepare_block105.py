"""Pass 105: Strömgatan in the north-west of Kvarnholmen (district volumes 92204154, 92204196,
92204205, 92204158, 92204191, 92379281, 91285791):
- 92204154: the brick house at the west end of the north side, rusticated ground floor; front
  range on the street and its rear wing;
- 92204196 (3 Strömgatan): the olive roughcast three-storey house on the south side; front range
  and the unseen rear part;
- 92204205: the grey rendered four-storey house with two box bays and a mansard;
- 92204158: the red brick three-storey house with grey arched hoods and mansard dormers;
- 92204191: the small green house with an orange tile roof (seen obliquely only);
- 92379281 (10 Strömgatan): the yellow brick four-storey house on the south side, its front range
  and the rear wing running south;
- 91285791: the large building to Södra Kanalgatan, not photographed, kept generic.
Note: the houses at y = 218 front SOUTH onto Strömgatan, the ones at y = 206 front NORTH onto it.
Heights from three resected Google Street View panoramas (see references/block105-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block105.py
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
IDS=['92204154','92204196','92204205','92204158','92204191','92379281','91285791']
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
# Joints: 92204154's front range ends at the rear-wing step (OSM vertices at y 228.9); 92204196's
# front range at the vertex row y 195.3; 92379281's front range at the wing corner y 195.8.
P=PG['92204154'];f154=P.intersection(half((-242.44,228.87),(-247.73,228.94),True));b154=P.difference(f154)
P=PG['92204196'];f196=P.intersection(half((-245.17,195.32),(-221.11,195.33),True));b196=P.difference(f196)
P=PG['92379281'];f281=P.intersection(half((-153.59,195.87),(-132.23,195.82),True));w281=P.difference(f281)
GEO={'f154':f154,'b154':b154,'f196':f196,'b196':b196,'o205':PG['92204205'],'r158':PG['92204158'],'g191':PG['92204191'],
 'y281':f281,'w281':w281,'k791':PG['91285791']}
# Heights (m) above the pavement: eaves 'height', ridge or roof top 'top'. Measured values from the
# resected panoramas; zones marked est. are not seen or only partly seen (see the notes).
# roof: 'hip', 'saddle' (ridge along the street front), 'saddle_across', 'mansard', 'flat'.
spec={
 'f154':dict(height=11.60,top=13.80,roof='hip',osm='92204154',est=True),
 'b154':dict(height=8.60,top=8.60,roof='flat',osm='92204154',est=True),
 'f196':dict(height=9.70,top=11.60,roof='hip',osm='92204196'),
 'b196':dict(height=8.60,top=8.60,roof='flat',osm='92204196',est=True),
 'o205':dict(height=11.60,top=14.20,roof='mansard',osm='92204205'),
 'r158':dict(height=9.95,top=12.80,roof='mansard',osm='92204158'),
 'g191':dict(height=6.30,top=9.30,roof='saddle',osm='92204191',est=True),
 'y281':dict(height=13.10,top=16.40,roof='saddle',osm='92379281',est=True),
 'w281':dict(height=12.00,top=14.80,roof='saddle_across',osm='92379281',est=True),
 'k791':dict(height=9.75,top=9.75,roof='flat',osm='91285791',est=True),
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
(R/'source/block105.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block105-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK105_ZONES_OK' if ok else 'BLOCK105_ZONES_REVIEW')
