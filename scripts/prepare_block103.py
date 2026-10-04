"""Pass 103: corrects pass 85's prison building (Anstalten Kalmar, OSM way 91053122). Pass 85 cut the
outline into three zones and laid boxed hipped roofs over them, which overlapped; its walls were
ochre with a generic window grid. Satellite imagery and the winter photograph from the Västerport
bridge (both view only) show a cross-shaped cell prison instead:
- the main cell range, 52.5 x 13 m, three storeys, running north-south (local bearing 30);
- the taller cross wing, 12.5 m wide, projecting 15 m east toward the water, with its pedimented
  gable end on the east;
- low one-storey annexes in the corner south of the cross wing;
- a modern flat-roofed range at the north end.
This script splits the OSM outline into those parts in the frame of the main range (s along it from
its south end, t across it toward the east) and writes source/block103.json.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block103.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
O=json.loads((R/'references/osm-prison85.json').read_text())
P=Polygon(O['91053122']['points']).buffer(0)
# Frame of the main range: origin at its south-west corner (OSM vertex 13), along its west face.
o=(-468.622,132.741);a=(-449.183,166.199);L=math.dist(o,a);d=((a[0]-o[0])/L,(a[1]-o[1])/L);n=(d[1],-d[0])
def X(s,t):return (o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
def rect(s0,s1,t0,t1):return Polygon([X(s0,t0),X(s1,t0),X(s1,t1),X(s0,t1)]).buffer(0)
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def ring(g):return [[round(c,3) for c in v] for v in list(orient(g.simplify(.05)).exterior.coords)[:-1]]
# Main range and cross wing from the OSM vertices: main s 0-52.5, t 0-13.0; wing s 20.0-32.5 out to
# t 27.9 (the east gable face, OSM vertices 1 and 2).
MAIN=dict(s0=0.0,s1=52.5,t0=0.0,t1=13.0)
WING=dict(s0=20.0,s1=32.5,t0=0.0,t1=27.9)
main=rect(MAIN['s0'],MAIN['s1'],MAIN['t0'],MAIN['t1']);wing=rect(WING['s0'],WING['s1'],13.0,WING['t1'])
rest=P.difference(unary_union([main,wing]).buffer(.05))
annex=[g for g in flat(rest) if g.area>3 and g.centroid.distance(Polygon([X(0,13),X(20,13),X(20,30),X(0,30)]))<1]
north=[g for g in flat(rest) if g.area>3 and g not in annex]
data={'frame':{'origin':o,'along':d,'across':n},'main':MAIN,'wing':WING,
 'annex':[ring(g) for g in annex],'north':[ring(g) for g in north],
 # Heights (m) above the yard: main eaves and ridge from storey count and the winter photograph
 # (three storeys under a low saddle), the wing scaled from the same photograph against the main
 # range with the distance ratio 96:81 from the camera on the bridge.
 'levels':{'main_eaves':10.2,'main_ridge':13.6,'wing_eaves':13.0,'wing_apex':17.8,'annex':4.2,'north':7.0},
 'checks':{'outline_m2':round(P.area,1),'main_in_outline_m2':round(main.intersection(P).area,1),'main_m2':round(main.area,1),
  'wing_in_outline_m2':round(wing.intersection(P).area,1),'wing_m2':round(wing.area,1),'annex_m2':round(sum(g.area for g in annex),1),
  'north_m2':round(sum(g.area for g in north),1)}}
c=data['checks'];ok=c['main_in_outline_m2']>.97*c['main_m2'] and c['wing_in_outline_m2']>.95*c['wing_m2']
(R/'source/block103.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
print(c);print('BLOCK103_PREP_OK' if ok else 'BLOCK103_PREP_REVIEW')
