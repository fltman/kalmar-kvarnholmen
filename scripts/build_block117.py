"""Pass 117: the second Gamla stan pass on the mainland west of Kvarnholmen. The houses along the west
part of Västerlånggatan (centroid x <= -930) and along Gamla Kungsgatan and Paters gränd, which pass
98 built as plain volumes in its chunk meshes, each now its own mesh SM_Slott117_<osm id>:
- boarded wooden houses (vertical boards, corner boards, white window frames and eaves boards) in falu
  red, yellow, pale yellow, white, grey, olive and sage green, under red tile saddle, hipped and
  gambrel roofs, with dormers, street gables, chimneys, shutters and knee-wall windows where the
  photos show them; the tall red gable house with its black trim; the long red house with green
  shutters under its gambrel roof;
- the rendered houses: the ochre Gamla Kungsgatan 10 with its rusticated ground floor, string
  course, double wooden door, slate mansard roof, dormers and the curved central gable; the salmon
  house beside it with pilaster strips, the projecting middle with its pediment and lunette, red
  dormers and the cellar windows; the yellow, ochre, beige and white rendered houses; the light brick
  house with its balcony on Paters gränd.
It also re-creates pass 98's chunk mesh SM_Slott98_Buildings_M without these houses, with pass 115's
slott98_chunks115 (pass 98's own code).
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block117.json; see references/block117-notes.md.
"""
B117D=json.loads((R/'source/block117.json').read_text());Z117=B117D['zones'];H117=B117D['houses'];G117=B117D['ground_z']
block117_names=[];B117={}
for old in [k for k in list(materials) if k.startswith('M_Block117_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownPaintBrown',(.50,.15,.11),.80,0),('Yellow','TownIvory',(.90,.76,.42),.85,0),('PaleYellow','TownIvory',(.92,.85,.62),.85,0),
 ('White','TownPaintWhite',(.90,.90,.87),.80,0),('Grey','TownPaintWhite',(.40,.42,.46),.80,0),('Olive','TownPaintGreen',(.60,.60,.40),.80,0),
 ('Sage','TownPaintGreen',(.66,.71,.64),.80,0),('Beige','TownIvory',(.86,.74,.62),.88,0),('Ochre','TownIvory',(.88,.72,.44),.88,0),
 ('OchreDark','TownIvory',(.74,.58,.33),.88,0),('Salmon','TownIvory',(.80,.52,.38),.88,0),('LightBrick','TownStone',(.80,.72,.58),.90,0),
 ('Trim','TownIvory',(.82,.79,.72),.85,0),('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('Black','TownMetalGrey',(.07,.07,.075),.60,.10),
 ('Tile','TownTileRed',(.68,.32,.21),.80,0),('TileDark','TownTileRed',(.40,.24,.19),.80,0),('RoofGrey','TownMetalGrey',(.36,.37,.38),.55,.30),
 ('RoofSlate','TownMetalGrey',(.20,.22,.26),.55,.30),('Door','TownPaintBrown',(.42,.28,.17),.70,0),('DoorWhite','TownPaintWhite',(.92,.92,.90),.60,0),
 ('Shutter','TownPaintWhite',(.80,.80,.78),.65,0),('ShutterGreen','TownPaintGreen',(.52,.62,.50),.70,0),('ShutterWhite','TownPaintWhite',(.92,.92,.90),.65,0),
 ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Chimney','TownIvory',(.85,.84,.80),.88,0),
 ('ChimneyBrick','TownTileRed',(.55,.27,.20),.90,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
 ]:
 name='M_Block117_'+key;B117[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block117_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M117=B117
def b117_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block117_names.append(name);return Mesh(name,category)
def drop_degenerate_faces117(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b117_finish(m,osm):
 obj=s21_finish(m);obj['block117_dropped_faces']=drop_degenerate_faces117(obj);print('BLOCK117_DROPPED',m.name,obj['block117_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=117;obj['reference_notes']='references/block117-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunk without these houses
# Pass 115's mechanism: the ids join SLOTT98_DETAILED (which keeps the ids of every earlier pass in the
# chain) and the chunk the houses sit in is re-created by pass 98's own code. All of this pass's houses
# have their centroid between x -1150 and -850, so only the 'M' chunk is touched.
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|set(B117D['ids'])
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in B117D['ids']},117,block117_names)

# ---------------------------------------------------------------- helpers
def g117(h):return G117+h
def ccw117(poly):
 poly=[tuple(v) for v in poly];return poly if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1]))>0 else poly[::-1]
def unit117(p,q):L=math.dist(p,q);return ((q[0]-p[0])/L,(q[1]-p[1])/L)
def roofrect117(zone):
 # The zone's rectangle (counter-clockwise) turned so that the ridge runs along r[0]->r[1]: for the
 # main body parallel to the street wall ('par') or across it ('perp'), else along the long side.
 z=Z117[zone];r=ccw117(z['rect']);h=H117[z['osm']]
 e01=math.dist(r[0],r[1]);e12=math.dist(r[1],r[2])
 if z['role']=='main' and z.get('street_wall'):
  d=unit117(*z['street_wall']);u=unit117(r[0],r[1]);par=abs(d[0]*u[0]+d[1]*u[1])>.7
  if par!=(h.get('ridge','par')=='par'):r=r[1:]+r[:1]
 elif e12>e01+.01:r=r[1:]+r[:1]
 return r
def endwall117(m,p,q,prof,ma,o0=.005,o1=.355):
 # A wall slab over the end p-q (outward to the right of p->q) with the outline prof [(s along p->q,
 # z)], drawn between o0 and o1 outside the line, like the walls.
 x,y,L,a=sf_edge(p,q);pts=[(s-L/2,z) for s,z in prof];n=len(pts)
 vs=[lp(x,y,u,o,z,a) for o in (o0,o1) for u,z in pts]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def slope117(m,quad,zs,ma):
 m.faces([(*v,z) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
 m.faces([(*v,z-.12) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
def gambrel117(m,r,H,Bk,T,ma,wall,ov=.40,verge=.30,kin=.30):
 # Gambrel (brutet sadeltak) over rectangle r, ridge along r[0]->r[1]: a steep lower slope up to the
 # break Bk, kin of the half depth in from the walls, and a low upper slope to the ridge T; the
 # gable walls carry the five-sided outline.
 p0,p1,p2,p3=r;L=math.dist(p0,p1);D=math.dist(p0,p3);hd=D/2;d=unit117(p0,p1);n=unit117(p0,p3)
 P=lambda s,t:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t);bi=hd*kin;sl=(Bk-H)/bi
 for t_e,t_b,t_r in ((-ov,bi,hd),(D+ov,D-bi,hd)):
  slope117(m,[P(-verge,t_e),P(L+verge,t_e),P(L+verge,t_b),P(-verge,t_b)],[H-ov*sl]*2+[Bk]*2,ma)
  slope117(m,[P(-verge,t_b),P(L+verge,t_b),P(L+verge,t_r),P(-verge,t_r)],[Bk,Bk,T,T],ma)
 prof=[(0,H),(bi,Bk),(hd,T),(D-bi,Bk),(D,H)]
 endwall117(m,p3,p0,[(D-s,z) for s,z in prof],wall);endwall117(m,p1,p2,prof,wall)
 return sl
def shed_roofs117(m,zone,H,T,ma,trim):
 for g in Z117[zone]['polygons']:
  g=clean115(g,.1)
  if len(g)<3:continue
  g=ccw117(g);m.faces([(*v,T) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,(H+T)/2,L+.3,.22,T-H+.1,trim,a)
def window117(m,x,y,u,b,w,h,a,fr,sur,sh=None,rows=None,o=0.0):
 # o: extra offset outwards, for windows on a gable slab (which has no hole) rather than in a wall
 if o:facade_box(m,x,y,u,o+.12,b+h/2,w,.02,h,GLAZE,a)
 cas81(m,x,y,u,b,w,h,a,M117[fr],.16+o,rows or (3 if h>1.45 else 2))
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38+o,b+h/2,.12,.06,h+.12,M117[sur],a)
 facade_box(m,x,y,u,.38+o,b+h+.08,w+.30,.06,.14,M117[sur],a);facade_box(m,x,y,u,.45+o,b-.05,w+.24,.18,.06,M117[sur],a)
 if sh:
  for s in (-1,1):facade_box(m,x,y,u+s*(w*.75+.14),.40+o,b+h/2,w/2,.04,h,M117[sh],a)
def door117(m,x,y,u,b,w,h,a,leaf,sur,glass=False,double=False):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,M117[leaf],a)
 if glass:
  facade_box(m,x,y,u,.165,b+h*.62,w-.30,.02,h*.62,GLAZE,a)
  for q in (-w/4,w/4) if double else (0,):facade_box(m,x,y,u+q,.18,b+h*.62,.05,.05,h*.62,M117[sur],a)
 else:
  for q in ((-w/4,w/4) if double else (0,)):
   for zz,hh in ((b+h*.28,h*.36),(b+h*.70,h*.36)):facade_box(m,x,y,u+q,.17,zz,(w/2 if double else w)-.24,.03,hh,M117[leaf],a)
  if double:facade_box(m,x,y,u,.17,b+h/2,.04,.05,h,M117['Black'],a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.07),.38,b+h/2,.14,.07,h+.14,M117[sur],a)
 facade_box(m,x,y,u,.38,b+h+.10,w+.34,.07,.16,M117[sur],a)
def chimney117(m,X,Y,z0,z1,ma,ang=0,w=.6,d=.6):
 m.box((X,Y,(z0+z1)/2),(w,d,z1-z0),ma,ang);m.box((X,Y,z1+.05),(w+.12,d+.12,.10),M117['Stone'],ang)
def lunette117(m,x,y,u,zs,r,a,fr,o=.37):
 k=12
 m.faces([lp(x,y,u+r*math.cos(math.pi*i/k),o,zs+r*math.sin(math.pi*i/k),a) for i in range(k+1)],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.07)*math.cos(math.pi*i/k),o+.05,zs+(r+.07)*math.sin(math.pi*i/k),a) for i in range(k+1)],.06,fr)
 facade_box(m,x,y,u,o+.05,zs-.03,2*r+.25,.10,.08,fr,a)
 for i in range(1,4):town_rod(m,lp(x,y,u,o+.03,zs,a),lp(x,y,u+r*math.cos(math.pi*i/4),o+.03,zs+r*math.sin(math.pi*i/4),a),.02,fr,6)
def wallframe117(p,q,inside):
 # sf_edge of p->q turned so that the facade faces away from the point 'inside'.
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*(x-inside[0])-math.cos(a)*(y-inside[1])<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a

# ---------------------------------------------------------------- per-house styles
# rows: window rows (bottom, height, width) above the ground; bay: window spacing along the eaves
# walls; plinth: height and material; door: (side, offset along the wall from its middle, width,
# height, bottom, kind). Measured values are in the notes; the rest by the storeys.
def rows117(h):
 if h.get('shed'):return []
 H=h['height'];st=h['st']
 if st>=2:b2=max(2.6,H*.56);return [(.9,min(1.4,H*.25),1.0),(b2,min(1.35,H-b2-.35),1.0)]
 return [(.85,min(1.4,H-1.25),1.0)]
STY={
 '93292674':dict(rows=[(1.1,1.65,1.0),(4.1,1.6,1.0)],bay=3.6,trim='Black',sur='Black'),
 '93292684':dict(rows=[(.75,.9,.75),(2.6,1.0,.75)],bay=2.4),
 '93292707':dict(rows=[(.6,1.6,1.15),(3.15,.7,1.15)],bay=3.9),
 '93292700':dict(rows=[(1.8,1.8,1.1),(4.7,2.15,1.1)],bay=2.55,plinth=(.9,'Stone'),sur='Trim',trim='Trim'),
 '93292694':dict(rows=[(1.6,1.7,1.0),(4.9,1.8,1.0)],bay=2.5,plinth=(.8,'Stone'),sur='Trim',trim='Trim'),
 '93292699':dict(rows=[(.9,1.35,.9)],bay=4.2),
 '93292703':dict(sur='Trim',trim='Trim',plinth=(.5,'Stone')),
 '93292676':dict(sur='Trim',trim='Trim',plinth=(.5,'Stone')),'93292698':dict(sur='Trim',trim='Trim',plinth=(.5,'Stone')),
 '93292678':dict(sur='Frame',trim='Frame',plinth=(.45,'Stone')),'93292658':dict(sur='Frame',trim='Trim',plinth=(.45,'Stone')),
 '93309098':dict(sur='Frame',trim='Frame',plinth=(.4,'Stone')),
 '93292670':dict(sur='Frame',trim='Trim',plinth=(.4,'Stone')),
 '93292660':dict(rows=[(.9,1.35,1.0),(3.3,1.3,1.0)],bay=2.6),
 '93306357':dict(rows=[(.9,1.35,1.0),(3.4,1.3,1.0)],bay=2.4),
 '93292705':dict(rows=[(.95,1.45,1.05)],bay=3.0),
}
DOOR117={  # kind: door, glass, double, garage
 '93292694':('street',0,1.7,2.6,.8,'double'),'93292700':('back',0,1.2,2.4,.9,'door'),'93292660':('street',1.5,1.0,2.2,.25,'glass'),
 '93292675':('street',0,2.6,2.2,0,'garage'),'93292705':('street',4.5,1.0,2.1,.3,'door'),'93292707':('back',0,1.0,2.1,.3,'door'),
 '93292674':('back',0,1.0,2.1,.3,'door'),'93292684':('back',0,.9,2.0,.25,'door'),'93292699':('back',0,1.0,2.1,.3,'door'),'93292671':('back',0,.9,2.0,.25,'door'),
}

# The street front of the two stone houses, read on k02_h14 and k01_h30 (the outline's south-west
# side); the nearest-street rule picks another side at the corner of Paters gränd.
FRONT117={'93292700':(0,1),'93292694':(0,1)}
for zone,z in Z117.items():
 if z['role']=='main' and z['osm'] in FRONT117:
  o_=[b for b in B98D['buildings'] if b['id']==z['osm']][0]['outer'];i_,j_=FRONT117[z['osm']];z['street_wall']=[list(o_[i_]),list(o_[j_])]

# ---------------------------------------------------------------- walls, windows, doors
meshes={}
for zone,z in Z117.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b117_new(z['mesh'],'Slottsområdet/Gamla stan')
for zone,z in Z117.items():
 m=meshes[z['mesh']];osm=z['osm'];h=H117[osm];sty=STY.get(osm,{});H=g117(z['height'])
 wm=M117[h['wall']];boarded=h['boards'];trim=sty.get('trim','Frame');sur=sty.get('sur','Frame')
 rows=sty.get('rows') or rows117(h);bay=sty.get('bay',2.8);pl=sty.get('plinth',(.3,'Stone'))
 if z['role']=='annex':rows=[r_ for r_ in rows if r_[0]+r_[1]<z['height']-.3][:1]
 if z['role']=='wing' and h['st']<2:rows=rows[:1]
 r=roofrect117(zone);rd=unit117(r[0],r[1])
 cen=(sum(v[0] for v in r)/4,sum(v[1] for v in r)/4)
 # the door: on the street wall (or the wall opposite it), main zone only
 dspec=DOOR117.get(osm,('street',0,1.0,2.1,.25 if boarded else .45,'door'))
 dwall=None
 if z['role']=='main':
  outs=[w for w in z['walls'] if w['kind']=='outer' and math.dist(w['p'],w['q'])>1.6]
  if z.get('street_wall') and outs:
   sw=z['street_wall'];smid=((sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2)
   key=(lambda w:-math.dist(((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2),smid)) if dspec[0]=='back' else (lambda w:math.dist(((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2),smid))
   dwall=min(outs,key=key)
  elif outs:dwall=max(outs,key=lambda w:math.dist(w['p'],w['q']))
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else g117(w['z0'])
  if L<.25:continue
  wd=unit117(w['p'],w['q']);gable=abs(wd[0]*rd[0]+wd[1]*rd[1])<.7
  holes=[];doors=[]
  if w is dwall:
   side,off,dw,dh,db,kind=dspec;u=max(-L/2+dw/2+.3,min(L/2-dw/2-.3,off))
   if L>dw+.7:doors.append((u,g117(db),dw,dh,kind));holes.append((u,g117(db),dw,dh,0))
  wins=[]
  if w['kind']=='outer' or z0<H-1.5:
   n=int(L/bay+.35) if not gable else max(1,int(L/3.2+.2))
   if L<1.8:n=0
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for b,hh,ww in rows:
     bb=g117(b)
     if bb<z0+.3 or bb+hh>H-.2:continue
     if any(abs(u-du)<(ww+dw)/2+.35 for du,db_,dw,dh,_ in doors):continue
     if L<ww+.9:continue
     wins.append((u,bb,ww,hh))
  holes+=[(u,b,ww,hh,0) for u,b,ww,hh in wins]
  bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if boarded:boards81(m,x,y,L,a,max(z0,G117+pl[0]+.02),H-.12,holes,wm,.21)
  for u,b,ww,hh in wins:window117(m,x,y,u,b,ww,hh,a,'Frame',sur,h.get('sh') if w['kind']=='outer' else None)
  for u,b,dw,dh,kind in doors:
   if kind=='garage':
    for s in (-1,1):facade_box(m,x,y,u+s*dw/4,.12,b+dh/2,dw/2-.04,.07,dh,M117['Black'],a)
    surround36(m,x,y,u,b,dw,dh,a,M117['Frame'],.12,.40)
   else:door117(m,x,y,u,b,dw,dh,a,'DoorWhite' if kind=='glass' else 'Door',sur,kind=='glass',kind=='double')
   if b>G117+.15:steps115(m,x,y,u,dw+.6,b,a,M117['Step'])
  if w['kind']=='outer':facade_box(m,x,y,0,.40,(G117+pl[0])/2,L+.02,.10,G117+pl[0],M117[pl[1]],a)
  # eaves board (boarded) or cornice (rendered); corner boards or quoins
  if not gable or z['roof'] in ('hip','mansard','flat'):facade_box(m,x,y,0,.44,H-.12,L+.12,.16 if boarded else .22,.22 if boarded else .26,M117[trim],a)
  if w['kind']=='outer':
   for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+G117+pl[0])/2,.18,.08,H-G117-pl[0],M117[trim],a)

# ---------------------------------------------------------------- roofs and the features
RM={'Tile':'Tile','TileDark':'TileDark','RoofGrey':'RoofGrey','RoofSlate':'RoofSlate'}
FEAT=[]
for zone,z in Z117.items():
 m=meshes[z['mesh']];osm=z['osm'];h=H117[osm];sty=STY.get(osm,{});H=g117(z['height']);T=g117(z['top'])
 wm=M117[h['wall']];rm=M117[RM[h['rm']]];trim=M117[sty.get('trim','Frame')]
 r=roofrect117(zone);Ls=math.dist(r[0],r[1]);Lt=math.dist(r[1],r[2]);ang=math.atan2(r[1][1]-r[0][1],r[1][0]-r[0][0])
 cen=(sum(v[0] for v in r)/4,sum(v[1] for v in r)/4)
 kind=z['roof'];ends=None;sl=None
 if kind=='flat':shed_roofs117(m,zone,H,H+.25,rm if h['rm']!='Tile' else M117['RoofGrey'],trim);continue
 if kind=='saddle':
  eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40,.30)
  for p,q,c,nn in ends:
   for u_ in (p,q):
    e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.30,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.30)
    town_rod(m,(*(e[0]+nn[0]*.40,e[1]+nn[1]*.40),H-.30*sl-.06),(c[0]+nn[0]*.40,c[1]+nn[1]*.40,T-.06),.07,trim,6)
 elif kind=='hip':inset_roof(m,r,H,min(Ls,Lt)/2-.30,T-H,rm,.40);sl=(T-H)/(min(Ls,Lt)/2+.10)
 elif kind=='gambrel':
  Bk=g117(h.get('brk',(z['height']+z['top'])/2+.6));sl=gambrel117(m,r,H,Bk,T,rm,wm)
  p0,p1,p2,p3=r;ends=((p0,p3,((p0[0]+p3[0])/2,(p0[1]+p3[1])/2),(-math.cos(ang),-math.sin(ang))),(p1,p2,((p1[0]+p2[0])/2,(p1[1]+p2[1])/2),(math.cos(ang),math.sin(ang))))
 elif kind=='mansard':
  Bk=g117(h['brk']);bi=1.0
  outer,inner=inset_roof(m,r,H,bi,Bk-H,rm,.40);inset_roof(m,ccw117(inner),Bk,min(Ls,Lt)/2-bi-.10,T-Bk,rm,.0);sl=(Bk-H)/(bi+.40)
 if z['role']!='main':continue
 FEAT.append((zone,r,sl,ends))
 ex=h.get('extras',[])
 # gable windows: one or two in each gable above the eaves (one-and-a-half storeys and up)
 if ends and (h['st']>=1.5 or 'gable_window' in ex or 'gable_windows' in ex):
  for p,q,c,nn in ends:
   x,y,L,a=wallframe117(p,q,cen)
   if kind=='gambrel':
    for s in ((-.9,.9) if L>6 else (0,)):window117(m,x,y,s,H+.45,.85,1.2,a,'Frame',sty.get('sur','Frame'),o=.24)
   else:
    gw=.8 if T-H>2.6 else .55;gh=min(1.2,(T-H)*.38)
    if 'lunette' in ex:lunette117(m,x,y,0,T-1.25,.45,a,M117['Frame'],.40);gh=min(1.1,T-H-2.0);gw=.8
    pair=('gable_windows' in ex) or (L>7 and T-H>2.4 and 'lunette' not in ex and 'gable_window' not in ex)
    for s in ((-.75,.75) if pair else (0,)):
     if gh>.45:window117(m,x,y,s,H+.30,gw,gh,a,'Frame',sty.get('sur','Frame'),o=.24)
 # chimney on the ridge, a third along
 cr=((r[0][0]+r[3][0])/2,(r[0][1]+r[3][1])/2);d=unit117(r[0],r[1])
 if 'chimney' in ex or 'chimney_brick' in ex or 'chimneys2' in ex:
  for f_ in ((.3,.72) if 'chimneys2' in ex else (.62,)):
   X,Y=cr[0]+d[0]*Ls*f_,cr[1]+d[1]*Ls*f_;chimney117(m,X,Y,T-1.0,T+.85,M117['ChimneyBrick' if 'chimney_brick' in ex or h['boards'] else 'Chimney'],ang)
 # the street front of the main body (the eaves wall nearest the street)
 sw=z.get('street_wall')
 if sw:
  smid=((sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2)
  eaves=[(r[0],r[1]),(r[2],r[3])];ep=min(eaves,key=lambda pq:math.dist(((pq[0][0]+pq[1][0])/2,(pq[0][1]+pq[1][1])/2),smid))
  ex_,ey_,eL,ea=wallframe117(ep[0],ep[1],cen)
 else:ex_,ey_,eL,ea=wallframe117(r[0],r[1],cen)
 rsl=sl if sl else .8
 if 'frontis' in ex:
  frontis83(m,ex_,ey_,0,3.4,H,H+1.3,H+2.9,ea,wm,M117['Frame'],rm,True)
 if 'dormer' in ex or 'dormers_red' in ex or 'dormers_slate' in ex:
  us=(0,) if 'dormer' in ex else ((-eL/4,eL/4) if eL>9 else (0,))
  body=M117['Red'] if 'dormers_red' in ex else (M117['RoofSlate'] if 'dormers_slate' in ex else wm)
  for uu in us:
   if 'curved_gable' in ex and abs(uu)<1:continue
   dormer82(m,ex_,ey_,uu,ea,H,min(rsl,1.6),1.2,.9,body,M117['Frame'],rm,.9 if kind!='mansard' else .7)
 if 'skylight' in ex:
  for f_ in (.35,.65):
   X,Y=lp(ex_,ey_,-eL/2+eL*f_,-(Lt/2)*.45,0,ea)[:2];skylight82(m,X,Y,H+(Lt/2)*.45*rsl+.03,ea+math.pi,rsl)
 if 'knee' in ex:pass
 if 'bands_black' in ex:
  for w in Z117[zone]['walls']:
   if w['kind']!='outer':continue
   x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.42,g117(3.7),L+.1,.08,.16,M117['Black'],a)
 if 'rustic' in ex:
  # rusticated ground floor: grooves every 0.42 m, the string course over it, cellar windows
  for w in Z117[zone]['walls']:
   if w['kind']!='outer':continue
   x,y,L,a=sf_edge(w['p'],w['q'])
   for k in range(1,9):
    zz=g117(.8+k*.42)
    if zz<g117(4.3):facade_box(m,x,y,0,.37,zz,L-.1,.04,.05,M117['OchreDark'],a)
   facade_box(m,x,y,0,.43,g117(4.45),L+.12,.16,.22,M117['Trim'],a)
 if 'cellar' in ex or 'rustic' in ex:
  for w in Z117[zone]['walls']:
   if w['kind']!='outer':continue
   x,y,L,a=sf_edge(w['p'],w['q']);n=int(L/(sty.get('bay',2.6))+.35)
   for k in range(n):
    u=-L/2+(k+.5)*L/max(1,n)
    if abs(u)<1.3 and 'rustic' in ex:continue
    facade_box(m,x,y,u,.47,g117(.40),.7,.04,.40,M117['Black'],a);facade_box(m,x,y,u,.50,g117(.40),.78,.03,.48,M117['Trim'],a)
 if 'curved_gable' in ex:
  # the curved central gable over the door: the facade carried up in an S-curved outline with two
  # windows and a round window, a slate lid behind it
  fw=5.4;prof=[(-fw/2,H-.1),(fw/2,H-.1),(fw/2,H+.9)]
  for i in range(1,9):t=i/8;prof.append((fw/2-(fw/2-.6)*t,H+.9+2.0*(math.sin(t*math.pi/2))))
  prof.append((-.6,H+2.9))
  for i in range(1,8):t=1-i/8;prof.append((-(fw/2-(fw/2-.6)*t),H+.9+2.0*(math.sin(t*math.pi/2))))
  prof.append((-fw/2,H+.9))
  vs=[lp(ex_,ey_,u,o,zz,ea) for o in (.005,.355) for u,zz in prof];nn=len(prof)
  m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],wm)
  town_path(m,[lp(ex_,ey_,u,.44,zz+.06,ea) for u,zz in prof[2:]+[prof[0+0]] if zz>H+.85],.07,M117['Trim'])
  box(m,*lp(ex_,ey_,0,-1.6,0,ea)[:2],fw-.8,3.2,2.4,H,wm,ea,rm)
  for s in (-.9,.9):window117(m,ex_,ey_,s,H+.25,.85,1.2,ea,'Frame','Trim',o=.28)
  porthole82(m,ex_,ey_,0,H+2.15,.28,ea,M117['Trim'])  # (sits on the gable face at 0.385-0.41)
 if 'pediment' in ex:
  # the middle (5.2 m) marked by pilaster strips, its pediment with the lunette
  fw=5.2
  for uu in (-eL/2+.3,eL/2-.3,-fw/2,fw/2):facade_box(m,ex_,ey_,uu,.47,(g117(.9)+H)/2,.5,.06,H-g117(.9),M117['Trim'],ea)
  frontis83(m,ex_,ey_,0,fw,H,H+.05,g117(9.9),ea,wm,M117['Trim'],rm,False)
  lunette117(m,ex_,ey_,0,H+.35,.55,ea,M117['Trim'])
 if 'balcony' in ex and ends:
  # the balcony on the gable towards Paters gränd
  p,q,c,nn=min(ends,key=lambda e:math.dist(e[2],(-1026.0,25.0)))
  x,y,L,a=wallframe117(p,q,cen);zb=g117(3.0)
  facade_box(m,x,y,0,.36+.6,zb,2.8,1.2,.16,M117['Stone'],a)
  town_rod(m,lp(x,y,-1.4,1.52,zb+1.0,a),lp(x,y,1.4,1.52,zb+1.0,a),.03,M117['Iron'],6)
  for k in range(15):town_rod(m,lp(x,y,-1.4+k*2.8/14,1.52,zb+.08,a),lp(x,y,-1.4+k*2.8/14,1.52,zb+1.0,a),.012,M117['Iron'],4)
  for s in (-1,1):town_rod(m,lp(x,y,s*1.4,.40,zb+1.0,a),lp(x,y,s*1.4,1.52,zb+1.0,a),.03,M117['Iron'],6)
  door117(m,x,y,0,zb+.08,.9,2.0,a,'DoorWhite','Frame',True)

for nm,m in meshes.items():b117_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block117_cameras=[
 sv_camera('601_Block117_Cal_RedGableHouse',-1076.85,55.19,2.75,119,10),
 sv_camera('602_Block117_Cal_Vasterlanggatan25',-1051.96,69.91,2.85,123,10),
 sv_camera('603_Block117_Cal_PatersGrand',-1021.62,31.52,2.5,14,12),
 sv_camera('604_Block117_Cal_GreenShutters',-994.7,95.7,2.7,134,10),
 ('605_Block117_Aerial',(-920.0,-60.0,80.0),(-1030.0,45.0,2.0),24)]
print('BLOCK117_GEOMETRY',len(block117_names))
