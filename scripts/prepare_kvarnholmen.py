"""Prepare full district streets and massing from OSM, preserving authored landmarks."""
from pathlib import Path
import xml.etree.ElementTree as E,math,json,collections,sys

from shapely.geometry import Polygon,LineString,Point,box,mapping
from shapely.ops import polygonize,unary_union
from shapely import make_valid,constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1]
lat0,lon0=56.66412,16.3656;a=math.radians(28.2)
def project(lat,lon):
 e=(lon-lon0)*111320*math.cos(math.radians(lat0));n=(lat-lat0)*111320
 return [round(e*math.cos(a)+n*math.sin(a),3),round(-e*math.sin(a)+n*math.cos(a),3)]
def tags(e):return {t.get('k'):t.get('v') for t in e.findall('tag')}
def parse(path):
 r=E.parse(path).getroot();nodes={n.get('id'):project(float(n.get('lat')),float(n.get('lon'))) for n in r.findall('node')}
 ways={w.get('id'):{'id':w.get('id'),'tags':tags(w),'points':[nodes[n.get('ref')] for n in w.findall('nd')]} for w in r.findall('way')}
 return r,nodes,ways
r,nodes,ways=parse(R/'references/osm-kvarnholmen-full.osm');_,_,bw=parse(R/'references/osm-kvarnholmen-boundary.osm')
boundary=unary_union(list(polygonize([LineString(w['points']) for w in bw.values()])))
island=make_valid(Polygon(ways['4222212']['points'])).intersection(boundary)
manifest=json.loads((R/'exports/manifest.json').read_text());existing={a['name'].removeprefix('SM_Building_') for a in manifest['assets'] if a['name'].startswith('SM_Building_')}
# Authored replacements whose mesh labels differ from the OSM footprint ID.
existing.update(['38319501','92412845','91846976','91265009','91265021'])
buildings={}
for wid,w in ways.items():
 if w['tags'].get('building') and len(w['points'])>=4 and w['points'][0]==w['points'][-1]:buildings[wid]={'id':wid,'tags':w['tags'],'geometry':make_valid(Polygon(w['points']))}
for rel in r.findall('relation'):
 t=tags(rel)
 if not t.get('building'):continue
 outer=[ways[m.get('ref')] for m in rel.findall('member') if m.get('role')=='outer' and m.get('ref') in ways];inner=[ways[m.get('ref')] for m in rel.findall('member') if m.get('role')=='inner' and m.get('ref') in ways]
 outerpolys=list(polygonize([LineString(w['points']) for w in outer]));holes=unary_union(list(polygonize([LineString(w['points']) for w in inner])))
 for i,g in enumerate(outerpolys):
  wid=outer[i]['id'] if i<len(outer) else 'r'+rel.get('id')+'_'+str(i);buildings[wid]={'id':wid,'tags':t,'geometry':make_valid(g.difference(holes))}
def polys(g):
 if g.geom_type=='Polygon':return [g] if g.area>.015 else []
 return [p for c in getattr(g,'geoms',[]) for p in polys(c)]
def lines(g):
 if g.geom_type=='LineString':return [g] if g.length>.10 else []
 return [p for c in getattr(g,'geoms',[]) for p in lines(c)]
buildings={wid:b for wid,b in buildings.items() if boundary.covers(b['geometry'].representative_point()) and b['geometry'].area>3}
passages=unary_union([LineString(w['points']).buffer(1.8,cap_style=2,join_style=2) for w in ways.values() if w['tags'].get('highway') and w['tags'].get('tunnel') in ['building_passage','yes']])
obstacles=unary_union([b['geometry'] for b in buildings.values()]).buffer(.05).difference(passages)
# Full surface layers are disjoint: carriageways, footways, sidewalks and curbs.
roads=[];areas=[]
exclude={'platform','steps','construction','proposed','raceway'}
for wid,w in ways.items():
 t=w['tags'];kind=t.get('highway')
 if not kind or kind in exclude:continue
 geom=LineString(w['points'])
 if t.get('area')=='yes' and w['points'][0]==w['points'][-1]:
  g=make_valid(Polygon(w['points'])).intersection(boundary)
  if g.area>1:areas.append((wid,t,g))
  continue
 clipped=geom.intersection(boundary)
 for index,g in enumerate(lines(clipped)):
  if t.get('access')=='private' or t.get('service') in ['driveway','parking_aisle']:continue
  pedestrian=kind in ['pedestrian','living_street'];path=kind in ['footway','path','cycleway','track']
  try:width=float(t.get('width','').replace('m','').strip())
  except ValueError:width=3.0 if path else (7.6 if pedestrian else (6.5 if kind in ['tertiary','secondary','unclassified'] else 5.6))
  width=max(1.6,min(12,width));side=0 if path else (1.4 if pedestrian else 1.55)
  surf=t.get('surface','');material='stone' if pedestrian or surf in ['paving_stones','cobblestone','sett','paved:stone','concrete:plates'] else ('path' if path else 'asphalt')
  roads.append({'id':wid+('p'+str(index) if index else ''),'osm_id':wid,'name':t.get('name',''),'kind':kind,'tags':t,'width':width,'sidewalk_width':side,'material':material,'points':[list(p) for p in g.coords],'length':g.length,'geometry':g})
protected=unary_union([box(-40,-33.65,59,73.65),box(-294,-10.0,-38,5.0),box(-340,-28,-293,26)])
# Extend surface endcaps by 35 cm across the administrative clipping edge.
def surface_line(g):
 pts=list(g.coords)
 for index,neighbor in [(0,1),(-1,-2)]:
  x,y=pts[index];qx,qy=pts[neighbor];length=math.hypot(x-qx,y-qy)
  if length:pts[index]=(x+.35*(x-qx)/length,y+.35*(y-qy)/length)
 return LineString(pts)
# Stone streets have material precedence at junctions; no overlapping coplanar slabs.
stone=unary_union([surface_line(r['geometry']).buffer(r['width']/2,cap_style=2,join_style=2) for r in roads if r['material']=='stone']+[g for wid,t,g in areas])
asphalt=unary_union([surface_line(r['geometry']).buffer(r['width']/2,cap_style=2,join_style=2) for r in roads if r['material']=='asphalt']).difference(stone)
paths=unary_union([surface_line(r['geometry']).buffer(r['width']/2,cap_style=2,join_style=2) for r in roads if r['material']=='path']).difference(unary_union([stone,asphalt]))
carriage=unary_union([stone,asphalt,paths])
full=unary_union([surface_line(r['geometry']).buffer(r['width']/2+r['sidewalk_width'],cap_style=2,join_style=2) for r in roads]+[g for wid,t,g in areas])
sidewalk=full.difference(carriage)
# Remove buildings from road corridors instead of forcing wide streets through facades.
clip=boundary.buffer(.35).difference(obstacles).difference(protected)
layers={k:make_valid(g.intersection(clip)) for k,g in [('stone',stone),('asphalt',asphalt),('path',paths),('sidewalk',sidewalk)]}
# Curbs are narrow sidewalk strips along carriageway boundaries, never across intersections.
curb=sidewalk.intersection(unary_union([stone,asphalt]).boundary.buffer(.11)).intersection(clip)
layers['sidewalk']=layers['sidewalk'].difference(curb);layers['curb']=curb
# Preserve existing plazas and the established street corridor; all other ground follows coastline.
def serialize(g):return [{'outer':[list(v) for v in p.exterior.coords[:-1]],'holes':[[list(v) for v in h.coords[:-1]] for h in p.interiors]} for p in polys(g)]
def triangles(g):
 return [[list(v) for v in t.exterior.coords[:3]] for p in polys(g) for t in constrained_delaunay_triangles(p).geoms if t.area>1e-7]
land=island.union(full.intersection(boundary.buffer(.35))).difference(protected)
# Group streets into 160-metre cells so collision and rendering can be culled locally.
chunks=[];xmin,ymin,xmax,ymax=boundary.bounds
for ix in range(math.floor(xmin/160),math.ceil(xmax/160)):
 for iy in range(math.floor(ymin/160),math.ceil(ymax/160)):
  cell=box(ix*160,iy*160,(ix+1)*160,(iy+1)*160);data={k:triangles(g.intersection(cell)) for k,g in layers.items()}
  if any(data.values()):chunks.append({'id':f'{ix+10:02d}_{iy+10:02d}','layers':data,'edges':{k:serialize(layers[k].intersection(cell)) for k in ['sidewalk','curb']}})
new=[]
for wid,b in buildings.items():
 if wid in existing:continue
 g=b['geometry'];t=b['tags'];category=t.get('building','yes')
 try:levels=float(t.get('building:levels',''))
 except ValueError:levels=1 if category in ['garage','garages','shed','roof'] or g.area<65 else 3 if g.area>450 else 2
 try:height=float(t.get('height','').replace('m','').strip())
 except ValueError:height=levels*3.1+.45
 roof=t.get('roof:shape','');roof='flat' if roof=='flat' or category in ['roof','garage','garages','shed','commercial','industrial'] and g.area>800 else 'hipped'
 if t.get('disused:man_made')=='water_tower':roof='flat'
 new.append({'id':wid,'tags':t,'polygons':serialize(g),'triangles':triangles(g),'bounds':list(g.bounds),'centroid':list(g.centroid.coords)[0],'height':max(2.4,min(90,height)),'levels':levels,'roof':roof,'area':g.area,'base_polygons':serialize(g.difference(passages)),'base_triangles':triangles(g.difference(passages)),'has_passage':g.intersects(passages)})
from shapely import delaunay_triangles
from shapely.geometry import MultiPoint
for b in new:
 if b['roof']=='flat':b['roof_triangles']=[];continue
 g=buildings[b['id']]['geometry'];cloud=[]
 for poly in polys(g):
  for ring in [poly.exterior]+list(poly.interiors):
   n=max(3,math.ceil(ring.length/2.5))
   cloud += [ring.interpolate(i/n,normalized=True).coords[0] for i in range(n)]
  x0,y0,x1,y1=poly.bounds
  for ix in range(math.floor(x0/3),math.ceil(x1/3)+1):
   for iy in range(math.floor(y0/3),math.ceil(y1/3)+1):
    pt=Point(ix*3,iy*3)
    if poly.contains(pt):cloud.append(pt.coords[0])
 roof=[]
 for tri in delaunay_triangles(MultiPoint(cloud)).geoms:
  q=tri.intersection(g)
  for t in triangles(q):
   roof.append([[x,y,min(3.8,Point(x,y).distance(g.boundary)*.63)] for x,y in t])
 b['roof_triangles']=roof
# Dense samples support in-engine ground/capsule tests of every named street.
checks=[]
for road in roads:
 if not road['name'] or road['kind'] in ['path','track','footway','cycleway']:continue
 g=road['geometry'];pts=[]
 for i in range(max(2,math.ceil(g.length/12)+1)):
  p=g.interpolate(i/max(1,math.ceil(g.length/12)),normalized=True)
  if not obstacles.buffer(.55).contains(p):pts.append(list(p.coords)[0])
 if pts:checks.append({'name':road['name'],'id':road['id'],'points':pts})
result={'origin':[lat0,lon0],'rotation_degrees':28.2,'source':'OpenStreetMap contributors, 2026-09-19','boundary':serialize(boundary),'land':serialize(land),'land_triangles':triangles(land),'island_outline':serialize(island),'roads':[{k:v for k,v in r.items() if k!='geometry'} for r in roads],'surface_chunks':chunks,'buildings':new,'preserved_building_ids':sorted(existing),'checks':checks,'stats':{'named_streets':sorted(set(r['name'] for r in roads if r['name'])),'road_segments':len(roads),'road_length_m':round(sum(r['length'] for r in roads),1),'new_buildings':len(new),'preserved_building_footprints':len([b for b in buildings if b in existing]),'surface_area_m2':{k:round(g.area,1) for k,g in layers.items()},'boundary_bounds':list(boundary.bounds)}}
(R/'source/kvarnholmen.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')))
print(json.dumps(result['stats'],indent=2,ensure_ascii=False))
# Diagnostic map generated directly from the geometry, not an edited reference image.
from PIL import Image,ImageDraw
im=Image.new('RGB',(1500,1300),'#172c40');d=ImageDraw.Draw(im);sc=min(1400/(xmax-xmin),1200/(ymax-ymin));xy=lambda p:(50+(p[0]-xmin)*sc,1250-(p[1]-ymin)*sc)
for p in polys(island):d.polygon([xy(v) for v in p.exterior.coords],fill='#d1cbbb')
for k,g in layers.items():
 for p in polys(g):d.polygon([xy(v) for v in p.exterior.coords],fill={'stone':'#a49175','asphalt':'#535b63','path':'#8caa8e','sidewalk':'#e4dfd2','curb':'#e4dfd2'}[k])
for bid,b in buildings.items():
 for p in polys(b['geometry']):
  d.polygon([xy(v) for v in p.exterior.coords],fill='#dc985d' if bid in existing else '#899798',outline='#394b54')
  for hole in p.interiors:d.polygon([xy(v) for v in hole.coords],fill='#d1cbbb')
for road in roads:
 if road['name'] and road['length']>150:
  p=road['geometry'].interpolate(.5,normalized=True);d.text(xy(p.coords[0]),road['name'],fill='#102230')
im.save(R/'previews/kvarnholmen-plan.png')
