"""Pass 110: ten generic pass-17 volumes on Storgatan, Norra Långgatan, Södra Långgatan and Västra
Sjögatan:
- Storgatan, north side: 91265011 (the 1960s stone-clad commercial block, one zone), 91970373 (the
  yellow two-storey Viore house: a 12 m front range and the unseen rear), 91970296 (split at the
  line x -103.43 of the OSM rear wing: the yellow Sakligheter house to the west, the brown granite
  Synsam house to the east, both as 12 m front ranges, and the unseen rear);
- Storgatan, south side: 92379278 (Dillbergs Bokhandel) and 92379304 (the limestone front), one
  zone each;
- 92379276 (25 Södra Långgatan): the front range south of y -58.5 and the rear wings;
- 92412841 (4 Västra Sjögatan): the green boarded house, one zone;
- Norra Långgatan: 92204180 split at the OSM line through (-132.38, 104.41)-(-132.0, 134.34),
  which the resected panorama puts on the visible joint (white render west, the louvred house
  east); 91264997 (the Åhléns/Kvasten block, one zone); 91970385 split at the rear OSM vertex x
  -58.67 (orange four-storey west, beige three-storey east; joint estimated from the contributor
  photo).
Heights from the resected Google panoramas and the contributor photos (see
references/block110-notes.md). Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block110.py
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
IDS=['91265011','92379278','92379304','91970373','91970296','92379276','92412841','92204180','91264997','91970385']
MESH={i:('SM_Kvarnholmen_House_'+i if i in ('92412841','92204180') else 'SM_Building_'+i) for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i];assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# Front ranges on Storgatan's north side: 12 m deep (the depth is not seen; estimated).
south=half((0,14.6),(-1,14.6),True)          # y < 14.6
P=PG['91970373'];v373=P.intersection(south);r373=P.difference(v373)
P=PG['91970296'];W=half((-103.43,33.04),(-103.16,63.3),True)   # west of the rear wing's line
s296=P.intersection(W).intersection(south);y296=P.difference(W).intersection(south);r296=P.difference(s296).difference(y296)
P=PG['92379276'];w276=P.intersection(half((0,-58.5),(-1,-58.5),True));b276=P.difference(w276)
P=PG['92204180'];w180=P.intersection(half((-132.38,104.41),(-132.0,134.34),True));l180=P.difference(w180)
P=PG['91970385'];o385=P.intersection(half((-58.67,40.0),(-58.67,70.0),True));b385=P.difference(o385)
GEO={'g011':PG['91265011'],'d278':PG['92379278'],'l304':PG['92379304'],'v373':v373,'r373':r373,'s296':s296,'y296':y296,'r296':r296,
 'w276':w276,'b276':b276,'g841':PG['92412841'],'w180':w180,'l180':l180,'a997':PG['91264997'],'o385':o385,'b385':b385}
# Heights (m) above the pavement: eaves 'height', ridge or roof top 'top'. est=True: not measured.
# roof: 'flat', 'saddle' (ridge along the street front), 'hip'.
spec={
 'g011':dict(height=8.20,top=8.20,roof='flat',osm='91265011',est=True),
 'd278':dict(height=10.00,top=12.40,roof='saddle',osm='92379278',est=True),
 'l304':dict(height=7.80,top=7.80,roof='flat',osm='92379304',est=True),
 'v373':dict(height=7.40,top=9.90,roof='saddle',osm='91970373',est=True),
 'r373':dict(height=7.40,top=7.40,roof='flat',osm='91970373',est=True),
 's296':dict(height=7.60,top=7.60,roof='flat',osm='91970296',est=True),
 'y296':dict(height=13.40,top=13.40,roof='flat',osm='91970296',est=True),
 'r296':dict(height=10.20,top=10.20,roof='flat',osm='91970296',est=True),
 'w276':dict(height=7.45,top=10.60,roof='saddle',osm='92379276'),
 'b276':dict(height=6.60,top=6.60,roof='flat',osm='92379276',est=True),
 'g841':dict(height=6.85,top=12.60,roof='hip',osm='92412841'),
 'w180':dict(height=7.45,top=7.45,roof='flat',osm='92204180'),
 'l180':dict(height=7.85,top=7.85,roof='flat',osm='92204180'),
 'a997':dict(height=9.30,top=9.30,roof='flat',osm='91264997'),
 'o385':dict(height=12.60,top=12.60,roof='flat',osm='91970385',est=True),
 'b385':dict(height=9.80,top=12.00,roof='saddle',osm='91970385',est=True),
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
(R/'source/block110.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block110-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK110_ZONES_OK' if ok else 'BLOCK110_ZONES_REVIEW')
