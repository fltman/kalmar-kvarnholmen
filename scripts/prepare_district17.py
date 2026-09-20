"""Whole-house coverage and exposed elevations, without changing protected landmark geometry."""
import sys,json,math,ast,collections
from pathlib import Path

from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'source/kvarnholmen.json').read_text());S=json.loads((R/'source/site.json').read_text());E=json.loads((R/'source/storgatan.json').read_text());M=json.loads((R/'exports/manifest.json').read_text());I=json.loads((R/'previews/district17/inventory.json').read_text())
F=json.loads((R/'source/facades15.json').read_text())['buildings']
footprints={b['id']:b for b in S['buildings']}
footprints.update({b['id']:b for b in E['buildings']});footprints.update({b['id']:b for b in D['buildings']})
polys={bid:unary_union([Polygon(p['outer'],p['holes']) for p in b['polygons']]) if 'polygons' in b else Polygon(b['polygon'],b.get('holes',[])) for bid,b in footprints.items()}
roadpairs=[(q.get('name') or q.get('tags',{}).get('name'),LineString(q['points'])) for q in D['roads'] if len(q['points'])>1]
roadpairs=[(n,p) for n,p in roadpairs if n];roads=unary_union([p for n,p in roadpairs])
town={'92412866','92412857','92412842','92412870','91926317','91846964','91970270','91970255','91970305','91970276'}
pass16=set(json.loads((R/'previews/street16-build.json').read_text())['changed'])
profiles={}
for n in ast.parse((R/'scripts/build_storgatan.py').read_text()).body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='profiles' for t in n.targets):profiles=ast.literal_eval(n.value)
oldcol={'M_Pale_Yellow':'Yellow','M_Warm_Limewash':'Ivory','M_OffWhite':'Ivory','M_Dusty_Rose':'Rose','M_Red_Plaster':'Rose','M_Grey_Plaster':'Lime'}
out={}
for s in M['assets']:
 name=s['name']
 if not name.startswith(('SM_Building_','SM_Kvarnholmen_House_')):continue
 bid=name.split('_')[-1];b=footprints[bid];shape=polys[bid];iv=I[name]
 protected=bid in town or name in pass16 or s['category'] in ['Storgatan/Landmarks','Kvarnholmen/Sodra Langgatan facades','Kvarnholmen/Landmarks']
 if bid in F:H=b['height'];floors=max(1,round(b['levels']));kind=F[bid]['style'];colour=next((ma.removeprefix('M_Town_') for ma,ar in iv['materials'] if ma in ['M_Town_Ivory','M_Town_Yellow','M_Town_Rose','M_Town_Lime']),'Ivory');paint='PaintWhite';roof=b['roof']
 elif bid in profiles:H,floors,colour,paint,roof,bays,kind=profiles[bid]
 else:
  H=next((z for z,a in iv['height_modes'] if z>3),7.1);floors=max(1,round(H/3.5));kind='traditional';colour=next((oldcol[ma] for ma,ar in iv['materials'] if ma in oldcol),'Ivory');paint='PaintWhite';roof='preserved'
 nearest=min(roadpairs,key=lambda r:shape.distance(r[1]))[0]
 service=b['tags'].get('building') in ['garage','garages','shed','roof'] or shape.area<45
 if service:kind='service'
 walls=[];neighbours=unary_union([p.buffer(.22) for bb,p in polys.items() if bb!=bid and p.distance(shape)<.35])
 tiers=[(b['base_polygons'],-.1,min(3.4,H)),(b['polygons'],3.4,H)] if b.get('has_passage') else [(b.get('polygons',[{'outer':b.get('polygon'),'holes':b.get('holes',[])}]),-.1,H)]
 for tier,(ps,z0,z1) in enumerate(tiers):
  if z1<=z0:continue
  for po in ps:
   pg=orient(Polygon(po['outer'],po['holes']),sign=1)
   for ri,ring in enumerate([pg.exterior]+list(pg.interiors)):
    coords=list(ring.coords)
    for p,q in zip(coords,coords[1:]):
     ln=LineString([p,q]);L=ln.length
     if L<.08:continue
     diff=ln.difference(neighbours);parts=[diff] if diff.geom_type=='LineString' else list(getattr(diff,'geoms',[]));intervals=[]
     for seg in parts:
      if seg.geom_type!='LineString' or seg.length<1.35:continue
      a,c=sorted([ln.project(Point(seg.coords[0])),ln.project(Point(seg.coords[-1]))]);intervals.append([a,c])
     mid=ln.interpolate(.5,normalized=True);a=math.atan2(q[1]-p[1],q[0]-p[0]);probe=Point(mid.x+math.sin(a)*2,mid.y-math.cos(a)*2)
     street,rd=min(roadpairs,key=lambda r:probe.distance(r[1]));distance=probe.distance(rd)
     facing=ri==0 and distance<13 and not shape.contains(rd.interpolate(rd.project(probe)))
     walls.append(dict(p=p,q=q,length=L,z0=z0,z1=z1,exposed=intervals,road_distance=distance,street=street,frontage=facing,tier=tier,courtyard=ri>0))
 possible=[i for i,w in enumerate(walls) if w['z0']<0 and any(v-u>2.1 for u,v in w['exposed'])]
 door=min(possible,key=lambda i:walls[i]['road_distance']) if possible else None
 out[name]=dict(id=bid,category=s['category'],action='retain_authored' if protected else 'rebuild',street=nearest,H=H,levels=floors,style=kind,colour=colour,paint=paint,roof=roof,area=shape.area,walls=walls,entrance_wall=door,has_passage=b.get('has_passage',False),reference_status='previous authored facade; see earlier pass documentation' if protected else 'mapped footprint; facade proportions and concealed detail estimated; prior palette retained',centroid=list(shape.centroid.coords)[0])
# Match reference geolocations to footprints. Coordinates are approximate; recorded distances aid review.
refs=json.loads((R/'references/district17/sources.json').read_text())
a=math.radians(28.2)
for slug,ref in refs.items():
 lat,lon=map(float,ref['maps'][0].split('=')[-1].split(','));e=(lon-16.3656)*111320*math.cos(math.radians(56.66412));n=(lat-56.66412)*111320;p=Point(e*math.cos(a)+n*math.sin(a),-e*math.sin(a)+n*math.cos(a))
 near=sorted([(polys[q['id']].distance(p),name) for name,q in out.items()])[:3]
 print('REFERENCE',slug,[(round(d,2),nm) for d,nm in near])
(R/'source/district17.json').write_text(json.dumps({'buildings':out,'counts':dict(collections.Counter(v['action'] for v in out.values()))},ensure_ascii=False,indent=2))
print('COVERAGE',len(out),collections.Counter(v['action'] for v in out.values()))

# Deterministic roof recipes used by full rebuilds.
import subprocess
for script in ['prepare_district17_rectangles.py','prepare_district17_roofs.py','prepare_district17_seams.py','prepare_klapphuset17.py']:
 subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
