"""Pass 115: the houses of Stadsparken and Slottsvägen on the mainland west of Kvarnholmen, which pass 98
built as plain volumes in its chunk meshes, each now its own mesh SM_Slott115_<osm id>:
- Kalmar konstmuseum (2008): the black angular block clad in square black panels, with the glazed
  entrance under a dark sign band facing the park, its steps and landing;
- Byttan: the white rendered park restaurant under a low dark roof with wide eaves, its windows with
  dark glazing bars and the set-back upper storey;
- two small park buildings without a usable view (91222187, 874870421), modelled as plain rendered
  pavilions;
- Slottshotellet: the red rendered main house with white window frames, steep red tile roofs and two
  cross gables, the north-east wing, and the green vertical-boarded west wing (Molinsgatan 3) with
  ochre window frames, an attic window in its gable and carved ochre bargeboards;
- the salmon rendered villa at Västerlånggatan 1 under a brown tile saddle roof, its cross gable with
  the arched balcony door, the iron-railed balcony over the porch, and a chimney;
- the red-brick house on Slottsvägen under a dark grey standing-seam roof with roof lights, with the
  glazed timber veranda along its south-east side;
- the low dark-green boarded house and the shed beside it;
- the cream villa on Slottsvägen: two high storeys over a grey plinth, a string course, arched
  ground-floor windows, the pedimented east gable with a window, and the arched door on its steps;
- the white pavilion under a dark brown mansard roof with dormers and a central chimney;
- the cream two-storey house with its glazed entrance porch and the dark set-back rooftop storey;
- the Söderport pavilion: cream, one storey, four tall windows under cornice hoods between pilaster
  strips, and the pediment with its lunette towards Kungsgatan; the narrow link north of it;
- the KIKAIN kiosk: a round kiosk under a conical roof (no usable view; estimated).

It also re-creates pass 98's chunk meshes SM_Slott98_Buildings_M and _E with pass 98's own code,
leaving out every house in SLOTT98_DETAILED (see slott98_chunks115 and the notes).
References: Google Street View panoramas, resected on the OSM outlines, view only. Zones:
source/block115.json; see references/block115-notes.md.
"""
import hashlib
B115D=json.loads((R/'source/block115.json').read_text());Z115=B115D['zones'];ZG115=B115D['ground_z']
block115_names=[];B115={}
for old in [k for k in list(materials) if k.startswith('M_Block115_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Black','TownMetalGrey',(.075,.075,.08),.80,.05),('BlackRib','TownMetalGrey',(.11,.11,.115),.75,.05),('Sign','TownMetalGrey',(.04,.04,.045),.50,.10),
 ('White','TownIvory',(.92,.91,.88),.88,0),('Cream','TownIvory',(.91,.86,.72),.88,0),('PaleCream','TownIvory',(.93,.90,.80),.88,0),
 ('Red','TownIvory',(.66,.27,.21),.85,0),('Green','TownPaintGreen',(.42,.52,.45),.75,0),('Ochre','TownIvory',(.82,.68,.40),.70,0),
 ('Salmon','TownIvory',(.87,.72,.58),.88,0),('Brick','TownTileRed',(.55,.30,.24),.90,0),('Timber','TownPaintBrown',(.36,.24,.16),.70,0),
 ('DarkGreen','TownPaintGreen',(.13,.22,.19),.75,0),('Grey','TownIvory',(.68,.68,.66),.88,0),('Stone','TownStone',(.55,.55,.53),.90,0),
 ('Step','TownStone',(.63,.62,.59),.90,0),('Frame','TownPaintWhite',(.95,.95,.93),.55,0),('FrameDark','TownMetalGrey',(.10,.10,.11),.50,.20),
 ('Tile','TownTileRed',(.70,.33,.22),.80,0),('TileBrown','TownTileRed',(.38,.24,.18),.80,0),('RoofDark','TownMetalGrey',(.20,.20,.22),.60,.25),
 ('RoofSlate','TownMetalGrey',(.30,.31,.33),.55,.30),('RoofBrown','TownMetalGrey',(.27,.23,.21),.65,.20),('Door','TownPaintBrown',(.30,.21,.15),.70,0),
 ('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),('Chimney','TownIvory',(.80,.78,.74),.88,0),
 ]:
 name='M_Block115_'+key;B115[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block115_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M115=B115
def b115_new(name,category,names=None):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 (block115_names if names is None else names).append(name);return Mesh(name,category)
def drop_degenerate_faces115(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b115_finish(m,osm='',dp=115,notes='references/block115-notes.md'):
 obj=s21_finish(m);obj['block115_dropped_faces']=drop_degenerate_faces115(obj);print('BLOCK115_DROPPED',m.name,obj['block115_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=dp;obj['reference_notes']=notes;obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 98's chunks without the detailed houses
# SLOTT98_DETAILED holds the OSM ids of the pass-98 mainland houses that later passes model as their
# own meshes. Pass 107 took the Stagnell chapel (500979084); this pass adds its fourteen houses. A later
# pass adds its ids to the set and calls slott98_chunks115 with the chunk keys its houses sit in;
# the chunks are then re-created by pass 98's own code (its materials, ground height 0.30, wall colour
# hash, roofs), every remaining house identical to pass 98's.
SLOTT98_DETAILED=globals().get('SLOTT98_DETAILED',set())|{'500979084'}
SLOTT98_DETAILED|=set(B115D['ids'])
WALLS98_115=['Ochre','White','PaleYellow','RedBoard','Grey','Brick','PaleGreen','White','Ochre','PaleYellow']  # pass 98's WALLS
def slott98_key115(b):
 cx_=sum(v[0] for v in b['outer'])/len(b['outer']);return 'W' if cx_<-1150 else ('M' if cx_<-850 else 'E')
def slott98_chunks115(keys,by_pass=115,names=None):
 # Re-create the chunk meshes SM_Slott98_Buildings_<key> for the given keys ('W', 'M', 'E') with
 # pass 98's exact code, skipping every id in SLOTT98_DETAILED. Returns the objects.
 objs=[]
 for key in sorted(keys):
  m=b115_new('SM_Slott98_Buildings_'+key,'Slottsområdet/Buildings',names)
  for b in B98D['buildings']:
   if slott98_key115(b)!=key or b['id'] in SLOTT98_DETAILED:continue
   ring=[tuple(v) for v in b['outer']];h=int(hashlib.sha256(b['id'].encode()).hexdigest()[:6],16)
   levels=b['levels'];H=b['height'] or (levels*3.0+.5);H=max(2.6,min(H,28.0))
   wm=B98[WALLS98_115[h%len(WALLS98_115)]] if b['kind'] not in ('garage','shed','garages') else B98['Grey']
   for p,q in zip(ring,ring[1:]+ring[:1]):
    if math.dist(p,q)<.3:continue
    w={'p':list(p),'q':list(q),'z0':0.0}
    if levels<=0 or H<3.2 or b['kind'] in ('garage','garages','shed','roof'):bz_wall(m,w['p'],w['q'],0,H,[],wm)
    else:plain(m,w,H,wm,B98['Frame'],B98['Frame'],levels,0.30+.9)
   r,Ls,Lt,fill=frame98(ring)
   if fill>.9 and min(Ls,Lt)<16 and len(ring)<=8:
    inset_roof(m,r,H,min(Ls,Lt)/2-.30,min(Ls,Lt)/2*.62,B98['Tile'] if h%3 else B98['DarkRoof'],.35)
   else:
    m.faces([(*v,H) for v in ring],[tuple(range(len(ring))),tuple(range(len(ring)-1,-1,-1))],B98['DarkRoof'])
    for p,q in zip(ring,ring[1:]+ring[:1]):
     L=math.dist(p,q)
     if L<.3:continue
     x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.20,H+.3,L+.2,.25,.6,wm,a)
  if not m.v:
   if names is None:block115_names.remove(m.name)
   continue
  obj=b115_finish(m,'',98,'references/block98-notes.md');obj['rebuilt_by_pass']=by_pass;objs.append(obj)
 return objs
slott98_chunks115({slott98_key115(b) for b in B98D['buildings'] if b['id'] in B115D['ids']})

# ---------------------------------------------------------------- helpers
G=ZG115
def zabs115(h):return G+h
def rect115(pts,a,b):
 # The points boxed in the frame of the front a->b: a counter-clockwise rectangle whose first edge
 # runs along the front; also its length and depth.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in pts];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in pts]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))
 if area<0:r=[r[1],r[0],r[3],r[2]]
 return r,max(ss)-min(ss),max(ts)-min(ts)
def P115(a,b,s,t=0):
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return (a[0]+d[0]*s-d[1]*t,a[1]+d[1]*s+d[0]*t)
def clean115(poly,tol=.25):
 out=[]
 for v in poly:
  if not out or math.dist(out[-1],v)>tol:out.append(tuple(v))
 if len(out)>3 and math.dist(out[0],out[-1])<tol:out.pop()
 return out
def zrect115(zone,k=None):
 z=Z115[zone];pts=[v for g in (z['polygons'] if k is None else [z['polygons'][k]]) for v in g]
 if z['front']:a,b=z['front']
 else:
  g=z['polygons'][0 if k is None else k];a,b=max(zip(g,g[1:]+g[:1]),key=lambda pq:math.dist(*pq))  # no front given: the longest edge
 return rect115(pts,a,b)
def rect_walls115(r):return [{'p':list(p),'q':list(q),'z0':0.0,'kind':'outer'} for p,q in zip(r,r[1:]+r[:1])]
def arch115(m,x,y,u,zs,w,a,frame,o=.16,k=10):
 # Semicircular glazed head over an opening of width w springing at zs, with a frame rim.
 r=w/2;pts=[lp(x,y,u+r*math.cos(math.pi*i/k),o-.04,zs+r*math.sin(math.pi*i/k),a) for i in range(k+1)]
 m.faces(pts,[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.06)*math.cos(math.pi*i/k),.38,zs+(r+.06)*math.sin(math.pi*i/k),a) for i in range(k+1)],.06,frame)
 town_path(m,[lp(x,y,u+r*math.cos(math.pi*i/k),o,zs+r*math.sin(math.pi*i/k),a) for i in range(k+1)],.035,frame)
def window115(m,x,y,u,b,w,h,a,st,arch=False,rows=None):
 fr=M115[st.get('frame','Frame')];cas81(m,x,y,u,b,w,h,a,fr,.16,rows or (3 if h>1.5 else 2))
 if st.get('surround',True):
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+(h+(w/2 if arch else 0))/2,.12,.06,h+(w/2 if arch else 0),fr,a)
  if not arch:facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a)
 facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,M115[st.get('sill','Frame')],a)
 if arch:arch115(m,x,y,u,b+h,w,a,fr)
 if st.get('hood'):facade_box(m,x,y,u,.46,b+h+.32,w+.5,.22,.14,M115[st.get('trim','Frame')],a)
def door115(m,x,y,u,b,w,h,a,st,arch=False,glass=False):
 fr=M115[st.get('frame','Frame')];leaf=M115[st.get('door','Door')]
 if glass:
  facade_box(m,x,y,u,.14,b+h/2,w,.02,h,GLAZE,a)
  for q in (-w/2+.05,0,w/2-.05):facade_box(m,x,y,u+q,.18,b+h/2,.08,.08,h,fr,a)
  for zz in (b+.05,b+h*.45,b+h-.05):facade_box(m,x,y,u,.18,zz,w,.08,.08,fr,a)
 else:
  facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GLAZE,a)
  for zz in (b+h*.30,):facade_box(m,x,y,u,.17,zz,w-.32,.03,h*.32,leaf,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.06),.38,b+(h+(w/2 if arch else 0))/2,.12,.06,h+(w/2 if arch else 0),fr,a)
 if arch:arch115(m,x,y,u,b+h,w,a,fr,.14)
 else:facade_box(m,x,y,u,.38,b+h+.06,w+.24,.06,.12,fr,a)
def steps115(m,x,y,u,w,top,a,ma,o=.36,tread=.32):
 n=max(1,round((top-G)/.17))
 for k in range(n):facade_box(m,x,y,u,o+tread*(n-k)/2,G+(k+.5)*(top-G)/n,w,tread*(n-k),(top-G)/n,ma,a)
def gable_tri115(m,p,q,c,zb,zt,ma):
 m.faces([(*p,zb),(*q,zb),(*c,zt)],[(0,1,2),(2,1,0)],ma)
def saddle115(m,r,H,T,ma,wall,ov=.40,verge=.35):
 # Saddle roof over rectangle r (ridge along r[0]->r[1]); gable triangles in the wall material.
 p0,p1,p2,p3=r;mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 e0,e1=mid(p0,p3),mid(p1,p2);half=math.dist(p0,p3)/2;sl=(T-H)/half
 ex=lambda p,q,k:(p[0]+(p[0]-q[0])/math.dist(p,q)*k,p[1]+(p[1]-q[1])/math.dist(p,q)*k)
 L=math.dist(p0,p1);dx,dy=(p1[0]-p0[0])/L,(p1[1]-p0[1])/L;sh=lambda p,s:(p[0]+dx*s,p[1]+dy*s)
 q0,q1,q2,q3=sh(ex(p0,p3,ov),-verge),sh(ex(p1,p2,ov),verge),sh(ex(p2,p1,ov),verge),sh(ex(p3,p0,ov),-verge);f0,f1=sh(e0,-verge),sh(e1,verge)
 for quad,zs in (([q0,q1,f1,f0],[H-ov*sl,H-ov*sl,T,T]),([f1,q2,q3,f0],[T,H-ov*sl,H-ov*sl,T])):
  m.faces([(*v,z) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
  m.faces([(*v,z-.12) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
 for a_,b_,c_ in ((p0,p3,e0),(p1,p2,e1)):
  # gable wall 0.355 thick, outside the line like the walls
  n_=(-dx,-dy) if c_ is e0 else (dx,dy);o=lambda v,k:(v[0]+n_[0]*k,v[1]+n_[1]*k)
  m.faces([(*o(a_,.005),H),(*o(b_,.005),H),(*o(c_,.005),T),(*o(a_,.355),H),(*o(b_,.355),H),(*o(c_,.355),T)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],wall)
 return (q0,q1,q2,q3),sl,((p0,p3,e0,(-dx,-dy)),(p1,p2,e1,(dx,dy)))
def pediment115(m,p,q,c,n,H,T,trim,lune=None,win=None,st=None):
 # Classical pediment over a gable end p-q (apex c, outward normal n): horizontal and raking cornices.
 o=lambda v,k:(v[0]+n[0]*k,v[1]+n[1]*k)
 town_rod(m,(*o(p,.42),H-.05),(*o(q,.42),H-.05),.13,trim,8)
 for u_ in (p,q):town_rod(m,(*o(u_,.48),H+.02),(*o(c,.48),T+.08),.11,trim,8)
 x,y,L,a=sf_edge(p,q);
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 if lune:
  r=lune;k=12;zs=H+.35
  m.faces([lp(x,y,r*math.cos(math.pi*i/k),.37,zs+r*math.sin(math.pi*i/k),a) for i in range(k+1)],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
  town_path(m,[lp(x,y,(r+.08)*math.cos(math.pi*i/k),.42,zs+(r+.08)*math.sin(math.pi*i/k),a) for i in range(k+1)],.07,trim)
  facade_box(m,x,y,0,.42,zs-.03,2*r+.3,.10,.08,trim,a)
  for i in range(1,4):town_rod(m,lp(x,y,0,.40,zs,a),lp(x,y,r*math.cos(math.pi*i/4),.40,zs+r*math.sin(math.pi*i/4),a),.025,trim,6)
 if win:
  b,w,h=win;window115(m,x,y,0,b,w,h,a,st)
 return x,y,a
def boards115(m,w,z0,z1,holes,ma,step=.21):
 x,y,L,a=sf_edge(w['p'],w['q']);boards81(m,x,y,L,a,z0,z1,holes,ma,step)
def chimney115(m,X,Y,z0,z1,ma,ang=0,w=.6,d=.6):
 m.box((X,Y,(z0+z1)/2),(w,d,z1-z0),ma,ang);m.box((X,Y,z1+.05),(w+.12,d+.12,.10),M115['Stone'],ang)

# ---------------------------------------------------------------- styles
# Per zone: wall/trim/frame materials, window rows (bottom, height, width above the ground; 'arch'),
# bay spacing, plinth height and colour, cornice, boards. All heights in metres above the ground.
ST={
 'mu':dict(rows=[],plinth=0,cornice=False,frame='FrameDark'),
 'by':dict(rows=[(1.0,1.3,1.3)],bay=3.0,plinth=.45,plinth_ma='Stone',frame='FrameDark',sill='Frame',roof='RoofDark',low_inset=3.0,ov=.95),
 'pa':dict(rows=[(1.0,1.3,1.0)],bay=3.0,plinth=.35,plinth_ma='Stone',frame='Frame',roof='Tile'),
 'pb':dict(rows=[(1.0,1.2,1.0)],bay=3.0,plinth=.35,plinth_ma='Stone',frame='Frame',roof='RoofDark',low_inset=2.5,ov=.6),
 'shg':dict(rows=[(1.0,1.35,1.0)],bay=3.2,plinth=.35,plinth_ma='Stone',frame='Ochre',sill='Ochre',boards=True,trim='Ochre',roof='RoofSlate'),
 'shm':dict(rows=[(1.1,1.7,1.15),(4.6,1.6,1.15)],bay=2.8,plinth=.5,plinth_ma='Stone',frame='Frame',roof='Tile',trim='Frame'),
 'shn':dict(rows=[(1.1,1.7,1.15),(4.6,1.6,1.15)],bay=2.8,plinth=.5,plinth_ma='Stone',frame='Frame',roof='Tile',trim='Frame'),
 'vl':dict(rows=[(1.0,1.4,1.3)],bay=3.4,plinth=.45,plinth_ma='Stone',frame='FrameDark',roof='TileBrown',trim='Salmon',sill='Frame'),
 'rb':dict(rows=[(1.0,1.8,.9)],bay=2.6,plinth=.3,plinth_ma='Stone',frame='Frame',roof='RoofSlate',trim='Brick'),
 'rv':dict(veranda=True,roof='RoofDark'),
 'gs':dict(rows=[],plinth=.2,plinth_ma='Stone',boards=True,frame='Frame',roof='RoofDark',trim='DarkGreen'),
 'gl':dict(rows=[(1.1,1.0,1.0)],bay=2.4,plinth=.25,plinth_ma='Stone',boards=True,frame='Frame',roof='RoofDark',trim='DarkGreen'),
 'vi':dict(rows=[(1.35,2.0,1.15,'arch'),(5.35,2.1,1.15)],bay=2.75,plinth=.95,plinth_ma='Stone',frame='Frame',roof='RoofSlate',trim='PaleCream',string=4.85,rectwalls=True),
 'vs':dict(steps=True),
 'vr':dict(rows=[(1.3,1.6,1.0),(4.6,1.5,1.0)],bay=2.8,plinth=.9,plinth_ma='Stone',frame='Frame',roof='RoofSlate',trim='PaleCream'),
 'mp':dict(rows=[(.75,1.85,1.1,'arch')],bay=3.0,plinth=.35,plinth_ma='Stone',frame='Frame',roof='RoofBrown',trim='White',rectwalls=True),
 'rt':dict(rows=[(1.55,1.75,1.15),(4.85,1.75,1.15)],bay=2.66,plinth=1.0,plinth_ma='Stone',frame='Frame',roof='RoofDark',trim='PaleCream',rectwalls=True),
 'so':dict(rows=[(1.05,2.2,1.1)],bay=3.0,plinth=.6,plinth_ma='Stone',frame='Frame',roof='RoofSlate',trim='PaleCream',hood=True,rectwalls=True,pilasters=True),
 'sw':dict(rows=[(1.1,1.0,.9)],bay=3.0,plinth=.3,plinth_ma='Stone',frame='Frame',roof='RoofDark',trim='Grey'),
 'ki':dict(rows=[],plinth=.3,plinth_ma='Stone',frame='Frame',roof='RoofDark',trim='White'),
}
WALLMA={'Black':'Black','White':'White','Cream':'Cream','Green':'Green','Red':'Red','Salmon':'Salmon','Brick':'Brick','Veranda':'Timber',
 'DarkGreen':'DarkGreen','Stone':'Stone','Grey':'Grey'}
# Doors: zone -> [(X, Y, width, height, bottom, kind)], kind 'door', 'arch' (arched door) or 'glass'.
VS=Z115['vi']['front'];SOF=Z115['so']['front'];RTF=Z115['rt']['front'];VLF=Z115['vl']['front'];SHF=Z115['shm']['front'];SGF=Z115['shg']['front']
DOORS={
 'vi':[(*P115(VS[0],VS[1],16.55,6.0),1.5,2.5,.95,'arch')],
 'rt':[(*P115(RTF[0],RTF[1],8.5),1.6,2.3,.25,'glass')],
 'so':[(*P115(SOF[0],SOF[1],11.0,11.75),1.2,2.4,.6,'door')],
 'vl':[(*P115(VLF[0],VLF[1],4.6),1.1,2.1,.45,'door')],
 'shm':[(*P115(SHF[0],SHF[1],8.2),1.3,2.4,.5,'door')],
 'shg':[(*P115(SGF[0],SGF[1],5.0),1.0,2.1,.35,'door')],
 'mp':[(-853.3,-51.8,1.1,2.2,.35,'door')],
 'by':[(-716.0,-53.7,1.6,2.4,.0,'glass')],
 'pa':[(-853.0,-87.8,1.0,2.1,.3,'door')],'pb':[(-745.2,-76.4,1.0,2.1,.3,'door')],
 'gl':[(-774.0,10.3,1.0,2.1,.2,'door')],'gs':[(-767.05,24.35,.9,2.0,.15,'door')],
 'rb':[(-788.6,7.0,1.0,2.2,.3,'door')],
}
SKIPWIN={'mu'}

meshes={}
for zone,z in Z115.items():
 if z['mesh'] not in meshes:meshes[z['mesh']]=b115_new(z['mesh'],'Slottsområdet/Buildings')
def zone_walls115(zone):
 z=Z115[zone];st=ST[zone]
 if st.get('rectwalls'):
  r,_,_=zrect115(zone);return rect_walls115(r)
 return z['walls']
for zone,z in Z115.items():
 m=meshes[z['mesh']];st=ST[zone];H=zabs115(z['height']);wm=M115[WALLMA[z['wall']]];tm=M115[st.get('trim','Frame')]
 if st.get('steps'):
  poly=clean115(z['polygons'][0],.1);m.prism(poly if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1]))>0 else poly[::-1],0,H,M115['Step']);continue
 if st.get('veranda'):
  # Glazed timber veranda: a boarded parapet, glazing between posts, a flat roof with a fascia.
  for w in z['walls']:
   x,y,L,a=sf_edge(w['p'],w['q'])
   if w['kind']!='outer':bz_wall(m,w['p'],w['q'],zabs115(w['z0']),H,[],M115['Timber']);continue
   facade_box(m,x,y,0,.18,(G+.9)/2,L,.30,G+.9,M115['Timber'],a);facade_box(m,x,y,0,.18,(G+.9+H)/2,L,.03,H-G-.9,GLAZE,a)
   n=max(1,round(L/1.1))
   for k in range(n+1):facade_box(m,x,y,-L/2+k*L/n,.22,(G+.9+H)/2,.12,.14,H-G-.9,M115['Timber'],a)
   facade_box(m,x,y,0,.22,G+.95,L,.16,.10,M115['Timber'],a);facade_box(m,x,y,0,.30,H+.05,L+.3,.20,.40,M115['RoofDark'],a)
  for g in z['polygons']:
   g=clean115(g,.1);m.faces([(*v,H+.2) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M115['RoofDark'])
  continue
 doors=[d for d in DOORS.get(zone,[])]
 for w in zone_walls115(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs115(w['z0'])
  if L<.25:continue
  mine=[]
  if w['kind']=='outer':
   for X,Y,dw,dh,db,kind in doors:
    u=U(w,X,Y);off=abs((X-x)*math.sin(a)-(Y-y)*math.cos(a))
    if off<.8 and abs(u)+dw/2<=L/2+.05:mine.append((kind,u,zabs115(db),dw,dh))
  holes=[(u,b,dw,dh,dw/2 if kind=='arch' else 0) for kind,u,b,dw,dh in mine]
  wins=[]
  if zone not in SKIPWIN:
   bay=st.get('bay',3.0);n=int(L/bay+.35)
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for row in st['rows']:
     b,hh,ww=zabs115(row[0]),row[1],row[2];arch=len(row)>3
     if b<z0+.3 or b+hh+(ww/2 if arch else 0)>H-.25:continue
     if any(abs(u-du)<(ww+dw)/2+.35 and b<db+dh+.2 for _,du,db,dw,dh in mine):continue
     if L<ww+1.0:continue
     wins.append((u,b,ww,hh,arch))
  holes+=[(u,b,ww,hh,ww/2 if arch else 0) for u,b,ww,hh,arch in wins]
  bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if st.get('boards'):boards115(m,w,max(z0,G+st.get('plinth',.3)+.02),H-.1,holes,wm)
  for u,b,ww,hh,arch in wins:window115(m,x,y,u,b,ww,hh,a,st,arch)
  for kind,u,b,dw,dh in mine:
   door115(m,x,y,u,b,dw,dh,a,st,kind=='arch',kind=='glass')
   if b>G+.15:steps115(m,x,y,u,dw+.6,b,a,M115['Step'])
  if w['kind']=='outer' and st.get('plinth'):facade_box(m,x,y,0,.40,(G+st['plinth'])/2,L+.02,.10,G+st['plinth'],M115[st['plinth_ma']],a)
  if st.get('string') and w['kind']=='outer':facade_box(m,x,y,0,.42,zabs115(st['string']),L+.1,.14,.16,tm,a)
  if st.get('cornice',True):facade_box(m,x,y,0,.44,H-.12,L+.12,.18,.24,tm,a)
  if st.get('boards'):
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+G+st['plinth'])/2,.20,.10,H-G-st['plinth'],tm,a)
  if st.get('pilasters') and w['kind']=='outer':
   for uu in [-L/2+.25,L/2-.25]+[(wins[i][0]+wins[i+1][0])/2 for i in range(len(wins)-1)]:facade_box(m,x,y,uu,.40,(H+G+st['plinth'])/2,.42,.10,H-G-st['plinth'],tm,a)

# ---------------------------------------------------------------- roofs and the special parts
def flatroof115(m,zone,H,T,ma,trim,inset=0):
 for g in Z115[zone]['polygons']:
  g=clean115(g,.1)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.18,(H+T)/2+.05,L+.36,.40,T-H+.1,trim,a)
def low115(m,zone,H,T,ma,inset,ov):
 for g in Z115[zone]['polygons']:
  g=clean115(g,.3)
  if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))<0:g=g[::-1]
  inset_roof(m,g,H,inset,T-H,ma,ov)

# Konstmuseum: black square panels (ribs on a 1.25 m grid), glazed entrance with a sign band,
# a few large windows, steps and a landing towards the park.
z=Z115['mu'];m=meshes[z['mesh']];H=zabs115(z['height'])
flatroof115(m,'mu',H,H+.25,M115['Black'],M115['Black'])
ENT115=[]
for w in z['walls']:
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer' or L<.6:continue
 glazed=x<-703.0 and 1.0<L<7.0  # the short north-west faces by the entrance, not the wall against Byttan
 for k in range(1,int((H-G)/1.25)+1):
  zz=G+k*1.25
  if glazed and zz<G+4.3:continue
  facade_box(m,x,y,0,.38,zz,L+.04,.05,.05,M115['BlackRib'],a)
 nv=int(L/1.25)
 for k in range(1,nv):facade_box(m,x,y,-L/2+k*L/nv,.38,(H+(G+4.3 if glazed else G))/2,.05,.05,H-(G+4.3 if glazed else G),M115['BlackRib'],a)
 if glazed:ENT115.append((x,y,L,a))
for x,y,L,a in ENT115:
 # The glazed ground floor: glass recessed behind the black block above, mullions, the sign band.
 facade_box(m,x,y,0,.36,G+.6+1.55,L-.1,.02,3.1,GLAZE,a)
 for k in range(int(L/1.3)+1):facade_box(m,x,y,-L/2+.05+k*(L-.1)/max(1,int(L/1.3)),.40,G+.6+1.55,.07,.10,3.1,M115['FrameDark'],a)
 facade_box(m,x,y,0,.42,G+4.0,L+.05,.12,.6,M115['Sign'],a)
 facade_box(m,x,y,0,1.6,G+.3,L+.6,3.0,.6,M115['Step'],a)
 for k in range(3):facade_box(m,x,y,0,3.1+.32*(2-k)+.16,G+(k+1)*.1,L+.6,.32,(k+1)*.2,M115['Step'],a)
MUP=[tuple(v) for v in B98D['buildings'][[b['id'] for b in B98D['buildings']].index('91931339')]['outer']]
for (i,j),zc,ww,hh in (((5,6),G+9.0,4.2,3.4),((4,5),G+5.2,3.2,2.6),((6,7),G+12.4,2.4,3.0)):
 p,q=MUP[i],MUP[j];x,y,L,a=sf_edge(p,q)
 if math.sin(a)*(x-(-696.0))-math.cos(a)*(y-(-46.0))<0:x,y,L,a=sf_edge(q,p)
 facade_box(m,x,y,0,.36,zc,ww,.02,hh,GLAZE,a);surround36(m,x,y,0,zc-hh/2,ww,hh,a,M115['FrameDark'],.10,.40)

# Byttan: low dark roof with wide eaves, the set-back upper storey with a band of windows.
z=Z115['by'];m=meshes[z['mesh']];H=zabs115(z['height']);up=z['upper']
low115(m,'by',H,zabs115(z['top']),M115['RoofDark'],ST['by']['low_inset'],ST['by']['ov'])
g=clean115(z['polygons'][0]);g=g if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))>0 else g[::-1]
ug=ring_offset(g,-up['inset']);UH=zabs115(up['height'])
for p,q in zip(ug,ug[1:]+ug[:1]):
 x,y,L,a=sf_edge(p,q);n=max(1,int(L/2.4));holes=[(-L/2+(k+.5)*L/n,zabs115(z['top'])+.9,1.5,1.1,0) for k in range(n)]
 bz_wall(m,p,q,zabs115(z['top'])-.3,UH,holes,M115['White'])
 for u,b,ww,hh,_ in holes:cas81(m,x,y,u,b,ww,hh,a,M115['FrameDark'],.16,2)
inset_roof(m,ug,UH,2.2,.4,M115['RoofDark'],.7)
chimney115(m,*P115(z['front'][0],z['front'][1],6.0,7.0),zabs115(z['top'])-.5,UH+.9,M115['White'])

# Park pavilions (no usable view): hip and low roofs.
for zone in ('pa',):
 z=Z115[zone];m=meshes[z['mesh']];r,Ls,Lt=zrect115(zone);inset_roof(m,r,zabs115(z['height']),min(Ls,Lt)/2-.30,z['top']-z['height'],M115[ST[zone]['roof']],.45)
z=Z115['pb'];low115(meshes[z['mesh']],'pb',zabs115(z['height']),zabs115(z['top']),M115['RoofDark'],ST['pb']['low_inset'],ST['pb']['ov'])

# Slottshotellet: the green west wing (saddle, ridge along its south-east side, ochre bargeboards and
# gable window), the red main range (hip with two cross gables on the south-east front), the wing.
z=Z115['shg'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('shg')  # ridge along the south-east side: gables at the south-west and north-east ends
eav,sl,ends=saddle115(m,r,H,T,M115['RoofSlate'],M115['Green'])
for p,q,c,n in ends:
 o=lambda v,k:(v[0]+n[0]*k,v[1]+n[1]*k)
 for u_ in (p,q):
  e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
  town_rod(m,(*o(e,.62),H-.35*sl-.05),(*o(c,.62),T-.05),.09,M115['Ochre'],8)
  # carved bargeboard: a row of short drops under the verge board
  for k in range(1,9):
   t=k/9;px,py=e[0]+(c[0]-e[0])*t,e[1]+(c[1]-e[1])*t;zz=H-.35*sl+(T-H+.35*sl)*t
   m.box((*o((px,py),.62),zz-.22),(.06,.05,.24),M115['Ochre'],math.atan2(c[1]-e[1],c[0]-e[0]))
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 window115(m,x,y,0,H+.45,.85,1.15,a,ST['shg'])
z=Z115['shm'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('shm');inset_roof(m,r,H,min(Ls,Lt)/2-.30,T-H,M115['Tile'],.40)
x,y,L,a=sf_edge(*SHF);a0=a
for s_ in (3.6,12.8):
 u=U({'p':SHF[0],'q':SHF[1]},*P115(SHF[0],SHF[1],s_));frontis83(m,x,y,u,3.6,H,H+1.4,H+3.6,a,M115['Red'],M115['Frame'],M115['Tile'],False)
 window115(m,x,y,u,H+.1,1.0,1.3,a,ST['shm'])
chimney115(m,*P115(SHF[0],SHF[1],8.0,5.0),T-1.0,T+.9,M115['Red'],a0)
z=Z115['shn'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
for k in range(len(z['polygons'])):
 r,Ls,Lt=zrect115('shn',k);inset_roof(m,r,H,min(Ls,Lt)/2-.30,min(T-H,(min(Ls,Lt)/2)*1.05),M115['Tile'],.40)

# Västerlånggatan 1: saddle along the street side, cross gable with the arched balcony door, the
# balcony on the porch, chimney.
z=Z115['vl'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('vl');saddle115(m,r,H,T,M115['TileBrown'],M115['Salmon'],.45)
x,y,L,a=sf_edge(*VLF)
if math.sin(a)*(x-(-717.5))-math.cos(a)*(y-79.4)<0:x,y,L,a=sf_edge(VLF[1],VLF[0])
u=U({'p':list(VLF[0]),'q':list(VLF[1])},*P115(VLF[0],VLF[1],4.6))
if sf_edge(*VLF)[3]!=a:u=-u
frontis83(m,x,y,u,4.4,H,H+2.0,T-.6,a,M115['Salmon'],M115['Salmon'],M115['TileBrown'],False)
door115(m,x,y,u,H+.15,1.1,1.6,a,ST['vl'],True,True)
facade_box(m,x,y,u,.36+.75,zabs115(3.25),4.2,1.5,.18,M115['Stone'],a)
for s in (-1,1):facade_box(m,x,y,u+s*1.9,.36+1.35,(G+zabs115(3.2))/2,.22,.22,zabs115(3.2)-G,M115['Salmon'],a)
town_rod(m,lp(x,y,u-2.05,1.80,zabs115(4.25),a),lp(x,y,u+2.05,1.80,zabs115(4.25),a),.03,M115['Iron'],6)
for k in range(15):town_rod(m,lp(x,y,u-2.05+k*4.1/14,1.80,zabs115(3.34),a),lp(x,y,u-2.05+k*4.1/14,1.80,zabs115(4.25),a),.012,M115['Iron'],4)
for s in (-1,1):town_rod(m,lp(x,y,u+s*2.05,.40,zabs115(4.25),a),lp(x,y,u+s*2.05,1.80,zabs115(4.25),a),.03,M115['Iron'],6)
chimney115(m,*P115(VLF[0],VLF[1],8.8,5.1),T-1.2,T+.8,M115['Chimney'],a)

# The red-brick house: saddle along its north-west wall, standing-seam roof with roof lights on the
# south-east slope.
z=Z115['rb'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('rb');eav,sl,ends=saddle115(m,r,H,T,M115['RoofSlate'],M115['Brick'])
p0,p1,p2,p3=r;d=((p1[0]-p0[0])/Ls,(p1[1]-p0[1])/Ls);ang=math.atan2(d[1],d[0])
for s_ in (3.2,6.4,7.6,11.0):
 # on the south-east slope, 22 % of the depth up from its eaves; the slope rises towards -n
 X,Y=p0[0]+d[0]*s_+(p3[0]-p0[0])*.78,p0[1]+d[1]*s_+(p3[1]-p0[1])*.78
 skylight82(m,X,Y,H+(Lt*.22)*sl+.03,ang+math.pi,sl)
for k in range(1,int(Ls/.5)):
 for half in (0,1):
  s_=k*.5;e=(p0[0]+d[0]*s_,p0[1]+d[1]*s_) if half==0 else (p3[0]+d[0]*s_,p3[1]+d[1]*s_);c=(e[0]+(p3[0]-p0[0])/2*(1 if half==0 else -1),e[1]+(p3[1]-p0[1])/2*(1 if half==0 else -1))
  town_rod(m,(*e,H+.06),(c[0],c[1],T+.06),.012,M115['RoofDark'],4)
for p,q,c,n in ends:
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*n[0]-math.cos(a)*n[1]<0:x,y,L,a=sf_edge(q,p)
 for s in (-.7,.7):window115(m,x,y,s,H+.3,.7,1.5,a,ST['rb'],True)
z=Z115['gs'];flatroof115(meshes[z['mesh']],'gs',zabs115(z['height']),zabs115(z['top']),M115['RoofDark'],M115['DarkGreen'])
z=Z115['gl'];flatroof115(meshes[z['mesh']],'gl',zabs115(z['height']),zabs115(z['top']),M115['RoofDark'],M115['DarkGreen'])

# The cream villa: saddle along Slottsvägen, the east gable as a pediment with a window and a round
# ornament, the arched door on its steps.
z=Z115['vi'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('vi');eav,sl,ends=saddle115(m,r,H,T,M115['RoofSlate'],M115['Cream'],.55)
p,q,c,n=ends[1];xx,yy,aa=pediment115(m,p,q,c,n,H,T,M115['PaleCream'],None,(H+.35,1.0,1.4),ST['vi'])
k=20;zc=H+.55;uo=1.6
m.faces([lp(xx,yy,uo+.28*math.cos(t*math.tau/k),.40,zc+1.5+.28*math.sin(t*math.tau/k),aa) for t in range(k)],[tuple(range(k)),tuple(range(k-1,-1,-1))],M115['PaleCream'])
p,q,c,n=ends[0];pediment115(m,p,q,c,n,H,T,M115['PaleCream'])
z=Z115['vr'];flatroof115(meshes[z['mesh']],'vr',zabs115(z['height']),zabs115(z['top']),M115['RoofSlate'],M115['PaleCream'])

# The mansard pavilion: lower steep slopes, a low hipped top, a dormer on each long side, chimney.
z=Z115['mp'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('mp');BRK=H+2.3
outer,inner=inset_roof(m,r,H,.95,BRK-H,M115['RoofBrown'],.40)
inset_roof(m,inner,BRK,min(Ls,Lt)/2-.95-.10,T-BRK,M115['RoofBrown'],.0)
cx_,cy_=sum(v[0] for v in r)/4,sum(v[1] for v in r)/4;chimney115(m,cx_,cy_,T-.4,T+.9,M115['White'],math.atan2(r[1][1]-r[0][1],r[1][0]-r[0][0]))
for i in range(4):
 p,q=r[i],r[(i+1)%4];x,y,L,a=sf_edge(p,q)
 if L<Ls-.1:continue
 # a dormer standing on the steep slope (slope 2.3/0.95)
 for uu in ((0,) if L<10 else (-2.2,2.2)):
  zb=H+.95;box(m,*lp(x,y,uu,-.85,0,a)[:2],1.3,1.6,1.55,zb-.4,M115['White'],a)
  facade_box(m,x,y,uu,-.05,zb+.45,.8,.02,1.0,GLAZE,a);cas81(m,x,y,uu,zb-.05,.8,1.0,a,M115['Frame'],-.02,2)
  pts=[lp(x,y,uu-.75,.0,zb+1.15,a),lp(x,y,uu+.75,.0,zb+1.15,a),lp(x,y,uu+.75,-1.7,zb+1.15,a),lp(x,y,uu-.75,-1.7,zb+1.15,a),lp(x,y,uu,.0,zb+1.55,a),lp(x,y,uu,-1.7,zb+1.55,a)]
  m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],M115['RoofBrown'])

# The cream house with the rooftop storey: flat roof with a railing, a dark set-back storey with
# windows, and the glazed entrance porch under a low dark roof.
z=Z115['rt'];m=meshes[z['mesh']];H=zabs115(z['height']);up=z['upper'];UH=zabs115(up['height'])
r,Ls,Lt=zrect115('rt');m.faces([(*v,H+.05) for v in r],[(0,1,2,3),(3,2,1,0)],M115['RoofDark'])
ug=[r[0],r[1],r[2],r[3]];d=((r[1][0]-r[0][0])/Ls,(r[1][1]-r[0][1])/Ls);nrm=(-d[1],d[0])
ug=[(r[0][0]+d[0]*.6+nrm[0]*up['inset'],r[0][1]+d[1]*.6+nrm[1]*up['inset']),(r[1][0]-d[0]*.6+nrm[0]*up['inset'],r[1][1]-d[1]*.6+nrm[1]*up['inset']),
 (r[2][0]-d[0]*.6-nrm[0]*up['inset'],r[2][1]-d[1]*.6-nrm[1]*up['inset']),(r[3][0]+d[0]*.6-nrm[0]*up['inset'],r[3][1]+d[1]*.6-nrm[1]*up['inset'])]
for p,q in zip(ug,ug[1:]+ug[:1]):
 x,y,L,a=sf_edge(p,q);n=max(1,int(L/3.0));holes=[(-L/2+(k+.5)*L/n,H+.5,1.5,1.4,0) for k in range(n)] if L>5 else []
 bz_wall(m,p,q,H,UH,holes,M115['RoofDark'])
 for u,b,ww,hh,_ in holes:cas81(m,x,y,u,b,ww,hh,a,M115['Frame'],.16,2)
 facade_box(m,x,y,0,.40,UH-.05,L+.3,.25,.2,M115['RoofDark'],a)
m.faces([(*v,UH+.02) for v in ug],[(0,1,2,3),(3,2,1,0)],M115['RoofDark'])
for p,q in zip(r,r[1:]+r[:1]):
 x,y,L,a=sf_edge(p,q);town_rod(m,lp(x,y,-L/2+.2,.2,H+1.05,a),lp(x,y,L/2-.2,.2,H+1.05,a),.025,M115['Iron'],6)
 for k in range(int(L/1.5)+1):town_rod(m,lp(x,y,-L/2+.2+k*(L-.4)/max(1,int(L/1.5)),.15,H+.05,a),lp(x,y,-L/2+.2+k*(L-.4)/max(1,int(L/1.5)),.15,H+1.05,a),.02,M115['Iron'],6)
x,y,L,a=sf_edge(*RTF);X,Y=P115(RTF[0],RTF[1],8.5)
if math.sin(a)*(x-(-876.5))-math.cos(a)*(y-(-45.7))<0:x,y,L,a=sf_edge(RTF[1],RTF[0])
u=U({'p':list(RTF[0]),'q':list(RTF[1])},X,Y)
if sf_edge(*RTF)[3]!=a:u=-u
facade_box(m,x,y,u,1.25,G+.15,3.4,1.9,.3,M115['Step'],a)
for s in (-1,1):facade_box(m,x,y,u+s*1.25,1.15,(G+.3+zabs115(3.6))/2,.12,1.6,zabs115(3.6)-G-.3,M115['Frame'],a)
facade_box(m,x,y,u,1.9,(G+.3+zabs115(3.6))/2,2.5,.04,zabs115(3.6)-G-.3,GLAZE,a)
for k in range(5):facade_box(m,x,y,u-1.25+k*.625,1.95,(G+.3+zabs115(3.6))/2,.07,.08,zabs115(3.6)-G-.3,M115['Frame'],a)
for zz in (G+.35,zabs115(1.3),zabs115(3.55)):facade_box(m,x,y,u,1.95,zz,2.6,.08,.08,M115['Frame'],a)
pts=[lp(x,y,u-1.6,2.25,zabs115(3.65),a),lp(x,y,u+1.6,2.25,zabs115(3.65),a),lp(x,y,u+1.6,.36,zabs115(3.65),a),lp(x,y,u-1.6,.36,zabs115(3.65),a),lp(x,y,u,2.25,zabs115(4.25),a),lp(x,y,u,.36,zabs115(4.25),a)]
m.faces(pts,[(0,1,4),(4,1,0),(1,2,5,4),(4,5,2,1),(3,0,4,5),(5,4,0,3)],M115['RoofDark'])

# Söderport: saddle along the long sides, the pediment with the lunette towards Kungsgatan.
z=Z115['so'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
r,Ls,Lt=zrect115('so');eav,sl,ends=saddle115(m,r,H,T,M115['RoofSlate'],M115['Cream'],.55)
p,q,c,n=ends[0];pediment115(m,p,q,c,n,H,T,M115['PaleCream'],1.0)
p,q,c,n=ends[1];pediment115(m,p,q,c,n,H,T,M115['PaleCream'])
z=Z115['sw'];flatroof115(meshes[z['mesh']],'sw',zabs115(z['height']),zabs115(z['top']),M115['RoofDark'],M115['Grey'])

# KIKAIN: a round kiosk under a conical roof, serving hatches.
z=Z115['ki'];m=meshes[z['mesh']];H=zabs115(z['height']);T=zabs115(z['top'])
g=clean115(z['polygons'][0],.1);cx_,cy_=sum(v[0] for v in g)/len(g),sum(v[1] for v in g)/len(g);rr=max(math.dist(v,(cx_,cy_)) for v in g)
m.lathe(cx_,cy_,H-.05,[(rr+.75,0),(rr+.75,.12),(.45,T-H-.15),(.12,T-H+.1)],M115['RoofDark'],16)
m.box((cx_,cy_,T+.15),(.12,.12,.5),M115['RoofDark'])
for i,(p,q) in enumerate(zip(g,g[1:]+g[:1])):
 if i%3:continue
 x,y,L,a=sf_edge(p,q);facade_box(m,x,y,0,.37,zabs115(1.6),L*.8,.03,.9,GLAZE,a);facade_box(m,x,y,0,.50,zabs115(1.1),L*.9,.30,.06,M115['Frame'],a)

for nm,m in meshes.items():b115_finish(m,nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block115_cameras=[
 sv_camera('580_Block115_Cal_SlottsvagenVilla',-781.2,-24.5,2.5,200,8),
 sv_camera('581_Block115_Cal_Pavilion',-850.5,-31.6,2.5,160,8),
 sv_camera('582_Block115_Cal_RooftopHouse',-879.8,-31.6,2.5,127,8),
 sv_camera('583_Block115_Cal_Soderport',-971.6,-101.5,2.5,18,8),
 ('584_Block115_Aerial',(-700.0,-175.0,85.0),(-790.0,0.0,2.0),24)]
print('BLOCK115_GEOMETRY',len(block115_names))
