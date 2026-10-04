"""Pass 99: the row of four red boarded two-storey townhouses on the west side of north
Landshövdingegatan (district volumes 90859885, 90859837, 90859849 and 90859898, south to north).
Each house turns its gable to the street (east, towards the water): falu-red vertical boarding on a
dark plinth, white corner boards between the houses, a dark saddle roof running back from the
street, a wide four-light window over a wide window on the south side of the front, a two-light
window over the entrance on the north side, and a small gabled porch roof on white brackets over
the door, with steps and a black handrail. One parameterised house, placed per outline with each
house's own measured window and door positions.

References: Google Street View (two panoramas on Landshövdingegatan, resected on the boundaries
between the gables), view only. Zones: source/block99.json; see references/block99-notes.md. The
rear (west) walls are not seen and get plain casements. Antennas, the heat pump, lamps, house
numbers and planting are omitted.
"""
B99D=json.loads((R/'source/block99.json').read_text());Z=B99D['zones']
block99_names=[];B99={}
for old in [k for k in list(materials) if k.startswith('M_Block99_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownPaintBrown',(.50,.14,.13),.80,0),('White','TownPaintWhite',(.94,.94,.92),.55,0),('Plinth','TownStone',(.30,.30,.31),.90,0),
 ('Roof','TownMetalGrey',(.17,.17,.18),.60,.20),('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),('Iron','TownMetalGrey',(.06,.06,.065),.45,.40),
 ('PorchTile','TownTileRed',(.62,.30,.22),.80,0),('PorchBrown','TownTileRed',(.45,.27,.20),.80,0),('PorchDark','TownMetalGrey',(.22,.22,.23),.60,.20),
 ('DoorWood','TownPaintBrown',(.70,.48,.26),.60,0),('DoorOak','TownPaintBrown',(.55,.36,.22),.60,0),('DoorWhite','TownPaintWhite',(.92,.92,.90),.55,0),
 ('DoorDark','TownPaintBrown',(.30,.20,.15),.60,0),('Step','TownStone',(.62,.62,.60),.90,0),
 ]:
 name='M_Block99_'+key;B99[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block99_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B99;WF=M['White']

def b99_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block99_names.append(name);return Mesh(name,category)
def drop_degenerate_faces99(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block99_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),5),) for f in bad[:6]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block99_dropped={};block99_samples={}
def b99_finish(m,osm):
 obj=s21_finish(m);block99_dropped[obj.name]=drop_degenerate_faces99(obj)
 obj['detail_pass']=99;obj['reference_notes']='references/block99-notes.md';obj['osm_way']=osm;return obj

# Street frames: s along the OSM front line from A (south) to B (north), t outwards (east, towards
# the street); the facade surfaces stand at t = 0.355.
def fr99(A,B):
 L=math.dist(A,B);D=((B[0]-A[0])/L,(B[1]-A[1])/L);return dict(A=A,B=B,D=D,N=(D[1],-D[0]),L=L,ang=math.atan2(D[1],D[0]))
def P99(f,s,t=0,z=None):
 p=(f['A'][0]+f['D'][0]*s+f['N'][0]*t,f['A'][1]+f['D'][1]*s+f['N'][1]*t);return p if z is None else (*p,z)
def rect99(f,zone):
 pts=[v for g in Z[zone]['polygons'] for v in g];A,D,N=f['A'],f['D'],f['N']
 ss=[(v[0]-A[0])*D[0]+(v[1]-A[1])*D[1] for v in pts];ts=[(v[0]-A[0])*N[0]+(v[1]-A[1])*N[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism99(m,f,outline,t0,t1,ma):
 # A closed prism with an (s, z) outline between depths t0 < t1 (left-handed frame, as pass 97).
 n=len(outline);vs=[P99(f,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def gable99(m,f,zone,wall,roof,trim,ov=.30,eave=.35):
 # Saddle roof with its ridge running back from the street over the boxed outline; gable prisms in
 # the wall material at the street front and at the back, dark verge boards, gutters.
 s0,s1,t0,t1=rect99(f,zone)
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P99(f,e,tb,ze+.12),P99(f,sm,tb,T+.12),P99(f,sm,tf,T+.12),P99(f,e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P99(f,e,tb,ze+.02),P99(f,e,tf,ze+.02),.07,M['Sheet'],8)
  for tt in (tf-.03,tb+.03):town_path(m,[P99(f,e,tt,ze+.06),P99(f,sm,tt,T+.06)],.08,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism99(m,f,g,t1+.005,t1+o,wall);prism99(m,f,g,t0-o,t0-.005,wall)
 return sL,sR,sm,t1+o,sl
def gable_boards99(m,f,sL,sR,sm,H,T,tface,holes,ma,step=.22):
 # Vertical boards on the street gable, clipped to the rakes and broken at windows (s, b, w, h).
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.14;segs=[(H,z1)]
  for hs,hb,hw,hh in holes:
   if abs(s-hs)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:
   if h0-l0>.06:m.box(P99(f,s,tface+.02,(l0+h0)/2),(.035,.03,h0-l0),ma,f['ang'])
def win99(m,x,y,u,b,w,h,a,lights):
 # White casement window: outer frame, (lights-1) mullions, white surround and sill.
 facade_box(m,x,y,u,.12,b+h/2,w,.02,h,GLAZE,a)
 for q in [-w/2+.04,w/2-.04]+[-w/2+k*w/lights for k in range(1,lights)]:facade_box(m,x,y,u+q,.16,b+h/2,.08 if abs(q)>w/2-.05 else .07,.08,h,WF,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,.16,zz,w,.08,.08,WF,a)
 surround36(m,x,y,u,b,w,h,a,WF,.10,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,WF,a)
def porch99(m,x,y,u,a,w,dep,ze,zr,roof):
 # The small gabled porch roof over the door: two slopes from the wall out over 'dep', a red
 # boarded gable triangle with white verge boards and tie beam, white brackets back to the wall.
 o0,o1=.36,.36+dep;hw=w/2
 for s in (-1,1):
  m.faces([lp(x,y,u+s*hw,o0,ze,a),lp(x,y,u,o0,zr,a),lp(x,y,u,o1+.10,zr,a),lp(x,y,u+s*hw,o1+.10,ze,a)],[(0,1,2,3),(3,2,1,0)],roof)
 sl=(zr-ze)/hw
 tri=[lp(x,y,u-hw+.20,o1-.02,ze+.20*sl-.05,a),lp(x,y,u+hw-.20,o1-.02,ze+.20*sl-.05,a),lp(x,y,u,o1-.02,zr-.10,a)]
 m.faces(tri,[(0,1,2),(2,1,0)],M['Red'])
 town_path(m,[lp(x,y,u-hw+.05,o1+.06,ze+.05*sl-.06,a),lp(x,y,u,o1+.06,zr-.06,a),lp(x,y,u+hw-.05,o1+.06,ze+.05*sl-.06,a)],.05,WF)
 facade_box(m,x,y,u,o1-.02,ze+.20*sl-.10,w-.30,.10,.12,WF,a)
 for s in (-1,1):
  uu=u+s*(hw-.22)
  town_rod(m,lp(x,y,uu,o0,ze+.20*sl-.10,a),lp(x,y,uu,o1-.02,ze+.20*sl-.10,a),.05,WF,6)
  town_rod(m,lp(x,y,uu,o0,ze-.75,a),lp(x,y,uu,o1-.25,ze+.20*sl-.12,a),.045,WF,6)
def door99(m,x,y,u,b,w,h,a,ma,side=0.0):
 # Door leaf (with an optional glazed side light) in a white frame and surround.
 # The side light stands on the south side of the leaf (90859849).
 dw=w-side
 facade_box(m,x,y,u+side/2,.12,b+h/2,dw,.06,h,ma,a)
 if side:facade_box(m,x,y,u-w/2+side/2,.10,b+h/2,side,.02,h,GLAZE,a);facade_box(m,x,y,u-w/2+side,.16,b+h/2,.06,.08,h,WF,a)
 facade_box(m,x,y,u+side/2,.15,b+h*.62,dw*.30,.02,h*.50,GLAZE,a)
 surround36(m,x,y,u,b,w,h,a,WF,.10,.40)
def steps99(m,x,y,u,w,top,a):
 n=max(1,round(top/.17))
 for k in range(n):facade_box(m,x,y,u,.36+.30*(n-k)/2,(k+.5)*top/n,w,.30*(n-k),top/n,M['Step'],a)
 for s in (-1,1):
  uu=u+s*(w/2-.05)
  town_rod(m,lp(x,y,uu,.40+.30*n,.90,a),lp(x,y,uu,.45,top+.90,a),.025,M['Iron'],6)
  for k in (0,n):town_rod(m,lp(x,y,uu,.42+.30*k,top*(1-k/n),a),lp(x,y,uu,.42+.30*k,top*(1-k/n)+.90,a),.022,M['Iron'],6)

# The houses, south to north. Positions are s (m) from the south end of each house's OSM front,
# measured on the facade plane in the resected panoramas (references/block99-notes.md).
# wide: the four-light windows over each other on the south side (centre, width); small: the
# two-light upper window on the north side; door: centre, width (with side light), leaf colour;
# porch: centre and roof colour; strip: the white board on 90859885's front.
ZB,ZU,WH=1.97,4.47,1.43             # window bottoms (ground, upper) and height
DB,DH=.65,2.10                      # door threshold and height
PZ=.55                              # dark plinth
HOUSES=[
 ('h85','90859885',dict(wide=(2.40,3.00),small=(5.70,1.50),door=(5.75,1.10,'DoorOak',0.0),porch=(5.85,'PorchTile'),strip=4.25)),
 ('h37','90859837',dict(wide=(2.33,2.76),small=(5.70,1.43),door=(5.85,1.00,'DoorWood',0.0),porch=(6.00,'PorchDark'))),
 ('h49','90859849',dict(wide=(1.80,2.70),small=(5.15,1.40),door=(5.15,1.30,'DoorWhite',.30),porch=(5.30,'PorchBrown'))),
 ('h98','90859898',dict(wide=(1.95,2.65),small=(5.27,1.37),door=(5.45,1.00,'DoorDark',0.0),porch=(5.70,'PorchBrown'))),
]
PW,PD,PE,PR=3.00,1.15,2.85,3.75     # porch roof width, depth, eaves and ridge heights
RE=M['Red']
for zone,osm,h in HOUSES:
 m=b99_new(Z[zone]['mesh'],'Kvarnholmen/Landshövdingegatan');H=Z[zone]['height'];T=Z[zone]['top']
 front=[w for w in walls(zone) if w['kind']=='outer' and abs(w['p'][0]-w['q'][0])<1 and w['p'][0]>290][0]
 F=fr99(tuple(front['p']),tuple(front['q']))
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],RE);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if w is not front:
   plain(m,w,H,RE,WF,WF,2,.9);continue
  S=lambda s:U(w,*P99(F,s))
  wc,ww=h['wide'];sc,sw=h['small'];dc,dw,dm,side=h['door']
  ops=[(S(wc),ZB,ww,WH,4),(S(wc),ZU,ww,WH,4),(S(sc),ZU,sw,WH,2)]
  holes=[(u,b,w_,hh,0) for u,b,w_,hh,n in ops]+[(S(dc),DB,dw,DH,0)]
  bz_wall(m,w['p'],w['q'],0,H,holes,RE);boards82(m,x,y,L,a,PZ+.02,H-.08,holes,RE)
  for u,b,w_,hh,n in ops:win99(m,x,y,u,b,w_,hh,a,n)
  door99(m,x,y,S(dc),DB,dw,DH,a,M[dm],side);steps99(m,x,y,S(dc),dw+.40,DB,a)
  pc,pm=h['porch'];porch99(m,x,y,S(pc),a,PW,PD,PE,PR,M[pm])
  if 'strip' in h:facade_box(m,x,y,S(h['strip']),.41,(PR+.1+H-.25)/2,.14,.06,H-.25-PR-.1,WF,a)
  facade_box(m,x,y,0,.39,PZ/2,L+.02,.08,PZ,M['Plinth'],a)
  for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+PZ)/2,.16,.10,H-PZ,WF,a)
 sL,sR,sm,tface,sl=gable99(m,F,zone,RE,M['Roof'],M['Sheet'])
 gable_boards99(m,F,sL,sR,sm,H,T,tface,[],RE)
 b99_finish(m,osm)

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block99_cameras=[
 sv_camera('481_Block99_Cal_RowSouth',304.36,112.65,2.30,245,15,90),
 sv_camera('482_Block99_Cal_RowNorth',304.80,122.37,2.30,245,15,90),
 sv_camera('483_Block99_Cal_SouthEast',312.0,98.0,1.80,290,8,60),
 sv_camera('484_Block99_Cal_NorthEast',312.0,136.0,1.80,194,8,60),
 ('485_Block99_Aerial',(325.0,95.0,32.0),(288.0,117.0,2.0),28),
]
print('BLOCK99_GEOMETRY',len(block99_names),'dropped',block99_dropped,block99_samples)
