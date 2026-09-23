"""Pass 25: tracks and platforms at Kalmar C from OpenStreetMap, clipped to the modelled land.
Writes source/rail25.json: track centrelines, the ballast bed, the land cut (bed plus a 1.2 m
slope band, minus platforms), platform areas, buffer stops, signals, crossings, and the
ground surfaces the cut touches. Levels: platform top +0.15 m (the station's platform doors),
rail top 0.58 m below it, ballast at -0.66 m so the timber sleepers stand 4 cm proud. Run with Shapely:
KALMAR_GEO=/path/to/site-packages python3 prepare_rail25.py
"""
from pathlib import Path
import json,math,os,sys
import xml.etree.ElementTree as E
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,LineString,Point,MultiLineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union,linemerge
from shapely import constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1]
lat0,lon0=56.66412,16.3656;a=math.radians(28.2)
def project(lat,lon):
 e=(lon-lon0)*111320*math.cos(math.radians(lat0));n=(lat-lat0)*111320
 return (round(e*math.cos(a)+n*math.sin(a),3),round(-e*math.sin(a)+n*math.cos(a),3))
root=E.parse(R/'references/osm-kvarnholmen-full.osm').getroot()
def tags(e):return {t.get('k'):t.get('v') for t in e.findall('tag')}
nodes={};ntags={}
for n in root.findall('node'):
 nodes[n.get('id')]=project(float(n.get('lat')),float(n.get('lon')));t=tags(n)
 if t:ntags[n.get('id')]=t
district=json.loads((R/'source/kvarnholmen.json').read_text())
land=Polygon(district['land'][0]['outer'],[h for h in district['land'][0].get('holes',[])]).buffer(0)
RAIL_TOP,PLATFORM_TOP,BALLAST=-0.43,0.15,-0.66
GAUGE_OFFSET=0.7535   # rail centreline from track centre: 1435 mm gauge plus half a 72 mm head
BED,SLOPE,EDGE=1.9,1.2,1.65  # ballast half-width, slope band, platform edge from track centre
def merged(parts):
 # linemerge rejects a single LineString; pieces of one track join end to end.
 g=unary_union(parts);return g if g.geom_type=='LineString' else linemerge(g)
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
tracks=[]
for w in root.findall('way'):
 t=tags(w)
 if t.get('railway')!='rail':continue
 pts=[nodes[x.get('ref')] for x in w.findall('nd') if x.get('ref') in nodes]
 if len(pts)<2:continue
 g=LineString(pts).intersection(land.buffer(.5))
 parts=[g] if g.geom_type=='LineString' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='LineString']
 for k,q in enumerate(parts):
  if q.length<1.0:continue
  tracks.append({'id':w.get('id')+('' if len(parts)==1 else f'_{k}'),'osm':w.get('id'),'tags':{kk:t[kk] for kk in ('usage','service','railway:track_ref','electrified','bridge') if kk in t},
   'points':[[round(x,3),round(y,3)] for x,y in q.coords],'length':round(q.length,2)})
lines=unary_union([LineString(t['points']) for t in tracks])
bed=unary_union([LineString(t['points']).buffer(BED,cap_style=2,join_style=1) for t in tracks]).intersection(land)
edge=unary_union([LineString(t['points']).buffer(EDGE,cap_style=2,join_style=1) for t in tracks])
# Platforms: mapped areas that serve trains, brought to a uniform edge 1.65 m from the nearest
# track: trimmed where the tracing sits closer, and track-facing edges traced up to 0.9 m too far
# out (2a sits at about 1.9 m, 2b and 1a at 1.8 m) pulled in to it.
def snap(g):
 quads=[]
 for a_,b_ in zip(list(g.exterior.coords),list(g.exterior.coords)[1:]):
  m=Point((a_[0]+b_[0])/2,(a_[1]+b_[1])/2);near=min(tracks,key=lambda t:LineString(t['points']).distance(m));T=LineString(near['points']);d=T.distance(m)
  if EDGE+.02<d<EDGE+.9 and lines.distance(m)>EDGE+.02:
   ends=[]
   for q in (a_,b_):
    f=T.interpolate(T.project(Point(q)));dq=math.dist(q,(f.x,f.y)) or 1;ends.append((f.x+(q[0]-f.x)*EDGE/dq,f.y+(q[1]-f.y)*EDGE/dq))
   quads.append(Polygon([a_,b_,ends[1],ends[0]]).buffer(0))
 return unary_union([g]+quads).buffer(0)
platforms=[]
for w in root.findall('way'):
 t=tags(w)
 if not(t.get('railway')=='platform' or (t.get('public_transport')=='platform' and t.get('train')=='yes')):continue
 pts=[nodes[x.get('ref')] for x in w.findall('nd') if x.get('ref') in nodes]
 if len(pts)<4:continue
 g=Polygon(pts).buffer(0).intersection(land).difference(edge)
 g=unary_union([snap(q) for q in flat(g)]).intersection(land).difference(edge).buffer(0)
 for q in ([g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']):
  if q.area>5:platforms.append({'id':w.get('id'),'ref':t.get('ref',''),'polygon':[[round(x,3),round(y,3)] for x,y in orient(q).exterior.coords][:-1],'area':round(q.area,1)})
# House platform: the station's own platform between track 1's edge and the building, along
# the building from the canopy's north-west end to the south wing (OSM maps only a 4 m strip).
S24=json.loads((R/'source/station24.json').read_text())
track1=merged([LineString(t['points']) for t in tracks if t['tags'].get('railway:track_ref')=='1' and not t['tags'].get('bridge')])
building=unary_union([Polygon(q) for z in S24['zones'].values() for q in z['polygons']]).buffer(.02)
C,D=S24['range1874']['corners'][2],S24['range1874']['corners'][3]
ux,uy=(D[0]-C[0])/math.dist(C,D),(D[1]-C[1])/math.dist(C,D);nw_end=(C[0]-ux*1.2,C[1]-uy*1.2)
s0=track1.project(Point(nw_end));s1=track1.project(Point(S24['zones']['wing']['polygons'][0][0]))+6.0
seg=LineString([track1.interpolate(s0+(s1-s0)*k/40).coords[0] for k in range(41)])
side=1 if seg.offset_curve(8.0).distance(building)<seg.offset_curve(-8.0).distance(building) else -1
house=Polygon(list(seg.offset_curve(side*EDGE).coords)+list(seg.offset_curve(side*13.8).coords)[::-1]).buffer(0).difference(building).difference(edge)
platforms.append({'id':'house','ref':'1','polygon':[[round(x,3),round(y,3)] for x,y in orient(max(flat(house),key=lambda q:q.area)).exterior.coords][:-1],'area':round(house.area,1)})
# Overlapping mapped platforms (and the house platform over 1b) are made disjoint, so no two
# surfaces share a plane.
taken=Polygon();disjoint=[]
for pl in sorted(platforms,key=lambda q:q['id']=='house'):
 g=Polygon(pl['polygon']).buffer(0).difference(taken)
 for k,q in enumerate([q for q in flat(g) if q.area>3]):
  disjoint.append(dict(pl,id=pl['id']+('' if k==0 else f'_{k}'),polygon=[[round(x,3),round(y,3)] for x,y in orient(q).exterior.coords][:-1],area=round(q.area,1)))
 taken=unary_union([taken,g])
platforms=disjoint
plat_union=unary_union([Polygon(p['polygon']) for p in platforms]).buffer(0)
fw=[r for r in district['roads'] if r['id']=='308440739'][0]['points']
# The parking area next to the siding keeps its surface: the cut stops at its edge.
park=[row for row in json.loads((R/'source/pass18.json').read_text())['surfaces'] if row['id']=='90965001'][0]
park=unary_union([Polygon(q['outer'],q.get('holes',[])).buffer(0) for q in park['polygons']])
cut=bed.buffer(SLOPE,join_style=1).intersection(land).difference(plat_union).difference(park.buffer(.05))
# Pedestrian crossing with full barriers (OSM footway 308440739 and crossing nodes 3137277175-77)
# over track 1, the crossover and track 2. Rubber panels at rail-top level between the outer
# rails; asphalt ramps beyond them climb through the slope band to the surface at the cut edge.
crossing=LineString(fw).buffer(1.3,cap_style=2).intersection(cut)
floor=bed.difference(plat_union).difference(crossing)
# Island surface left as slivers under 12 m between track beds becomes yard gravel at island level
# (not within 3 m of a building).
near_bld=unary_union([Polygon(b['polygons'][0]['outer']).buffer(0) for b in district['buildings']]).buffer(3.0)
yard=cut.buffer(6.0,join_style=2).buffer(-6.0,join_style=2).intersection(land).difference(cut).difference(plat_union.buffer(.02)).difference(near_bld)
yard=unary_union([q for q in flat(yard) if q.area>2.0])
def cdt(g,minarea=1e-4):
 # Constrained Delaunay triangles of a polygonal area, keeping only real (non-sliver) triangles.
 out=[]
 for q in flat(g):
  if q.area<minarea:continue
  for t in constrained_delaunay_triangles(q).geoms:
   if t.area>minarea:out.append([[round(x,4),round(y,4)] for x,y in list(t.exterior.coords)[:-1]])
 return out
def poly_json(p):return {'outer':[[round(x,3),round(y,3)] for x,y in orient(p).exterior.coords][:-1],'holes':[[[round(x,3),round(y,3)] for x,y in h.coords][:-1] for h in orient(p).interiors]}
# Ground meshes the cut overlaps: street chunk layers and pass-18 surfaces.
touched_chunks=[]
for chunk in district['surface_chunks']:
 hit=[key for key,tris in chunk['layers'].items() if any(Polygon(tr).buffer(0).intersects(cut) and Polygon(tr).buffer(0).intersection(cut).area>.01 for tr in tris)]
 if hit:touched_chunks.append({'id':chunk['id'],'layers':hit})
touched18=[]
for row in json.loads((R/'source/pass18.json').read_text())['surfaces']:
 for poly in row['polygons']:
  g=Polygon(poly['outer'],poly.get('holes',[])).buffer(0)
  if g.intersects(cut) and g.intersection(cut).area>.01:touched18.append({'id':row['id'],'kind':row['kind'],'overlap_m2':round(g.intersection(cut).area,1)});break
buildings=[{'id':b['id'],'overlap_m2':round(Polygon(b['polygons'][0]['outer']).buffer(0).intersection(cut).area,2)} for b in district['buildings'] if Polygon(b['polygons'][0]['outer']).buffer(0).intersects(cut) and Polygon(b['polygons'][0]['outer']).buffer(0).intersection(cut).area>.05]
way_at={}
for w in root.findall('way'):
 if tags(w).get('railway')!='rail':continue
 refs=[x.get('ref') for x in w.findall('nd') if x.get('ref') in nodes]
 for i,r in enumerate(refs):
  a_,b_=nodes[refs[max(0,i-1)]],nodes[refs[min(len(refs)-1,i+1)]]
  if a_!=b_:way_at.setdefault(r,round(math.atan2(b_[1]-a_[1],b_[0]-a_[0]),5))
KEEP=('ref','railway:signal:main','railway:switch','railway:signal:direction','railway:signal:position','railway:signal:main:height','railway:switch:electric','crossing:barrier')
feature=lambda kind:[dict({'id':nid,'point':list(nodes[nid]),'tags':{k:v for k,v in t.items() if k in KEEP}},**({'way_dir':way_at[nid]} if nid in way_at else {})) for nid,t in ntags.items() if t.get('railway')==kind and lines.distance(Point(nodes[nid]))<1.0]
# Ground rebuilt around the cut: the island surface and the street chunk under the crossing.
land_tris=[]
for tr in district['land_triangles']:
 g=Polygon(tr).buffer(0)
 land_tris+=cdt(g.difference(cut).difference(yard)) if g.intersects(cut) or g.intersects(yard) else [tr]
chunk=[c for c in district['surface_chunks'] if c['id']=='07_09'][0]
chunk_layers={}
for key,tris in chunk['layers'].items():
 area=unary_union([Polygon(t).buffer(0) for t in tris])
 chunk_layers[key]=cdt(area.difference(cut)) if key=='path' else tris
chunk_edges={k:v for k,v in chunk.get('edges',{}).items()}
if 'path' in chunk_edges:
 pa=unary_union([Polygon(q['outer'],q.get('holes',[])).buffer(0) for q in chunk_edges['path']]).difference(cut)
 chunk_edges['path']=[poly_json(q) for q in flat(pa) if q.area>.01]
# Slope band from the ballast up to the island surface (-0.115 m), heights by distance to the bed.
band=cut.difference(bed).difference(crossing)
path_area=unary_union([Polygon(t).buffer(0) for t in chunk['layers']['path']]).buffer(0)
fx,fy=fw[-1][0]-fw[0][0],fw[-1][1]-fw[0][1];fl=math.hypot(fx,fy);fx,fy=fx/fl,fy/fl
along=lambda x,y:(x-fw[0][0])*fx+(y-fw[0][1])*fy
rail_s=[]
for t in tracks:
 for r in (LineString(t['points']).offset_curve(sg*GAUGE_OFFSET,join_style=1,quad_segs=4) for sg in (1,-1)):
  hit=LineString(fw).intersection(r)
  rail_s+=[along(q.x,q.y) for q in ([hit] if hit.geom_type=='Point' else getattr(hit,'geoms',[])) if q.geom_type=='Point']
cs=[along(x,y) for q in flat(crossing) for x,y in q.exterior.coords];s_lo,s_hi=min(cs),max(cs);s_a,s_b=min(rail_s)-.15,max(rail_s)+.15
def surface_top(s):
 # What the ramp meets beyond the cut edge: a platform, the mapped footway, or the island.
 q=Point(fw[0][0]+fx*s,fw[0][1]+fy*s)
 return PLATFORM_TOP if plat_union.buffer(.05).contains(q) else .015 if path_area.buffer(.05).contains(q) else -.115
top_lo,top_hi=surface_top(s_lo-.4),surface_top(s_hi+.4);CROSS=RAIL_TOP-.005
def cross_z(x,y):
 s=along(x,y)
 if s<s_a:return round(top_lo+(CROSS-top_lo)*max(0.0,s-s_lo)/(s_a-s_lo),4)
 if s>s_b:return round(CROSS+(top_hi-CROSS)*min(1.0,(s-s_b)/(s_hi-s_b)),4)
 return CROSS
def half(s0,s1):
 # Strip of the crossing between two positions along the footway (a rotated box).
 nx_,ny_=-fy,fx;w=20
 return Polygon([(fw[0][0]+fx*s0+nx_*w,fw[0][1]+fy*s0+ny_*w),(fw[0][0]+fx*s1+nx_*w,fw[0][1]+fy*s1+ny_*w),(fw[0][0]+fx*s1-nx_*w,fw[0][1]+fy*s1-ny_*w),(fw[0][0]+fx*s0-nx_*w,fw[0][1]+fy*s0-ny_*w)])
cross_tris={'flat':[[[x,y,cross_z(x,y)] for x,y in t] for t in cdt(crossing.intersection(half(s_a,s_b)))],
 'ramp':[[[x,y,cross_z(x,y)] for x,y in t] for part in (half(s_lo-1,s_a),half(s_b,s_hi+1)) for t in cdt(crossing.intersection(part))]}
cross_walls=[]
for q in flat(crossing):
 ring=list(q.exterior.coords)[:-1]
 for a_,b_ in zip(ring,ring[1:]+ring[:1]):
  mid=Point((a_[0]+b_[0])/2,(a_[1]+b_[1])/2)
  if cut.boundary.distance(mid)<.02 and not bed.buffer(.02).contains(mid):continue
  cross_walls.append([[round(a_[0],4),round(a_[1],4),cross_z(*a_)],[round(b_[0],4),round(b_[1],4),cross_z(*b_)]])
# The trimmed footway surface (+0.015) gets a face down to the island level along the cut edge.
path_walls=[]
for q in flat(path_area.difference(cut)):
 for ring in [list(q.exterior.coords)]+[list(h.coords) for h in q.interiors]:
  for a_,b_ in zip(ring,ring[1:]):
   if cut.buffer(.03).contains(LineString([a_,b_])):path_walls.append([[round(a_[0],4),round(a_[1],4)],[round(b_[0],4),round(b_[1],4)]])
band_tris=[[[x,y,round(BALLAST+(-0.115-BALLAST)*min(1.0,bed.distance(Point(x,y))/SLOPE),4)] for x,y in t] for t in cdt(band)]
# Platform tops as photographed on platforms 2b and 3: from each track-facing edge a 0.25 m edge
# stone, 0.70 m of light warning tiles with studs, 0.60 m of grey slabs and a 0.60 m ribbed
# guidance strip; asphalt beyond. Each platform keeps its long axis for aligned tile courses.
bands=[(k,unary_union([LineString(t['points']).buffer(EDGE+d,cap_style=2,join_style=1) for t in tracks])) for k,d in (('edge',.25),('warning',.95),('slabs',1.55),('tactile',2.15))]
for pl in platforms:
 g=Polygon(pl['polygon']).buffer(0);zones={};inner=Polygon()
 for k,e in bands:zones[k]=cdt(g.intersection(e).difference(inner));inner=unary_union([inner,e])
 zones['surface']=cdt(g.difference(inner));pl['zones']=zones
 r=list(g.minimum_rotated_rectangle.exterior.coords)[:4];e=max([(r[i],r[(i+1)%4]) for i in range(4)],key=lambda q:math.dist(*q))
 pl['axis']=round(math.atan2(e[1][1]-e[0][1],e[1][0]-e[0][0]),5)
# Rails, sleepers and furniture positions, computed here so the Blender builder only extrudes.
SLEEPER=0.60
for t in tracks:
 g=LineString(t['points'])
 t['rails']=[[[round(x,4),round(y,4)] for x,y in g.offset_curve(sgn*GAUGE_OFFSET,join_style=1,quad_segs=4).coords] for sgn in (1,-1)]
 n=int(g.length/SLEEPER);sl=[]
 for k in range(n+1):
  d0=min(g.length,k*SLEEPER);p0=g.interpolate(max(0,d0-.3));p1=g.interpolate(min(g.length,d0+.3));pc=g.interpolate(d0)
  sl.append([round(pc.x,3),round(pc.y,3),round(math.atan2(p1.y-p0.y,p1.x-p0.x),4)])
 t['sleepers']=sl
# Lamps and island furniture follow the centre line of each group of touching platforms: the
# island (2a, 2b and 3 in OSM) carries one row down its middle, as photographed, not one per half.
groups=[]
for pl in platforms:
 g=Polygon(pl['polygon']).buffer(0);hit=[k for k,gr in enumerate(groups) if gr['geom'].distance(g)<.05]
 groups=[gr for k,gr in enumerate(groups) if k not in hit]+[{'geom':unary_union([g]+[groups[k]['geom'] for k in hit]).buffer(0),'refs':[pl['ref']]+[r for k in hit for r in groups[k]['refs']]}]
def centre_points(g,step,margin,avoid):
 # Stations every `step` m along the group's long axis, each moved to the middle of the widest
 # cross-section there, leaving out the part within reach of a building (`avoid`); returns x, y,
 # axis angle and the free width used.
 rect=g.minimum_rotated_rectangle;r=list(rect.exterior.coords)[:4];e=[(r[i],r[(i+1)%4]) for i in range(4)];lg=max(e,key=lambda q:math.dist(*q))
 ang=math.atan2(lg[1][1]-lg[0][1],lg[1][0]-lg[0][0]);ux,uy=math.cos(ang),math.sin(ang);cx,cy=rect.centroid.coords[0];L=math.dist(*lg);pts=[]
 for k in range(int((L-2*margin)/step)+1):
  s0=-L/2+margin+k*step;px,py=cx+ux*s0,cy+uy*s0
  cut_=LineString([(px+uy*40,py-ux*40),(px-uy*40,py+ux*40)]).intersection(g)
  segs=[cut_] if cut_.geom_type=='LineString' else [q for q in getattr(cut_,'geoms',[]) if q.geom_type=='LineString']
  if not segs:continue
  sg=max(segs,key=lambda q:q.length);free=sg.difference(avoid)
  free=[free] if free.geom_type=='LineString' else [q for q in getattr(free,'geoms',[]) if q.geom_type=='LineString']
  if not free:continue
  sg=max(free,key=lambda q:q.length)
  if sg.length>=3.0:m=sg.interpolate(.5,normalized=True);pts.append([round(m.x,3),round(m.y,3),round(ang,4),round(sg.length,2)])
 return pts
# Columns keep 5 m from the station house (clear of its platform canopy and the paths along its
# walls) and 3 m from other buildings.
avoid=unary_union([building.buffer(5.0),unary_union([Polygon(b['polygons'][0]['outer']).buffer(0) for b in district['buildings']]).buffer(3.0)])
platform_groups=[{'refs':sorted(gr['refs']),'lamps':centre_points(gr['geom'],22.0,6.0,avoid),'area':round(gr['geom'].area,1)} for gr in groups]
# Overhead line portals across tracks 1-3 every 45 m through the platform area; masts 3.0 m
# outside the outer tracks, moved further out if they would land in another track's bed.
t2=merged([LineString(t['points']) for t in tracks if t['tags'].get('railway:track_ref')=='2' and not t['tags'].get('bridge')])
t3=merged([LineString(t['points']) for t in tracks if t['tags'].get('railway:track_ref')=='3'])
portals=[];s_cross=track1.project(Point(fw[0]))+8.0;s_end=track1.length-6.0;s_start=s_cross-45.0*int((s_cross-12.0)/45.0)
def meet(line,p,n):
 cut_=LineString([(p.x-n[0]*20,p.y-n[1]*20),(p.x+n[0]*20,p.y+n[1]*20)]).intersection(line)
 pts=[cut_] if cut_.geom_type=='Point' else [q for q in getattr(cut_,'geoms',[]) if q.geom_type=='Point']
 return min(pts,key=lambda q:q.distance(p)) if pts else None
k=0
while s_start+k*45.0<s_end:
 sv=s_start+k*45.0;p=track1.interpolate(sv);q=track1.interpolate(min(track1.length,sv+1.0));d=(q.x-p.x,q.y-p.y);l=math.hypot(*d);n=(-d[1]/l,d[0]/l)
 hits=[h for h in (meet(t2,p,n),meet(t3,p,n)) if h is not None and h.distance(p)<16]
 far=max(hits,key=lambda h:h.distance(p)) if hits else None
 if far is not None:
  sgn=1 if (far.x-p.x)*n[0]+(far.y-p.y)*n[1]>0 else -1
  inner=(p.x-sgn*n[0]*3.0,p.y-sgn*n[1]*3.0);off=3.0
  while off<7 and lines.distance(Point(far.x+sgn*n[0]*off,far.y+sgn*n[1]*off))<2.4:off+=.5
  outer=(far.x+sgn*n[0]*off,far.y+sgn*n[1]*off)
  portals.append({'inner':[round(v,3) for v in inner],'outer':[round(v,3) for v in outer],'wires':[[round(h.x,3),round(h.y,3)] for h in [p]+hits]})
 k+=1
electrified=[t['id'] for t in tracks if t['tags'].get('railway:track_ref') in ('1','2','3') and not t['tags'].get('bridge')]
# Contact wire runs: track 1 over its whole modelled length; tracks 2 and 3 between the first and
# last portal, following their own centrelines.
def run(line,s0,s1):
 s0,s1=max(0.0,min(s0,s1)),min(line.length,max(s0,s1));pts=[line.interpolate(s0)]+[Point(c) for c in line.coords if s0<line.project(Point(c))<s1]+[line.interpolate(s1)]
 return [[round(q.x,3),round(q.y,3)] for q in pts]
wires=[{'track':'1','points':run(track1,0.0,track1.length)}]
for ref,line in (('2',t2),('3',t3)):
 hits=[line.project(Point(w)) for p in portals for w in p['wires'] if line.distance(Point(w))<.05]
 if len(hits)>=2:wires.append({'track':ref,'points':run(line,min(hits),max(hits))})
data={'source':'OpenStreetMap contributors, '+district['source'],'levels':{'rail_top':RAIL_TOP,'platform_top':PLATFORM_TOP,'ballast':BALLAST},
 'dimensions':{'rail_offset':GAUGE_OFFSET,'bed_half_width':BED,'slope_band':SLOPE,'platform_edge':EDGE},
 'tracks':tracks,'platforms':platforms,'platform_groups':platform_groups,'bed':[poly_json(p) for p in flat(floor)],'cut':[poly_json(p) for p in flat(cut)],
 'bed_triangles':cdt(floor),'yard_triangles':cdt(yard),'band_triangles':band_tris,'crossing':[poly_json(p) for p in flat(crossing)],'crossing_triangles':cross_tris,'crossing_walls':cross_walls,'crossing_line':fw,
 'crossing_profile':{'s_lo':round(s_lo,3),'s_a':round(s_a,3),'s_b':round(s_b,3),'s_hi':round(s_hi,3),'top_lo':top_lo,'top_hi':top_hi,'rails_s':sorted(round(v,3) for v in rail_s)},
 'land_triangles':land_tris,'street_07_09':{'layers':chunk_layers,'edges':chunk_edges,'cut_walls':{'path':path_walls}},'portals':portals,'electrified':electrified,'wires':wires,
 'buffer_stops':feature('buffer_stop'),'signals':feature('signal'),'switches':feature('switch'),'crossings':feature('crossing'),
 'touched':{'street_chunks':touched_chunks,'pass18_surfaces':touched18,'buildings':buildings},
 'checks':{'crossing_m2':round(crossing.area,1),'house_platform_m2':round(house.area,1),'land_triangles':len(land_tris),'track_length_m':round(sum(t['length'] for t in tracks),1),'tracks':len(tracks),'platform_m2':round(plat_union.area,1),'yard_m2':round(yard.area,1),'cut_m2':round(cut.area,1),'bed_m2':round(floor.area,1)}}
(R/'source/rail25.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
print(json.dumps(data['checks']));print('touched',json.dumps(data['touched']));print('platforms',[(p['ref'],p['area']) for p in platforms])
print('features',{k:len(data[k]) for k in ('buffer_stops','signals','switches','crossings')});print('crossing',json.dumps(data['crossing_profile']),{k:len(v) for k,v in cross_tris.items()},'walls',len(cross_walls),'path walls',len(path_walls))
print('groups',[(g['refs'],len(g['lamps']),g['area']) for g in platform_groups]);print('portals',len(portals),'wires',[(w['track'],len(w['points'])) for w in wires]);print('RAIL25_PREPARED')
