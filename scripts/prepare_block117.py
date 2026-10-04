"""Pass 117: the second Gamla stan pass on the mainland west of Kvarnholmen. The west part of
Västerlånggatan (centroid x <= -930) and Gamla Kungsgatan with Paters gränd: 18th-19th-century boarded
wooden houses (red, yellow, white, green, grey) under tile roofs, and a few rendered stone houses (the
ochre house at Gamla Kungsgatan 10 with its rusticated ground floor and mansard roof, the salmon house
with the pediment beside it). Pass 98 built them as plain volumes inside its chunk meshes
(source/block98.json, OSM, ODbL); this pass selects the outlines that lie within 25 m of
Västerlånggatan with their centroid at x <= -930, or within 25 m of Gamla Kungsgatan or Paters gränd
(the OSM street lines in references/osm-slott98.json), leaving out the houses of passes 107, 115 and
116, and splits each into rectangular zones for its roofs (the slab method of pass 116):
- each outline is framed on its longest edge and cut into slabs at its vertices; slabs with the same
  depth are merged, so an L or T outline becomes two or three rectangles;
- the largest rectangle is the main body (eaves, ridge and roof from the spec below); the others are
  wings with the same eaves (a lower ridge from their width) or, when small or narrow, one-storey
  annexes.
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas resected on the OSM outlines; the rest is estimated from storeys, doors
and windows. See references/block117-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings'];BY={b['id']:b for b in B98}
OSM=json.loads((R/'references/osm-slott98.json').read_text())
P115={'91931339','91222116','91222187','874870421','93332243','93332252','93306354','387312778','387312779','91970278','91970355','91970390','91970274','564958332'}
P107={'500979084'}  # the Stagnell chapel (pass 107)

# ---------------------------------------------------------------- selection
STREETS=('Molinsgatan','Västerlånggatan','Gamla Kungsgatan','Paters gränd')
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') in STREETS and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
MOL,VLG,GKG,PAT=SL['Molinsgatan'],SL['Västerlånggatan'],SL['Gamla Kungsgatan'],SL['Paters gränd']
IDS=[]
for b in B98:
 if b['id'] in P115 or b['id'] in P107:continue
 g=Polygon(b['outer']).buffer(0)
 if g.distance(MOL)<25 or (g.distance(VLG)<25 and g.centroid.x>-930):continue  # pass 116
 if (g.distance(VLG)<25 and g.centroid.x<=-930) or g.distance(GKG)<25 or g.distance(PAT)<25:IDS.append(b['id'])

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; st: storeys (1, 1.5, 2); height/top: eaves and
# ridge above the ground; roof: saddle, hip, gambrel (brutet sadeltak), mansard (hipped, two slopes),
# flat; ridge: 'par' (parallel to the street wall) or 'perp' (gable on the street); brk: the break of
# a gambrel or mansard roof; rm: roof material; fr: window frame colour; sh: shutter colour;
# seen: the photo the values are read from (None = not seen; estimated); extras: features drawn in the
# build.
H={
 # Västerlånggatan, south-east side (south-west to north-east)
 '93292658':dict(name='beige rendered villa',wall='Beige',boards=False,st=1.5,height=4.8,top=8.8,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w01_h106 (far, 37 m)',extras=['frontis','chimneys2']),
 '93292678':dict(name='yellow rendered one-and-a-half-storey villa with shutters and red dormers',wall='Yellow',boards=False,st=1.5,height=4.0,top=8.6,roof='saddle',ridge='perp',rm='Tile',fr='Frame',sh='Shutter',seen='w01_h106, w02_h108',extras=['dormers_red','chimney','gable_windows']),
 '93292704':dict(name='red boarded one-and-a-half-storey house with the street dormer',wall='Red',boards=True,st=1.5,height=3.6,top=7.4,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w02_h108',extras=['frontis','chimney']),
 '93292681':dict(name='small red boarded outbuilding',wall='Red',boards=True,st=1,height=2.5,top=4.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None,shed=True),
 '93292660':dict(name='pale yellow boarded two-storey house with white trim and the glazed door',wall='PaleYellow',boards=True,st=2,height=5.4,top=7.9,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w03_h119',extras=['chimney','door_glass']),
 '93292686':dict(name='red boarded cottage',wall='Red',boards=True,st=1,height=2.8,top=5.0,roof='saddle',ridge='perp',rm='Tile',fr='Frame',seen='w03_h119'),
 '93292708':dict(name='red boarded cottage with a tile roof',wall='Red',boards=True,st=1,height=2.8,top=4.9,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w04_h119',extras=['chimney']),
 '93292684':dict(name='pale yellow boarded two-storey gable house with white trim',wall='PaleYellow',boards=True,st=2,height=4.0,top=5.7,roof='saddle',ridge='perp',rm='Tile',fr='Frame',seen='w04_h119',measured='eaves 4.0, apex 5.7, windows 0.7-1.5 and 2.6-3.6 (resected, two cameras)',extras=['gable_window','low_storeys']),
 '93292674':dict(name='tall red boarded gable house with black trim',wall='Red',boards=True,st=2,height=7.0,top=10.2,roof='saddle',ridge='perp',rm='Tile',fr='Frame',trim='Black',seen='w04_h119, w05_h123',measured='eaves 6.8-7.4, apex 9.6-10.4, windows 1.1-2.8, 4.1-5.7 and the gable window 6.8-8.3 (resected, two cameras)',extras=['gable_window','bands_black','dormers_red']),
 '93292657':dict(name='red boarded house behind the tall gable house',street='Västerlånggatan',wall='Red',boards=True,st=1.5,height=4.0,top=7.4,roof='saddle',ridge='perp',rm='Tile',fr='Frame',seen=None),
 '93292707':dict(name='Västerlånggatan 25: long red boarded corner house with the knee-wall windows',street='Västerlånggatan',wall='Red',boards=True,st=1.5,height=4.2,top=6.9,roof='hip',ridge='par',rm='Tile',fr='Frame',seen='w05_h123',measured='eaves 4.2-4.5, ridge 6.9, chimney top 7.4, windows 0.6-2.2 and 3.2-3.9 (resected)',extras=['knee','chimney']),
 '93292675':dict(name='white boarded garage with black doors',wall='White',boards=True,st=1,height=2.6,top=3.1,roof='saddle',ridge='par',rm='RoofGrey',fr='Frame',seen='w06_h126',shed=True,extras=['garage_black']),
 '93292665':dict(name='grey boarded one-and-a-half-storey house with the big red tile roof',wall='Grey',boards=True,st=1.5,height=3.4,top=7.8,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w06_h126, w07_h134',measured='eaves about 3.2 (Google camera)',extras=['skylight','chimneys2']),
 '93292699':dict(name='long red boarded house with green shutters under a gambrel roof',wall='Red',boards=True,st=1,height=3.2,top=6.2,brk=5.0,roof='gambrel',ridge='par',rm='Tile',fr='Frame',sh='ShutterGreen',seen='w07_h134, w08_h121',measured='eaves about 3.0-3.4, break about 5.0, ridge about 6.2 (Google camera, the wall reads 0.6 m short)',extras=['chimney']),
 '93292693':dict(name='pale yellow boarded house under a gambrel roof with its gable on the street',wall='PaleYellow',boards=True,st=2,height=3.6,top=7.6,brk=6.0,roof='gambrel',ridge='perp',rm='Tile',fr='Frame',seen='w08_h121, v09_h121 (pass 116)',extras=['chimney','dormer','gable_windows']),
 '93306348':dict(name='pale yellow boarded cottage (behind)',wall='PaleYellow',boards=True,st=1,height=3.0,top=5.4,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='v09_h121 (pass 116, partly)'),
 '93306357':dict(name='sage-green boarded two-storey gable house with the lunette',wall='Sage',boards=True,st=2,height=5.6,top=8.6,roof='saddle',ridge='perp',rm='RoofGrey',fr='Frame',seen='v09_h121 (pass 116)',extras=['lunette']),
 '93306344':dict(name='white boarded house under a gambrel roof',wall='White',boards=True,st=1.5,height=3.2,top=6.6,brk=5.4,roof='gambrel',ridge='par',rm='Tile',fr='Frame',seen='v09_h121 (pass 116)'),
 # Västerlånggatan, north-west side (the field)
 '149905962':dict(name='red boarded outbuilding by the field',wall='Red',boards=True,st=1,height=2.6,top=4.6,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='w01_h286, w02_h288 (far)',shed=True),
 '93309098':dict(name='white rendered house with the red tile hipped roof and the dormer',wall='White',boards=False,st=1.5,height=4.2,top=8.6,roof='hip',ridge='par',rm='Tile',fr='Frame',seen='w08_h301, v09_h301 (pass 116)',extras=['dormer','chimney']),
 # Gamla Kungsgatan and Paters gränd, west and north
 '93292705':dict(name='Gamla Kungsgatan 9: olive-green boarded house with white frames',wall='Olive',boards=True,st=1,height=3.8,top=6.6,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='k01_h210',extras=['eaves_deep']),
 '93292703':dict(name='yellow rendered two-storey house',wall='Yellow',boards=False,st=2,height=6.0,top=8.8,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='k01_h210, k02_h194'),
 '93292694':dict(name='Gamla Kungsgatan 10: ochre rendered two-storey house, rusticated ground floor, mansard roof with the curved gable',wall='Ochre',boards=False,st=2,height=7.2,top=10.6,brk=9.6,roof='mansard',ridge='par',rm='RoofSlate',fr='Frame',seen='k01_h30, k02_h14',measured='string course 4.4, eaves 7.3, curved gable top 10.3 (resected)',extras=['rustic','curved_gable','dormers_slate','door_double','cellar']),
 '93292700':dict(name='salmon rendered two-storey house with the pediment and lunette',wall='Salmon',boards=False,st=2,height=8.0,top=11.6,roof='hip',ridge='par',rm='Tile',fr='Frame',seen='k02_h14',measured='cornice 7.9-8.3, pediment apex 9.9, frontispiece 5.2 m wide in the middle, windows 1.8-3.6 and 4.7-6.9, plinth 0.7, dormer top 10.7 (resected)',extras=['pediment','pilasters','dormers_red','chimney','cellar']),
 '93292676':dict(name='ochre rendered two-storey house with a hipped roof (end of Paters gränd)',wall='Ochre',boards=False,st=2,height=6.0,top=9.4,roof='hip',ridge='par',rm='Tile',fr='Frame',seen='k02_h194 (far)'),
 '93292698':dict(name='ochre rendered two-storey house (beside it)',wall='Ochre',boards=False,st=2,height=6.0,top=9.4,roof='hip',ridge='par',rm='Tile',fr='Frame',seen='k02_h194 (far)'),
 # Gamla Kungsgatan, south-west and east
 '93292670':dict(name='light brick one-and-a-half-storey house with the balcony on Paters gränd',wall='LightBrick',boards=False,st=1.5,height=4.0,top=7.6,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='k02_h194',extras=['balcony']),
 '93292661':dict(name='yellow boarded house (not seen)',wall='Yellow',boards=True,st=1.5,height=3.8,top=7.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None),
 '93292662':dict(name='small red boarded outbuilding (not seen)',wall='Red',boards=True,st=1,height=2.5,top=4.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None,shed=True),
 '93292664':dict(name='white boarded cottage (not seen)',wall='White',boards=True,st=1,height=3.0,top=5.4,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None),
 '93292663':dict(name='red boarded house (not seen)',wall='Red',boards=True,st=1.5,height=3.8,top=7.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None),
 '93292659':dict(name='pale yellow boarded cottage (not seen)',wall='PaleYellow',boards=True,st=1,height=3.0,top=5.4,roof='saddle',ridge='perp',rm='Tile',fr='Frame',seen=None),
 '93292668':dict(name='yellow boarded cottage (not seen)',wall='Yellow',boards=True,st=1,height=3.0,top=5.2,roof='saddle',ridge='perp',rm='Tile',fr='Frame',seen=None),
 '93292697':dict(name='white boarded cottage with shutters and the brick chimney',wall='White',boards=True,st=1,height=2.9,top=5.2,roof='saddle',ridge='par',rm='Tile',fr='Frame',sh='ShutterWhite',seen='k04_h9',extras=['chimney_brick']),
 '93292671':dict(name='red boarded low house at the east end of Gamla Kungsgatan',wall='Red',boards=True,st=1,height=2.7,top=4.8,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen='k04_h9'),
 '93292687':dict(name='grey boarded cottage (not seen)',wall='Grey',boards=True,st=1,height=3.0,top=5.4,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None),
 '93292692':dict(name='small white boarded shed with a dark roof',wall='White',boards=True,st=1,height=2.3,top=3.4,roof='saddle',ridge='par',rm='RoofGrey',fr='Frame',seen='k03_h189 (edge)',shed=True),
 '93292669':dict(name='white boarded cottage (behind the hedge)',wall='White',boards=True,st=1,height=3.0,top=5.0,roof='saddle',ridge='par',rm='RoofGrey',fr='Frame',seen='k03_h189 (edge)'),
 '93292695':dict(name='small yellow boarded outbuilding (not seen)',wall='Yellow',boards=True,st=1,height=2.5,top=4.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None,shed=True),
 '93292691':dict(name='red boarded cottage (not seen)',wall='Red',boards=True,st=1,height=2.9,top=5.0,roof='saddle',ridge='par',rm='Tile',fr='Frame',seen=None),
}
assert set(H)==set(IDS),(sorted(set(IDS)-set(H)),sorted(set(H)-set(IDS)))

def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>.5]
def frame_of(poly):
 cs=list(poly.exterior.coords)[:-1];a,b=max(zip(cs,cs[1:]+cs[:1]),key=lambda pq:math.dist(*pq))
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return a,d,(-d[1],d[0])
def decompose(poly):
 # Slab decomposition in the frame of the longest edge: rectangles (s0,s1,t0,t1). (Pass 116's.)
 o,d,n=frame_of(poly);cs=list(poly.simplify(.15).exterior.coords)[:-1]
 st=[((v[0]-o[0])*d[0]+(v[1]-o[1])*d[1],(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1]) for v in cs]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 S0,S1,T0,T1=min(s for s,t in st),max(s for s,t in st),min(t for s,t in st),max(t for s,t in st)
 if poly.area>.85*(S1-S0)*(T1-T0):
  return [(dict(s0=S0,s1=S1,t0=T0,t1=T1),Polygon([P(S0,T0),P(S1,T0),P(S1,T1),P(S0,T1)]))]
 ss=sorted(s for s,t in st);cuts=[ss[0]]
 for s in ss[1:]:
  if s-cuts[-1]>1.0:cuts.append(s)
 cuts[-1]=ss[-1]
 if len(cuts)<2:cuts=[ss[0],ss[-1]]
 tlo,thi=min(t for s,t in st)-1,max(t for s,t in st)+1;slabs=[]
 for s0,s1 in zip(cuts,cuts[1:]):
  e=min(.15,(s1-s0)/4);piece=poly.intersection(Polygon([P(s0+e,tlo),P(s1-e,tlo),P(s1-e,thi),P(s0+e,thi)]))
  if piece.area<.2:continue
  ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for g in flat(piece) for v in g.exterior.coords]
  slabs.append([s0,s1,min(ts),max(ts)])
 c0,c1=max(sl[2] for sl in slabs),min(sl[3] for sl in slabs);dmax=max(sl[3]-sl[2] for sl in slabs)
 if len(slabs)>1 and c1-c0>=3.0 and c1-c0>=.5*dmax:
  pcs=[]
  for s0,s1,t0,t1 in slabs:
   for a_,b_ in ((t0,c0),(c1,t1)):
    if b_-a_>.6:pcs.append([s0,s1,a_,b_])
  wings=[]
  for pc in pcs:
   if wings and abs(wings[-1][1]-pc[0])<.01 and abs(wings[-1][2]-pc[2])<.6 and abs(wings[-1][3]-pc[3])<.6:wings[-1][1]=pc[1]
   else:wings.append(pc)
  out=[[slabs[0][0],slabs[-1][1],c0,c1]]+[w_ for w_ in wings if w_[1]-w_[0]>=1.2]
  return [(dict(s0=s0,s1=s1,t0=t0,t1=t1),Polygon([P(s0,t0),P(s1,t0),P(s1,t1),P(s0,t1)])) for s0,s1,t0,t1 in out]
 out=[]
 for sl in slabs:
  if out and abs(out[-1][2]-sl[2])<.6 and abs(out[-1][3]-sl[3])<.6:out[-1][1]=sl[1];out[-1][2]=min(out[-1][2],sl[2]);out[-1][3]=max(out[-1][3],sl[3])
  else:out.append(sl)
 i=0
 while len(out)>1 and i<len(out):
  if out[i][1]-out[i][0]<1.2:
   j=i-1 if i>0 else i+1;out[j]=[min(out[j][0],out[i][0]),max(out[j][1],out[i][1]),min(out[j][2],out[i][2]),max(out[j][3],out[i][3])];out.pop(i);i=0
  else:i+=1
 return [(dict(s0=s0,s1=s1,t0=t0,t1=t1),Polygon([P(s0,t0),P(s1,t0),P(s1,t1),P(s0,t1)])) for s0,s1,t0,t1 in out]

OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
zones={}
for osm in IDS:
 spec=H[osm];rs=decompose(OUT[osm]);rs.sort(key=lambda r:-r[1].area)
 taken=Polygon()
 for k,(fr,rect) in enumerate(rs):
  ps=parts(OUT[osm].intersection(rect).difference(taken))
  if not ps:continue
  taken=unary_union([taken]+ps)
  cs=list(rect.exterior.coords)[:-1]
  if Polygon(cs).exterior.is_ccw is False:cs=cs[::-1]
  ed=[math.dist(cs[i],cs[(i+1)%4]) for i in range(4)];w=min(ed);area=sum(p.area for p in ps)
  if k==0:z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
  elif area<12 or w<2.6:z=dict(height=min(spec['height'],3.1),top=min(spec['height'],3.1)+.25,roof='flat',role='annex')
  else:
   c0=list(rs[0][1].exterior.coords)[:-1];mw=min(math.dist(c0[i],c0[(i+1)%4]) for i in range(4))
   rf=spec['roof'] if spec['roof'] in ('saddle','hip') else 'saddle'
   z=dict(height=spec['height'],top=spec['height']+(spec['top']-spec['height'])*min(1,w/mw),roof=rf,role='wing')
  zones[f'{osm}_{k}']=(osm,ps,dict(z,rect=[list(v) for v in cs]))
 rem=OUT[osm].difference(taken)
 for bit in flat(rem):
  if bit.area<.01:continue
  mine=[k for k in zones if zones[k][0]==osm]
  k=max(mine,key=lambda k:Polygon(zones[k][2]['rect']).buffer(.3).intersection(bit).area)
  o_,ps_,sp_=zones[k];zones[k]=(o_,parts(unary_union(ps_+[bit])),sp_)
# Walls against a neighbour start at the neighbour's eaves: pass 98's height for the houses this pass
# leaves alone, the spec's eaves for the houses of this pass.
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0))-.30,b['id']) for b in B98 if b['id'] not in IDS and b['id'] not in P107]
mine_main=[(OUT[i],H[i]['height'],i) for i in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in mine_main:
  if bid!=osm and g.buffer(.001).contains(pt):return bid,h
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
out={};report={}
for name,(osm,ps,spec) in zones.items():
 Hh=spec['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(osm,Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=Hh-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':Hh,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 # the outer wall that faces the nearest of the four streets (outward normal towards it)
 best=None;hs=H[osm]
 for w in walls:
  if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
  mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
  nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
  for nm,ln in SL.items():
   if nm=='Molinsgatan' or (H[osm].get('street') and nm!=H[osm]['street']):continue
   sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
   if dd<.01 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
   if best is None or dd<best[0]:best=(dd,nm,[w['p'],w['q']])
 hs=H[osm]
 out[name]=dict(spec,osm=osm,mesh='SM_Slott117_'+osm,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best else None,
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'street':out[name]['street']}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'houses':H,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block117.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block117-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK117_ZONES_OK' if ok else 'BLOCK117_ZONES_REVIEW')
