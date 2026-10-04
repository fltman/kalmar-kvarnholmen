"""Pass 103: rebuilds the prison building of pass 85 (SM_Prison85_Anstalten) as the cross-shaped cell
prison that satellite imagery and the winter photograph from the Västerport bridge show (view only):
- the main cell range: three storeys of pale cream render over a grey plinth, rows of small windows
  in dark frames, a cornice band, a low saddle roof in dark grey sheet with hipped ends, a row of
  chimneys along the ridge, roof hatches on the west slope and long roof lights on the east slope;
- the taller cross wing to the east: its gable end on the east is a pediment over a cornice, with a
  chimney at the apex, a small pair of windows in the tympanum, a row of seven tall round-headed
  windows high up and the single entrance door in a stone surround; side walls with three rows of
  windows; its saddle roof runs across the main range;
- the low flat-roofed annexes in the corner south of the cross wing;
- the modern flat-roofed range at the north end, grey render with a white parapet.
Data: source/block103.json; see references/block103-notes.md. This deliberately changes the pass 85
mesh SM_Prison85_Anstalten; the other pass 85 meshes (ground, walls, Rotunda) are untouched.
"""
B103D=json.loads((R/'source/block103.json').read_text());block103_names=[];B103={}
for old in [k for k in list(materials) if k.startswith('M_Block103_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.90,.84,.63),.90,0),('Trim','TownPaintWhite',(.93,.90,.80),.60,0),('Plinth','TownStone',(.60,.59,.57),.90,0),
 ('Frame','TownMetalGrey',(.22,.22,.23),.55,.10),('Door','TownPaintBrown',(.45,.32,.22),.60,0),('Roof','TownMetalGrey',(.30,.31,.33),.55,.30),
 ('RoofLight','TownMetalGrey',(.62,.64,.66),.30,.40),('Hatch','TownMetalGrey',(.10,.10,.11),.45,.30),('Chimney','TownStone',(.30,.29,.29),.85,0),
 ('Grey','TownIvory',(.66,.66,.64),.88,0),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block103_'+key;B103[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block103_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M103=B103
def drop_degenerate_faces103(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
F103=B103D['frame'];O103=tuple(F103['origin']);D103=tuple(F103['along']);N103=tuple(F103['across']);LV=B103D['levels'];Z103=0.30
def X103(s,t):return (O103[0]+D103[0]*s+N103[0]*t,O103[1]+D103[1]*s+N103[1]*t)
def ccw103(pts):
 a=sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))
 return pts if a>0 else pts[::-1]
def facade103(m,p,q,z0,H,rows,bay,ww,hh,wm,skip=()):
 # One wall with rows of small windows (bottoms in rows) at the given bay width, a plinth, a
 # cornice band at the eaves; skip lists (u0,u1) spans kept blank.
 x,y,L,a=sf_edge(p,q);n=max(1,int(L/bay));holes=[]
 for k in range(n):
  u=-L/2+(k+.5)*L/n
  if any(s0<=u<=s1 for s0,s1 in skip) or abs(u)>L/2-.8:continue
  for b in rows:holes.append((u,z0+b,ww,hh,0))
 bz_wall(m,p,q,z0-.3,z0+H,holes,wm)
 for u,b,w_,h_,r in holes:
  facade_box(m,x,y,u,.16,b+h_/2,w_,.02,h_,GLAZE,a)
  for q_ in (-w_/2+.04,w_/2-.04,0):facade_box(m,x,y,u+q_,.20,b+h_/2,.07,.06,h_,M103['Frame'],a)
  for zz in (b+.04,b+h_-.04,b+h_*.55):facade_box(m,x,y,u,.20,zz,w_,.05,.06,M103['Frame'],a)
  facade_box(m,x,y,u,.44,b-.06,w_+.24,.16,.08,M103['Trim'],a);surround36(m,x,y,u,b,w_,h_,a,M103['Trim'],.10,.40)
 facade_box(m,x,y,0,.40,z0+.45,L,.10,.90,M103['Plinth'],a)
 facade_box(m,x,y,0,.46,z0+H-.25,L+.1,.20,.50,M103['Trim'],a)
 for uu in (-L/2+.2,L/2-.2):facade_box(m,x,y,uu,.42,z0+H/2,.40,.08,H,M103['Trim'],a)
 return x,y,L,a
old=bpy.data.objects.get('SM_Prison85_Anstalten')
if old:bpy.data.objects.remove(old,do_unlink=True)
m=Mesh('SM_Prison85_Anstalten','Anstalten Kalmar/Buildings');block103_names.append('SM_Prison85_Anstalten')
MA,WG=B103D['main'],B103D['wing']
He,Hr=LV['main_eaves'],LV['main_ridge'];We,Wa=LV['wing_eaves'],LV['wing_apex']
ROWS=(1.5,4.8,8.0);BAY=3.1
# ---------------------------------------------------------------- main range walls
s0,s1,t0,t1=MA['s0'],MA['s1'],MA['t0'],MA['t1']
corners=ccw103([X103(s0,t0),X103(s1,t0),X103(s1,t1),X103(s0,t1)])
for p,q in zip(corners,corners[1:]+corners[:1]):
 # Skip the east face where the cross wing meets it (s 20-32.5 at t 13).
 mid=((p[0]+q[0])/2,(p[1]+q[1])/2)
 sm=(mid[0]-O103[0])*D103[0]+(mid[1]-O103[1])*D103[1];tm=(mid[0]-O103[0])*N103[0]+(mid[1]-O103[1])*N103[1]
 if abs(tm-t1)<.5:
  # East face in two runs either side of the wing.
  for a_,b_ in ((s0,WG['s0']),(WG['s1'],s1)):
   # Order the ends so the wall's outward normal points east (+t).
   P0,P1=X103(a_,t1),X103(b_,t1);x_,y_,L_,ang=sf_edge(P0,P1);ox,oy=math.sin(ang),-math.cos(ang)
   if ox*N103[0]+oy*N103[1]<0:P0,P1=P1,P0
   facade103(m,P0,P1,Z103,He,ROWS,BAY,1.0,1.25,M103['Cream'])
 else:
  facade103(m,p,q,Z103,He,ROWS,BAY,1.0,1.25,M103['Cream'])
# Main roof: low saddle with hipped ends, over the boxed range with a 0.45 m overhang.
inset_roof(m,corners,Z103+He,(t1-t0)/2-.30,Hr-He,M103['Roof'],.45)
rise=(Hr-He)/((t1-t0)/2-.30+.45)
for k in range(9):
 s=s0+4.5+k*(s1-s0-9)/8
 if WG['s0']-1<s<WG['s1']+1:continue
 cx,cy=X103(s,(t0+t1)/2);box(m,cx,cy,.7,.9,1.5,Z103+Hr-.4,M103['Chimney'],math.atan2(D103[1],D103[0]),M103['Dark'])
 # A roof hatch on the west slope and a roof light on the east slope beside each chimney bay.
 hx,hy=X103(s,t0+2.6);box(m,hx,hy,.8,.8,.35,Z103+He+(2.6+.45)*rise-.1,M103['Hatch'],math.atan2(D103[1],D103[0]))
 lx,ly=X103(s,t1-2.8);box(m,lx,ly,2.6,1.1,.12,Z103+He+(2.8+.45)*rise-.02,M103['RoofLight'],math.atan2(D103[1],D103[0]))
# ---------------------------------------------------------------- the cross wing
ws0,ws1,wt1=WG['s0'],WG['s1'],WG['t1']
# Side walls (north and south) from the main range's east face out to the gable, then the gable.
for sa,flip in ((ws0,True),(ws1,False)):
 P0,P1=X103(sa,t1),X103(sa,wt1);x_,y_,L_,ang=sf_edge(P0,P1);ox,oy=math.sin(ang),-math.cos(ang)
 want=(-D103[0],-D103[1]) if sa==ws0 else D103
 if ox*want[0]+oy*want[1]<0:P0,P1=P1,P0
 facade103(m,P0,P1,Z103,We,ROWS+(11.0,),BAY,1.0,1.25,M103['Cream'])
# Above the main roof, the wing's side walls continue across the main range to its west face.
for sa in (ws0,ws1):
 P0,P1=X103(sa,t0),X103(sa,t1);bz_wall(m,P0,P1,Z103+He,Z103+We,[],M103['Cream'])
P0,P1=X103(ws0,t0),X103(ws1,t0);bz_wall(m,P0,P1,Z103+He,Z103+We,[],M103['Cream'])
# East gable face.
G0,G1=X103(ws0,wt1),X103(ws1,wt1);x,y,L,a=sf_edge(G0,G1);ox,oy=math.sin(a),-math.cos(a)
if ox*N103[0]+oy*N103[1]<0:G0,G1=G1,G0;x,y,L,a=sf_edge(G0,G1)
arched=[(-L/2+1.6+k*(L-3.2)/6,10.0,.60,2.3,.30) for k in range(7)]
door=(0,0,1.6,3.2,.8)
bz_wall(m,G0,G1,Z103-.3,Z103+We,[(u,Z103+b,w_,h_,r) for u,b,w_,h_,r in arched]+[(0,Z103,1.6,3.2,.8)],M103['Cream'])
for u,b,w_,h_,r in arched:
 facade_box(m,x,y,u,.16,Z103+b+(h_-r)/2,w_,.02,h_-r,GLAZE,a)
 p18_arch(m,x,y,Z103+b+h_-r,w_,r,.10,.40,a,M103['Trim'])
 facade_box(m,x,y,u,.42,Z103+b-.05,w_+.2,.14,.08,M103['Trim'],a)
facade_box(m,x,y,0,.12,Z103+1.2,1.6,.06,2.4,M103['Door'],a);p18_arch(m,x,y,Z103+2.4,1.6,.8,.35,.48,a,M103['Plinth'])
for s_ in (-1,1):facade_box(m,x,y,s_*1.05,.46,Z103+1.2,.5,.16,2.4,M103['Plinth'],a)
facade_box(m,x,y,0,.40,Z103+.45,L,.10,.90,M103['Plinth'],a)
for uu in (-L/2+.25,L/2-.25):facade_box(m,x,y,uu,.44,Z103+We/2,.50,.10,We,M103['Trim'],a)
# Pediment: cornice across the gable at the eaves, tympanum, raking cornices, the window pair.
facade_box(m,x,y,0,.55,Z103+We+.1,L+.5,.40,.35,M103['Trim'],a)
for o_ in (.005,.36):m.faces([lp(x,y,-L/2,o_,Z103+We+.25,a),lp(x,y,L/2,o_,Z103+We+.25,a),lp(x,y,0,o_,Z103+Wa,a)],[(0,1,2),(2,1,0)],M103['Cream'])
for s_ in (-1,1):town_path(m,[lp(x,y,s_*(L/2+.2),.55,Z103+We+.3,a),lp(x,y,0,.55,Z103+Wa+.12,a)],.16,M103['Trim'])
for s_ in (-.45,.45):facade_box(m,x,y,s_,.37,Z103+We+1.7,.55,.02,1.0,GLAZE,a);facade_box(m,x,y,s_,.40,Z103+We+1.7,.65,.06,1.1,M103['Frame'],a)
# Wing roof: saddle across the main range from its west face to the east gable, gable at both ends.
ov=.45;half=(ws1-ws0)/2;sl=(Wa-We)/half;sm=(ws0+ws1)/2
for sa in (ws0-ov,ws1+ov):
 q=[(*X103(sa,t0-ov),Z103+We-ov*sl),(*X103(sm,t0-ov),Z103+Wa),(*X103(sm,wt1+ov),Z103+Wa),(*X103(sa,wt1+ov),Z103+We-ov*sl)]
 m.faces(q,[(0,1,2,3),(3,2,1,0)],M103['Roof'])
W0,W1=X103(ws0,t0),X103(ws1,t0)
for o_ in (.005,.36):m.faces([(*W0,Z103+We),(*W1,Z103+We),(*X103(sm,t0),Z103+Wa)],[(0,1,2),(2,1,0)],M103['Cream'])
cx,cy=X103(sm,wt1-.6);box(m,cx,cy,.8,.8,1.6,Z103+Wa-.6,M103['Chimney'],math.atan2(D103[1],D103[0]),M103['Dark'])
# ---------------------------------------------------------------- annexes and the north range
for g in B103D['annex']:
 ring=[tuple(v) for v in g];H=LV['annex']
 for p,q in zip(ring,ring[1:]+ring[:1]):
  if math.dist(p,q)<.3:continue
  w={'p':list(p),'q':list(q),'z0':0.0};x,y,L,a=sf_edge(p,q)
  if L<2.5:bz_wall(m,p,q,Z103-.3,Z103+H,[],M103['Cream']);continue
  plain(m,w,Z103+H,M103['Cream'],M103['Frame'],M103['Trim'],1,Z103+1.2)
  facade_box(m,x,y,0,.42,Z103+H+.15,L+.1,.20,.40,M103['Trim'],a)
 m.faces([(*v,Z103+H+.02) for v in ring],[tuple(range(len(ring))),tuple(range(len(ring)-1,-1,-1))],M103['Roof'])
for g in B103D['north']:
 ring=[tuple(v) for v in g];H=LV['north']
 for p,q in zip(ring,ring[1:]+ring[:1]):
  if math.dist(p,q)<.3:continue
  w={'p':list(p),'q':list(q),'z0':0.0};x,y,L,a=sf_edge(p,q)
  if L<2.5:bz_wall(m,p,q,Z103-.3,Z103+H,[],M103['Grey']);continue
  plain(m,w,Z103+H,M103['Grey'],M103['Frame'],M103['Trim'],2,Z103+1.0)
  facade_box(m,x,y,0,.30,Z103+H+.25,L+.1,.40,.50,M103['Trim'],a)
 m.faces([(*v,Z103+H+.02) for v in ring],[tuple(range(len(ring))),tuple(range(len(ring)-1,-1,-1))],M103['Dark'])
obj=s21_finish(m);obj['block103_dropped_faces']=drop_degenerate_faces103(obj)
obj['detail_pass']=103;obj['reference_notes']='references/block103-notes.md';obj['osm_way']='91053122'

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block103_cameras=[sv_camera('504_Block103_Cal_Bridge',-357.3,109.1,1.8,245,8,90),('505_Block103_Aerial',(-400.0,110.0,55.0),(-450.0,158.0,6.0),28)]
print('BLOCK103_GEOMETRY',len(block103_names),obj['block103_dropped_faces'])
