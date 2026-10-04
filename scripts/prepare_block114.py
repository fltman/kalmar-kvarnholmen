"""Pass 114: correction of the round glass drum at 50 Larmgatan (886305409), first built by pass 109.
The OSM ring is a 19-vertex trace of a round building. The drum is rebuilt as a regular 66-facet
polygon (one facet per facade panel column, measured at about 0.84 m) on the circle fitted to the
OSM vertices. One zone, the whole outline.
Heights and the facade rows come from two resected Google Street View panoramas (view only); see
references/block114-notes.md.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block114.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
import numpy as np
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
OSM='886305409';MESH='SM_Kvarnholmen_House_'+OSM
assert MESH in d17,MESH
ring=[tuple(w['p']) for w in d17[MESH]['walls']];PG=Polygon(ring).buffer(0);assert PG.is_valid
# Least-squares circle through the OSM vertices.
P=np.array(ring);A=np.c_[2*P,np.ones(len(P))];s=np.linalg.lstsq(A,(P**2).sum(1),rcond=None)[0]
CX,CY=float(s[0]),float(s[1]);RFIT=math.sqrt(s[2]+CX*CX+CY*CY)
res=[math.hypot(x-CX,y-CY)-RFIT for x,y in ring]
N=66                       # facade panel columns (facets) around the drum, measured about 0.84 m wide
RA=8.80                    # apothem of the panel plane: the facade stands on the OSM line
RC=RA/math.cos(math.pi/N)  # circumradius of the zone polygon
T0=math.atan2(ring[0][1]-CY,ring[0][0]-CX)
poly=[(round(CX+RC*math.cos(T0+2*math.pi*k/N),3),round(CY+RC*math.sin(T0+2*math.pi*k/N),3)) for k in range(N)]
ZP=orient(Polygon(poly))
walls=[{'p':list(p),'q':list(q),'z0':0.0,'z1':10.2,'kind':'outer','neighbour':None} for p,q in zip(poly,poly[1:]+poly[:1])]
# Facade rows bottom-up (z0, z1, kind): 's' short mixed row, 't' tall glass row (a dark ledge at its
# top), 'o' opaque panel row. Measured on the two panoramas, see the notes.
ROWS=[(0.0,.73,'s'),(.73,2.30,'t'),(2.30,3.08,'o'),(3.08,3.83,'s'),(3.83,5.52,'t'),(5.52,6.16,'o'),(6.16,6.85,'s'),(6.85,8.52,'t'),(8.52,9.27,'s'),(9.27,10.08,'o')]
zone={'mesh':MESH,'osm':OSM,'height':10.2,'top':10.2,'roof':'flat','centre':[round(CX,3),round(CY,3)],'osm_fit_radius':round(RFIT,3),
 'apothem':RA,'facets':N,'theta0':round(T0,6),'rows':[list(r) for r in ROWS],'door_angle_deg':-158.4,
 'polygons':[[list(v) for v in list(ZP.exterior.coords)[:-1]]],'walls':walls}
checks={'footprint_m2':round(PG.area,1),'zoned_m2':round(ZP.area,1),'outside_osm_m2':round(ZP.difference(PG).area,2),'osm_not_zoned_m2':round(PG.difference(ZP).area,2),
 'overlap_m2':0.0,'osm_vertex_radius_residual_m':[round(min(res),3),round(max(res),3)]}
data={'source':'district volume '+OSM+' (source/district17.json), '+district['source'],'zones':{'d886':zone},'checks':checks}
(R/'source/block114.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# The 19-vertex OSM ring is inscribed in the circle, so a true round drum on the same circle lies a
# few square metres outside its straight chords. That sliver is expected and bounded here.
ok=checks['outside_osm_m2']<6.0 and checks['osm_not_zoned_m2']<.5 and abs(ZP.area-PG.area)<6.0 and max(map(abs,res))<.25
report={'d886':{'area_m2':round(ZP.area,1),'polygons':1,'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls),1)}}
(R/'previews/block114-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':checks},indent=2,ensure_ascii=False))
print(json.dumps(report));print(checks);print('centre',round(CX,3),round(CY,3),'r',round(RFIT,3));print('BLOCK114_ZONES_OK' if ok else 'BLOCK114_ZONES_REVIEW')
