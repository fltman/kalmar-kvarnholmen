"""Pass 119: the fourth and last Gamla stan pass on the mainland west of Kvarnholmen. Stora Dammgatan,
Lilla Dammgatan, Bremergatan, Smålandsgatan and Spikgatan. Pass 98 built these 22 houses as plain
volumes in its chunk meshes; each is now its own mesh SM_Slott119_<osm id> with its real form: storeys,
saddle, hipped, mansard (gambrel) or shallow hipped roofs in red tile, dark tile, green or dark sheet
metal, vertical boarding, render or brick in the house's colour, corner boards, eaves boards and window
frames, windows per storey, a door on the street, dormers, chimneys and the notable features:
- Bremergatan 9, the white rendered Jugend villa: green sheet hipped roof, the swept round-headed gable
  on the street with its three arched windows, the arched dormer, red-brown window frames, and the
  square entrance tower at its north corner with a cornice, arched windows and the green spire with
  its finial;
- Bremergatan 13, the four-storey public building: the granite plinth, the cream rusticated ground
  floor with arched windows, a cornice band, red-brick upper floors with cream pilaster strips, cream
  window surrounds and sill bands, green window frames and the main cornice; its pale yellow rendered
  corner range with floor bands under a red tile roof;
- the grey-beige rendered villa with the red tile hipped roof, the yellow boarded mansard house with
  the lunette, the yellow-brick house with the dark tile roof;
- on Stora and Lilla Dammgatan the red boarded two-storey house with the lunette in its gable, the long
  red one-and-a-half-storey house with knee-wall windows, and the yellow-brick 1950s apartment block
  with balconies, the glazed stair bay and a dormer;
- at the west end the white rendered house with its gable and balcony on the street and the long white
  two-storey house;
- houses seen in no photo get a plain form matched to their neighbours: boarded, a tile saddle roof,
  the storeys and colour from the street around them.
It also re-creates pass 98's chunk meshes the houses sit in with slott98_chunks115 (pass 115),
leaving out every house in SLOTT98_DETAILED.
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block119.json; see references/block119-notes.md.
"""
B119D=json.loads((R/'source/block119.json').read_text());Z119=B119D['zones'];HS119=B119D['houses'];G119=B119D['ground_z']
block119_names=[];B119={}
for old in [k for k in list(materials) if k.startswith('M_Block119_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownIvory',(.52,.18,.14),.85,0),('Yellow','TownIvory',(.87,.73,.40),.85,0),('PaleYellow','TownIvory',(.86,.82,.64),.85,0),
 ('White','TownPaintWhite',(.92,.92,.89),.80,0),('GreyBeige','TownIvory',(.74,.71,.64),.88,0),('Beige','TownIvory',(.85,.78,.62),.88,0),
 ('PaleYellowRender','TownIvory',(.90,.84,.62),.88,0),('YellowBrick','TownIvory',(.83,.74,.52),.92,0),('Brick','TownTileRed',(.50,.30,.25),.92,0),
 ('Cream','TownIvory',(.89,.85,.73),.88,0),('CreamShade','TownIvory',(.70,.66,.56),.90,0),('Granite','TownStone',(.42,.41,.40),.90,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('FrameRed','TownPaintBrown',(.42,.14,.12),.60,0),('FrameGreen','TownPaintGreen',(.22,.32,.24),.60,0),
 ('Tile','TownTileRed',(.66,.32,.22),.80,0),('TileDark','TownTileRed',(.20,.19,.19),.80,0),('RoofGreen','TownPaintGreen',(.38,.52,.44),.55,.30),
 ('RoofDark','TownMetalGrey',(.22,.22,.24),.60,.25),('RoofGrey','TownMetalGrey',(.36,.36,.37),.70,.15),
 ('Door','TownPaintBrown',(.30,.21,.15),.70,0),('DoorWood','TownPaintBrown',(.50,.33,.20),.70,0),
 ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Chimney','TownTileRed',(.55,.28,.22),.90,0),
 ('ChimneyWhite','TownIvory',(.86,.85,.81),.88,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),('Concrete','TownStone',(.72,.71,.68),.90,0),
 ]:
 name='M_Block119_'+key;B119[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block119_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M119=B119
def b119_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block119_names.append(name);return Mesh(name,category)
def drop_degenerate_faces119(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b119_finish(m,osm):
 obj=s21_finish(m);obj['block119_dropped_faces']=drop_degenerate_faces119(obj);print('BLOCK119_DROPPED',m.name,obj['block119_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=119;obj['reference_notes']='references/block119-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without these houses
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|set(B119D['ids'])
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in B119D['ids']},119,block119_names)
# slott98_chunks115 finishes the chunks with pass 115's finisher (detail_pass 98, rebuilt_by_pass 119).

# ---------------------------------------------------------------- helpers
G=G119
def zabs119(h):return G+h
def long_first119(r):
 # The rectangle's corners reordered so that r[0]->r[1] is a long side (counter-clockwise kept).
 r=[tuple(v) for v in r]
 return r if math.dist(r[0],r[1])>=math.dist(r[1],r[2])-.01 else r[1:]+r[:1]
def end_frame119(p,q,n):
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def gambrel119(m,r,H,T,ma,wall,ov=.35,verge=.30):
 # A Swedish mansard (gambrel) roof with gable ends (pass 116's form): steep lower slopes to the
 # break, 60 % of the rise up, low upper slopes to the ridge; the gables in the wall material.
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
 return k,ZB,((p0,p3,mid(p0,p3),(-d[0],-d[1])),(p1,p2,mid(p1,p2),d))
def flat119(m,polys,H,ma,trim):
 for g in polys:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.22,trim,a)
def window119(m,x,y,u,b,w,h,a,frame,sill=None,surround=None,arch=False,o=.16):
 # casement, surround and sill; an arched head (pass 115's arch) springing at the top when arch. On a
 # solid face (a gable slab or the tower) o=.41 sets the glass and casement just proud of the surface.
 fr=M119[frame];sr=M119[surround or frame];cas81(m,x,y,u,b,w,h,a,fr,o,3 if h>1.2 else 2)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38+max(0,o-.30),b+(h+(w/2 if arch else 0))/2,.12,.06,h+(w/2 if arch else 0),sr,a)
 if arch:arch115(m,x,y,u,b+h,w,a,sr,.40)
 else:facade_box(m,x,y,u,.38+max(0,o-.30),b+h+.06,w+.24,.06,.12,sr,a)
 facade_box(m,x,y,u,.45+max(0,o-.30),b-.05,w+.24,.18,.06,M119[sill or frame],a)
def door119(m,x,y,u,b,w,h,a,leaf,frame):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
 facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,leaf,a)
 if w>1.2:facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,frame,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,frame,a)
def lunette119(m,x,y,u,zs,r,a,frame,k=12):
 # A half-round gable window: glass, a frame ring, the sill and three radial bars.
 # The glass is a fan of triangles from the sill's midpoint, not one half-disc n-gon: the export
 # triangulates n-gons, and this one gave a sliver along its straight sill with a repeated corner
 # and no UV frame (loop 97914 of 93292001 in the first official build).
 cen=lp(x,y,u,.37,zs,a);arc=[lp(x,y,u+r*math.cos(math.pi*i/k),.37,zs+r*math.sin(math.pi*i/k),a) for i in range(k+1)]
 m.faces([cen]+arc,[f for i in range(k) for f in ((0,i+1,i+2),(0,i+2,i+1))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.06)*math.cos(math.pi*i/k),.41,zs+(r+.06)*math.sin(math.pi*i/k),a) for i in range(k+1)],.06,frame)
 facade_box(m,x,y,u,.41,zs-.03,2*r+.25,.10,.08,frame,a)
 for i in (1,2,3):town_rod(m,lp(x,y,u,.39,zs,a),lp(x,y,u+r*math.cos(math.pi*i/4),.39,zs+r*math.sin(math.pi*i/4),a),.022,frame,6)
def balcony119(m,x,y,u,z,w,d,a,slab,rail):
 # a slab on the wall with a solid railing panel at the front and sides
 facade_box(m,x,y,u,.36+d/2,z,w,d,.16,slab,a)
 facade_box(m,x,y,u,.36+d-.03,z+.55,w,.05,.95,rail,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.03),.36+d/2,z+.55,.05,d,.95,rail,a)
def rows119(hs,Hh,plinth):
 # window rows (bottom, height, width) above the ground for the house's storeys
 st=hs['st']
 if 'rows' in hs:return [tuple(r) for r in hs['rows']]
 if Hh<2.9:return [(.9,.8,.8)]
 if st>=3:
  n=int(st);fh=(Hh-plinth-.5)/n;return [(plinth+k*fh+.9,min(1.45,fh-1.35),1.1) for k in range(n)]
 if st>=2:return [(max(plinth+.6,.95),1.35,1.0),(max(Hh*.5+.75,Hh-1.85),1.25,1.0)]
 rr=[(max(plinth+.5,.85),1.35 if Hh>3.2 else 1.15,1.0)]
 if 'knee' in hs.get('extras',[]):rr.append((Hh-.85,.55,.9))
 return rr
def wall_by_v119(osm,i,j):
 # the zone wall that runs along the outline edge from vertex i to vertex j
 ring={b['id']:b['outer'] for b in B98D['buildings']}[osm];a_,b_=ring[i],ring[j]
 for zone,z in Z119.items():
  if z['osm']!=osm:continue
  for w in z['walls']:
   if w['kind']=='outer' and math.dist(w['p'],a_)<.3 and math.dist(w['q'],b_)<.3:return zone,w
 return None,None
CHIM119={'chimney','chimneys2'}

# ---------------------------------------------------------------- walls, windows and doors
meshes={}
for zone,z in Z119.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b119_new(z['mesh'],'Slottsområdet/Gamla stan')
for zone,z in Z119.items():
 hs=HS119[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs119(Hh);ex=hs.get('extras',[])
 wm=M119[z['wall']];frk=hs.get('fr','Frame');trim=M119['Frame'] if z['boards'] or z['wall'] not in ('Brick',) else M119['Cream']
 if z['wall'] in ('Brick','YellowBrick','GreyBeige','PaleYellowRender','Beige'):trim=M119['Cream'] if z['wall']=='Brick' else M119[z['wall']]
 public='public' in ex;plinth=hs.get('plinth',.35 if Hh>2.9 else .2)
 rows=rows119(hs,Hh,plinth) if z['role'] in ('main','wing') else rows119(dict(st=1),Hh,plinth)
 if public:
  # ground floor: arched windows, sill 2.1, springing 3.5 (r 0.7); upper floors: windows 2.0 high
  rows=[(2.1,1.4,1.4,'arch')]+[(f+.75,2.0,1.2,None) for f in (5.3,9.4,13.4) if f+2.9<Hh]
 else:rows=[(b,h,w,None) for b,h,w in rows]
 door=None
 if z['role']=='main' and z.get('street_wall') and 'no_door' not in ex:door=z['street_wall']
 for w in z['walls']:
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs119(w['z0'])
  if L<.25:continue
  wins=[];mine=[]
  if w['kind']=='outer':
   if door and math.dist(w['p'],door[0])<1e-3 and math.dist(w['q'],door[1])<1e-3 and L>1.6 and 'jugend' not in ex:
    dw=1.6 if public or hs['st']>=3 else 1.0;du=0.0 if L<6 or hs['st']>=3 else -L/2+min(L*.35,3.0)
    mine.append(('door',du,G+(plinth*.5 if not public else .45),dw,2.15 if not public else 3.0))
   bay=hs.get('bay',3.0 if public else (2.7 if hs['st']>=2 else 2.9));n=int(L/bay+.3)
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for b,hh,ww,kind in rows:
     b=zabs119(b);top=b+hh+(ww/2 if kind=='arch' else 0)
     if b<z0+.3 or top>H-.25 or L<ww+1.0:continue
     if any(abs(u-du_)<(ww+dw_)/2+.30 and b<db+dh+.2 for _,du_,db,dw_,dh in mine):continue
     wins.append((u,b,ww,hh,kind))
  holes=[(u,b,ww,hh,0) for u,b,ww,hh,k in wins]+[(du_,db,dw_,dh,0) for _,du_,db,dw_,dh in mine]
  if public and w['kind']=='outer':
   # cream rusticated ground floor under the cornice band at 5.3, red brick above
   GF=zabs119(5.3)
   bz_wall(m,w['p'],w['q'],z0,GF,[h_ for h_ in holes if h_[1]<GF],M119['Cream'])
   bz_wall(m,w['p'],w['q'],GF,H,[h_ for h_ in holes if h_[1]>=GF],wm)
   for k in range(1,9):
    zz=zabs119(plinth)+k*(5.3-plinth-.5)/9
    facade_box(m,x,y,0,.37,zz,L+.02,.03,.05,M119['CreamShade'],a)
   facade_box(m,x,y,0,.47,GF+.05,L+.2,.24,.40,M119['Cream'],a)       # the ground-floor cornice band
   for f in (9.4,13.4):
    if f+2<Hh:facade_box(m,x,y,0,.42,zabs119(f+.62),L+.1,.14,.16,M119['Cream'],a)  # sill bands
   # cream pilaster strips between pairs of bays on the brick floors
   nb=max(1,n)
   for k in range(0,nb+1,2):
    uu=-L/2+k*L/nb;uu=max(-L/2+.35,min(L/2-.35,uu))
    facade_box(m,x,y,uu,.40,(GF+H)/2,.70,.10,H-GF,M119['Cream'],a)
  else:bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if z['boards']:boards115(m,w,max(z0,G+plinth+.02),H-.12,holes,wm)
  surround='Cream' if public else ('Frame' if z['wall'] in ('YellowBrick',) else None)
  for u,b,ww,hh,kind in wins:
   window119(m,x,y,u,b,ww,hh,a,frk,frk if not public else 'Cream',surround,kind=='arch')
   if 'bands' in ex and b>G+4:facade_box(m,x,y,u,.40,b+hh+.35,ww+.5,.12,.12,M119['Frame'],a)  # cornice hoods
  for kind,du_,db,dw_,dh in mine:
   leaf='DoorWood' if public or z['wall'] in ('YellowBrick','Beige') else ('Frame' if z['wall'] in ('Yellow','PaleYellow','Red') else 'Door')
   door119(m,x,y,du_,db,dw_,dh,a,M119[leaf],M119['Cream'] if public else M119['Frame'])
   if public:arch115(m,x,y,du_,db+dh,dw_,a,M119['Cream'],.37)
   if db>G+.12:steps115(m,x,y,du_,dw_+.5,db,a,M119['Step'])
  if w['kind']=='outer':facade_box(m,x,y,0,.40,(G+plinth)/2,L+.02,.10,G+plinth,M119['Granite' if public or hs['st']>=3 else 'Stone'],a)
  if public:facade_box(m,x,y,0,.62,H-.30,L+.5,.55,.60,M119['Cream'],a)             # main cornice
  elif 'bands' in ex:
   for f in [zabs119(plinth+.5+k*(Hh-plinth-.5)/hs['st']) for k in range(1,int(hs['st']))]:facade_box(m,x,y,0,.42,f,L+.1,.14,.18,M119['Cream'],a)
   facade_box(m,x,y,0,.55,H-.25,L+.4,.40,.50,M119['Cream'],a)
  else:facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,trim,a)
  if z['boards']:
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+plinth)/2,.20,.10,H-G-plinth,M119['Frame'],a)

# ---------------------------------------------------------------- roofs and features
for zone,z in Z119.items():
 hs=HS119[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs119(Hh);T=zabs119(z['top']);ex=hs.get('extras',[]) if z['role']=='main' else []
 wm=M119[z['wall']];rm=M119[hs['rm']];fr=hs.get('fr','Frame')
 if z['role'] in ('annex','link') or z['roof']=='flat':
  flat119(m,z['polygons'],H,M119['RoofDark'],M119['Frame'] if z['boards'] else wm);continue
 r=long_first119(z['rect'])
 if hs.get('ridge')=='short' and z['role']=='main':r=r[1:]+r[:1]
 if hs.get('gable_street') and z['role']=='main' and z.get('street_wall'):
  # the gable on the street: the ridge runs across the street wall
  sw=z['street_wall'];sd=((sw[1][0]-sw[0][0]),(sw[1][1]-sw[0][1]))
  def _par(rr):return abs((rr[1][0]-rr[0][0])*sd[0]+(rr[1][1]-rr[0][1])*sd[1])/(math.dist(rr[0],rr[1])*math.hypot(*sd))
  if _par(r)>.7:r=r[1:]+r[:1]
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
 cm=M119['ChimneyWhite'] if z['wall'] in ('White','Cream','GreyBeige','PaleYellowRender','Beige') else M119['Chimney']
 if z['roof'] in ('hip','low'):
  inset_roof(m,r,H,max(.3,min(Ls,Lt)/2-.30),T-H,rm,hs.get('ov',.45 if z['roof']=='hip' else .60));sl=(T-H)/max(.5,min(Ls,Lt)/2)
  ends=()
 elif z['roof']=='gambrel':
  k,ZB,ends=gambrel119(m,r,H,T,rm,wm);sl=(ZB-H)/k
  for p,q,c,n in ends:
   x,y,L,a=end_frame119(p,q,n)
   for s in ((-1.1,1.1) if L>8 else (0,)):window119(m,x,y,s,H+.30,.8,min(1.2,ZB-H-.4),a,fr,o=.41)
   if 'lunette' in ex:lunette119(m,x,y,0,ZB+.05,min(.65,(T-ZB)*.8),a,M119['Frame'])
   o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
   for u_ in (p,q):
    km=(u_[0]+(c[0]-u_[0])*k/(L/2),u_[1]+(c[1]-u_[1])*k/(L/2))
    town_rod(m,(*o(u_,.40),H),(*o(km,.40),ZB),.06,M119['Frame'],6);town_rod(m,(*o(km,.40),ZB),(*o(c,.40),T),.06,M119['Frame'],6)
 else:
  eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40)
  for p,q,c,n in ends:
   x,y,L,a=end_frame119(p,q,n)
   if T-H>2.3 and L>3.0:
    gh=min(1.1,(T-H)*.45)
    if 'lunette' in ex:
     window119(m,x,y,0,H+.25,.75,min(1.0,gh),a,fr,o=.41);lunette119(m,x,y,0,H+.25+min(1.0,gh)+.45,.42,a,M119['Frame'])
    elif hs['st']>=1.5 and L>6.5:
     for s in (-.8,.8):window119(m,x,y,s,H+.35,.7,gh,a,fr,o=.41)
    else:window119(m,x,y,0,H+.35,.75,gh,a,fr,o=.41)
   o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
   for u_ in (p,q):
    e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
    town_rod(m,(*o(e,.48),H-.35*sl-.04),(*o(c,.48),T-.04),.06,M119['Frame'],6)
   if 'balcony_gable' in ex and z.get('street_wall') and abs(U({'p':z['street_wall'][0],'q':z['street_wall'][1]},*c))<.5 and \
      min(math.dist(c,v) for v in z['street_wall'])<L/2+.5:
    # the balcony on the street gable at the upper floor
    balcony119(m,x,y,0,G+2.9,2.6,1.1,a,M119['Concrete'],M119['Frame'])
 # chimneys on the ridge
 cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;d_=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d_[1],d_[0])
 if 'chimneys2' in ex:
  for s in (-Ls*.25,Ls*.25):chimney115(m,cx_+d_[0]*s,cy_+d_[1]*s,T-.6,T+.8,cm,ang)
 elif set(ex)&CHIM119 or (z['role']=='main' and hs['st']>=1 and Hh>2.9 and hs['st']<3 and 'jugend' not in ex):
  chimney115(m,cx_+d_[0]*Ls*.15,cy_+d_[1]*Ls*.15,T-.6,T+.7,cm,ang)
 # one dormer or roof window on the street slope
 if set(ex)&{'dormer_one','roof_window'} and z.get('street_wall'):
  sw=z['street_wall'];x,y,L,a=sf_edge(*sw)
  if 'roof_window' in ex:dormer82(m,x,y,0,a,H,sl,1.1,.55,rm,M119['Frame'],rm,1.2)
  else:dormer82(m,x,y,L*.15,a,H,sl,1.6,1.0,M119['White'],M119['Frame'],rm,.9)
 # balconies and the glazed stair bay of the apartment blocks on their long front
 if set(ex)&{'balconies','stair_bay'}:
  fw=max((w for w in z['walls'] if w['kind']=='outer'),key=lambda w:math.dist(w['p'],w['q']))
  if z['osm']=='93292007':fw=wall_by_v119('93292007',3,0)[1] or fw   # the long south-east front (ld01_h10)
  x,y,L,a=sf_edge(fw['p'],fw['q']);n_=int(hs['st'])
  if 'stair_bay' in ex:
   facade_box(m,x,y,0,.40,G+1.0+(H-G-1.8)/2,1.5,.06,H-G-1.8,GLAZE,a);cas81(m,x,y,0,G+1.0,1.5,H-G-1.8,a,M119['Frame'],.43,8)
   door119(m,x,y,0,G+.15,1.4,2.2,a,M119['DoorWood'],M119['Frame'])
   facade_box(m,x,y,0,.95,G+2.6,2.2,1.3,.14,M119['Concrete'],a)
  if 'balconies' in ex:
   fh=(Hh-.6-.5)/n_
   for k in range(1,n_):
    for uu in (-L*.30,L*.18):balcony119(m,x,y,uu,zabs119(.6+k*fh),2.8,1.2,a,M119['Concrete'],M119['Frame'])

# ---------------------------------------------------------------- Bremergatan 9: the Jugend villa
# Read on br01_h214: the swept round-headed gable over the south end of the street front (s 0-4.6 from
# vertex 3), its eaves at 5.4 and apex at 9.0; three arched windows in it; an arched dormer in the
# middle of the roof; the square entrance tower at the north corner (vertex 0), cornice 8.7, spire to
# 14.2 with a finial; the main eaves 4.5 and the big windows 1.4-3.9 above the base.
_zv,_wv=wall_by_v119('93309086',3,0)
if _wv:
 m=meshes['SM_Slott119_93309086'];x,y,L,a=sf_edge(_wv['p'],_wv['q']);zz=Z119[_zv];H=zabs119(zz['height']);T=zabs119(zz['top'])
 nx_,ny_=math.sin(a),-math.cos(a);dx_,dy_=math.cos(a),math.sin(a)
 cpt=lambda u,o:(x+dx_*u+nx_*o,y+dy_*u+ny_*o)     # u along the front from its middle, o outwards
 # the cross gable: a saddle over the south end, its ridge running in from the street front
 gw,gd,gH,gT=4.6,6.0,zabs119(5.0),zabs119(9.0);u0=-L/2+gw/2+.05
 uL,uR=u0-gw/2,u0+gw/2;rr=[cpt(uL,0),cpt(uL,-gd),cpt(uR,-gd),cpt(uR,0)]
 if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(rr,rr[1:]+rr[:1]))<0:rr=[cpt(uR,0),cpt(uR,-gd),cpt(uL,-gd),cpt(uL,0)]
 bz_wall(m,cpt(uL,0),cpt(uR,0),H-.05,gH,[],M119['White'])
 _e,gsl,gends=saddle115(m,rr,gH,gT,M119['RoofGreen'],M119['White'],.45,.30)
 for p,q,c,n in gends:
  if math.dist(c,cpt(u0,0))>1.0:continue
  gx,gy,gL,ga=end_frame119(p,q,n)
  # three arched windows, the middle one higher
  for s,hh in ((-1.05,.95),(0,1.2),(1.05,.95)):window119(m,gx,gy,s,gH+.30,.62,hh,ga,'FrameRed','FrameRed','Frame',True,.41)
  # the swept round-headed bargeboard on a half ellipse over the gable, with its eaves returns
  # The gable's outline swells above the straight rakes (a cosine arc from eaves to apex); the space
  # between the arc and the rakes is filled with roof sheet, and the white board runs on the arc.
  k=16;hw=gL/2+.35;z0_,z1_=gH-.20,gT+.15;us=[-hw+2*hw*i/k for i in range(k+1)]
  arc=[z0_+(z1_-z0_)*math.cos(math.pi/2*u/hw) for u in us];rake=[z0_+(z1_-z0_)*(1-abs(u)/hw) for u in us]
  for i in range(k):
   if arc[i]-rake[i]<.02 and arc[i+1]-rake[i+1]<.02:continue
   q=[lp(gx,gy,us[i],.50,rake[i],ga),lp(gx,gy,us[i+1],.50,rake[i+1],ga),lp(gx,gy,us[i+1],.50,arc[i+1],ga),lp(gx,gy,us[i],.50,arc[i],ga)]
   if arc[i]-rake[i]<.02:q=q[:3]
   elif arc[i+1]-rake[i+1]<.02:q=[q[0],q[1],q[3]]
   m.faces(q,[tuple(range(len(q))),tuple(range(len(q)-1,-1,-1))],M119['RoofGreen'])
  town_path(m,[lp(gx,gy,u,.56,z,ga) for u,z in zip(us,arc)],.12,M119['Frame'])
  for s in (-1,1):facade_box(m,gx,gy,s*(gL/2+.25),.60,gH-.30,.8,.55,.22,M119['Frame'],ga)
  facade_box(m,gx,gy,0,.45,gH+.12,gL+.4,.16,.12,M119['Frame'],ga)
 # the arched dormer in the middle of the front slope
 rs=[tuple(v) for v in zz['rect']];hsl=(T-H)/max(.5,min(math.dist(rs[0],rs[1]),math.dist(rs[1],rs[2]))/2)
 dormer82(m,x,y,.6,a,H,hsl,1.4,1.0,M119['White'],M119['FrameRed'],M119['RoofGreen'],.8)
 # the entrance tower at the north corner: 3.0 m square, 0.25 m past the end and 0.30 m in front
 tw,th,tsp,ttip=3.0,zabs119(8.7),zabs119(9.5),zabs119(14.2);tu=L/2-tw/2+.25;tc=cpt(tu,.30-tw/2)
 m.box((tc[0],tc[1],(G+th)/2),(tw,tw,th-G),M119['White'],a)
 m.box((tc[0],tc[1],th+.12),(tw+.6,tw+.6,.24),M119['Frame'],a)
 m.box((tc[0],tc[1],th+.40),(tw+.2,tw+.2,.32),M119['White'],a)
 # brackets under the cornice on the front face
 for k in range(7):
  bp=cpt(tu-tw/2+.2+k*(tw-.4)/6,.30+.10);m.box((bp[0],bp[1],th-.15),(.08,.20,.30),M119['Frame'],a)
 # the green spire: a flared pyramid to the tip, and the finial
 c2,s2=math.cos(a),math.sin(a);hv=lambda s,t,z:(tc[0]+c2*s-s2*t,tc[1]+s2*s+c2*t,z)
 e=(tw+.9)/2;e2=(tw+.1)/2
 ring0=[hv(-e,-e,th+.45),hv(e,-e,th+.45),hv(e,e,th+.45),hv(-e,e,th+.45)]
 ring1=[hv(-e2,-e2,tsp+.15),hv(e2,-e2,tsp+.15),hv(e2,e2,tsp+.15),hv(-e2,e2,tsp+.15)]
 tip=hv(0,0,ttip)
 m.faces(ring0+ring1+[tip],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,8),(5,6,8),(6,7,8),(7,4,8),(3,2,1,0)],M119['RoofGreen'])
 town_rod(m,tip,(tip[0],tip[1],ttip+1.0),.04,M119['Iron'],6);m.box((tip[0],tip[1],ttip+.55),(.5,.04,.04),M119['Iron'],a+.6)
 # the tower's front face: two arched windows above, the door on its steps below
 fx,fy=cpt(tu,.30-.355)
 for s in (-.42,.42):window119(m,fx,fy,s,zabs119(5.6),.55,1.2,a,'FrameRed','FrameRed','Frame',True,.41)
 door119(m,fx,fy,0,G+.55,1.2,2.3,a,M119['DoorWood'],M119['Frame'])
 facade_box(m,fx,fy,0,.33,G+.55+1.15,1.2,.06,2.3,M119['DoorWood'],a)
 steps115(m,fx,fy,0,1.8,G+.55,a,M119['Step'],.40)
 # the tower's north face: one arched window
 sp_=(tc[0]+dx_*(tw/2-.355),tc[1]+dy_*(tw/2-.355));window119(m,sp_[0],sp_[1],0,zabs119(5.6),.6,1.2,a+math.pi/2,'FrameRed','FrameRed','Frame',True,.41)

for nm,m in meshes.items():b119_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block119_cameras=[
 sv_camera('631_Block119_Cal_Bremergatan9',-892.5,213.7,2.3,214,10),
 sv_camera('632_Block119_Cal_Bremergatan13',-917.3,265.3,3.2,213,10),
 sv_camera('633_Block119_Cal_StoraDammgatan4',-1023.2,132.8,2.6,352,10),
 sv_camera('634_Block119_Cal_BremergatanVillas',-893.2,212.2,2.6,34,10),
 ('635_Block119_Aerial',(-860.0,140.0,90.0),(-960.0,230.0,2.0),24)]
print('BLOCK119_GEOMETRY',len(block119_names))
