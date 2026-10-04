"""Pass 122: twenty-five generic pass-17 volumes inside the blocks of the east half of Kvarnholmen
(courtyard houses, back ranges, outbuildings) get a plausible form, and Klapphuset, the small boarded
house off Bastion Carolus Philippus, gets its piles, pier and deck.
- the roof form, ridge direction and roof colour are read from top-down Google satellite views (view
  only, never textures): red and tan tile saddle and hipped roofs, dark and grey sheet metal, flat
  roofs on links, bays and one back range;
- the storeys come from the district volume (sheds capped at one storey); ridges follow from a pitch
  (about 38 degrees for red tile, 30-32 for the tan tile and hips, 22 for sheet metal);
- walls are boarded (falu red, yellow, ochre) or rendered in the colours of typical courtyard
  buildings; windows per storey, a door on the side facing the yard, plinth, eaves board and corner
  boards; roof lights and chimneys on some ranges;
- Klapphuset keeps the pass-17 eaves (2.95 m) and low dark hip with two ventilators (photo-based in
  pass 17), now with lap boarding, high windows, round piles under the house, a timber pier to the
  shore and a deck on the east end, placed from the satellite view;
- where a house is now lower than the pass-17 volume and a neighbour stands taller, a plain wall fills
  the band up to the old height so the neighbour's party wall has no hole.
Everything is estimated; see references/block122-notes.md. Zones: source/block122.json.
"""
B122D=json.loads((R/'source/block122.json').read_text());Z122=B122D['zones']
block122_names=[];B122={}
for old in [k for k in list(materials) if k.startswith('M_Block122_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Falu','TownIvory',(.50,.17,.13),.85,0),('Yellow','TownIvory',(.88,.74,.42),.85,0),('Sage','TownIvory',(.66,.74,.60),.85,0),
 ('White','TownPaintWhite',(.91,.90,.86),.80,0),('PaleYellow','TownIvory',(.90,.83,.60),.88,0),('Ochre','TownIvory',(.84,.66,.38),.88,0),
 ('GreyBeige','TownIvory',(.74,.70,.62),.88,0),('PaleGrey','TownPaintWhite',(.78,.78,.75),.88,0),('Rose','TownIvory',(.82,.66,.60),.88,0),
 ('Ivory','TownIvory',(.88,.86,.78),.88,0),('Party','TownIvory',(.70,.66,.58),.90,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('Door','TownPaintBrown',(.32,.22,.16),.70,0),('DoorGreen','TownPaintGreen',(.20,.30,.24),.65,0),
 ('Tile','TownTileRed',(.70,.36,.24),.80,0),('TileDark','TownTileRed',(.30,.24,.21),.80,0),('RoofDark','TownMetalGrey',(.20,.20,.22),.60,.25),
 ('RoofGrey','TownMetalGrey',(.42,.40,.38),.70,.15),('RoofBrown','TownMetalGrey',(.47,.42,.39),.70,.15),('RoofPale','TownMetalGrey',(.62,.56,.52),.70,.15),
 ('Stone','TownStone',(.58,.57,.54),.90,0),('Chimney','TownTileRed',(.56,.30,.23),.90,0),('Unit','TownMetalGrey',(.55,.55,.56),.60,.30),
 ('TileTan','TownTileRed',(.70,.50,.36),.80,0),('TileBrown','TownTileRed',(.58,.38,.30),.80,0),('Timber','TownPaintWhite',(.56,.53,.48),.90,0),
 ('TimberDark','TownPaintBrown',(.26,.22,.18),.90,0),
 ]:
 name='M_Block122_'+key;B122[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block122_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M122=B122;WF122=M122['Frame']
def b122_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block122_names.append(name);return Mesh(name,category)
def drop_degenerate_faces122(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b122_finish(m,osm):
 obj=s21_finish(m);obj['block122_dropped_faces']=drop_degenerate_faces122(obj);print('BLOCK122_DROPPED',m.name,obj['block122_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=122;obj['reference_notes']='references/block122-notes.md';obj['osm_way']=osm;obj['block122_estimated']=True;return obj

# ---------------------------------------------------------------- helpers
def out122(p,q):x,y,L,a=sf_edge(p,q);return (math.sin(a),-math.cos(a))
def window122(m,x,y,u,b,w,h,a,frame=None):
 fr=frame or WF122;cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2);surround36(m,x,y,u,b,w,h,a,fr,.10,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,fr,a)
def door122(m,x,y,u,b,w,h,a,leaf,frame=None,glass=True):
 fr=frame or WF122;facade_box(m,x,y,u,.12,b+h/2,w,.06,h,leaf,a)
 if glass:facade_box(m,x,y,u,.16,b+h*.78,w-.30,.02,h*.26,GLAZE,a)
 for zz in ((b+h*.40,) if glass else (b+h*.70,b+h*.30)):facade_box(m,x,y,u,.17,zz,w-.24,.03,h*.24,leaf,a)
 surround36(m,x,y,u,b,w,h,a,fr,.10,.40)
 if b>.12:
  n=max(1,round(b/.17))
  for k in range(n):facade_box(m,x,y,u,.36+.32*(n-k)/2,(k+.5)*b/n,w+.5,.32*(n-k),b/n,M122['Stone'],a)
def slide122(m,x,y,u,w,h,a,leaf,frame):
 # a boarded sliding door on its rail, as on goods sheds
 facade_box(m,x,y,u,.42,h/2,w,.08,h,leaf,a)
 for k in range(1,int(w/.25)):facade_box(m,x,y,u-w/2+k*w/int(w/.25),.47,h/2,.035,.03,h-.1,leaf,a)
 for zz in (.25,h/2,h-.25):facade_box(m,x,y,u,.48,zz,w-.1,.04,.10,frame,a)
 facade_box(m,x,y,u+w/2,.52,h+.12,2*w+.3,.08,.10,M122['RoofDark'],a)
def laps122(m,x,y,L,a,z0,z1,holes,ma,step=.15):
 # horizontal lap boarding: one shadow strip per board, broken at the openings
 for k in range(1,int((z1-z0)/step)):
  zz=z0+k*step;segs=[(-L/2+.05,L/2-.05)]
  for hu,hb,hw,hh,hr in holes:
   if hb-.06<zz<hb+hh+.06:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hu-hw/2-.10)),(max(l,hu+hw/2+.10),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,(l0+h0)/2,.37,zz,h0-l0,.03,.03,ma,a)
def rows122(z):
 # window rows (bottom, height, width) above the ground, per storey
 H,st=z['height'],z['storeys']
 if z['kind']=='shed':return [(1.1,.6,.7)] if H<2.9 else [(1.0,.8,.8)]
 if z['kind']=='goods':return [(2.3,.8,1.0)]
 if z['kind']=='pavilion':return [(.9,min(1.7,H-1.5),1.6)]
 if z['kind']=='annex':return [(.9,1.0,.9)]
 if z['kind']=='klapp':return [(1.68,.87,2.0)]
 if st>=2:return [(.95,1.35,1.0),(max(H*.5+.75,H-1.85),1.25,1.0)]
 return [(.85,1.30 if H>3.6 else 1.1,1.0)]
def door_wall122(z):
 # the outer wall whose outward side best faces the yard direction given in the zone
 if z.get('door_at'):
  P=z['door_at']
  def dist(w):
   (px,py),(qx,qy)=w['p'],w['q'];L=math.dist(w['p'],w['q']);t=max(0,min(L,((P[0]-px)*(qx-px)+(P[1]-py)*(qy-py))/L))
   return math.dist(P,(px+(qx-px)*t/L,py+(qy-py)*t/L))
  return min((w for w in z['walls'] if w['kind']=='outer'),key=dist)
 if not z.get('door'):return None
 dx,dy=z['door'];best=None;bs=-2
 for w in z['walls']:
  if w['kind']!='outer':continue
  L=math.dist(w['p'],w['q'])
  if L<2.2:continue
  ox,oy=out122(w['p'],w['q']);s=(ox*dx+oy*dy)/math.hypot(dx,dy)+min(L,12)/120
  if s>bs:bs=s;best=w
 return best
def mono122(m,r,H,T,ma,wall,ov=.40,verge=.30):
 # Mono-pitch roof over rectangle r: low eaves on r[0]->r[1], rising to r[3]->r[2]; the side walls
 # carry the sloping triangles and the high wall the band from H to T.
 p0,p1,p2,p3=r;L=math.dist(p0,p1);W=math.dist(p0,p3);d=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L);n=((p3[0]-p0[0])/W,(p3[1]-p0[1])/W);sl=(T-H)/W
 P=lambda s,t:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t,H+t*sl)
 q=[P(-verge,-ov),P(L+verge,-ov),P(L+verge,W+ov),P(-verge,W+ov)]
 m.faces(q,[(0,1,2,3),(3,2,1,0)],ma);m.faces([(v[0],v[1],v[2]-.12) for v in q],[(0,1,2,3),(3,2,1,0)],ma)
 for a_,b_,o_ in ((p3,p0,(-d[0],-d[1])),(p1,p2,d)):
  o=lambda v,k:(v[0]+o_[0]*k,v[1]+o_[1]*k);hi=p3 if a_ is p3 else p2;lo=p0 if a_ is p3 else p1
  m.faces([(*o(lo,.005),H),(*o(hi,.005),H),(*o(hi,.005),T),(*o(lo,.355),H),(*o(hi,.355),H),(*o(hi,.355),T)],
   [(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],wall)
 bz_wall(m,p2,p3,H,T,[],wall)
 x,y,_,a=sf_edge(p0,p1);facade_box(m,x,y,0,.40+ov,H-ov*sl-.10,L+2*verge,.06,.24,WF122,a)
 return sl
def flat122(m,polys,H,ma,trim):
 for g in polys:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.24,trim,a)
def slope_front122(z,r):
 # the eaves edge (p, q) of rectangle r whose slope faces the yard (door direction) or the south
 dx,dy=z.get('door') or (0,-1)
 a_=(r[0],r[1]);b_=(r[2],r[3]);oa=out122(*a_)
 return a_ if oa[0]*dx+oa[1]*dy>=0 else b_
def wall_dormer122(m,x,y,u,a,H,w,body,roof,frame):
 # a gabled wall dormer standing on the facade: the wall carried up through the eaves, a small
 # gable and a saddle running back into the main roof, a window in its face.
 dep=2.4;zb=H-.30;zt=H+1.25;ridge=zt+.85
 facade_box(m,x,y,u,.355-dep/2,(zb+zt)/2,w,dep,zt-zb,body,a)
 tri=[(u-w/2,zt),(u+w/2,zt),(u,ridge)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.355,.355-dep) for uu,zz in tri]
 m.faces(vs,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],body)
 for s in (-1,1):
  q=[lp(x,y,u+s*(w/2+.18),.355+.25,zt-.12,a),lp(x,y,u,.355+.25,ridge+.06,a),lp(x,y,u,.355-dep-.3,ridge+.06,a),lp(x,y,u+s*(w/2+.18),.355-dep-.3,zt-.12,a)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],roof)
 cas81(m,x,y,u,zb+.45,w-.7,1.1,a,frame,.41,2);facade_box(m,x,y,u,.37,zb+.45+.55,w-.7,.02,1.1,GLAZE,a)
 for uu in (u-w/2+.06,u+w/2-.06):facade_box(m,x,y,uu,.40,(zb+zt)/2,.12,.08,zt-zb,frame,a)

# ---------------------------------------------------------------- walls, windows and doors
meshes={}
for zone,z in Z122.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b122_new(z['mesh'],'Kvarnholmen/Courtyards')
for zone,z in Z122.items():
 m=meshes[z['mesh']];H=z['height'];wm0=M122[z['wall']];boarded0=z['boards']
 plinth=.15 if z['kind'] in ('shed','goods') else (.25 if z['kind']=='pavilion' else (0.0 if z['kind']=='klapp' else .35))
 dw=door_wall122(z);rows=rows122(z)
 leaf=M122['DoorGreen'] if z['wall'] in ('Falu','Sage') else M122['Door']
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q'])
  if L<.25:continue
  wm,boarded=wm0,boarded0
  if z.get('end_wall'):
   ox,oy=out122(w['p'],w['q']);ex,ey=z['end_wall'][1]
   if ox*ex+oy*ey>.9*math.hypot(ex,ey):wm,boarded=M122[z['end_wall'][0]],True
  if w['kind']=='fill':bz_wall(m,w['p'],w['q'],w['z0'],w['z1'],[],M122['Party']);continue
  if w['kind']=='upper':
   bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm)
   if boarded:boards81(m,x,y,L,a,w['z0']+.05,H-.10,[],wm)
   continue
  doors=[];wins=[];slides=[]
  if z['kind']=='goods':
   if L>20:
    slides=[(-L/4,3.0,3.0),(L/4,3.0,3.0)]
    n=int(L/5.0)
    for k in range(n):
     u=-L/2+(k+.5)*L/n
     if all(abs(u-su)>sw/2+1.0 for su,sw,sh in slides):wins.append((u,2.3,1.0,.8))
   elif L>5:doors.append((0.0,.15,1.0,2.1))
  else:
   if w is dw:
    du=0.0 if L<6 else -L/2+min(L*.3,2.6)
    if z.get('door_at'):
     P=z['door_at'];du=((P[0]-x)*math.cos(a)+(P[1]-y)*math.sin(a))
    if z['kind']=='pavilion':dw_,dh=1.8,2.3
    elif z['kind']=='shed':dw_,dh=min(1.0,L-.8),min(2.0,H-.3)
    else:dw_,dh=1.0,2.1
    doors.append((du,.05 if z['kind']=='klapp' else (.15 if z['kind']!='range' or z['storeys']<2 else .45),dw_,dh))
   bay=2.6 if z['kind']=='pavilion' else (4.0 if z['kind'] in ('shed','klapp') else 2.9)
   n=int(L/bay+.3) if z['kind']!='shed' else (1 if L>3.0 and w is not dw else (1 if L>4.5 else 0))
   for k in range(n):
    u=-L/2+(k+.5)*L/n if z['kind']!='shed' or w is not dw else L/4
    for b,hh,ww in rows:
     if b+hh>H-.25 or L<ww+1.0:continue
     if any(abs(u-du_)<(ww+dw2)/2+.35 and b<db+dh_+.2 for du_,db,dw2,dh_ in doors):continue
     wins.append((u,b,ww,hh))
  holes=[(u,b,ww,hh,0) for u,b,ww,hh in wins]+[(u,b,ww,hh,0) for u,b,ww,hh in doors]+[(u,0,ww,hh,0) for u,ww,hh in slides]
  bz_wall(m,w['p'],w['q'],w['z0'],H,holes,wm)
  if boarded=='lap':laps122(m,x,y,L,a,.05,H-.12,holes,wm)
  elif boarded:boards81(m,x,y,L,a,plinth+.03,H-.12,holes,wm)
  for u,b,ww,hh in wins:window122(m,x,y,u,b,ww,hh,a)
  for u,b,ww,hh in doors:door122(m,x,y,u,b,ww,hh,a,leaf,glass=z['kind']!='shed')
  for u,ww,hh in slides:slide122(m,x,y,u,ww,hh,a,wm,WF122)
  # plinth (gaps at the doors on the ground), corner boards on boarded walls, eaves board
  at=-L/2 if plinth>0 else L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for u,b,ww,hh in doors if b<plinth+.05)+sorted((u-ww/2,u+ww/2) for u,ww,hh in slides)+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,(plinth-.1)/2,lo-at,.08,plinth+.1,M122['Stone'],a)
   at=max(at,hi)
  if boarded:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+plinth)/2,.20,.10,H-plinth,WF122,a)
  if z['roof']!='flat':facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,WF122,a)

# ---------------------------------------------------------------- roofs and roof features
for zone,z in Z122.items():
 m=meshes[z['mesh']];H=z['height'];T=z['top'];wm=M122[z['wall']];rm=M122[z['rm']];r=[tuple(v) for v in z['rect']]
 if z['roof']=='flat':
  flat122(m,z['polygons'],H,rm,WF122 if z['kind']=='pavilion' else wm)
  continue
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
 if z['roof']=='mono':
  sl=mono122(m,r,H,T,rm,wm);continue
 if z['roof']=='hip':
  inset_roof(m,r,H,max(.3,Lt/2-.30),T-H,rm,.45);sl=(T-H)/max(.5,Lt/2+.15)
 else:
  _q,sl,ends=saddle115(m,r,H,T,rm,wm,.40,.35)
  for p,q,c,n in ends:
   # bargeboards on the verges
   o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
   for u_ in (p,q):
    e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.40,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.40)
    town_rod(m,(*o(e,.40),H-.40*sl-.04),(*o(c,.40),T-.04),.05,WF122,6)
   if z.get('end_wall') and n[0]*z['end_wall'][1][0]+n[1]*z['end_wall'][1][1]>.9*math.hypot(*z['end_wall'][1]):
    # the end gable in the end wall's colour, boarded, over the gable saddle115 built
    em=M122[z['end_wall'][0]]
    m.faces([(*o(p,.356),H),(*o(q,.356),H),(*o(c,.356),T),(*o(p,.37),H),(*o(q,.37),H),(*o(c,.37),T)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],em)
    gx,gy,gL,ga=sf_edge(p,q)
    if math.sin(ga)*n[0]-math.cos(ga)*n[1]<0:gx,gy,gL,ga=sf_edge(q,p)
    for k in range(1,int(gL/.22)):
     u=-gL/2+k*gL/int(gL/.22);zt=T-(T-H)*abs(u)/(gL/2)
     if zt-H>.12:facade_box(m,gx,gy,u,.385,(H+zt)/2-.03,.035,.03,zt-H-.06,em,ga)
 fp,fq=slope_front122(z,r);fx,fy,fL,fa=sf_edge(fp,fq);d_=((fq[0]-fp[0])/fL,(fq[1]-fp[1])/fL);nin=(-math.sin(fa),math.cos(fa))
 if z.get('dormers'):
  k=z['dormers']
  for i in range(k):dormer82(m,fx,fy,-fL/2+(i+.5)*fL/k,fa,H,sl,1.3,.9,wm,WF122,rm,.9)
 if z.get('wall_dormer'):wall_dormer122(m,fx,fy,0.0,fa,H,2.6,wm,rm,WF122)
 if z.get('skylights'):
  k=z['skylights'];ang=math.atan2(d_[1],d_[0])
  for i in range(k):
   s=-fL/2+(i+.5)*fL/k;t=min(2.2,Lt/2-.8);X,Y=fx+d_[0]*s+nin[0]*t,fy+d_[1]*s+nin[1]*t;skylight82(m,X,Y,H+t*sl,ang,sl)
 cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;dd=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(dd[1],dd[0])
 if z['kind']=='range' and z['storeys']>=1.5:
  for s in ((-Ls*.25,Ls*.25) if z.get('chimneys',1)>=2 else (Ls*.15,)):
   top=T if z['roof']!='hip' or abs(s)<Ls/2-Lt/2 else T-.8
   chimney115(m,cx_+dd[0]*s,cy_+dd[1]*s,top-.6,top+.75,M122['Chimney'] if z['wall'] in ('Falu','Yellow','Sage','Ochre') else M122['White'],ang)

def klapp122(m,z):
 # Klapphuset: two ventilators on the ridge, a floor and a timber beam over the water, round piles,
 # the pier from the door to the shore and the deck on the east end (placed from sat_e6).
 H=z['height'];T=z['top'];r=[tuple(v) for v in z['rect']];tim=M122['Timber'];dark=M122['TimberDark']
 Ls=math.dist(r[0],r[1]);d=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d[1],d[0])
 cx,cy=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4
 for s in (-Ls*.25,Ls*.25):
  X,Y=cx+d[0]*s,cy+d[1]*s;m.box((X,Y,T+.23),(.85,.65,.46),M122['RoofDark'],ang);m.box((X,Y,T+.48),(1.08,.87,.12),M122['RoofGrey'],ang)
  for zz in (T+.13,T+.28):
   for o in (-1,1):m.box((X-d[1]*o*.335,Y+d[0]*o*.335,zz),(.76,.02,.05),WF122,ang)
 g=clean115(z['polygons'][0],.1)
 if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
 m.faces([(*v,-.12) for v in g],[tuple(range(len(g)-1,-1,-1))],dark)
 for p,q in zip(g,g[1:]+g[:1]):
  L=math.dist(p,q)
  if L<.5:continue
  x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.22,-.30,L+.30,.30,.36,dark,a)
  n=max(2,round(L/2.4))
  for k in range(n+1):
   u=-L/2+.2+k*(L-.4)/n;town_rod(m,lp(x,y,u,.15,-2.3,a),lp(x,y,u,.15,-.12,a),.12,dark,8)
 # pier: from the door (outer face) to the shore
 P,Q=z['pier'];x,y,L,a=sf_edge(P,Q);ux,uy=(Q[0]-P[0])/L,(Q[1]-P[1])/L
 P0=(P[0]+ux*.36,P[1]+uy*.36);x,y,L,a=sf_edge(P0,Q);W=2.2
 facade_box(m,x,y,0,0,-.07,L,W,.14,tim,a)
 for k in range(1,int(L/.16)):facade_box(m,x,y,-L/2+k*L/int(L/.16),0,.002,.02,W-.02,.01,dark,a)
 for side in (-1,1):
  facade_box(m,x,y,0,side*(W/2-.08),-.24,L,.16,.20,dark,a)
  n=max(2,round(L/2.5))
  for k in range(n+1):
   u=-L/2+.15+k*(L-.3)/n;town_rod(m,lp(x,y,u,side*(W/2-.10),-2.3,a),lp(x,y,u,side*(W/2-.10),-.14,a),.11,dark,8)
 # deck on the east end: the outer wall facing east (local (0.881,-0.473)) and 1.6 m out
 ew=max((w for w in z['walls'] if w['kind']=='outer'),key=lambda w:out122(w['p'],w['q'])[0]*.881-out122(w['p'],w['q'])[1]*.473)
 x,y,L,a=sf_edge(ew['p'],ew['q']);D=1.6
 facade_box(m,x,y,0,.355+D/2,-.07,L+.4,D,.14,tim,a)
 for k in range(1,int(D/.16)):facade_box(m,x,y,0,.355+k*D/int(D/.16),.002,L+.38,.02,.01,dark,a)
 for u in (-L/2,0,L/2):
  town_rod(m,lp(x,y,u,.355+D-.1,-2.3,a),lp(x,y,u,.355+D-.1,-.14,a),.11,dark,8)
  town_rod(m,lp(x,y,u,.355+D-.1,0,a),lp(x,y,u,.355+D-.1,1.0,a),.05,tim,6)
 for zz in (.55,1.0):town_rod(m,lp(x,y,-L/2,.355+D-.1,zz,a),lp(x,y,L/2,.355+D-.1,zz,a),.035,tim,6)
for zone,z in Z122.items():
 if z['kind']=='klapp':klapp122(meshes[z['mesh']],z)

for nm,m in meshes.items():b122_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block122_cameras=[
 sv_camera('656_Block122_Cal_StorgatanNorthAerial',200.0,-30.0,45.0,8.7,-31,60),
 sv_camera('657_Block122_Cal_StorgatanSouthAerial',235.0,10.0,40.0,151.8,-38,60),
 sv_camera('658_Block122_Cal_OstraVallgatanAerial',320.0,-10.0,45.0,5.5,-40,60),
 sv_camera('659_Block122_Cal_Klapphuset',415.0,100.0,6.0,14.2,-11,60),
 ('660_Block122_Aerial',(280.0,-120.0,140.0),(290.0,20.0,2.0),22)]
print('BLOCK122_GEOMETRY',len(block122_names))
