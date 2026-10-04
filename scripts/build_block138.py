"""Pass 138: the mainland street houses along Stensövägen, Stensviksvägen, Långviksvägen and
Sturevägen, west and south-west of Drottning Margaretas väg. Pass 98 built these houses as plain
volumes in its chunk mesh W; 61 of them are now each its own mesh SM_Slott138_<osm id> with its real
form: storeys, saddle, hipped and gambrel roofs in red or red-brown tile or dark tile, render in the
house's colour, vertical boarding with white corner boards, brick, white (or red-brown, or dark) window
frames, a door on the street, basement windows, dormers, chimneys and the notable features:
- on Stensövägen near Ståthållaregatan the beige corner house with the shop door, the pink house with two
  chimneys, the white corner house with the dark red wall dormer, the pale yellow block with three broad
  dormers and the white block with the central gabled dormer; further west the grey-white villa with
  the dark mansard roof and the black balcony, the white boarded house, the beige villa with the hipped
  roof and the cream house with the cross gable;
- in the villa quarter between Sturevägen, Långviksvägen and Stensviksvägen the boarded villas in white,
  yellow, olive green, salmon and grey-blue, with cross gables over porches with balconies, the yellow
  villa's mansard roof, the white villa with the tower (a square stand-in for the octagonal tower with
  its spire), the white house with the tower-like top storey and its roof terrace, the brown boarded
  gable of the low villa on Sturevägen, the round gable window of the salmon house, the cream block with
  the dark red wall dormers;
- on Stensviksvägen the grey 1930s block with the hipped roof, the wall dormer, the pedimented double door
  and red-brown frames, the white villa with the balcony on its street gable, the yellow boarded houses,
  the brick block, the two new white houses at the east end (one with a set-back glazed top storey) and
  the garages and sheds of the back lots;
- houses seen in no photo get a plausible form from their neighbours.
It also re-creates pass 98's chunk mesh the houses sit in (W) with slott98_chunks115 (pass 115),
leaving out every house in SLOTT98_DETAILED (which keeps the ids of every earlier pass, those of passes
134 and 138 included).
References: Google Street View panoramas captured for this pass, resected on the OSM outlines where
noted, view only. Zones: source/block138.json; see references/block138-notes.md.
"""
# Pass 125 leaves numbers in the shared names TS and TC, which the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B138D=json.loads((R/'source/block138.json').read_text());Z138=B138D['zones'];HS138=B138D['houses'];G138=B138D['ground_z']
block138_names=[];B138={}
def mats138():
 # pass 82's material setup loop, in a function so that its loop names stay local
 for old in [k for k in list(materials) if k.startswith('M_Block138_')]:bpy.data.materials.remove(materials.pop(old))
 for key,texture,target,rough,metal in [
  ('Red','TownIvory',(.70,.32,.24),.88,0),('Cream','TownIvory',(.90,.84,.68),.88,0),('PaleCream','TownIvory',(.87,.85,.77),.88,0),
  ('GreyBeige','TownIvory',(.78,.77,.70),.88,0),('GreyWhite','TownIvory',(.86,.86,.84),.88,0),('WhiteRender','TownIvory',(.92,.91,.88),.88,0),
  ('Yellow','TownIvory',(.90,.78,.52),.88,0),('YellowDeep','TownIvory',(.87,.65,.32),.88,0),('Ochre','TownIvory',(.80,.62,.42),.88,0),
  ('Salmon','TownIvory',(.85,.55,.40),.88,0),('PaleYellowRender','TownIvory',(.89,.84,.64),.88,0),
  ('RedBoard','TownIvory',(.50,.15,.12),.85,0),('BrownBoard','TownPaintBrown',(.33,.24,.18),.80,0),('Weathered','TownPaintBrown',(.50,.42,.33),.85,0),
  ('GreyBoard','TownPaintWhite',(.62,.63,.62),.80,0),('White','TownPaintWhite',(.94,.94,.92),.80,0),('GreyGround','TownIvory',(.55,.56,.56),.85,0),
  ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('FrameRed','TownPaintBrown',(.55,.20,.17),.60,0),('FrameDark','TownMetalGrey',(.12,.12,.13),.50,.20),
  ('Tile','TownTileRed',(.70,.33,.22),.80,0),('TileBrown','TownTileRed',(.45,.22,.16),.80,0),('RoofDark','TownMetalGrey',(.22,.22,.24),.60,.25),
  ('RoofGrey','TownMetalGrey',(.52,.53,.54),.55,.30),('DormerRed','TownPaintBrown',(.45,.20,.15),.75,0),('Awning','TownPaintBrown',(.60,.18,.20),.80,0),
  ('Orange','TownIvory',(.86,.56,.32),.85,0),('Door','TownPaintBrown',(.30,.21,.15),.70,0),('GarageDoor','TownPaintWhite',(.70,.70,.68),.70,0),
  ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Chimney','TownTileRed',(.55,.28,.22),.90,0),
  ('ChimneyWhite','TownIvory',(.86,.85,.81),.88,0),('OchreYellow','TownIvory',(.86,.68,.38),.88,0),('YellowBrick','TownIvory',(.80,.70,.48),.92,0),
  ('GreyDirty','TownIvory',(.62,.60,.56),.90,0),('PaleGrey','TownPaintWhite',(.80,.80,.78),.85,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
  ('Pink','TownIvory',(.86,.68,.64),.88,0),('Sage','TownIvory',(.80,.78,.60),.88,0),('SageBoard','TownPaintGreen',(.66,.68,.56),.80,0),
  ('YellowBoard','TownPaintWhite',(.88,.74,.46),.80,0),('Charcoal','TownPaintBrown',(.20,.19,.18),.80,0),('LightBrick','TownIvory',(.80,.78,.72),.92,0),
  ('OrangeRender','TownIvory',(.84,.56,.38),.88,0),('RoofRed','TownMetalGrey',(.55,.25,.20),.55,.25),('DormerBrown','TownPaintBrown',(.36,.24,.18),.75,0),
  ('BlueGreyBoard','TownPaintWhite',(.52,.58,.64),.80,0),('SalmonBoard','TownPaintWhite',(.84,.56,.42),.80,0),('OliveBoard','TownPaintGreen',(.55,.56,.40),.80,0),
  ('RoofGreen','TownMetalGrey',(.30,.45,.36),.55,.25),('BrownBrick','TownIvory',(.62,.50,.40),.92,0),
  ]:
  name='M_Block138_'+key;B138[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
  mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block138_target_srgb']=list(target)
  ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
  mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
  for node in nodes:
   if node.bl_idname=='ShaderNodeTexImage' and node.image:
    twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
    if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
mats138()
M138=B138
def b138_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block138_names.append(name);return Mesh(name,category)
def drop_degenerate_faces138(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b138_finish(m,osm):
 obj=s21_finish(m);obj['block138_dropped_faces']=drop_degenerate_faces138(obj);print('BLOCK138_DROPPED',m.name,obj['block138_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=138;obj['reference_notes']='references/block138-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without these houses
# No house of this pass is demolished (source/block138.json['demolished'] is empty); every id gets its own mesh.
# 93326725 (clipped by pass 98's box, source/block138.json['left_clipped']) is not in the ids and stays in the chunk.
GONE138=set(B138D['ids'])|set(B138D.get('demolished',[]))
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|GONE138
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in GONE138},138,block138_names)
# slott98_chunks115 finishes the chunks with pass 115's finisher (detail_pass 98, rebuilt_by_pass 138).

# ---------------------------------------------------------------- helpers
# steps115 (pass 115) reads the shared name G as the ground level; it is set for this build only and
# given back at the end.
G_PREV138=globals().get('G');G=G138
def zabs138(h):return G138+h
def long_first138(r):
 r=[tuple(v) for v in r]
 return r if math.dist(r[0],r[1])>=math.dist(r[1],r[2])-.01 else r[1:]+r[:1]
def end_frame138(p,q,n):
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def gambrel138(m,r,H,T,ma,wall,ov=.35,verge=.30):
 # pass 118's Swedish mansard (gambrel) with gable ends: steep lower slopes 0.85 m in and 60 % of the
 # rise up, low upper slopes to the ridge (along r[0]->r[1]); the gables as pentagons in the wall material.
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
def mhip138(m,r,H,T,ma,ov=.40):
 # A hipped mansard: steep lower slopes from the eaves to the break (1.1 m in, 70 % of the rise up),
 # then a low hip to the top.
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2]);k=min(1.1,min(Ls,Lt)/4);ZB=H+(T-H)*.7
 outer,inner=inset_roof(m,r,H,k,ZB-H,ma,ov)
 inset_roof(m,[tuple(v) for v in inner],ZB,max(.3,min(Ls,Lt)/2-k-.3),T-ZB,ma,.12)
 return k,ZB
def simp138(g,tol=.02):
 # drops vertices that lie within tol of the line through their neighbours, spikes included: a flat
 # roof n-gon with such a vertex triangulates (in the export tail) into a sliver with no UV frame
 # (pass 136's 93361215 annex, first sandbox run there)
 g=[tuple(v) for v in g];changed=True
 while changed and len(g)>3:
  changed=False
  for i in range(len(g)):
   a,b,c=g[i-1],g[i],g[(i+1)%len(g)];L=math.dist(a,c)
   if L<1e-9 or abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/L<tol:g.pop(i);changed=True;break
 return g
def flat138(m,polys,H,ma,trim):
 for g in polys:
  g=simp138(clean115(g,.1))
  if len(g)<3 or abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1])))<.1:continue
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.22,trim,a)
def window138(m,x,y,u,b,w,h,a,frame='Frame',awning=False):
 # pass 116's window: casement, surround, sill; a red awning on the boarded villa
 fr=M138[frame];cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,fr,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a);facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,fr,a)
 if awning:awning82(m,x,y,u,b+h,w+.3,a,M138['Awning'],.55,.7)
def door138(m,x,y,u,b,w,h,a,leaf,frame):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
 facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,leaf,a)
 if w>1.2:facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,frame,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,frame,a)
def archdoor138(m,x,y,u,b,w,h,a,leaf,frame):
 # an arched door: the leaf, a fan light in the arch (a triangle fan, see the export notes), the frame
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.70,w-.36,.02,h*.35,GLAZE,a)
 r=w/2;k=10;c=lp(x,y,u,.10,b+h,a)
 pts=[lp(x,y,u+r*math.cos(math.pi*i/k),.10,b+h+r*math.sin(math.pi*i/k),a) for i in range(k+1)]
 m.faces([c]+pts,[(0,i+1,i+2) for i in range(k)]+[(0,i+2,i+1) for i in range(k)],GLAZE)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+(h+r)/2,.12,.06,h+r,frame,a)
 town_path(m,[lp(x,y,u+(r+.06)*math.cos(math.pi*i/k),.38,b+h+(r+.06)*math.sin(math.pi*i/k),a) for i in range(k+1)],.06,frame)
def rows138(hs,z,Hh):
 # window rows (bottom, height, width) above the ground for a zone
 st=z.get('st',hs['st']);f0=hs.get('f0',0.0)
 if Hh<2.9:return [(.9,.8,.8)]
 n=int(st)
 if n>=2 and f0>0 or n>=3:
  sh=(Hh-f0-.5)/n;return [(f0+i*sh+.85,min(1.45,sh-1.4),1.1) for i in range(n)]
 if n>=2:return [(.95,1.35,1.0),(max(Hh*.5+.75,Hh-1.85),1.25,1.0)]
 return [(max(.85,f0+.6),1.35 if Hh>3.2 else 1.15,1.0)]
MINE138=('Stensövägen','Stensviksvägen','Långviksvägen','Sturevägen')
def door_wall138(z):
 # the wall on the pass's street when the zone faces one, else the nearest street's
 if z.get('street') in MINE138 or not z.get('street_walls'):return z.get('street_wall')
 for nm in MINE138:
  if nm in z['street_walls']:return z['street_walls'][nm]
 return z.get('street_wall')
def street_side138(r,sw):
 sides=[(r[0],r[1]),(r[2],r[3])]
 if sw:
  mx,my=(sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2;sides.sort(key=lambda pq:math.dist(((pq[0][0]+pq[1][0])/2,(pq[0][1]+pq[1][1])/2),(mx,my)))
 return sides[0]
def west_u138(sw,inset):
 # u of the point 'inset' metres in from the west (smaller x) end of the wall sw
 p,q=sw;x,y,L,a=sf_edge(p,q);end=p if p[0]<q[0] else q;ue=U({'p':p,'q':q},*end)
 return ue-math.copysign(inset,ue) if L>2*inset else 0.0
def gdormer138(m,x,y,u,a,H,sl,w,h,body,frame,roof,back=.6):
 # a gabled dormer: pass 82's box dormer with a small saddle roof and a pediment in the body colour
 dormer82(m,x,y,u,a,H,sl,w,h,body,frame,roof,back)
 zb=H+(back+.40-.355+.05)*sl-.15;zt=zb+h+.55;dep=2.2;o0=.355-back+.05;o1=o0-dep
 pts=[lp(x,y,u-w/2-.15,o0+.1,zt+.1,a),lp(x,y,u+w/2+.15,o0+.1,zt+.1,a),lp(x,y,u+w/2+.15,o1,zt+.1,a),lp(x,y,u-w/2-.15,o1,zt+.1,a),lp(x,y,u,o0+.1,zt+.1+w*.45,a),lp(x,y,u,o1,zt+.1+w*.45,a)]
 m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],roof)
 town_path(m,[lp(x,y,u-w/2-.1,o0+.14,zt+.12,a),lp(x,y,u,o0+.14,zt+.12+w*.43,a),lp(x,y,u+w/2+.1,o0+.14,zt+.12,a)],.05,frame)

def build138_houses():
 # The houses, in a function so that its loop names (H, T, m, x, y, ...) stay local and no shared
 # global name is clobbered (see pass 125's TS/TC).
 meshes={}
 for zone,z in Z138.items():
  if z['mesh'] not in meshes:meshes[z['mesh']]=b138_new(z['mesh'],'Slottsområdet/Mainland')
 # ---------------------------------------------------------------- walls, windows, doors
 for zone,z in Z138.items():
  hs=HS138[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs138(Hh);ex=hs.get('extras',[]) if z['role']=='main' else []
  wm=M138[z['wall']];fr=z.get('fr',hs.get('fr','Frame'));trim=M138['Frame'];st=z.get('st',hs['st'])
  rows=rows138(hs,z,Hh) if z['role'] in ('main','wing') or st>=3 else ([(.9,.8,.8)] if Hh>2.4 else [])
  dwall=door_wall138(z) if (z['role']=='main' and 'no_door' not in ex) else None
  f0=hs.get('f0',0.0);plinth=max(.35 if Hh>2.9 else .2,min(f0,1.0))
  for w in z['walls']:
   x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs138(w['z0'])
   if L<.25:continue
   wins=[];mine=[];isdoor=False
   if w['kind']=='outer':
    if dwall and abs(w['p'][0]-dwall[0][0])<1e-6 and abs(w['p'][1]-dwall[0][1])<1e-6 and L>1.6:
     isdoor=True;dh=2.15;dw=1.0
     du=0.0 if L<6 else -L/2+min(L*.35,3.0)
     if 'arch_door' in ex:du=west_u138(dwall,1.4)
     if 'door_mid' in ex:du=0.0  # the door in the centre of the front (pass 136's 93358523; here 93460234)
     if 'pediment' in ex:dw=1.8  # the double door of 93460234 (sv05_h150)
     if 'garage_door' in ex:mine.append(('garage',0.0,G+.02,2.5,2.0))
     else:mine.append(('arch' if 'arch_door' in ex else 'door',du,G+(min(f0,.45) if f0>0 else plinth*.5),1.1 if 'arch_door' in ex else dw,1.9 if 'arch_door' in ex else dh))
    bay=2.9 if st>=3 else 2.7 if st>=2 else 2.9;n=int(L/bay+.3)
    for k in range(n):
     u=-L/2+(k+.5)*L/n
     for i,(b,hh,ww) in enumerate(rows):
      b=zabs138(b)
      if b<z0+.3 or b+hh>H-.25 or L<ww+1.0:continue
      if any(abs(u-du_)<(ww+dw_)/2+.30 and (kind_=='bay' or b<db+dh_+.2) for kind_,du_,db,dw_,dh_ in mine):continue
      wins.append((u,b,ww,hh,i))
    if f0>=1.0 and z['role'] in ('main','wing'):
     for k in range(n):
      u=-L/2+(k+.5)*L/n
      if not any(abs(u-du_)<1.2 for _,du_,db,dw_,dh_ in mine):wins.append((u,G+f0-.80,.7,.5,-1))
   holes=[(u,b,ww,hh,0) for u,b,ww,hh,i in wins]+[(du_,db,dw_,dh_,dw_/2 if kind_=='arch' else 0) for kind_,du_,db,dw_,dh_ in mine if kind_!='bay']
   bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
   if z['boards']:boards115(m,w,max(z0,G+plinth+.02),H-.12,holes,wm)
   for u,b,ww,hh,i in wins:window138(m,x,y,u,b,ww,hh,a,fr,'awnings' in ex and i>=0)
   for kind,du_,db,dw_,dh_ in mine:
    if kind=='garage':
     facade_box(m,x,y,du_,.15,db+dh_/2,dw_,.06,dh_,M138['GarageDoor'],a)
     for k in range(1,5):facade_box(m,x,y,du_,.19,db+k*dh_/5,dw_-.1,.02,.03,M138['Frame'],a)
     surround36(m,x,y,du_,db,dw_,dh_,a,M138['Frame'],.10,.40);continue
    leaf=M138['Door']
    if kind=='arch':
     archdoor138(m,x,y,du_,db,dw_,dh_,a,leaf,M138['Frame'])
     surround36(m,x,y,du_,db,dw_,dh_+dw_/2,a,M138['Stone'],.18,.42)
    else:door138(m,x,y,du_,db,dw_,dh_,a,leaf,M138['Frame'])
    if 'pediment' in ex:
     # the pedimented door surround of 93460234 (sv05_h150): white pilasters, an entablature and a
     # triangular pediment (a double-sided triangle)
     for s_ in (-1,1):facade_box(m,x,y,du_+s_*(dw_/2+.32),.44,db+(dh_+.3)/2,.26,.14,dh_+.3,M138['WhiteRender'],a)
     facade_box(m,x,y,du_,.46,db+dh_+.42,dw_+1.2,.20,.24,M138['WhiteRender'],a)
     pts=[lp(x,y,du_-(dw_/2+.62),.48,db+dh_+.54,a),lp(x,y,du_+(dw_/2+.62),.48,db+dh_+.54,a),lp(x,y,du_,.48,db+dh_+1.15,a)]
     m.faces(pts,[(0,1,2),(2,1,0)],M138['WhiteRender'])
    if 'oculus_door' in ex:
     # the round window over the door (pass 136's 93358523; unused here), a triangle fan in a white frame
     kk=14;rw=.36;zc=db+dh_+.62;cc=lp(x,y,du_,.40,zc,a)
     m.faces([cc]+[lp(x,y,du_+rw*math.cos(2*math.pi*i/kk),.40,zc+rw*math.sin(2*math.pi*i/kk),a) for i in range(kk)],[(0,i+1,(i+1)%kk+1) for i in range(kk)]+[(0,(i+1)%kk+1,i+1) for i in range(kk)],GLAZE)
     town_path(m,[lp(x,y,du_+(rw+.07)*math.cos(2*math.pi*i/kk),.42,zc+(rw+.07)*math.sin(2*math.pi*i/kk),a) for i in range(kk+1)],.07,M138['Frame'])
    if db>G+.12:steps115(m,x,y,du_,dw_+.5,db,a,M138['Step'])
    if 'entrance_balcony' in ex or 'balcony_small' in ex:
     # the small balcony over the entrance, a railing on three sides
     bz=zabs138(rows[1][0])-.15 if len(rows)>1 else H-1.9;facade_box(m,x,y,du_,.36+.45,bz,1.6,.9,.14,M138['Stone'],a)
     town_rod(m,lp(x,y,du_-.8,1.23,bz+1.0,a),lp(x,y,du_+.8,1.23,bz+1.0,a),.025,M138['Iron'],6)
     for kk in range(9):town_rod(m,lp(x,y,du_-.8+kk*.2,1.23,bz+.07,a),lp(x,y,du_-.8+kk*.2,1.23,bz+1.0,a),.012,M138['Iron'],4)
     for s in (-1,1):town_rod(m,lp(x,y,du_+s*.8,.38,bz+1.0,a),lp(x,y,du_+s*.8,1.23,bz+1.0,a),.02,M138['Iron'],4)
    if 'canopy' in ex:
     # the entrance canopy: two posts and a small gabled roof (red frame on the 1990s block)
     cm=M138['DormerRed'] if z['wall']=='Yellow' else M138['WhiteRender'];zc=db+dh_+.35
     for s in (-1,1):facade_box(m,x,y,du_+s*.85,1.45,(G+zc)/2,.12,.12,zc-G,cm,a)
     pts=[lp(x,y,du_-1.05,1.65,zc,a),lp(x,y,du_+1.05,1.65,zc,a),lp(x,y,du_+1.05,.36,zc,a),lp(x,y,du_-1.05,.36,zc,a),lp(x,y,du_,1.65,zc+.55,a),lp(x,y,du_,.36,zc+.55,a)]
     m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],M138['RoofGrey'])
     town_path(m,[lp(x,y,du_-1.05,1.68,zc,a),lp(x,y,du_,1.68,zc+.55,a),lp(x,y,du_+1.05,1.68,zc,a)],.06,cm)
   if w['kind']=='outer':facade_box(m,x,y,0,.40,(G+plinth)/2,L+.02,.10,G+plinth,M138['Stone'],a)
   if z['role'] not in ('annex',):facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,trim,a)
   if z['boards']:
    for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+plinth)/2,.20,.10,H-G-plinth,M138['Frame'],a)
   if isdoor and 'oriel' in ex:
    # the white oriel on the upper floor of the street front (93358536; the bay window under the
    # grey section's gable, 93358528, sits in the middle): a closed box on brackets, glazed on three sides
    uu=0.0 if 'gable_mid' in ex else -L*.25
    if hs.get('oriel_near'):
     # 3 m in from the end of the front at the named neighbour (read on se02_h231)
     J=next(b['outer'] for b in B98D['buildings'] if b['id']==hs['oriel_near']);jx,jy=sum(v[0] for v in J)/len(J),sum(v[1] for v in J)/len(J)
     ue=min(((U(w,*e),e) for e in (w['p'],w['q'])),key=lambda t:math.dist(t[1],(jx,jy)))[0];uu=ue-math.copysign(3.0,ue)
    zb=zabs138(3.3) if st<3 else zabs138(rows[1][0])-.45;zt_=min(H-.6,zb+2.6)
    facade_box(m,x,y,uu,.355+.35,(zb+zt_)/2,2.8,.70,zt_-zb,M138['White'],a)
    facade_box(m,x,y,uu,.355+.72,(zb+zt_)/2+.05,2.4,.02,zt_-zb-.6,GLAZE,a)
    for s_ in (-1,0,1):facade_box(m,x,y,uu+s_*1.2,.355+.74,(zb+zt_)/2+.05,.08,.04,zt_-zb-.6,M138['Frame'],a)
    for s_ in (-1,1):facade_box(m,x,y,uu+s_*1.15,.355+.25,zb-.25,.14,.50,.40,M138['White'],a)
   if isdoor and 'balcony' in ex:
    # a porch on posts at the door with a balcony on its roof (pass 118's 'balcony')
    u=next((mm[1] for mm in mine if mm[0] in ('door','arch')),0.0)
    bz=min(zabs138(3.2),H-.4)
    facade_box(m,x,y,u,.36+.8,bz,2.8,1.6,.16,M138['Frame'],a)
    town_rod(m,lp(x,y,u-1.4,1.92,bz+1.0,a),lp(x,y,u+1.4,1.92,bz+1.0,a),.04,M138['Frame'],6)
    for kk in range(15):facade_box(m,x,y,u-1.35+kk*.193,1.92,bz+.55,.05,.05,.9,M138['Frame'],a)
    for s in (-1,1):facade_box(m,x,y,u+s*1.3,1.82,(G+bz)/2,.16,.16,bz-G,M138['Frame'],a)
   if isdoor and 'gable_balcony' in ex:
    # the balcony on the street gable of 93460157 (sv03_h324): a slab at the eaves with an iron-grey
    # railing on three sides, in the middle of the gable
    bz=H-.05;facade_box(m,x,y,0,.355+.7,bz,3.4,1.4,.14,M138['Frame'],a)
    town_rod(m,lp(x,y,-1.7,1.42,bz+1.0,a),lp(x,y,1.7,1.42,bz+1.0,a),.03,M138['Iron'],6)
    for kk in range(18):town_rod(m,lp(x,y,-1.7+kk*.2,1.42,bz+.07,a),lp(x,y,-1.7+kk*.2,1.42,bz+1.0,a),.012,M138['Iron'],4)
    for s in (-1,1):town_rod(m,lp(x,y,s*1.7,.38,bz+1.0,a),lp(x,y,s*1.7,1.42,bz+1.0,a),.02,M138['Iron'],4)
   if isdoor and 'tower' in ex:
    # the tower-like top storey of 93460185 (lv01_h155): a square block 3.6 m wide at one end of the
    # street front (which end is estimated), rising 2.6 m over the eaves, flat-topped, with a window
    # on its front and a railing round its roof terrace; built from 0.3 m under the eaves so that it
    # does not lie on the wall below
    TW=3.6;tu=L/2-TW/2-.3 if L>TW+1 else 0.0;zt=H+2.6;zb=H-.3
    facade_box(m,x,y,tu,.355-TW/2,(zb+zt)/2,TW,TW,zt-zb,wm,a)
    facade_box(m,x,y,tu,.355-TW/2,zt+.08,TW+.3,TW+.3,.16,M138['Frame'],a)
    facade_box(m,x,y,tu,.37,H+1.15,.9,.02,1.2,GLAZE,a);surround36(m,x,y,tu,H+.55,.9,1.2,a,M138['Frame'],.08,.40)
    cs=[lp(x,y,tu+su*(TW/2+.1),so,zt+1.0,a) for su,so in ((-1,.455),(1,.455),(1,.255-TW),(-1,.255-TW))]
    for i_ in range(4):
     town_rod(m,cs[i_],cs[(i_+1)%4],.03,M138['Frame'],6)
     town_rod(m,(cs[i_][0],cs[i_][1],zt+.16),cs[i_],.03,M138['Frame'],4)
   if isdoor and 'spire' in ex:
    # the tower of 93460161 (lv02_h150, lv03_h145), octagonal with a spire in the photos: drawn as a
    # square tower 3.0 m wide standing 0.6 m out of one end of the street front (which end is
    # estimated), to 1.4 m over the eaves, under a dark pyramid roof 3.2 m high, windows on its front
    TW=3.0;tu=-L/2+TW/2+.2 if L>TW+1 else 0.0;zt=H+1.4;oc=.955-TW/2
    facade_box(m,x,y,tu,oc,(G+zt)/2,TW,TW,zt-G,wm,a)
    for zz in (G+1.0,H+.1):facade_box(m,x,y,tu,.97,zz+.6,.8,.02,1.2,GLAZE,a);surround36(m,x,y,tu,zz,.8,1.2,a,M138['Frame'],.08,1.0)
    sq=[lp(x,y,tu+su*TW/2,oc+so*TW/2,0,a)[:2] for su,so in ((-1,-1),(1,-1),(1,1),(-1,1))]
    if sum(p_[0]*q_[1]-q_[0]*p_[1] for p_,q_ in zip(sq,sq[1:]+sq[:1]))<0:sq=sq[::-1]
    inset_roof(m,sq,zt,TW/2-.06,3.2,M138['RoofDark'],.25)

 # ---------------------------------------------------------------- roofs and features
 for zone,z in Z138.items():
  hs=HS138[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs138(Hh);T=zabs138(z['top']);ex=hs.get('extras',[]) if z['role']=='main' else []
  wm=M138[z['wall']];rm=M138[z.get('rm',hs['rm'])];fr=z.get('fr',hs.get('fr','Frame'));st=z.get('st',hs['st'])
  if z['role']=='annex' or z['roof']=='flat':
   flat138(m,z['polygons'],H,M138['RoofDark'],M138['Frame'] if z['boards'] else wm)
   if 'glass_top' in ex:
    # the glazed, set-back top storey of the new house 93477789 (sv04_h330) with its thin flat roof
    # (pass 134's 'glass_top')
    for g in z['polygons']:
     g=simp138(clean115(g,.1))
     if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
     ug=ring_offset(g,-1.2);UH=H+2.6
     for p,q in zip(ug,ug[1:]+ug[:1]):
      x,y,L,a=sf_edge(p,q)
      if L<.3:continue
      facade_box(m,x,y,0,0,H+1.32,L,.04,2.5,GLAZE,a)
      for k in range(int(L/1.2)+1):facade_box(m,x,y,-L/2+k*L/max(1,int(L/1.2)),.03,H+1.32,.06,.08,2.5,M138['FrameDark'],a)
      facade_box(m,x,y,0,.25,UH,L+.6,.6,.2,M138['WhiteRender'],a)
     m.faces([(*v,UH+.1) for v in ug],[tuple(range(len(ug))),tuple(range(len(ug)-1,-1,-1))],M138['RoofDark'])
   continue
  r=[tuple(v) for v in z['rect']] if z.get('ridge_fixed') else long_first138(z['rect'])
  sw0=door_wall138(z) if hs.get('ridge')=='street' and z['role']=='main' and not z.get('ridge_fixed') else None
  if sw0:
   # the ridge parallel to the street wall (the rows on the avenue and on Sankt Eriks gata)
   ex_,ey_=sw0[1][0]-sw0[0][0],sw0[1][1]-sw0[0][1];Lw=math.hypot(ex_,ey_)
   if Lw>0 and abs(((r[1][0]-r[0][0])*ex_+(r[1][1]-r[0][1])*ey_)/(math.dist(r[0],r[1])*Lw))<.7:r=r[1:]+r[:1]
  sw1=door_wall138(z) if hs.get('ridge')=='across' and z['role']=='main' and not z.get('ridge_fixed') else None
  if sw1:
   # the ridge at right angles to the street wall: the gable on the street (93329949)
   ex_,ey_=sw1[1][0]-sw1[0][0],sw1[1][1]-sw1[0][1];Lw=math.hypot(ex_,ey_)
   if Lw>0 and abs(((r[1][0]-r[0][0])*ex_+(r[1][1]-r[0][1])*ey_)/(math.dist(r[0],r[1])*Lw))>.7:r=r[1:]+r[:1]
  Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
  if z['roof'] in ('hip','low'):
   inset_roof(m,r,H,max(.3,min(Ls,Lt)/2-.30),T-H,rm,.45);sl=(T-H)/max(.5,min(Ls,Lt)/2)
  elif z['roof']=='mhip':
   k,ZB=mhip138(m,r,H,T,rm);sl=(ZB-H)/k
   if z['role']=='wing':
    # the roof storey's windows: dormers on all four steep slopes
    for i in range(4):
     p,q=r[i],r[(i+1)%4];x,y,L,a=sf_edge(p,q)
     for kk in range(max(1,int(L/3.2))):dormer82(m,x,y,-L/2+(kk+.5)*L/max(1,int(L/3.2)),a,H,sl,1.3,1.1,rm,M138['Frame'],rm,.25)
  elif z['roof']=='gambrel':
   k,ZB,ends=gambrel138(m,r,H,T,rm,wm)
   for p,q,c,n in ends:
    x,y,L,a=end_frame138(p,q,n)
    if T-H>2.4:
     if L>6.5:
      for s in (-1.1,1.1):window138(m,x,y,s,H+.45,.9,min(1.3,ZB-H-.4),a,fr)
     else:window138(m,x,y,0,H+.35,.8,min(1.1,ZB-H-.2),a,fr)
   sl=(ZB-H)/k
  else:
   eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40 if st>=1 else .30)
   for p,q,c,n in ends:
    x,y,L,a=end_frame138(p,q,n)
    if 'gable_boards' in ex:
     # the dark brown boarded gable of 93460152 (su01_h100): a triangle over the gable wall
     gb=[lp(x,y,-L/2,.40,H,a),lp(x,y,L/2,.40,H,a),lp(x,y,0,.40,T-.05,a)];m.faces(gb,[(0,1,2),(2,1,0)],M138['BrownBoard'])
    elif 'oculus_end' in ex and T-H>2.3 and L>3.0:
     # the round gable window of 93460238 (su02_h90), a triangle fan in a white frame
     kk=14;rw=.35;zc=H+(T-H)*.42;cc=lp(x,y,0.0,.40,zc,a)
     m.faces([cc]+[lp(x,y,rw*math.cos(2*math.pi*i/kk),.40,zc+rw*math.sin(2*math.pi*i/kk),a) for i in range(kk)],[(0,i+1,(i+1)%kk+1) for i in range(kk)]+[(0,(i+1)%kk+1,i+1) for i in range(kk)],GLAZE)
     town_path(m,[lp(x,y,(rw+.07)*math.cos(2*math.pi*i/kk),.42,zc+(rw+.07)*math.sin(2*math.pi*i/kk),a) for i in range(kk+1)],.06,M138['Frame'])
    elif T-H>2.3 and L>3.0 and z['role']!='annex':
     gh=min(1.1,(T-H)*.45)
     if st>=1.5 and L>6.5:
      for s in (-.8,.8):window138(m,x,y,s,H+.35,.7,gh,a,fr)
     else:window138(m,x,y,0,H+.35,.75,gh,a,fr)
    o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
    for u_ in (p,q):
     e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
     town_rod(m,(*o(e,.48),H-.35*sl-.04),(*o(c,.48),T-.04),.06,M138['Frame'],6)
  # chimneys on the ridge
  cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;d_=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d_[1],d_[0])
  cm=M138['ChimneyWhite'] if z['wall'] in ('White','WhiteRender','Cream','PaleCream','GreyWhite','PaleYellowRender','PaleGrey') else M138['Chimney']
  if 'chimneys2' in ex:
   for s in (-Ls*.25,Ls*.25):chimney115(m,cx_+d_[0]*s,cy_+d_[1]*s,T-.6,T+.8,cm,ang)
  elif 'chimney' in ex:chimney115(m,cx_+d_[0]*Ls*.15,cy_+d_[1]*Ls*.15,T-.6,T+.7,cm,ang)
  sw=door_wall138(z)
  # dormers on the street slope
  nd={'dormers2':2}.get(next((e for e in ex if e=='dormers2'),''),0)
  if 'dormers' in ex or 'dormers_wall' in ex or 'gdormers' in ex:nd=max(1,int(Ls/6.5))
  if nd and hs.get('nd'):nd=hs['nd']  # the count read on the photo
  dmat=M138[hs['dormer_mat']] if hs.get('dormer_mat') else None
  if nd and z['roof'] in ('saddle','hip','mhip','gambrel'):
   p,q=street_side138(r,sw);x,y,L,a=sf_edge(p,q)
   body=M138['DormerRed'] if (z['wall'] in ('Cream','PaleCream','Yellow') and st>=2) else (M138['Frame'] if z['boards'] else wm)
   for kk in range(nd):
    u=-L/2+(kk+.5)*L/nd if nd>1 else 0.0
    if nd==2:u=(-1 if kk==0 else 1)*min(L*.22,3.2)
    if 'dormers2' in ex:gdormer138(m,x,y,u,a,H,sl,1.6,1.1,wm,M138['Frame'],rm,.7)
    elif 'gdormers' in ex:gdormer138(m,x,y,u,a,H,sl,1.6,1.0,dmat or M138['DormerRed'],M138['Frame'],rm,.7)
    elif 'dormers_wall' in ex:dormer82(m,x,y,u,a,H,sl,2.6 if kk%2==0 else 1.7,1.1,dmat or (M138['DormerBrown'] if z['wall']=='WhiteRender' else M138['DormerRed']),M138['Frame'],rm,.45)
    elif z['roof']=='gambrel':dormer82(m,x,y,u,a,H,sl,1.6,1.0,body,M138['Frame'],rm,.25)
    else:dormer82(m,x,y,u,a,H,sl,1.6 if st<2 else 1.5,1.0,body,M138['Frame'],rm,.9+(.3 if z['roof']=='hip' else 0))
  # the central gable on the street front: width and apex read per house (gable_w, gable_top)
  if 'gable_mid' in ex and sw:
   x,y,L,a=sf_edge(*sw);gw=min(hs.get('gable_w',4.2),L-1.0);ga=zabs138(hs.get('gable_top',z['top']-.9))
   frontis83(m,x,y,0.0,gw,H,H+.25,ga,a,wm,M138['Frame'],rm,'oculus' not in ex)
   if 'oculus' in ex:
    # the round window in the gable (a triangle fan, see the export notes)
    kk=14;rw=.38;zc=H+.25+(ga-H-.25)*.38;cc=lp(x,y,0.0,.40,zc,a)
    m.faces([cc]+[lp(x,y,rw*math.cos(2*math.pi*i/kk),.40,zc+rw*math.sin(2*math.pi*i/kk),a) for i in range(kk)],[(0,i+1,(i+1)%kk+1) for i in range(kk)]+[(0,(i+1)%kk+1,i+1) for i in range(kk)],GLAZE)
    town_path(m,[lp(x,y,(rw+.07)*math.cos(2*math.pi*i/kk),.42,zc+(rw+.07)*math.sin(2*math.pi*i/kk),a) for i in range(kk+1)],.06,M138['Frame'])
  # the brown boarded roof storey of 93329984: a box over the middle of the low roof with its own saddle
  if 'attic' in ex:
   cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4
   d0=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);d1=((r[2][0]-r[1][0])/Lt,(r[2][1]-r[1][1])/Lt);aw,ad=min(7.0,Ls*.4),min(Lt*.6,7.0)
   ra=[(cx_+d0[0]*s0*aw/2+d1[0]*s1*ad/2,cy_+d0[1]*s0*aw/2+d1[1]*s1*ad/2) for s0,s1 in ((-1,-1),(1,-1),(1,1),(-1,1))]
   ZA=T+1.6
   for p,q in zip(ra,ra[1:]+ra[:1]):
    bz_wall(m,list(p),list(q),H,ZA,[],M138['BrownBoard'])
    boards115(m,{'p':list(p),'q':list(q)},H+.05,ZA-.1,[],M138['BrownBoard'])
   rb=[ra[1],ra[2],ra[3],ra[0]]
   eav,sl_,ends=saddle115(m,rb,ZA,ZA+1.4,rm,M138['BrownBoard'],.30)
   for p,q,c,n in ends:
    x,y,L,a=end_frame138(p,q,n)
    for s_ in (-1.1,1.1):window138(m,x,y,s_,ZA-1.45,.8,1.1,a,fr)

 for nm,m in meshes.items():b138_finish(m,nm.split('_')[-1])
build138_houses()
if G_PREV138 is not None:G=G_PREV138  # steps115 reads the shared G; give back what the chain had

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block138_cameras=[
 # resected on the OSM outlines where noted in references/block138-notes.md, else the pano position
 sv_camera('755_Block138_Cal_StensovagenNorthWestYellowBlock',-1393.38,239.01,2.5,304,10),
 sv_camera('756_Block138_Cal_StensovagenNorthWestWhiteBlock',-1285.67,276.38,2.5,310,10),
 sv_camera('757_Block138_Cal_StensovagenSouthEastPinkHouse',-1411.09,228.72,2.5,130,10),
 sv_camera('758_Block138_Cal_LangviksvagenNorthCreamBlock',-1538.26,-9.47,2.5,330,10),
 sv_camera('759_Block138_Cal_LangviksvagenSouthTowerVilla',-1538.26,-9.47,2.5,150,10),
 sv_camera('760_Block138_Cal_LangviksvagenSouthYellowVilla',-1589.82,-18.86,2.5,145,10),
 sv_camera('761_Block138_Cal_StensviksvagenSouthGreyBlock',-1512.52,-163.97,2.5,150,10),
 sv_camera('762_Block138_Cal_SturevagenEastBlueVilla',-1639.2,-56.1,2.5,90,10),
 sv_camera('763_Block138_Cal_StensovagenNorthWestMansardVilla',-1585.9,158.6,2.5,20,10),
 ('764_Block138_Aerial',(-1380.0,-260.0,130.0),(-1520.0,10.0,2.0),24)]
print('BLOCK138_GEOMETRY',len(block138_names))
