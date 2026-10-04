"""Pass 87: the north side of the east end of Södra Långgatan, nos. 63–69 and the ochre gable-front
house east of them: four district volumes (91928581, 91928560, 91928553, 91928566) split into
seven parts:
- no. 63 (91928581): the pale green three-storey house and its two-storey west bay;
- no. 67 (91928560): the cream west part with the archway and bay, the pink east part with its
  bay, and the rear wing behind the pink part;
- no. 69 (91928553): the ochre roughcast front range and the lower rear part behind it;
- 91928566: the ochre roughcast house with its gambrel gable to the street.
Heights from four Google Street View panoramas (2025); see references/block87-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
G81,P60,O53,G66=PG('91928581'),PG('91928560'),PG('91928553'),PG('91928566')
def band(a,b,depth,s0=-60,s1=60):
 # The strip behind the street front a-b (local street frame: s along the front, t inwards), as a
 # polygon in model coordinates; inwards is to the left of a->b.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,0-.5),(s1,0-.5),(s1,depth),(s0,depth))])
# Street fronts (west to east; inwards = north). The OSM outline vertices.
F81=((201.0,-71.88),(215.96,-72.42))
F60=((215.96,-72.42),(239.54,-72.9))
F53=((239.54,-72.9),(248.65,-73.0))
F66=((252.4,-71.74),(262.04,-71.65))
# No. 63: the two-storey west bay is 3.9 m wide (the lesene at s 3.55-3.88 on the resected
# heading-332 view); the three-storey main house fills the rest. No. 67: the cream and pink parts
# meet at the downpipe, s 10.6 (10.4-11.1 on the two views); both front ranges are 13.5 m deep as the
# outline's step at y -58.9 shows; the rear wing is the outline's northern arm. No. 69: an 11 m
# front range, the outline's deeper rest behind it.
seeds=[('gw',G81.intersection(band(*F81,20,-60,3.9))),('gm',G81),
 ('cr',P60.intersection(band(*F60,13.6,-60,10.6))),('pk',P60.intersection(band(*F60,13.6,10.6,60))),('rw',P60),
 ('oc',O53.intersection(band(*F53,11.0))),('ob',O53),('gb',G66)]
# Heights (m) above the facade base. Eaves measured on the street fronts (see the notes); ridges
# and the rear parts are estimates.
spec={'gw':dict(height=6.1,top=7.9,mesh='SM_Kvarnholmen_House_91928581',roof='saddle'),
 'gm':dict(height=8.8,top=12.2,mesh='SM_Kvarnholmen_House_91928581',roof='saddle'),
 'cr':dict(height=9.4,top=13.0,mesh='SM_Kvarnholmen_House_91928560',roof='saddle'),
 'pk':dict(height=9.4,top=13.0,mesh='SM_Kvarnholmen_House_91928560',roof='saddle'),
 'rw':dict(height=6.4,top=8.4,mesh='SM_Kvarnholmen_House_91928560',roof='hip'),
 'oc':dict(height=8.8,top=10.6,mesh='SM_Kvarnholmen_House_91928553',roof='hip'),
 'ob':dict(height=6.4,top=6.6,mesh='SM_Kvarnholmen_House_91928553',roof='flat'),
 'gb':dict(height=6.8,top=11.8,mesh='SM_Kvarnholmen_House_91928566',roof='gambrel')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91928581','91928560','91928553','91928566'}
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
foot=unary_union([G81,P60,O53,G66]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91928581, 91928560, 91928553 and 91928566 (source/district17.json), '+district['source'],
 'fronts':{'gm':F81,'cr':F60,'oc':F53,'gb':F66},'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block87.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block87-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK87_ZONES_OK' if ok else 'BLOCK87_ZONES_REVIEW')
