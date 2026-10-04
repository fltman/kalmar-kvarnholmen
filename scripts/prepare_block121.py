"""Pass 121: sixteen generic pass-17 volumes inside the blocks (courtyard houses, outbuildings, back
ranges) in the west half of Kvarnholmen, and the sheds and pavilions by the railway station. None of
them is measured: the roof form, ridge direction and roof colour are read from top-down Google
satellite views (view only), registered on the OSM outlines; heights come from the district volume's
storeys (capped at one storey for sheds) and, for two houses on Ölandsgatan, from one Street View
panorama. See references/block121-notes.md.
Zones: each house is one zone, or a main range plus a wing where the outline is an L. Walls carry kind
'outer' (free), 'upper' (above a lower neighbour) or 'fill' (where a house is now lower than the
pass-17 volume it replaces and a neighbour stands taller: the band from the new eaves up to the old
height, which the neighbour's own walls may leave open).
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
 # The strip behind the front a-b (inwards = left of a->b), as in pass 82.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,t0),(s1,t0),(s1,depth),(s0,depth))])
def seedgeom(seed):
 # ('band', a, b, depth): the strip behind the front a-b; ('cut', a, b): everything left of the line a->b.
 return band(*seed[1:]) if seed[0]=='band' else band(seed[1],seed[2],60,t0=0)

# Per house: zones as (name, seed, spec). seed None = the rest of the outline.
# spec: height (eaves) and top (ridge) in m above the ground; roof saddle | hip | mono | flat;
# ridge 'long' or 'short' (along the boxed outline's long or short side); for mono, 'low' is the
# local direction the roof falls to; wall/roof material keys (build_block121.py); boards; storeys;
# door: the local direction of the yard side that gets the door; end_wall: (material, direction) for
# an end wall and its gable in another colour (the red boarded east gable of 91846989 in the panorama).
# Roofs and colours read from the satellite views sat_a1..a5 (pass 121 captures); see the notes.
H17={v['id']:v['H'] for v in d17.values()}
HOUSES={
 # Station and railway area, Ölandskajen / Stationsgatan (sat_a1)
 # the south-east 10.5 m of the goods shed has a paler roof on the satellite view
 '90965018':[('ge',('band',(-403.51,-228.83),(-397.48,-225.38),10.5),dict(height=4.6,top=6.3,roof='saddle',ridge='long',wall='Falu',rm='RoofPale',boards=True,storeys=1,door=(1,1),kind='goods')),
   ('gs','rest',dict(height=4.6,top=6.3,roof='saddle',ridge='long',wall='Falu',rm='RoofBrown',boards=True,storeys=1,door=(1,1),kind='goods'))],
 '90977165':[('ps',None,dict(height=3.6,top=3.9,roof='flat',wall='Ivory',rm='RoofDark',boards=False,storeys=1,door=(1,1),kind='pavilion'))],
 '90977169':[('pz',None,dict(height=3.8,top=4.1,roof='flat',wall='Rose',rm='RoofDark',boards=False,storeys=1,door=(1,1),kind='pavilion'))],
 '90965000':[('ts',None,dict(height=2.8,top=3.9,roof='saddle',ridge='long',wall='Falu',rm='RoofBrown',boards=True,storeys=1,door=(1,1),kind='shed'))],
 # Behind Kaggensgatan 38 (no satellite view)
 '92379301':[('kb',None,dict(height=2.5,top=3.8,roof='saddle',ridge='long',wall='Falu',rm='Tile',boards=True,storeys=1,door=(1,0),kind='shed'))],
 # Block Södra Långgatan / Kaggensgatan / Ölandsgatan (sat_a2)
 '92379273':[('kg',None,dict(height=6.65,top=8.7,roof='saddle',ridge='long',wall='GreyBeige',rm='RoofDark',boards=False,storeys=2,door=(0,-1),kind='range',skylights=2))],
 '92379300':[('kr',None,dict(height=6.65,top=9.5,roof='saddle',ridge='long',wall='Ochre',rm='Tile',boards=False,storeys=2,door=(0,-1),kind='range'))],
 '92379268':[('kh',None,dict(height=6.65,top=9.3,roof='hip',ridge='long',wall='Yellow',rm='Tile',boards=True,storeys=2,door=(0,-1),kind='range'))],
 # Block Västra Sjögatan / Södra Långgatan / Östra Sjögatan / Ölandsgatan (sat_a3)
 '92412871':[('vb',None,dict(height=3.1,top=5.0,roof='saddle',ridge='long',wall='Falu',rm='TileDark',boards=True,storeys=1,door=(1,0),kind='shed'))],
 '92412839':[('vm',None,dict(height=6.65,top=7.6,roof='mono',low=(0,-1),wall='PaleGrey',rm='RoofGrey',boards=False,storeys=2,door=(0,-1),kind='range'))],
 '92412854':[('vs',None,dict(height=6.65,top=9.6,roof='saddle',ridge='long',wall='PaleYellow',rm='Tile',boards=False,storeys=2,door=(-1,0),kind='range',skylights=2))],
 # Behind the town hall, north of Storgatan (sat_a5)
 '93238216':[('sm',('band',(99.95,34.11),(87.08,34.59),5.45),dict(height=6.4,top=8.9,roof='saddle',ridge='long',wall='GreyBeige',rm='TileDark',boards=False,storeys=2,door=(0,1),kind='range')),
   ('sl','rest',dict(height=3.2,top=3.4,roof='flat',wall='GreyBeige',rm='RoofDark',boards=False,storeys=1,door=None,kind='annex'))],
 # Block Södra Långgatan / Östra Sjögatan / Proviantgatan / Ölandsgatan (sat_a4, panorama 91846937_h337)
 '91846989':[('ow',('cut',(109.0,-120.86),(98.44,-123.19)),dict(height=6.65,top=9.9,roof='saddle',ridge='long',wall='White',rm='Tile',boards=False,storeys=2,door=(0,-1),kind='range',dormers=3,end_wall=('Falu',(0.976,0.22)))),
   ('ox','rest',dict(height=3.2,top=3.4,roof='flat',wall='Falu',rm='RoofDark',boards=True,storeys=1,door=None,kind='annex'))],
 '91846939':[('og',None,dict(height=4.4,top=8.2,roof='saddle',ridge='long',wall='Sage',rm='Tile',boards=True,storeys=1.5,door=(0,-1),kind='range',wall_dormer=True))],
 '91846948':[('oy',('cut',(143.97,-114.53),(128.79,-118.03)),dict(height=4.4,top=7.8,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=True,storeys=1.5,door=(0,-1),kind='range')),
   ('oz','rest',dict(height=4.4,top=7.0,roof='saddle',ridge='long',wall='Yellow',rm='Tile',boards=True,storeys=1.5,door=None,kind='wing'))],
 # Courtyard of the Storgatan / Proviantgatan / Södra Långgatan block (sat_a5)
 '91846923':[('sc',None,dict(height=6.65,top=10.4,roof='hip',ridge='long',wall='PaleYellow',rm='Tile',boards=False,storeys=2,door=(1,0),kind='range',chimneys=2))],
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
 out[name]=dict(spec,polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in z['ps']],rect=rect_of(z['ps'],z),walls=walls)
 report[name]={'osm':z['osm'],'area_m2':round(sum(p.area for p in z['ps']),1),'polygons':len(z['ps']),'walls':len(walls),
  'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'fill_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='fill'),1)}
foot=unary_union([PG(o) for o in HOUSES]);covered=unary_union([p for z in zones.values() for p in z['ps']])
data={'source':'district volumes '+', '.join(HOUSES)+' (source/district17.json), '+district['source'],'ids':list(HOUSES),'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for z in zones.values() for p in z['ps'])-covered.area,3)}}
(R/'source/block121.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(len(z['ps'])>=1 for z in zones.values())
(R/'previews/block121-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK121_ZONES_OK' if ok else 'BLOCK121_ZONES_REVIEW')
