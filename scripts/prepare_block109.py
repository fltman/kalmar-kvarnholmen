"""Pass 109: generic pass-17 volumes in the north-west of Kvarnholmen, on Larmgatan, Strömgatan,
Norra Långgatan and Västra Vallgatan (district volumes 92204179, 92204177, 92204174, 886305409,
91846958, 91846925 and 91846945):
- 92204179 (38 Larmgatan): the red boarded outbuilding front, one zone;
- 92204177 (40 Larmgatan): the 1950s three-storey office block (the north range, from the joint
  seen on the street front at y = 194.8) and the lower two-storey wing (the rest of the ring);
- 92204174 (1 Strömgatan): the three-storey west end (to the downpipe at x = -276.2), the
  two-storey street range with dormers, and the back ranges behind y = 229.0 (not seen);
- 886305409 (50 Larmgatan): the round glass and panel drum, one zone (the whole outline is the
  drum; its 2.8 m 'street front' is one of its 19 facets);
- 91846958 (4 Norra Långgatan): the cream corner house: the street block with the chamfered corner
  (north of y = 50.9) and its south wing;
- 91846925: the grey boarded two-storey house, one zone;
- 91846945: the block between Norra Långgatan, Larmgatan and Västra Vallgatan; no usable photo,
  one generic zone.
Heights from six resected Google Street View panoramas (view only); see references/block109-notes.md.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block109.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['92204179','92204177','92204174','886305409','91846958','91846925','91846945']
# Two of the volumes are stored as SM_Building_<id> (the Storgatan list), the rest as
# SM_Kvarnholmen_House_<id>; the build reuses whichever name the district has.
MESH={}
for i in IDS:
 MESH[i]=next(p+i for p in ('SM_Kvarnholmen_House_','SM_Building_') if p+i in d17)
 assert d17[MESH[i]].get('detail_pass') in (None,17),MESH[i]
PG={i:Polygon([tuple(w['p']) for w in d17[MESH[i]]['walls']]).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid,i
BIG=lambda x0,y0,x1,y1:box(x0,y0,x1,y1)
GEO={
 'r179':PG['92204179'],
 'o177':PG['92204177'].intersection(BIG(-300,194.8,-240,220)),
 'w177':PG['92204177'],
 'sw174':PG['92204174'].intersection(BIG(-300,200,-276.2,229.0)),
 'sf174':PG['92204174'].intersection(BIG(-276.2,200,-240,229.0)),
 'sb174':PG['92204174'],
 'd886':PG['886305409'],
 'c958':PG['91846958'].intersection(BIG(-350,50.9,-300,80)),
 'w958':PG['91846958'],
 'g925':PG['91846925'],
 'b945':PG['91846945'],
}
# Heights (m) above the street: eaves, cornice or parapet top ('height') and ridge ('top').
# Measured on the resected panoramas unless marked est. (see the notes).
spec={
 'r179':dict(height=3.80,top=4.40,roof='saddle',osm='92204179'),          # wall top measured, roof est.
 'o177':dict(height=10.10,top=10.10,roof='flat',osm='92204177'),
 'w177':dict(height=7.10,top=7.10,roof='flat',osm='92204177'),
 'sw174':dict(height=10.60,top=12.60,roof='hip',osm='92204174',est=True),   # 3rd floor seen, eaves est.
 'sf174':dict(height=8.30,top=11.30,roof='saddle',osm='92204174'),         # ridge est.
 'sb174':dict(height=7.00,top=7.00,roof='flat',osm='92204174',est=True),
 'd886':dict(height=9.60,top=9.60,roof='flat',osm='886305409'),
 'c958':dict(height=10.00,top=12.80,roof='hip',osm='91846958'),           # ridge est.
 'w958':dict(height=10.00,top=12.40,roof='hip',osm='91846958',est=True),
 'g925':dict(height=6.85,top=9.00,roof='saddle',osm='91846925'),          # ridge est.
 'b945':dict(height=9.75,top=9.75,roof='flat',osm='91846945',est=True),
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
(R/'source/block109.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(zones[k] for k in zones)
(R/'previews/block109-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print({i:round(PG[i].difference(covered).area,2) for i in IDS});print('BLOCK109_ZONES_OK' if ok else 'BLOCK109_ZONES_REVIEW')
