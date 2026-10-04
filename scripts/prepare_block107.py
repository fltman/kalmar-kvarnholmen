"""Pass 107: Gamla kyrkogården (OSM way 149032114), the Stagnell burial chapel (OSM way 500979084) and the
medieval town church Bykyrkan (Storkyrkan, S:t Nikolai), demolished 1678.

Sources (view only, never used as textures; see references/gamla-kyrkogarden-research.md):
- Harald Åkerlund's grave plan 1944/1974, Sveriges kyrkor vol. 162 pl. XIII (pl13hi-010.png): scale bar
  0-40 m, north arrow, about 170 numbered graves drawn as black shapes, walls, paths, the chapel;
- Sven Rosman's excavation plan 1924, vol. 158 pl. I (r243-243.png, 1:300): church foundations, the
  present cemetery boundary, the wall and the octagonal chapel;
- Martin Olsson's reconstruction of the church about 1610, vol. 158 pl. II (plan), V and VII (elevations).

What this script does:
1. georeferences the grave plan to the project frame: a similarity transform (scale, rotation,
   translation) fitted by least squares to five wall corners of the OSM outline and the chapel;
2. georeferences Rosman's plan: scale from its metre bar, rotation and translation fitted to the chapel,
   the wall corner and the gate kink of the grave plan and the straight south-east boundary;
3. places the 1610 reconstruction (measured from pl. II in a church frame) on Rosman's foundations;
4. detects the graves on the grave plan as black shapes (connected components; solid blobs after a
   morphological opening, thin bars by stroke thickness, digits rejected), with position, size and
   orientation, and tags the notable ones from the research table;
5. writes source/block107.json and previews/block107-zones.json.

Run: KALMAR_GEO=<site-packages with shapely> python3 scripts/prepare_block107.py
The rendered plan pages are read from $KALMAR_GK; they are research-only and not redistributed.
"""
from pathlib import Path
import json,math,os,sys,hashlib
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
import numpy as np,cv2
from PIL import Image
from scipy.optimize import least_squares
from shapely.geometry import Polygon,Point,LineString,MultiLineString,box as sbox
from shapely.ops import unary_union,nearest_points
from shapely import affinity
R=Path(__file__).resolve().parents[1]
GK=Path(os.environ['KALMAR_GK'])
O=json.loads((R/'references/osm-slott98.json').read_text())
CEM=[tuple(p) for p in O['w149032114']['points'][:-1]]
CP=Polygon(CEM)
CH=np.array(O['w500979084']['points'][:-1]);CHC=CH.mean(0)
TRUE_N=28.2  # local bearing of true north
def H(s):return int(hashlib.sha256(s.encode()).hexdigest()[:8],16)
def rnd(v,n=3):return round(float(v),n)

# ---------------------------------------------------------------- 1. the grave plan (Åkerlund)
# Pixel positions read on pl13hi-010.png (1870 x 2459). Wall corners are the middle of the double
# wall line; the north-west corner is the intersection of the west and north wall lines (it is
# hidden under the drawn charnel house); the south tip is where the wall stub meets the south-east
# boundary line.
AK_BAR=(1185.75,1776.0,40.0)          # x of 0 and 40 m on the scale bar
AK_PXM=(AK_BAR[1]-AK_BAR[0])/AK_BAR[2]
wy=np.array([450,550,650,750,850,950.]);wx=np.array([374,333.5,292,248.5,205.5,162.5])
nx_=np.array([560,800,1100,1400,1650.]);ny_=np.array([353.5,323.5,278.5,231,192.5])
a1,b1=np.polyfit(wy,wx,1);a2,b2=np.polyfit(nx_,ny_,1);_y=(a2*b1+b2)/(1-a2*a1);NW_PX=(a1*_y+b1,_y)
AK_CORNERS=[('south tip',(813,2025),CEM[0]),('south-west bend',(343,1773),CEM[1]),('west bend',(144.5,992.5),CEM[2]),
 ('north-west corner',NW_PX,CEM[3]),('north-east corner',(1761,175),CEM[4])]
g_ak=np.array(Image.open(GK/'pl13hi-010.png').convert('L'));dark=(g_ak<128).astype(np.uint8)
def comp_at(mask,seed,minA=30):
 n,lab,st,cen=cv2.connectedComponentsWithStats(mask,8);best=None
 for i in range(1,n):
  x,y,w,h,A=st[i]
  if A<minA:continue
  if x<=seed[0]<=x+w and y<=seed[1]<=y+h:
   if best is None or w*h<best[1]:best=(i,w*h)
 i=best[0];x,y,w,h,A=st[i];m=(lab==i).astype(np.uint8)
 cn,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);c=max(cn,key=cv2.contourArea)
 return dict(bbox=(int(x),int(y),int(w),int(h)),rect=cv2.minAreaRect(c),A=int(A))
# The chapel octagon on the plan: the centre of the outline's box; the round gravel area: median
# radius to the first line outside the octagon along 72 rays.
oc=comp_at(dark,(610,1667));bx,by,bw,bh=oc['bbox'];AK_OCT=(bx+bw/2,by+bh/2);AK_OCT_R=(bw+bh)/4
rr=[]
for k in range(72):
 t=k*math.tau/72;r0=AK_OCT_R+6
 for r in np.arange(r0,AK_OCT_R+120,.5):
  x,y=int(round(AK_OCT[0]+r*math.cos(t))),int(round(AK_OCT[1]+r*math.sin(t)))
  if dark[y,x]:rr.append(r);break
AK_ROUND_R=float(np.median(rr))+2.5  # rays stop at the inner edge of the drawn line; +2.5 px to its middle
def fit_sim(src,dst,w=None,fix_scale=None):
 # dst = a*src + b in complex form (src y flipped: plans have y down); returns (a,b).
 z=np.array([p[0]-1j*p[1] for p in src]);t=np.array([q[0]+1j*q[1] for q in dst]);w=np.ones(len(z)) if w is None else np.array(w,float)
 A=np.c_[z,np.ones(len(z))]*np.sqrt(w)[:,None];sol=np.linalg.lstsq(A,t*np.sqrt(w),rcond=None)[0]
 return complex(sol[0]),complex(sol[1])
AKS=[c[1] for c in AK_CORNERS]+[AK_OCT];AKD=[c[2] for c in AK_CORNERS]+[tuple(CHC)]
AK_A,AK_B=fit_sim(AKS,AKD)
def ak(p):
 w=AK_A*(p[0]-1j*p[1])+AK_B;return (w.real,w.imag)
def ak_len(px):return px*abs(AK_A)
def ak_ang(deg_img):
 # an image angle (degrees, x right, y down, as cv2 gives) -> a local angle (radians from +x)
 return -math.radians(deg_img)+math.atan2(AK_A.imag,AK_A.real)
AK_RES=[(n,rnd(math.dist(ak(p),q),2)) for (n,p,q) in AK_CORNERS]+[('chapel centre',rnd(math.dist(ak(AK_OCT),CHC),2))]
AK_SCALE=1/abs(AK_A);AK_NORTH=math.degrees(math.atan2((AK_A*1j).real,(AK_A*1j).imag))  # local bearing of plan "up"

# ---------------------------------------------------------------- 2. Rosman's plan
# Read on r243-243.png (2137 x 1474). Metre bar: 0 at x 1111.5, 40 m at x 1881.5 -> 19.25 px/m.
RO_PXM=(1881.5-1111.5)/40
RO_OCT=(525,852);RO_SW=(156,932);RO_KINK=(597,1271)
RO_SE=[(1838,150),(1748,250),(1657,350),(1565,450),(1473,550),(1381,650),(1288,750),(1104,950),(1012,1050),(920,1150),(828,1250),(735,1350)]
se_a,se_b=np.array(CEM[0]),np.array(CEM[7]);se_d=(se_b-se_a)/np.linalg.norm(se_b-se_a);se_n=np.array([-se_d[1],se_d[0]])
def ro_T(q,p):
 s,th,tx,ty=q;x=p[0]/s;y=-p[1]/s
 return np.array([x*math.cos(th)-y*math.sin(th)+tx,x*math.sin(th)+y*math.cos(th)+ty])
def ro_res(q):
 r=list(ro_T(q,RO_OCT)-CHC)+list(ro_T(q,RO_SW)-np.array(ak((343,1773))))+list(ro_T(q,RO_KINK)-np.array(ak((708,1964))))
 r+=[float((ro_T(q,p)-se_a)@se_n) for p in RO_SE];return np.array(r)
ro_free=least_squares(ro_res,[RO_PXM,.5,-985,60]).x
ro_fix=least_squares(lambda q:ro_res([RO_PXM,*q]),[.5,-985,60]).x;RO_Q=[RO_PXM,*ro_fix]
def ro(p):return tuple(ro_T(RO_Q,p))
def ro_report(q):
 r=ro_res(q);return {'px_per_m':rnd(q[0],2),'chapel_m':rnd(math.hypot(*r[0:2]),2),'wall_corner_m':rnd(math.hypot(*r[2:4]),2),
  'gate_kink_m':rnd(math.hypot(*r[4:6]),2),'se_line_rms_m':rnd(np.sqrt(np.mean(np.array(r[6:])**2)),2),'se_line_max_m':rnd(np.max(np.abs(r[6:])),2)}
RO_BEAR_X=math.degrees(math.atan2(math.cos(RO_Q[1]),math.sin(RO_Q[1])))  # local bearing of Rosman's +x

# ---------------------------------------------------------------- 3. the church about 1610 (Olsson pl. II)
# Church frame: u east along the axis from the west face of Södra valvet, v north from the axis
# (metres, measured on pl. II at 19.69 px/m: u=(x-545)/19.69, v=(650-y)/19.69).
CHURCH={
 'kalkkoret':dict(u=(3.45,13.2),v=(10.4,19.3),eave=6.3,ridge=13.0,roof='u',gable='w'),
 'north':[dict(name=n,u=u,v=(9.65,19.3),eave=6.3,ridge=13.0,roof='v',gable='n') for n,u in
  [('T',(13.2,22.2)),('S',(22.2,29.3)),('R',(29.3,37.4)),('Q',(37.4,43.5)),('P',(43.5,53.8))]],
 'sodra_valvet':dict(u=(0.0,11.2),v=(-16.5,-9.0),eave=6.3,ridge=12.5,roof='u',gable='w'),
 'south':[dict(name=n,u=u,v=(-16.5,-9.14),eave=6.3,ridge=13.0,roof='v',gable='s') for n,u in
  [('E',(11.2,20.1)),('F',(20.1,28.3)),('G',(28.3,36.8)),('H',(36.8,45.0)),('I',(45.0,52.8))]],
 'sakristia':dict(u=(52.8,57.9),v=(-16.5,-9.65),eave=6.3,ridge=9.0,roof='u',gable='e'),
 'west_low':dict(u=(6.2,14.7),v=(-9.1,10.4),eave=6.3),
 'tower':dict(u=(6.2,15.2),v=(-7.0,7.0),eave=26.0,spire_top=52.5),
 'hall':dict(u=(14.7,53.1),v=(-9.14,9.65),eave=13.5,ridge=22.0),
 'choir':dict(u=(53.1,66.0),v=(-9.65,10.7),eave=13.5,ridge=22.0),
 'hogkor':dict(u=(66.0,76.9),v=(-4.6,4.6),apse=72.4,eave=8.0,ridge=14.5),
 'turret':dict(u=61.7,ridge=22.0,top=30.0),
 'porch_door_u':16.1,'gravhus_uv':(13.7,-16.5),'kalkkoret_nw':(3.45,19.3)}
# Church frame -> Rosman pixels: Rosman's foundations give the Kalkkoret north-west corner, the
# chapel (the octagon of pl. II stands on the south wall line at u 13.7) and the outer face of the
# north wall (y about 176.3 - 0.008x on Rosman's sheet).
RO_KNW=(305,170);RO_NL=[(x,176.3-.00802*x) for x in range(320,1330,100)]
def cf_T(q,uv):
 th,tx,ty=q;u,v=uv;x=u*math.cos(th)-v*math.sin(th);y=u*math.sin(th)+v*math.cos(th)
 return np.array([tx+x*RO_PXM,ty-y*RO_PXM])
def cf_res(q):
 r=list(cf_T(q,CHURCH['kalkkoret_nw'])-RO_KNW)+list(cf_T(q,CHURCH['gravhus_uv'])-RO_OCT)
 th=q[0];nrm=np.array([-math.sin(th),-math.cos(th)])  # image-space normal of the church's u axis (y down)
 p0=cf_T(q,(0,19.3));r+=[float((np.array(p)-p0)@nrm) for p in RO_NL];return np.array(r)/RO_PXM
cf_q=least_squares(cf_res,[0.0,240,540]).x;CF_R=cf_res(cf_q)
def cf(uv):return ro(tuple(cf_T(cf_q,uv)))
C0=np.array(cf((0,0)));CU=np.array(cf((1,0)))-C0;CV=np.array(cf((0,1)))-C0
AXIS_BEAR=math.degrees(math.atan2(CU[0],CU[1]))
def cfi(xy):
 d=np.array(xy)-C0;M=np.c_[CU,CV];return tuple(np.linalg.solve(M,d))
# The church footprint (local), for the kerb and the zones preview.
def rect_uv(u,v):return [(u[0],v[0]),(u[1],v[0]),(u[1],v[1]),(u[0],v[1])]
fp_uv=[rect_uv(CHURCH['kalkkoret']['u'],CHURCH['kalkkoret']['v']),rect_uv(CHURCH['sodra_valvet']['u'],CHURCH['sodra_valvet']['v']),
 rect_uv(CHURCH['sakristia']['u'],CHURCH['sakristia']['v']),rect_uv(CHURCH['west_low']['u'],CHURCH['west_low']['v']),
 rect_uv(CHURCH['hall']['u'],CHURCH['hall']['v']),rect_uv(CHURCH['choir']['u'],CHURCH['choir']['v'])]
fp_uv+=[rect_uv(c['u'],c['v']) for c in CHURCH['north']+CHURCH['south']]
hk=CHURCH['hogkor'];hw=(hk['v'][1]-hk['v'][0])/2  # three-sided east end
HK_UV=[(hk['u'][0],-hw),(hk['apse'],-hw),(hk['u'][1],-hw*.42),(hk['u'][1],hw*.42),(hk['apse'],hw),(hk['u'][0],hw)]
fp_uv.append(HK_UV)
FOOT=unary_union([Polygon([cf(p) for p in r]) for r in fp_uv]).buffer(.01).buffer(-.01)
foot_ring=LineString(list(FOOT.exterior.coords))
inner=CP.buffer(-1.0)
kerb=foot_ring.intersection(inner)
KERB=[[(rnd(x),rnd(y)) for x,y in g.coords] for g in getattr(kerb,'geoms',[kerb]) if g.geom_type=='LineString' and g.length>.5]

# ---------------------------------------------------------------- 4. graves from the grave plan
a=dark.copy();a[1900:,:]=0;a[:,:60]=0
k9=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9));op=cv2.morphologyEx(a,cv2.MORPH_OPEN,k9)
def comps(m):
 n,lab,st,cen=cv2.connectedComponentsWithStats(m,8);out=[]
 for i in range(1,n):
  x,y,w,h,A=st[i]
  mm=(lab[y:y+h,x:x+w]==i).astype(np.uint8)
  cn,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);c=max(cn,key=cv2.contourArea)
  (cx,cy),(rw,rh),ang=cv2.minAreaRect(c);hull=cv2.contourArea(cv2.convexHull(c))
  out.append(dict(i=i,x=int(x),y=int(y),w=int(w),h=int(h),A=int(A),cx=cx+x,cy=cy+y,rw=rw,rh=rh,ang=ang,fill=A/max(rw*rh,1),sol=A/max(hull,1)))
 return out,lab
big,lb=comps(op)
big=[b for b in big if b['A']>=70 and b['w']<110 and b['h']<110 and b['sol']>.8]
dil=cv2.dilate(np.isin(lb,[b['i'] for b in big]).astype(np.uint8),k9)
sm,ls=comps(a);dist=cv2.distanceTransform(a,cv2.DIST_L2,3)
txt=[s for s in sm if 16<=s['h']<=27 and s['w']<=22 and s['A']>=20]
def isdigit(s):
 # a glyph of the numbering: text height, and a neighbour of the same height and top close beside it
 if not(16<=s['h']<=27):return False
 for t in txt:
  if t is s:continue
  if abs(t['y']-s['y'])<=3 and abs(t['h']-s['h'])<=3 and max(t['x']-(s['x']+s['w']),s['x']-(t['x']+t['w']))<=9:return True
 return False
small=[]
for s in sm:
 if s['A']<12 or s['w']>40 or s['h']>40 or dil[int(s['cy']),int(s['cx'])]:continue
 th=float(dist[ls==s['i']].max())
 if not(s['fill']>.65 and s['sol']>.75 and th>=2.0):continue
 # Bars of headstones are drawn with a heavier pen (stroke half-width 3.8 px) than the digits (2.7 px).
 if th>=3.2 or (s['A']>=85 and min(s['rw'],s['rh'])>=5.5 and not isdigit(s)):small.append(s)
# Corrections after checking the overlay (SCR/p107/ex3_all.png): glyphs or drawn outlines taken as
# graves (the digit 8 of no. 8, the 1 of the chapel, two arrow heads of the charnel house outline,
# the outlines of nos. 20 and 45, modelled separately) and bars missed because they touch a line or a
# digit (nos. 155, 90, 158, 23, 51).
DROP=[(561,1770),(563,1666),(499,401),(434,487),(814,1370),(431,1583)]
ADD=[(710,454),(567,627),(1045,414),(534,1605),(903,1199)]
small=[s for s in small if min(math.dist((s['cx'],s['cy']),d) for d in DROP)>12]
have={(round(s['cx']),round(s['cy'])) for s in small}
for p in ADD:
 c=min((s for s in sm if s['A']>=40 and s['w']<45 and s['h']<45),key=lambda s:math.dist((s['cx'],s['cy']),p))
 if math.dist((c['cx'],c['cy']),p)<15 and (round(c['cx']),round(c['cy'])) not in have:small.append(c)
# Outlined features (not black): enclosures, the urn of no. 20, the Kristoffer monument no. 45,
# no. 154 (a small ring), Wijk's square (no. 15) and the plot of no. 18.
SEEDS={'36':(390,1387),'34':(463,1424),'35':(393,1460),'44':(723,1173),'153':(287,757),'15':(737,1679),'18':(837,1583),
 '45':(814,1370),'20':(431,1583),'154':(647,430)}
outl={}
for k,p in SEEDS.items():
 c=comp_at(dark,p,minA=20);(cx,cy),(rw,rh),ang=c['rect'];outl[k]=dict(px=(cx,cy),L=max(rw,rh),W=min(rw,rh),ang=ang+(90 if rh>rw else 0))
# Research positions (references/gamla-kyrkogarden-research.md, project frame) of the notable graves.
NOTE={'15':(-948.7,7.6),'28':(-953.9,19.7),'20':(-963.4,22.9),'22':(-958.0,18.1),'36':(-961.1,33.2),'44':(-935.1,34.5),'50':(-921.1,28.0),
 '53':(-921.0,13.2),'54':(-916.0,13.8),'73':(-904.5,13.1),'74':(-902.6,15.4),'96':(-874.5,63.0),'139':(-875.7,36.3),'45':(-934.2,23.4)}
graves=[]
def add(px,L,W,ang,src):
 x,y=ak(px);graves.append(dict(x=x,y=y,L=ak_len(L),W=ak_len(W),a=ak_ang(ang),src=src,num=''))
for b in big:
 L,W,ang=(b['rw'],b['rh'],b['ang']) if b['rw']>=b['rh'] else (b['rh'],b['rw'],b['ang']+90)
 add((b['cx'],b['cy']),L,W,ang,'blob' if not(b['fill']<.86 and abs(b['rw']-b['rh'])<.25*max(b['rw'],b['rh'])) else 'round')
for s in small:
 L,W,ang=(s['rw'],s['rh'],s['ang']) if s['rw']>=s['rh'] else (s['rh'],s['rw'],s['ang']+90)
 add((s['cx'],s['cy']),L,W,ang,'bar')
def tag(num,src=None,maxd=3.5):
 p=NOTE[num];cand=[g for g in graves if not g['num'] and (src is None or g['src'] in src)]
 g=min(cand,key=lambda g:math.dist((g['x'],g['y']),p));d=math.dist((g['x'],g['y']),p)
 if d<=maxd:g['num']=num;return rnd(d,2)
 return None
MATCH={n:tag(n) for n in ['28','53','54','73','74','96','139','50']}
# 166-168, the 1500s slabs: the three blobs nearest (-868,39..44) along the south-east path.
for n,p in [('166',(-868.0,39.0)),('167',(-868.0,44.0)),('168',(-868.0,41.5))]:
 NOTE[n]=p
for n in ['167','168','166']:MATCH[n]=tag(n,('blob',),5.0)
# Wijk's obelisk stands in the square no. 15: the blob inside it.
NOTE['15']=ak(outl['15']['px']);MATCH['15']=tag('15',None,1.5)
# Johansson's marble urn monument no. 20 and Kristoffer no. 45 are drawn as outlines.
G20=ak(outl['20']['px']);G45=ak(outl['45']['px']);G154=ak(outl['154']['px'])
MATCH['20']=rnd(math.dist(G20,NOTE['20']),2);MATCH['45']=rnd(math.dist(G45,NOTE['45']),2)
# Nordenanckar nos. 22-23: the two bars nearest (-958.0,18.1).
for n in ['22','23']:
 NOTE[n]=NOTE['22'];MATCH[n]=tag(n,('bar',),3.0)
# Kind and height of every grave (estimated): bars are standing stones or cast-iron crosses,
# 0.8-1.6 m; blobs are lying slabs (0.12-0.25 m) or, for some mid-sized ones, chest tombs (0.5-0.65 m).
for g in graves:
 h=H(f"{g['x']:.2f},{g['y']:.2f}");g['seed']=h
 if g['src']=='bar':
  g['kind']='cross' if h%3==0 else 'stone';g['h']=round(.8+(h>>4)%9*.1,2);g['L']=min(max(g['L'],.45),1.1)
 elif g['src']=='round':g['kind']='round';g['h']=round(.5+(h>>4)%4*.1,2)
 else:
  A=g['L']*g['W']
  if A<.9:g['kind']='block';g['h']=round(.45+(h>>4)%4*.08,2)
  elif 1.8<A<4.6 and h%4==0:g['kind']='tumba';g['h']=round(.5+(h>>4)%4*.05,2)
  else:g['kind']='slab';g['h']=round(.12+(h>>4)%4*.04,2)
SPEC={'28':dict(kind='ironcross_ped',h=1.87,cw=1.07),'53':dict(kind='ironcross',h=2.5,cw=1.19),'73':dict(kind='ironcross',h=1.36,cw=.88),
 '54':dict(kind='tumba',h=.56,L=2.07,W=1.52,mat='Limestone'),'50':dict(kind='tumba_rail',h=.55,L=2.23,W=1.62,rail=1.33),
 '74':dict(kind='pillar',h=2.5,mat='RedLime'),'96':dict(kind='urn',h=1.06),'139':dict(kind='obelisk',h=2.4,mat='RedLime'),
 '15':dict(kind='obelisk_mound',h=3.5,mat='BlackGranite'),'166':dict(kind='slab',h=.14,L=1.8,W=1.5,mat='Limestone'),
 '167':dict(kind='slab',h=.14,L=2.36,W=1.2,mat='Limestone'),'168':dict(kind='slab',h=.14,L=2.1,W=1.24,mat='Limestone'),
 '22':dict(kind='marblecross',h=1.27),'23':dict(kind='marblestone',h=1.44)}
for g in graves:
 if g['num'] in SPEC:g.update(SPEC[g['num']])
# Keep every grave inside the walls: a grave whose footprint crosses 0.6 m inside the OSM outline is
# pushed inwards (the plan and OSM differ by up to a few metres at the south-west wall).
pushed=0
for g in graves:
 r=max(g['L'],g['W'])/2;core=CP.buffer(-.6-r)
 if not core.contains(Point(g['x'],g['y'])):
  q=nearest_points(core,Point(g['x'],g['y']))[0];g['x'],g['y']=q.x,q.y;pushed+=1
# Enclosures: iron railings (36, 44, 18, 153) and stone kerbs (34, 35), from the outlines.
# Rectangles read on the plan (centre px, long side px, short side px, image angle of the long side):
# the outlines are broken (posts, gate openings), so they are read by hand, except no. 153.
RECT={'36':((389.6,1435),48,47,-14),'44':((722,1225),80,55,81.7),'18':((837,1582),44,35,70),'34':((462,1473),46,42,-14),'35':((395,1505),32,28,-14)}
o=outl['153'];RECT['153']=(o['px'],o['L'],o['W'],o['ang'])
ENCL=[]
for k,kind,h in [('36','rail',.9),('44','rail_blocks',.92),('18','rail',.9),('153','rail',.9),('34','kerb',.25),('35','kerb',.25)]:
 c,Lp,Wp,an=RECT[k];x,y=ak(c);ENCL.append(dict(num=k,x=rnd(x),y=rnd(y),L=rnd(ak_len(Lp)),W=rnd(ak_len(Wp)),a=rnd(ak_ang(an),4),kind=kind,h=h))
# no. 36 holds two cast-iron crosses (Wiberg); no. 153 a round element; the bars inside 36 are its crosses.
for g in graves:
 for e in ENCL:
  if e['num']=='36' and math.dist((g['x'],g['y']),(e['x'],e['y']))<1.7 and g['src']=='bar':g['kind']='ironcross';g['h']=1.3;g['cw']=.7;g['num']=g['num'] or '36'

# ---------------------------------------------------------------- 5. paths, gates, walls
# Centre lines read on the grave plan (pixel rows/columns between the two path lines, 2.0-2.4 m).
MAIN_PX=[(751,1962),(781,1900),(829,1800),(896,1700),(973,1600),(1043,1500),(1130,1400),(1271,1200),(1428,1000),(1506,900),(1557,800),
 (1603,700),(1641,600),(1675,500),(1701,400),(1727,300),(1742,240)]
BRANCH_PX=[(1043,1492),(1000,1486),(950,1505),(900,1521),(850,1536),(800,1557),(750,1585),(700,1598)]
main=[ak(p) for p in MAIN_PX];branch=[ak(p) for p in BRANCH_PX]
# The plan stops at the north-east corner; the OSM outline runs on 28 m in a narrow passage to the
# north-east gate on Molinsgatan, which the OSM path (way 149032157) follows.
ne_end=LineString([CEM[5],CEM[6]]);osm_path=LineString(O['w149032157']['points'])
NE_GATE=ne_end.intersection(osm_path);NE_GATE=(NE_GATE.x,NE_GATE.y)
main+=[NE_GATE]
# The south gate: between the pier and the stub end on the plan, moved onto the OSM wall line.
sg=((735+766)/2,(1953+1985)/2);sgl=ak(sg);sw_edge=LineString([CEM[0],CEM[1]]);q=sw_edge.interpolate(sw_edge.project(Point(sgl)))
S_GATE=(q.x,q.y);main[0]=S_GATE
CHAPEL_R=float(np.mean(np.hypot(*(CH-CHC).T)))
ROUND_R=ak_len(AK_ROUND_R)
branch[-1]=tuple(np.array(CHC)+(np.array(branch[-1])-CHC)/np.linalg.norm(np.array(branch[-1])-CHC)*(ROUND_R-.5))
PATH_W=2.1
paths=unary_union([LineString(main).buffer(PATH_W/2,cap_style=2,join_style=1),LineString(branch).buffer(PATH_W/2,join_style=1),
 Point(*CHC).buffer(ROUND_R,resolution=24)]).intersection(CP)
# Walls along south-west, west, north to the north-east gate (RAÄ: walls S-W-N-NE, none NE-S).
WALL_RUN=[CEM[0],CEM[1],CEM[2],CEM[3],CEM[4],CEM[5],CEM[6]]
def gap_split(run,gates,half):
 # cut the wall polyline at the gates (gap 2*half), returning pieces and gate frames
 L=LineString(run);out=[];cuts=sorted((L.project(Point(g)),g) for g in gates);s0=0
 for s,g in cuts:
  if s-half>s0:out.append([(p.x,p.y) for p in [L.interpolate(t) for t in [s0]+[L.project(Point(v)) for v in run if s0<L.project(Point(v))<s-half]+[s-half]]])
  s0=s+half
 out.append([(p.x,p.y) for p in [L.interpolate(t) for t in [s0]+[L.project(Point(v)) for v in run if s0<L.project(Point(v))<L.length]+[L.length]]])
 return out
GATE_HALF=1.5
walls=gap_split(WALL_RUN,[S_GATE,NE_GATE],GATE_HALF)
def gate_frame(g,run):
 L=LineString(run);s=L.project(Point(g));p=L.interpolate(max(0,s-.5));q=L.interpolate(min(L.length,s+.5))
 return dict(x=rnd(g[0]),y=rnd(g[1]),a=rnd(math.atan2(q.y-p.y,q.x-p.x),4),w=2*GATE_HALF)
GATES=[gate_frame(S_GATE,WALL_RUN),gate_frame(NE_GATE,WALL_RUN)]

# ---------------------------------------------------------------- 6. Kristoffer and trees
u45,v45=cfi(G45);KRIST=cf((u45,0.0))
# Old trees (positions estimated): the research names elms, limes, horse chestnuts and a weeping ash;
# the museum map shows trees spread over the lawn with a group on the church site and a few along
# the south-east path, and photos show large chestnuts south and east of the Kristoffer pillar.
graves_pts=unary_union([Point(g['x'],g['y']).buffer(max(g['L'],g['W'])/2+1.2) for g in graves]+
 [Point(e['x'],e['y']).buffer(max(e['L'],e['W'])/2+1.2) for e in ENCL]+[Point(*G20).buffer(1.5),Point(*G45).buffer(2.5),Point(*KRIST).buffer(6.0)])
free=CP.buffer(-3.5).difference(paths.buffer(2.0)).difference(graves_pts).difference(Point(*CHC).buffer(ROUND_R+2.5))
rng=np.random.default_rng(107);trees=[]
def try_place(region,n,species,minsep=9.0,tries=4000):
 got=0;mx,my,Mx,My=region.bounds
 for _ in range(tries):
  if got>=n:break
  p=(float(rng.uniform(mx,Mx)),float(rng.uniform(my,My)))
  if not region.contains(Point(p)) or not free.contains(Point(p)):continue
  if any(math.dist(p,(t['x'],t['y']))<minsep for t in trees):continue
  trees.append(dict(x=rnd(p[0]),y=rnd(p[1]),sp=species[got%len(species)],s=rnd(rng.uniform(.9,1.15),2)));got+=1
kx,ky=KRIST;ax_=CU/np.linalg.norm(CU)
try_place(Point(kx-ax_[1]*6+ax_[0]*3,ky+ax_[0]*6+ax_[1]*3).buffer(5).union(Point(kx+ax_[0]*8,ky+ax_[1]*8).buffer(5)),2,['chestnut'],9.0)
try_place(FOOT.buffer(-1),3,['lime','elm','chestnut'],11.0)
try_place(LineString(main).buffer(7).difference(LineString(main).buffer(2.5)),4,['lime','elm'],13.0)
try_place(Point(*CHC).buffer(ROUND_R+6).difference(Point(*CHC).buffer(ROUND_R+2.5)),1,['weeping_ash'],8.0)
try_place(CP,7,['elm','lime','chestnut'],15.0)

# ---------------------------------------------------------------- output
def ring(p):return [(rnd(x),rnd(y)) for x,y in p.exterior.coords[:-1]]
def flat(g):return [g] if g.geom_type=='Polygon' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='Polygon']
lawn=CP.difference(paths)
data={'source':'Åkerlund grave plan 1944/1974 (Sveriges kyrkor vol. 162 pl. XIII), Rosman excavation plan 1924 and Olsson reconstruction c. 1610 (vol. 158 pl. I, II, V, VII), OpenStreetMap ways 149032114, 500979084, 149032157 (ODbL); view only',
 'cemetery':[(rnd(x),rnd(y)) for x,y in CEM],
 'lawn':[{'outer':ring(p),'holes':[[(rnd(x),rnd(y)) for x,y in h.coords[:-1]] for h in p.interiors]} for p in flat(lawn)],
 'gravel':[{'outer':ring(p),'holes':[[(rnd(x),rnd(y)) for x,y in h.coords[:-1]] for h in p.interiors]} for p in flat(paths)],
 'walls':[[(rnd(x),rnd(y)) for x,y in w] for w in walls if len(w)>=2],'gates':GATES,
 'chapel':{'c':(rnd(CHC[0]),rnd(CHC[1])),'r':rnd(CHAPEL_R),'osm_rot':rnd(math.atan2(*(CH[0]-CHC)[::-1]),4),'round_r':rnd(ROUND_R,2),'north_bearing':TRUE_N},
 'graves':[{k:(rnd(v,4) if isinstance(v,float) else v) for k,v in g.items()} for g in graves],
 'enclosures':ENCL,'urn20':(rnd(G20[0]),rnd(G20[1])),'ring154':(rnd(G154[0]),rnd(G154[1])),
 'kristoffer':{'xy':(rnd(KRIST[0]),rnd(KRIST[1])),'axis':rnd(math.atan2(CU[1],CU[0]),4),'plan45_offset_from_axis_m':rnd(v45*np.linalg.norm(CV),2)},
 'trees':trees,'kerb':KERB,
 'church':{'origin':(rnd(C0[0]),rnd(C0[1])),'u':(rnd(CU[0],5),rnd(CU[1],5)),'v':(rnd(CV[0],5),rnd(CV[1],5)),'spec':CHURCH,'hogkor_uv':HK_UV},
 'georef':{
  'grave_plan':{'px_per_m_bar':rnd(AK_PXM,3),'px_per_m_fit':rnd(AK_SCALE,3),'plan_north_bearing_fit':rnd(AK_NORTH,2),'plan_north_bearing_expected':TRUE_N,
   'residuals_m':dict(AK_RES),'rms_m':rnd(math.sqrt(np.mean([r**2 for _,r in AK_RES])),2)},
  'rosman_fixed_bar':ro_report(RO_Q),'rosman_free_scale':ro_report(ro_free),'rosman_x_bearing':rnd(RO_BEAR_X,2),
  'church_on_rosman_residuals_m':{'kalkkoret_nw':rnd(math.hypot(*CF_R[0:2]),2),'chapel':rnd(math.hypot(*CF_R[2:4]),2),'north_wall_rms':rnd(np.sqrt(np.mean(CF_R[4:]**2)),2)},
  'church_axis_bearing_local':rnd(AXIS_BEAR,2),'church_axis_bearing_true':rnd(AXIS_BEAR-TRUE_N,2),
  'notable_match_m':MATCH}}
checks={'cemetery_m2':rnd(CP.area,1),'lawn_m2':rnd(lawn.area,1),'gravel_m2':rnd(paths.area,1),'lawn_plus_gravel_m2':rnd(lawn.area+paths.area,1),
 'overlap_m2':rnd(lawn.intersection(paths).area,3),'graves':len(graves),'bars':sum(g['src']=='bar' for g in graves),'blobs':sum(g['src']!='bar' for g in graves),
 'graves_pushed_inside':pushed,'graves_outside':sum(not CP.contains(Point(g['x'],g['y'])) for g in graves),'enclosures':len(ENCL),'trees':len(trees),
 'kerb_m':rnd(sum(LineString(k).length for k in KERB),1),'church_footprint_m2':rnd(FOOT.area,1),
 'church_footprint_in_cemetery_m2':rnd(FOOT.intersection(CP).area,1),'wall_m':rnd(sum(LineString(w).length for w in walls if len(w)>=2),1),
 'chapel_r':rnd(CHAPEL_R,2),'round_r':rnd(ROUND_R,2),'church_bbox_uv':(76.9,35.8)}
data['checks']=checks
(R/'source/block107.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
ok=abs(checks['lawn_plus_gravel_m2']-checks['cemetery_m2'])<1 and checks['overlap_m2']<.01 and checks['graves_outside']==0 and None not in [MATCH[k] for k in ['28','53','54','73','96','139','15']]
(R/'previews/block107-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':{
 'cemetery':{'area_m2':checks['cemetery_m2']},'lawn':{'area_m2':checks['lawn_m2']},'gravel':{'area_m2':checks['gravel_m2']},
 'church_1610':{'area_m2':checks['church_footprint_m2'],'inside_cemetery_m2':checks['church_footprint_in_cemetery_m2']}},'checks':checks,'georef':data['georef']},indent=2,ensure_ascii=False))
print(json.dumps(data['georef'],indent=1,ensure_ascii=False))
print(json.dumps(checks,ensure_ascii=False))
print('BLOCK107_PREPARE','OK' if ok else 'REVIEW')
