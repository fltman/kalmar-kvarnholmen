"""Pass 122: twenty-six generic pass-17 volumes inside the blocks (courtyard houses, outbuildings, back
ranges) in the east half of Kvarnholmen, and Klapphuset, the small boarded house on piles off Bastion
Carolus Philippus. None of them is measured: the roof form, ridge direction and roof colour are read
from top-down Google satellite views (view only), registered on the OSM outlines; heights come from
the district volume's storeys (sheds capped at one storey). Klapphuset keeps the pass-17 eaves and
roof (photo-based) and gets piles, a pier and an east deck placed from the satellite view.
See references/block122-notes.md.
Zones: each house is one zone, or a main range plus wings or annexes where the outline is an L or has
bays. Walls carry kind 'outer' (free), 'upper' (above a lower neighbour) or 'fill' (where a house is
now lower than the pass-17 volume it replaces and a neighbour stands taller: the band from the new
eaves up to the old height, which the neighbour's own walls may leave open). The ridge height is
computed from the zone's boxed width and a pitch, unless the spec gives 'top'.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def key(osm):return next(k for k in d17 if k.endswith('_'+osm))
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda osm:Polygon([tuple(w['p']) for w in d17[key(osm)]['walls']]).buffer(0)
def band(a,b,depth,s0=-60,s1=60,t0=-.5):
 # The strip behind the line a-b (inwards = left of a->b), as in pass 82.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,t0),(s1,t0),(s1,depth),(s0,depth))])
def seedgeom(seed):
 # ('cut', a, b): everything left of the line a->b, up to 60 m from it.
 return band(seed[1],seed[2],60,s0=-1000,s1=1000,t0=0)
# local cuts: x>v, x<v, y>v, y<v
def XGT(v):return ('cut',(v,300.0),(v,-300.0))
def XLT(v):return ('cut',(v,-300.0),(v,300.0))
def YGT(v):return ('cut',(-300.0,v),(600.0,v))
def YLT(v):return ('cut',(600.0,v),(-300.0,v))

# Per house: zones as (name, seed, spec). seed None = the whole outline, 'rest' = what is left.
# spec: height (eaves, m above the ground), pitch (deg; the ridge follows from the boxed width) or top;
# roof saddle | hip | mono | flat; ridge 'long' or 'short'; wall/roof material keys (build_block122.py);
# boards; storeys; door: the local direction of the yard side that gets the door (or door_at: a point
# on the wall); kind: range (house or back range), shed, annex (flat link or bay), klapp (Klapphuset).
# Roofs and colours read from the satellite views sat_e1..e7 (pass 122 captures); see the notes.
H17={v['id']:v['H'] for v in d17.values()}
T38,T22=38,22
HOUSES={
 # Block Proviantgatan / Storgatan / Norra Långgatan, west part (sat_e1)
 '91926312':[('pa',None,dict(height=2.9,pitch=30,roof='saddle',ridge='long',wall='Yellow',rm='TileTan',boards=True,storeys=1,door=(0,1),kind='shed'))],
 '93192396':[('pb',None,dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Ochre',rm='Tile',boards=False,storeys=2,door=(0,1),kind='range'))],
 '93192383':[('pc',None,dict(height=3.55,top=3.75,roof='flat',wall='PaleGrey',rm='RoofPale',boards=False,storeys=1,door=(0,-1),kind='annex'))],
 '93192368':[('pd',None,dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='PaleYellow',rm='Tile',boards=False,storeys=2,door=(0,-1),kind='range'))],
 '93192379':[('pe',None,dict(height=6.65,pitch=T22,roof='saddle',ridge='long',wall='GreyBeige',rm='RoofDark',boards=False,storeys=2,door=(0,1),kind='range'))],
 # Same block, east part (sat_e1, sat_e3)
 '93192407':[('qw',YLT(24.3),dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=False,storeys=2,door=(-1,0),kind='range')),
   ('qm','rest',dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=False,storeys=2,door=(0,-1),kind='range',skylights=1))],
 '93192355':[('qa',None,dict(height=3.55,pitch=T38,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=True,storeys=1,door=(-1,0),kind='range'))],
 '93192451':[('qb',None,dict(height=3.55,pitch=T38,roof='saddle',ridge='long',wall='Falu',rm='Tile',boards=True,storeys=1,door=(-1,0),kind='range'))],
 '93192363':[('qc',None,dict(height=3.55,pitch=32,roof='saddle',ridge='long',wall='Ochre',rm='TileTan',boards=True,storeys=1,door=(1,0),kind='range'))],
 '93192371':[('qd',None,dict(height=3.55,pitch=32,roof='saddle',ridge='long',wall='Yellow',rm='TileTan',boards=True,storeys=1,door=(0,-1),kind='range'))],
 '93192450':[('qe',None,dict(height=6.65,pitch=32,roof='saddle',ridge='long',wall='PaleYellow',rm='TileTan',boards=False,storeys=2,door=(0,1),kind='range',skylights=1))],
 # Fiskaregatan / Landshövdingegatan, north of Norra Långgatan (sat_e3, sat_e4; partly under the search box)
 '90859854':[('fa',None,dict(height=3.55,pitch=T38,roof='saddle',ridge='long',wall='Falu',rm='TileBrown',boards=True,storeys=1,door=(0,-1),kind='range'))],
 '90859839':[('fb',None,dict(height=6.65,pitch=T22,roof='saddle',ridge='long',wall='Rose',rm='RoofGrey',boards=False,storeys=2,door=(-1,0),kind='range'))],
 # Block Storgatan / Proviantgatan / Södra Långgatan / Landshövdingegatan (sat_e1, sat_e2)
 '91928592':[('sa',None,dict(height=3.0,pitch=T22,roof='saddle',ridge='long',wall='Falu',rm='RoofDark',boards=True,storeys=1,door=(0,1),kind='shed'))],
 '91928555':[('sb',None,dict(height=6.65,pitch=T38,roof='hip',ridge='long',wall='Ivory',rm='TileBrown',boards=False,storeys=2,door=(1,0),kind='range'))],
 '91928547':[('sc',None,dict(height=6.65,pitch=30,roof='hip',ridge='long',wall='Yellow',rm='RoofBrown',boards=False,storeys=2,door=(0,-1),kind='range',chimneys=1))],
 '91928595':[('sd',None,dict(height=6.65,top=6.85,roof='flat',wall='Ivory',rm='RoofPale',boards=False,storeys=2,door=(-1,0),kind='range'))],
 '91928593':[('se',None,dict(height=6.65,pitch=30,roof='saddle',ridge='long',wall='Ochre',rm='TileTan',boards=False,storeys=2,door=(-1,0),kind='range'))],
 # Block Norra Långgatan / Landshövdingegatan / Storgatan / Östra Vallgatan (sat_e4)
 '93238177':[('ka',YGT(36.35),dict(height=3.2,top=3.4,roof='flat',wall='Yellow',rm='RoofDark',boards=False,storeys=1,door=None,kind='annex')),
   ('kc','rest',dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Yellow',rm='TileTan',boards=False,storeys=2,door=(0,-1),kind='range'))],
 '93238180':[('kd',XGT(336.35),dict(height=3.0,top=3.2,roof='flat',wall='Falu',rm='RoofDark',boards=True,storeys=1,door=(1,0),kind='shed')),
   ('ke','rest',dict(height=2.7,top=2.9,roof='flat',wall='Falu',rm='RoofDark',boards=True,storeys=1,door=None,kind='shed'))],
 '93238174':[('kf',XLT(344.25),dict(height=3.2,top=3.4,roof='flat',wall='Rose',rm='RoofDark',boards=False,storeys=1,door=None,kind='annex')),
   ('kg',YGT(47.45),dict(height=6.65,top=6.85,roof='flat',wall='Rose',rm='RoofGrey',boards=False,storeys=2,door=None,kind='range')),
   ('kh',YLT(33.3),dict(height=6.65,top=6.85,roof='flat',wall='Rose',rm='RoofGrey',boards=False,storeys=2,door=None,kind='range')),
   ('ki','rest',dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Rose',rm='Tile',boards=False,storeys=2,door=(-1,0),kind='range'))],
 '93238167':[('kj',None,dict(height=3.0,pitch=T22,roof='saddle',ridge='long',wall='Falu',rm='RoofDark',boards=True,storeys=1,door=(-1,0),kind='shed'))],
 '93238219':[('kk',None,dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='PaleYellow',rm='TileBrown',boards=False,storeys=2,door=(-1,0),kind='range',chimneys=2))],
 '93238152':[('kl',XGT(372.9),dict(height=6.65,pitch=T22,roof='saddle',ridge='long',wall='GreyBeige',rm='RoofGrey',boards=False,storeys=2,door=(-1,0),kind='range')),
   ('km',YLT(28.3),dict(height=6.65,pitch=T38,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=False,storeys=2,door=(-1,0),kind='range')),
   ('kn','rest',dict(height=3.4,top=3.6,roof='flat',wall='GreyBeige',rm='RoofGrey',boards=False,storeys=1,door=(0,1),kind='annex'))],
 # Block Storgatan / Södra Långgatan / Landshövdingegatan / Östra Vallgatan (sat_e7)
 '93199612':[('ta',None,dict(height=6.65,pitch=32,roof='hip',ridge='long',wall='Yellow',rm='Tile',boards=False,storeys=2,door=(0,1),kind='range',chimneys=2))],
 # Klapphuset on piles off Bastion Carolus Philippus (sat_e6). Eaves and the low hip with two
 # ventilators as in the photo-based pass-17 build; the pier and the east deck from the satellite view.
 '93199604':[('wa',None,dict(height=2.95,top=4.2,roof='hip',ridge='long',wall='Falu',rm='RoofGrey',boards='lap',storeys=1,door_at=(436.4,122.3),kind='klapp',
   pier=[[436.4,122.3],[426.8,104.3]],deck='east'))],
}
zones={};taken={}
for osm,zl in HOUSES.items():
 P=PG(osm);tk=Polygon()
 for name,seed,spec in zl:
  g=P if seed in (None,'rest') else P.intersection(seedgeom(seed))
  ps=parts(g.difference(tk));tk=unary_union([tk]+ps)
  zones[name]=dict(spec,osm=osm,mesh=key(osm),old_height=H17[osm],ps=ps)
 taken[osm]=tk
mine=set(HOUSES)
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in mine and len(v['walls'])>=3]
def neighbour_at(pt,me):
 for name,z in zones.items():
  if name!=me and any(p.buffer(.001).contains(pt) for p in z['ps']):return name,z['height'],True
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h,False
 return None,0.0,False
def rect_of(ps,spec):
 # The zone boxed in its minimum rotated rectangle, counter-clockwise, rotated so that r[0]->r[1]
 # is the ridge (long or short side) or, for a mono-pitch roof, the low eaves (outward = 'low').
 r=list(orient(unary_union(ps).minimum_rotated_rectangle).exterior.coords)[:4]
 sides=[math.dist(r[i],r[(i+1)%4]) for i in range(4)]
 if spec['roof']=='mono':
  lx,ly=spec['low']
  def score(i):
   p,q=r[i],r[(i+1)%4];L=math.dist(p,q);return ((q[1]-p[1])/L)*lx-((q[0]-p[0])/L)*ly
  k=max(range(4),key=score)
 else:
  k=max(range(4),key=lambda i:sides[i]) if spec.get('ridge','long')=='long' else min(range(4),key=lambda i:sides[i])
 return [list(map(lambda c:round(c,3),r[(k+j)%4])) for j in range(4)]
out={};report={}
for name,z in zones.items():
 H=z['height'];walls=[]
 for poly in z['ps']:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h,own=neighbour_at(Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3),name)
    if runs and runs[-1][0]==nb:runs[-1][4]=(k+1)/n
    else:runs.append([nb,h,own,k/n,(k+1)/n])
   for nb,h,own,t0,t1 in runs:
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    if nb is None:walls.append({'p':list(a),'q':list(b),'z0':-0.1,'z1':H,'kind':'outer','neighbour':None});continue
    if h<H-.05:walls.append({'p':list(a),'q':list(b),'z0':h,'z1':H,'kind':'upper','neighbour':nb})
    if not own and h>H+.05 and z['old_height']>H+.05:
     walls.append({'p':list(a),'q':list(b),'z0':H,'z1':round(min(h,z['old_height']),3),'kind':'fill','neighbour':nb})
 spec={k:v for k,v in z.items() if k!='ps'}
 rect=rect_of(z['ps'],z)
 if 'top' not in spec:
  # ridge from the pitch over half the boxed width (hip and saddle); mono over the full width
  W=math.dist(rect[1],rect[2]);spec['top']=round(H+math.tan(math.radians(spec['pitch']))*(W if spec['roof']=='mono' else W/2),2)
 out[name]=dict(spec,polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in z['ps']],rect=rect,walls=walls)
 report[name]={'osm':z['osm'],'area_m2':round(sum(p.area for p in z['ps']),1),'polygons':len(z['ps']),'walls':len(walls),'eaves':H,'top':spec['top'],
  'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'fill_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='fill'),1)}
foot=unary_union([PG(o) for o in HOUSES]);covered=unary_union([p for z in zones.values() for p in z['ps']])
data={'source':'district volumes '+', '.join(HOUSES)+' (source/district17.json), '+district['source'],'ids':list(HOUSES),'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for z in zones.values() for p in z['ps'])-covered.area,3)}}
(R/'source/block122.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(len(z['ps'])>=1 for z in zones.values())
(R/'previews/block122-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK122_ZONES_OK' if ok else 'BLOCK122_ZONES_REVIEW')
