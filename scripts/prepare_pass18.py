"""Mapped land use and explicitly referenced landmark corrections, no invented legal parking rules."""
from pathlib import Path
import sys,json,math,xml.etree.ElementTree as E,subprocess

from shapely.geometry import Polygon,LineString,box
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
ways={w.get('id'):{'tags':{t.get('k'):t.get('v') for t in w.findall('tag')},'points':[nodes[n.get('ref')] for n in w.findall('nd')]} for w in root.findall('way')}
land=geom(D['land']);boundary=geom(D['boundary']);obstacles=unary_union([make_valid(Polygon(w['points'])) for w in ways.values() if w['tags'].get('building') and len(w['points'])>3 and w['points'][0]==w['points'][-1]])
street=unary_union([Polygon(t) for c in D['surface_chunks'] for tt in c['layers'].values() for t in tt])
protected=unary_union([box(-40,-33.65,59,73.65),box(-294,-10,-38,5),box(-340,-28,-293,26)])
L14=json.loads((R/'source/landmarks14.json').read_text());ramparts=unary_union([Polygon(p['outer'],p['holes']) for p in L14['ramparts']]);wallbands=unary_union([LineString(w['points']).buffer(w['width']/2+.12) for w in L14['walls']])
cut=obstacles.buffer(.12).union(street.buffer(.025)).union(protected).union(ramparts).union(wallbands)
rows=[]
for wid,w in ways.items():
 t=w['tags'];kind='parking' if t.get('amenity')=='parking' and t.get('parking')!='underground' else 'green' if t.get('landuse') in ['grass','meadow','recreation_ground'] or t.get('leisure') in ['park','garden'] or t.get('natural') in ['grassland','scrub'] else None
 if not kind or len(w['points'])<4 or w['points'][0]!=w['points'][-1]:continue
 g=make_valid(Polygon(w['points'])).intersection(land).intersection(boundary).difference(cut)
 if g.area<2:continue
 rows.append({'id':wid,'name':t.get('name',kind+' '+wid),'kind':kind,'tags':t,'polygons':serial(g),'triangles':tris(g),'area_m2':g.area})
# Park takes precedence only where the map contains a genuine park polygon.
parks=unary_union([geom(r['polygons']) for r in rows if r['kind']=='green'])
for row in rows:
 if row['kind']=='parking':
  g=geom(row['polygons']).difference(parks);row.update(polygons=serial(g),triangles=tris(g),area_m2=g.area)
# Parking bays are schematic 2.5 x 5 m cells with six-metre drive aisles, clipped to actual lot.
for row in rows:
 row['bays']=[]
 if row['kind']!='parking':continue
 for p in polys(geom(row['polygons'])):
  rect=list(p.minimum_rotated_rectangle.exterior.coords);a,b=max(zip(rect,rect[1:]),key=lambda pq:math.dist(*pq));ang=math.atan2(b[1]-a[1],b[0]-a[0]);co,si=math.cos(ang),math.sin(ang)
  local=[(x*co+y*si,-x*si+y*co) for x,y in p.exterior.coords];x0=min(v[0] for v in local);x1=max(v[0] for v in local);y0=min(v[1] for v in local);y1=max(v[1] for v in local)
  conv=lambda u,v:(u*co-v*si,u*si+v*co)
  # Small/irregular street bays omitted rather than painted across entrances.
  for j in range(max(1,int((y1-y0)/16)+1)):
   for yy,sgn in [(y0+.4+j*16,1),(y0+11.4+j*16,-1)]:
    for i in range(int((x1-x0-.8)/2.5)):
     xx=x0+.4+i*2.5;corners=[conv(xx,yy),conv(xx+2.5,yy),conv(xx+2.5,yy+5),conv(xx,yy+5)]
     if p.buffer(-.10).covers(Polygon(corners)):row['bays'].append({'corners':corners,'open_side':0 if sgn<0 else 2})
ids=['91285823','91285828','91285833','91846944','91846928'];out={'buildings':{bid:next(b for b in D['buildings'] if b['id']==bid) for bid in ids},'surfaces':rows,'gates':L14['gates'],'notes':'Reference dimensions estimated; surfaces from OSM, bay layouts inferred; no fees or current regulations asserted.'}
(R/'source/pass18.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
names=['SM_Kvarnholmen_House_'+bid for bid in ids]+['SM_Kvarnholmen_Port_'+g['name'] for g in L14['gates']]+['SM_Kvarnholmen_Vall_'+s for s in ['Sodra','Regeringen','CarolusPhilippus']]
back=R/'source/backups/detail-pass-17';back.mkdir(parents=True,exist_ok=True)
paths=['source/Stortorget.blend','exports/manifest.json','Unreal/Content/Kalmar/Maps/Stortorget.umap']+['exports/meshes/'+n+'.fbx' for n in names]+['Unreal/Content/Kalmar/Meshes/'+n+'.uasset' for n in names]
for f in paths:
 src=R/f;dst=back/f
 if src.exists() and not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);subprocess.run(['cp','-c',str(src),str(dst)],check=True)
print(json.dumps({'surfaces':len(rows),'greens':sum(r['kind']=='green' for r in rows),'parking':sum(r['kind']=='parking' for r in rows),'parking_bays':sum(len(r['bays']) for r in rows),'green_m2':round(sum(r['area_m2'] for r in rows if r['kind']=='green'))}))
