"""Pass 101: the west side of Östra Vallgatan south of the gate, house numbers 7 to 9 (district
volumes 93238179, 93238159, 93238211 and 93238209), from south to north:
- 93238179 (7): the grey rendered two-storey house with its railed roof, on the north 6.7 m of the
  OSM front, and a low grey boarded shed with a lean-to roof on the south 3.8 m;
- 93238159: the yellow boarded cottage, gable to the street;
- 93238211: the green boarded cottage, gable to the street;
- 93238209: the low yellow boarded cottage, gable to the street, and the brown gate to its north.
Heights from two resected Google Street View panoramas (see references/block101-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block101.py
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
IDS=['93238179','93238159','93238211','93238209']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i]
for i in IDS:assert not d17[MESH[i]].get('detail_pass') or d17[MESH[i]]['detail_pass']<=17,i
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# 93238179: the rendered house begins 3.85 m north of the south end of the OSM front (measured);
# south of that the boarded shed. The cut runs square to the front, westwards.
P=PG['93238179'];C0=(386.475,20.07);C1=(C0[0]-9.997,C0[1]+0.247)
s179=P.intersection(half(C0,C1,True));h179=P.difference(s179)
GEO={'g179':h179,'g179s':s179,'y159':PG['93238159'],'g211':PG['93238211'],'y209':PG['93238209']}
# Heights (m) above the ground at the house: eaves 'height', ridge 'top'. Measured from the resected
# panoramas except where est. (see the notes).
# roof: 'hip' (a low railed hip), 'lean' (lean-to rising to the north), 'gable_street' (ridge at
# right angles to the street front).
spec={
 'g179':dict(height=5.75,top=6.35,roof='hip',osm='93238179',top_est=True),
 'g179s':dict(height=3.40,top=3.90,roof='lean',osm='93238179'),
 'y159':dict(height=2.15,top=4.05,roof='gable_street',osm='93238159'),
 'g211':dict(height=2.25,top=4.05,roof='gable_street',osm='93238211'),
 'y209':dict(height=1.60,top=3.30,roof='gable_street',osm='93238209'),
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
(R/'source/block101.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block101-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK101_ZONES_OK' if ok else 'BLOCK101_ZONES_REVIEW')
