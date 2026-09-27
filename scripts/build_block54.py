"""Pass 54: the district volume 91285838 at the east end of Ölandsgatan (south side), a classical
two-storey building:
- a symmetrical front of three parts: wings of three axes, two risalits projecting 0.35 m under
  pediments (each with a round-headed niche over its upper window; the west one holds a door up
  steps, the east one an arched window), and a centre of three axes under a set-back attic with its
  own pediment;
- round-headed ground-floor windows on a granite plinth, a string course, upper casements under
  small cornices, a main cornice and a low hipped sheet roof with two small pedimented dormers;
- the east wing's door, and the one-storey annex with a large and a small arched window and a
  rounded east end.
The Skeppsbrogatan side stays plain.

References: Google Street View April 2025 (three panoramas chained on shared risalit and window
edges, anchored on the west corner and spaced as their GPS positions), view only. Zones:
source/block54.json; see references/block54-notes.md. The signs, the railings, the bicycle stands
and the heat pump are omitted.
"""
B54D=json.loads((R/'source/block54.json').read_text());Z=B54D['zones']
block54_names=[];B54={}
for old in [k for k in list(materials) if k.startswith('M_Block54_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownIvory',(.93,.91,.84),.88,0),
 ('Trim','TownIvory',(.96,.95,.90),.84,0),
 ('Granite','TownStone',(.62,.55,.52),.86,0),
 ('Frame','TownPaintBrown',(.22,.25,.24),.55,0),
 ('Door','TownPaintBrown',(.30,.34,.32),.60,0),
 ('Roof','TownMetalGrey',(.18,.19,.20),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block54_'+key;B54[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block54_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B54;TR=M['Trim'];PL=M['Plaster']

def b54_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block54_names.append(name);return Mesh(name,category)
def b54_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=54;obj['reference_notes']='references/block54-notes.md';obj['osm_way']=osm;return obj
def yf54(X):return -158.649+(X-105.56)*(-160.324+158.649)/(149.226-105.56)
def street54(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-160.5
def cas54(m,x,y,u,b,w,h,a,o=.18,rows=(.66,)):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,M['Frame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['Frame'],a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,M['Frame'],a)
 for t in rows:facade_box(m,x,y,u,o+.01,b+h*t,w,.05,.05,M['Frame'],a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Granite'],a)
def arch54(m,x,y,u,a,spring,half,rise,o,r,ma,n=14):
 pts=[(u-half,spring)]+[(u-half*math.cos(math.pi*k/n),spring+rise*math.sin(math.pi*k/n)) for k in range(1,n)]+[(u+half,spring)]
 town_path(m,[lp(x,y,uu,o,zz,a) for uu,zz in pts],r,ma)
def pediment54(m,x,y,u,a,w,base,apex,o0,o1,ma):
 prof=[(u-w/2,base),(u+w/2,base),(u,apex)]
 vs=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
 for s in (-1,1):town_rod(m,lp(x,y,u+s*(w/2+.1),o1+.05,base-.02,a),lp(x,y,u,o1+.05,apex+.08,a),.09,TR,8)
 facade_box(m,x,y,u,(o0+o1)/2+.04,base-.10,w+.24,o1-o0+.10,.20,TR,a)

m=b54_new('SM_Kvarnholmen_House_91285838','Kvarnholmen/Ölandsgatan south')
H=Z['mn']['height']
GF_B,GF_H,GF_R=1.40,1.52,.48          # round-headed ground windows: sill 1.40, springing 2.92, crown 3.40
UP_B,UP_H=4.95,2.25
for zone in Z:
 HZ=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf54(X))
  if zone=='mn' and street54(w):
   RIS=[(117.33,4.35),(130.07,4.35)]
   wing=[108.0,110.75,113.5,120.95,123.6,126.14,133.3,136.15,138.97]
   gf=[(S(X0),GF_B,1.32,GF_H,GF_R) for X0 in wing if X0!=138.7]
   door_e=(S(138.7),.45,1.30,2.47,.48)
   gf=[g for g in gf if abs(g[0]-door_e[0])>.8]
   up=[(S(X0),UP_B,1.27,UP_H,0) for X0 in wing]
   rg=[(S(130.07),GF_B,1.40,GF_H,GF_R)];rd=[(S(117.33),.45,1.36,2.47,.48)]
   ru=[(S(X0),UP_B,1.34,UP_H,0) for X0,_ in RIS]
   holes=gf+up+rg+rd+ru+[door_e]
   bz_wall(m,w['p'],w['q'],0,HZ,holes,PL)
   for u,b,ww,hh,r in gf+rg:cas54(m,x,y,u,b,ww,hh+r*.7,a,rows=(.55,));arch54(m,x,y,u,a,b+hh,ww/2+.10,r+.08,.40,.07,TR)
   for u,b,ww,hh,r in up+ru:
    surround36(m,x,y,u,b,ww,hh,a,TR,.12,.39);cas54(m,x,y,u,b,ww,hh,a)
    facade_box(m,x,y,u,.46,b+hh+.22,ww+.40,.16,.10,TR,a);facade_box(m,x,y,u,.50,b+hh+.32,ww+.56,.24,.10,TR,a)
   for u,b,ww,hh,r in rd+[door_e]:
    facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['Door'],a)
    for zz in (b+.45,b+1.25):facade_box(m,x,y,u,.14,zz,ww-.24,.02,.6,M['Frame'],a)
    facade_box(m,x,y,u,.12,b+hh+r*.6,ww,.02,r*1.1,GLAZE,a);arch54(m,x,y,u,a,b+hh,ww/2+.12,r+.10,.40,.08,TR)
    steps36(m,x,y,u,a,ww+1.0,ww+.6,b,3,.34,M['Granite'])
   # The plinth, the string course, the main cornice.
   at=-L/2
   for u,ww in sorted([(g[0],g[2]+.1) for g in rd+[door_e]])+[(L/2+2,0)]:
    lo=max(-L/2,min(L/2,u-ww/2))
    if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.24,lo-at,.08,.48,M['Granite'],a)
    at=max(at,min(L/2,u+ww/2))
   facade_box(m,x,y,0,.42,4.30,L,.10,.10,TR,a);facade_box(m,x,y,0,.46,4.52,L,.18,.34,TR,a)
   facade_box(m,x,y,0,.42,8.62,L,.10,.30,TR,a);facade_box(m,x,y,0,.52,8.92,L+.10,.34,.30,TR,a);facade_box(m,x,y,0,.64,9.12,L+.20,.56,.16,TR,a)
   # The risalits: a second wall layer 0.35 m proud with the same openings, pilasters, a niche over
   # the upper window, an entablature and the pediment.
   for X0,ww in RIS:
    u0=S(X0);p0=lp(x,y,u0-ww/2,0,0,a)[:2];p1=lp(x,y,u0+ww/2,0,0,a)[:2]
    bz_wall(m,p0,p1,0,9.25,[(h[0]-u0,*h[1:]) for h in holes if abs(h[0]-u0)<ww/2],PL,.355,.70)
    for s in (-1,1):facade_box(m,x,y,u0+s*(ww/2-.22),.74,(0.48+8.6)/2,.44,.08,8.12,TR,a)
    arch54(m,x,y,u0,a,7.6,.95,1.0,.74,.09,TR)
    facade_box(m,x,y,u0,.76,9.00,ww+.20,.30,.50,TR,a)
    pediment54(m,x,y,u0,a,ww+.10,9.30,11.55,.40,.72,PL)
    facade_box(m,x,y,u0,.72,.24,ww,.06,.48,M['Granite'],a)
  elif zone=='ax' and street54(w):
   big=(S(147.5),.80,2.80,2.09,.48);small=(S(143.6),1.29,1.47,1.60,.48)
   bz_wall(m,w['p'],w['q'],0,HZ,[big,small],PL)
   for u,b,ww,hh,r in (big,small):cas54(m,x,y,u,b,ww,hh+r*.7,a,rows=(.62,));arch54(m,x,y,u,a,b+hh,ww/2+.10,r+.08,.40,.07,TR)
   for k in (1,2):facade_box(m,x,y,big[0]-1.4+k*.93,.18,big[1]+big[3]/2,.07,.08,big[3],M['Frame'],a)
   facade_box(m,x,y,0,.39,.24,L,.08,.48,M['Granite'],a)
   facade_box(m,x,y,0,.42,4.72,L,.10,.26,TR,a);facade_box(m,x,y,0,.52,5.02,L+.10,.34,.34,TR,a)
   for X0 in (141.45,149.0):town_rod(m,lp(x,y,S(X0),.48,.25,a),lp(x,y,S(X0),.48,HZ,a),.05,M['Dark'],8)
  else:
   if w['kind']=='outer':plain(m,w,HZ,PL,M['Frame'],TR,2 if zone=='mn' else 1,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],PL)
for zone,rise,ins in (('mn',2.6,4.0),('ax',1.0,2.0)):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.5)
  inset_roof(m,pts,Z[zone]['height'],min(ins,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),rise,M['Roof'],.40)
for w in walls('mn'):
 if street54(w):
  x,y,L,a=sf_edge(w['p'],w['q']);uc=U(w,123.6,yf54(123.6))
  # The attic over the centre: set back 1.2 m, two windows, its own pediment.
  facade_box(m,x,y,uc,-1.4,H+.85,6.2,1.6,1.7,PL,a)
  for X0 in (122.35,124.85):cas54(m,x,y,U(w,X0,yf54(X0)),H+.45,1.05,.95,a,-.42,(.5,))
  facade_box(m,x,y,uc,-.55,H+1.78,6.4,.10,.16,TR,a)
  pediment54(m,x,y,uc,a,6.3,H+1.85,H+2.85,-1.3,-.58,PL)
  sl=2.6/4.0
  for X0 in (107.2,139.9):roof_dormer(m,x,y,U(w,X0,yf54(X0)),a,H,sl,.9,.75,.85,PL,M['Roof'],TR,False)
for cx,cy,zz in ((112.0,-166.0,Z['mn']['top']),(135.0,-166.5,Z['mn']['top']),(144.2,-165.0,Z['ax']['top']+.6)):box(m,cx,cy,.60,.80,1.1,zz-.4,M['Dark'],0,M['Dark'])
b54_finish(m,'91285838')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'W':(110.33,8.15),'M':(120.91,9.29),'E':(141.06,7.90)}
def _cam(n):X,D_=_C[n];return X,yf54(X)+.355+D_,2.62
block54_cameras=[
 sv_camera('308_Block54_Cal_West',*_cam('W'),152,10,90),
 sv_camera('309_Block54_Cal_Centre',*_cam('M'),152,10,90),
 sv_camera('310_Block54_Cal_East',*_cam('E'),152,10,90),
 ('311_Block54_Aerial',(128.0,-132.0,28.0),(128.0,-164.0,4.0),28),
]
print('BLOCK54_GEOMETRY',len(block54_names))
