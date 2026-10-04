"""Pass 121: sixteen generic pass-17 volumes inside the blocks of the west half of Kvarnholmen and by
the railway station get a plausible form: courtyard houses, back ranges, outbuildings, the goods shed
by the tracks and the two pavilions on Stationsgatan.
- the roof form, ridge direction and roof colour are read from top-down Google satellite views (view
  only, never textures): red tile saddle and hipped roofs, dark sheet metal, a grey mono-pitch roof,
  flat dark roofs on the pavilions;
- the storeys come from the district volume (sheds capped at one storey), and for 91846939 and
  91846989 on Ölandsgatan from one Street View panorama (the sage-green boarded house with its wall
  dormer, the white rendered house with three dormers);
- walls are boarded (falu red, yellow, sage green) or rendered in the colours of typical courtyard
  buildings; windows per storey, a door on the side facing the yard, plinth, eaves board and corner
  boards; dormers, roof lights and chimneys where the satellite shows them;
- where a house is now lower than the pass-17 volume and a neighbour stands taller, a plain wall fills
  the band up to the old height so the neighbour's party wall has no hole.
Everything is estimated; see references/block121-notes.md. Zones: source/block121.json.
"""
B121D=json.loads((R/'source/block121.json').read_text());Z121=B121D['zones']
block121_names=[];B121={}
for old in [k for k in list(materials) if k.startswith('M_Block121_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Falu','TownIvory',(.50,.17,.13),.85,0),('Yellow','TownIvory',(.88,.74,.42),.85,0),('Sage','TownIvory',(.66,.74,.60),.85,0),
 ('White','TownPaintWhite',(.91,.90,.86),.80,0),('PaleYellow','TownIvory',(.90,.83,.60),.88,0),('Ochre','TownIvory',(.84,.66,.38),.88,0),
 ('GreyBeige','TownIvory',(.74,.70,.62),.88,0),('PaleGrey','TownPaintWhite',(.78,.78,.75),.88,0),('Rose','TownIvory',(.82,.66,.60),.88,0),
 ('Ivory','TownIvory',(.88,.86,.78),.88,0),('Party','TownIvory',(.70,.66,.58),.90,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('Door','TownPaintBrown',(.32,.22,.16),.70,0),('DoorGreen','TownPaintGreen',(.20,.30,.24),.65,0),
 ('Tile','TownTileRed',(.70,.36,.24),.80,0),('TileDark','TownTileRed',(.30,.24,.21),.80,0),('RoofDark','TownMetalGrey',(.20,.20,.22),.60,.25),
 ('RoofGrey','TownMetalGrey',(.42,.40,.38),.70,.15),('RoofBrown','TownMetalGrey',(.47,.42,.39),.70,.15),('RoofPale','TownMetalGrey',(.62,.56,.52),.70,.15),
 ('Stone','TownStone',(.58,.57,.54),.90,0),('Chimney','TownTileRed',(.56,.30,.23),.90,0),('Unit','TownMetalGrey',(.55,.55,.56),.60,.30),
 ]:
 name='M_Block121_'+key;B121[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block121_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M121=B121;WF121=M121['Frame']
def b121_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block121_names.append(name);return Mesh(name,category)
def drop_degenerate_faces121(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b121_finish(m,osm):
 obj=s21_finish(m);obj['block121_dropped_faces']=drop_degenerate_faces121(obj);print('BLOCK121_DROPPED',m.name,obj['block121_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=121;obj['reference_notes']='references/block121-notes.md';obj['osm_way']=osm;obj['block121_estimated']=True;return obj

# ---------------------------------------------------------------- helpers
def out121(p,q):x,y,L,a=sf_edge(p,q);return (math.sin(a),-math.cos(a))
def window121(m,x,y,u,b,w,h,a,frame=None):
 fr=frame or WF121;cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2);surround36(m,x,y,u,b,w,h,a,fr,.10,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,fr,a)
def door121(m,x,y,u,b,w,h,a,leaf,frame=None,glass=True):
 fr=frame or WF121;facade_box(m,x,y,u,.12,b+h/2,w,.06,h,leaf,a)
 if glass:facade_box(m,x,y,u,.16,b+h*.78,w-.30,.02,h*.26,GLAZE,a)
 for zz in ((b+h*.40,) if glass else (b+h*.70,b+h*.30)):facade_box(m,x,y,u,.17,zz,w-.24,.03,h*.24,leaf,a)
 surround36(m,x,y,u,b,w,h,a,fr,.10,.40)
 if b>.12:
  n=max(1,round(b/.17))
  for k in range(n):facade_box(m,x,y,u,.36+.32*(n-k)/2,(k+.5)*b/n,w+.5,.32*(n-k),b/n,M121['Stone'],a)
def slide121(m,x,y,u,w,h,a,leaf,frame):
 # a boarded sliding door on its rail, as on goods sheds
 facade_box(m,x,y,u,.42,h/2,w,.08,h,leaf,a)
 for k in range(1,int(w/.25)):facade_box(m,x,y,u-w/2+k*w/int(w/.25),.47,h/2,.035,.03,h-.1,leaf,a)
 for zz in (.25,h/2,h-.25):facade_box(m,x,y,u,.48,zz,w-.1,.04,.10,frame,a)
 facade_box(m,x,y,u+w/2,.52,h+.12,2*w+.3,.08,.10,M121['RoofDark'],a)
def rows121(z):
 # window rows (bottom, height, width) above the ground, per storey
 H,st=z['height'],z['storeys']
 if z['kind']=='shed':return [(1.1,.6,.7)] if H<2.9 else [(1.0,.8,.8)]
 if z['kind']=='goods':return [(2.3,.8,1.0)]
 if z['kind']=='pavilion':return [(.9,min(1.7,H-1.5),1.6)]
 if z['kind']=='annex':return [(.9,1.0,.9)]
 if st>=2:return [(.95,1.35,1.0),(max(H*.5+.75,H-1.85),1.25,1.0)]
 return [(.85,1.30 if H>3.6 else 1.1,1.0)]
def door_wall121(z):
 # the outer wall whose outward side best faces the yard direction given in the zone
 if not z.get('door'):return None
 dx,dy=z['door'];best=None;bs=-2
 for w in z['walls']:
  if w['kind']!='outer':continue
  L=math.dist(w['p'],w['q'])
  if L<2.2:continue
  ox,oy=out121(w['p'],w['q']);s=(ox*dx+oy*dy)/math.hypot(dx,dy)+min(L,12)/120
  if s>bs:bs=s;best=w
 return best
def mono121(m,r,H,T,ma,wall,ov=.40,verge=.30):
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
 x,y,_,a=sf_edge(p0,p1);facade_box(m,x,y,0,.40+ov,H-ov*sl-.10,L+2*verge,.06,.24,WF121,a)
 return sl
def flat121(m,polys,H,ma,trim):
 for g in polys:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.24,trim,a)
def slope_front121(z,r):
 # the eaves edge (p, q) of rectangle r whose slope faces the yard (door direction) or the south
 dx,dy=z.get('door') or (0,-1)
 a_=(r[0],r[1]);b_=(r[2],r[3]);oa=out121(*a_)
 return a_ if oa[0]*dx+oa[1]*dy>=0 else b_
def wall_dormer121(m,x,y,u,a,H,w,body,roof,frame):
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
for zone,z in Z121.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b121_new(z['mesh'],'Kvarnholmen/Courtyards')
for zone,z in Z121.items():
 m=meshes[z['mesh']];H=z['height'];wm0=M121[z['wall']];boarded0=z['boards']
 plinth=.15 if z['kind'] in ('shed','goods') else (.25 if z['kind']=='pavilion' else .35)
 dw=door_wall121(z);rows=rows121(z)
 leaf=M121['DoorGreen'] if z['wall'] in ('Falu','Sage') else M121['Door']
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q'])
  if L<.25:continue
  wm,boarded=wm0,boarded0
  if z.get('end_wall'):
   ox,oy=out121(w['p'],w['q']);ex,ey=z['end_wall'][1]
   if ox*ex+oy*ey>.9*math.hypot(ex,ey):wm,boarded=M121[z['end_wall'][0]],True
  if w['kind']=='fill':bz_wall(m,w['p'],w['q'],w['z0'],w['z1'],[],M121['Party']);continue
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
    if z['kind']=='pavilion':dw_,dh=1.8,2.3
    elif z['kind']=='shed':dw_,dh=min(1.0,L-.8),min(2.0,H-.3)
    else:dw_,dh=1.0,2.1
    doors.append((du,.15 if z['kind']!='range' or z['storeys']<2 else .45,dw_,dh))
   bay=2.6 if z['kind']=='pavilion' else (4.0 if z['kind']=='shed' else 2.9)
   n=int(L/bay+.3) if z['kind']!='shed' else (1 if L>3.0 and w is not dw else (1 if L>4.5 else 0))
   for k in range(n):
    u=-L/2+(k+.5)*L/n if z['kind']!='shed' or w is not dw else L/4
    for b,hh,ww in rows:
     if b+hh>H-.25 or L<ww+1.0:continue
     if any(abs(u-du_)<(ww+dw2)/2+.35 and b<db+dh_+.2 for du_,db,dw2,dh_ in doors):continue
     wins.append((u,b,ww,hh))
  holes=[(u,b,ww,hh,0) for u,b,ww,hh in wins]+[(u,b,ww,hh,0) for u,b,ww,hh in doors]+[(u,0,ww,hh,0) for u,ww,hh in slides]
  bz_wall(m,w['p'],w['q'],w['z0'],H,holes,wm)
  if boarded:boards81(m,x,y,L,a,plinth+.03,H-.12,holes,wm)
  for u,b,ww,hh in wins:window121(m,x,y,u,b,ww,hh,a)
  for u,b,ww,hh in doors:door121(m,x,y,u,b,ww,hh,a,leaf,glass=z['kind']!='shed')
  for u,ww,hh in slides:slide121(m,x,y,u,ww,hh,a,wm,WF121)
  # plinth (gaps at the doors on the ground), corner boards on boarded walls, eaves board
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for u,b,ww,hh in doors if b<plinth+.05)+sorted((u-ww/2,u+ww/2) for u,ww,hh in slides)+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,(plinth-.1)/2,lo-at,.08,plinth+.1,M121['Stone'],a)
   at=max(at,hi)
  if boarded:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+plinth)/2,.20,.10,H-plinth,WF121,a)
  if z['roof']!='flat':facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,WF121,a)

# ---------------------------------------------------------------- roofs and roof features
for zone,z in Z121.items():
 m=meshes[z['mesh']];H=z['height'];T=z['top'];wm=M121[z['wall']];rm=M121[z['rm']];r=[tuple(v) for v in z['rect']]
 if z['roof']=='flat':
  flat121(m,z['polygons'],H,rm,WF121 if z['kind']=='pavilion' else wm)
  if zone=='pz':
   for (X,Y,w_,d_) in ((-383.6,-151.0,1.6,1.1),(-380.4,-154.2,1.2,1.2)):m.box((X,Y,H+.47),(w_,d_,.9),M121['Unit'],math.radians(-45))
  continue
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
 if z['roof']=='mono':
  sl=mono121(m,r,H,T,rm,wm);continue
 if z['roof']=='hip':
  inset_roof(m,r,H,max(.3,Lt/2-.30),T-H,rm,.45);sl=(T-H)/max(.5,Lt/2+.15)
 else:
  _q,sl,ends=saddle115(m,r,H,T,rm,wm,.40,.35)
  for p,q,c,n in ends:
   # bargeboards on the verges
   o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
   for u_ in (p,q):
    e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.40,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.40)
    town_rod(m,(*o(e,.40),H-.40*sl-.04),(*o(c,.40),T-.04),.05,WF121,6)
   if z.get('end_wall') and n[0]*z['end_wall'][1][0]+n[1]*z['end_wall'][1][1]>.9*math.hypot(*z['end_wall'][1]):
    # the end gable in the end wall's colour, boarded, over the gable saddle115 built
    em=M121[z['end_wall'][0]]
    m.faces([(*o(p,.356),H),(*o(q,.356),H),(*o(c,.356),T),(*o(p,.37),H),(*o(q,.37),H),(*o(c,.37),T)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],em)
    gx,gy,gL,ga=sf_edge(p,q)
    if math.sin(ga)*n[0]-math.cos(ga)*n[1]<0:gx,gy,gL,ga=sf_edge(q,p)
    for k in range(1,int(gL/.22)):
     u=-gL/2+k*gL/int(gL/.22);zt=T-(T-H)*abs(u)/(gL/2)
     if zt-H>.12:facade_box(m,gx,gy,u,.385,(H+zt)/2-.03,.035,.03,zt-H-.06,em,ga)
 fp,fq=slope_front121(z,r);fx,fy,fL,fa=sf_edge(fp,fq);d_=((fq[0]-fp[0])/fL,(fq[1]-fp[1])/fL);nin=(-math.sin(fa),math.cos(fa))
 if z.get('dormers'):
  k=z['dormers']
  for i in range(k):dormer82(m,fx,fy,-fL/2+(i+.5)*fL/k,fa,H,sl,1.3,.9,wm,WF121,rm,.9)
 if z.get('wall_dormer'):wall_dormer121(m,fx,fy,0.0,fa,H,2.6,wm,rm,WF121)
 if z.get('skylights'):
  k=z['skylights'];ang=math.atan2(d_[1],d_[0])
  for i in range(k):
   s=-fL/2+(i+.5)*fL/k;t=min(2.2,Lt/2-.8);X,Y=fx+d_[0]*s+nin[0]*t,fy+d_[1]*s+nin[1]*t;skylight82(m,X,Y,H+t*sl,ang,sl)
 cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;dd=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(dd[1],dd[0])
 if z['kind']=='range' and z['storeys']>=1.5:
  for s in ((-Ls*.25,Ls*.25) if z.get('chimneys',1)>=2 else (Ls*.15,)):
   top=T if z['roof']!='hip' or abs(s)<Ls/2-Lt/2 else T-.8
   chimney115(m,cx_+dd[0]*s,cy_+dd[1]*s,top-.6,top+.75,M121['Chimney'] if z['wall'] in ('Falu','Yellow','Sage','Ochre') else M121['White'],ang)

for nm,m in meshes.items():b121_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block121_cameras=[
 sv_camera('651_Block121_Cal_Olandsgatan30',130.49,-154.68,2.58,337,15,90),
 sv_camera('652_Block121_Cal_StationAerial',-330.0,-260.0,45.0,270,-30,60),
 sv_camera('653_Block121_Cal_KaggensgatanAerial',-150.0,-170.0,55.0,325,-40,60),
 sv_camera('654_Block121_Cal_SjogatanAerial',60.0,-175.0,55.0,310,-40,60),
 ('655_Block121_Aerial',(40.0,-230.0,140.0),(-40.0,-90.0,2.0),22)]
print('BLOCK121_GEOMETRY',len(block121_names))
