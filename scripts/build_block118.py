"""Pass 118: the third Gamla stan pass on the mainland west of Kvarnholmen, Kungsgatan, Söderportsgatan,
Klostergatan and Skansgatan. Pass 98 built these 40 houses as plain volumes in its chunk meshes; each is
now its own mesh SM_Slott118_<osm id> with its real form: storeys, saddle, hipped, gambrel and hipped
mansard roofs in red or red-brown tile, vertical boarding, render or brick in the house's colour,
white corner boards, eaves boards and window frames, windows per storey, a door on the street,
dormers, chimneys and the notable features:
- on Söderportsgatan the derelict white-grey boarded house at the Klostergatan corner (a two-storey
  cross part with low gables on both streets between gambrel wings, boarded-up windows, the green door
  in its carved surround); the 18th-century pink rough-rendered stone house with light quoins, the
  stone door surround and two dormers; the pale yellow boarded gambrel villa on its raised plinth with
  the glazed porch; the yellow cottage, the brick villa, the red boarded house at the Skansgatan
  corner and the outbuildings and garages;
- on the north side the white rendered villa with the corner tower (pyramid roof), the cross gable
  and the balcony; the pale yellow villa with the hipped mansard roof, its dormers and the white curved
  Jugend gable; the red boarded villa with the hipped roof;
- on Kungsgatan further north the 1940s rendered apartment row (pale green and yellow sections, white
  curved window hoods, the balcony over the entrance of no. 13A), the white rendered two-storey blocks
  at Ståthållaregatan, the yellow three-storey block with the hipped roof, the salmon three-storey
  blocks with balconies and the yellow-brick 1950s houses with roof lights and the garage;
- houses seen in no photo get a plain Gamla stan form: boarded, tile saddle roof, the colour from
  their neighbours.
It also re-creates pass 98's chunk meshes the houses sit in with slott98_chunks115 (pass 115), leaving
out every house in SLOTT98_DETAILED.
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block118.json; see references/block118-notes.md.
"""
B118D=json.loads((R/'source/block118.json').read_text());Z118=B118D['zones'];HS118=B118D['houses'];G118=B118D['ground_z']
block118_names=[];B118={}
for old in [k for k in list(materials) if k.startswith('M_Block118_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownIvory',(.52,.18,.14),.85,0),('Yellow','TownIvory',(.87,.73,.40),.85,0),('PaleYellow','TownIvory',(.88,.82,.60),.85,0),
 ('White','TownPaintWhite',(.92,.92,.89),.80,0),('WhiteGrey','TownPaintWhite',(.80,.80,.77),.85,0),('Grey','TownIvory',(.66,.66,.63),.88,0),
 ('Brown','TownPaintBrown',(.38,.26,.20),.80,0),('Brick','TownIvory',(.56,.26,.19),.92,0),('YellowBrick','TownIvory',(.80,.70,.50),.92,0),
 ('PinkRender','TownIvory',(.70,.46,.41),.92,0),('PaleYellowRender','TownIvory',(.89,.84,.64),.88,0),('PaleGreen','TownIvory',(.68,.75,.64),.88,0),
 ('YellowRender','TownIvory',(.85,.66,.36),.88,0),('WhiteRender','TownIvory',(.90,.89,.85),.88,0),('Salmon','TownIvory',(.85,.55,.40),.88,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('Tile','TownTileRed',(.66,.32,.22),.80,0),('TileBrown','TownTileRed',(.45,.22,.16),.80,0),
 ('RoofDark','TownMetalGrey',(.22,.22,.24),.60,.25),('RoofTower','TownTileRed',(.40,.34,.30),.85,0),
 ('Door','TownPaintBrown',(.30,.21,.15),.70,0),('GreenDoor','TownPaintGreen',(.26,.44,.30),.60,0),('Plywood','TownPaintBrown',(.55,.45,.33),.85,0),
 ('GarageDoor','TownPaintWhite',(.62,.58,.52),.70,0),('Quoin','TownStone',(.84,.82,.76),.90,0),
 ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Chimney','TownTileRed',(.55,.28,.22),.90,0),
 ('ChimneyWhite','TownIvory',(.86,.85,.81),.88,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
 ]:
 name='M_Block118_'+key;B118[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block118_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M118=B118
B98ID118={b['id']:b for b in B98D['buildings']}
def b118_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block118_names.append(name);return Mesh(name,category)
def drop_degenerate_faces118(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b118_finish(m,osm):
 obj=s21_finish(m);obj['block118_dropped_faces']=drop_degenerate_faces118(obj);print('BLOCK118_DROPPED',m.name,obj['block118_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=118;obj['reference_notes']='references/block118-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without these houses
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|set(B118D['ids'])
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in B118D['ids']},118,block118_names)
# slott98_chunks115 finishes the chunks with pass 115's finisher (detail_pass 98, rebuilt_by_pass 118).

# ---------------------------------------------------------------- helpers
G=G118
def zabs118(h):return G+h
def long_first118(r):
 r=[tuple(v) for v in r]
 return r if math.dist(r[0],r[1])>=math.dist(r[1],r[2])-.01 else r[1:]+r[:1]
def end_frame118(p,q,n):
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def gambrel118(m,r,H,T,ma,wall,ov=.35,verge=.30):
 # pass 116's Swedish mansard (gambrel) with gable ends: steep lower slopes 0.85 m in and 60 % of the
 # rise up, low upper slopes to the ridge (along r[0]->r[1]); the gables as pentagons in the wall
 # material. Returns the break inset, the break height and the ends.
 p0,p1,p2,p3=r;L=math.dist(p0,p1);W=math.dist(p1,p2);d=((p1[0]-p0[0])/L,(p1[1]-p0[1])/L);n=((p3[0]-p0[0])/W,(p3[1]-p0[1])/W)
 k=min(.85,W/4);ZB=H+(T-H)*.6;prof=[(-ov,H-ov*(ZB-H)/k),(0,H),(k,ZB),(W/2,T),(W-k,ZB),(W,H),(W+ov,H-ov*(ZB-H)/k)]
 P=lambda s,t,z:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t,z)
 for (t0,z0),(t1,z1) in [(prof[0],prof[2]),(prof[2],prof[3]),(prof[3],prof[4]),(prof[4],prof[6])]:
  q=[P(-verge,t0,z0),P(L+verge,t0,z0),P(L+verge,t1,z1),P(-verge,t1,z1)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],ma);m.faces([(v[0],v[1],v[2]-.10) for v in q],[(0,1,2,3),(3,2,1,0)],ma)
 for s,sg in ((0,-1),(L,1)):
  pts=[P(s+sg*o,t,z) for o in (.005,.355) for t,z in prof[1:6]]
  m.faces(pts,[(0,1,2,3,4),(9,8,7,6,5),(0,5,6,1),(1,6,7,2),(2,7,8,3),(3,8,9,4),(4,9,5,0)],wall)
 mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 return k,ZB,((p0,p3,mid(p0,p3),(-d[0],-d[1])),(p1,p2,mid(p1,p2),(d[0],d[1])))
def mhip118(m,r,H,T,ma,ov=.40):
 # A hipped mansard: steep lower slopes on all four sides from the eaves to the break (1.1 m in,
 # 70 % of the rise up), then a low hip to the top.
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2]);k=min(1.1,min(Ls,Lt)/4);ZB=H+(T-H)*.7
 outer,inner=inset_roof(m,r,H,k,ZB-H,ma,ov)
 inset_roof(m,[tuple(v) for v in inner],ZB,max(.3,min(Ls,Lt)/2-k-.3),T-ZB,ma,.12)
 return k,ZB
def flat118(m,polys,H,ma,trim):
 for g in polys:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.22,trim,a)
def window118(m,x,y,u,b,w,h,a,frame='Frame',board=False,hood=False):
 # pass 116's window: casement, surround, sill; a plywood panel over a boarded-up one; a white hood
 fr=M118[frame];cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,fr,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a);facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,fr,a)
 if board:facade_box(m,x,y,u,.40,b+h/2,w+.10,.03,h+.10,M118['Plywood'],a)
 if hood:
  # the curved 1940s hood: a raised centre over two shoulders
  facade_box(m,x,y,u,.42,b+h+.30,w+.50,.10,.16,M118['Frame'],a)
  facade_box(m,x,y,u,.42,b+h+.46,w*.45,.10,.18,M118['Frame'],a)
def door118(m,x,y,u,b,w,h,a,leaf,frame):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
 facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,leaf,a)
 if w>1.2:facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,frame,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,frame,a)
def rows118(hs,z,Hh):
 # Window rows (bottom, height, width) above the ground for a zone.
 st=z.get('st',hs['st']);f0=hs.get('f0',0.0)
 if z['role']=='main' and hs.get('rows'):return [tuple(v) for v in hs['rows']]
 if z['osm']=='93293026':return [(3.1,1.75,1.1)]
 if z['osm']=='93292672':return [(2.5,1.7,1.1)]
 if Hh<2.9:return [(.9,.8,.8)]
 n=int(st)
 if n>=2 and f0>0 or n>=3:
  sh=(Hh-f0-.5)/n;return [(f0+i*sh+.85,min(1.45,sh-1.4),1.1) for i in range(n)]
 if n>=2:return [(.95,1.35,1.0),(max(Hh*.5+.75,Hh-1.85),1.25,1.0)]
 return [(.85,1.35 if Hh>3.2 else 1.15,1.0)]
def street_side118(r,sw):
 # the long side of the rectangle r nearest the given street wall (for dormers and roof lights)
 sides=[(r[0],r[1]),(r[2],r[3])]
 if sw:
  mx,my=(sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2;sides.sort(key=lambda pq:math.dist(((pq[0][0]+pq[1][0])/2,(pq[0][1]+pq[1][1])/2),(mx,my)))
 return sides[0]
WSTREET118={'93293023':'Söderportsgatan','93292672':'Söderportsgatan','93292679':'Söderportsgatan','93293026':'Söderportsgatan','93293038':'Söderportsgatan'}
def door_wall118(z,hs):
 nm=WSTREET118.get(z['osm'])
 if nm and nm in z.get('street_walls',{}):return z['street_walls'][nm]
 return z.get('street_wall')

meshes={}
for zone,z in Z118.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b118_new(z['mesh'],'Slottsområdet/Gamla stan')
# ---------------------------------------------------------------- walls, windows, doors
for zone,z in Z118.items():
 hs=HS118[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs118(Hh);ex=hs.get('extras',[])
 wm=M118[z['wall']];fr=hs.get('fr','Frame');trim=M118['Frame']
 rows=rows118(hs,z,Hh) if z['role'] in ('main','wing') or hs['st']>=3 else ([(.9,.8,.8)] if Hh>2.4 else [])
 if 'garages' in ex:rows=[]
 dwall=door_wall118(z,hs) if (z['role']=='main' and 'no_door' not in ex) else None
 f0=hs.get('f0',0.0);plinth=max(.35 if Hh>2.9 else .2,f0)
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs118(w['z0'])
  if L<.25:continue
  wins=[];mine=[]
  if w['kind']=='outer':
   if dwall and abs(w['p'][0]-dwall[0][0])<1e-6 and abs(w['p'][1]-dwall[0][1])<1e-6 and L>1.6:
    dh=hs.get('door_h',2.15);dw=1.1 if dh>2.5 else 1.0
    du=0.0 if (L<6 or 'quoins' in ex or z['osm'] in ('93293023',)) else -L/2+min(L*.35,3.0)
    if 'garage_door' in ex and L>8:mine.append(('garage',L/2-2.2,G+.02,2.5,2.1))
    mine.append(('door',du,G+((f0 if z['osm']=='93293026' else min(f0,.45)) if f0>0 else plinth*.5),dw,dh))
   if 'garages' in ex and L>5:
    n=max(1,int(L/3.0))
    for k in range(n):mine.append(('garage',-L/2+(k+.5)*L/n,G+.02,2.4,2.0))
   bay=2.9 if hs['st']>=3 else (2.7 if hs['st']>=2 else 2.9);n=int(L/bay+.3)
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for i,(b,hh,ww) in enumerate(rows):
     b=zabs118(b)
     if b<z0+.3 or b+hh>H-.25 or L<ww+1.0:continue
     if any(abs(u-du_)<(ww+dw_)/2+.30 and b<db+dh_+.2 for _,du_,db,dw_,dh_ in mine):continue
     wins.append((u,b,ww,hh,i))
   # small basement windows under a raised ground floor
   if f0>=1.0 and z['role'] in ('main','wing'):
    for k in range(n):
     u=-L/2+(k+.5)*L/n
     if not any(abs(u-du_)<1.2 for _,du_,db,dw_,dh_ in mine):wins.append((u,G+f0-.80,.7,.5,-1))
  holes=[(u,b,ww,hh,0) for u,b,ww,hh,i in wins]+[(du_,db,dw_,dh_,0) for _,du_,db,dw_,dh_ in mine]
  bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if z['boards']:boards115(m,w,max(z0,G+plinth+.02),H-.12,holes,wm)
  for u,b,ww,hh,i in wins:
   board='boarded_up' in ex and (i>=1 or u>0)
   window118(m,x,y,u,b,ww,hh,a,fr,board,'hoods' in ex and i>=0)
  for kind,du_,db,dw_,dh_ in mine:
   if kind=='garage':
    facade_box(m,x,y,du_,.15,db+dh_/2,dw_,.06,dh_,M118['GarageDoor'],a)
    for k in range(1,5):facade_box(m,x,y,du_,.19,db+k*dh_/5,dw_-.1,.02,.03,M118['Frame'],a)
    surround36(m,x,y,du_,db,dw_,dh_,a,M118['Frame'],.10,.40);continue
   leaf='GreenDoor' if 'door_green' in ex else ('Frame' if z['wall'] in ('Yellow','PaleYellow','Red') else 'Door')
   door118(m,x,y,du_,db,dw_,dh_,a,M118[leaf],M118['Frame'])
   if db>G+.12:steps115(m,x,y,du_,dw_+.5,db,a,M118['Step'])
   if 'door_green' in ex:
    # the carved surround: pilasters and a hood with a round crown over the door
    for s in (-1,1):facade_box(m,x,y,du_+s*(dw_/2+.20),.42,db+dh_/2,.18,.10,dh_+.1,M118['Frame'],a)
    facade_box(m,x,y,du_,.45,db+dh_+.22,dw_+.70,.16,.18,M118['Frame'],a)
    town_path(m,[lp(x,y,du_+.45*math.cos(math.pi*i/8),.44,db+dh_+.32+.30*math.sin(math.pi*i/8),a) for i in range(9)],.06,M118['GreenDoor'])
   if 'door_stone' in ex:
    surround36(m,x,y,du_,db,dw_,dh_,a,M118['Quoin'],.26,.42)
    facade_box(m,x,y,du_,.46,db+dh_+.36,dw_+.9,.14,.22,M118['Quoin'],a)
   if 'entrance_balcony' in ex:
    # the balcony over the entrance of Kungsgatan 13A, with a railing on three sides
    bz=G+3.55;facade_box(m,x,y,du_,.36+.55,bz,1.9,1.1,.14,M118['Stone'],a)
    town_rod(m,lp(x,y,du_-.95,1.43,bz+1.0,a),lp(x,y,du_+.95,1.43,bz+1.0,a),.025,M118['Iron'],6)
    for kk in range(11):town_rod(m,lp(x,y,du_-.95+kk*.19,1.43,bz+.07,a),lp(x,y,du_-.95+kk*.19,1.43,bz+1.0,a),.012,M118['Iron'],4)
  if w['kind']=='outer':facade_box(m,x,y,0,.40,(G+plinth)/2,L+.02,.10,G+plinth,M118['Stone'],a)
  if z['role'] not in ('annex',):facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,trim,a)
  if z['boards']:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+plinth)/2,.20,.10,H-G-plinth,M118['Frame'],a)
  if 'quoins' in ex and w['kind']=='outer':
   # light stone quoins at both corners, long and short blocks in turn
   k=0;zz=G+.35
   while zz<H-.3:
    bw=.62 if k%2==0 else .40
    for s in (-1,1):facade_box(m,x,y,s*(L/2-bw/2+.02),.40,zz+.15,bw,.06,.30,M118['Quoin'],a)
    zz+=.32;k+=1
  if 'balconies' in ex and w['kind']=='outer' and dwall and abs(w['p'][0]-dwall[0][0])<1e-6 and L>10:
   for i,(b,hh,ww) in enumerate(rows[1:]):
    for uu in (-L/4,L/4):
     bz=zabs118(b)-.15;facade_box(m,x,y,uu,.36+.65,bz,2.8,1.3,.14,M118['WhiteRender'],a)
     facade_box(m,x,y,uu,.36+1.28,bz+.55,2.8,.05,.95,M118['WhiteRender'],a)
     for s in (-1,1):facade_box(m,x,y,uu+s*1.38,.36+.65,bz+.55,.05,1.3,.95,M118['WhiteRender'],a)

# ---------------------------------------------------------------- roofs and features
for zone,z in Z118.items():
 hs=HS118[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs118(Hh);T=zabs118(z['top']);ex=hs.get('extras',[]) if z['role']=='main' else []
 if 'porch_glazed' in hs.get('extras',[]):
  # the porch stands at the north-east corner (vertex 0 of the outline), whichever zone holds it
  sw_=z.get('street_walls',{}).get('Söderportsgatan');c_=B98ID118[z['osm']]['outer'][0]
  ex=[e for e in ex if e!='porch_glazed']+(['porch_glazed'] if sw_ and min(math.dist(sw_[0],c_),math.dist(sw_[1],c_))<.6 else [])
 wm=M118[z['wall']];rm=M118[hs['rm']];fr=hs.get('fr','Frame')
 if z['role']=='annex' or z['roof']=='flat':
  flat118(m,z['polygons'],H,M118['RoofDark'],M118['Frame'] if z['boards'] else wm);continue
 r=[tuple(v) for v in z['rect']] if z.get('ridge_fixed') else long_first118(z['rect'])
 if hs.get('ridge')=='short' and z['role']=='main' and not z.get('ridge_fixed'):r=r[1:]+r[:1]
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2]);st=z.get('st',hs['st'])
 if z['roof'] in ('hip','low'):
  inset_roof(m,r,H,max(.3,min(Ls,Lt)/2-.30),T-H,rm,.45);sl=(T-H)/max(.5,min(Ls,Lt)/2)
 elif z['roof']=='mhip':
  k,ZB=mhip118(m,r,H,T,rm);sl=(ZB-H)/k
 elif z['roof']=='gambrel':
  k,ZB,ends=gambrel118(m,r,H,T,rm,wm)
  for p,q,c,n in ends:
   x,y,L,a=end_frame118(p,q,n)
   if T-H>2.4:
    if L>6.5:
     for s in (-1.1,1.1):window118(m,x,y,s,H+.45,.9,min(1.3,ZB-H-.4),a,fr)
    else:window118(m,x,y,0,H+.35,.8,min(1.1,ZB-H-.2),a,fr,'boarded_up' in hs.get('extras',[]))
  sl=(ZB-H)/k
 else:
  eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40 if st>=1 else .30)
  for p,q,c,n in ends:
   x,y,L,a=end_frame118(p,q,n)
   if T-H>2.3 and L>3.0 and not (z['role']=='main' and z['osm']=='93293023'):
    gh=min(1.1,(T-H)*.45)
    if st>=1.5 and L>6.5:
     for s in (-.8,.8):window118(m,x,y,s,H+.35,.7,gh,a,fr)
    else:window118(m,x,y,0,H+.35,.75,gh,a,fr)
   o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
   for u_ in (p,q):
    e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
    town_rod(m,(*o(e,.48),H-.35*sl-.04),(*o(c,.48),T-.04),.06,M118['Frame'],6)
 # chimneys on the ridge
 cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;d_=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d_[1],d_[0])
 cm=M118['ChimneyWhite'] if z['wall'] in ('White','WhiteRender','PaleYellowRender','Salmon','YellowRender','PaleGreen') else M118['Chimney']
 if 'chimneys2' in ex:
  for s in (-Ls*.25,Ls*.25):chimney115(m,cx_+d_[0]*s,cy_+d_[1]*s,T-.6,T+.8,cm,ang)
 elif 'chimney' in ex or (z['role']=='main' and st>=1.5 and Hh>3.4 and 'tower' not in ex):
  chimney115(m,cx_+d_[0]*Ls*.15,cy_+d_[1]*Ls*.15,T-.6,T+.7,cm,ang)
 sw=door_wall118(z,hs)
 # dormers on the street slope
 nd={'dormers2':2,'dormer1':1}.get(next((e for e in ex if e in ('dormers2','dormer1')),''),0)
 if 'dormers' in ex:nd=max(1,int(Ls/6.5))
 if nd and z['roof'] in ('saddle','hip','mhip'):
  p,q=street_side118(r,sw);x,y,L,a=sf_edge(p,q)
  if z['roof']=='mhip':
   # mansard dormers stand on the steep slope, their face near the wall
   for kk in range(nd):
    u=-L/2+(kk+.5)*L/nd
    dormer82(m,x,y,u,a,H,sl,1.4,1.1,wm,M118['Frame'],rm,.25)
  else:
   for kk in range(nd):
    u=-L/2+(kk+.5)*L/nd if nd>1 else 0.0
    if nd==2:u=(-1 if kk==0 else 1)*min(L*.22,3.2)
    dormer82(m,x,y,u,a,H,sl,1.5 if hs['st']<3 else 1.3,1.0,wm if not z['boards'] else M118['Frame'] if z['wall']=='White' else wm,M118['Frame'],rm,.9+(.3 if z['roof']=='hip' else 0))
 # roof lights on the street slope (the 1950s houses)
 if 'skylights' in ex and z['roof']=='saddle':
  p,q=street_side118(r,sw);x,y,L,a=sf_edge(p,q)
  for u in (-L*.30,-L*.18,L*.20):
   X,Y,_=lp(x,y,u,-1.6,0,a);skylight82(m,X,Y,H+1.6*sl+.05,a,sl)
 # the curved Jugend gable of 93292672 on Söderportsgatan: the white wall carried up from the eaves in
 # a bell curve to a crown 3.6 m higher, with an oculus and a pair of windows
 if 'jugend' in ex and sw:
  x,y,L,a=sf_edge(*sw);gw=min(6.2,L*.42);u0=L*.12
  prof=[]
  for i in range(13):
   t=i/12;uu=-gw/2+gw*t;s=abs(2*t-1)
   zz=H+1.1+(3.6-1.1)*(math.cos(s*math.pi/2)**1.4)
   prof.append((uu,zz))
  pts=[(-gw/2,H)]+prof+[(gw/2,H)]
  vs=[lp(x,y,u0+uu,o,zz,a) for o in (.005,.38) for uu,zz in pts];N=len(pts)
  m.faces(vs,[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]+[(i,i+1,N+i+1,N+i) for i in range(N-1)]+[(N-1,0,N,2*N-1)],M118['White'])
  town_path(m,[lp(x,y,u0+uu,.42,zz+.06,a) for uu,zz in prof],.08,M118['Frame'])
  k=14;rr=.42;zc=H+2.75
  m.faces([lp(x,y,u0+rr*math.cos(2*math.pi*i/k),.40,zc+rr*math.sin(2*math.pi*i/k),a) for i in range(k)],[tuple(range(k)),tuple(range(k-1,-1,-1))],GLAZE)
  town_path(m,[lp(x,y,u0+(rr+.07)*math.cos(2*math.pi*i/k),.42,zc+(rr+.07)*math.sin(2*math.pi*i/k),a) for i in range(k+1)],.06,M118['Frame'])
  for s in (-.6,.6):window118(m,x,y,u0+s,H+.35,.8,1.3,a,fr)
 # the corner tower of 93292679 at the south-east corner (the right end of the street front)
 if 'tower' in ex and sw:
  x,y,L,a=sf_edge(*sw);tw=3.8;TE=zabs118(8.2);TA=zabs118(10.6)
  c0=lp(x,y,L/2-tw/2+.15,-tw/2+.30,0,a)[:2]
  ring=[lp(c0[0],c0[1],uu,oo,0,a)[:2] for uu,oo in ((-tw/2,tw/2),(-tw/2,-tw/2),(tw/2,-tw/2),(tw/2,tw/2))]
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(ring,ring[1:]+ring[:1]))<0:ring=ring[::-1]
  cx2,cy2=sum(v[0] for v in ring)/4,sum(v[1] for v in ring)/4
  for p,q in zip(ring,ring[1:]+ring[:1]):
   tx,ty,tL,ta=sf_edge(p,q)
   holes=[(0,zabs118(1.0),1.0,1.4,0),(0,zabs118(4.0),1.0,1.3,0),(0,zabs118(6.6),.8,1.0,0)]
   bz_wall(m,p,q,G,TE,holes,M118['White'])
   for (uu,bb,ww,hh,_) in holes:window118(m,tx,ty,uu,bb,ww,hh,ta,fr)
   facade_box(m,tx,ty,0,.44,TE-.12,tL+.12,.16,.24,M118['Frame'],ta)
   facade_box(m,tx,ty,0,.40,(G+.35)/2,tL+.02,.10,G+.35,M118['Stone'],ta)
  pr=ring_offset(ring,.40)
  for i in range(4):
   j=(i+1)%4;m.faces([(*pr[i],TE-.15),(*pr[j],TE-.15),(cx2,cy2,TA)],[(0,1,2),(2,1,0)],M118['RoofTower'])
  town_rod(m,(cx2,cy2,TA-.1),(cx2,cy2,TA+.9),.03,M118['Iron'],6)
 # the cross gable over the west part of 93292679's street front
 if 'gable_left' in ex and sw:
  x,y,L,a=sf_edge(*sw);frontis83(m,x,y,-L/2+2.6,4.6,H,H+.25,T-.5,a,wm,M118['Frame'],rm,True)
 # the balcony between the cross gable and the tower
 if 'balcony' in ex and sw:
  x,y,L,a=sf_edge(*sw);u=L*.08;bz=zabs118(4.6)
  facade_box(m,x,y,u,.36+.7,bz,3.0,1.4,.16,M118['Frame'],a)
  town_rod(m,lp(x,y,u-1.5,1.72,bz+1.0,a),lp(x,y,u+1.5,1.72,bz+1.0,a),.04,M118['Frame'],6)
  for kk in range(16):facade_box(m,x,y,u-1.45+kk*.193,1.72,bz+.55,.05,.05,.9,M118['Frame'],a)
  for s in (-1,1):facade_box(m,x,y,u+s*1.4,1.62,(G+bz)/2,.16,.16,bz-G,M118['Frame'],a)
 # the glazed porch at the east end of 93293026's street front (two storeys, sp04_h142)
 if 'porch_glazed' in ex and sw:
  sw=z['street_walls']['Söderportsgatan'];x,y,L,a=sf_edge(*sw);pw,pd=2.6,1.8
  u=L/2-pw/2-.2 if U({'p':sw[0],'q':sw[1]},*c_)>0 else -L/2+pw/2+.2
  pb,pt=zabs118(1.8),zabs118(5.5)
  facade_box(m,x,y,u,.36+pd/2,(G+pb)/2,pw,pd,pb-G,M118['Stone'],a)
  facade_box(m,x,y,u,.36+pd/2,pb+.55,pw,pd,1.1,M118['PaleYellow'],a)
  for zz0,zz1 in ((pb+1.1,pb+2.3),(pb+2.6,pt-.3)):
   facade_box(m,x,y,u,.36+pd,(zz0+zz1)/2,pw-.1,.02,zz1-zz0,GLAZE,a)
   for s in (-1,1):facade_box(m,x,y,u+s*pw/2,.36+pd/2,(zz0+zz1)/2,.02,pd-.1,zz1-zz0,GLAZE,a)
   for kk in range(4):facade_box(m,x,y,u-pw/2+kk*pw/3,.36+pd+.02,(zz0+zz1)/2,.07,.07,zz1-zz0,M118['Frame'],a)
   for zz in (zz0,zz1):facade_box(m,x,y,u,.36+pd+.02,zz,pw,.08,.08,M118['Frame'],a)
  facade_box(m,x,y,u,.36+pd/2,pb+2.45,pw,pd,.30,M118['PaleYellow'],a)
  facade_box(m,x,y,u,.36+pd/2+.1,pt+.08,pw+.4,pd+.3,.16,M118['RoofDark'],a)
  for s in (-1,1):facade_box(m,x,y,u+s*(pw/2-.05),.36+pd-.05,(pb+pt)/2,.12,.12,pt-pb,M118['Frame'],a)

for nm,m in meshes.items():b118_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block118_cameras=[
 sv_camera('616_Block118_Cal_Soderportsgatan6S',-1086.26,-56.26,2.4,151,10),
 sv_camera('617_Block118_Cal_Soderportsgatan6N',-1085.86,-57.36,2.6,331,10),
 sv_camera('618_Block118_Cal_Soderportsgatan10',-1022.56,-54.7,2.27,145,10),
 sv_camera('619_Block118_Cal_Kungsgatan13A',-1120.67,166.8,2.6,212,10),
 ('620_Block118_Aerial',(-1000.0,-160.0,90.0),(-1090.0,40.0,2.0),24)]
print('BLOCK118_GEOMETRY',len(block118_names))
