"""Pass 89: five generic pass-17 volumes on the south side of east Storgatan, west to east:
- Storgatan 60 (91928538): the pale green rendered two-storey house with the gateway;
- Storgatan 62 (91928591): the yellow boarded two-storey house with the pediment;
- Storgatan 64 (91928561): the long pale yellow rendered two-storey house with gables at both ends
  and two red dormers;
- 91928583: the small green boarded house with its gable to the street;
- 91928590: the green boarded wall with the black carriage gate and the low shed behind it.
One zone per volume: each photographed front is one house. Heights from four resected Google Street
View panoramas (April 2025); see references/block89-notes.md.
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
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
G60,Y62,Y64,GH,GW=PG('91928538'),PG('91928591'),PG('91928561'),PG('91928583'),PG('91928590')
seeds=[('g60',G60),('y62',Y62),('y64',Y64),('gh',GH),('gw',GW)]
# Heights (m) above the pavement at the front. Eaves measured on the resected panoramas (camera
# height 2.4 m from the pavement line), at the gutter line, which stands about 0.5 m in front of the
# facade (so 0.2-0.3 m below its reading on the facade plane); the ridges of 60 and 64 from the roof crest seen over the
# eaves, taken to be the ridge at mid-depth; the ridge of 62 and the shed roof of the gate estimated (see the notes).
spec={'g60':dict(height=6.15,top=10.6,mesh='SM_Kvarnholmen_House_91928538',roof='hip'),
 'y62':dict(height=6.0,top=8.2,mesh='SM_Kvarnholmen_House_91928591',roof='saddle'),
 'y64':dict(height=7.1,top=13.8,mesh='SM_Kvarnholmen_House_91928561',roof='saddle'),
 'gh':dict(height=4.3,top=6.3,mesh='SM_Kvarnholmen_House_91928583',roof='saddle_x'),
 'gw':dict(height=2.9,top=3.05,mesh='SM_Kvarnholmen_House_91928590',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91928538','91928591','91928561','91928583','91928590'}
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
foot=unary_union([G60,Y62,Y64,GH,GW]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91928538, 91928591, 91928561, 91928583 and 91928590 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block89.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block89-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK89_ZONES_OK' if ok else 'BLOCK89_ZONES_REVIEW')
