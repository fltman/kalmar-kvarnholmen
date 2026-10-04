"""Pass 101: the west side of Östra Vallgatan south of the gate (house numbers 7-9), from south to north:
- 93238179 (7): the light grey rendered two-storey house on a black plinth, dark red casements in
  pale surrounds (door and two windows below, three windows above), black downpipes, a black roof
  edge and a railing round its low roof, two chimneys; on the south 3.8 m of the same OSM way, a
  grey boarded shed under a lean-to roof rising to the house;
- 93238159: the yellow boarded cottage with its gable to the street, one window with dark frames
  and a flower box, white corner and verge boards, red tiled roof;
- 93238211: the sage green boarded cottage, gable to the street, a tall window with dark red frames
  and a flower box;
- 93238209: the low yellow boarded cottage, gable to the street, a window and an attic vent, and
  the brown boarded gate between it and the grey cottage 93238202 (pass 100).

References: Google Street View (two panoramas on Östra Vallgatan, resected on house corners), view
only. Zones: source/block101.json; see references/block101-notes.md. Bicycles, plants, the lamp
post, signs and cars are omitted; so is the boarded fence south of the OSM way.
"""
B101D=json.loads((R/'source/block101.json').read_text());Z=B101D['zones']
block101_names=[];B101={}
for old in [k for k in list(materials) if k.startswith('M_Block101_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Render','TownPaintWhite',(.78,.78,.76),.85,0),('Surround','TownPaintWhite',(.88,.87,.83),.70,0),('WinRed','TownPaintBrown',(.42,.13,.10),.60,0),
 ('Door','TownPaintGreen',(.22,.24,.21),.60,0),('Plinth','TownStone',(.13,.13,.13),.90,0),('Black','TownMetalGrey',(.10,.10,.11),.55,.30),
 ('Boards','TownPaintWhite',(.60,.61,.60),.85,0),('Yellow','TownIvory',(.86,.68,.32),.80,0),('Green','TownPaintGreen',(.50,.62,.50),.75,0),
 ('White','TownPaintWhite',(.93,.93,.90),.55,0),('WinDark','TownPaintGreen',(.16,.22,.19),.60,0),('WinPlum','TownPaintBrown',(.38,.12,.15),.60,0),
 ('Tile','TownTileRed',(.78,.42,.27),.80,0),('Gate','TownStone',(.30,.20,.16),.85,0),('Stone','TownStone',(.45,.45,.44),.90,0),
 ('Chimney','TownStone',(.15,.15,.15),.85,0),('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),
 ('Flowers','TownPaintGreen',(.30,.45,.25),.80,0),
 ]:
 name='M_Block101_'+key;B101[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block101_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
# chimney82 and the earlier helpers read the global M (they need 'Dark').
M=B101;WF=M['White']

def b101_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block101_names.append(name);return Mesh(name,category)
def drop_degenerate_faces101(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block101_dropped={};block101_samples={}
def b101_finish(m,osm):
 obj=s21_finish(m)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 block101_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),6),len(f.verts)) for f in bm.faces if f.calc_area()<1e-9 or (max(e.calc_length() for e in f.edges)>0 and 2*f.calc_area()/max(e.calc_length() for e in f.edges)<1e-4)][:4]
 bm.free();block101_dropped[obj.name]=drop_degenerate_faces101(obj)
 obj['detail_pass']=101;obj['reference_notes']='references/block101-notes.md';obj['osm_way']=osm;return obj

def pt101(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
# Street frames for the gable fronts (as passes 99-100): s along the OSM front from A (south) to B
# (north), t outwards (east, to the right of A->B); the facade surfaces stand at t = 0.355.
def fr101(A,B):
 L=math.dist(A,B);D=((B[0]-A[0])/L,(B[1]-A[1])/L);return dict(A=A,B=B,D=D,N=(D[1],-D[0]),L=L,ang=math.atan2(D[1],D[0]))
def P101(f,s,t=0,z=None):
 p=(f['A'][0]+f['D'][0]*s+f['N'][0]*t,f['A'][1]+f['D'][1]*s+f['N'][1]*t);return p if z is None else (*p,z)
def rect101(f,zone):
 pts=[v for g in Z[zone]['polygons'] for v in g];A,D,N=f['A'],f['D'],f['N']
 ss=[(v[0]-A[0])*D[0]+(v[1]-A[1])*D[1] for v in pts];ts=[(v[0]-A[0])*N[0]+(v[1]-A[1])*N[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism101(m,f,outline,t0,t1,ma):
 n=len(outline);vs=[P101(f,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def gable101(m,f,zone,wall,roof,trim,ov=.30,eave=.30):
 # Saddle roof with its ridge running back from the street over the boxed outline; gable prisms in
 # the wall material at the street front and at the back, verge boards, gutters.
 s0,s1,t0,t1=rect101(f,zone)
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P101(f,e,tb,ze+.12),P101(f,sm,tb,T+.12),P101(f,sm,tf,T+.12),P101(f,e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P101(f,e,tb,ze+.02),P101(f,e,tf,ze+.02),.06,M['Sheet'],8)
  for tt in (tf-.03,tb+.03):town_path(m,[P101(f,e,tt,ze+.06),P101(f,sm,tt,T+.06)],.08,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism101(m,f,g,t1+.005,t1+o,wall);prism101(m,f,g,t0-o,t0-.005,wall)
 return sL,sR,sm,t1+o,sl
def gable_boards101(m,f,sL,sR,sm,H,T,tface,ma,step=.22):
 # Vertical boards on the street gable, clipped to the rakes.
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.14
  if z1-H>.06:m.box(P101(f,s,tface+.02,(H+z1)/2),(.035,.03,z1-H),ma,f['ang'])
def win101(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.10):
 # Casement in its frame, a flat surround and a sill.
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def flowers101(m,x,y,u,b,w,a,box_ma,fl):
 facade_box(m,x,y,u,.60,b-.16,w+.10,.30,.18,box_ma,a);facade_box(m,x,y,u,.60,b-.03,w,.24,.10,fl,a)
def fronts101(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, unseen outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if test(ox,oy,x,y):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
EAST=lambda ox,oy,x,y:ox>.9 and x>385.5

# ---- 93238179 (7): the grey rendered house (s from the south end of the OSM front).
m=b101_new(Z['g179']['mesh'],'Kvarnholmen/Östra Vallgatan');RD=M['Render'];SU=M['Surround'];WR=M['WinRed']
A9,B9=(386.378,16.223),(386.645,26.728);H=Z['g179']['height']
for w in fronts101(m,'g179',EAST,RD,WR,SU,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt101(A9,B9,s))
 ops=[(S(7.61),.93,1.10,1.17),(S(9.37),.93,1.15,1.17),(S(5.25),3.00,1.03,1.57),(S(7.65),3.00,1.10,1.57),(S(9.39),3.00,1.15,1.57)]
 du=S(5.25);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(du,.25,1.55,1.87,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,RD)
 for u,b,ww,hh in ops:win101(m,x,y,u,b,ww,hh,a,WR,SU,3,bw=.13)
 # The double door: two dark panelled leaves (the photo has the right one open), a pale surround.
 facade_box(m,x,y,du,.12,.25+1.87/2,1.55,.07,1.87,M['Door'],a)
 for s_ in (-1,1):facade_box(m,x,y,du+s_*.39,.17,.25+1.87*.62,.50,.03,.85,M['Door'],a);facade_box(m,x,y,du+s_*.39,.17,.25+1.87*.20,.50,.03,.45,M['Door'],a)
 facade_box(m,x,y,du,.17,.25+1.87/2,.03,.03,1.87,M['Dark'],a);surround36(m,x,y,du,.25,1.55,1.87,a,SU,.13,.40)
 facade_box(m,x,y,du,.55,.12,1.75,.40,.25,M['Stone'],a)
 facade_box(m,x,y,0,.39,.21,L+.02,.08,.42,M['Plinth'],a)
 # Pale frieze under the black roof edge, downpipes at both corners.
 facade_box(m,x,y,0,.40,H-.20,L+.04,.06,.30,SU,a)
 for uu in (-L/2+.12,L/2-.12):town_rod(m,lp(x,y,uu,.50,.30,a),lp(x,y,uu,.50,H-.05,a),.05,M['Black'],8)
r,sl=hip82(m,'g179',A9,B9,M['Black'])
# The railing round the roof edge: a top rail at 6.19 m on posts, inside the eave ring.
ring=ring_offset(r,.10);n=len(ring)
for i in range(n):
 p,q=ring[i],ring[(i+1)%n];town_rod(m,(*p,6.19),(*q,6.19),.025,M['Black'],6)
 k=max(1,int(math.dist(p,q)/1.6))
 for j in range(k):
  t=j/k;X,Y=p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t;town_rod(m,(X,Y,H+.08),(X,Y,6.19),.02,M['Black'],6)
for s in (5.2,7.5):X,Y=pt101(A9,B9,s);chimney82(m,X-1.2,Y,H,7.05,M['Chimney'])
# The boarded shed on the south 3.85 m: walls to the lean-to roof, which rises from 3.40 m at the
# south end to 3.90 m at the house.
ZS=lambda X,Y:3.40+.50*max(0.0,min(1.0,((X-A9[0])*(B9[0]-A9[0])+(Y-A9[1])*(B9[1]-A9[1]))/math.dist(A9,B9)/3.85))
BO=M['Boards']
for w in walls('g179s','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);up=U(w,*w['p']);uq=U(w,*w['q']);zp=ZS(*w['p']);zq=ZS(*w['q'])
 bz_wall(m,w['p'],w['q'],0,3.40,[],BO)
 if max(zp,zq)>3.42:
  pts=[(up,3.40),(uq,3.40)]+([(uq,zq)] if zq>3.42 else [])+([(up,zp)] if zp>3.42 else [])
  k=len(pts);vs=[lp(x,y,u_,o,z_,a) for o in (.005,.355) for u_,z_ in pts]
  m.faces(vs,[tuple(range(k-1,-1,-1)),tuple(range(k,2*k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)],BO)
 boards82(m,x,y,L,a,.10,min(zp,zq)-.10,[],BO)
sr=ring_offset([tuple(v) for v in Z['g179s']['polygons'][0]],.30)
m.faces([(*v,ZS(*v)+.05) for v in sr],[tuple(range(len(sr))),tuple(range(len(sr)-1,-1,-1))],M['Sheet'])
b101_finish(m,'93238179')

# ---- The three gable cottages (s from the south end of each OSM front).
def cottage101(zone,A,B,wall,frame,wins,vent=None,plinth=.25):
 m=b101_new(Z[zone]['mesh'],'Kvarnholmen/Östra Vallgatan');H=Z[zone]['height'];T=Z[zone]['top'];F=fr101(A,B)
 for w in fronts101(m,zone,EAST,wall,WF,WF,1,.8):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt101(A,B,s))
  holes=[(S(s),b,ww,hh,0) for s,b,ww,hh,fl in wins]
  bz_wall(m,w['p'],w['q'],0,H,holes,wall);boards82(m,x,y,L,a,plinth+.02,H-.08,holes,wall)
  for s,b,ww,hh,fl in wins:
   win101(m,x,y,S(s),b,ww,hh,a,frame,WF,2,bw=.09)
   if fl:flowers101(m,x,y,S(s),b,ww,a,WF,M['Flowers'])
  facade_box(m,x,y,0,.39,plinth/2,L+.02,.08,plinth,M['Plinth'],a)
  for uu in (-L/2+.07,L/2-.07):facade_box(m,x,y,uu,.42,(H+plinth)/2,.14,.10,H-plinth,WF,a)
 sL,sR,sm,tface,sl=gable101(m,F,zone,wall,M['Tile'],WF);gable_boards101(m,F,sL,sR,sm,H,T,tface,wall)
 if vent:
  s,b,ww,hh=vent;facade_box(m,*P101(F,s,tface+.02)[:2],0,0,b+hh/2,ww,.02,hh,GLAZE,F['ang'])
  surround36(m,*P101(F,s,tface-.355)[:2],0,b,ww,hh,F['ang'],WF,.07,.40)
 return m,F,tface
YE=M['Yellow']
m,F,tf=cottage101('y159',(385.937,27.739),(385.945,32.181),YE,M['WinDark'],[(2.20,.85,1.00,1.20,True)]);b101_finish(m,'93238159')
m,F,tf=cottage101('g211',(386.091,34.175),(386.492,37.837),M['Green'],M['WinPlum'],[(1.95,.74,.95,1.45,True)]);b101_finish(m,'93238211')
m,F,tf=cottage101('y209',(386.354,38.795),(386.811,43.363),YE,M['WinDark'],[(2.30,.47,1.05,1.30,False)],vent=(2.40,2.27,.45,.55))
# The brown boarded gate across the 1.5 m gap to 93238202, on the street line.
gp,gq=(386.811,43.363),(387.278,44.83);x,y,L,a=sf_edge(gp,gq)
facade_box(m,x,y,0,.30,.85,L,.06,1.70,M['Gate'],a)
for k in range(1,7):facade_box(m,x,y,-L/2+k*L/7,.34,.85,.04,.03,1.66,M['Gate'],a)
facade_box(m,x,y,0,.34,1.72,L+.04,.10,.06,M['Gate'],a)
b101_finish(m,'93238209')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block101_cameras=[
 sv_camera('494_Block101_Cal_Grey',394.11,22.50,2.05,243,15,90),
 sv_camera('495_Block101_Cal_Cottages',395.01,42.20,2.05,243,15,90),
 sv_camera('496_Block101_Cal_Row',395.01,42.20,2.54,222,15,90),
 ('497_Block101_Aerial',(410.0,30.0,26.0),(382.0,30.0,2.0),28),
]
print('BLOCK101_GEOMETRY',len(block101_names),'dropped',block101_dropped,block101_samples)
