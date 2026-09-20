"""Mapped landmark footprints and surviving fortifications; heights remain estimates."""
from pathlib import Path
import json,math,sys,xml.etree.ElementTree as ET

from shapely.geometry import Polygon,LineString,box
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/kvarnholmen.json').read_text());out={'buildings':{},'walls':[],'ramparts':[]}
ids=['92204204','92204192','92204165','91846928','91846968','91285823','91285828','91285833']
for b in D['buildings']:
 if b['id'] in ids:out['buildings'][b['id']]={'polygon':b['polygons'][0]['outer'],'bounds':b['bounds']}
r=ET.parse(R/'references/osm-kvarnholmen-full.osm').getroot();ns={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.findall('node')};a=math.radians(28.2)
def xy(p):
 lat,lon=p;e=(lon-16.3656)*111320*math.cos(math.radians(56.66412));n=(lat-56.66412)*111320;return [round(e*math.cos(a)+n*math.sin(a),3),round(-e*math.sin(a)+n*math.cos(a),3)]
W={w.get('id'):[xy(ns[n.get('ref')]) for n in w.findall('nd')] for w in r.findall('way') if any(t.get('k')=='barrier' and t.get('v')=='city_wall' for t in w.findall('tag'))}
# Each listed chain is surviving masonry, not a complete historical ring.
# Paths through the gates and extant stair/ramp approaches remain clear.
roads=unary_union([LineString(r['points']).buffer(max(.9,r['width']/2)+.8,cap_style=1) for r in D['roads'] if r['kind'] not in ['steps']])
def wall(name,points,height,width=1.25,clip=True):
 line=LineString(points);g=line.difference(roads) if clip else line
 parts=[g] if g.geom_type=='LineString' else list(getattr(g,'geoms',[]))
 for i,p in enumerate(parts):
  if p.geom_type=='LineString' and p.length>.3:out['walls'].append({'name':name,'points':list(p.coords),'height':height,'width':width})
# South closed OSM line describes outer and inner rampart faces, not two independent high walls.
p=W['91066703'];out['south_outline']=p
wall('Sodra',p,4.25,1.4)
# Eastern curtains are low reconstructed remains; Regeringen is the tall southern bastion.
p=W['91931331'];wall('Regeringen',p[:7],3.8,1.65);wall('Ostra',p[6:],1.25,1.05)
p=W['91931333'];wall('Ostra',p[:3],1.25,1.05);wall('CarolusPhilippus',p[2:],2.35,1.35)
wall('Vaster',W['91931338'],4.0,1.7)
wall('Muren',W['698954012'],2.55,1.2);wall('Lustgarden',W['698954011'],.20,1.4)
# Gate clearances at the actual road intersections, expressed in scene metres.
out['gates']=[{'name':'Vasterport','x':-348.3,'y':92.3,'a':.988,'w':4.6,'spring':2.5,'rise':2.3,'depth':12.0,'height':9.5,'width':8.8}, {'name':'Jordbroporten','x':-187.7,'y':-194.5,'a':0,'w':6.0,'spring':2.4,'rise':1.4,'depth':9.0,'height':4.8,'width':15.2}, {'name':'Kavaljersporten','x':51.3,'y':-165.8,'a':0,'w':6.6,'spring':2.6,'rise':2.0,'depth':12.4,'height':5.6,'width':17.5}]
# Earthwork interiors end before existing mapped walkways. Tops taper to ground at their back edge in the model.
for name,poly,z in [('Sodra',Polygon(W['91066703']),2.9),('Regeringen',Polygon(W['91931331'][:7]),2.8),('CarolusPhilippus',Polygon([W['91931333'][i] for i in [2,3,4,5]]),1.55)]:
 g=poly.buffer(-1.0).difference(roads)
 if name=='Regeringen':g=g.intersection(box(415,-130,460,10))
 parts=[g] if g.geom_type=='Polygon' else list(getattr(g,'geoms',[]))
 for part in parts:
  if part.geom_type=='Polygon' and part.area>1:out['ramparts'].append({'name':name,'height':z,'outer':list(part.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in part.interiors],'triangles':[[list(p) for p in list(t.exterior.coords)[:3]] for t in constrained_delaunay_triangles(part).geoms]})
# Store audit metadata; clipping is a gameplay accommodation, not an archival feature.
out['notes']={'footprints':'OpenStreetMap','fortifications':'KLM Bevarande- och utvecklingsplan 2020 pp 23,75,101,107','height_policy':'Photo/report-informed estimates. District terrain still simplified; road clearances preserved.'}
(R/'source/landmarks14.json').write_text(json.dumps(out,indent=2));print(len(out['walls']),'wall chains',len(out['ramparts']),'earthwork pieces')
