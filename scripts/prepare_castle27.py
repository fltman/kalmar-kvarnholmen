"""Pass 27: Kalmar slott on Slottsholmen, with its ramparts, the four postejer, the dry moat, the
bridge and drawbridge, the ravelin with the castellan's house and the islets of Slottsfjärden.
Every outline comes from OpenStreetMap (references/castle27/osm-castle27.osm, ODbL); heights come
from Google Street View (September 2014), measured by inverting the panorama camera, and from
Helgo Zettervall's 1883 west elevation, which agrees with the measurements (see notes).
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_castle27.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon,Point,LineString,MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union,split
R=Path(__file__).resolve().parents[1]
OSM=ET.parse(R/'references/castle27/osm-castle27.osm').getroot()
NODES={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in OSM.iter('node')}
WAYS={w.get('id'):w for w in OSM.iter('way')}
LAT0,LON0,ROT=56.66412,16.3656,math.radians(28.2)
def local(lat,lon):
 e=(lon-LON0)*111320*math.cos(math.radians(LAT0));n=(lat-LAT0)*111320
 return (round(e*math.cos(ROT)+n*math.sin(ROT),3),round(-e*math.sin(ROT)+n*math.cos(ROT),3))
def way(wid):
 p=[local(*NODES[nd.get('ref')]) for nd in WAYS[wid].findall('nd')]
 return p[:-1] if len(p)>2 and p[0]==p[-1] else p
def tags(wid):return {t.get('k'):t.get('v') for t in WAYS[wid].findall('tag')}
def ring(g):return [list(v) for v in list(orient(g).exterior.coords)[:-1]]
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='Polygon']
def pieces(g,minarea=1.0):
 out=[]
 for q in flat(g):
  if q.area<minarea:continue
  out.append({'outer':ring(q),'holes':[[list(v) for v in list(h.coords)[:-1]] for h in orient(q).interiors]})
 return out
# Heights in metres above the water of the moat and Slottsfjärden. The model's water plane is at
# z=-1.33, so z = WATER + h. Street View, 2014 (see references/castle27-notes.md):
#  rampart camera 13.5 m above the water: castle foot -8.6, eaves +8.2, tower walls +11.7/+12.0,
#  finials +30.6/+29.0, south postej wall top -0.1 and foot -11.6, dry moat wall coping -2.5..-3.0;
#  bridge camera: water -7.9, camera 2.2-2.6 m above the deck; courtyard (resected camera): eaves
#  12.2 m above the courtyard floor. Kuretornet from the bridge, tied to the west tower's wall top:
#  cornice 27.1-27.3, lantern base ~36.8, crown ~54 m above the castle foot (Zettervall 1883: 27.0
#  and 53.9 m).
WATER=-1.33
H=dict(curtain_top=6.8,berm_low=1.5,berm_high=5.0,foot=5.0,gate=5.0,deck=5.0,courtyard=9.5,rampart=11.4,coping=11.0,ring_coping=11.2,
 eaves=21.6,postej_foot=1.2,postej_top=13.4,ravelin=5.6,ravelin_parapet=7.2,islet=0.5)
Z={k:round(WATER+v,3) for k,v in H.items()};Z['water']=WATER
# ---------------------------------------------------------------- island and fortification
island=orient(Polygon(way('23228811')).buffer(0))
post_ids={'W':'90613967','S':'90614026','E':'90613973','N':'90613977'}
postejer={}
for key,wid in post_ids.items():
 g=Polygon(way(wid)).buffer(0);c=g.centroid
 postejer[key]={'osm_way':wid,'centre':[round(c.x,3),round(c.y,3)],'radius':round(math.sqrt(g.area/math.pi),3),'polygon':ring(g),
  'round':key!='N','area_m2':round(g.area,1)}
curtain_ids=[('NW','90614013'),('SW','90614008'),('SE','90614025'),('NE','90614009')]
outline=[]
for side,wid in curtain_ids:outline+=way(wid)
rampart_outer=orient(Polygon(outline).buffer(0))
post_union=unary_union([Polygon(p['polygon']) for p in postejer.values()])
fort=unary_union([rampart_outer,post_union])
ring_poly=orient(Polygon(way('90613964')).buffer(0))   # dry moat counterscarp (retaining wall)
castle_outer=orient(Polygon(way('90613970')).buffer(0));court=orient(Polygon(way('90614029')).buffer(0))
dry_moat=ring_poly.difference(castle_outer)
terreplein=rampart_outer.difference(ring_poly).difference(post_union)
# Berms outside the curtain: the north-west side (lower wall, berm and revetment, photographs from
# the park and Street View on the bridge) is a high berm at the gate level; the other sides are low
# grass berms with boulder riprap at the water.
berm=island.difference(fort)
cent=island.centroid
def wedge(a,b):
 # sector from the island centre through two neighbouring postejer, far beyond the shore
 pa,pb=postejer[a]['centre'],postejer[b]['centre']
 far=lambda p:(cent.x+(p[0]-cent.x)*6,cent.y+(p[1]-cent.y)*6)
 return Polygon([(cent.x,cent.y),far(pa),far(pb)]).buffer(0)
berms={}
for side,(a,b) in {'NW':('N','W'),'SW':('W','S'),'SE':('S','E'),'NE':('E','N')}.items():
 berms[side]=[g for g in flat(berm.intersection(wedge(a,b))) if g.area>=2]
low_wall=LineString(way('1084130859'))
curtains=[]
for side,wid in curtain_ids:
 pts=way(wid)
 # trim each curtain where it runs into a postej, so the wall stops at the bastion face
 L=LineString(pts).difference(post_union.buffer(.05))
 segs=[list(map(list,g.coords)) for g in (L.geoms if hasattr(L,'geoms') else [L]) if g.length>1]
 base=H['berm_high'] if side=='NW' else H['berm_low']
 curtains.append({'side':side,'osm_way':wid,'runs':segs,'foot_h':base,'top_h':H['coping'],'batter':0.18 if side=='NW' else 0.08})
# ---------------------------------------------------------------- castle
CO=way('90613970');CI=way('90614029')
co=list(orient(Polygon(CO)).exterior.coords)[:-1];ci=list(orient(Polygon(CI)).exterior.coords)[:-1]
towers={}
for key,wid in [('W','628144756'),('S','628144757'),('E','628144758'),('N','628144759')]:
 g=Polygon(way(wid)).buffer(0);c=g.centroid;towers[key]={'osm_way':wid,'centre':[round(c.x,3),round(c.y,3)],'radius':round(math.sqrt(g.area/math.pi),3)}
kure=orient(Polygon(way('628144976')).buffer(0))
# Kuretornet as a rectangle on its longest side (the model builds its walls and bell roof on it).
kp_=list(kure.exterior.coords)[:-1];ek=max(zip(kp_,kp_[1:]+kp_[:1]),key=lambda e:math.dist(*e));ka=math.atan2(ek[1][1]-ek[0][1],ek[1][0]-ek[0][0])
ku_=(math.cos(ka),math.sin(ka));kv_=(-ku_[1],ku_[0]);kc=kure.centroid
us_=[(v[0]-kc.x)*ku_[0]+(v[1]-kc.y)*ku_[1] for v in kp_];vs_=[(v[0]-kc.x)*kv_[0]+(v[1]-kc.y)*kv_[1] for v in kp_]
kcx_=kc.x+ku_[0]*(max(us_)+min(us_))/2+kv_[0]*(max(vs_)+min(vs_))/2;kcy_=kc.y+ku_[1]*(max(us_)+min(us_))/2+kv_[1]*(max(vs_)+min(vs_))/2
hu_,hv_=(max(us_)-min(us_))/2,(max(vs_)-min(vs_))/2
kure_rect=[[round(kcx_+ku_[0]*a_*hu_+kv_[0]*b_*hv_,3),round(kcy_+ku_[1]*a_*hu_+kv_[1]*b_*hv_,3)] for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))]
well=Polygon(way('1084130848')).centroid
def fit_range(name,outer,inner,ends):
 # A rectangle along the range: axis from the averaged outer/inner direction, cross-section from
 # the innermost courtyard point to the outermost facade point, ends at the corner towers.
 ux=sum(q[0]-p[0] for p,q in outer+inner);uy=sum(q[1]-p[1] for p,q in outer+inner);L=math.hypot(ux,uy);ux,uy=ux/L,uy/L
 nx,ny=uy,-ux  # outward for a CCW footprint
 o=outer[0][0];cross=lambda p:(p[0]-o[0])*nx+(p[1]-o[1])*ny;along=lambda p:(p[0]-o[0])*ux+(p[1]-o[1])*uy
 out_d=max(cross(p) for s in outer for p in s);in_d=min(cross(p) for s in inner for p in s)
 s0=min(along(p) for p in ends);s1=max(along(p) for p in ends)
 return {'name':name,'origin':list(o),'u':[round(ux,6),round(uy,6)],'n':[round(nx,6),round(ny,6)],'s0':round(s0,3),'s1':round(s1,3),
  'outer':round(out_d,3),'inner':round(in_d,3),'depth':round(out_d-in_d,3)}
def seg(P,i,j):return [(P[i],P[i+1]) for i in range(i,j)]
T={k:tuple(v['centre']) for k,v in towers.items()}
ranges=[
 fit_range('SW',seg(CO,7,10),seg(CI,1,2),[T['W'],T['S']]),
 fit_range('SE_w',[(CO[22],CO[23])],seg(CI,2,3),[T['S'],CO[23]]),
 fit_range('SE_e',[(CO[26],CO[27]),(CO[30],CO[32])],seg(CI,3,5),[CO[26],T['E']]),
 fit_range('NE',[(CO[39],CO[41]),(CO[45],CO[46])],seg(CI,5,8),[T['E'],T['N']]),
 fit_range('NW',[(CO[55],CO[56]),(CO[60],CO[0])],seg(CI,8,10)+[(CI[10],CI[0])],[T['N'],T['W']]),
]
bays=[{'name':'bay1','polygon':[list(CO[i]) for i in range(23,27)]},{'name':'bay2','polygon':[list(CO[i]) for i in range(27,31)]}]
# ---------------------------------------------------------------- gate, tunnel, entrance, bridges
gate_out=local(*NODES['265787093']);gate_in=local(*NODES['1051549610'])
passage=orient(Polygon(way('1084130856')).buffer(0))   # walled entrance causeway, 5 m walls
south_court=orient(Polygon(way('1084130853')).buffer(0))
bridges={
 'main':{'osm_way':'24455363','points':way('24455363'),'deck_h':H['deck'],'width':3.2},
 'drawbridge':{'osm_way':'1084130862','points':way('1084130862')},
 'ravelin':{'osm_way':'91222140','points':way('91222140'),'deck_h':H['ravelin'],'width':2.6},
 'north_east':{'osm_way':'1084130845','points':way('1084130845'),'width':2.4},
 'south':{'osm_way':'368199596','points':way('368199596'),'width':3.0},
}
walls={'east_corner':way('1084130844'),'north_postej':way('1084130860'),'east_gate':list(local(*NODES['1051549480']))}
dry_path=way('90614021')
# ---------------------------------------------------------------- ravelin and islets
rv_band=way('1084130864')
ravelin_poly=orient(Polygon([(-965.5,-188.1),(-923.7,-200.1),(-913.9,-212.7)]+way('1084130863')[::-1]+[(-954.1,-244.5),(-964.0,-231.5)]).buffer(0))
parapet=orient(Polygon(rv_band).buffer(0)).intersection(ravelin_poly)
# The bridge from the park lands on the ravelin's north face; its path runs through a gap in the
# raised grass parapet (the parapet would otherwise stand across the landing).
rv_gap=LineString(way('91222140')[-2:]+way('1084130865')+way('206979655')[:3]).buffer(1.7,cap_style=2)
parapet=parapet.difference(rv_gap)
villa=Polygon(way('93293028'))
islets=[{'osm_way':w,'polygon':ring(Polygon(way(w)).buffer(0)),'area_m2':round(Polygon(way(w)).area,1)} for w in ('90977141','90831117','4222113')]
# ---------------------------------------------------------------- paths
paths=[]
for wid,w in WAYS.items():
 t=tags(wid)
 if t.get('highway') not in ('footway','path','steps','track','pedestrian') or t.get('bridge')=='yes':continue
 pts=way(wid);L=LineString(pts)
 if L.length<1 or not (island.buffer(2).intersects(L) or ravelin_poly.buffer(2).intersects(L)):continue
 paths.append({'osm_way':wid,'kind':t['highway'],'surface':t.get('surface',''),'points':[list(p) for p in pts]})
# ---------------------------------------------------------------- cannons on the ramparts
# Cast-iron guns on timber carriages line the south-west rampart (Street View 2014) and the
# north-west rampart north of the gate (photographs from the park); spacing from the 2021 aerials.
cannons=[]
def along_edge(line,offset,spacing,start,stop,face_out):
 L=line.length;d=start
 while d<=L-stop:
  p=line.interpolate(d);q=line.interpolate(min(L,d+.5));ux,uy=(q.x-p.x)/.5,(q.y-p.y)/.5;ul=math.hypot(ux,uy);ux,uy=ux/ul,uy/ul
  nx,ny=uy,-ux
  if not face_out:nx,ny=-nx,-ny
  cannons.append({'at':[round(p.x-nx*offset,3),round(p.y-ny*offset,3)],'facing':[round(nx,4),round(ny,4)]});d+=spacing
along_edge(LineString(way('90614008')),7.4,9.5,16,14,True)   # beyond the top of the grassed slope
nw=LineString(way('90614013'));along_edge(LineString([nw.interpolate(8).coords[0],nw.interpolate(52).coords[0]]),3.4,9.0,2,2,True)
# ---------------------------------------------------------------- rampart slopes over the low curtains
# On the south-west, south-east and north-east sides a stone curtain about 5 m high carries a steep
# grassed slope up to the rampart top (photographs 2019-22; Street View on the south-west rampart
# looks down that slope to the coping). The north-west revetment rises to the rampart itself.
def mitred(pts):
 n=len(pts);out=[]
 for i in range(n):
  ds=[]
  pairs=([(pts[i-1],pts[i])] if i>0 else [])+([(pts[i],pts[i+1])] if i<n-1 else [])
  for a_,b_ in pairs:
   L_=math.dist(a_,b_);ds.append(((b_[1]-a_[1])/L_,-(b_[0]-a_[0])/L_))
  nx_=sum(d[0] for d in ds);ny_=sum(d[1] for d in ds);k_=math.hypot(nx_,ny_);sc=1
  if len(ds)==2:dot=ds[0][0]*ds[1][0]+ds[0][1]*ds[1][1];sc=1/max(.35,math.sqrt((1+dot)/2))
  out.append((nx_/k_*sc,ny_/k_*sc))
 return out
SLOPE_W=6.0;slopes=[];bands=[]
def densify(pts,step):
 out=[list(pts[0])]
 for a_,b_ in zip(pts,pts[1:]):
  n_=max(1,int(math.dist(a_,b_)/step));out+=[[a_[0]+(b_[0]-a_[0])*k/n_,a_[1]+(b_[1]-a_[1])*k/n_] for k in range(1,n_+1)]
 return out
for cur in curtains:
 if cur['side']=='NW':continue
 for run in cur['runs']:
  # The slope narrows to 2.2 m towards the postejer, where the rampart walk passes close to the edge.
  run=densify(run,2.0);acc=[0.0]
  for a_,b_ in zip(run,run[1:]):acc.append(acc[-1]+math.dist(a_,b_))
  Lr=acc[-1];ws=[min(SLOPE_W,2.2+3.8*max(0,min(d,Lr-d)-8)/14) for d in acc]
  ns=mitred(run);inner=[[round(p_[0]-n_[0]*w_,3),round(p_[1]-n_[1]*w_,3)] for p_,n_,w_ in zip(run,ns,ws)]
  slopes.append({'side':cur['side'],'outer':run,'inner':inner});bands.append(Polygon(run+inner[::-1]).buffer(0))
terreplein_flat=terreplein.difference(unary_union(bands))
# ---------------------------------------------------------------- surface zones and gravel paths
# North-west berm: the lower wall splits it into the walkway at the gate level (behind the wall)
# and a low strip of grass and boulders in front of it, at the water.
lw=list(low_wall.coords);(ax,ay),(bx,by)=lw[0],lw[-1];L=math.hypot(bx-ax,by-ay);ux,uy=(bx-ax)/L,(by-ay)/L
ext=[(ax-ux*8,ay-uy*8),(bx+ux*8,by+uy*8)];nx,ny=uy,-ux
if (cent.x-ax)*nx+(cent.y-ay)*ny<0:nx,ny=-nx,-ny
inner_side=Polygon(ext+[(ext[1][0]+nx*40,ext[1][1]+ny*40),(ext[0][0]+nx*40,ext[0][1]+ny*40)])
nw_berm=unary_union(berms['NW']);nw_walk=nw_berm.intersection(inner_side);nw_shore=nw_berm.difference(inner_side)
rv_inner=ravelin_poly.difference(parapet)
# The outer 2.2 m of every berm is the sloping grassed bank under the riprap (built in Blender).
shore_in=island.buffer(-2.2,join_style=2)
def path_buffers(zone):
 out=[]
 for pth in paths:
  if pth['kind']=='steps':continue
  w=1.8 if pth['surface'] in ('compacted','pebblestone','dirt','grass') else 1.6
  out.append(LineString(pth['points']).buffer(w/2,cap_style=2,join_style=2))
 return unary_union(out).intersection(zone.buffer(-.15))
path_zones=[('terreplein',terreplein_flat,H['rampart']),('dry_moat',dry_moat,H['foot']),('nw_walk',nw_walk,H['berm_high']),('ravelin',rv_inner,H['ravelin'])]
path_surfaces=[{'zone':z,'h':h,'pieces':pieces(path_buffers(g),.5)} for z,g,h in path_zones]
# ---------------------------------------------------------------- checks and output
checks={'island_m2':round(island.area,1),'fort_m2':round(fort.area,1),'terreplein_m2':round(terreplein.area,1),'dry_moat_m2':round(dry_moat.area,1),
 'castle_m2':round(castle_outer.area,1),'courtyard_m2':round(court.area,1),'berm_m2':{k:round(sum(g.area for g in v),1) for k,v in berms.items()},
 'fort_outside_island_m2':round(fort.difference(island).area,2),'ring_outside_rampart_m2':round(ring_poly.difference(rampart_outer).area,2),
 'castle_outside_ring_m2':round(castle_outer.difference(ring_poly).area,2),'ranges':{r['name']:r['depth'] for r in ranges},
 'ravelin_m2':round(ravelin_poly.area,1),'villa_inside_ravelin':bool(ravelin_poly.contains(villa)),'lower_wall_inside_island':bool(island.contains(low_wall)),
 'cannons':len(cannons),'paths':len(paths),'nw_walk_m2':round(nw_walk.area,1),'nw_shore_m2':round(nw_shore.area,1),
 'path_m2':{z['zone']:round(sum(Polygon(q['outer'],q['holes']).area for q in z['pieces']),1) for z in path_surfaces}}
data={'source':'OpenStreetMap contributors (ODbL), references/castle27/osm-castle27.osm; heights: see references/castle27-notes.md',
 'levels_h':H,'levels_z':Z,
 'island':pieces(island),'fort':pieces(fort),'terreplein':pieces(terreplein_flat),'slopes':slopes,'dry_moat':pieces(dry_moat),'ring':ring(ring_poly),
 'berms':{k:pieces(unary_union(v).intersection(shore_in)) for k,v in berms.items() if k!='NW'},'nw_walk':pieces(nw_walk),'nw_shore':pieces(nw_shore.intersection(shore_in)),'path_surfaces':path_surfaces,'curtains':curtains,'lower_wall':[list(p) for p in low_wall.coords],
 'postejer':postejer,'castle':{'outer':[list(p) for p in co],'court':[list(p) for p in ci],'towers':towers,'kure':ring(kure),'kure_rect':kure_rect,
  'well':[round(well.x,3),round(well.y,3)],'ranges':ranges,'bays':bays},
 'gate':{'outer':list(gate_out),'inner':list(gate_in)},'dry_moat_path':[list(v) for v in dry_path],
 'tunnel':[list(v) for v in way('90614014')],'corridor_doors':[list(v) for v in way('1084130855')],'castle_door':list(way('90613986')[0]),'passage':ring(passage),'south_court':ring(south_court),'bridges':bridges,'walls':walls,
 'ravelin':{'polygon':ring(ravelin_poly),'parapet':pieces(parapet),'inner':pieces(rv_inner),'villa':ring(villa),'villa_osm_way':'93293028'},
 'islets':islets,'paths':paths,'cannons':cannons,'checks':checks}
(R/'source/castle27.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
ok=checks['fort_outside_island_m2']<60 and checks['ring_outside_rampart_m2']<1 and checks['castle_outside_ring_m2']<1 and checks['villa_inside_ravelin']
(R/'previews/castle27-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','checks':checks},indent=2,ensure_ascii=False))
print(json.dumps(checks,ensure_ascii=False,indent=1));print('CASTLE27_ZONES_OK' if ok else 'CASTLE27_ZONES_REVIEW')
