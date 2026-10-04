"""Pass 104: Kaggensgatan at Fiskaregatan, the north side of Fiskaregatan and the south side of
Strömgatan (district volumes 92204193, 92379265, 92204176 and 550598948):
- 92204193, its east front on Kaggensgatan (fronts facing local +x), split at the joints seen in
  the photo: the cream boarded gable house at the Fiskaregatan corner, the recessed white link with
  the glazed door, and the tan rendered two-storey house with the black roof and dormers (Gardell);
  the long unseen rest of the outline (west along Fiskaregatan) low and flat;
- 92379265, its west front on Kaggensgatan (fronts facing local -x): the yellow boarded gable house
  at the Fiskaregatan corner (Outnorth), the low white glazed gable shop, and the grey boarded
  one-storey gable house; the unseen rest flat;
- 92204176, its north front on Fiskaregatan: the pale green stucco two-storey house (west) and the
  cream house with a red tiled roof and dormer (east). The OSM ring of this way is broken (the
  courtyard ring is spliced into the outer ring, which leaves a diagonal slit through the street
  front); it is repaired here as the outer ring with the courtyard as a hole. Its recorded area in
  district17 (442.6 m2) is that of the repaired shape;
- 550598948, its north front on Strömgatan: the modern four-storey block (red boarded ground
  storey, two storeys of red render, a grey metal top storey), 12.5 m deep; the unseen rest of the
  big outline (the north wing behind it and the south part along Fiskaregatan) flat.
Heights from three resected Google Street View panoramas (see references/block104-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block104.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['92204193','92379265','92204176','550598948']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:
 assert MESH[i] in d17,MESH[i]
 assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
# Repair of 92204176: vertices 0-3 are the outer ring, 4-9 the courtyard.
r176=ring('92204176');RAW176=PG['92204176']
PG['92204176']=Polygon(r176[:4],[r176[4:]]).buffer(0)
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
X=lambda x0,x1,y0,y1:sbox(x0,y0,x1,y1)
GEO={}
P=PG['92204193']   # east front x -190.6; joints at y 157.05 and 159.23 (resected)
GEO['c193']=P.intersection(X(-201.0,-180,140,157.05))
GEO['l193']=P.intersection(X(-199.0,-180,157.05,159.23))
GEO['b193']=P.intersection(X(-203.0,-180,159.23,190))
GEO['r193']=P.difference(unary_union([GEO['c193'],GEO['l193'],GEO['b193']]))
P=PG['92379265']   # west front x -180.2; joints at y 155.2 and 162.9 (resected)
GEO['y265']=P.intersection(X(-190,-170.5,140,155.2))
GEO['w265']=P.intersection(X(-190,-172.0,155.2,162.9))
GEO['g265']=P.intersection(X(-190,-168.0,162.9,180))
GEO['r265']=P.difference(unary_union([GEO['y265'],GEO['w265'],GEO['g265']]))
P=PG['92204176']   # north front y 134.5; joint at x -141.9 (resected)
GEO['g176']=P.intersection(X(-160,-141.9,126.5,140))
GEO['y176']=P.intersection(X(-141.9,-120,126.5,140))
GEO['r176']=P.difference(unary_union([GEO['g176'],GEO['y176']]))
P=PG['550598948']  # north front y 205.2 on Strömgatan
GEO['m948']=P.intersection(X(-130,-75,193.0,210))
GEO['n948']=P.intersection(X(-130,-75,174.5,193.0))
GEO['s948']=P.difference(unary_union([GEO['m948'],GEO['n948']]))
# Heights (m) above the street: eaves 'height', ridge 'top'. est = not seen, estimated.
# roof: 'gable_street' ridge at right angles to the street front; 'saddle' ridge along it; 'flat'.
spec={
 'c193':dict(height=5.56,top=9.46,roof='gable_street',osm='92204193'),
 'l193':dict(height=5.40,top=5.40,roof='flat',osm='92204193'),
 'b193':dict(height=6.00,top=10.80,roof='saddle',osm='92204193'),
 'r193':dict(height=7.00,top=7.00,roof='flat',osm='92204193',est=True),
 'y265':dict(height=5.25,top=7.11,roof='gable_street',osm='92379265'),
 'w265':dict(height=2.70,top=4.61,roof='flat',osm='92379265'),
 'g265':dict(height=2.81,top=4.57,roof='gable_street',osm='92379265'),
 'r265':dict(height=6.00,top=6.00,roof='flat',osm='92379265',est=True),
 'g176':dict(height=7.57,top=9.00,roof='saddle',osm='92204176'),
 'y176':dict(height=5.10,top=8.30,roof='saddle',osm='92204176'),
 'r176':dict(height=6.00,top=6.00,roof='flat',osm='92204176',est=True),
 'm948':dict(height=13.60,top=13.60,roof='flat',osm='550598948'),
 'n948':dict(height=10.70,top=10.70,roof='flat',osm='550598948',est=True),
 's948':dict(height=9.75,top=9.75,roof='flat',osm='550598948',est=True),
}
for z in spec:spec[z]['mesh']=MESH[spec[z]['osm']]
taken=Polygon();zones={}
for name in spec:
 ps=parts(GEO[name].difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
 assert ps,name
 for p in ps:assert not p.interiors,name
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
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json; 92204176 repaired as outer ring minus courtyard), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),
  'repair_176_raw_m2':round(RAW176.area,1),'repair_176_m2':round(PG['92204176'].area,1),'repair_176_district_area_m2':round(d17[MESH['92204176']]['area'],1),
  'repair_176_outside_raw_m2':round(PG['92204176'].difference(RAW176).area,1)}}
(R/'source/block104.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and abs(c['repair_176_m2']-c['repair_176_district_area_m2'])<2
(R/'previews/block104-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK104_ZONES_OK' if ok else 'BLOCK104_ZONES_REVIEW')
