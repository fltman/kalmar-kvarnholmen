"""Pass 79: green areas left grey by pass 18 and the east bastion lawns.
Pass 18 made surfaces only from leisure=park/garden and landuse=grass/meadow. This adds the mapped
landuse=village_green and leisure=common areas and the playgrounds (as sand), and the lawns between
the eastern city walls (OSM 91931331, 91931333) and the shore, which OSM leaves untagged but the
April 2025 Street View panorama at Östra Vallgatan shows as lawn with trees and a playground.
Trees: OSM natural=tree points on land plus an estimated planting in the parks and lawns (a
jittered 13 m grid, 3 m clear of paths, walls and buildings), recorded as estimates.
Run with Shapely: KALMAR_GEO=/path/to/site-packages python3 prepare_block79.py
"""
from pathlib import Path
import sys,os,json,math,random,xml.etree.ElementTree as E
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union
from shapely import make_valid,constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/kvarnholmen.json').read_text());A=math.radians(28.2)
def xy(lat,lon):
 e=(lon-16.3656)*111320*math.cos(math.radians(56.66412));n=(lat-56.66412)*111320;return(e*math.cos(A)+n*math.sin(A),-e*math.sin(A)+n*math.cos(A))
def polys(g):return [g] if g.geom_type=='Polygon' and g.area>.1 else [p for c in getattr(g,'geoms',[]) for p in polys(c)]
def geom(rows):return unary_union([Polygon(p['outer'],p['holes']) for p in rows])
def serial(g):return [{'outer':list(p.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in p.interiors]} for p in polys(g)]
def tris(g):return [list(t.exterior.coords)[:3] for p in polys(g) for t in constrained_delaunay_triangles(p).geoms if t.area>1e-7]
root=E.parse(R/'references/osm-kvarnholmen-full.osm').getroot();nodes={n.get('id'):xy(float(n.get('lat')),float(n.get('lon'))) for n in root.findall('node')}
ntags={n.get('id'):{t.get('k'):t.get('v') for t in n.findall('tag')} for n in root.findall('node')}
ways={w.get('id'):{'tags':{t.get('k'):t.get('v') for t in w.findall('tag')},'points':[nodes[n.get('ref')] for n in w.findall('nd')]} for w in root.findall('way')}
land=geom(D['land']);boundary=geom(D['boundary'])
bld=unary_union([make_valid(Polygon(w['points'])) for w in ways.values() if w['tags'].get('building') and len(w['points'])>3 and w['points'][0]==w['points'][-1]])
street=unary_union([Polygon(t) for c in D['surface_chunks'] for tt in c['layers'].values() for t in tt])
protected=unary_union([box(-40,-33.65,59,73.65),box(-294,-10,-38,5),box(-340,-28,-293,26)])
L14=json.loads((R/'source/landmarks14.json').read_text());ramparts=unary_union([Polygon(p['outer'],p['holes']) for p in L14['ramparts']]);wallbands=unary_union([LineString(w['points']).buffer(w['width']/2+.12) for w in L14['walls']])
P18=json.loads((R/'source/pass18.json').read_text());existing=unary_union([geom(s['polygons']) for s in P18['surfaces']])
cut=bld.buffer(.12).union(street.buffer(.025)).union(protected).union(ramparts).union(wallbands).union(existing.buffer(.02))
rows=[]
def add(wid,name,kind,g):
 g=g.intersection(land).intersection(boundary).difference(cut)
 if g.area<2:return
 rows.append({'id':wid,'name':name,'kind':kind,'polygons':serial(g),'triangles':tris(g),'area_m2':round(g.area,1)})
for wid,w in ways.items():
 t=w['tags']
 if len(w['points'])<4 or w['points'][0]!=w['points'][-1]:continue
 kind='lawn' if t.get('landuse')=='village_green' or t.get('leisure')=='common' else 'sand' if t.get('leisure')=='playground' else None
 if kind:add(wid,t.get('name',kind+' '+wid),kind,make_valid(Polygon(w['points'])))
# The east bastion lawns: land east of the two eastern wall lines, between them and the shore.
east=[]
for wid in ('91931331','91931333'):east+=ways[wid]['points']
east=sorted(east,key=lambda p:p[1])
region=Polygon([(p[0]+.5,p[1]) for p in east]+[(520,east[-1][1]),(520,east[0][1])]).buffer(0)
play=unary_union([geom(r['polygons']) for r in rows if r['kind']=='sand']) if any(r['kind']=='sand' for r in rows) else Polygon()
paths=unary_union([LineString(w['points']).buffer(1.2) for w in ways.values() if w['tags'].get('highway') in ('path','footway','track','steps','cycleway') and len(w['points'])>1])
# The panorama at Östra Vallgatan shows lawn on both sides of the low eastern walls: from the street
# to the shore, over the stretch it sees (y -60 to 60).
ov=ways['35813679']['points'];ov=sorted(ov,key=lambda p:p[1])
inner=Polygon([(p[0],p[1]) for p in ov]+[(520,ov[-1][1]),(520,ov[0][1])]).buffer(0).intersection(box(300,-60,520,60))
region=unary_union([region,inner])
add('east-bastions','Carolus and Östra lawns','lawn',region.difference(play).difference(paths))
# Trees: mapped points on land, then an estimated planting in the parks and lawns.
greens=unary_union([geom(s['polygons']) for s in P18['surfaces'] if s['kind']=='green']+[geom(r['polygons']) for r in rows if r['kind']=='lawn'])
clear=paths.union(wallbands.buffer(2.5)).union(bld.buffer(3)).union(street.buffer(1.5))
trees=[]
for nid,t in ntags.items():
 if t.get('natural')=='tree' and land.contains(Point(nodes[nid])) and not bld.contains(Point(nodes[nid])):trees.append({'x':round(nodes[nid][0],2),'y':round(nodes[nid][1],2),'source':'osm '+nid})
rng=random.Random(79)
ok=greens.difference(clear).buffer(-1.5)
x0,y0,x1,y1=greens.bounds;step=13
yy=y0
while yy<y1:
 xx=x0+(rng.random()*step)
 while xx<x1:
  p=Point(xx+rng.uniform(-3,3),yy+rng.uniform(-3,3))
  if ok.contains(p) and all(math.dist((p.x,p.y),(t['x'],t['y']))>8 for t in trees):trees.append({'x':round(p.x,2),'y':round(p.y,2),'source':'estimate'})
  xx+=step
 yy+=step
for t in trees:t['h']=round(rng.uniform(11,17) if t['source']=='estimate' else rng.uniform(9,14),1);t['r']=round(t['h']*rng.uniform(.30,.38),1);t['seed']=rng.randrange(10**6)
# The hedge on the Skeppsbrovallen crest, along the southern wall seen from Skeppsbrogatan.
# Only the outer faces seen from Skeppsbrogatan: the bastion's two flanks and the long southern runs.
sod=[w['points'] for w in L14['walls'] if w['name']=='Sodra']
hedge=[sod[i] for i in (0,1,8,9)]
# The rampart's inner side. Pass 14 built the whole OSM city-wall ring as 4.25 m masonry, but the
# April 2025 panoramas from Södra Vallgatan show the inner side of Skeppsbrovallen as a grass slope
# (about 5 m wide) up to the rampart top, with a row of pollarded limes on the crest and a low
# parapet only on the outer edge. The inner runs are dropped from the wall and replaced by a slope;
# the passage and end walls are kept.
walls_sodra=[list(map(list,r)) for r in sod]
inner_runs={5:(0,7),7:(0,2)}
rmp=unary_union([Polygon(p['outer'],p['holes']) for p in L14['ramparts'] if p['name']=='Sodra']).buffer(0);rmp0=rmp
kept=[]
for i,r in enumerate(walls_sodra):
 if i in inner_runs:
  a,b=inner_runs[i];rest=r[b-1:] if b-1>0 else r
  rest=r[b-1:]
  if len(rest)>=2:kept.append(rest)
 else:kept.append(r)
# The western slope starts 3 m clear of the path that climbs onto the rampart by the passage.
g2=list(walls_sodra[7][0:2]);ls=LineString(g2);st=ls.interpolate(3.0);g2[0]=[st.x,st.y]
glacis=[walls_sodra[5][0:7],g2]
def side79(line):
 # +1 when the rampart lies to the left of the line's direction; the slope goes to the other side.
 (x0,y0),(x1,y1)=line[0],line[1];L=math.hypot(x1-x0,y1-y0);mx,my=(x0+x1)/2,(y0+y1)/2
 return 1 if rmp0.contains(Point(mx-(y1-y0)/L*2.5,my+(x1-x0)/L*2.5)) else -1
limes=[]
for line,step in (([walls_sodra[7][1],walls_sodra[7][0]],5.0),(walls_sodra[5][5:7][::-1],5.0),(walls_sodra[5][0:2][::-1],5.0)):
 ls=LineString(line);n=int(ls.length/step)
 for k in range(n+1):
  p=ls.interpolate(min(ls.length,.5*step+k*step));q=ls.interpolate(min(ls.length,.5*step+k*step+.1))
  dx,dy=q.x-p.x,q.y-p.y;L=math.hypot(dx,dy) or 1;nx,ny=-dy/L,dx/L
  for sgn in (1,-1):
   c=Point(p.x+sgn*nx*1.8,p.y+sgn*ny*1.8)
   if rmp.buffer(.05).contains(c):limes.append({'x':round(c.x,2),'y':round(c.y,2)});break
out={'surfaces':rows,'trees':trees,'hedge':hedge,'sodra_walls':kept,'glacis':[{'points':g,'rampart_side':side79(g)} for g in glacis],'rampart_top':2.9,'limes':limes,'notes':'Village greens, common and playgrounds from OSM; east bastion lawns derived from the walls and the shore; tree planting in parks estimated.'}
(R/'source/block79.json').write_text(json.dumps(out,ensure_ascii=False,indent=1))
rep={'limes':len(limes),'glacis_m':round(sum(LineString(g).length for g in glacis),1),'glacis_sides':[side79(g) for g in glacis],'sodra_runs_kept':len(kept),'surfaces':[(r['id'],r['name'],r['kind'],r['area_m2']) for r in rows],'trees':len(trees),'osm_trees':sum(t['source']!='estimate' for t in trees),'hedge_runs':len(hedge),'hedge_m':round(sum(LineString(h).length for h in hedge),1)}
(R/'previews/block79-zones.json').write_text(json.dumps(dict(status='passed',**rep),indent=2,ensure_ascii=False));print(json.dumps(rep,ensure_ascii=False));print('BLOCK79_ZONES_OK')
