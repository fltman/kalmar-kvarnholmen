"""Pass 83: the south side of Kom snart igen, the old warehouse row between Kom snart igen and
Skeppsbron: two district volumes (91915622 and 91915624) split into the white boarded warehouse at
the west end, three boarded warehouses with frontispieces, the white rendered house at the east end,
and the three narrow links between them (the middle one with a glazed front on Skeppsbron).
Heights from Google Street View panoramas (April 2025); see references/block83-notes.md.
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
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
W22,ROW=PG('91915622'),PG('91915624')
# The row's frame: along the Kom snart igen fronts (west to east), inwards to the south.
O=(-47.4,-281.6);D=(.963,-.269);N=(D[1],-D[0])
S=lambda p:(p[0]-O[0])*D[0]+(p[1]-O[1])*D[1]
def slab(s0,s1):
 # Everything of the row between two cross-sections s0 and s1.
 P=lambda s,t:(O[0]+D[0]*s+N[0]*t,O[1]+D[1]*s+N[1]*t)
 return Polygon([P(s0,-30),P(s1,-30),P(s1,30),P(s0,30)])
# The links are the narrow necks between the notches in both fronts: their ends are the extreme
# notch corners along the row.
notch=[[(-28.0,-279.3),(-25.8,-280.0),(-29.8,-284.5),(-26.1,-285.5)],[(-6.6,-284.8),(-3.7,-285.6),(-8.3,-290.8),(-4.5,-291.8)],
 [(14.9,-292.2),(17.4,-292.9),(13.1,-296.8),(16.8,-297.8)]]
cuts=[(min(S(p) for p in q),max(S(p) for p in q)) for q in notch]
(a1,b1),(a2,b2),(a3,b3)=cuts
# The middle link: a low lean-to on Kom snart igen, the glazed two-storey front on Skeppsbron.
def front_band(depth):
 P=lambda s,t:(O[0]+D[0]*s+N[0]*t,O[1]+D[1]*s+N[1]*t)
 return Polygon([P(-10,-30),P(80,-30),P(80,depth),P(-10,depth)])
# Each link is the quadrilateral between the inner corners of its two notches; the warehouses are
# what remains, in order along the row.
links=[Polygon([q[0],q[1],q[3],q[2]]).buffer(.02,join_style=2) for q in notch]
rest=sorted(flat(ROW.difference(unary_union(links))),key=lambda g:S(g.centroid.coords[0]))
rest=[g for g in rest if g.area>5]
assert len(rest)==4,[round(g.area,1) for g in rest]
L1,L2,L3=[ROW.intersection(l) for l in links]
seeds=[('wh',W22),('u1',rest[0]),('l1',L1),('u2',rest[1]),('l2n',L2.intersection(front_band(-4.7))),('l2s',L2),('u3',rest[2]),('l3',L3),('u4',rest[3]),('u4',ROW)]
# Heights (m): the boarded warehouses' eaves and frontispiece apexes measured on the green one;
# the others estimated from the same views (see the notes).
WH={'wh':dict(height=6.6,top=8.4,fr=(8.0,9.2)),'u1':dict(height=6.9,top=9.0,fr=(8.0,9.5)),'l1':dict(height=6.3,top=6.6),'u2':dict(height=6.9,top=9.0,fr=(8.0,9.5)),
 'l2n':dict(height=3.5,top=3.7),'l2s':dict(height=7.0,top=7.2),'u3':dict(height=6.9,top=9.0,fr=(8.0,9.5)),'l3':dict(height=5.8,top=6.2),'u4':dict(height=7.0,top=8.8,fr=(7.9,9.0))}
mesh={'wh':'SM_Kvarnholmen_House_91915622'};spec={k:dict(v,mesh=mesh.get(k,'SM_Kvarnholmen_House_91915624')) for k,v in WH.items()}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=zones.get(name,[])+ps;taken=unary_union([taken]+ps)
# Slivers left along the cuts join the zone they touch most.
for name in list(zones):
 if len(zones[name])>1:zones[name]=[max(zones[name],key=lambda g:g.area)]
scope={'91915622','91915624'}
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
foot=unary_union([W22,ROW]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91915622 and 91915624 (source/district17.json), '+district['source'],'frame':{'origin':O,'along':D,'inwards':N},'cuts':cuts,'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block83.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block83-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c,cuts);print('BLOCK83_ZONES_OK' if ok else 'BLOCK83_ZONES_REVIEW')
