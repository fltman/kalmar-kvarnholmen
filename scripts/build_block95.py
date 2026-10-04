"""Pass 95: the south side of Fiskaregatan, east part (fronts face north onto the narrow street):
- 91926308 and 91926299: a boarded gate wall with a green double gate and a white door (the yard
  behind is open), then the pale boarded one-storey cottage with its gable to the street and one
  window in green frames reaching into the gable, standing across the joint of the two outlines;
  east of it a narrow link to the grey house, not seen on any panorama (estimated);
- 91926297: the pale grey boarded two-storey house with its gable to the street, a lunette in the
  gable, three window columns in green frames, pilaster strips and a tiled roof; east of it the
  gateway to the yard: a white boarded portal with a green gate, and a rendered stone pier and wall
  against the red house;
- 91926357: the red boarded two-storey house with white corner and bay pilasters, eight windows in
  white surrounds on the street, a light plinth and a tiled saddle roof along the street.

References: Google Street View (two panoramas on this block and one from pass 94, heading 166, two
of them resected on house corners), view only. Zones: source/block95.json; see
references/block95-notes.md. The lamp post, the low red boarded piece with the green cap at the red
house's west corner, the TV aerial and the yard behind the gate are omitted.
"""
B95D=json.loads((R/'source/block95.json').read_text());Z=B95D['zones']
block95_names=[];B95={}
for old in [k for k in list(materials) if k.startswith('M_Block95_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grey','TownIvory',(.78,.80,.78),.82,0),('GreyTrim','TownPaintWhite',(.84,.86,.84),.65,0),('Pale','TownIvory',(.85,.86,.83),.82,0),
 ('Cream','TownIvory',(.86,.81,.66),.82,0),('Red','TownPaintBrown',(.53,.16,.14),.80,0),('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('GreenFrame','TownPaintGreen',(.22,.40,.32),.60,0),('GreyGreen','TownPaintGreen',(.44,.50,.47),.60,0),('GateGreen','TownPaintGreen',(.27,.47,.38),.60,0),
 ('Render','TownIvory',(.86,.85,.82),.90,0),('Stone','TownStone',(.58,.55,.50),.92,0),('Plinth','TownStone',(.66,.66,.64),.90,0),('LightPlinth','TownStone',(.84,.84,.82),.88,0),
 ('Tile','TownTileRed',(.70,.38,.26),.80,0),('Chimney','TownTileRed',(.66,.45,.38),.85,0),('Sheet','TownMetalGrey',(.40,.41,.42),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block95_'+key;B95[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block95_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B95;WF=M['WhiteFrame']

def b95_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block95_names.append(name);return Mesh(name,category)
def drop_degenerate_faces95(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block95_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block95_dropped={};block95_samples={}
def b95_finish(m,osm):
 obj=s21_finish(m);block95_dropped[obj.name]=drop_degenerate_faces95(obj)
 obj['detail_pass']=95;obj['reference_notes']='references/block95-notes.md';obj['osm_way']=osm;return obj

# The street frame: origin at the front corner shared by 91926297 and 91926357, s eastwards along
# the fronts, t northwards (towards the street). Outlines lie at t = 0 on the street; the facade
# surfaces stand 0.355 m out.
C95=tuple(B95D['frame']['origin']);D95=tuple(B95D['frame']['along']);N95=(-B95D['frame']['inwards'][0],-B95D['frame']['inwards'][1])
A95=math.atan2(D95[1],D95[0])
def P95(s,t=0,z=None):
 p=(C95[0]+D95[0]*s+N95[0]*t,C95[1]+D95[1]*s+N95[1]*t);return p if z is None else (*p,z)
def rect95(zone):
 pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-C95[0])*D95[0]+(v[1]-C95[1])*D95[1] for v in pts];ts=[(v[0]-C95[0])*N95[0]+(v[1]-C95[1])*N95[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism95(m,outline,t0,t1,ma):
 # A closed prism with an (s, z) outline between depths t0 < t1 (gables, piers).
 n=len(outline);vs=[P95(s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)],ma)
def sbox95(m,s0,s1,t0,t1,z0,z1,ma):m.box(P95((s0+s1)/2,(t0+t1)/2,(z0+z1)/2),(s1-s0,t1-t0,z1-z0),ma,A95)
def gable_street95(m,zone,wall,roof,trim,ov=.30,eave=.40,srange=None):
 # Gable to the street: the ridge runs back from the street over the zone's boxed outline; gable
 # prisms in the wall material on the street front and at the back, bargeboards, gutters.
 s0,s1,t0,t1=rect95(zone)
 if srange:s0,s1=srange
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P95(e,tb,ze+.12),P95(sm,tb,T+.12),P95(sm,tf,T+.12),P95(e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P95(e,tb,ze+.02),P95(e,tf,ze+.02),.07,M['Sheet'],8)
  for tt in (tf-.02,tb+.02):town_path(m,[P95(e,tt,ze+.08),P95(sm,tt,T+.08)],.07,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism95(m,g,t1+.005,t1+o,wall);prism95(m,g,t0-o,t0-.005,wall)
 return s0,s1,t0,t1,sm,sl
def gable_boards95(m,sL,sR,sm,H,T,tface,holes,ma,step=.22):
 # Vertical boards on a street gable, clipped to the rakes and broken at the windows (s, b, w, h).
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.12;segs=[(H,z1)]
  for hs,hb,hw,hh in holes:
   if abs(s-hs)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:m.box(P95(s,tface+.02,(l0+h0)/2),(.035,.03,h0-l0),ma,A95)
def saddle95(m,zone,roof,wall,ov=.45,verge=.30):
 # Ridge along the street over the boxed outline; eaves from the wall faces pushed out by the
 # overhang; closed gable prisms at both ends.
 s0,s1,t0,t1=rect95(zone);H=Z[zone]['height'];T=Z[zone]['top'];o=.355;tm=(t0+t1)/2;half=t1-tm+o;sl=(T-H)/half
 for ta,sg in ((t1+o,1),(t0-o,-1)):
  e=ta+sg*ov;ze=H-ov*sl
  m.faces([P95(s0-o-verge,e,ze),P95(s1+o+verge,e,ze),P95(s1+o+verge,tm,T),P95(s0-o-verge,tm,T)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P95(s0-o-verge,e,ze-.05),P95(s1+o+verge,e,ze-.05),.07,M['WhiteFrame'],8)
 for s,sg in ((s0-o,1),(s1+o,-1)):
  sa,sb=(s,s+.30) if sg>0 else (s-.30,s)
  n=3;vs=[P95(ss,t,z) for ss in (sa,sb) for t,z in ((t1+o,H),(t0-o,H),(tm,T-.02))]
  m.faces(vs,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],wall)
 return s0,s1,t0,t1,tm,sl
def win95(m,x,y,u,b,w,h,a,frame,trim,o=.16,rows=None,bw=.12,head=False):
 cas81(m,x,y,u,b,w,h,a,frame,o,rows or (2 if h<1.1 else 3));surround36(m,x,y,u,b,w,h,a,trim,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,trim,a)
 if head:facade_box(m,x,y,u,.46,b+h+.20,w+.40,.16,.10,trim,a)
def slabwin95(m,x,y,u,b,w,h,a,frame,trim,head=False):
 # A window standing on a gable prism face (0.355 out): glass, casement and surround stand proud.
 facade_box(m,x,y,u,.365,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.40,2 if h<1.1 else 3)
 surround36(m,x,y,u,b,w,h,a,trim,.12,.42);facade_box(m,x,y,u,.50,b-.05,w+.24,.16,.06,trim,a)
 if head:facade_box(m,x,y,u,.50,b+h+.20,w+.40,.16,.10,trim,a)
def lunette95(m,s,zb,r,t,frame):
 # A half-round window on the gable face at depth t: glass half-disc and a framed arch.
 k=16;arc=[(s+r*math.cos(math.pi*i/k),zb+r*math.sin(math.pi*i/k)) for i in range(k+1)]
 m.faces([P95(ss,t+.012,zz) for ss,zz in arc],[tuple(range(k,-1,-1)),tuple(range(k+1))],GLAZE)
 town_path(m,[P95(s+(r+.06)*math.cos(math.pi*i/k),t+.05,zb+(r+.06)*math.sin(math.pi*i/k)) for i in range(k+1)],.06,frame)
 m.box(P95(s,t+.06,zb-.04),(2*r+.30,.12,.08),frame,A95);m.box(P95(s,t+.04,zb+r*.5),(.04,.03,r),frame,A95)
def oculus95(m,s,t,zc,r,frame,ang):
 # A round window on a wall facing along -s (the red house's west gable), at depth t.
 k=18;ring=[P95(s-.012,t+r*math.cos(i*math.tau/k),zc+r*math.sin(i*math.tau/k)) for i in range(k)]
 m.faces(ring,[tuple(range(k)),tuple(range(k-1,-1,-1))],GLAZE)
 town_path(m,[P95(s-.05,t+(r+.05)*math.cos(i*math.tau/k),zc+(r+.05)*math.sin(i*math.tau/k)) for i in range(k+1)],.05,frame)

# The street fronts: openings as (kind, s, bottom, width, height) in the street frame. Measured on
# the resected panoramas (see the notes); kinds: win, slab (a window reaching above the eaves,
# drawn on the gable prism).
GR_COLS=(-5.40,-8.07,-10.74)
OPS={'gr':[('win',s,1.57,1.15,1.32) for s in GR_COLS]+[('slab',s,4.22,1.15,1.03) for s in GR_COLS],
 'rd':[('win',s,b,1.00,1.52) for s in (2.14,5.03,7.91,10.80) for b in (1.40,3.88)],
 'co':[('slab',-17.49,1.50,1.10,1.10)],
 'ln':[]}
STYLE={'gr':dict(wall='Grey',trim='GreyTrim',frame='GreenFrame',plinth=(.45,'Plinth'),head=True),
 'rd':dict(wall='Red',trim='WhiteFrame',frame='GreyGreen',plinth=(.42,'LightPlinth')),
 'co':dict(wall='Pale',trim='WhiteFrame',frame='GreenFrame',plinth=(.30,'Plinth')),
 'ln':dict(wall='Pale',trim='WhiteFrame',frame='WhiteFrame',plinth=(.30,'Plinth'))}
PIL={'gr':[(-13.10+.16,.32),(-3.04-.16,.32),(-6.735,.28),(-9.405,.28)],'rd':[(.17,.34),(12.94-.17,.34),(4.24,.30),(8.70,.30)]}
def front95(w):
 ox,oy=outward(w);return w['kind']=='outer' and ox*N95[0]+oy*N95[1]>.9

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b95_new(nm,'Kvarnholmen/Fiskaregatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];st=STYLE[zone];wm=M[st['wall']];tm=M[st['trim']];fm=M[st['frame']];pz,pm=st['plinth']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if not front95(w):
   ox,oy=outward(w)
   if zone=='rd' and -(ox*D95[0]+oy*D95[1])>.9:
    # The red house's west wall over the gateway: boards only (the panorama shows no windows
    # below the gable; the round window is added with the roof).
    bz_wall(m,w['p'],w['q'],0,H,[],wm);boards82(m,x,y,L,a,pz+.02,H-.08,[],wm);facade_box(m,x,y,0,.39,pz/2,L+.02,.08,pz,M[pm],a);continue
   if L<1.5:bz_wall(m,w['p'],w['q'],0,H,[],wm);continue
   plain(m,w,H,wm,fm,tm,1 if H<4 else 2,.9);continue
  mine=[]
  for kind,s,b,ww,hh in OPS[zone]:
   X,Y=P95(s);u=U(w,X,Y)
   if abs(u)+ww/2<=L/2+.01:mine.append((kind,u,b,ww,hh))
  low=[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if kind=='win']
  bz_wall(m,w['p'],w['q'],0,H,low,wm)
  boards82(m,x,y,L,a,pz+.02,H-.08,low+[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if kind=='slab'],wm)
  for kind,u,b,ww,hh in mine:
   if kind=='slab':slabwin95(m,x,y,u,b,ww,hh,a,fm,tm,st.get('head',False))
   else:win95(m,x,y,u,b,ww,hh,a,fm,tm,head=st.get('head',False))
  # Plinth, pilasters (or corner boards), the eaves board on the eaves-to-street house.
  facade_box(m,x,y,0,.39,pz/2,L+.02,.08,pz,M[pm],a)
  if zone in PIL:
   for s,pw in PIL[zone]:
    X,Y=P95(s);u=U(w,X,Y)
    facade_box(m,x,y,u,.43,(pz+H-.12)/2,pw,.12,H-.12-pz,tm,a);facade_box(m,x,y,u,.46,pz+.25,pw+.08,.16,.50,tm,a)
    if zone=='gr':facade_box(m,x,y,u,.47,H-.25,pw+.14,.18,.18,tm,a)
  else:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+pz)/2,.18,.10,H-pz,tm,a)
  if zone=='rd':facade_box(m,x,y,0,.46,H-.10,L+.1,.16,.22,WF,a)
# Roofs and gables.
m=meshes[Z['gr']['mesh']];s0,s1,t0,t1,sm,sl=gable_street95(m,'gr',M['Grey'],M['Tile'],M['GreyTrim'],srange=(-13.10+.355,-3.04-.355))
H=Z['gr']['height'];T=Z['gr']['top'];o=.355
gable_boards95(m,s0-o,s1+o,sm,H,T,t1+o,[(s,4.22,1.15,1.03) for s in GR_COLS]+[(sm,6.03,1.35,.72)],M['Grey'])
lunette95(m,sm,6.09,.60,t1+o+.01,M['GreyTrim'])
X,Y=P95(sm+1.2,t0+4.0);chimney82(m,X,Y,T-.8,T+.75,M['Chimney'])
m=meshes[Z['co']['mesh']];s0,s1,t0,t1,sm,sl=gable_street95(m,'co',M['Pale'],M['Tile'],M['WhiteFrame'],ov=.25,eave=.35)
gable_boards95(m,s0-o,s1+o,sm,Z['co']['height'],Z['co']['top'],t1+o,[(-17.49,1.50,1.10,1.10)],M['Pale'])
X,Y=P95(sm,t1-3.0);chimney82(m,X,Y,Z['co']['top']-.5,Z['co']['top']+.7,M['Chimney'])
m=meshes[Z['ln']['mesh']];saddle95(m,'ln',M['Tile'],M['Pale'],ov=.30,verge=.0)
m=meshes[Z['rd']['mesh']];s0,s1,t0,t1,tm_,sl=saddle95(m,'rd',M['Tile'],M['Red'])
X,Y=P95(5.2,tm_-.6);chimney82(m,X,Y,Z['rd']['top']-.6,Z['rd']['top']+.8,M['Chimney'])
# The round window seen in a red gable over the gateway: placed on the red house's west gable
# (estimated; see the notes).
oculus95(m,s0-o,tm_,Z['rd']['height']+1.0,.30,WF,0)
# The gateway (released strip, s -3.04..0): the white boarded portal with the green gate, the
# rendered pier against the red house, and the rendered wall running back along the passage.
m=meshes[Z['gr']['mesh']];tf=.355
for sa,sb in ((-3.04,-2.89),(-1.10,-.95)):sbox95(m,sa,sb,tf-.30,tf,0,2.45,WF)
sbox95(m,-3.04,-.95,tf-.30,tf+.04,2.25,2.45,WF);sbox95(m,-3.10,-.89,tf-.36,tf+.10,2.45,2.53,M['Sheet'])
gx,gy=P95(-1.995,tf-.30);gate83(m,gx,gy,0,0,1.79,2.25,A95+math.pi,M['GateGreen'],WF)
sbox95(m,-.95,0,-.60,tf+.10,0,3.86,M['Render']);sbox95(m,-1.0,.05,-.65,tf+.15,3.86,3.96,M['Stone'])
sbox95(m,-.85,-.35,-6.0,-.60,0,3.60,M['Render']);sbox95(m,-.90,-.30,-6.05,-.60,3.60,3.68,M['Stone'])
# The boarded gate wall in the west 3.4 m of 91926308 (released strip): the green double gate and
# a white door, the yard behind.
m=meshes[Z['co']['mesh']];p,q=P95(-19.65+.005),P95(-23.09);x,y,L,a=sf_edge(p,q);Sg=lambda s:U({'p':p,'q':q},*P95(s))
holes=[(Sg(-21.765),0,2.13,2.10,0),(Sg(-20.28),.05,.74,2.0,0)]
bz_wall(m,p,q,0,2.23,holes,M['Pale']);boards82(m,x,y,L,a,.10,2.15,holes,M['Pale'])
gate83(m,x,y,holes[0][0],0,2.13,2.10,a,M['GateGreen'],WF);door83(m,x,y,holes[1][0],.05,.74,2.0,a,M['Pale'],WF,glass=False)
facade_box(m,x,y,0,.40,2.26,L+.1,.20,.08,WF,a)
for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,1.12,.16,.10,2.23,WF,a)
for nm in meshes:b95_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block95_cameras=[
 sv_camera('466_Block95_Cal_Grey',162.62,110.04,2.30,168.9,12.6,90),
 sv_camera('467_Block95_Cal_Red',170.88,108.36,2.30,166.8,14.1,90),
 sv_camera('468_Block95_Cal_Cottage',145.87,114.25,2.45,171.3,15,90),
 ('469_Block95_Aerial',(160.0,135.0,30.0),(160.0,104.0,2.0),28),
]
print('BLOCK95_GEOMETRY',len(block95_names),'dropped',block95_dropped,block95_samples)
