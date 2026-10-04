"""Pass 91: the east end of Storgatan, five district volumes:
- north side, west to east: the red boarded house with its gable to the street (black bargeboards,
  a black corner board), the grey double door under the east half of the gable; the green boarded gable house with
  two windows below and one above; the red door in the yellow boarded gateway with its tiled
  lean-to; the yellow boarded gable house with two windows below and one in the gable;
- south side: the cream stucco shop with the stepped gable (five steps a side, grey copings, a
  finial), corner pilasters, the portal round the big shop window, a glass door and a second window;
  Storgatan 65, the grey boarded two-storey house on a dark plinth, three windows a floor, white
  corner boards, a dark tiled saddle roof and two windows in its west gable.
93192417 (west of the red house) is not in any photograph and keeps its pass-17 volume.

References: Google Street View April 2025 (three panoramas on Storgatan, resected on house
corners), view only. Zones: source/block91.json; see references/block91-notes.md. Signs, house
numbers, lamps, pipes, the plants and the cars are omitted.
"""
B91D=json.loads((R/'source/block91.json').read_text());Z=B91D['zones']
block91_names=[];B91={}
for old in [k for k in list(materials) if k.startswith('M_Block91_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownIvory',(.55,.17,.13),.82,0),('Green','TownIvory',(.60,.66,.55),.82,0),('Yellow','TownIvory',(.90,.75,.44),.82,0),
 ('Grey','TownIvory',(.60,.60,.57),.82,0),('Stucco','TownIvory',(.86,.80,.63),.90,0),('Pilaster','TownIvory',(.80,.72,.54),.90,0),
 ('Trim','TownPaintWhite',(.93,.93,.90),.55,0),('Black','TownPaintBrown',(.12,.11,.10),.60,0),('GreyDoor','TownPaintGreen',(.47,.51,.47),.60,0),
 ('RedDoor','TownPaintBrown',(.68,.12,.11),.55,0),('Sash','TownPaintWhite',(.32,.40,.53),.55,0),
 ('Plinth','TownStone',(.55,.55,.53),.90,0),('PlinthDark','TownStone',(.34,.35,.36),.90,0),('Coping','TownStone',(.30,.30,.31),.90,0),
 ('Tile','TownTileRed',(.72,.38,.25),.80,0),('TileDark','TownTileRed',(.36,.27,.22),.80,0),
 ('Dark','TownMetalGrey',(.06,.06,.065),.40,.20),('Bronze','TownMetalGrey',(.24,.22,.19),.45,.30),
 ]:
 name='M_Block91_'+key;B91[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block91_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B91;TR=M['Trim']

def b91_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block91_names.append(name);return Mesh(name,category)
def drop_degenerate_faces91(obj,tol=1e-9):
 # The FBX export (tangent frames) fails on zero-area faces and faces with a repeated corner.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b91_finish(m,osm):
 obj=s21_finish(m);n=drop_degenerate_faces91(obj)
 if n:print('BLOCK91_DROPPED_DEGENERATE',m.name,n)
 obj['detail_pass']=91;obj['reference_notes']='references/block91-notes.md';obj['osm_way']=osm;return obj
def P91(a,b,s):L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def gable91(m,w,H,T,ma):
 # A solid gable triangle on a wall, flush with the wall's thickness (offsets 0.005-0.355).
 x,y,L,a=sf_edge(w['p'],w['q']);prof=[(-L/2,H),(L/2,H),(0,T)];vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def win91(m,x,y,u,b,w,h,a,frame,sash=None,face=False):
 # A casement with a plain surround and sill; face=True sets it on the wall face (gable windows,
 # where the wall behind is the solid gable).
 o=.40 if face else .16
 cas81(m,x,y,u,b,w,h,a,sash or frame,o,3 if h>1.2 else 2)
 surround36(m,x,y,u,b,w,h,a,frame,.10,.42 if face else .40);facade_box(m,x,y,u,.47,b-.05,w+.26,.16,.06,frame,a)
def barge91(m,w,H,T,ma,ov=.30):
 x,y,L,a=sf_edge(w['p'],w['q']);sl=(T-H)/(L/2)
 for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+ov),.62,H-ov*sl-.05,a),lp(x,y,0,.62,T+.02,a)],.08,ma)
def front91(m,p,q,H,ops,wm,boarded=True,plinth=.30,pm=None):
 # A street front p->q: the wall with its openings cut, boards, and the openings drawn whose
 # centre lies on this wall (an opening may span two walls). ops: (kind, X, bottom, w, h, extra).
 x,y,L,a=sf_edge(p,q);w={'p':list(p),'q':list(q)};mine=[];holes=[]
 for k,X,b,ww,hh,ex in ops:
  u=U(w,X,p[1]+(q[1]-p[1])*(X-p[0])/(q[0]-p[0]))
  if abs(u)-ww/2<L/2-.01:
   if b<H:holes.append((u,b,ww,min(hh,H-b),0))
   if abs(u)<=L/2:mine.append((k,u,b,ww,hh,ex))
 bz_wall(m,p,q,0,H,[hh for hh in holes if hh[1]+hh[3]<=H+.01],wm)
 if boarded:boards81(m,x,y,L,a,plinth+.05,H-.12,holes,wm)
 if plinth>0:
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for u,b,ww,hh,r in holes if b<plinth)+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,plinth/2,lo-at,.10,plinth,pm or M['PlinthDark'],a)
   at=max(at,hi)
 return x,y,L,a,mine

# Fronts and openings. North side: fronts face south; X is the model x of an opening's centre on
# the front line. Measured on the 68 Storgatan panorama (camera 269.68,-3.92, resected on the shop
# opposite) and the 63 panorama (279.89,-4.55); the west ground window of the red house estimated.
NORTH=[('win',261.9,1.10,.90,1.10,'rh'),('win',263.6,1.10,.90,1.10,'rh'),('win',263.15,3.00,.85,1.10,'rhg'),
 ('door',265.69,.05,1.25,2.15,'grey'),
 ('win',268.0,1.09,.95,1.02,'gh'),('win',269.6,1.09,.95,1.02,'gh'),('win',268.8,2.95,1.0,1.25,'gh'),
 ('gate',271.75,0,1.57,2.15,'red'),
 ('win',275.1,1.02,1.0,1.13,'yh'),('win',278.15,1.02,1.0,1.13,'yh'),('win',276.65,2.75,1.15,1.35,'yhg')]
NWALL={'rh':'Red','gl':'Red','gh':'Green','gg':'Yellow','yl':'Yellow','yh':'Yellow'}
NCORNER={'gh':'Trim','yh':'Trim'};NGABLE={'rh','gl'}
# South side: fronts face north, east corner -> west corner; s in metres from the east corner.
FSH=((275.19,-11.0),(265.24,-10.79));FGR=((295.35,-11.26),(279.97,-10.73))

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b91_new(nm,'Kvarnholmen/Storgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];T=spec['top']
 if zone in NWALL:
  wm=M[NWALL[zone]]
  for w in walls(zone):
   if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
   ox,oy=outward(w)
   if oy>-.85:
    if spec['roof']=='flat' or math.dist(w['p'],w['q'])<2:bz_wall(m,w['p'],w['q'],0,H,[],wm)
    else:plain(m,w,H,wm,TR,TR,1,.9)
    if spec['roof']!='flat' and oy>.85:gable91(m,w,H,T,wm)
    continue
   x,y,L,a,mine=front91(m,w['p'],w['q'],H,NORTH,wm)
   for k,u,b,ww,hh,ex in mine:
    if k=='win':win91(m,x,y,u,b,ww,hh,a,TR,face=b+hh>H)
    elif k=='door':gate83(m,x,y,u,b,ww,hh,a,M['GreyDoor'],TR);facade_box(m,x,y,u,.42,b+hh+.08,ww+.3,.10,.16,TR,a)
   if zone in NGABLE:pass
   elif zone in NCORNER:
    cm=M[NCORNER[zone]]
    for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,H/2,.18,.10,H,cm,a)
    gable91(m,w,H,T,wm);barge91(m,w,H,T,cm)
   else:
    facade_box(m,x,y,0,.42,H-.06,L+.02,.12,.12,wm,a)
# The gateway: the yellow boarded wall in the 1.5 m gap between the green and the yellow volumes
# (outside the OSM outlines), the red double door under a white beam, white posts, and a tiled
# lean-to from x 270.85 to 273.93; the low red link's lean-to likewise.
m=meshes['SM_Kvarnholmen_House_93192442']
x,y,L,a,_=front91(m,(271.79,0.34),(273.27,0.39),3.2,NORTH,M['Yellow'])
facade_box(m,x,y,0,.42,3.14,L+.02,.12,.12,M['Yellow'],a)
gp=(270.85,0.335);gq=(273.93,0.38);x,y,L,a=sf_edge(gp,gq);u=U({'p':list(gp),'q':list(gq)},271.75,.34)
gate83(m,x,y,u,0,1.57,2.15,a,M['RedDoor'],TR)
facade_box(m,x,y,u,.44,2.23,1.95,.12,.16,TR,a)
for s in (-1,1):facade_box(m,x,y,u+s*.885,.42,1.1,.18,.10,2.2,TR,a)
facade_box(m,x,y,L/2-.09,.42,1.6,.18,.10,3.2,TR,a)
def lean91(m,p,q,z,ma,depth=1.4,rise=.45):
 x,y,L,a=sf_edge(p,q);m.faces([lp(x,y,-L/2,.70,z,a),lp(x,y,L/2,.70,z,a),lp(x,y,L/2,-depth,z+rise,a),lp(x,y,-L/2,-depth,z+rise,a)],[(0,1,2,3),(3,2,1,0)],ma)
lean91(m,gp,gq,3.12,M['Tile'])
for zone in ('gl','gg'):
 for g in Z[zone]['polygons']:m.faces([(*v,Z[zone]['height']+.03) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Dark'])
# The red house: one gable front from x 259.58 to 266.45 over the red volume and the west 0.8 m
# of the green one, the ridge at x 263.0 (apex measured at 263.15); a black corner board at x 264.5
# where the boarding changes, white trim at the green house.
m=meshes['SM_Kvarnholmen_House_93192424']
Z['rhx']=dict(Z['rh'],polygons=Z['rh']['polygons']+Z['gl']['polygons'])
saddle82(m,'rhx',(259.58,0.26),(266.45,0.32),M['Tile'],M['Red'],along=False)
H,T=Z['rh']['height'],Z['rh']['top']
for wf in ({'p':[259.58,0.26],'q':[266.45,0.32]},{'p':[266.45,10.64],'q':[259.47,10.58]}):gable91(m,wf,H,T,M['Red'])
wf={'p':[259.58,0.26],'q':[266.45,0.32]};x,y,L,a=sf_edge(wf['p'],wf['q']);barge91(m,wf,H,T,M['Black'])
for X,cm in ((259.67,'Black'),(264.5,'Black'),(266.36,'Trim')):facade_box(m,x,y,U(wf,X,.3),.42,(H+.6)/2+.1,.18,.10,H+.6 if X==264.5 else H,M[cm],a)
m=meshes['SM_Kvarnholmen_House_93192442'];saddle82(m,'gh',(266.45,0.32),(270.85,0.34),M['Tile'],M['Green'],along=False)
m=meshes['SM_Kvarnholmen_House_93192397'];saddle82(m,'yh',(273.93,0.38),(280.19,0.29),M['Tile'],M['Yellow'],along=False)
for g in Z['yl']['polygons']:m.faces([(*v,Z['yl']['height']+.03) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Dark'])

# The shop (91928597): stucco front to the cornice at 4.5 m, the stepped gable above. Steps (s from
# the east corner, top height) measured on the 68 panorama; the west half mirrors the east half
# about the gable's axis at s 4.915.
m=meshes['SM_Kvarnholmen_House_91928597'];H=Z['sh']['height'];T=Z['sh']['top']
SHOPS=[('door',1.30,.25,.80,2.35),('win',5.065,.65,3.05,2.65),('win',8.25,.65,1.90,1.95)]
for w in walls('sh'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Stucco']);continue
 ox,oy=outward(w)
 if oy<.85:
  plain(m,w,H,M['Stucco'],TR,TR,1,.9)
  if oy<-.85:gable91(m,w,H,T,M['Stucco'])
  continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*P91(*FSH,s))
 holes=[(S(s),b,ww,hh,0) for k,s,b,ww,hh in SHOPS]
 bz_wall(m,w['p'],w['q'],0,H,holes,M['Stucco'])
 for k,s,b,ww,hh in SHOPS:
  u=S(s);facade_box(m,x,y,u,.10,b+hh/2,ww,.02,hh,GLAZE,a)
  for q in (-ww/2+.04,ww/2-.04):facade_box(m,x,y,u+q,.14,b+hh/2,.08,.08,hh,M['Bronze'],a)
  for zz in (b+.04,b+hh-.04):facade_box(m,x,y,u,.14,zz,ww,.08,.08,M['Bronze'],a)
  if k=='win':
   facade_box(m,x,y,u,.14,b+.33,ww,.06,.62,M['Dark'],a)
   facade_box(m,x,y,u,.15,b+hh*.65,ww,.06,.06,M['Bronze'],a)
   if ww>2:facade_box(m,x,y,u,.15,b+hh/2,.07,.06,hh,M['Bronze'],a)
 # Plinth, corner pilasters with caps, the portal round the big window.
 at=-L/2
 for lo,hi in ((S(1.30)-.40,S(1.30)+.40),(L/2,L/2)):
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,.125,lo-at,.10,.25,M['Coping'],a)
  at=max(at,hi)
 for s in (.275,L-.275):
  facade_box(m,x,y,S(s),.45,2.25,.55,.12,4.0,M['Pilaster'],a);facade_box(m,x,y,S(s),.50,4.37,.66,.22,.26,M['Pilaster'],a)
 for s in (3.15,6.95):facade_box(m,x,y,S(s),.45,2.12,.50,.12,3.75,M['Pilaster'],a)
 facade_box(m,x,y,S(5.05),.50,4.20,4.60,.20,.40,M['Pilaster'],a)
 facade_box(m,x,y,S(5.05),.42,5.05,2.40,.10,1.30,M['Pilaster'],a)
 facade_box(m,x,y,S(5.05),.42,6.00,1.00,.10,.60,M['Pilaster'],a)
 facade_box(m,x,y,S(5.05),.45,6.65,.10,.10,.70,M['Black'],a);facade_box(m,x,y,S(5.05),.45,6.75,.40,.10,.08,M['Black'],a)
 for s in (1.60,8.25):
  facade_box(m,x,y,S(s),.40,6.55,.07,.06,.70,M['Black'],a);facade_box(m,x,y,S(s),.40,6.65,.40,.06,.07,M['Black'],a)
 # The stepped gable: one block per step from the cornice up, a grey coping on each, the finial.
 E=[.55,1.25,2.0,2.8,3.56,4.47];TOPS=[5.93,6.72,7.61,8.49,9.38]
 blocks=[(E[i],E[i+1],TOPS[i]) for i in range(5)]+[(4.47,5.36,9.90)]+[(9.83-E[i+1],9.83-E[i],TOPS[i]) for i in range(5)]
 for s0,s1,top in blocks:
  facade_box(m,x,y,S((s0+s1)/2),.18,(H+top)/2,s1-s0+.01,.35,top-H,M['Stucco'],a)
  facade_box(m,x,y,S((s0+s1)/2),.20,top+.07,s1-s0+.06,.46,.16,M['Coping'],a)
 facade_box(m,x,y,S(4.915),.20,10.10,.36,.36,.25,M['Coping'],a);facade_box(m,x,y,S(4.915),.20,10.45,.42,.42,.46,M['Coping'],a)
saddle82(m,'sh',FSH[1],FSH[0],M['Tile'],M['Stucco'],along=False,ov=.12)

# Storgatan 65 (91928575): boarded front with three windows a floor (s from the east corner),
# frieze and eaves, white corner boards, dark plinth; two windows in the west gable.
m=meshes['SM_Kvarnholmen_House_91928575'];H=Z['gr']['height'];T=Z['gr']['top']
for w in walls('gr'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if abs(ox)>.85:
  if ox<0:
   s0=U(w,*P91(w['p'],w['q'],4.3))
   bz_wall(m,w['p'],w['q'],0,H,[(s0,4.35,.90,1.25,0)],M['Grey']);boards81(m,x,y,L,a,.85,H-.12,[(s0,4.35,.90,1.25,0)],M['Grey'])
   win91(m,x,y,s0,4.35,.90,1.25,a,TR,M['Sash']);win91(m,x,y,s0,6.55,.80,1.10,a,TR,M['Sash'],face=True)
   facade_box(m,x,y,0,.40,.40,L,.10,.80,M['PlinthDark'],a)
  else:plain(m,w,H,M['Grey'],TR,TR,2,.9)
  gable91(m,w,H,T,M['Grey']);barge91(m,w,H,T,TR,.35)
  for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.42,H/2,.30,.10,H,TR,a)
  continue
 if oy<.85:plain(m,w,H,M['Grey'],TR,TR,2,.9);continue
 ops=[('win',s,1.60,1.12,1.50) for s in (2.90,8.18,11.95)]+[('win',s,4.50,1.12,1.55) for s in (2.78,8.15,11.94)]
 holes=[(U(w,*P91(*FGR,s)),b,ww,hh,0) for k,s,b,ww,hh in ops]
 bz_wall(m,w['p'],w['q'],0,H,holes,M['Grey']);boards81(m,x,y,L,a,.85,H-.40,holes,M['Grey'])
 for u,b,ww,hh,r in holes:win91(m,x,y,u,b,ww,hh,a,TR,M['Sash'])
 facade_box(m,x,y,0,.40,.40,L,.10,.80,M['PlinthDark'],a);facade_box(m,x,y,0,.43,.84,L,.14,.08,TR,a)
 for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.42,H/2+.4,.30,.10,H-.8,TR,a)
 facade_box(m,x,y,0,.42,H-.22,L+.05,.14,.30,TR,a);facade_box(m,x,y,0,.47,H-.05,L+.12,.24,.10,TR,a)
 town_rod(m,lp(x,y,-L/2,.64,H-.02,a),lp(x,y,L/2,.64,H-.02,a),.06,M['Dark'],8)
saddle82(m,'gr',FGR[1],FGR[0],M['TileDark'],M['Grey'],along=True)
for nm in meshes:b91_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block91_cameras=[
 sv_camera('446_Block91_Cal_North',269.68,-3.92,2.40,332,20,90),
 sv_camera('447_Block91_Cal_Yellow',279.89,-4.55,2.40,2,20,90),
 sv_camera('448_Block91_Cal_Shop',269.68,-3.92,2.40,152,15,90),
 sv_camera('449_Block91_Cal_SixtyFive',289.74,-4.20,2.40,152,15,90),
 ('450_Block91_Aerial',(272.0,-45.0,32.0),(272.0,-8.0,2.0),28),
]
print('BLOCK91_GEOMETRY',len(block91_names))
