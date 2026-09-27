"""Pass 34: the three low houses on Södra Långgatan east of number 16 (OSM 92379287, 92379267,
92379282).

The Blanc house (number 18 over its door): pale render; four slender columns framing two shop
windows and the door; a pilaster dividing the front; a side door and a boarded double gate; four
upper windows in white surrounds over panels with roundels; a moulded band; an eaves board; a red
tile roof with three round-headed dormers in salmon surrounds (the middle one larger, with a
finial) and a chimney. The yellow house (number 21): yellow render with white lesenes; two shop
windows and the door; a red double gate under a latticed transom; a moulded band; five upper
windows in white surrounds under fabric awnings, over panels; an eaves board; a red tile roof with
a large boarded dormer and two skylights. The cream house: a long shop front of two windows and
two doors under a fascia, between white pilasters; four upper windows; an eaves board; a dark
roof with a chimney. References: Google Street View April 2025 (registered on the houses' OSM
joints), view only. Zones: source/block34.json; see references/block34-notes.md. Tenant signs,
awning texts and shop lettering are omitted.
"""
B34D=json.loads((R/'source/block34.json').read_text());Z=B34D['zones']
block34_names=[];B34={}
for old in [k for k in list(materials) if k.startswith('M_Block34_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Pale','TownIvory',(.86,.86,.82),.88,0),
 ('Yellow','TownIvory',(.93,.84,.60),.88,0),
 ('Cream','TownIvory',(.91,.88,.79),.88,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('GreyGreen','TownPaintBrown',(.52,.57,.52),.55,0),
 ('RedBrown','TownPaintBrown',(.42,.19,.14),.55,0),
 ('RedGate','TownPaintBrown',(.55,.22,.18),.60,0),
 ('Wood','TownPaintBrown',(.50,.33,.20),.58,0),
 ('Salmon','TownIvory',(.86,.55,.50),.82,0),
 ('Ochre','TownPaintBrown',(.66,.47,.32),.66,0),
 ('Plinth','TownStone',(.46,.46,.45),.80,0),
 ('Tile','TownTileRed',(.62,.32,.22),.80,0),
 ('RoofDark','TownMetalGrey',(.28,.29,.30),.55,.30),
 ('Awning','TownPanel',(.92,.92,.89),.90,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block34_'+key;B34[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block34_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B34;WH,PL=M['White'],M['Plinth']

def b34_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block34_names.append(name);return Mesh(name,category)
def b34_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=34;obj['reference_notes']='references/block34-notes.md';obj['osm_way']=osm;return obj
def street34(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-66
def win34(m,x,y,u,b,w,h,a,frame,wall,bw=.12):
 s20_window(m,x,y,u,b,w,h,a,frame,wall,.66,False)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),.38,b+h/2,bw,.07,h+2*bw,WH,a)
 facade_box(m,x,y,u,.38,b+h+bw/2,w+2*bw,.07,bw,WH,a);facade_box(m,x,y,u,.42,b-.05,w+2*bw+.08,.14,.08,WH,a)
def panel34(m,x,y,u,z0,z1,w,a,roundel=False):
 facade_box(m,x,y,u,.37,(z0+z1)/2,w,.05,z1-z0,WH,a)
 if roundel:
  kk=16;town_path(m,[lp(x,y,u+.09*math.cos(t*math.tau/kk),.41,(z0+z1)/2+.09*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.02,WH)
def plinth34(m,x,y,L,a,gaps,H=.45):
 at=-L/2
 for l,r in sorted(gaps)+[(L/2,L/2)]:
  if l>at+.02:facade_box(m,x,y,(at+l)/2,.40,H/2,l-at,.10,H,PL,a)
  at=max(at,r)
def eaves34(m,x,y,L,a,H,board):
 # Plain eaves board and gutter.
 facade_box(m,x,y,0,.40,H-.25,L+.1,.10,.40,board,a)
 facade_box(m,x,y,0,.50,H-.02,L+.2,.30,.08,board,a)
 town_rod(m,lp(x,y,-L/2,.70,H-.02,a),lp(x,y,L/2,.70,H-.02,a),.07,METAL,8)
def roof34(m,zone,ma,wall):
 RF=Z[zone]['roof'];outer,r1,fw=RF['outer'],RF['r1'],RF['firewall'];H=Z[zone]['height'];T=Z[zone]['top'];n=len(outer)
 for i in range(n):
  j=(i+1)%n;m.faces([(*outer[i],H),(*outer[j],H),(*r1[j],T),(*r1[i],T)],[(0,1,2,3)],wall if fw[i] else ma)
 m.faces([(*p,T) for p in r1],[tuple(range(n))],ma)
 return (T-H)/RF['inset']
def rear34(m,zone,wall,frame,roof):
 for w in walls(zone):
  if w['kind']=='outer':plain(m,w,Z[zone]['height'],wall,frame,WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(2.4,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],roof,.35)
def front_walls(zone,wall):
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
  elif not street34(w):plain(m,w,Z[zone]['height'],wall,M['Dark'],WH,2,.9)

# ---------------------------------------------------------------- the Blanc house
PA,GG=M['Pale'],M['GreyGreen'];H18=Z['b18']['height']
m=b34_new('SM_Kvarnholmen_House_92379287','Kvarnholmen/Södra Långgatan north')
front_walls('b18',PA)
for w in walls('b18'):
 if not street34(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
 gf=[(S(1.06),.46,1.54,2.00,0),(S(2.57),0,.81,2.13,0),(S(4.07),.46,1.56,2.00,0),(S(6.92),0,1.08,2.60,0),(S(10.18),0,1.52,2.75,0)]
 up=[(S(s),3.88,1.05,1.48,0) for s in (1.55,3.72,6.99,10.33)]
 bz_wall(m,w['p'],w['q'],0,H18,gf+up,PA)
 for u,b,ww,hh,r in gf:
  if b>0:s21_glass(m,x,y,u,b,ww,hh,a,GG,1,.82,False)
  elif ww<1.2:s20_door(m,x,y,u,b,ww,hh,a,GG)
  else:
   # Boarded double gate.
   facade_box(m,x,y,u,.14,hh/2,ww,.08,hh,WH,a)
   for k in range(1,6):facade_box(m,x,y,u-ww/2+k*ww/6,.19,hh/2,.03,.04,hh-.1,M['Pale'],a)
   facade_box(m,x,y,u,.20,hh/2,.04,.05,hh,GG,a)
 # Slender columns round the shop front, the fascia over it, the dividing pilaster.
 for s in (0.13,2.00,3.16,5.06):town_rod(m,lp(x,y,S(s),.50,.46,a),lp(x,y,S(s),.50,2.50,a),.10,WH,12);facade_box(m,x,y,S(s),.50,2.56,.30,.24,.12,WH,a)
 facade_box(m,x,y,S(2.6),.42,2.75,5.3,.16,.38,WH,a)
 facade_box(m,x,y,S(5.39),.40,H18/2,.36,.10,H18,WH,a)
 for s0,s1 in ((0,.22),(12.0,12.08)):facade_box(m,x,y,S((s0+s1)/2),.40,H18/2,s1-s0,.10,H18,WH,a)
 for u,b,ww,hh,r in up:win34(m,x,y,u,b,ww,hh,a,GG,PA);panel34(m,x,y,u,3.33,3.80,ww+.24,a,True)
 facade_box(m,x,y,0,.40,3.17,L,.12,.22,WH,a);p18_band(m,x,y,L+.1,3.24,a,WH,.22)
 plinth34(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.45])
 eaves34(m,x,y,L,a,H18,WH)
sl=roof34(m,'b18',M['Tile'],PA)
for w in walls('b18'):
 if street34(w):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
  # Round-headed dormers in salmon surrounds; the middle one larger with a finial.
  for s,ww,hh in ((1.47,.80,.55),(5.30,1.20,.80),(8.70,.80,.55)):
   roof_dormer(m,x,y,S(s),a,H18,sl,.60,ww,hh,M['Salmon'],M['Tile'],WH,True)
  xx,yy,_=lp(x,y,S(5.30),-.60,0,a);m.lathe(xx,yy,H18+.60*sl+.25+.80+.62,[(.05,0),(.09,.10),(.03,.20),(.02,.55)],M['Dark'],8)
box(m,-144.2,-62.4,.70,.90,Z['b18']['top']+.9-H18,H18,M['RedBrown'],0,M['Dark'])
rear34(m,'b18r',PA,M['Dark'],M['Tile'])
b34_finish(m,'92379287')

# ---------------------------------------------------------------- the yellow house
YE,RB=M['Yellow'],M['RedBrown'];H21=Z['y21']['height']
m=b34_new('SM_Kvarnholmen_House_92379267','Kvarnholmen/Södra Långgatan north')
front_walls('y21',YE)
for w in walls('y21'):
 if not street34(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
 gf=[(S(1.85),.36,2.60,1.51,0),(S(4.45),0,.87,2.08,0),(S(6.75),.36,2.06,1.51,0),(S(9.58),0,1.97,2.51,0)]
 # The fabric awnings hang over the upper part of the windows: the panorama's window top (4.79)
 # is the awnings' lower edge; the windows reach about 5.1 under them.
 up=[(S(s),3.61,1.10,1.49,0) for s in (1.75,3.69,5.58,7.30,9.60)]
 bz_wall(m,w['p'],w['q'],0,H21,gf+up,YE)
 for u,b,ww,hh,r in gf:
  if b>0:s21_glass(m,x,y,u,b,ww,hh,a,RB,1,.85,False);facade_box(m,x,y,u,.40,b+hh+.08,ww+.24,.08,.16,WH,a)
  elif ww<1.2:s20_door(m,x,y,u,b,ww,hh,a,RB);facade_box(m,x,y,u,.40,b+hh+.08,ww+.24,.08,.16,WH,a)
  else:
   # Red double gate under a latticed transom, in a white surround.
   facade_box(m,x,y,u,.14,1.02,ww,.08,2.04,M['RedGate'],a)
   for k in range(1,3):facade_box(m,x,y,u-ww/2+k*ww/3,.19,1.02,.05,.05,2.00,M['RedGate'],a)
   for k in range(3):
    for zz in (.5,1.4):facade_box(m,x,y,u-ww/2+(k+.5)*ww/3,.19,zz,ww/3-.2,.04,.6,M['RedGate'],a)
   facade_box(m,x,y,u,.12,2.28,ww,.05,.45,GLAZE,a)
   for k in range(4):town_rod(m,lp(x,y,u-ww/2+k*ww/3,.16,2.06,a),lp(x,y,u-ww/2+(k+.5)*ww/3,.16,2.48,a),.018,M['RedGate'],6);town_rod(m,lp(x,y,u-ww/2+(k+.5)*ww/3,.16,2.48,a),lp(x,y,u-ww/2+(k+1)*ww/3,.16,2.06,a),.018,M['RedGate'],6)
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.08),.40,hh/2,.16,.08,hh,WH,a)
   facade_box(m,x,y,u,.40,hh+.08,ww+.32,.08,.16,WH,a)
 for u,b,ww,hh,r in up:
  win34(m,x,y,u,b,ww,hh,a,RB,YE);panel34(m,x,y,u,3.23,3.55,ww+.24,a)
  # Fabric awning over the window.
  s21_shallow_awning(m,x,y,u,5.32,ww+.30,a,M['Awning'],.55)
 for s0,s1 in ((0,.34),(10.83,11.17)):facade_box(m,x,y,S((s0+s1)/2),.40,H21/2,s1-s0,.10,H21,WH,a)
 facade_box(m,x,y,0,.40,3.03,L,.12,.31,WH,a);p18_band(m,x,y,L+.1,3.12,a,WH,.24)
 plinth34(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.30],.30)
 eaves34(m,x,y,L,a,H21,WH)
sl=roof34(m,'y21',M['Tile'],YE)
for w in walls('y21'):
 if street34(w):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
  # The large boarded dormer with a gable, and two skylights.
  roof_dormer(m,x,y,S(5.67),a,H21,sl,1.0,1.15,1.25,M['Ochre'],M['Tile'],WH,False)
  for s in (3.3,8.6):
   xx,yy,_=lp(x,y,S(s),-1.6,0,a);zz=H21+1.6*sl
   facade_box(m,xx,yy,0,0,zz+.05,.55,.70,.08,M['Dark'],a)
rear34(m,'y21r',YE,RB,M['Tile'])
b34_finish(m,'92379267')

# ---------------------------------------------------------------- the cream house
CR,WD=M['Cream'],M['Wood'];H23=Z['c23']['height']
m=b34_new('SM_Kvarnholmen_House_92379282','Kvarnholmen/Södra Långgatan north')
front_walls('c23',CR)
for w in walls('c23'):
 if not street34(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
 gf=[(S(2.58),.25,2.87,2.30,0),(S(4.80),0,1.30,2.42,0),(S(6.50),0,1.40,2.42,0),(S(8.97),.25,3.39,2.30,0)]
 up=[(S(s),3.55,1.15,1.95,0) for s in (2.60,5.30,7.80,9.80)]
 bz_wall(m,w['p'],w['q'],0,H23,gf+up,CR)
 for u,b,ww,hh,r in gf:
  if b>0:s21_glass(m,x,y,u,b,ww,hh,a,WD,2,0,False)
  else:s21_glass(m,x,y,u,b,ww,hh,a,WD,1,.85,True)
 for u,b,ww,hh,r in up:win34(m,x,y,u,b,ww,hh,a,WH,CR)
 # White pilasters at both ends and a fascia over the shop front.
 for s0,s1 in ((.45,1.15),(10.66,11.39)):facade_box(m,x,y,S((s0+s1)/2),.40,H23/2,s1-s0,.12,H23,WH,a)
 facade_box(m,x,y,S(5.9),.42,2.83,9.6,.14,.52,CR,a);facade_box(m,x,y,S(5.9),.47,3.13,9.8,.20,.10,WH,a)
 plinth34(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.25],.25)
 eaves34(m,x,y,L,a,H23,WH)
sl=roof34(m,'c23',M['RoofDark'],CR)
box(m,-125.5,-61.4,.60,.90,Z['c23']['top']+.8-H23,H23,M['RedBrown'],0,M['Dark'])
rear34(m,'c23r',CR,M['Dark'],M['RoofDark'])
b34_finish(m,'92379282')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block34_cameras=[
 sv_camera('190_Block34_Cal_Blanc',-154.08,-74.56,2.30,345,0),
 sv_camera('191_Block34_Cal_Blanc_Roof',-154.08,-74.56,2.30,345,30),
 sv_camera('192_Block34_Cal_Yellow',-133.32,-74.33,2.20,332,0),
 sv_camera('193_Block34_Cal_Yellow_Roof',-133.32,-74.33,2.20,332,28),
 sv_camera('194_Block34_Cal_Cream_West',-133.32,-74.33,2.20,30,5),
 sv_camera('195_Block34_Cal_Cream_East',-113.90,-74.35,2.20,285,5),
 ('196_Block34_Aerial',(-118.0,-100.0,34.0),(-136.0,-60.0,4.0),28),
]
print('BLOCK34_GEOMETRY',len(block34_names))
