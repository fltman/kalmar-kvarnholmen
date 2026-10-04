"""Pass 116: the first Gamla stan pass on the mainland west of Kvarnholmen, Molinsgatan and the east
part of Västerlånggatan. Pass 98 built these 37 houses as plain volumes in its chunk meshes; each is now
its own mesh SM_Slott116_<osm id> with its real form: storeys, saddle, hipped or mansard (gambrel)
roofs in red tile, black tile or black sheet metal, vertical boarding or render in the house's colour,
white corner boards, eaves boards and window frames, windows per storey, a door on the street,
dormers, chimneys and the notable features:
- Molinsgatan 6, the red boarded two-storey house with its gable on the street, the red cottage beside
  it and the low link with the entrance;
- the pale yellow one-storey gable house with carved bargeboards; the white gable house with red
  window frames; the long white range with dormers; the red houses with white trim on the south-west
  side, the dark brown corner house and the blue-grey house with the mansard roof;
- the grey-green rendered 1940s block with its raised ground floor, chimneys and glazed stair bays;
  the dark green corrugated store; the sage rendered house with the dormer balcony;
- on Västerlånggatan the pink villa with the carved glazed veranda, the yellow and white boarded
  houses, the light blue gable house, the cottage with the red garage door, the white gambrel
  outbuilding, the white rendered corner villa, the white rendered house with the black sheet-metal
  hipped roof (no. 12), the red villa with the central gable (no. 14) and the yellow house with the
  red arched dormer;
- houses seen in no photo get a plain Gamla stan form: boarded, the storeys from OSM, a tile saddle
  roof, the colour from their neighbours.
It also re-creates pass 98's chunk meshes the houses sit in with slott98_chunks115 (pass 115),
leaving out every house in SLOTT98_DETAILED.
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block116.json; see references/block116-notes.md.
"""
B116D=json.loads((R/'source/block116.json').read_text());Z116=B116D['zones'];HS116=B116D['houses'];G116=B116D['ground_z']
block116_names=[];B116={}
for old in [k for k in list(materials) if k.startswith('M_Block116_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownIvory',(.52,.18,.14),.85,0),('Yellow','TownIvory',(.87,.73,.40),.85,0),('PaleYellow','TownIvory',(.86,.82,.64),.85,0),
 ('White','TownPaintWhite',(.92,.92,.89),.80,0),('Pink','TownIvory',(.84,.62,.60),.85,0),('Blue','TownPaintWhite',(.64,.74,.83),.80,0),
 ('DarkBrown','TownPaintBrown',(.13,.10,.09),.80,0),('BlueGrey','TownPaintWhite',(.29,.32,.37),.80,0),('GreyGreen','TownIvory',(.60,.66,.62),.88,0),
 ('Sage','TownIvory',(.60,.66,.57),.88,0),('Cream','TownIvory',(.90,.85,.72),.88,0),('DarkGreen','TownPaintGreen',(.14,.24,.19),.70,.10),
 ('Grey','TownIvory',(.72,.72,.70),.88,0),('Ochre','TownIvory',(.80,.64,.36),.85,0),('RedRender','TownIvory',(.62,.28,.21),.88,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('FrameRed','TownPaintBrown',(.46,.16,.12),.60,0),('FrameOchre','TownIvory',(.80,.70,.48),.60,0),
 ('Tile','TownTileRed',(.66,.32,.22),.80,0),('TileDark','TownTileRed',(.17,.16,.16),.80,0),('RoofBlack','TownMetalGrey',(.09,.09,.10),.45,.40),
 ('RoofDark','TownMetalGrey',(.22,.22,.24),.60,.25),('RoofSlate','TownMetalGrey',(.30,.31,.33),.55,.30),('RoofGrey','TownMetalGrey',(.42,.42,.42),.70,.15),
 ('Door','TownPaintBrown',(.30,.21,.15),.70,0),('DoorWood','TownPaintBrown',(.56,.38,.22),.70,0),('GarageRed','TownPaintBrown',(.62,.13,.10),.60,0),
 ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Chimney','TownTileRed',(.55,.28,.22),.90,0),
 ('ChimneyWhite','TownIvory',(.86,.85,.81),.88,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
 ]:
 name='M_Block116_'+key;B116[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block116_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M116=B116
def b116_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block116_names.append(name);return Mesh(name,category)
def drop_degenerate_faces116(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b116_finish(m,osm):
 obj=s21_finish(m);obj['block116_dropped_faces']=drop_degenerate_faces116(obj);print('BLOCK116_DROPPED',m.name,obj['block116_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=116;obj['reference_notes']='references/block116-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without these houses
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|set(B116D['ids'])
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in B116D['ids']},116,block116_names)
# slott98_chunks115 finishes the chunks with pass 115's finisher (detail_pass 98, rebuilt_by_pass 116).

# ---------------------------------------------------------------- helpers
G=G116
def zabs116(h):return G+h
def long_first116(r):
 # The rectangle's corners reordered so that r[0]->r[1] is a long side (counter-clockwise kept).
 r=[tuple(v) for v in r]
 return r if math.dist(r[0],r[1])>=math.dist(r[1],r[2])-.01 else r[1:]+r[:1]
def ends116(r):
 # The two short ends of a long-first rectangle, each (p, q, apex point on the ridge line, normal).
 p0,p1,p2,p3=r;L=math.dist(p0,p1);dx,dy=(p1[0]-p0[0])/L,(p1[1]-p0[1])/L
 mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 return ((p0,p3,mid(p0,p3),(-dx,-dy)),(p1,p2,mid(p1,p2),(dx,dy)))
def end_frame116(p,q,n):
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def gambrel116(m,r,H,T,ma,wall,ov=.35,verge=.30):
 # A Swedish mansard (gambrel) roof with gable ends: steep lower slopes from the eaves to the break,
 # 0.85 m in and 60 % of the rise up, then low upper slopes to the ridge; the gables in the wall
 # material as pentagons.
 p0,p1,p2,p3=r;L=math.dist(p0,p1);W=math.dist(p1,p2);d=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L);n=((p3[0]-p0[0])/W,(p3[1]-p0[1])/W)
 k=min(.85,W/4);ZB=H+(T-H)*.6;prof=[(-ov,H-ov*(ZB-H)/k),(0,H),(k,ZB),(W/2,T),(W-k,ZB),(W,H),(W+ov,H-ov*(ZB-H)/k)]
 P=lambda s,t,z:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t,z)
 seg=[(prof[0],prof[2]),(prof[2],prof[3]),(prof[3],prof[4]),(prof[4],prof[6])]
 for (t0,z0),(t1,z1) in seg:
  q=[P(-verge,t0,z0),P(L+verge,t0,z0),P(L+verge,t1,z1),P(-verge,t1,z1)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],ma);m.faces([(v[0],v[1],v[2]-.10) for v in q],[(0,1,2,3),(3,2,1,0)],ma)
 for s,sg in ((0,-1),(L,1)):
  pts=[P(s+sg*o,t,z) for o in (.005,.355) for t,z in prof[1:6]]
  m.faces(pts,[(0,1,2,3,4),(9,8,7,6,5),(0,5,6,1),(1,6,7,2),(2,7,8,3),(3,8,9,4),(4,9,5,0)],wall)
 return k,ZB
def flat116(m,polys,H,ma,trim):
 for g in polys:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.22,trim,a)
def carved116(m,p,q,c,n,H,T,ma,sl,k=9):
 # Carved bargeboards: a board along each rake with a row of short drops under it.
 o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
 for u_ in (p,q):
  e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
  town_rod(m,(*o(e,.55),H-.35*sl-.05),(*o(c,.55),T-.05),.08,ma,8)
  for i in range(1,k):
   t=i/k;px,py=e[0]+(c[0]-e[0])*t,e[1]+(c[1]-e[1])*t;zz=H-.35*sl+(T-H+.35*sl)*t
   m.box((*o((px,py),.55),zz-.20),(.06,.05,.22),ma,math.atan2(c[1]-e[1],c[0]-e[0]))
 town_rod(m,(*o(c,.55),T-.05),(*o(c,.55),T-.75),.05,ma,6)

def window116(m,x,y,u,b,w,h,a,st):
 # pass 115's window with this pass's materials: casement, surround, sill
 fr=M116[st.get('frame','Frame')];cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,fr,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a);facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,M116[st.get('sill','Frame')],a)
def door116(m,x,y,u,b,w,h,a,leaf,frame):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
 facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,leaf,a)
 if w>1.2:facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,frame,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,frame,a)

# ---------------------------------------------------------------- house styles
# rows: window rows (bottom, height, width) above the ground per storey count; doors are 1.0 x 2.1
# on the street wall of the main body.
def rows116(st,Hh,top):
 if Hh<2.9:return [(.9,.8,.8)]
 if st>=2:return [(.95,1.35,1.0),(max(Hh*.5+.75,Hh-1.85),1.25,1.0)]
 return [(.85,1.35 if Hh>3.2 else 1.15,1.0)]
CHIM116={'chimney','chimneys2','chimney_red'}
meshes={}
for zone,z in Z116.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b116_new(z['mesh'],'Slottsområdet/Gamla stan')
for zone,z in Z116.items():
 hs=HS116[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs116(Hh);T=zabs116(z['top'])
 wm=M116[z['wall']];fr=M116[hs.get('fr','Frame')];trim=M116['FrameRed'] if 'red_eaves' in hs.get('extras',[]) else (fr if z['boards'] else M116['Frame'])
 st=dict(frame=hs.get('fr','Frame'),sill=hs.get('fr','Frame'),surround=True)
 if z['wall']=='DarkBrown' or z['wall']=='BlueGrey' or z['wall']=='Red':st['frame']='Frame';st['sill']='Frame'
 rows=rows116(hs['st'] if z['role'] in ('main','wing') else 1,Hh,z['top']) if z['role']!='veranda' else []
 if hs.get('small_windows'):rows=[(2.2,.5,.9)]
 door=None
 if z['role']=='main' and z.get('street_wall') and 'no_door' not in hs.get('extras',[]):door=z['street_wall']
 if z['role']=='link' and z.get('street_wall'):door=z['street_wall']
 plinth=.35 if Hh>2.9 else .2
 if z['osm']=='93306345':plinth=1.2   # raised ground floor over a basement
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs116(w['z0'])
  if L<.25:continue
  holes=[];wins=[];mine=[]
  if w['kind']=='outer':
   if door and abs(w['p'][0]-door[0][0])<1e-6 and abs(w['p'][1]-door[0][1])<1e-6 and L>1.6:
    dw=1.4 if 'door_double' in hs.get('extras',[]) else 1.0;du=0.0 if L<6 else -L/2+min(L*.35,3.0)
    if 'garage_red' in hs.get('extras',[]) and L>4.5:mine.append(('garage',L/2-1.7,G+.05,2.4,2.1))
    mine.append(('door',du,G+plinth*.5,dw,2.15))
   bay=hs.get('bay',2.7 if hs['st']>=2 else 2.9);n=int(L/bay+.3)
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for b,hh,ww in rows:
     b=zabs116(b)
     if b<z0+.3 or b+hh>H-.25 or L<ww+1.0:continue
     if any(abs(u-du_)<(ww+dw_)/2+.30 and b<db+dh+.2 for _,du_,db,dw_,dh in mine):continue
     wins.append((u,b,ww,hh))
  holes=[(u,b,ww,hh,0) for u,b,ww,hh in wins]+[(du_,db,dw_,dh,0) for _,du_,db,dw_,dh in mine]
  bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if z['boards']:boards115(m,w,max(z0,G+plinth+.02),H-.12,holes,wm)
  for u,b,ww,hh in wins:window116(m,x,y,u,b,ww,hh,a,st)
  for kind,du_,db,dw_,dh in mine:
   if kind=='garage':
    facade_box(m,x,y,du_,.15,db+dh/2,dw_,.06,dh,M116['GarageRed'],a)
    for k in range(1,5):facade_box(m,x,y,du_,.19,db+k*dh/5,dw_-.1,.02,.03,M116['Frame'],a)
    surround36(m,x,y,du_,db,dw_,dh,a,M116['Frame'],.10,.40);continue
   leaf='DoorWood' if 'door_double' in hs.get('extras',[]) else ('Frame' if z['wall'] in ('Yellow','PaleYellow','Red') else 'Door')
   door116(m,x,y,du_,db,dw_,dh,a,M116[leaf],M116['Frame'])
   if db>G+.12:steps115(m,x,y,du_,dw_+.5,db,a,M116['Step'])
   if 'door_porch' in hs.get('extras',[]) and z['role']=='main':awning82(m,x,y,du_,db+dh+.15,dw_+1.0,a,M116['Tile'],.6,1.0)
  if w['kind']=='outer':facade_box(m,x,y,0,.40,(G+plinth)/2,L+.02,.10,G+plinth,M116['Stone'],a)
  if z['role']!='veranda':facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,trim,a)
  if z['boards']:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+plinth)/2,.20,.10,H-G-plinth,M116['Frame'] if z['wall']!='White' else M116['Frame'],a)

# ---------------------------------------------------------------- roofs and features
for zone,z in Z116.items():
 hs=HS116[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs116(Hh);T=zabs116(z['top']);ex=hs.get('extras',[]) if z['role']=='main' else []
 wm=M116[z['wall']];rm=M116[hs['rm']];fr=hs.get('fr','Frame')
 if z['role'] in ('annex','link','veranda') or z['roof']=='flat':
  if z['role']=='veranda':
   for w in z['walls']:
    if w['kind']!='outer':continue
    x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.30,H-.10,L+.2,.25,.25,M116['Frame'],a)
  flat116(m,z['polygons'],H,M116['RoofDark'] if z['role']!='annex' or hs['rm']!='Tile' else M116['RoofDark'],M116['Frame'] if z['boards'] else wm);continue
 r=long_first116(z['rect'])
 if hs.get('ridge')=='short' and z['role']=='main':r=r[1:]+r[:1]
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
 if z['roof'] in ('hip','low'):
  inset_roof(m,r,H,max(.3,min(Ls,Lt)/2-.30),T-H,rm,hs.get('ov',.45));sl=(T-H)/max(.5,min(Ls,Lt)/2)
 elif z['roof']=='gambrel':
  k,ZB=gambrel116(m,r,H,T,rm,wm)
  for p,q,c,n in ends116(r):
   x,y,L,a=end_frame116(p,q,n)
   if T-H>2.4:window116(m,x,y,0,H+.25,.8,min(1.1,ZB-H-.2),a,dict(frame=fr,sill=fr))
  sl=(ZB-H)/k
 else:
  eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40 if hs['st']>=1 else .30)
  for p,q,c,n in ends:
   x,y,L,a=end_frame116(p,q,n)
   if T-H>2.3 and L>3.0:
    gh=min(1.1,(T-H)*.45)
    if hs['st']>=1.5 and L>6.5:
     for s in (-.8,.8):window116(m,x,y,s,H+.35,.7,gh,a,dict(frame=fr,sill=fr))
    else:window116(m,x,y,0,H+.35,.75,gh,a,dict(frame=fr,sill=fr))
   if 'carved' in hs.get('extras',[]):carved116(m,p,q,c,n,H,T,M116['Frame'],sl)
   else:
    # plain white bargeboards
    o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
    for u_ in (p,q):
     e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
     town_rod(m,(*o(e,.48),H-.35*sl-.04),(*o(c,.48),T-.04),.06,M116['Frame'],6)
 # chimneys on the ridge
 cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;d_=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d_[1],d_[0])
 cm=M116['ChimneyWhite'] if z['wall'] in ('White','Cream','GreyGreen','Sage') and 'chimney_red' not in ex else M116['Chimney']
 if 'chimneys2' in ex:
  for s in (-Ls*.25,Ls*.25):chimney115(m,cx_+d_[0]*s,cy_+d_[1]*s,T-.6,T+.8,cm,ang)
 elif ex and set(ex)&CHIM116 or (z['role']=='main' and hs['st']>=1 and Hh>2.9 and not set(ex)&{'chimneys2'}):
  chimney115(m,cx_+d_[0]*Ls*.15,cy_+d_[1]*Ls*.15,T-.6,T+.7,cm,ang)
 # dormers on the street slope (or the first long side)
 if set(ex)&{'dormers','arched_dormer','dormer_balcony'} and z['roof']=='saddle':
  sw=z.get('street_wall');sides=[(r[0],r[1]),(r[2],r[3])]
  if sw:
   mx,my=(sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2;sides.sort(key=lambda pq:math.dist(((pq[0][0]+pq[1][0])/2,(pq[0][1]+pq[1][1])/2),(mx,my)))
  p,q=sides[0];x,y,L,a=sf_edge(p,q)
  nd=1 if 'arched_dormer' in ex or 'dormer_balcony' in ex else max(1,int(L/6))
  for k in range(nd):
   u=-L/2+(k+.5)*L/nd if nd>1 else 0.0
   if 'arched_dormer' in ex:
    dormer82(m,x,y,u,a,H,sl,1.5,.95,M116['Red'],M116['Frame'],M116['Red'],.7)
   else:dormer82(m,x,y,u,a,H,sl,1.6,1.0,wm,M116[fr] if fr in M116 else M116['Frame'],rm,.9)
   if 'dormer_balcony' in ex:
    facade_box(m,x,y,u,.9,H-.05,2.4,1.0,.15,M116['Stone'],a)
    town_rod(m,lp(x,y,u-1.2,1.35,H+.95,a),lp(x,y,u+1.2,1.35,H+.95,a),.03,M116['Iron'],6)
    for kk in range(13):town_rod(m,lp(x,y,u-1.2+kk*.2,1.35,H+.05,a),lp(x,y,u-1.2+kk*.2,1.35,H+.95,a),.012,M116['Iron'],4)
 # the central gable (frontispiece) on the street front
 if 'frontis' in ex and z.get('street_wall'):
  sw=z['street_wall'];x,y,L,a=sf_edge(*sw)
  frontis83(m,x,y,0,2.8,H,H+1.3,T-.3,a,wm,M116['Frame'],rm,True)
 # the glazed stair bays of the 1940s block on its street front
 if 'stair_bays' in ex and z.get('street_wall'):
  sw=z['street_wall'];x,y,L,a=sf_edge(*sw)
  for u in (-L*.30,L*.18):
   facade_box(m,x,y,u,.37,G+4.6,1.2,.02,4.6,GLAZE,a);cas81(m,x,y,u,G+2.3,1.2,4.6,a,M116['Frame'],.41,6)
 # the carved glazed veranda of the pink villa (the south-west corner, seen on v02_h358)
 if z['osm']=='93333644' and z['role']=='main':
  VP=(-745.0,107.6)  # the veranda's place, read on v02_h358: the side nearest it, centred on it
  p,q=min(zip(r,r[1:]+r[:1]),key=lambda pq:abs((VP[0]-pq[0][0])*(pq[1][1]-pq[0][1])-(VP[1]-pq[0][1])*(pq[1][0]-pq[0][0]))/math.dist(*pq))
  x,y,L,a=sf_edge(p,q);vw,vd,vh=3.2,2.2,3.1
  u0=max(-L/2+vw/2,min(L/2-vw/2,U({'p':p,'q':q},*VP)))
  # corner posts, front mullions, rails, glazing on the front and both sides over a boarded parapet
  for s in (-1,1):
   facade_box(m,x,y,u0+s*vw/2,.36+vd,G+vh/2,.14,.14,vh,M116['Frame'],a)
   facade_box(m,x,y,u0+s*vw/2,.36+vd/2,G+.95+(vh-1.3)/2,.02,vd-.1,vh-1.3,GLAZE,a)
   for zz in (G+.95,G+vh-.30):facade_box(m,x,y,u0+s*vw/2,.36+vd/2,zz,.10,vd,.08,M116['Frame'],a)
  for k in range(1,4):facade_box(m,x,y,u0-vw/2+k*vw/4,.36+vd,G+.95+(vh-1.3)/2,.07,.08,vh-1.3,M116['Frame'],a)
  for zz in (G+.95,G+vh-.30):facade_box(m,x,y,u0,.36+vd,zz,vw,.10,.08,M116['Frame'],a)
  facade_box(m,x,y,u0,.36+vd-.02,G+.95+(vh-1.3)/2,vw-.1,.02,vh-1.3,GLAZE,a)
  facade_box(m,x,y,u0,.36+vd/2,G+.45,vw,vd,.9,M116['Frame'],a)
  # the carved frieze under the veranda roof: a row of short drops
  for k in range(13):facade_box(m,x,y,u0-vw/2+.2+k*(vw-.4)/12,.36+vd+.08,G+vh-.32,.07,.05,.36,M116['Frame'],a)
  facade_box(m,x,y,u0,.36+vd+.08,G+vh-.08,vw,.06,.14,M116['Frame'],a)
  facade_box(m,x,y,u0,.36+vd/2,G+vh+.08,vw+.4,vd+.3,.16,M116['Tile'],a)

for nm,m in meshes.items():b116_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block116_cameras=[
 sv_camera('585_Block116_Cal_Molinsgatan6',-795.0,68.5,2.62,16,10),
 sv_camera('586_Block116_Cal_Molinsgatan1940s',-771.0,49.5,2.3,196,10),
 sv_camera('587_Block116_Cal_Vasterlanggatan14',-911.6,117.9,2.6,329,10),
 sv_camera('588_Block116_Cal_Vasterlanggatan12',-881.1,121.3,2.5,329,10),
 ('589_Block116_Aerial',(-760.0,20.0,75.0),(-830.0,110.0,2.0),24)]
print('BLOCK116_GEOMETRY',len(block116_names))
