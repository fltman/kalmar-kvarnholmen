"""Pass 134: the mainland west of Gamla stan along Ståthållaregatan, Gustaf Vasagatan, Vegagatan and
Folkungagatan (started as a parked 'pass 123' and renumbered). Pass 98 built these houses as plain
volumes in its chunk meshes; 43 of them are now each its own
mesh SM_Slott134_<osm id> with its real form: storeys, saddle, hipped, gambrel and hipped mansard roofs
in red or red-brown tile, dark tile or grey sheet metal, render, vertical boarding in the house's
colour, white (or red) window frames, a door on the street, dormers, chimneys and the notable features:
- on Ståthållaregatan the two 1940s two-storey terrace rows in alternating red, cream and grey render
  with ridges along the street, the white arched entrance bays, the arched door portal, the balcony over
  a door and the small entrance balcony; the white villa pair with the gabled dormers and red window
  frames and the yellow three-storey block with its metal-clad roof storey; the red boarded
  18th-century-style house with its gable on the street; the yellow 1990s block with the grey ground
  floor, the white bay windows and the red entrance canopy; the cream and yellow blocks over basements
  with dark red dormers, the yellow 1990s block's balconies and round-topped gable, the fire ladder;
- on Folkungagatan the cream 1940s two-storey blocks with the dark red boarded wall dormers;
- on Vegagatan the ochre four-storey 1940s block, the grey garage row and the grey-white four-storey
  block with the orange balconies and the glazed balcony tower;
- on Gustaf Vasagatan the villas: rendered and boarded, saddle and gambrel roofs, the central cross
  gable, porches with balconies on top, the red awnings, the glazed balcony, the new white houses and the
  modern house with the glazed top storey;
- houses seen in no photo get a plausible form from their neighbours.
It also re-creates pass 98's chunk meshes the houses sit in (W and M) with slott98_chunks115 (pass 115),
leaving out every house in SLOTT98_DETAILED. The 44th outline, 93358501 on Gustaf Vasagatan, is a cleared
building site in the 2025 imagery: it leaves the chunk and gets no mesh.
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block134.json; see references/block134-notes.md.
"""
# Pass 125 leaves numbers in the shared names TS and TC, which the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B134D=json.loads((R/'source/block134.json').read_text());Z134=B134D['zones'];HS134=B134D['houses'];G134=B134D['ground_z']
block134_names=[];B134={}
def mats134():
 # pass 82's material setup loop, in a function so that its loop names stay local
 for old in [k for k in list(materials) if k.startswith('M_Block134_')]:bpy.data.materials.remove(materials.pop(old))
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
  ]:
  name='M_Block134_'+key;B134[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
  mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block134_target_srgb']=list(target)
  ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
  mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
  for node in nodes:
   if node.bl_idname=='ShaderNodeTexImage' and node.image:
    twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
    if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
mats134()
M134=B134
B98ID134={b['id']:b for b in B98D['buildings']}
def b134_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block134_names.append(name);return Mesh(name,category)
def drop_degenerate_faces134(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b134_finish(m,osm):
 obj=s21_finish(m);obj['block134_dropped_faces']=drop_degenerate_faces134(obj);print('BLOCK134_DROPPED',m.name,obj['block134_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=134;obj['reference_notes']='references/block134-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without these houses
# The demolished house (93358501, a cleared building site in the 2025 imagery) leaves the chunk with no mesh of its own.
GONE134=set(B134D['ids'])|set(B134D.get('demolished',[]))
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|GONE134
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in GONE134},134,block134_names)
# slott98_chunks115 finishes the chunks with pass 115's finisher (detail_pass 98, rebuilt_by_pass 134).

# ---------------------------------------------------------------- helpers
# steps115 (pass 115) reads the shared name G as the ground level; it is set for this build only and
# given back at the end.
G_PREV134=globals().get('G');G=G134
def zabs134(h):return G134+h
def long_first134(r):
 r=[tuple(v) for v in r]
 return r if math.dist(r[0],r[1])>=math.dist(r[1],r[2])-.01 else r[1:]+r[:1]
def end_frame134(p,q,n):
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def gambrel134(m,r,H,T,ma,wall,ov=.35,verge=.30):
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
def mhip134(m,r,H,T,ma,ov=.40):
 # A hipped mansard: steep lower slopes from the eaves to the break (1.1 m in, 70 % of the rise up),
 # then a low hip to the top.
 Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2]);k=min(1.1,min(Ls,Lt)/4);ZB=H+(T-H)*.7
 outer,inner=inset_roof(m,r,H,k,ZB-H,ma,ov)
 inset_roof(m,[tuple(v) for v in inner],ZB,max(.3,min(Ls,Lt)/2-k-.3),T-ZB,ma,.12)
 return k,ZB
def simp134(g,tol=.02):
 # drops vertices that lie within tol of the line through their neighbours, spikes included: a flat
 # roof n-gon with such a vertex triangulates (in the export tail) into a sliver with no UV frame
 # (93361215's annex, first sandbox run)
 g=[tuple(v) for v in g];changed=True
 while changed and len(g)>3:
  changed=False
  for i in range(len(g)):
   a,b,c=g[i-1],g[i],g[(i+1)%len(g)];L=math.dist(a,c)
   if L<1e-9 or abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/L<tol:g.pop(i);changed=True;break
 return g
def flat134(m,polys,H,ma,trim):
 for g in polys:
  g=simp134(clean115(g,.1))
  if len(g)<3 or abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1])))<.1:continue
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  if len(g)<3:continue
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.30,H+.05,L+.30,.40,.22,trim,a)
def window134(m,x,y,u,b,w,h,a,frame='Frame',awning=False):
 # pass 116's window: casement, surround, sill; a red awning on the boarded villa
 fr=M134[frame];cas81(m,x,y,u,b,w,h,a,fr,.16,3 if h>1.2 else 2)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,fr,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a);facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,fr,a)
 if awning:awning82(m,x,y,u,b+h,w+.3,a,M134['Awning'],.55,.7)
def door134(m,x,y,u,b,w,h,a,leaf,frame):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
 facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,leaf,a)
 if w>1.2:facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+h/2,.12,.06,h,frame,a)
 facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,frame,a)
def archdoor134(m,x,y,u,b,w,h,a,leaf,frame):
 # an arched door: the leaf, a fan light in the arch (a triangle fan, see the export notes), the frame
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.70,w-.36,.02,h*.35,GLAZE,a)
 r=w/2;k=10;c=lp(x,y,u,.10,b+h,a)
 pts=[lp(x,y,u+r*math.cos(math.pi*i/k),.10,b+h+r*math.sin(math.pi*i/k),a) for i in range(k+1)]
 m.faces([c]+pts,[(0,i+1,i+2) for i in range(k)]+[(0,i+2,i+1) for i in range(k)],GLAZE)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+(h+r)/2,.12,.06,h+r,frame,a)
 town_path(m,[lp(x,y,u+(r+.06)*math.cos(math.pi*i/k),.38,b+h+(r+.06)*math.sin(math.pi*i/k),a) for i in range(k+1)],.06,frame)
def rows134(hs,z,Hh):
 # window rows (bottom, height, width) above the ground for a zone
 st=z.get('st',hs['st']);f0=hs.get('f0',0.0)
 if Hh<2.9:return [(.9,.8,.8)]
 n=int(st)
 if n>=2 and f0>0 or n>=3:
  sh=(Hh-f0-.5)/n;return [(f0+i*sh+.85,min(1.45,sh-1.4),1.1) for i in range(n)]
 if n>=2:return [(.95,1.35,1.0),(max(Hh*.5+.75,Hh-1.85),1.25,1.0)]
 return [(max(.85,f0+.6),1.35 if Hh>3.2 else 1.15,1.0)]
MINE134=('Ståthållaregatan','Gustaf Vasagatan','Vegagatan','Folkungagatan')
def door_wall134(z):
 # the wall on the pass's street when the zone faces one, else the nearest street's
 if z.get('street') in MINE134 or not z.get('street_walls'):return z.get('street_wall')
 for nm in MINE134:
  if nm in z['street_walls']:return z['street_walls'][nm]
 return z.get('street_wall')
def street_side134(r,sw):
 sides=[(r[0],r[1]),(r[2],r[3])]
 if sw:
  mx,my=(sw[0][0]+sw[1][0])/2,(sw[0][1]+sw[1][1])/2;sides.sort(key=lambda pq:math.dist(((pq[0][0]+pq[1][0])/2,(pq[0][1]+pq[1][1])/2),(mx,my)))
 return sides[0]
def west_u134(sw,inset):
 # u of the point 'inset' metres in from the west (smaller x) end of the wall sw
 p,q=sw;x,y,L,a=sf_edge(p,q);end=p if p[0]<q[0] else q;ue=U({'p':p,'q':q},*end)
 return ue-math.copysign(inset,ue) if L>2*inset else 0.0
def gdormer134(m,x,y,u,a,H,sl,w,h,body,frame,roof,back=.6):
 # a gabled dormer: pass 82's box dormer with a small saddle roof and a pediment in the body colour
 dormer82(m,x,y,u,a,H,sl,w,h,body,frame,roof,back)
 zb=H+(back+.40-.355+.05)*sl-.15;zt=zb+h+.55;dep=2.2;o0=.355-back+.05;o1=o0-dep
 pts=[lp(x,y,u-w/2-.15,o0+.1,zt+.1,a),lp(x,y,u+w/2+.15,o0+.1,zt+.1,a),lp(x,y,u+w/2+.15,o1,zt+.1,a),lp(x,y,u-w/2-.15,o1,zt+.1,a),lp(x,y,u,o0+.1,zt+.1+w*.45,a),lp(x,y,u,o1,zt+.1+w*.45,a)]
 m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],roof)
 town_path(m,[lp(x,y,u-w/2-.1,o0+.14,zt+.12,a),lp(x,y,u,o0+.14,zt+.12+w*.43,a),lp(x,y,u+w/2+.1,o0+.14,zt+.12,a)],.05,frame)

def round_gable_wall134(osm,P):
 # the outer wall of any zone of house osm that passes within 5 cm of point P, and P's u on it
 if not P:return None
 for z in Z134.values():
  if z['osm']!=osm:continue
  for w in z['walls']:
   if w['kind']!='outer':continue
   p,q=w['p'],w['q'];L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);s=(P[0]-p[0])*d[0]+(P[1]-p[1])*d[1]
   if -.01<s<L+.01 and abs((P[0]-p[0])*d[1]-(P[1]-p[1])*d[0])<.05:return (p,q),U({'p':p,'q':q},*P)
 return None
def build134_houses():
 # The houses, in a function so that its loop names (H, T, m, x, y, ...) stay local and no shared
 # global name is clobbered (see pass 125's TS/TC).
 meshes={}
 for zone,z in Z134.items():
  if z['mesh'] not in meshes:meshes[z['mesh']]=b134_new(z['mesh'],'Slottsområdet/Mainland')
 # ---------------------------------------------------------------- walls, windows, doors
 for zone,z in Z134.items():
  hs=HS134[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs134(Hh);ex=hs.get('extras',[]) if z['role']=='main' else []
  wm=M134[z['wall']];fr=z.get('fr',hs.get('fr','Frame'));trim=M134['Frame'];st=z.get('st',hs['st'])
  rows=rows134(hs,z,Hh) if z['role'] in ('main','wing') or st>=3 else ([(.9,.8,.8)] if Hh>2.4 else [])
  if 'garages' in ex:rows=[]
  dwall=door_wall134(z) if (z['role']=='main' and 'no_door' not in ex) else None
  f0=hs.get('f0',0.0);plinth=max(.35 if Hh>2.9 else .2,min(f0,1.0))
  split=zabs134(2.6) if 'grey_ground' in ex else None
  for w in z['walls']:
   x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs134(w['z0'])
   if L<.25:continue
   wins=[];mine=[];isdoor=False
   if w['kind']=='outer':
    if dwall and abs(w['p'][0]-dwall[0][0])<1e-6 and abs(w['p'][1]-dwall[0][1])<1e-6 and L>1.6:
     isdoor=True;dh=2.15;dw=1.0
     du=0.0 if L<6 else -L/2+min(L*.35,3.0)
     if 'arch_bay' in ex or 'arch_door' in ex:du=west_u134(dwall,1.4)
     if 'garage_door' in ex:mine.append(('garage',0.0,G+.02,2.5,2.0))
     elif 'arch_bay' in ex:mine.append(('bay',du,G,2.2,0))
     else:mine.append(('arch' if 'arch_door' in ex else 'door',du,G+(min(f0,.45) if f0>0 else plinth*.5),1.1 if 'arch_door' in ex else dw,1.9 if 'arch_door' in ex else dh))
    if 'garages' in ex and L>5:
     n=max(1,int(L/3.0))
     for k in range(n):mine.append(('garage',-L/2+(k+.5)*L/n,G+.02,2.4,2.0))
    bay=2.9 if st>=3 else 2.7 if st>=2 else 2.9;n=int(L/bay+.3)
    for k in range(n):
     u=-L/2+(k+.5)*L/n
     for i,(b,hh,ww) in enumerate(rows):
      b=zabs134(b)
      if b<z0+.3 or b+hh>H-.25 or L<ww+1.0:continue
      if any(abs(u-du_)<(ww+dw_)/2+.30 and (kind_=='bay' or b<db+dh_+.2) for kind_,du_,db,dw_,dh_ in mine):continue
      wins.append((u,b,ww,hh,i))
    if f0>=1.0 and z['role'] in ('main','wing'):
     for k in range(n):
      u=-L/2+(k+.5)*L/n
      if not any(abs(u-du_)<1.2 for _,du_,db,dw_,dh_ in mine):wins.append((u,G+f0-.80,.7,.5,-1))
   holes=[(u,b,ww,hh,0) for u,b,ww,hh,i in wins]+[(du_,db,dw_,dh_,dw_/2 if kind_=='arch' else 0) for kind_,du_,db,dw_,dh_ in mine if kind_!='bay']
   if split and w['kind']=='outer':
    bz_wall(m,w['p'],w['q'],z0,split,holes,M134['GreyGround']);bz_wall(m,w['p'],w['q'],split,H,holes,wm)
   else:bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
   if z['boards']:boards115(m,w,max(z0,G+plinth+.02),H-.12,holes,wm)
   for u,b,ww,hh,i in wins:window134(m,x,y,u,b,ww,hh,a,fr,'awnings' in ex and i>=0)
   for kind,du_,db,dw_,dh_ in mine:
    if kind=='garage':
     facade_box(m,x,y,du_,.15,db+dh_/2,dw_,.06,dh_,M134['GarageDoor'],a)
     for k in range(1,5):facade_box(m,x,y,du_,.19,db+k*dh_/5,dw_-.1,.02,.03,M134['Frame'],a)
     surround36(m,x,y,du_,db,dw_,dh_,a,M134['Frame'],.10,.40);continue
    if kind=='bay':
     # the white arched entrance bay of the 1940s row: a shallow two-storey projection with an arched
     # door on its steps and an arched window above, under a small tile roof
     BW,BD=1.8,.55;zt=H-.6;xb,yb,_=lp(x,y,0,BD,0,a)
     facade_box(m,x,y,du_,.355+BD/2-.02,(G+zt)/2,BW,BD+.04,zt-G,M134['WhiteRender'],a)
     archdoor134(m,xb,yb,du_,G+.45,1.1,1.95,a,M134['Door'],M134['Frame'])
     steps115(m,xb,yb,du_,1.5,G+.45,a,M134['Step'])
     zw=min(zt-1.8,G+4.1);facade_box(m,xb,yb,du_,.33,zw+.6,.75,.02,1.2,GLAZE,a)
     k=8;c=lp(xb,yb,du_,.33,zw+1.2,a);pts=[lp(xb,yb,du_+.375*math.cos(math.pi*i/k),.33,zw+1.2+.375*math.sin(math.pi*i/k),a) for i in range(k+1)]
     m.faces([c]+pts,[(0,i+1,i+2) for i in range(k)]+[(0,i+2,i+1) for i in range(k)],GLAZE)
     town_path(m,[lp(xb,yb,du_+.43*math.cos(math.pi*i/k),.38,zw+1.2+.43*math.sin(math.pi*i/k),a) for i in range(k+1)],.05,M134['Frame'])
     facade_box(m,xb,yb,du_,.37,zw-.05,.95,.12,.06,M134['Frame'],a)
     pts=[lp(x,y,du_-BW/2-.15,BD+.5,zt,a),lp(x,y,du_+BW/2+.15,BD+.5,zt,a),lp(x,y,du_+BW/2+.15,.2,zt+.45,a),lp(x,y,du_-BW/2-.15,.2,zt+.45,a)]
     m.faces(pts,[(0,1,2,3),(3,2,1,0)],M134[hs['rm']]);continue
    leaf=M134['Door']
    if kind=='arch':
     archdoor134(m,x,y,du_,db,dw_,dh_,a,leaf,M134['Frame'])
     surround36(m,x,y,du_,db,dw_,dh_+dw_/2,a,M134['Stone'],.18,.42)
    else:door134(m,x,y,du_,db,dw_,dh_,a,leaf,M134['Frame'])
    if db>G+.12:steps115(m,x,y,du_,dw_+.5,db,a,M134['Step'])
    if 'entrance_balcony' in ex or 'balcony_small' in ex:
     # the small balcony over the entrance, a railing on three sides
     bz=zabs134(rows[1][0])-.15 if len(rows)>1 else H-1.9;facade_box(m,x,y,du_,.36+.45,bz,1.6,.9,.14,M134['Stone'],a)
     town_rod(m,lp(x,y,du_-.8,1.23,bz+1.0,a),lp(x,y,du_+.8,1.23,bz+1.0,a),.025,M134['Iron'],6)
     for kk in range(9):town_rod(m,lp(x,y,du_-.8+kk*.2,1.23,bz+.07,a),lp(x,y,du_-.8+kk*.2,1.23,bz+1.0,a),.012,M134['Iron'],4)
     for s in (-1,1):town_rod(m,lp(x,y,du_+s*.8,.38,bz+1.0,a),lp(x,y,du_+s*.8,1.23,bz+1.0,a),.02,M134['Iron'],4)
    if 'canopy' in ex:
     # the entrance canopy: two posts and a small gabled roof (red frame on the 1990s block)
     cm=M134['DormerRed'] if z['wall']=='Yellow' else M134['WhiteRender'];zc=db+dh_+.35
     for s in (-1,1):facade_box(m,x,y,du_+s*.85,1.45,(G+zc)/2,.12,.12,zc-G,cm,a)
     pts=[lp(x,y,du_-1.05,1.65,zc,a),lp(x,y,du_+1.05,1.65,zc,a),lp(x,y,du_+1.05,.36,zc,a),lp(x,y,du_-1.05,.36,zc,a),lp(x,y,du_,1.65,zc+.55,a),lp(x,y,du_,.36,zc+.55,a)]
     m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],M134['RoofGrey'])
     town_path(m,[lp(x,y,du_-1.05,1.68,zc,a),lp(x,y,du_,1.68,zc+.55,a),lp(x,y,du_+1.05,1.68,zc,a)],.06,cm)
   if w['kind']=='outer':facade_box(m,x,y,0,.40,(G+plinth)/2,L+.02,.10,G+plinth,M134['Stone'],a)
   if z['role'] not in ('annex',):facade_box(m,x,y,0,.44,H-.12,L+.12,.16,.24,trim,a)
   if z['boards']:
    for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+plinth)/2,.20,.10,H-G-plinth,M134['Frame'],a)
   if isdoor and 'balconies' in ex and L>10:
    # balconies with iron railings on the upper storeys, two per front
    for b,hh,ww in rows[1:]:
     for uu in (-L/4,L/4):
      bz=zabs134(b)-.15;facade_box(m,x,y,uu,.36+.65,bz,2.8,1.3,.14,M134['Stone'],a)
      town_rod(m,lp(x,y,uu-1.4,1.63,bz+1.0,a),lp(x,y,uu+1.4,1.63,bz+1.0,a),.025,M134['Iron'],6)
      for kk in range(15):town_rod(m,lp(x,y,uu-1.4+kk*.2,1.63,bz+.07,a),lp(x,y,uu-1.4+kk*.2,1.63,bz+1.0,a),.012,M134['Iron'],4)
   if isdoor and 'balconies_orange' in ex:
    # the orange balcony slabs with solid fronts on every storey above the ground floor
    for b,hh,ww in rows[1:]:
     for uu in [-L/2+(k+.5)*L/max(1,int(L/7)) for k in range(max(1,int(L/7)))]:
      bz=zabs134(b)-.15;facade_box(m,x,y,uu,.36+.6,bz,2.6,1.2,.16,M134['Orange'],a)
      facade_box(m,x,y,uu,.36+1.17,bz+.5,2.6,.06,.85,M134['Orange'],a)
      for s in (-1,1):facade_box(m,x,y,uu+s*1.27,.36+.6,bz+.5,.06,1.2,.85,M134['Orange'],a)
   if isdoor and 'bays' in ex:
    # the white two-storey bay windows above the grey ground floor
    for uu in (-L/3,L/3):
     zb=zabs134(2.6);zt_=H-.5;facade_box(m,x,y,uu,.355+.35,(zb+zt_)/2,2.8,.7,zt_-zb,M134['WhiteRender'],a)
     xb,yb,_=lp(x,y,0,.7,0,a)
     for b,hh,ww in rows[1:]:
      facade_box(m,xb,yb,uu,.36,zabs134(b)+hh/2,2.0,.02,hh,GLAZE,a)
      for s in (-1,0,1):facade_box(m,xb,yb,uu+s*1.0,.38,zabs134(b)+hh/2,.08,.06,hh,M134['Frame'],a)
   if isdoor and 'fire_ladder' in ex:
    uu=-L*.2
    for s in (-.22,.22):town_rod(m,lp(x,y,uu+s,.55,G+2.6,a),lp(x,y,uu+s,.55,H+.9,a),.025,M134['Iron'],6)
    k=0;zz=G+2.8
    while zz<H+.8:town_rod(m,lp(x,y,uu-.22,.55,zz,a),lp(x,y,uu+.22,.55,zz,a),.015,M134['Iron'],4);zz+=.35
   if isdoor and 'glazed_balcony' in ex:
    # the glazed balcony on posts at the upper floor of the street front
    uu=L*.2;bz=zabs134(rows[1][0])-.4 if len(rows)>1 else H-2.0
    facade_box(m,x,y,uu,.36+.8,bz,3.2,1.6,.18,M134['White'],a);facade_box(m,x,y,uu,.36+.8,bz+1.25,3.0,1.5,2.2,GLAZE,a)
    facade_box(m,x,y,uu,.36+.8,bz+2.4,3.4,1.8,.14,M134['White'],a)
    for s in (-1,1):facade_box(m,x,y,uu+s*1.5,.36+1.5,(G+bz)/2,.14,.14,bz-G,M134['White'],a)
   if isdoor and 'balcony' in ex:
    # a porch on posts at the door with a balcony on its roof (pass 118's 'balcony')
    u=next((mm[1] for mm in mine if mm[0] in ('door','arch')),0.0)
    bz=min(zabs134(3.2),H-.4)
    facade_box(m,x,y,u,.36+.8,bz,2.8,1.6,.16,M134['Frame'],a)
    town_rod(m,lp(x,y,u-1.4,1.92,bz+1.0,a),lp(x,y,u+1.4,1.92,bz+1.0,a),.04,M134['Frame'],6)
    for kk in range(15):facade_box(m,x,y,u-1.35+kk*.193,1.92,bz+.55,.05,.05,.9,M134['Frame'],a)
    for s in (-1,1):facade_box(m,x,y,u+s*1.3,1.82,(G+bz)/2,.16,.16,bz-G,M134['Frame'],a)

 # ---------------------------------------------------------------- roofs and features
 for zone,z in Z134.items():
  hs=HS134[z['osm']];m=meshes[z['mesh']];Hh=z['height'];H=zabs134(Hh);T=zabs134(z['top']);ex=hs.get('extras',[]) if z['role']=='main' else []
  wm=M134[z['wall']];rm=M134[z.get('rm',hs['rm'])];fr=z.get('fr',hs.get('fr','Frame'));st=z.get('st',hs['st'])
  if z['role']=='annex' or z['roof']=='flat':
   flat134(m,z['polygons'],H,M134['RoofDark'],M134['Frame'] if z['boards'] else wm)
   if 'glass_top' in ex:
    # the glazed, set-back top storey of the modern house with its thin flat roof
    for g in z['polygons']:
     g=clean115(g,.1)
     if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
     ug=ring_offset(g,-1.2);UH=H+2.6
     for p,q in zip(ug,ug[1:]+ug[:1]):
      x,y,L,a=sf_edge(p,q)
      if L<.3:continue
      facade_box(m,x,y,0,0,H+1.32,L,.04,2.5,GLAZE,a)
      for k in range(int(L/1.2)+1):facade_box(m,x,y,-L/2+k*L/max(1,int(L/1.2)),.03,H+1.32,.06,.08,2.5,M134['FrameDark'],a)
      facade_box(m,x,y,0,.25,UH,L+.6,.6,.2,M134['WhiteRender'],a)
     m.faces([(*v,UH+.1) for v in ug],[tuple(range(len(ug))),tuple(range(len(ug)-1,-1,-1))],M134['RoofDark'])
   continue
  r=[tuple(v) for v in z['rect']] if z.get('ridge_fixed') else long_first134(z['rect'])
  if hs.get('ridge')=='short' and not z.get('ridge_fixed') and z['role'] in ('main','wing'):r=r[1:]+r[:1]
  Ls,Lt=math.dist(r[0],r[1]),math.dist(r[1],r[2])
  if z['roof'] in ('hip','low'):
   inset_roof(m,r,H,max(.3,min(Ls,Lt)/2-.30),T-H,rm,.45);sl=(T-H)/max(.5,min(Ls,Lt)/2)
  elif z['roof']=='mhip':
   k,ZB=mhip134(m,r,H,T,rm);sl=(ZB-H)/k
   if z['role']=='wing':
    # the roof storey's windows: dormers on all four steep slopes
    for i in range(4):
     p,q=r[i],r[(i+1)%4];x,y,L,a=sf_edge(p,q)
     for kk in range(max(1,int(L/3.2))):dormer82(m,x,y,-L/2+(kk+.5)*L/max(1,int(L/3.2)),a,H,sl,1.3,1.1,rm,M134['Frame'],rm,.25)
  elif z['roof']=='gambrel':
   k,ZB,ends=gambrel134(m,r,H,T,rm,wm)
   for p,q,c,n in ends:
    x,y,L,a=end_frame134(p,q,n)
    if T-H>2.4:
     if L>6.5:
      for s in (-1.1,1.1):window134(m,x,y,s,H+.45,.9,min(1.3,ZB-H-.4),a,fr)
     else:window134(m,x,y,0,H+.35,.8,min(1.1,ZB-H-.2),a,fr)
   sl=(ZB-H)/k
  else:
   eav,sl,ends=saddle115(m,r,H,T,rm,wm,.40 if st>=1 else .30)
   for p,q,c,n in ends:
    x,y,L,a=end_frame134(p,q,n)
    if T-H>2.3 and L>3.0 and z['role']!='annex':
     gh=min(1.1,(T-H)*.45)
     if st>=1.5 and L>6.5:
      for s in (-.8,.8):window134(m,x,y,s,H+.35,.7,gh,a,fr)
     else:window134(m,x,y,0,H+.35,.75,gh,a,fr)
    o=lambda v,kk:(v[0]+n[0]*kk,v[1]+n[1]*kk)
    for u_ in (p,q):
     e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
     town_rod(m,(*o(e,.48),H-.35*sl-.04),(*o(c,.48),T-.04),.06,M134['Frame'],6)
  # chimneys on the ridge
  cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;d_=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);ang=math.atan2(d_[1],d_[0])
  cm=M134['ChimneyWhite'] if z['wall'] in ('White','WhiteRender','Cream','PaleCream','GreyWhite','PaleYellowRender','PaleGrey') else M134['Chimney']
  if 'chimneys2' in ex:
   for s in (-Ls*.25,Ls*.25):chimney115(m,cx_+d_[0]*s,cy_+d_[1]*s,T-.6,T+.8,cm,ang)
  elif 'chimney' in ex:chimney115(m,cx_+d_[0]*Ls*.15,cy_+d_[1]*Ls*.15,T-.6,T+.7,cm,ang)
  sw=door_wall134(z)
  # dormers on the street slope
  nd={'dormers2':2}.get(next((e for e in ex if e=='dormers2'),''),0)
  if 'dormers' in ex or 'dormers_wall' in ex or 'gdormers' in ex:nd=max(1,int(Ls/6.5))
  if nd and z['roof'] in ('saddle','hip','mhip','gambrel'):
   p,q=street_side134(r,sw);x,y,L,a=sf_edge(p,q)
   body=M134['DormerRed'] if (z['wall'] in ('Cream','PaleCream','Yellow') and st>=2) else (M134['Frame'] if z['boards'] else wm)
   for kk in range(nd):
    u=-L/2+(kk+.5)*L/nd if nd>1 else 0.0
    if nd==2:u=(-1 if kk==0 else 1)*min(L*.22,3.2)
    if 'dormers2' in ex:gdormer134(m,x,y,u,a,H,sl,1.6,1.1,wm,M134['Frame'],rm,.7)
    elif 'gdormers' in ex:gdormer134(m,x,y,u,a,H,sl,1.6,1.0,M134['DormerRed'],M134['Frame'],rm,.7)
    elif 'dormers_wall' in ex:dormer82(m,x,y,u,a,H,sl,2.6 if kk%2==0 else 1.7,1.1,M134['DormerRed'],M134['Frame'],M134['RoofGrey'],.45)
    elif z['roof']=='gambrel':dormer82(m,x,y,u,a,H,sl,1.6,1.0,body,M134['Frame'],rm,.25)
    else:dormer82(m,x,y,u,a,H,sl,1.6 if st<2 else 1.5,1.0,body,M134['Frame'],rm,.9+(.3 if z['roof']=='hip' else 0))
  # the central cross gable of the villa (93460168) over its porch
  if 'gable_mid' in ex and sw:
   x,y,L,a=sf_edge(*sw);frontis83(m,x,y,0.0,4.2,H,H+.25,T-.9,a,wm,M134['Frame'],rm,True)
  # the round-topped gable of the 1990s block (94560092) near the west end of its street front
  rg=round_gable_wall134(z['osm'],hs.get('round_gable_at')) if 'round_gable' in ex else None
  if rg:
   # placed at the point read on st08_h4 (over the grey stair bay, 6 m from the west corner), on the
   # outer wall of whichever zone of the house carries it; the stair bay in grey render below it
   (gp,gq),gu=rg;x,y,L,a=sf_edge(gp,gq);gw=4.0;u0=gu;rr=gw/2;k=16
   facade_box(m,x,y,u0,.355+.30,(G134+H)/2,3.2,.60,H-G134,M134['GreyGround'],a)
   prof=[(-gw/2,H)]+[(rr*math.cos(math.pi*(1-i/k)),H+.5+rr*.75*math.sin(math.pi*i/k)) for i in range(k+1)]+[(gw/2,H)]
   vs=[lp(x,y,u0+uu,o,zz,a) for o in (.005,.38) for uu,zz in prof];N=len(prof)
   # the face as a triangle fan from its base middle, the back likewise
   c0=lp(x,y,u0,.005,H,a);c1=lp(x,y,u0,.38,H,a);base=len(vs);vs=vs+[c0,c1]
   m.faces(vs,[(base,i+1,i) for i in range(N-1)]+[(base+1,N+i,N+i+1) for i in range(N-1)]+[(i,i+1,N+i+1,N+i) for i in range(N-1)]+[(N-1,0,N,2*N-1)],wm)
   town_path(m,[lp(x,y,u0+uu,.42,zz+.06,a) for uu,zz in prof[1:-1]],.08,M134['Frame'])
   kk=14;rw=.45;zc=H+1.25;cc=lp(x,y,u0,.40,zc,a)
   m.faces([cc]+[lp(x,y,u0+rw*math.cos(2*math.pi*i/kk),.40,zc+rw*math.sin(2*math.pi*i/kk),a) for i in range(kk)],[(0,i+1,(i+1)%kk+1) for i in range(kk)]+[(0,(i+1)%kk+1,i+1) for i in range(kk)],GLAZE)
   town_path(m,[lp(x,y,u0+(rw+.07)*math.cos(2*math.pi*i/kk),.42,zc+(rw+.07)*math.sin(2*math.pi*i/kk),a) for i in range(kk+1)],.06,M134['Frame'])
  # the glazed balcony tower of 93325620 at the end nearest the Jugend house (93325650)
  if 'glazed_tower' in ex and sw:
   x,y,L,a=sf_edge(*sw);J=B98ID134['93325650']['outer'];jx,jy=sum(v[0] for v in J)/len(J),sum(v[1] for v in J)/len(J)
   ends_=[(U({'p':sw[0],'q':sw[1]},*sw[0]),sw[0]),(U({'p':sw[0],'q':sw[1]},*sw[1]),sw[1])];ue=min(ends_,key=lambda e:math.dist(e[1],(jx,jy)))[0]
   u=ue-math.copysign(1.6,ue);zb=zabs134(3.0)
   facade_box(m,x,y,u,.36+.75,(zb+H)/2,2.8,1.5,H-zb,GLAZE,a)
   nf=max(1,int((H-zb)/2.9))
   for kk in range(nf+1):facade_box(m,x,y,u,.36+.75,zb+kk*(H-zb)/nf,3.0,1.6,.16,M134['Orange'],a)
   for s in (-1,1):facade_box(m,x,y,u+s*1.42,.36+1.48,(zb+H)/2,.08,.08,H-zb,M134['Frame'],a)

 for nm,m in meshes.items():b134_finish(m,nm.split('_')[-1])
build134_houses()
if G_PREV134 is not None:G=G_PREV134  # steps115 reads the shared G; give back what the chain had

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block134_cameras=[
 # resected on the OSM outlines where noted in references/block134-notes.md, else the pano position
 sv_camera('725_Block134_Cal_StathallaregatanRow',-1242.52,223.36,2.5,166,10),
 sv_camera('726_Block134_Cal_Stathallaregatan1',-1270.83,234.51,2.5,175,10),
 sv_camera('727_Block134_Cal_StathallaregatanRoundGable',-1376.54,303.30,2.5,4,10),
 sv_camera('728_Block134_Cal_Stathallaregatan3',-1297.51,250.06,2.5,188,10),
 sv_camera('729_Block134_Cal_Folkungagatan3',-1459.01,236.90,2.5,220,10),
 sv_camera('730_Block134_Cal_Vegagatan8',-1028.31,238.27,2.5,213,10),
 sv_camera('731_Block134_Cal_Vegagatan8North',-1028.31,238.27,2.5,33,10),
 sv_camera('732_Block134_Cal_GustafVasagatan',-1425.27,-59.03,2.5,296,10),
 sv_camera('733_Block134_Cal_GustafVasagatan17',-1557.86,-194.08,2.5,96,10),
 ('734_Block134_Aerial',(-1180.0,-60.0,110.0),(-1330.0,140.0,2.0),24)]
print('BLOCK134_GEOMETRY',len(block134_names))
