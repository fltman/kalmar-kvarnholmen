"""Pass 83: the warehouse row on the south side of Kom snart igen, backing onto Skeppsbron:
- the white boarded warehouse at the west end (Kom snart igen 2), with a large and a small
  frontispiece on the street, two on Skeppsbron;
- three boarded two-storey warehouses (cream, cream, pale green): two frontispieces on each long
  front, tall upper windows in brown frames, diamond windows, carriage gates and doors below, a
  fretwork frieze under the low metal roofs;
- the white rendered house at the east end with two small frontispieces;
- the links: a boarded one, the middle one with a low lean-to on the street and a glazed two-storey
  front on Skeppsbron, and the white one with garage doors and a black box dormer.

References: Google Street View April 2025 (panoramas on Kom snart igen and Skeppsbron; the green
warehouse measured from a resected one), view only. Zones: source/block83.json; see
references/block83-notes.md. Signs, awnings, lamps, the spiral stair and the heat pumps are omitted.
"""
B83D=json.loads((R/'source/block83.json').read_text());Z=B83D['zones']
block83_names=[];B83={}
for old in [k for k in list(materials) if k.startswith('M_Block83_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.90,.90,.91),.82,0),('Cream','TownIvory',(.92,.89,.79),.82,0),('CreamPale','TownIvory',(.93,.91,.84),.82,0),('Green','TownIvory',(.80,.84,.72),.82,0),
 ('Render','TownIvory',(.94,.93,.89),.88,0),('Frame','TownPaintBrown',(.43,.36,.30),.60,0),('Door','TownPaintBrown',(.50,.38,.29),.60,0),('GreyDoor','TownMetalGrey',(.42,.42,.40),.55,.10),
 ('WhiteTrim','TownPaintWhite',(.95,.95,.93),.55,0),('Roof','TownMetalGrey',(.24,.25,.27),.55,.30),('Black','TownMetalGrey',(.07,.075,.08),.45,.20),
 ('Plinth','TownStone',(.62,.60,.57),.90,0),('Mullion','TownMetalGrey',(.20,.21,.22),.45,.40),
 ]:
 name='M_Block83_'+key;B83[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block83_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B83;FR=M['Frame']

def b83_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block83_names.append(name);return Mesh(name,category)
def b83_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=83;obj['reference_notes']='references/block83-notes.md';obj['osm_way']=osm;return obj
FO=tuple(B83D['frame']['origin']);FD=tuple(B83D['frame']['along']);FN=tuple(B83D['frame']['inwards'])
def rect83(zone,d=FD,n=FN,o=FO):
 pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-o[0])*d[0]+(v[1]-o[1])*d[1] for v in pts];ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for v in pts]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))
 return (r if area>0 else r[::-1])
def saddle83(m,zone,ma,wall,ov=.6,d=FD,n=FN,o=FO):
 # Saddle roof along the row over the zone's boxed outline (ridge along d), gable triangles at the
 # ends, eaves pushed out by the overhang.
 pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-o[0])*d[0]+(v[1]-o[1])*d[1] for v in pts];ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for v in pts]
 s0,s1,t0,t1=min(ss),max(ss),min(ts),max(ts);H=Z[zone]['height'];T=Z[zone]['top'];tm=(t0+t1)/2;sl=(T-H)/((t1-t0)/2)
 P=lambda s,t,z:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t,z)
 for ta in (t0-ov,t1+ov):
  m.faces([P(s0-.25,ta,H-ov*sl),P(s1+.25,ta,H-ov*sl),P(s1+.25,tm,T),P(s0-.25,tm,T)],[(0,1,2,3),(3,2,1,0)],ma)
  town_rod(m,P(s0-.25,ta,H-ov*sl-.04),P(s1+.25,ta,H-ov*sl-.04),.07,M['Black'],8)
 for s in (s0,s1):m.faces([P(s,t0,H),P(s,t1,H),P(s,tm,T)],[(0,1,2),(2,1,0)],wall)
 return sl
def flat83(m,zone,z,ma):
 for g in Z[zone]['polygons']:m.faces([(*v,z) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
def diamond83(m,x,y,u,zc,r,a,frame):
 m.faces([lp(x,y,u-r,.37,zc,a),lp(x,y,u,.37,zc-r,a),lp(x,y,u+r,.37,zc,a),lp(x,y,u,.37,zc+r,a)],[(0,1,2,3),(3,2,1,0)],GLAZE)
 town_path(m,[lp(x,y,u-r-.06,.41,zc,a),lp(x,y,u,.41,zc-r-.06,a),lp(x,y,u+r+.06,.41,zc,a),lp(x,y,u,.41,zc+r+.06,a),lp(x,y,u-r-.06,.41,zc,a)],.06,frame)
 town_path(m,[lp(x,y,u,.40,zc-.02-r,a),lp(x,y,u,.40,zc+r+.02,a)],.02,frame)
def frontis83(m,x,y,u,fw,H,fe,fa,a,wall,frame,roof,win=True):
 # A frontispiece: the facade carried up past the eaves to its own eaves, a gable over it, a deep
 # roof running back into the main slope, bargeboards, and a pair of windows.
 facade_box(m,x,y,u,.18,(H+fe)/2,fw,.36,fe-H,wall,a)
 prof=[(u-fw/2,fe),(u+fw/2,fe),(u,fa)];vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],wall)
 of,ob=.95,-3.2;sl=(fa-fe)/(fw/2)
 for s in (-1,1):
  e=fw/2+.35;q=[lp(x,y,u+s*e,of,fa+.12-e*sl,a),lp(x,y,u,of,fa+.12,a),lp(x,y,u,ob,fa+.12,a),lp(x,y,u+s*e,ob,fa+.12-e*sl,a)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],roof)
  town_path(m,[lp(x,y,u+s*e,of-.02,fa-.05-e*sl,a),lp(x,y,u,of-.02,fa-.05,a)],.07,frame)
 if win:
  for s in (-1,1):
   uu=u+s*.45;b=fe-1.25
   facade_box(m,x,y,uu,.37,b+.5,.58,.02,1.0,GLAZE,a);cas81(m,x,y,uu,b,.58,1.0,a,frame,.41,2)
 # Fretwork frieze: a deep board with a scalloped lower edge suggested by short drops.
 facade_box(m,x,y,u,.42,fe-.15,fw+.1,.08,.30,wall,a);facade_box(m,x,y,u,.46,fe-.32,fw+.1,.05,.06,frame,a)
def gate83(m,x,y,u,b,w,h,a,leaf,frame):
 for s in (-1,1):
  facade_box(m,x,y,u+s*w/4,.12,b+h/2,w/2-.03,.07,h,leaf,a)
  for zz in (b+.35,b+h-.35):facade_box(m,x,y,u+s*w/4,.17,zz,w/2-.15,.03,.08,frame,a)
 facade_box(m,x,y,u,.18,b+h/2,.05,.05,h,frame,a);surround36(m,x,y,u,b,w,h,a,frame,.12,.40)
def door83(m,x,y,u,b,w,h,a,leaf,frame,glass=True):
 facade_box(m,x,y,u,.12,b+h/2,w,.07,h,leaf,a)
 if glass:facade_box(m,x,y,u,.17,b+h*.72,w-.30,.02,h*.36,GLAZE,a)
 for zz in (b+h*.32,):facade_box(m,x,y,u,.17,zz,w-.28,.03,h*.30,frame,a)
 surround36(m,x,y,u,b,w,h,a,frame,.12,.40)

# Facade layouts (u along the wall from its middle, metres). The green warehouse's street front is
# measured: gates under the frontispieces, which stand about a quarter of the length in from each
# end; the other boarded fronts follow the same pattern, which the panoramas show on all of them.
def layout83(L,kind):
 ops=[];fr=[]
 if kind in ('boarded','white'):
  cs=(-.23*L,.23*L);fw=3.8
  for c in cs:
   fr.append((c,fw));ops+=[('win',c-.85,3.75,1.0,1.85),('win',c+.85,3.75,1.0,1.85),('gate',c,.30,2.0,2.35)]
  ops+=[('diam',-.23*L+2.5,4.70,.38,0),('diam',.23*L-2.5,4.70,.38,0),('win',-L/2+1.5,3.75,1.0,1.85),('win',L/2-1.5,3.75,1.0,1.85),
   ('door',-L/2+1.6,.30,1.0,2.2),('door',L/2-1.6,.30,1.0,2.2),('shop',0,.75,1.7,1.8)]
 elif kind=='render':
  cols=[-L/2+1.7+k*(L-3.4)/5 for k in range(6)]
  for k,c in enumerate(cols):
   ops.append(('win',c,3.90,.95,1.55))
   if k not in (2,3):ops.append(('win',c,1.10,.95,1.55))
  ops+=[('door',(cols[2]+cols[3])/2,.25,1.1,2.25),('diam',cols[2],2.0,.30,0),('diam',cols[3],2.0,.30,0)]
  fr=[(cols[1],2.2),(cols[4],2.2)]
 return ops,fr
KIND={'wh':'white','u1':'boarded','u2':'boarded','u3':'boarded','u4':'render'}
WALL={'wh':'White','u1':'Cream','u2':'CreamPale','u3':'Green','u4':'Render','l1':'White','l2n':'White','l2s':'White','l3':'White'}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b83_new(nm,'Kvarnholmen/Kom snart igen')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];wm=M[WALL[zone]];kind=KIND.get(zone)
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  front=abs(oy)>.85 and L>8 and kind is not None
  if zone=='l2s' and oy<-.85:
   # The glazed front on Skeppsbron: two storeys of glass in dark mullions, a canopy between.
   bz_wall(m,w['p'],w['q'],0,H,[(0,.05,L-.3,H-.45,0)],wm)
   facade_box(m,x,y,0,.30,H/2,L-.3,.02,H-.45,GLAZE,a)
   for k in range(5):facade_box(m,x,y,-L/2+.15+k*(L-.3)/4,.34,H/2,.08,.10,H-.45,M['Mullion'],a)
   for zz in (.05,2.9,4.6,H-.4):facade_box(m,x,y,0,.34,zz,L-.3,.10,.08,M['Mullion'],a)
   facade_box(m,x,y,0,1.0,3.05,L+.4,1.4,.10,M['Mullion'],a);continue
  if zone=='l3' and oy>.85:
   holes=[(-.7,0,1.25,2.4,0),(.75,0,1.25,2.4,0)];bz_wall(m,w['p'],w['q'],0,H,holes,wm)
   for u,b,ww,hh,r in holes:
    facade_box(m,x,y,u,.12,hh/2,ww,.06,hh,M['GreyDoor'] if u<0 else M['WhiteTrim'],a)
    for k in range(1,8):facade_box(m,x,y,u,.16,k*hh/8,ww-.1,.02,.03,M['Mullion'],a)
   facade_box(m,x,y,0,.42,H-.12,L+.1,.14,.24,M['Black'],a);continue
  if not front:
   plain(m,w,H,wm,FR,M['WhiteTrim'],2 if H>5 else 1,.9);continue
  ops,fr=layout83(L,kind)
  if zone=='wh' and oy>.85:
   ops=[o for o in ops if not (o[0]=='gate' and o[1]<0)]+[('door',-.23*L,.30,1.0,2.2)];fr=[(-.30*L,2.6),(.12*L,3.8)]
  holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in ops if k!='diam']
  bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  if kind!='render':boards81(m,x,y,L,a,.45,H-.95,holes+[(u,b-ww-.1,2*ww+.2,2*ww+.2,0) for k,u,b,ww,hh in ops if k=='diam'],wm)
  frame=FR if kind!='render' else M['WhiteTrim']
  for k,u,b,ww,hh in ops:
   if k=='diam':diamond83(m,x,y,u,b,ww,a,frame);continue
   if k=='win':
    cas81(m,x,y,u,b,ww,hh,a,frame,.16,3);surround36(m,x,y,u,b,ww,hh,a,frame,.10,.40);facade_box(m,x,y,u,.47,b-.05,ww+.24,.16,.06,frame,a)
    if kind!='render':facade_box(m,x,y,u,.44,b+hh+.16,ww+.30,.14,.16,frame,a)
   elif k=='shop':
    facade_box(m,x,y,u,.14,b+hh/2,ww,.02,hh,GLAZE,a);cas81(m,x,y,u,b,ww,hh,a,frame,.18,2);surround36(m,x,y,u,b,ww,hh,a,frame,.12,.40)
   elif k=='gate':gate83(m,x,y,u,b,ww,hh,a,M['Door'],frame)
   else:door83(m,x,y,u,b,ww,hh,a,M['Door'] if kind!='render' else M['WhiteTrim'],frame)
  # Plinth, corner boards, the frieze under the eaves, the storey band.
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for k,u,b,ww,hh in ops if k in ('door','gate'))+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.22,lo-at,.08,.44,M['Plinth'],a)
   at=max(at,hi)
  for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,H/2,.22,.10,H,frame if kind!='render' else M['WhiteTrim'],a)
  if kind!='render':
   # The frieze: boards in the wall colour with a fretted lower edge (short drops) in the frame colour.
   facade_box(m,x,y,0,.40,H-.47,L,.06,.90,wm,a);facade_box(m,x,y,0,.44,H-.93,L,.05,.06,frame,a)
   for k in range(int(L/.3)):facade_box(m,x,y,-L/2+.15+k*L/int(L/.3),.45,H-1.02,.10,.04,.12,frame,a)
  else:facade_box(m,x,y,0,.44,H-.12,L+.1,.16,.24,M['WhiteTrim'],a);facade_box(m,x,y,0,.42,3.3,L,.06,.12,M['WhiteTrim'],a)
  fe,fa=spec['fr']
  for c,fw in fr:frontis83(m,x,y,c,fw,H,fe,fa,a,wm,frame,M['Roof'],True)
# Roofs.
for zone in ('u1','u2','u3','u4'):saddle83(meshes[Z[zone]['mesh']],zone,M['Roof'],M[WALL[zone]])
wd=(-48.4-(-65.9),-268.5-(-263.6));Lw=math.hypot(*wd);wd=(wd[0]/Lw,wd[1]/Lw)
saddle83(meshes['SM_Kvarnholmen_House_91915622'],'wh',M['Roof'],M['White'],d=wd,n=(wd[1],-wd[0]),o=(-65.9,-263.6))
m=meshes['SM_Kvarnholmen_House_91915624']
flat83(m,'l1',Z['l1']['height']+.02,M['Roof']);flat83(m,'l2n',Z['l2n']['height']+.02,M['Black']);flat83(m,'l2s',Z['l2s']['height']+.02,M['Mullion']);flat83(m,'l3',Z['l3']['height']+.02,M['Roof'])
# The black box dormer on the east link.
cx=sum(v[0] for v in Z['l3']['polygons'][0])/len(Z['l3']['polygons'][0]);cy=sum(v[1] for v in Z['l3']['polygons'][0])/len(Z['l3']['polygons'][0])
box(m,cx,cy,2.6,3.0,2.2,Z['l3']['height'],M['Black'],math.atan2(FD[1],FD[0]))
P=lambda s,t:(cx+FD[0]*s+FN[0]*t,cy+FD[1]*s+FN[1]*t)
X,Y=P(0,-1.52);m.box((X,Y,Z['l3']['height']+1.2),(1.6,.04,1.0),GLAZE,math.atan2(FD[1],FD[0]))
for nm in meshes:b83_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block83_cameras=[
 sv_camera('412_Block83_Cal_Green',19.32,-281.51,2.40,182,10,90),
 sv_camera('413_Block83_Cal_Cream',-9.84,-274.6,2.20,152,10,90),
 sv_camera('414_Block83_Cal_Render',19.32,-281.51,2.40,122,10,90),
 ('415_Block83_Aerial',(0.0,-320.0,32.0),(-5.0,-285.0,2.0),28),
]
print('BLOCK83_GEOMETRY',len(block83_names))
