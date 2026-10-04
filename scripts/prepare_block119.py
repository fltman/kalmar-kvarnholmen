"""Pass 119: the fourth and last Gamla stan pass on the mainland west of Kvarnholmen. Stora Dammgatan,
Lilla Dammgatan, Bremergatan, Smålandsgatan and Spikgatan: boarded wooden houses (red, yellow, white)
under tile roofs, the white Jugend villa with the green sheet roof and the entrance tower with its spire
(Bremergatan 9), the large four-storey public building at Bremergatan 13 (red-brick upper floors over a
cream rusticated ground floor with arched windows) and its pale yellow rendered corner range, rendered
villas, a yellow-brick villa and the 1940s-50s apartment blocks. Pass 98 built them as plain volumes
inside its chunk meshes (source/block98.json, OSM, ODbL); this pass selects the outlines that lie
within 25 m of one of the five streets (the OSM street lines in references/osm-slott98.json), leaving
out the houses of passes 107, 115, 116 and 117 and every house of pass 118 (within 25 m of Kungsgatan,
Söderportsgatan, Klostergatan or Skansgatan, unless pass 117's rule takes it), and splits each into
rectangular zones for its roofs (the slab method of pass 116):
- each outline is framed on its longest edge and cut into slabs at its vertices; slabs with the same
  depth are merged, so an L or T outline becomes two or three rectangles;
- the largest rectangle is the main body (eaves, ridge and roof from the spec below); the others are
  wings with the same eaves (a lower ridge from their width) or, when small or narrow, one-storey
  annexes.
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas resected on the OSM outlines; the rest is estimated from storeys, doors
and windows. See references/block119-notes.md.
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
PREV={'500979084'}
for n in (115,116,117,118):
 f=R/f'source/block{n}.json'
 if f.exists():PREV|=set(json.loads(f.read_text())['ids'])

# ---------------------------------------------------------------- selection
MINE=('Stora Dammgatan','Lilla Dammgatan','Bremergatan','Smålandsgatan','Spikgatan')
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
VLG,GKG,PAT=SL['Västerlånggatan'],SL['Gamla Kungsgatan'],SL['Paters gränd']
def p117(g):return (g.distance(VLG)<25 and g.centroid.x<=-930) or g.distance(GKG)<25 or g.distance(PAT)<25
def p118(g):return any(g.distance(SL[n])<25 for n in ('Kungsgatan','Söderportsgatan','Klostergatan','Skansgatan')) and not p117(g)
IDS=[]
for b in B98:
 if b['id'] in PREV:continue
 g=Polygon(b['outer']).buffer(0)
 if any(g.distance(SL[n])<25 for n in MINE) and not p117(g) and not p118(g):IDS.append(b['id'])

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; brick: brick coursing; st: storeys; height/top:
# eaves and ridge above the ground; roof: saddle, hip, gambrel, low (shallow hip) or flat; ridge:
# 'long' (along the main rectangle's long side), 'short', or gable_street=True (the gable on the
# street wall); rm: roof material; fr: window frame colour; plinth: plinth height; seen: the photo the
# values are read from (None = not seen; estimated); extras: per-house features drawn in the build.
H={
 # Stora Dammgatan, west end (seen only far on sd05 or not at all)
 '93292003':dict(name='white rendered two-storey house with its gable and balcony on the street',wall='White',boards=False,st=2,height=5.8,top=7.8,roof='saddle',rm='Tile',fr='Frame',seen='sd05_h332 (21 m)',gable_street=True,extras=['balcony_gable']),
 '93238223':dict(name='long white rendered two-storey house with a low saddle roof',wall='White',boards=False,st=2,height=5.8,top=7.6,roof='saddle',rm='Tile',fr='Frame',seen='sd05_h332 (35 m, its west part)'),
 '93238263':dict(name='red boarded house',wall='Red',boards=True,st=1.5,height=3.8,top=6.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93238280':dict(name='yellow boarded house on Stora Dammgatan',wall='Yellow',boards=True,st=1.5,height=3.8,top=6.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93238199':dict(name='white boarded cottage with an L-shaped outline',wall='White',boards=True,st=1,height=3.0,top=5.2,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93238233':dict(name='small red shed',wall='Red',boards=True,st=1,height=2.4,top=3.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93329943':dict(name='pale yellow boarded house',wall='PaleYellow',boards=True,st=1.5,height=3.8,top=6.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93329979':dict(name='red boarded outbuilding',wall='Red',boards=True,st=1,height=2.8,top=4.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 # Stora and Lilla Dammgatan, east part
 '93291981':dict(name='long red boarded one-and-a-half-storey house with knee-wall windows',wall='Red',boards=True,st=1.5,height=4.0,top=7.1,roof='saddle',rm='Tile',fr='Frame',seen='sd02_h339, ld01_h190 (edge)',measured='eaves 3.95-4.2 (Google camera, assumed height 2.3)',extras=['chimneys2','knee']),
 '93292001':dict(name='red boarded two-storey house with the lunette in its gable (Stora Dammgatan 4)',wall='Red',boards=True,st=2,height=5.3,top=7.9,roof='saddle',rm='Tile',fr='Frame',seen='sd04_h352',measured='eaves 5.2-5.4, apex 7.9, windows 1.0 and 3.4, lunette 5.1 (resected)',extras=['lunette','chimney']),
 '93292007':dict(name='yellow-brick three-storey 1950s apartment block with balconies',wall='YellowBrick',boards=False,brick=True,st=3,height=9.0,top=11.0,roof='saddle',rm='RoofDark',fr='Frame',plinth=.6,seen='ld01_h10, sd03_h340 (far)',measured='eaves 8.5-9.4 (Google camera)',extras=['chimneys2','balconies','stair_bay','dormer_one']),
 # Bremergatan
 '93309086':dict(name='Bremergatan 9: white rendered Jugend villa with the green sheet roof, the swept street gable and the entrance tower with its spire',wall='White',boards=False,st=1.5,height=4.5,top=8.2,roof='hip',rm='RoofGreen',fr='FrameRed',plinth=.6,rows=[[1.4,2.2,1.3]],bay=2.3,seen='br01_h214',measured='eaves 4.5, street gable apex 9.0, tower cornice 8.7, spire tip 14.2, windows 1.4-3.9 above the house base (Google camera; the garden stands about 0.7 m above the street)',extras=['jugend']),
 '93309102':dict(name='yellow-brick one-and-a-half-storey house with a dark tile roof',wall='YellowBrick',boards=False,brick=True,st=1.5,height=3.6,top=7.6,roof='saddle',rm='TileDark',fr='Frame',seen='br03_h214'),
 '93333650':dict(name='grey-beige rendered two-storey villa with a red tile hipped roof',wall='GreyBeige',boards=False,st=2,height=5.2,top=10.0,roof='hip',rm='Tile',fr='Frame',seen='br01_h34',measured='eaves 5.2 (resected, camera height 2.35)',extras=['chimney','roof_window']),
 '93333624':dict(name='yellow boarded two-storey house with a mansard (gambrel) roof and a lunette in its gable',wall='Yellow',boards=True,st=2,height=5.0,top=8.8,roof='gambrel',rm='RoofGrey',fr='Frame',seen='br01_h34',measured='eaves about 5.2, mansard break about 7.6 (resected, oblique)',extras=['lunette','chimney']),
 '93333632':dict(name='white boarded house',wall='White',boards=True,st=1.5,height=3.8,top=6.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93325640':dict(name='pale yellow rendered four-storey corner range of the Bremergatan 13 block',wall='PaleYellowRender',boards=False,st=4,height=16.0,top=19.0,roof='low',rm='Tile',fr='Frame',plinth=.9,annex_spec=dict(height=16.0,top=16.25),seen='br01_h214 (behind trees), br04_h213 (left edge)',extras=['bands']),
 '93325641':dict(name='Bremergatan 13: four-storey public building, red-brick upper floors over a cream rusticated ground floor with arched windows',wall='Brick',boards=False,brick=True,st=4,height=17.5,top=20.5,roof='low',rm='RoofDark',fr='FrameGreen',plinth=.9,seen='br04_h213',measured='plinth 0.9, ground-floor cornice 5.3, second-floor band 9.5 (Google camera, scaled to a 2.7 m camera height)',extras=['public']),
 '93325644':dict(name='north range of the Bremergatan 13 building',wall='Brick',boards=False,brick=True,st=4,height=17.5,top=20.5,roof='low',rm='RoofDark',fr='FrameGreen',plinth=.9,seen=None,extras=['public']),
 '93325643':dict(name='courtyard wing of the Bremergatan 13 building',wall='Brick',boards=False,brick=True,st=3,height=11.0,top=13.0,roof='low',rm='RoofDark',fr='FrameGreen',plinth=.9,annex_spec=dict(height=11.0,top=11.25),seen=None),
 # Smålandsgatan and Spikgatan
 '93453479':dict(name='beige rendered three-storey 1940s apartment block',wall='Beige',boards=False,st=3,height=9.6,top=12.6,roof='saddle',rm='Tile',fr='Frame',plinth=.6,seen=None,extras=['chimneys2','balconies']),
 '93453484':dict(name='small white boarded house',wall='White',boards=True,st=1.5,height=3.6,top=6.4,roof='saddle',rm='Tile',fr='Frame',seen=None),
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
RECTS={}
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
 # the nearest of this pass's five streets; another named street only when none of them is faced
 for group in (MINE,tuple(k for k in SL if k not in MINE)):
  for w in walls:
   if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
   mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
   nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
   for nm in group:
    ln=SL[nm];sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
    if dd<.01 or dd>30 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
    if best is None or dd<best[0]:best=(dd,nm,[w['p'],w['q']])
  if best:break
 spec=dict(spec,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best else None)
 out[name]=dict(spec,osm=osm,mesh='SM_Slott119_'+osm,wall=(spec.get('wall') or hs['wall']),boards=spec.get('boards',hs['boards']),
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:{k:v for k,v in H[i].items()} for i in IDS}
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block119.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block119-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK119_ZONES_OK' if ok else 'BLOCK119_ZONES_REVIEW')
