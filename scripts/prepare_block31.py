"""Pass 31: Larmgatan 16 (OSM 92204162), the yellow house north of the Larmgatan 14 corner building.

Two storeys under a steep red-tiled roof with three dormers: a yellow front between white
rusticated lesenes, a central carriage passage under a cartouche with the house number, a door and
a shop window either side, five upper windows under cornice heads (a pediment in the middle), a
dentilled main cornice. Behind the front range two lower courtyard wings. Heights come from a
Google Street View panorama (April 2025) straight in front of the house, registered on its two OSM
joints; see references/block31-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block31.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text());B={b['id']:b for b in district['buildings']}
def ring(bid):
 r=[tuple(p) for p in B[bid]['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
P=Polygon(ring('92204162')).buffer(0)
# The front range is 12.9 m deep (to x -272.2, where the courtyard wall steps); behind it the south
# wing to x -265.0 and the long north wing to the block's east side.
front=P.intersection(box(-300,-50,-272.2,-25));rest=P.difference(front)
seeds=[('front',front)]+[('wing_s' if g.centroid.y<-38 else 'wing_n',g) for g in flat(rest) if g.area>1]
# Heights (m) above the Larmgatan facade base. Measured: ground-floor cornice 3.61-3.94, upper
# windows 4.70-6.69, pediment 7.68, main cornice 7.85-8.2 after allowing for its projection, a
# steep tiled lower roof slope visible above it with dormers reaching about 10.6. The wings, the
# roof's upper slope and ridge are estimates.
spec={'front':dict(height=8.2,break_=10.3,top=11.8,mesh='SM_Kvarnholmen_House_92204162',cornice_ground=[3.61,3.94],windows=[4.70,6.69]),
 'wing_s':dict(height=6.3,top=7.9,mesh='SM_Kvarnholmen_House_92204162'),
 'wing_n':dict(height=6.3,top=7.9,mesh='SM_Kvarnholmen_House_92204162')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=zones.get(name,[])+ps;taken=unary_union([taken]+ps)
b30=json.loads((R/'source/block30.json').read_text())['zones']['main']
others=[(Polygon(b30['polygons'][0]).buffer(0),b30['height'],'block30:main')]
b29=json.loads((R/'source/block29.json').read_text())['zones']
others+=[(Polygon(ps).buffer(0),z['height'],'block29:'+n) for n,z in b29.items() for ps in z['polygons']]
others+=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in {'92204162','92204170','92204156','92204161','92204198','92204187','92204189'}]
# The authored Storgatan buildings (not in the district outlines): Larmgatan 18 (92204199) adjoins
# the north side, its eaves at 8.2 like this house's.
sg=json.loads((R/'source/storgatan.json').read_text())['buildings'];d17=json.loads((R/'source/district17.json').read_text())['buildings']
others+=[(Polygon(b['polygon']).buffer(0),d17.get('SM_Building_'+b['id'],{}).get('H',8.0),'storgatan:'+b['id']) for b in sg if b.get('polygon')]
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
   ux,uy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=uy,-ux;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+ux*Lw*t+nx*.3,p[1]+uy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+ux*Lw*t0,3),round(p[1]+uy*Lw*t0,3));b=(round(p[0]+ux*Lw*t1,3),round(p[1]+uy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
# Roof of the front range: a steep tiled lower slope (8.2 -> 10.3, 1.2 m in, as seen above the
# cornice) and a low upper slope to a narrow flat top; no inset at the party walls to the north and
# south, whose neighbours are as tall or taller.
def merge(ring):
 out=list(ring);changed=True
 while changed:
  changed=False
  for i in range(len(out)):
   a,b,c=out[i-1],out[i],out[(i+1)%len(out)]
   u=(b[0]-a[0],b[1]-a[1]);v=(c[0]-b[0],c[1]-b[1])
   if abs(u[0]*v[1]-u[1]*v[0])<.2*math.hypot(*u)*math.hypot(*v):out.pop(i);changed=True;break
 return out
def inner(ring,insets):
 lines=[]
 for (p,q),d in zip(zip(ring,ring[1:]+ring[:1]),insets):
  L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=-uy,ux
  lines.append(((p[0]+nx*d,p[1]+ny*d),(ux,uy)))
 pts=[]
 for i in range(len(ring)):
  (p1,d1),(p2,d2)=lines[i-1],lines[i];det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
  t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det;pts.append((round(p1[0]+d1[0]*t,3),round(p1[1]+d1[1]*t,3)))
 return pts
# The roof follows the range's four corners (the 0.2 m kink in the courtyard wall is ignored).
fr=[(-272.2,-31.64),(-284.96,-31.534),(-285.206,-43.086),(-272.2,-43.296)]
fw=[True,False,True,False]
r1=inner(fr,[0 if f else 1.2 for f in fw]);r2=inner(r1,[0 if f else 4.8 for f in fw])
for name,r in (('r1',r1),('r2',r2)):
 g=Polygon(r);assert g.is_valid and g.area<Polygon(fr).area and Polygon(fr).buffer(.01).contains(g),name
out['front']['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],r2=[list(v) for v in r2],firewall=fw,areas=[round(Polygon(fr).area,1),round(Polygon(r1).area,1),round(Polygon(r2).area,1)])
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap way 92204162, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(P.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(P).area,2),'osm_not_zoned_m2':round(P.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block31.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block31-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK31_ZONES_OK' if ok else 'BLOCK31_ZONES_REVIEW')
