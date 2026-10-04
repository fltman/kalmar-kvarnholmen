"""Pass 123: a correction of pass 115 (Stadsparken and Slottsvägen). Five of pass 115's meshes are
re-created under the same names and categories, from new contributor photos of the hotel courtyard
and the park and a closer reading of pass 115's own photos:
- SM_Slott115_93332243, Slottshotellet: the red rendered main range of two and a half storeys with
  white window surrounds and grey pilaster strips, a red tile hip with two dark dormers towards the
  courtyard; the steep cross gable that projects into the courtyard (two storeys and a gable storey
  with an attic window); the polygonal glazed porch with a terrace and railing on top and the
  entrance canopy; the front risalit on the south-east side under its own cross gable; the green
  boarded west wing (ochre trim, cross-barred windows, carved bargeboards and scalloped eaves under
  a black roof) and the low green link between it and the main range;
- SM_Slott115_91931339, Kalmar konstmuseum: the stepped black massing clad in shingle courses, the
  tall tower by the entrance, the lower core, the front block cantilevered over a recess on a
  slanted soffit, the tall glazed slot between tower and front block, and the low glazed entrance
  link towards Byttan with its sign band, landing and steps;
- SM_Slott115_91222116, Byttan: the white one-storey restaurant on its plinth under a low dark roof
  with wide eaves, the set-back upper storey with its band of windows and chimney, and the terrace
  with an iron railing along the park front;
- SM_Slott115_874870421: the grey boarded park pavilion under a dark saddle roof, with the glazed
  east gable and the glazed east half of its south side, and its lower annex;
- SM_Slott115_91222187: re-created in pass 115's plain form (a cream pavilion under a red tile hip),
  since no photo identifies it; the open shelter of the new park photo is not this outline.
Every other pass-115 mesh and the pass-98 chunks are left as they are (these five houses are
already in SLOTT98_DETAILED). References: contributor photos and Google Street View, view only.
Zones: source/block123.json; see references/block123-notes.md.
"""
B123D=json.loads((R/'source/block123.json').read_text());Z123=B123D['zones'];G123=B123D['ground_z']
block123_names=[];M123={}
for old in [k for k in list(materials) if k.startswith('M_Block123_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Black','TownMetalGrey',(.075,.075,.08),.80,.05),('BlackRib','TownMetalGrey',(.12,.12,.125),.75,.05),('Sign','TownMetalGrey',(.04,.04,.045),.50,.10),
 ('White','TownIvory',(.92,.91,.88),.88,0),('Red','TownIvory',(.66,.28,.21),.85,0),('Pilaster','TownIvory',(.44,.44,.45),.85,0),
 ('Green','TownPaintGreen',(.42,.52,.45),.75,0),('Ochre','TownIvory',(.82,.68,.40),.70,0),('GreyBoard','TownPaintWhite',(.58,.63,.62),.75,0),
 ('Stone','TownStone',(.55,.55,.53),.90,0),('Step','TownStone',(.63,.62,.59),.90,0),('Frame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('FrameDark','TownMetalGrey',(.10,.10,.11),.50,.20),('Tile','TownTileRed',(.70,.33,.22),.80,0),('RoofDark','TownMetalGrey',(.20,.20,.22),.60,.25),
 ('RoofBlack','TownMetalGrey',(.09,.09,.10),.45,.30),('Dormer','TownMetalGrey',(.24,.25,.27),.65,.20),('Door','TownPaintBrown',(.30,.21,.15),.70,0),
 ('DoorGreen','TownPaintGreen',(.24,.36,.31),.65,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),('Post','TownMetalGrey',(.13,.13,.14),.60,.20),
 ('Timber','TownPaintBrown',(.30,.22,.16),.70,0),('Cream','TownIvory',(.91,.86,.72),.88,0),('Chimney','TownIvory',(.80,.78,.74),.88,0),
 ]:
 name='M_Block123_'+key;M123[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block123_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
GL123=town_mats['Glass']
def b123_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block123_names.append(name);return Mesh(name,category)
def drop_degenerate_faces123(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b123_finish(m,osm):
 obj=s21_finish(m);obj['block123_dropped_faces']=drop_degenerate_faces123(obj);print('BLOCK123_DROPPED',m.name,obj['block123_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=123;obj['corrects_pass']=115;obj['reference_notes']='references/block123-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- helpers
def zabs123(h):return G123+h
def P123(fr,s,t=0):
 # The point s along the frame's a->b and t to its left (into the building).
 a,b=fr;L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return (a[0]+d[0]*s-d[1]*t,a[1]+d[1]*s+d[0]*t)
def rect123(fr,s0,s1,t0,t1):
 # Counter-clockwise rectangle in a frame (first edge along s at t0).
 return [P123(fr,s0,t0),P123(fr,s1,t0),P123(fr,s1,t1),P123(fr,s0,t1)]
def ccw123(g):
 g=[tuple(v) for v in g];return g if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(g,g[1:]+g[:1]))>0 else g[::-1]
def clean123(poly,tol=.25):
 out=[]
 for v in poly:
  if not out or math.dist(out[-1],v)>tol:out.append(tuple(v))
 if len(out)>3 and math.dist(out[0],out[-1])<tol:out.pop()
 return out
def frame_of123(zone):return tuple(tuple(v) for v in Z123[zone]['front'])
def st123(zone,fr=None):
 # The zone's extent in its frame: (s0, s1, t0, t1).
 fr=fr or frame_of123(zone);a,b=fr;L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L)
 pts=[v for g in Z123[zone]['polygons'] for v in g]
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in pts];ts=[-(v[0]-a[0])*d[1]+(v[1]-a[1])*d[0] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def uof123(x,y,a,X,Y):return (X-x)*math.cos(a)+(Y-y)*math.sin(a)
def outface123(p,q,ref):
 # sf_edge of the wall p-q turned so that +out points away from the point ref.
 x,y,L,a=sf_edge(p,q)
 if math.sin(a)*(x-ref[0])-math.cos(a)*(y-ref[1])<0:x,y,L,a=sf_edge(q,p)
 return x,y,L,a
def window123(m,x,y,u,b,w,h,a,frame='Frame',surround=None,sill='Frame',rows=None,cross=False,o=.16):
 fr=M123[frame];cas81(m,x,y,u,b,w,h,a,fr,o,rows or (3 if h>1.5 else 2))
 if cross:
  # cross-barred sashes (the green wing): two diagonals in each half
  for s0 in (-w/2+.06,.02):
   s1=s0+w/2-.08
   for z0,z1 in ((b+.06,b+h-.06),(b+h-.06,b+.06)):town_rod(m,lp(x,y,u+s0,o,z0,a),lp(x,y,u+s1,o,z1,a),.018,fr,4)
 if surround:surround36(m,x,y,u,b,w,h,a,M123[surround],.14,.38)
 facade_box(m,x,y,u,.45,b-.05,w+.24,.18,.06,M123[sill],a)
def door123(m,x,y,u,b,w,h,a,leaf='Door',frame='Frame',glass=False):
 fr=M123[frame]
 if glass:
  facade_box(m,x,y,u,.14,b+h/2,w,.02,h,GL123,a)
  for q in (-w/2+.05,0,w/2-.05):facade_box(m,x,y,u+q,.18,b+h/2,.08,.08,h,fr,a)
  for zz in (b+.05,b+h*.45,b+h-.05):facade_box(m,x,y,u,.18,zz,w,.08,.08,fr,a)
 else:
  lf=M123[leaf];facade_box(m,x,y,u,.12,b+h/2,w,.07,h,lf,a);facade_box(m,x,y,u,.17,b+h*.75,w-.36,.02,h*.3,GL123,a)
  facade_box(m,x,y,u,.17,b+h*.30,w-.32,.03,h*.32,lf,a)
 surround36(m,x,y,u,b,w,h,a,fr,.12,.38)
def steps123(m,x,y,u,w,top,a,ma,o=.36,tread=.32):
 n=max(1,round((top-G123)/.17))
 for k in range(n):facade_box(m,x,y,u,o+tread*(n-k)/2,G123+(k+.5)*(top-G123)/n,w,tread*(n-k),(top-G123)/n,ma,a)
def canopy123(m,x,y,u,z,w,reach,a,ma,fascia):
 # A flat entrance canopy on two brackets.
 facade_box(m,x,y,u,.36+reach/2,z,w,reach,.12,ma,a);facade_box(m,x,y,u,.36+reach,z-.04,w+.04,.06,.24,fascia,a)
 for s in (-1,1):town_rod(m,lp(x,y,u+s*(w/2-.15),.40,z-.8,a),lp(x,y,u+s*(w/2-.15),.36+reach-.1,z-.05,a),.03,M123['Iron'],6)
def scallops123(m,p,q,z,out,ma,step=.17):
 # A row of small rounded tabs under an eave or verge from p to q (3-D points), 'out' outwards.
 L=math.dist(p,q);n=max(1,int(L/step))
 ang=math.atan2(q[1]-p[1],q[0]-p[0])
 for k in range(n):
  t=(k+.5)/n;X=p[0]+(q[0]-p[0])*t+out[0];Y=p[1]+(q[1]-p[1])*t+out[1];Z=p[2]+(q[2]-p[2])*t
  m.box((X,Y,Z-.07),(.11,.04,.12),ma,ang)
def gable123(m,p,q,c,zb,zt,ma,o0=.005,o1=.355,n=None):
 # A gable triangle p-q-apex c standing on the wall line, from o0 to o1 outwards along n.
 o=lambda v,k:(v[0]+n[0]*k,v[1]+n[1]*k)
 m.faces([(*o(p,o0),zb),(*o(q,o0),zb),(*o(c,o0),zt),(*o(p,o1),zb),(*o(q,o1),zb),(*o(c,o1),zt)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],ma)
def saddle123(m,r,H,T,ma,wall,ov=.40,verge=.35):
 # Saddle roof over rectangle r (ridge along r[0]->r[1]); gable triangles in the wall material.
 p0,p1,p2,p3=r;mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 e0,e1=mid(p0,p3),mid(p1,p2);half=math.dist(p0,p3)/2;sl=(T-H)/half
 ex=lambda p,q,k:(p[0]+(p[0]-q[0])/math.dist(p,q)*k,p[1]+(p[1]-q[1])/math.dist(p,q)*k)
 L=math.dist(p0,p1);dx,dy=(p1[0]-p0[0])/L,(p1[1]-p0[1])/L;sh=lambda p,s:(p[0]+dx*s,p[1]+dy*s)
 q0,q1,q2,q3=sh(ex(p0,p3,ov),-verge),sh(ex(p1,p2,ov),verge),sh(ex(p2,p1,ov),verge),sh(ex(p3,p0,ov),-verge);f0,f1=sh(e0,-verge),sh(e1,verge)
 for quad,zs in (([q0,q1,f1,f0],[H-ov*sl,H-ov*sl,T,T]),([f1,q2,q3,f0],[T,H-ov*sl,H-ov*sl,T])):
  m.faces([(*v,z) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
  m.faces([(*v,z-.12) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
 ends=((p0,p3,e0,(-dx,-dy)),(p1,p2,e1,(dx,dy)))
 for a_,b_,c_,n_ in ends:gable123(m,a_,b_,c_,H,T,wall,n=n_)
 return (q0,q1,q2,q3),sl,ends
def cross_gable123(m,p,q,H,A,back,wall,roof,verge_ma,ov=.40):
 # A cross gable on the wall p-q (outer face to the right of p->q): the gable triangle from H to the
 # apex A, and a saddle roof running 'back' metres into the building to meet the main roof.
 x,y,L,a=sf_edge(p,q);n=(math.sin(a),-math.cos(a));c=((p[0]+q[0])/2,(p[1]+q[1])/2);sl=(A-H)/(L/2)
 gable123(m,p,q,c,H,A,wall,n=n)
 e=L/2+.30
 for s in (-1,1):
  quad=[lp(x,y,s*e,ov,A+.12-e*sl,a),lp(x,y,0,ov,A+.12,a),lp(x,y,0,-back,A+.12,a),lp(x,y,s*e,-back,A+.12-e*sl,a)]
  m.faces(quad,[(0,1,2,3),(3,2,1,0)],roof);m.faces([(v[0],v[1],v[2]-.12) for v in quad],[(0,1,2,3),(3,2,1,0)],roof)
  town_path(m,[lp(x,y,s*e,ov+.02,A+.02-e*sl,a),lp(x,y,0,ov+.02,A+.02,a)],.07,verge_ma)
 return x,y,L,a,sl
def flatroof123(m,zone,H,T,ma,trim,poly=None):
 for g in ([poly] if poly else Z123[zone]['polygons']):
  g=ccw123(clean123(g,.1))
  m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
  for p,q in zip(g,g[1:]+g[:1]):
   L=math.dist(p,q)
   if L<.2:continue
   x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.18,(H+T)/2+.05,L+.36,.40,T-H+.1,trim,a)
def chimney123(m,X,Y,z0,z1,ma,ang=0,w=.6,d=.6):
 m.box((X,Y,(z0+z1)/2),(w,d,z1-z0),ma,ang);m.box((X,Y,z1+.05),(w+.12,d+.12,.10),M123['Stone'],ang)
def railing123(m,pts,z0,h,ma,post=1.2,r=.025):
 for p,q in zip(pts,pts[1:]):
  town_rod(m,(*p,z0+h),(*q,z0+h),r*1.4,ma,6);town_rod(m,(*p,z0+.12),(*q,z0+.12),r,ma,6)
  n=max(1,int(math.dist(p,q)/post))
  for k in range(n+1):
   t=k/n;X,Y=p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t;town_rod(m,(X,Y,z0),(X,Y,z0+h),r,ma,6)

# Generic facades: per wall, windows in bays (rows: bottom, height, width above the ground), doors,
# plinth, cornice, corner boards or pilaster strips. Walls are the zone's own (kind 'outer' from the
# ground, 'upper' above a lower neighbour).
DOORS123={}
def facade123(m,zone,st,walls=None):
 z=Z123[zone];H=zabs123(z['height']);wm=M123[st['wall']]
 for w in (walls or z['walls']):
  x,y,L,a=sf_edge(w['p'],w['q']);z0=0.0 if w['z0']<=0 else zabs123(w['z0'])
  if L<.25:continue
  mine=[]
  if w['kind']=='outer':
   for X,Y,dw,dh,db,kind in DOORS123.get(zone,[]):
    u=U(w,X,Y);off=abs((X-x)*math.sin(a)-(Y-y)*math.cos(a))
    if off<.8 and abs(u)+dw/2<=L/2+.05:mine.append((kind,u,zabs123(db),dw,dh))
  holes=[(u,b,dw,dh,0) for kind,u,b,dw,dh in mine];wins=[]
  bay=st.get('bay',3.0);n=int(L/bay+.35)
  for k in range(n):
   u=-L/2+(k+.5)*L/n
   for row in st.get('rows',[]):
    b,hh,ww=zabs123(row[0]),row[1],row[2]
    if b<z0+.3 or b+hh>H-.25:continue
    if any(abs(u-du)<(ww+dw)/2+.35 and b<db+dh+.2 for _,du,db,dw,dh in mine):continue
    if L<ww+1.0:continue
    wins.append((u,b,ww,hh))
  holes+=[(u,b,ww,hh,0) for u,b,ww,hh in wins]
  bz_wall(m,w['p'],w['q'],z0,H,holes,wm)
  if st.get('boards'):boards81(m,x,y,L,a,max(z0,G123+st.get('plinth',.3)+.02),H-.1,holes,wm,.21)
  for u,b,ww,hh in wins:window123(m,x,y,u,b,ww,hh,a,st.get('frame','Frame'),st.get('surround'),st.get('sill','Frame'),None,st.get('cross',False))
  for kind,u,b,dw,dh in mine:
   door123(m,x,y,u,b,dw,dh,a,st.get('door','Door'),st.get('frame','Frame'),kind=='glass')
   if b>G123+.15:steps123(m,x,y,u,dw+.6,b,a,M123['Step'])
  if w['kind']=='outer' and st.get('plinth'):facade_box(m,x,y,0,.40,(G123+st['plinth'])/2,L+.02,.10,st['plinth'],M123[st.get('plinth_ma','Stone')],a)
  if st.get('cornice'):facade_box(m,x,y,0,.44,H-.12,L+.12,.18,.24,M123[st['cornice']],a)
  if st.get('corners'):
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+max(z0,G123+st.get('plinth',0)))/2,.20,.10,H-max(z0,G123+st.get('plinth',0)),M123[st['corners']],a)
  if st.get('pilasters') and L>3:
   zb=max(z0,G123+st.get('plinth',0));us=[-L/2+.22,L/2-.22]
   if len(wins)>3:us+=[(wins[i][0]+wins[i+1][0])/2 for i in range(1,len(wins)-1,2)]
   for uu in us:facade_box(m,x,y,uu,.40,(H-.25+zb)/2,.45,.09,H-.25-zb,M123[st['pilasters']],a)

# ================================================================ Slottshotellet (93332243)
m=b123_new('SM_Slott115_93332243','Slottsområdet/Buildings');HF=frame_of123('hm')
hmS0,hmS1,hmT0,hmT1=st123('hm')
ST123H={'hm':dict(wall='Red',rows=[(1.1,1.6,1.15),(4.3,1.6,1.15)],bay=2.8,plinth=.5,surround='Frame',cornice='RoofDark',pilasters='Pilaster'),
 'hr':dict(wall='Red',rows=[(1.1,1.6,1.15),(4.3,1.6,1.15)],bay=2.4,plinth=.5,surround='Frame',cornice='RoofDark',pilasters='Pilaster'),
 'hx':dict(wall='Red',rows=[(1.1,1.6,1.2),(4.3,1.9,1.2)],bay=5.0,plinth=.5,surround='Frame',cornice='RoofDark'),
 'hg':dict(wall='Green',rows=[(1.0,1.35,1.0)],bay=3.2,plinth=.35,boards=True,frame='Ochre',surround='Ochre',sill='Ochre',corners='Ochre',cross=True,door='DoorGreen'),
 'hl':dict(wall='Green',rows=[],plinth=.35,boards=True,corners='Ochre')}
# Doors: the green door on the courtyard face left of the cross gable (with a lantern), the entrance
# in the front risalit (south-east, under a canopy), the green wing's door (pass 115).
GW123=frame_of123('hg')
DOORS123.update({'hm':[(*P123(HF,8.7,hmT1),1.1,2.3,.55,'door')],'hr':[(*P123(HF,19.65,-3.44),1.5,2.5,.55,'door')],
 'hg':[(*P123(GW123,5.0,0),1.0,2.1,.35,'door')]})
for zone in ('hm','hr','hx','hg','hl'):facade123(m,zone,ST123H[zone])
# Main roof: a red tile hip over the range (27.4 x 9.9 m), ridge 12.6.
H=zabs123(Z123['hm']['height']);T=zabs123(Z123['hm']['top'])
r=rect123(HF,hmS0,hmS1,0,hmT1);Ls,Lt=hmS1-hmS0,hmT1
inset_roof(m,r,H,Lt/2-.30,T-H,M123['Tile'],.40);slope_hm=(T-H)/(Lt/2-.30)
# Front risalit: walls to the eaves, its cross gable towards Slottsvägen with an attic window.
s0,s1,t0,t1=st123('hr');A=zabs123(Z123['hr']['top'])
x,y,L,a,sl=cross_gable123(m,P123(HF,s0,t0),P123(HF,s1,t0),H,A,-t0+(A-H)/slope_hm+.3,M123['Red'],M123['Tile'],M123['RoofDark'])
window123(m,x,y,0,H+.35,1.0,1.25,a,'Frame','Frame')
canopy123(m,x,y,U({'p':P123(HF,s0,t0),'q':P123(HF,s1,t0)},*P123(HF,19.65,-3.44)),zabs123(3.25),2.4,1.3,a,M123['RoofDark'],M123['Frame'])
# Courtyard cross gable: projects 2.3 m; two storeys and the gable storey with the attic window.
s0,s1,t0,t1=st123('hx');s0=max(s0,2.04);A=zabs123(Z123['hx']['top'])
x,y,L,a,sl=cross_gable123(m,P123(HF,s1,t1),P123(HF,s0,t1),H,A,(t1-hmT1)+(A-H)/slope_hm+.3,M123['Red'],M123['Tile'],M123['RoofDark'])
window123(m,x,y,0,H+.30,.95,1.15,a,'Frame','Frame')
window123(m,x,y,-1.75,zabs123(2.75),.45,.95,a,'Frame','Frame',rows=2)  # the narrow stair window
for s in (-1,1):facade_box(m,x,y,s*(L/2-.22),.40,(H-.25+G123+.5)/2,.45,.09,H-.25-G123-.5,M123['Pilaster'],a)
# Dormers on the courtyard slope: the wide triple one over the porch, a single one by the gable.
bx,by_,bL,ba=sf_edge(P123(HF,hmS1,hmT1),P123(HF,hmS0,hmT1))
for s_,ww in ((20.6,2.7),(10.3,1.45)):
 u=bL/2-(s_-hmS0);dormer82(m,bx,by_,u,ba,H,slope_hm,ww,1.0,M123['Dormer'],M123['Frame'],M123['RoofDark'],.9)
chimney123(m,*P123(HF,13.2,hmT1/2+.6),T-1.0,T+1.0,M123['Red'],ba)
chimney123(m,*P123(HF,24.0,hmT1/2-.6),T-1.6,T+.6,M123['Red'],ba)
# The lantern by the courtyard door.
lx,ly,_,la=sf_edge(P123(HF,hmS1,hmT1),P123(HF,hmS0,hmT1));lu=bL/2-(9.75-hmS0)
facade_box(m,lx,ly,lu,.55,zabs123(2.55),.22,.22,.34,M123['Iron'],la);facade_box(m,lx,ly,lu,.55,zabs123(2.55),.16,.24,.26,GL123,la)
# The polygonal glazed porch: white posts and parapet, glazing, a fascia, the roof terrace with its
# dark timber railing; the porch door on its north-west face under an awning.
z=Z123['hp'];HP=zabs123(z['height']);g=ccw123(clean123(z['polygons'][0],.1))
cen=(sum(v[0] for v in g)/len(g),sum(v[1] for v in g)/len(g));terr=[]
for w in z['walls']:
 if w['kind']!='outer':continue
 x,y,L,a=outface123(w['p'],w['q'],cen)
 facade_box(m,x,y,0,.18,(G123+G123+.75)/2,L,.30,.75,M123['White'],a)
 facade_box(m,x,y,0,.12,(G123+.75+HP-.45)/2,L,.03,HP-.45-G123-.75,GL123,a)
 facade_box(m,x,y,0,.18,HP-.22,L+.1,.32,.45,M123['White'],a)
 for s in (-1,1):facade_box(m,x,y,s*(L/2-.12),.20,(G123+HP)/2,.26,.30,HP-G123,M123['White'],a)
 for k in range(1,max(1,round(L/1.0))):facade_box(m,x,y,-L/2+k*L/max(1,round(L/1.0)),.15,(G123+.75+HP-.45)/2,.06,.07,HP-.45-G123-.75,M123['Frame'],a)
 facade_box(m,x,y,0,.15,G123+.75+1.45,L,.06,.06,M123['Frame'],a)
m.faces([(*v,HP+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M123['RoofDark'])
# railing on the outer edges only (not along the main range)
for w in z['walls']:
 if w['kind']!='outer':continue
 railing123(m,[tuple(w['p']),tuple(w['q'])],HP+.02,1.0,M123['Timber'],.9,.03)
# the porch door: on the face looking straight into the courtyard (OSM vertices 4-5)
pw=min((w for w in z['walls'] if w['kind']=='outer'),key=lambda w:math.dist(((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2),(-744.92,66.43)))
x,y,L,a=outface123(pw['p'],pw['q'],cen);facade_box(m,x,y,0,.10,G123+.75/2,1.1,.32,.76,GL123,a)
door123(m,x,y,0,G123+.05,1.0,2.3,a,'Door','Frame',True);awning82(m,x,y,0,HP-.5,2.2,a,M123['Red'],.45,.9)
# The green wing: saddle (ridge along its south-east side), black roof, ochre bargeboards with
# carved drops, scalloped eaves, attic windows in both gables.
z=Z123['hg'];H=zabs123(z['height']);T=zabs123(z['top']);s0,s1,t0,t1=st123('hg')
r=rect123(GW123,max(s0,-0.2),min(s1,9.9),max(t0,-0.2),min(t1,8.9))
eav,sl,ends=saddle123(m,r,H,T,M123['RoofBlack'],M123['Green'])
for p,q,c,n in ends:
 o=lambda v,k:(v[0]+n[0]*k,v[1]+n[1]*k)
 for u_ in (p,q):
  e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.35,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.35)
  town_rod(m,(*o(e,.62),H-.35*sl-.05),(*o(c,.62),T-.05),.09,M123['Ochre'],8)
  for k in range(1,9):
   t=k/9;px,py=e[0]+(c[0]-e[0])*t,e[1]+(c[1]-e[1])*t;zz=H-.35*sl+(T-H+.35*sl)*t
   m.box((*o((px,py),.62),zz-.22),(.06,.05,.24),M123['Ochre'],math.atan2(c[1]-e[1],c[0]-e[0]))
 x,y,L,a=outface123(p,q,c if False else ((r[0][0]+r[2][0])/2,(r[0][1]+r[2][1])/2))
 window123(m,x,y,0,H+.45,.85,1.15,a,'Ochre','Ochre','Ochre',None,True)
q0,q1,q2,q3=eav;zE=H-.40*sl
for p_,q_,ref in ((q0,q1,q3),(q2,q3,q1)):
 d=(p_[0]-ref[0],p_[1]-ref[1]);dl=math.hypot(*d);out=(d[0]/dl*.03,d[1]/dl*.03)
 town_rod(m,(*p_,zE-.02),(*q_,zE-.02),.07,M123['Ochre'],6);scallops123(m,(*p_,zE-.08),(*q_,zE-.08),0,out,M123['Ochre'])
# The low link: flat black roof with an ochre scalloped fascia.
z=Z123['hl'];flatroof123(m,'hl',zabs123(z['height']),zabs123(z['height'])+.3,M123['RoofBlack'],M123['Ochre'])
b123_finish(m,'93332243')

# ================================================================ Kalmar konstmuseum (91931339)
m=b123_new('SM_Slott115_91931339','Slottsområdet/Buildings');MF=frame_of123('mt');MC=P123(MF,8.7,11.5)
def ribs123(m,p,q,z0,z1,glazed=()):
 # Shingle courses on a black wall p-q: a lip every 0.77 m and staggered joints (about 0.9 m).
 x,y,L,a=outface123(p,q,MC)
 if L<.5 or z1-z0<.3:return
 nz=max(1,round((z1-z0)/.77));hz=(z1-z0)/nz;nu=max(1,round(L/.9));wu=L/nu
 for k in range(nz+1):
  zz=z0+k*hz
  if any(g0<=zz<=g1 for g0,g1 in glazed):continue
  facade_box(m,x,y,0,.38,zz,L+.04,.06,.05,M123['BlackRib'],a)
 for k in range(nz):
  zm=z0+(k+.5)*hz
  if any(g0<=zm<=g1 for g0,g1 in glazed):continue
  for j in range(nu+(k%2)):
   uu=-L/2+(j+(.5 if k%2 else 1))*wu
   if abs(uu)>=L/2-.05:continue
   facade_box(m,x,y,uu,.37,zm,.04,.04,hz-.06,M123['BlackRib'],a)
for zone in ('ml','mt','mc'):
 z=Z123[zone];H=zabs123(z['height'])
 for w in z['walls']:
  z0=G123 if w['z0']<=0 else zabs123(w['z0']);x,y,L,a=outface123(w['p'],w['q'],MC)
  if L<.25:continue
  slot=zone=='mt' and w['kind']=='outer' and 1.2<L<1.6   # the tall glazed slot beside the front block
  entr=zone=='ml' and w['kind']=='outer'                 # the glazed ends of the entrance link
  if slot:
   bz_wall(m,w['p'],w['q'],zabs123(15.2),H,[],M123['Black'])
   facade_box(m,x,y,0,.25,(G123+zabs123(15.2))/2,L,.03,zabs123(15.2)-G123,GL123,a)
   for k in range(1,15):facade_box(m,x,y,0,.30,G123+k*15.2/15,L,.08,.06,M123['FrameDark'],a)
   facade_box(m,x,y,0,.30,(G123+zabs123(15.2))/2,.07,.08,15.2,M123['FrameDark'],a);ribs123(m,w['p'],w['q'],zabs123(15.2),H);continue
  if entr:
   bz_wall(m,w['p'],w['q'],zabs123(3.6),H,[],M123['Black'])
   facade_box(m,x,y,0,.30,(zabs123(.6)+zabs123(3.6))/2,L-.1,.02,3.0,GL123,a)
   nm=max(1,int(L/1.3))
   for k in range(nm+1):facade_box(m,x,y,-L/2+.05+k*(L-.1)/nm,.34,(zabs123(.6)+zabs123(3.6))/2,.07,.10,3.0,M123['FrameDark'],a)
   facade_box(m,x,y,0,.42,zabs123(4.05),L+.05,.12,.75,M123['Sign'],a)
   bz_wall(m,w['p'],w['q'],G123,zabs123(.6),[],M123['Black']);continue
  bz_wall(m,w['p'],w['q'],z0,H,[],M123['Black']);ribs123(m,w['p'],w['q'],z0,H-.1)
 flatroof123(m,zone,H,H+.25,M123['Black'],M123['Black'])
# The entrance landing and steps in front of the north-west glazed end of the link (towards the park
# path), as pass 115, widened along Byttan's front.
ew=[w for w in Z123['ml']['walls'] if w['kind']=='outer'];ent=max(ew,key=lambda w:-math.dist(w['p'],P123(MF,-2,24)))
x,y,L,a=outface123(ent['p'],ent['q'],MC);sh_=1.7 if uof123(x,y,a,*P123(MF,-6,20.8))>0 else -1.7
facade_box(m,x,y,sh_,1.8,G123+.3,L+3.4,3.0,.6,M123['Step'],a)
for k in range(3):facade_box(m,x,y,sh_,3.3+.32*(2-k)+.16,G123+(k+1)*.1,L+3.4,.32,(k+1)*.2,M123['Step'],a)
# The front block: cantilevered from the tower over a recess, its soffit slanting from 6.0 m by the
# tower to 8.0 m at its north-east end; the recess wall below is black with a glazed band.
z=Z123['mf'];FT=zabs123(z['height']);sf0,sf1=z['soffit']
c0=[P123(MF,6.72,17.33),P123(MF,12.31,17.33),P123(MF,12.31,21.74),P123(MF,6.72,21.74)]
zb=[zabs123(sf0),zabs123(sf1),zabs123(sf1),zabs123(sf0)]
m.faces([(*v,zz) for v,zz in zip(c0,zb)]+[(*v,FT) for v in c0],[(3,2,1,0),(4,5,6,7),(1,2,6,5),(2,3,7,6),(0,1,5,4),(3,0,4,7)],M123['Black'])
for (p,q),(za,zb_) in (((c0[1],c0[2]),(zabs123(sf1),zabs123(sf1))),((c0[2],c0[3]),(zabs123(sf0),zabs123(sf1)))):ribs123(m,p,q,max(za,zb_)+.1,FT-.1)
bz_wall(m,P123(MF,12.31,17.33),P123(MF,6.72,17.33),G123,zabs123(sf0)+.2,[],M123['Black'])
bz_wall(m,P123(MF,6.72,17.33),P123(MF,6.72,21.74),G123,zabs123(sf0)+.1,[],M123['Black'])
x,y,L,a=outface123(P123(MF,12.31,17.33),P123(MF,6.72,17.33),MC)
facade_box(m,x,y,0,.30,zabs123(1.9),L-.6,.03,3.2,GL123,a);surround36(m,x,y,0,zabs123(.3),L-.6,3.2,a,M123['FrameDark'],.10,.40)
m.faces([(*v,FT+.02) for v in c0],[(0,1,2,3),(3,2,1,0)],M123['Black'])
for p,q in zip(c0,c0[1:]+c0[:1]):
 x,y,L,a=outface123(p,q,MC);facade_box(m,x,y,0,.18,FT+.15,L+.36,.40,.35,M123['Black'],a)
# Large windows: one high on the park (north-east) face of the core, one on the south-east face.
for (sa,ta,sb,tb),zc,ww,hh in (((17.41,0,17.42,17.33),zabs123(10.5),4.2,3.4),((6.72,0,17.41,0),zabs123(6.0),3.0,2.6)):
 p,q=P123(MF,sa,ta),P123(MF,sb,tb);x,y,L,a=outface123(p,q,MC)
 facade_box(m,x,y,0,.36,zc,ww,.03,hh,GL123,a);surround36(m,x,y,0,zc-hh/2,ww,hh,a,M123['FrameDark'],.10,.40)
b123_finish(m,'91931339')

# ================================================================ Byttan (91222116)
m=b123_new('SM_Slott115_91222116','Slottsområdet/Buildings');BF=frame_of123('by')
DOORS123['by']=[(*P123(BF,4.6,0),1.6,2.4,.45,'glass')]
facade123(m,'by',dict(wall='White',rows=[(1.0,1.3,1.3)],bay=3.0,plinth=.45,frame='FrameDark',sill='Frame',cornice='White'))
z=Z123['by'];H=zabs123(z['height']);g=ccw123(clean123(z['polygons'][0]))
inset_roof(m,g,H,3.0,zabs123(z['top'])-H,M123['RoofDark'],.95)
up=z['upper'];ug=rect123(BF,up['s0'],up['s1'],up['t0'],up['t1']);ug=ccw123(ug);UH=zabs123(up['height']);UB=zabs123(z['top'])-.3
for p,q in zip(ug,ug[1:]+ug[:1]):
 x,y,L,a=sf_edge(p,q);n=max(1,int(L/1.6));holes=[(-L/2+(k+.5)*L/n,UB+1.05,1.2,1.0,0) for k in range(n)]
 bz_wall(m,p,q,UB,UH,holes,M123['White'])
 for u,b,ww,hh,_ in holes:cas81(m,x,y,u,b,ww,hh,a,M123['FrameDark'],.16,2)
 facade_box(m,x,y,0,.44,UH-.12,L+.12,.18,.24,M123['White'],a)
inset_roof(m,ug,UH,2.4,zabs123(up['top'])-UH,M123['RoofDark'],.6)
chimney123(m,*P123(BF,up['s0']+.6,up['t0']+3.0),UH-.3,UH+1.2,M123['White'],math.atan2(BF[1][1]-BF[0][1],BF[1][0]-BF[0][0]))
# The terrace along the park front (north-west), with an iron railing; open towards the museum steps.
x,y,L,a=outface123(P123(BF,0,0),P123(BF,18.2,0),P123(BF,9,10))
tu0,tu1=uof123(x,y,a,*P123(BF,6.0,0)),uof123(x,y,a,*P123(BF,17.4,0))
facade_box(m,x,y,(tu0+tu1)/2,1.55,G123+.25,abs(tu1-tu0),2.4,.5,M123['Stone'],a)
railing123(m,[lp(x,y,tu0,2.70,0,a)[:2],lp(x,y,tu1,2.70,0,a)[:2]],G123+.5,1.0,M123['Iron'],1.0,.022)
b123_finish(m,'91222116')

# ================================================================ the grey boarded pavilion (874870421)
m=b123_new('SM_Slott115_874870421','Slottsområdet/Buildings');PF=frame_of123('pv')
PV={'pv':dict(wall='GreyBoard',rows=[],plinth=.3,boards=True,corners='Frame'),'pn':dict(wall='GreyBoard',rows=[(1.0,1.2,1.0)],bay=3.0,plinth=.3,boards=True,corners='Frame')}
DOORS123['pn']=[(*P123(PF,4.62+(-2.01-4.62)*.5,12.7+(4.15-12.7)*.5),1.0,2.0,.30,'door')]
facade123(m,'pn',PV['pn'])
z=Z123['pv'];H=zabs123(z['height']);T=zabs123(z['top']);s0,s1,t0,t1=st123('pv');s0=max(s0,0.0)
for w in z['walls']:
 x,y,L,a=outface123(w['p'],w['q'],P123(PF,5,2.8));z0=G123 if w['z0']<=0 else zabs123(w['z0'])
 if L<.25:continue
 # glazing: the whole east end and the east half of the south side
 sm=[(v[0]-PF[0][0])*(PF[1][0]-PF[0][0])/10.53+(v[1]-PF[0][1])*(PF[1][1]-PF[0][1])/10.53 for v in (w['p'],w['q'])]
 east=min(sm)>9.5;south=w['kind']=='outer' and L>9
 if east or south:
  gu0,gu1=(-L/2,L/2) if east else sorted((uof123(x,y,a,*P123(PF,5.2,0)),uof123(x,y,a,*P123(PF,10.4,0))))
  zg0,zg1=G123+.8,H-.25;holes=[((gu0+gu1)/2,zg0,gu1-gu0-.3,zg1-zg0,0)]
  bz_wall(m,w['p'],w['q'],z0,H,holes,M123['GreyBoard']);boards81(m,x,y,L,a,G123+.32,H-.1,holes,M123['GreyBoard'],.21)
  facade_box(m,x,y,(gu0+gu1)/2,.14,(zg0+zg1)/2,gu1-gu0-.3,.02,zg1-zg0,GL123,a)
  nm=max(1,round((gu1-gu0)/.8))
  for k in range(nm+1):facade_box(m,x,y,gu0+.15+k*(gu1-gu0-.3)/nm,.20,(zg0+zg1)/2,.07,.08,zg1-zg0,M123['Frame'],a)
  for zz in (zg0,zg0+1.1,zg1):facade_box(m,x,y,(gu0+gu1)/2,.20,zz,gu1-gu0-.3,.08,.07,M123['Frame'],a)
  if south:
   window123(m,x,y,uof123(x,y,a,*P123(PF,2.6,0)),G123+1.0,1.0,1.2,a,'Frame')
 else:
  bz_wall(m,w['p'],w['q'],z0,H,[],M123['GreyBoard']);boards81(m,x,y,L,a,max(z0,G123+.32),H-.1,[],M123['GreyBoard'],.21)
 if w['kind']=='outer':facade_box(m,x,y,0,.40,(G123+.3)/2,L+.02,.10,.3,M123['Stone'],a)
 for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+max(z0,G123))/2,.18,.08,H-max(z0,G123),M123['Frame'],a)
r=rect123(PF,s0,10.53,0,5.59);eav,sl,ends=saddle123(m,r,H,T,M123['RoofDark'],M123['GreyBoard'],.45,.30)
for p,q,c,n in ends:
 o=lambda v,k:(v[0]+n[0]*k,v[1]+n[1]*k)
 for u_ in (p,q):
  e=(u_[0]+(u_[0]-c[0])/math.dist(u_,c)*.45,u_[1]+(u_[1]-c[1])/math.dist(u_,c)*.45)
  town_rod(m,(*o(e,.48),H-.45*sl-.03),(*o(c,.48),T-.03),.07,M123['Frame'],8)
q0,q1,q2,q3=eav
for p_,q_ in ((q0,q1),(q2,q3)):town_rod(m,(*p_,H-.45*sl-.06),(*q_,H-.45*sl-.06),.06,M123['Frame'],6)
z=Z123['pn'];flatroof123(m,'pn',zabs123(z['height']),zabs123(z['height'])+.35,M123['RoofDark'],M123['Frame'])
b123_finish(m,'874870421')

# ================================================================ the park building 91222187
# No photo shows it: the open shelter in park_pav_b stands 25-40 degrees away from its bearing (see the
# notes). Pass 115's plain form is kept: a cream rendered pavilion under a red tile hip, one door.
m=b123_new('SM_Slott115_91222187','Slottsområdet/Buildings');SF=frame_of123('sh')
DOORS123['sh']=[(-853.0,-87.8,1.0,2.1,.3,'door')]
facade123(m,'sh',dict(wall='Cream',rows=[(1.0,1.3,1.0)],bay=3.0,plinth=.35,frame='Frame',surround='Frame',cornice='Frame'))
z=Z123['sh'];H=zabs123(z['height']);s0,s1,t0,t1=st123('sh');r=rect123(SF,s0,s1,t0,t1)
inset_roof(m,r,H,min(s1-s0,t1-t0)/2-.30,z['top']-z['height'],M123['Tile'],.45)
b123_finish(m,'91222187')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block123_cameras=[
 sv_camera('661_Block123_Cal_HotelCourtyard',-760.5,55.0,1.7,64,15),
 sv_camera('662_Block123_Cal_HotelGate',-760.5,55.0,1.7,181,15),
 sv_camera('663_Block123_Cal_Konstmuseum',-713.7,-39.7,1.7,100,15),
 sv_camera('664_Block123_Cal_ParkPavilion',-754.9,-103.8,1.6,318,8),
 ('665_Block123_Aerial',(-640.0,-150.0,90.0),(-760.0,-20.0,2.0),24)]
print('BLOCK123_GEOMETRY',len(block123_names))
