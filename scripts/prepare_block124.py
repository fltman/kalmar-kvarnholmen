"""Pass 124: the approach to Kalmar slott and its courtyard (corrects pass 27 and pass 98).
This script prepares the one part that needs plan geometry: the park end of the footbridge from
Stadsparken to the ravelin (OSM way 91222140).

Pass 98 laid the whole mainland flat at z 0.30, and pass 27 measured the ravelin and the bridge from
Street View, so the bridge's park end stood 3.8 m above the park with nothing under it. OpenStreetMap
shows what is really there:
- a city wall (way 1084130858) along the north edge of the grassed ditch round the ravelin; the
  bridge lands on it;
- Kungsgatan (way 44397508, sett) and the park footway (way 440762333) arrive at the wall top;
- a wooden stair of 30 steps with a ramp (way 93293022) climbs from the ditch path along the wall to
  the bridge.
So the park stands about one bridge height above the ditch. Pass 98's flat park is lifted here into
a smooth rise round the landing (the "approach"): the ditch stays at 0.30, the city wall retains the
park, and the stair climbs it.

Output (source/block124.json):
- approach: the landing, the lift field's radii, the domain (pass 98's land, inside the lift radius,
  north of the ditch), pass 98's ground layers clipped to the domain on a 1.5 m grid, and the
  domain's walled edges;
- stair: the OSM stair line;
- gate: the OSM line of the gate passage through the west range (way 90613986), and the route the
  walk check follows.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block124.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon,Point,LineString,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text());C27=json.loads((R/'source/castle27.json').read_text())
O98=json.loads((R/'references/osm-slott98.json').read_text())
OSM=ET.parse(R/'references/castle27/osm-castle27.osm').getroot()
NODES={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in OSM.iter('node')}
WAYS={w.get('id'):w for w in OSM.iter('way')}
LAT0,LON0,ROT=56.66412,16.3656,math.radians(28.2)
def local(lat,lon):
 e=(lon-LON0)*111320*math.cos(math.radians(LAT0));n=(lat-LAT0)*111320
 return (round(e*math.cos(ROT)+n*math.sin(ROT),3),round(-e*math.sin(ROT)+n*math.cos(ROT),3))
def way27(wid):return [local(*NODES[nd.get('ref')]) for nd in WAYS[wid].findall('nd')]
def way98(wid):return [tuple(p) for p in O98['w'+wid]['points']]
def poly(piece):return Polygon(piece['outer'],piece.get('holes',[])).buffer(0)
def rnd(v):return [round(v[0],3),round(v[1],3)]
def ring(g):return [rnd(v) for v in list(orient(g).exterior.coords)[:-1]]
def pieces(g,minarea=.02):
 out=[]
 for q in ([g] if g.geom_type=='Polygon' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='Polygon']):
  if q.area<minarea:continue
  q=orient(q);out.append({'outer':ring(q),'holes':[[rnd(v) for v in list(h.coords)[:-1]] for h in q.interiors]})
 return out

# ---------------------------------------------------------------- the landing and the lift field
RV=C27['bridges']['ravelin']['points'];LAND=tuple(RV[0])            # park end of the footbridge (way 91222140)
assert math.dist(LAND,way98('91222140')[0])<.01
R_FLAT,R_FALL=6.0,48.0;RADIUS=R_FLAT+R_FALL
# Heights: the bridge's park end is pass 27's ravelin level less 0.2 m; pass 98's ground is 0.30.
ZRV=round(-1.33+C27['levels_h']['ravelin'],4);Z_TOP=round(ZRV-.2,4);ZG=0.30
land=unary_union([poly(p) for p in B98['land']])
ditch_ring=way98('1084130843')                                     # landuse=grass, the ditch round the ravelin
ditch=Polygon(ditch_ring).buffer(0)
b98_ditch=[g for g in B98['greens'] if g['kind']=='grass' and any(abs(v[0]+934.1)<.2 and abs(v[1]+171.1)<.2 for p in g['pieces'] for v in p['outer'])]
assert len(b98_ditch)==1 and abs(poly(b98_ditch[0]['pieces'][0]).area-ditch.area)<1.0   # pass 98 drew the same ditch
disc=Point(LAND).buffer(RADIUS,256)
domain=land.intersection(disc).difference(ditch).buffer(0)
if domain.geom_type!='Polygon':domain=max(domain.geoms,key=lambda g:g.area)
domain=orient(domain.simplify(.01))
wall=way98('1084130858')                                           # barrier=city_wall along the ditch
assert math.dist(wall[7],LAND)<.01

# Pass 98's ground layers (build_block98.py: land at ZG, greens +0.01 or +0.018, paths +0.025,
# roads +0.03), clipped to the domain and cut on a 1.5 m grid so that the lifted surface can follow
# the field between grid lines.
KG={'park':'Lawn','garden':'Lawn','village_green':'Lawn','grass':'Lawn','common':'Common','grassland':'Common','scrub':'Common','flowerbed':'Flower'}
layers=[('land','Grass',0.0,[poly(p) for p in B98['land']])]
for g in B98['greens']:
 layers.append(('green:'+g['kind'],KG.get(g['kind'],'Lawn'),.018 if g['kind']=='flowerbed' else .01,[poly(p) for p in g['pieces']]))
layers.append(('paths','Gravel',.025,[poly(p) for p in B98['paths']]))
layers.append(('roads','Asphalt',.03,[poly(p) for p in B98['roads']]))
GRID=1.5;minx,miny,maxx,maxy=domain.bounds
cells=[box(minx+i*GRID,miny+j*GRID,minx+(i+1)*GRID,miny+(j+1)*GRID) for i in range(int((maxx-minx)/GRID)+1) for j in range(int((maxy-miny)/GRID)+1)]
cells=[c for c in cells if c.intersects(domain)]
out_layers=[];areas={}
for kind,key,off,polys in layers:
 g=unary_union([p.intersection(domain) for p in polys if p.intersects(domain)])
 if g.is_empty or g.area<.05:continue
 ps=[]
 for c in cells:
  if not c.intersects(g):continue
  ps+=pieces(c.intersection(g))
 areas[kind]=round(sum(Polygon(p['outer'],p['holes']).area for p in ps),2)
 out_layers.append({'kind':kind,'mat':key,'offset':off,'pieces':ps})

# The domain's edges where the lifted park meets the ditch or the water; the arc at the lift radius
# lies on pass 98's ground and gets no wall.
edges=[];ext=list(domain.exterior.coords)[:-1]
for p,q in zip(ext,ext[1:]+ext[:1]):
 mid=((p[0]+q[0])/2,(p[1]+q[1])/2)
 if math.dist(mid,LAND)>RADIUS-.6 or math.dist(p,q)<.02:continue
 L=math.dist(p,q);nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L            # outward for a counter-clockwise ring
 probe=Point(mid[0]+nx*.3,mid[1]+ny*.3)
 side='ditch' if ditch.buffer(.05).contains(probe) else ('land' if land.contains(probe) else 'water')
 edges.append({'p':rnd(p),'q':rnd(q),'side':side})

# The wooden stair (way 93293022: 30 steps, ramp, handrail, wood), from the ditch path up to the bridge.
STAIR=way98('93293022');assert len(STAIR)==2

# ---------------------------------------------------------------- the gate passage and the walk
PASSAGE=way27('90613986')                                          # tunnel=yes, layer -1, sett: outer bailey -> courtyard
assert math.dist(PASSAGE[0],C27['castle_door'])<.05
route={
 'kungsgatan':[rnd(p) for p in way98('44397508')]+[rnd(LAND)],
 'park_east':[rnd(p) for p in way98('440762333')[:4]][::-1]+[rnd(LAND)],
 'ravelin':[rnd(p) for p in way98('91222140')]+[rnd(p) for p in way98('1084130865')[1:]]+[rnd(p) for p in way98('206979655')[1:]],
 'main_bridge':[list(p) for p in C27['bridges']['main']['points']],
 'tunnel':[list(p) for p in C27['tunnel']],
 'bailey':[rnd(p) for p in way27('90613989')],
}

checks={'domain_m2':round(domain.area,1),'land_layer_m2':areas.get('land'),'ditch_overlap_m2':round(domain.intersection(ditch).area,3),
 'layers':areas,'walled_edges':len(edges),'walled_by_side':{s:sum(e['side']==s for e in edges) for s in ('ditch','water','land')},
 'stair_length_m':round(math.dist(*STAIR),2),'landing_on_wall_m':round(LineString(wall).distance(Point(LAND)),3),
 'passage_length_m':round(math.dist(*PASSAGE[:2]),2)}
assert abs(checks['land_layer_m2']-checks['domain_m2'])<.01*checks['domain_m2'],checks    # the clipped ground covers the domain
assert checks['ditch_overlap_m2']<.05
data={'source':'pass 124; OpenStreetMap (references/osm-slott98.json, references/castle27/osm-castle27.osm), ODbL; pass 98 and pass 27 geometry',
 'approach':{'landing':list(LAND),'r_flat':R_FLAT,'r_fall':R_FALL,'z_top':Z_TOP,'zg':ZG,'domain':{'outer':ring(domain),'holes':[[rnd(v) for v in list(h.coords)[:-1]] for h in domain.interiors]},
  'layers':out_layers,'edges':edges,'wall_osm':[rnd(p) for p in wall]},
 'stair':{'osm_way':'93293022','points':[list(p) for p in STAIR],'steps':30},
 'gate':{'passage_osm_way':'90613986','passage':[list(p) for p in PASSAGE]},
 'route':route,'checks':checks}
(R/'source/block124.json').write_text(json.dumps(data,separators=(',',':')))
zones={'pass':124,'approach':{'landing':list(LAND),'radius':RADIUS,'domain_m2':checks['domain_m2'],'layers':areas,'edges':checks['walled_by_side']},
 'stair':data['stair'],'gate':data['gate'],'checks':checks}
(R/'previews/block124-zones.json').write_text(json.dumps(zones,indent=1))
print('BLOCK124_PREPARE_OK',json.dumps(checks))
