"""Pass 66: the district volume 91885531 on Norra Långgatan (number 49), a salmon rendered
three-storey house:
- a rusticated ground floor on a dark granite plinth, four tall brown-framed windows with dark sills
  and the round-arched gateway (49) with its panelled wooden doors at the west end;
- a cream cornice over the ground floor, the first floor with a grouped triple window under one
  entablature and single windows over the gateway and at the east end, each over a carved apron;
- plain surrounds on the second floor, a frieze and a bracketed cornice under a low saddle roof.
The courtyard wing keeps a plain two-storey rhythm.

References: Google Street View April 2025 (a close panorama facing the gateway, anchored on the joint
with the 1964 block, and one near the east corner, anchored on the corner and chained on the
gateway), view only. Zones: source/block66.json; see references/block66-notes.md. The drainpipes
and the number plate are omitted.
"""
B66D=json.loads((R/'source/block66.json').read_text());Z=B66D['zones']
block66_names=[];B66={}
for old in [k for k in list(materials) if k.startswith('M_Block66_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Salmon','TownIvory',(.92,.68,.55),.92,0),
 ('Groove','TownIvory',(.74,.50,.40),.95,0),
 ('Cream','TownIvory',(.94,.90,.78),.86,0),
 ('Plinth','TownStone',(.24,.22,.22),.88,0),
 ('BrownFrame','TownPaintBrown',(.44,.32,.25),.55,0),
 ('Door','TownPaintBrown',(.46,.31,.19),.60,0),
 ('Roof','TownMetalGrey',(.24,.24,.25),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block66_'+key;B66[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block66_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B66;SA=M['Salmon'];CR=M['Cream']

def b66_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block66_names.append(name);return Mesh(name,category)
def b66_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=66;obj['reference_notes']='references/block66-notes.md';obj['osm_way']=osm;return obj
def ys66(X):return 72.331+(X-121.713)*(72.403-72.331)/(134.275-121.713)
def cas66(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['BrownFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.70):facade_box(m,x,y,u,o,zz,w,.08,.06,M['BrownFrame'],a)
def arc66(m,x,y,u,a,spring,half,rise,o,r,ma,n=12):
 pts=[(u-half,spring)]+[(u-half*math.cos(math.pi*k/n),spring+rise*math.sin(math.pi*k/n)) for k in range(1,n)]+[(u+half,spring)]
 town_path(m,[lp(x,y,uu,o,zz,a) for uu,zz in pts],r,ma)
def apron66(m,x,y,u,a,w):
 # The carved apron under a first-floor window: a sunk panel between two consoles, a scroll in it.
 facade_box(m,x,y,u,.42,4.30,w,.08,.44,CR,a);facade_box(m,x,y,u,.40,4.30,w-.40,.10,.26,SA,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.08),.48,4.30,.18,.14,.50,CR,a)
 town_path(m,[lp(x,y,u+du,.46,4.30+dz,a) for du,dz in ((-.36,-.02),(-.18,.06),(0,.10),(.18,.06),(.36,-.02))],.035,CR)

GF=[126.05,127.8,129.45,132.5];UP=[123.2,126.05,127.8,129.45,132.5];GATE=123.68
m=b66_new('SM_Kvarnholmen_House_91885531','Kvarnholmen/Norra Långgatan')
for zone in ('fr','wg'):
 HZ=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if zone=='fr' and w['kind']=='outer' and oy<-.9:
   S=lambda X:U(w,X,ys66(X))
   gf=[(S(X0),1.12,1.32,1.90,0) for X0 in GF]
   u1=[(S(X0),4.55,1.25,1.82,0) for X0 in UP];u2=[(S(X0),7.90,1.20,1.73,0) for X0 in UP]
   gate=(S(GATE),0,2.30,2.50,.55)
   bz_wall(m,w['p'],w['q'],0,HZ,gf+u1+u2+[gate],SA)
   # The rusticated ground floor: grooves every 0.30 m, broken round the windows and the gateway.
   for k in range(1,11):
    zz=.75+k*.265;at=-L/2
    for uu,ww in sorted([(u,ww+.40) for u,b,ww,hh,r in gf if b-.1<zz<b+hh+.1]+([(gate[0],gate[2]+.50)] if zz<3.1 else [])):
     if uu-ww/2>at+.05:facade_box(m,x,y,(at+uu-ww/2)/2,.37,zz,uu-ww/2-at,.03,.03,M['Groove'],a)
     at=uu+ww/2
    if L/2>at+.05:facade_box(m,x,y,(at+L/2)/2,.37,zz,L/2-at,.03,.03,M['Groove'],a)
   for u,b,ww,hh,r in gf:
    surround36(m,x,y,u,b,ww,hh,a,SA,.16,.40);cas66(m,x,y,u,b,ww,hh,a)
    facade_box(m,x,y,u,.46,b-.05,ww+.22,.22,.07,M['BrownFrame'],a)
   u,b,ww,hh,r=gate
   for s in (-1,1):
    facade_box(m,x,y,u+s*ww/4,.12,(hh+r-.15)/2,ww/2-.02,.06,hh+r-.15,M['Door'],a)
    for zz,ph in ((.55,.8),(1.55,.9),(2.40,.45)):facade_box(m,x,y,u+s*ww/4,.16,zz,ww/2-.30,.03,ph,M['Door'],a)
    facade_box(m,x,y,u+s*(ww/2+.20),.41,hh/2,.36,.10,hh,SA,a)
   arc66(m,x,y,u,a,hh,ww/2+.12,r+.06,.42,.10,SA);arc66(m,x,y,u,a,hh+.10,ww/2+.30,r+.10,.41,.06,M['Groove'])
   gl,gh=gate[0]-gate[2]/2-.30,gate[0]+gate[2]/2+.30
   for lo,hi in ((-L/2,gl),(gh,L/2)):facade_box(m,x,y,(lo+hi)/2,.39,.36,hi-lo,.08,.72,M['Plinth'],a)
   for s in (-1,1):facade_box(m,x,y,s*(L/2-.30),.40,(.72+3.5)/2,.60,.08,2.78,SA,a)
   # The cream cornice over the ground floor and the sill band of the first floor.
   facade_box(m,x,y,0,.42,3.62,L,.10,.12,CR,a);facade_box(m,x,y,0,.52,3.78,L+.08,.30,.20,CR,a);facade_box(m,x,y,0,.46,3.98,L,.18,.10,M['Dark'],a)
   facade_box(m,x,y,0,.44,4.05,L,.14,.08,CR,a)
   for u,b,ww,hh,r in u1:
    cas66(m,x,y,u,b,ww,hh,a);apron66(m,x,y,u,a,ww+.36)
    surround36(m,x,y,u,b,ww,hh,a,CR,.14,.40)
   # The triple window: one entablature over the three, pilasters between them.
   ua,ub=S(GF[0]),S(GF[2]);lo,hi=min(ua,ub)-.85,max(ua,ub)+.85
   facade_box(m,x,y,(lo+hi)/2,.44,6.62,hi-lo,.12,.22,CR,a);facade_box(m,x,y,(lo+hi)/2,.54,6.82,hi-lo+.16,.32,.14,CR,a)
   for X0 in (123.2,132.5):
    facade_box(m,x,y,S(X0),.44,6.62,1.70,.12,.22,CR,a);facade_box(m,x,y,S(X0),.54,6.82,1.86,.32,.14,CR,a)
   facade_box(m,x,y,0,.42,7.72,L,.10,.10,CR,a)
   for u,b,ww,hh,r in u2:
    cas66(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,CR,.12,.40)
    facade_box(m,x,y,u,.46,b-.06,ww+.34,.20,.08,CR,a)
   # The frieze and the bracketed cornice.
   facade_box(m,x,y,0,.42,10.05,L,.10,.18,CR,a)
   n=int(L/.55)
   for k in range(n):facade_box(m,x,y,-L/2+(k+.5)*L/n,.50,10.40,.14,.26,.30,CR,a)
   facade_box(m,x,y,0,.46,10.62,L+.06,.20,.12,CR,a);facade_box(m,x,y,0,.62,10.78,L+.20,.52,.16,CR,a)
  else:
   if w['kind']=='outer':plain(m,w,HZ,SA,M['BrownFrame'],CR,3 if zone=='fr' else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],SA)
roof34(m,'fr',M['Roof'],SA)
for g in Z['wg']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,Z['wg']['height'],min(2.4,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['wg']['top']-Z['wg']['height'],M['Roof'],.35)
for cx in (125.0,131.0):box(m,cx,79.0,.55,.75,1.0,Z['fr']['top']-.6,M['Roof'],0,M['Dark'])
b66_finish(m,'91885531')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block66_cameras=[
 sv_camera('349_Block66_Cal_Gate',121.33,68.23-.355,2.30,332,15,90),
 sv_camera('350_Block66_Cal_East',132.05,68.51-.355,2.30,282,15,90),
 ('351_Block66_Aerial',(128.0,55.0,28.0),(128.0,80.0,4.0),28),
]
print('BLOCK66_GEOMETRY',len(block66_names))
