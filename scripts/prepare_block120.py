"""Pass 120: correction of the fire station site at Larmgatan / Södra Kanalgatan, mesh
SM_Kvarnholmen_House_91846968 (landmarks pass 14). Pass 14's old 1905 station in the east half stays as
it is; this script only zones the modern western part, which pass 14 drew as one cream 3-row box at 10 m.
Zones (heights in metres above the ground, model z 0):
- stone: the five-storey limestone-clad block on Larmgatan, a 9.2 m deep bar along the OSM west line,
  extended north to the measured north face (about 8 m north of the OSM north-west corner);
- stone_top: its top floor north of y 259.76, set back 3.0 m from the courtyard (east) face, flush on
  the street faces;
- pavilion: the one-storey glazed pavilion in front of the white wing, between the stone block and
  x -240.5, its north face in line with the stone block's;
- white: the rest of pass 14's `modern` polygon, the white rendered wing (two full storeys and a
  third in a mansard with wall dormers).
The north extension and the heights come from three Google Street View panoramas, resected on the OSM
drum, the OSM west line and the old station (view only); see references/block120-notes.md.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block120.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
OSM='91846968';MESH='SM_Kvarnholmen_House_'+OSM
d17=json.loads((R/'source/district17.json').read_text())['buildings'];assert MESH in d17
L14=json.loads((R/'source/landmarks14.json').read_text())['buildings'][OSM]
# Pass 14's split of the combined outline (build_landmarks14.py, lines 185 and 215).
MODERN=[(-273.94,277.619),(-267.079,277.818),(-266.184,279.89),(-232.567,280.42),(-226.912,259.792),(-226.105,251.187),(-253.53,247.59),(-282.848,247.672),(-282.832,255.457),(-281.189,255.725),(-281.664,259.757)]
OLD=[(-232.567,280.42),(-190.347,273.407),(-190.38,259.505),(-202.368,261.499),(-204.359,255.417),(-226.912,259.792)]
SOUTH_NB=[tuple(w['p']) for w in d17['SM_Kvarnholmen_House_92204174']['walls']];SOUTH_H=d17['SM_Kvarnholmen_House_92204174']['H']

# ---------------------------------------------------------------- measured lines (see the notes)
# OSM north face of the modern part, (-266.184,279.89) -> (-232.567,280.42).
K=(280.42-279.89)/(-232.567+266.184)
def y_osm(x):return 279.89+(x+266.184)*K
# North face of the stone block and the pavilion: measured at y 285.3-286.0 on two cameras, laid
# parallel to the OSM north face through y 285.65 at x -265.45.
def y_north(x):return 285.65+(x+265.45)*K
# The OSM west line (-281.664,259.757) -> (-273.94,277.619), extended north to the north face.
W0=(-281.664,259.757);W1=(-273.94,277.619);WD=((W1[0]-W0[0]),(W1[1]-W0[1]));WL=math.hypot(*WD);WD=(WD[0]/WL,WD[1]/WL)
def west_x(y):return W1[0]+(y-W1[1])*WD[0]/WD[1]
y=285.6
for _ in range(20):y=y_north(west_x(y))
NW=(round(west_x(y),3),round(y,3))
PAV_E=-240.5          # east end of the pavilion (three cameras, -235.8 .. -248; estimated +-3 m)
STONE_D=9.2           # stone block depth from the west line (north face 9.9 m measured on two cameras)
TOP_SET=3.0           # top-floor setback from the stone block's courtyard face
# Heights (measured, see the notes): stone parapet 13.5 (main) / 16.3 (top floor); white wing eaves
# 9.3 and mansard top 12.6; pavilion 5.0 (4.6-5.6 on two cameras) with a 1.1 m glass rail on its roof terrace.
HT={'stone':(13.5,13.5),'stone_top':(16.3,16.3),'white':(9.3,12.6),'pavilion':(5.0,5.0)}
FLOOR0={'stone':0.0,'stone_top':13.5,'white':0.0,'pavilion':0.0}

# The extended footprint: pass 14's modern polygon with its north face from the west line to x PAV_E
# moved to the measured north face (one explicit ring; a union leaves a hair spike on the shared edge).
EXT=[(-273.94,277.619),NW,(PAV_E,round(y_north(PAV_E),3)),(PAV_E,round(y_osm(PAV_E),3))]+MODERN[3:]
ext=Polygon(EXT)
assert ext.is_valid and ext.geom_type=='Polygon'
# Half-plane within STONE_D east of the west line.
nrm=(WD[1],-WD[0])     # east-pointing normal of the west line
def strip(d):
 far=200;a=(W1[0]-WD[0]*far,W1[1]-WD[1]*far);b=(W1[0]+WD[0]*far,W1[1]+WD[1]*far)
 return Polygon([(a[0]-nrm[0]*50,a[1]-nrm[1]*50),(b[0]-nrm[0]*50,b[1]-nrm[1]*50),(b[0]+nrm[0]*d,b[1]+nrm[1]*d),(a[0]+nrm[0]*d,a[1]+nrm[1]*d)])
stone=ext.intersection(strip(STONE_D))
# The top floor stops at the OSM west-line kink (y 259.76): further south the setback face would pinch
# against the street jog. The south end keeps the main roof at 13.5 (estimated, not seen).
stone_top=ext.intersection(strip(STONE_D-TOP_SET)).intersection(Polygon([(-300,259.757),(-200,259.757),(-200,300),(-300,300)]))
pav_region=Polygon([(-300,y_osm(-300)),(PAV_E,y_osm(PAV_E)),(PAV_E,300),(-300,300)])
pav=ext.intersection(pav_region).difference(stone)
white=ext.difference(stone).difference(pav)
def clean(g):
 if g.geom_type!='Polygon':g=max(g.geoms,key=lambda q:q.area)
 g=orient(g.simplify(0.01),1.0);return [(round(x,3),round(y,3)) for x,y in list(g.exterior.coords)[:-1]]
Z={'stone':clean(stone),'stone_top':clean(stone_top),'pavilion':clean(pav),'white':clean(white)}

# Insert every other zone's vertex that lies on an edge, so edges classify cleanly.
def node(ring,others):
 out=[]
 for i,p in enumerate(ring):
  q=ring[(i+1)%len(ring)];out.append(p);L=math.dist(p,q);extra=[]
  for v in others:
   if math.dist(v,p)<.02 or math.dist(v,q)<.02:continue
   t=((v[0]-p[0])*(q[0]-p[0])+(v[1]-p[1])*(q[1]-p[1]))/(L*L)
   if 0<t<1 and math.dist(v,(p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))<.02:extra.append((t,v))
  for t,v in sorted(extra):
   if all(math.dist(v,w)>.02 for w in out+[q]):out.append(v)
 return out
allv=[v for r in list(Z.values())+[OLD,SOUTH_NB] for v in r]
for k in Z:Z[k]=node(Z[k],allv)

# ---------------------------------------------------------------- walls
PG={k:Polygon(v) for k,v in Z.items()};PG_OLD=Polygon(OLD);PG_S=Polygon(SOUTH_NB)
def neighbour(zk,p,q):
 # What lies just outside the edge's midpoint.
 L=math.dist(p,q);mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2;nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
 pt=Point(mx+nx*.15,my+ny*.15)
 if zk=='stone_top' and PG['stone'].contains(pt):return 'stone'
 for k in ('stone','pavilion','white'):
  if k!=zk and PG[k].contains(pt):return k
 if PG_OLD.buffer(.05).contains(pt):return 'old'
 if PG_S.buffer(.05).contains(pt):return 'south'
 return None
NBH={'stone':13.5,'pavilion':0.0,  # walls behind the glass pavilion are built from the ground
 'white':9.3,'old':10.6,'south':SOUTH_H}
walls={}
for zk,ring in Z.items():
 ws=[]
 for p,q in zip(ring,ring[1:]+ring[:1]):
  if math.dist(p,q)<.05:continue
  nb=neighbour(zk,p,q);top=HT[zk][0];base=FLOOR0[zk]
  if zk=='stone_top':
   kind='setback' if nb=='stone' else 'outer';z0=base
  elif nb is None:kind='outer';z0=base
  elif zk=='white' and nb=='old':kind='party_old';z0=8.8;top=10.6     # closes the gap under pass 14's old roof
  elif NBH[nb]<top-.05:kind='upper';z0=NBH[nb]
  else:kind='party';z0=top
  ws.append({'p':list(p),'q':list(q),'z0':z0,'z1':top,'kind':kind,'neighbour':nb})
 walls[zk]=ws

# ---------------------------------------------------------------- roofs
def ring_offset(poly,d):
 # Mitred offset of a counter-clockwise ring; positive d grows the ring outward (as pass 23's).
 n=len(poly);out=[]
 for i in range(n):
  a,b,c=poly[i-1],poly[i],poly[(i+1)%n]
  u1=((b[0]-a[0]),(b[1]-a[1]));l1=math.hypot(*u1);u1=(u1[0]/l1,u1[1]/l1)
  u2=((c[0]-b[0]),(c[1]-b[1]));l2=math.hypot(*u2);u2=(u2[0]/l2,u2[1]/l2)
  n1=(u1[1],-u1[0]);n2=(u2[1],-u2[0]);bis=(n1[0]+n2[0],n1[1]+n2[1]);k=1+n1[0]*n2[0]+n1[1]*n2[1]
  out.append((round(b[0]+bis[0]*d/k,3),round(b[1]+bis[1]*d/k,3)))
 return out
def earclip(ring):
 # Ear clipping that always cuts the fattest ear (largest smallest angle), to avoid slivers.
 pts=list(ring);idx=list(range(len(pts)));tris=[]
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 def inside(p,a,b,c):return cross(a,b,p)>1e-9 and cross(b,c,p)>1e-9 and cross(c,a,p)>1e-9
 def minang(a,b,c):
  def ang(o,p,q):
   v=(p[0]-o[0],p[1]-o[1]);w=(q[0]-o[0],q[1]-o[1]);return math.acos(max(-1,min(1,(v[0]*w[0]+v[1]*w[1])/(math.hypot(*v)*math.hypot(*w)))))
  return min(ang(a,b,c),ang(b,c,a),ang(c,a,b))
 while len(idx)>3:
  best=None
  for i in range(len(idx)):
   a,b,c=pts[idx[i-1]],pts[idx[i]],pts[idx[(i+1)%len(idx)]]
   if cross(a,b,c)<=1e-9:continue
   if any(inside(pts[j],a,b,c) for j in idx if j not in (idx[i-1],idx[i],idx[(i+1)%len(idx)])):continue
   s=minang(a,b,c)
   if best is None or s>best[0]:best=(s,i)
  assert best,'ear clipping failed'
  i=best[1];tris.append((idx[i-1],idx[i],idx[(i+1)%len(idx)]));idx.pop(i)
 tris.append(tuple(idx));return tris
def decollinear(ring):
 # The roof rings drop the vertices the noding inserted on straight edges.
 out=list(ring);changed=True
 while changed:
  changed=False
  for i in range(len(out)):
   a,b,c=out[i-1],out[i],out[(i+1)%len(out)]
   if abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/math.dist(a,c)<.01:out.pop(i);changed=True;break
 return out
RR={k:decollinear(v) for k,v in Z.items()}
WHITE_INSET=1.6
inner=ring_offset(RR['white'],-WHITE_INSET)
outer_eave=ring_offset(RR['white'],.40)
zones={}
for zk,ring in Z.items():
 h,t=HT[zk];zone={'mesh':MESH,'osm':OSM,'kind':zk,'height':h,'top':t,'floor0':FLOOR0[zk],'roof':'mansard' if zk=='white' else 'flat',
  'polygon':[list(v) for v in ring],'roof_ring':[list(v) for v in RR[zk]],'walls':walls[zk]}
 if zk=='white':zone['inner']=[list(v) for v in inner];zone['outer_eave']=[list(v) for v in outer_eave];zone['inset']=WHITE_INSET;zone['roof_tris']=earclip(inner)
 else:zone['roof_tris']=earclip(RR[zk])
 zones[zk]=zone

# ---------------------------------------------------------------- checks
fp=ext.area;zoned=sum(PG[k].area for k in ('stone','pavilion','white'))
ov=sum(PG[a].intersection(PG[b]).area for a,b in [('stone','pavilion'),('stone','white'),('pavilion','white')])
ov_old=sum(PG[k].intersection(PG_OLD).area for k in ('stone','pavilion','white'))
pin=Polygon(inner)
def tri_min_alt(ring,tris):
 m=1e9
 for a,b,c in tris:
  A,B,C=ring[a],ring[b],ring[c];ar=abs((B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0]))/2;L=max(math.dist(A,B),math.dist(B,C),math.dist(C,A));m=min(m,2*ar/L)
 return m
inner_ok=pin.is_valid and pin.area>0 and all(
 ((q[0]-p[0])*(Q[0]-P[0])+(q[1]-p[1])*(Q[1]-P[1]))>0 and math.dist(P,Q)>.25
 for p,q,P,Q in zip(RR['white'],RR['white'][1:]+RR['white'][:1],inner,inner[1:]+inner[:1]))
checks={'footprint_m2':round(fp,1),'osm_modern_m2':round(Polygon(MODERN).area,1),'north_extension_m2':round(fp-Polygon(MODERN).area,1),
 'zoned_m2':round(zoned,1),'overlap_m2':round(ov,3),'overlap_old_m2':round(ov_old,3),'stone_top_outside_stone_m2':round(PG['stone_top'].difference(PG['stone']).area,3),
 'white_inner_valid':inner_ok,'roof_min_tri_altitude_m':{k:round(tri_min_alt(z['inner'] if k=='white' else z['roof_ring'],z['roof_tris']),3) for k,z in zones.items()},
 'north_west_corner':list(NW)}
ok=abs(zoned-fp)<.5 and ov<.01 and ov_old<.05 and checks['stone_top_outside_stone_m2']<.01 and inner_ok and min(checks['roof_min_tri_altitude_m'].values())>.05
data={'source':'pass 14 split of OSM way '+OSM+' (build_landmarks14.py), source/district17.json, three Street View panoramas (view only)','zones':zones,'checks':checks,
 'old_polygon':[list(v) for v in OLD]}
(R/'source/block120.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
report={k:{'area_m2':round(PG[k].area,1),'vertices':len(Z[k]),'walls':{kk:sum(1 for w in walls[k] if w['kind']==kk) for kk in sorted({w['kind'] for w in walls[k]})}} for k in Z}
(R/'previews/block120-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':checks},indent=2,ensure_ascii=False))
print(json.dumps(report));print(checks);print('BLOCK120_ZONES_OK' if ok else 'BLOCK120_ZONES_REVIEW')
