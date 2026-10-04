"""Pass 116: the first Gamla stan pass on the mainland west of Kvarnholmen. Molinsgatan and the east
part of Västerlånggatan (centroid x > -930): 18th-19th-century boarded wooden houses (red, yellow,
white, pink, pale blue, dark brown), a few rendered villas and the 1940s block on Molinsgatan. Pass 98
built them as plain volumes inside its chunk meshes (source/block98.json, OSM, ODbL); this pass
selects the 37 outlines that lie within 25 m of Molinsgatan, or within 25 m of Västerlånggatan with
their centroid at x > -930 (the OSM street lines in references/osm-slott98.json), and splits each into
rectangular zones for its roofs:
- each outline is framed on its longest edge and cut into slabs at its vertices; slabs with the same
  depth are merged, so an L or T outline becomes two or three rectangles;
- the largest rectangle is the main body (eaves, ridge and roof from the spec below); the others are
  wings with the same eaves (a lower ridge from their width) or, when small or narrow, one-storey
  annexes; a spec can override the wings.
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas resected on the OSM outlines; the rest is estimated from storeys, doors
and windows. See references/block116-notes.md.
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

# ---------------------------------------------------------------- selection
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') in ('Molinsgatan','Västerlånggatan') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
MOL=unary_union(ST['Molinsgatan']);VLG=unary_union(ST['Västerlånggatan'])
IDS=[]
for b in B98:
 if b['id'] in P115:continue
 g=Polygon(b['outer']).buffer(0)
 if g.distance(MOL)<25 or (g.distance(VLG)<25 and g.centroid.x>-930):IDS.append(b['id'])

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; st: storeys (1, 1.5, 2); height/top: eaves and
# ridge above the ground; roof: saddle, hip, gambrel, low (shallow hip on any outline) or flat;
# ridge: 'long' (along the main rectangle's long side) or 'short'; rm: roof material; fr: window
# frame colour; seen: the photo the values are read from (None = not seen; estimated).
# wing: overrides for the other rectangles; extras: per-house features drawn in the build.
H={
 # Molinsgatan, north-east side (south-east to north-west)
 '387312777':dict(name='dark green corrugated store',wall='DarkGreen',boards=True,st=1,height=3.9,top=4.4,roof='saddle',rm='RoofDark',fr='Frame',seen='m01_h196, m02_h196',measured='top 4.1-4.6 (m02_h196)',small_windows=True),
 '93332240':dict(name='sage rendered two-storey house',wall='Sage',boards=False,st=2,height=6.0,top=9.4,roof='saddle',rm='RoofSlate',fr='FrameOchre',seen='m02_h16',measured='eaves about 6 (scaled; the camera is not resected)',extras=['dormer_balcony']),
 '93332253':dict(name='Molinsgatan 6: red boarded two-storey gable house, the cottage beside it and the link',wall='Red',boards=True,st=2,height=5.8,top=7.9,roof='saddle',rm='Tile',fr='Frame',seen='m03_h16',measured='eaves 5.8, ridge 7.9, windows 0.95-2.3 and 3.9-5.2 (resected)',
  wing=dict(height=3.0,top=5.2),extras=['door_link','no_door']),
 '93332235':dict(name='pale yellow boarded one-storey gable house with carved bargeboards',wall='PaleYellow',boards=True,st=1,height=3.4,top=5.4,roof='saddle',rm='Tile',fr='Frame',seen='m04_h16',measured='eaves 3.4, ridge 5.4 (resected, 6 m shift)',extras=['carved','gate_white','no_door']),
 '93332239':dict(name='red boarded house (behind)',wall='Red',boards=True,st=1.5,height=3.8,top=6.4,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93332238':dict(name='red boarded house (behind)',wall='Red',boards=True,st=1.5,height=3.8,top=6.4,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93332244':dict(name='long white boarded range with dormers',wall='White',boards=True,st=1.5,height=4.0,top=7.6,roof='saddle',rm='Tile',fr='Frame',seen='m05_h8 (roof), v04_h157',extras=['dormers']),
 '93332251':dict(name='small shed with a tile roof',wall='White',boards=True,st=1,height=2.4,top=3.9,roof='saddle',rm='Tile',fr='Frame',seen='m05_h8'),
 '93332250':dict(name='white boarded gable house with red window frames',wall='White',boards=True,st=2,height=5.4,top=8.8,roof='saddle',rm='Tile',fr='FrameRed',seen='m05_h8, v05_h150, v04_h157',measured='storeys and gable windows read by eye'),
 '93332247':dict(name='red rendered house with dormers in the courtyard',wall='RedRender',boards=False,st=1.5,height=4.4,top=8.0,roof='saddle',rm='Tile',fr='Frame',seen='m02_h16 (far), v02_h178 (far)',extras=['dormers']),
 '93332246':dict(name='red boarded house (inside the block)',wall='Red',boards=True,st=1.5,height=3.8,top=6.4,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93332241':dict(name='yard shed',wall='Red',boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '1433973300':dict(name='yard shed',wall='Red',boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 # Molinsgatan, south-west side
 '93306345':dict(name='grey-green rendered 1940s block',wall='GreyGreen',boards=False,st=2,height=8.2,top=10.0,roof='hip',rm='RoofDark',fr='Frame',seen='m02_h196, m03_h196',measured='eaves 8.4, chimney top 10.4, raised ground floor 2.1 (Google camera, camera height 2.0)',extras=['chimneys2','stair_bays']),
 '93306337':dict(name='dark boarded house',wall='DarkBrown',boards=True,st=1.5,height=4.0,top=6.6,roof='saddle',rm='RoofDark',fr='Frame',seen='m03_h196 (edge)'),
 '93306341':dict(name='dark blue-grey boarded house with a mansard (gambrel) roof',wall='BlueGrey',boards=True,st=1.5,height=3.6,top=7.0,roof='gambrel',rm='Tile',fr='Frame',seen='v05_h150, v06_h149 (far)'),
 '93306358':dict(name='red boarded two-storey house with white trim',wall='Red',boards=True,st=2,height=5.4,top=8.2,roof='saddle',rm='Tile',fr='Frame',seen='v06_h149 (far)'),
 '93306347':dict(name='red boarded house with white trim and the ornamented chimney',wall='Red',boards=True,st=2,height=5.2,top=8.0,roof='saddle',rm='Tile',fr='Frame',seen='v05_h150, v06_h149',extras=['chimney']),
 '93306339':dict(name='dark brown boarded two-storey gable house at the corner',wall='DarkBrown',boards=True,st=2,height=5.4,top=8.0,roof='saddle',rm='RoofGrey',fr='Frame',seen='v06_h149',measured='storeys read by eye (two rows of windows)',extras=['gate_blue']),
 # Västerlånggatan, north side (east to west)
 '93333661':dict(name='cream rendered two-storey house with deep eaves',wall='Cream',boards=False,st=2,height=6.4,top=8.6,roof='low',rm='Tile',fr='Frame',seen='v10_h15, v01_h344',ov=.9),
 '93333644':dict(name='pink boarded villa with the carved glazed veranda',wall='Pink',boards=True,st=1.5,height=4.0,top=7.4,roof='saddle',rm='Tile',fr='Frame',seen='v02_h358, v01_h344',ridge='short',extras=['carved','chimney_red'],annex='veranda'),
 '93333651':dict(name='light blue boarded one-and-a-half-storey gable house',wall='Blue',boards=True,st=1.5,height=4.0,top=7.6,roof='saddle',rm='Tile',fr='Frame',seen='v03_h355',ridge='short'),
 '93333666':dict(name='Västerlånggatan 6: yellow boarded cottage with the red garage door',wall='Yellow',boards=True,st=1,height=3.0,top=4.9,roof='saddle',rm='Tile',fr='Frame',seen='v03_h355',extras=['garage_red']),
 '93333625':dict(name='boarded two-storey house (behind)',wall='Ochre',boards=True,st=2,height=5.4,top=8.4,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93333618':dict(name='white boarded two-storey house',wall='White',boards=True,st=2,height=5.6,top=8.4,roof='saddle',rm='Tile',fr='Frame',seen='v04_h337'),
 '93333634':dict(name='white rendered corner villa with the yellow boarded porch at its east end',wall='White',boards=False,st=2,height=6.0,top=9.4,roof='hip',rm='Tile',fr='Frame',seen='v06_h329, v05_h330',annex_spec=dict(wall='Yellow',boards=True),extras=['porch_gable']),
 '93309091':dict(name='white rendered house with the black sheet-metal hipped roof (Västerlånggatan 12)',wall='White',boards=False,st=1,height=3.5,top=5.6,roof='hip',rm='RoofBlack',fr='FrameRed',seen='v07_h329',bay=1.9,measured='eaves 3.5, door top 2.25, ridge about 5.6 (Google camera, height 2.2)',extras=['chimneys2','door_double']),
 '93309084':dict(name='red boarded two-storey villa with the central gable (Västerlånggatan 14)',wall='Red',boards=True,st=2,height=5.7,top=9.0,roof='saddle',rm='Tile',fr='Frame',seen='v08_h329',measured='eaves 4.9-5.0 and gable apex 8.6 on the hedge line, read up by 0.8 to a 2.3 m camera: eaves 5.7; frontispiece 2.8 m wide at the middle',extras=['frontis','chimneys2','door_porch']),
 '93309092':dict(name='house under renovation (wrapped)',wall='Grey',boards=True,st=1.5,height=3.6,top=6.4,roof='saddle',rm='RoofDark',fr='Frame',seen='v07_h329 (edge, wrapped in plastic)'),
 # Västerlånggatan, south side (east to west)
 '93332237':dict(name='yellow boarded two-storey house',wall='Yellow',boards=True,st=2,height=5.6,top=8.5,roof='saddle',rm='Tile',fr='Frame',seen='v02_h178'),
 '93332254':dict(name='Västerlånggatan 5: yellow boarded one-storey house',wall='Yellow',boards=True,st=1,height=3.4,top=6.0,roof='saddle',rm='Tile',fr='Frame',seen='v03_h175',extras=['chimney','door_street']),
 '93332236':dict(name='white boarded outbuilding with a mansard (gambrel) roof and a dormer window',wall='White',boards=True,st=1.5,height=2.6,top=5.8,roof='gambrel',rm='Tile',fr='Frame',seen='v04_h157',extras=['gable_window']),
 '93332245':dict(name='yellow boarded two-storey house',wall='Yellow',boards=True,st=2,height=5.5,top=8.2,roof='saddle',rm='Tile',fr='Frame',seen='v04_h157'),
 '93306360':dict(name='white boarded two-storey house',wall='White',boards=True,st=2,height=5.6,top=8.4,roof='saddle',rm='Tile',fr='Frame',seen='v07_h149'),
 '93306359':dict(name='boarded two-storey house behind the trees',wall='PaleYellow',boards=True,st=2,height=5.4,top=8.2,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93306350':dict(name='yellow boarded one-storey house with the red arched dormer',wall='Yellow',boards=True,st=1,height=3.3,top=6.4,roof='saddle',rm='TileDark',fr='Frame',seen='v08_h149',extras=['arched_dormer','red_eaves','no_door']),
 '93306353':dict(name='white boarded cottage with a mansard (gambrel) roof',wall='White',boards=True,st=1,height=2.8,top=5.6,roof='gambrel',rm='Tile',fr='Frame',seen='v09_h121'),
}
assert set(H)==set(IDS),(sorted(set(IDS)-set(H)),sorted(set(H)-set(IDS)))

def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>.5]
def frame_of(poly):
 cs=list(poly.exterior.coords)[:-1];a,b=max(zip(cs,cs[1:]+cs[:1]),key=lambda pq:math.dist(*pq))
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return a,d,(-d[1],d[0])
def decompose(poly):
 # Slab decomposition in the frame of the longest edge: rectangles (s0,s1,t0,t1).
 o,d,n=frame_of(poly);cs=list(poly.simplify(.15).exterior.coords)[:-1]
 st=[((v[0]-o[0])*d[0]+(v[1]-o[1])*d[1],(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1]) for v in cs]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 S0,S1,T0,T1=min(s for s,t in st),max(s for s,t in st),min(t for s,t in st),max(t for s,t in st)
 if poly.area>.85*(S1-S0)*(T1-T0):
  # nearly a rectangle (small notches only): one zone, the roof on the boxed outline
  return [(dict(s0=S0,s1=S1,t0=T0,t1=T1),Polygon([P(S0,T0),P(S1,T0),P(S1,T1),P(S0,T1)]))]
 ss=sorted(s for s,t in st);cuts=[ss[0]]
 for s in ss[1:]:
  if s-cuts[-1]>1.0:cuts.append(s)
 cuts[-1]=ss[-1]
 if len(cuts)<2:cuts=[ss[0],ss[-1]]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 tlo,thi=min(t for s,t in st)-1,max(t for s,t in st)+1;slabs=[]
 for s0,s1 in zip(cuts,cuts[1:]):
  # the depth is read inside the slab, 0.15 m in from its cuts, so that a cut a few cm off a vertex
  # does not carry the neighbour's depth
  e=min(.15,(s1-s0)/4);piece=poly.intersection(Polygon([P(s0+e,tlo),P(s1-e,tlo),P(s1-e,thi),P(s0+e,thi)]))
  if piece.area<.2:continue
  ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for g in flat(piece) for v in g.exterior.coords]
  slabs.append([s0,s1,min(ts),max(ts)])
 # A main strip over the full length, where the slabs share enough depth (an L, T or a house with
 # a bump at the back); the rest of each slab beside it becomes wing pieces.
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
 # absorb slivers (under 1.2 m along the frame) into the neighbour
 i=0
 while len(out)>1 and i<len(out):
  if out[i][1]-out[i][0]<1.2:
   j=i-1 if i>0 else i+1;out[j]=[min(out[j][0],out[i][0]),max(out[j][1],out[i][1]),min(out[j][2],out[i][2]),max(out[j][3],out[i][3])];out.pop(i);i=0
  else:i+=1
 return [(dict(s0=s0,s1=s1,t0=t0,t1=t1),Polygon([P(s0,t0),P(s1,t0),P(s1,t1),P(s0,t1)])) for s0,s1,t0,t1 in out]

OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
zones={}
def rect_on(a,b,depth,length=None):
 # The rectangle on the edge a->b (extended to 'length'), 'depth' to the left of a->b.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0]);L=length or L
 return Polygon([a,(a[0]+d[0]*L,a[1]+d[1]*L),(a[0]+d[0]*L+n[0]*depth,a[1]+d[1]*L+n[1]*depth),(a[0]+n[0]*depth,a[1]+n[1]*depth)])
V=lambda i,k:tuple(BY[i]['outer'][k])
# Molinsgatan 6 (93332253), read on m03_h16: the two-storey house stands with its 6.2 m gable on the
# street and runs 15.5 m back; the cottage beside it also has its gable (5.5 m) on the street; the
# rest of the outline is the low link with the entrance between them.
RECTS={'93332253':[rect_on(V('93332253',7),V('93332253',8),6.2),rect_on(V('93332253',2),V('93332253',3),9.6,5.45)]}
for osm in IDS:
 spec=H[osm]
 if osm in RECTS:
  rs=[(None,orient(r)) for r in RECTS[osm]]
  rest=OUT[osm].difference(unary_union([r for _,r in rs]))
  for bit in flat(rest):
   if bit.area>3:rs.append(('link',orient(bit)))
 else:
  rs=decompose(OUT[osm]);rs.sort(key=lambda r:-r[1].area)
 taken=Polygon()
 for k,(fr,rect) in enumerate(rs):
  ps=parts(OUT[osm].intersection(rect).difference(taken))
  if not ps:continue
  taken=unary_union([taken]+ps)
  cs=list(rect.exterior.coords)[:-1]
  if Polygon(cs).exterior.is_ccw is False:cs=cs[::-1]
  ed=[math.dist(cs[i],cs[(i+1)%4]) for i in range(4)];w=min(ed);area=sum(p.area for p in ps)
  if fr=='link':z=dict(height=2.8,top=3.0,roof='flat',role='link')  # the low link between the parts
  elif k==0:z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
  elif area<12 or w<2.6:
   z=dict(height=min(spec['height'],3.1),top=min(spec['height'],3.1)+.25,roof='flat',role='annex')
   z.update(spec.get('annex_spec',{}))
  else:
   c0=list(rs[0][1].exterior.coords)[:-1];mw=min(math.dist(c0[i],c0[(i+1)%4]) for i in range(4))
   z=dict(height=spec['height'],top=spec['height']+(spec['top']-spec['height'])*min(1,w/mw),roof=spec['roof'] if spec['roof']!='low' else 'low',role='wing')
   z.update(spec.get('wing',{}))
   if 'height' in spec.get('wing',{}) and 'top' not in spec.get('wing',{}):z['top']=z['height']+(spec['top']-spec['height'])*min(1,w/mw)
  zones[f'{osm}_{k}']=(osm,ps,dict(z,rect=[list(v) for v in cs]))
 if spec.get('annex')=='veranda':
  # the glazed veranda is the annex nearest the street
  ax=[k for k in zones if zones[k][0]==osm and zones[k][2]['role']=='annex']
  if ax:zones[min(ax,key=lambda k:unary_union(zones[k][1]).distance(VLG))][2]['role']='veranda'
 # Bits of the outline outside every rectangle (slivers at the cuts) join the zone they touch most.
 rem=OUT[osm].difference(taken)
 for bit in flat(rem):
  if bit.area<.01:continue
  mine=[k for k in zones if zones[k][0]==osm]
  k=max(mine,key=lambda k:Polygon(zones[k][2]['rect']).buffer(.3).intersection(bit).area)
  o_,ps_,sp_=zones[k];zones[k]=(o_,parts(unary_union(ps_+[bit])),sp_)
# the remainder of an outline not covered by its rectangles (should be nothing)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0)),b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h-.30
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
 hs=H[osm]
 # the outer wall that faces the nearest street (outward normal towards it), for the door
 best=None
 for w in walls:
  if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
  mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
  nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
  for nm,ln in (('Molinsgatan',MOL),('Västerlånggatan',VLG)):
   sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
   if dd<.01 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
   if best is None or dd<best[0]:best=(dd,nm,[w['p'],w['q']])
 spec=dict(spec,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best else None)
 out[name]=dict(spec,osm=osm,mesh='SM_Slott116_'+osm,wall=(spec.get('wall') or hs['wall']),boards=spec.get('boards',hs['boards']),
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:{k:v for k,v in H[i].items()} for i in IDS}
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block116.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block116-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK116_ZONES_OK' if ok else 'BLOCK116_ZONES_REVIEW')
