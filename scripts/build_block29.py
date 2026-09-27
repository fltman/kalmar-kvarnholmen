"""Pass 29: the north side of Södra Långgatan between Larmgatan and Kaggensgatan.

Södra Långgatan 9: a cream two-storey house with white lesenes, a red-brown gutter band over a
white frieze, a wall gable with a lunette, a wide arched doorway between two shop windows and a
tiled roof. Södra Långgatan 11: beige rough-cast, white window surrounds and quoins, a stepped
door surround round the courtyard passage, a moulded cornice broken by a segmental gable with a
fan light, two round dormers. The long ochre house: a grey-white shop floor with a white band,
wrought-iron sign brackets and an arched carriage gateway, twelve upper windows, a white cornice
and red dormers; it stands 0.55 m in front of its neighbour, whose side shows the brown west end.
The corner house on Kaggensgatan: orange rough-cast with smooth bands and surrounds, three storeys,
round-arched shop windows, a door with an oculus in an ochre surround, sconces, iron wall anchors
and a hipped tiled roof with eyebrow dormers. The Kaggensgatan range: yellow, two storeys, shop
windows and a tiled roof with dormers. References: Google Street View April 2025 (registered on the
north facades) and a contributed photosphere on Kaggensgatan (2020), view only. Zones:
source/block29.json; see references/block29-notes.md. Tenant signs and lettering are omitted.
"""
B29D=json.loads((R/'source/block29.json').read_text());Z=B29D['zones']
block29_names=[];B29={}
for old in [k for k in list(materials) if k.startswith('M_Block29_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.92,.88,.76),.86,0),
 ('CreamWhite','TownIvory',(.95,.94,.90),.82,0),
 ('GutterRed','TownPaintBrown',(.50,.26,.18),.60,0),
 ('Tile','TownTileRed',(.60,.31,.21),.80,0),
 ('TileDark','TownTileRed',(.46,.25,.19),.82,0),
 ('Beige','TownIvory',(.74,.66,.57),.95,0),
 ('White','TownIvory',(.94,.93,.90),.82,0),
 ('RedFrame','TownPaintBrown',(.50,.20,.15),.55,0),
 ('Plinth','TownStone',(.55,.55,.54),.82,0),
 ('MetalRoof','TownMetalGrey',(.30,.32,.33),.55,.30),
 ('Ochre','TownIvory',(.90,.74,.50),.90,0),
 ('GreyWhite','TownIvory',(.86,.86,.85),.86,0),
 ('Frame','TownPaintBrown',(.28,.20,.15),.55,0),
 ('RedDormer','TownMetalRed',(.60,.24,.19),.55,.20),
 ('BrownRough','TownIvory',(.46,.37,.31),.95,0),
 ('Salmon','TownIvory',(.80,.52,.38),.95,0),
 ('SalmonTrim','TownIvory',(.86,.66,.48),.84,0),
 ('OchreDoor','TownIvory',(.86,.64,.32),.82,0),
 ('LightStone','TownStone',(.72,.70,.66),.84,0),
 ('Yellow','TownIvory',(.90,.78,.46),.88,0),
 ('AwningPurple','TownPanel',(.40,.20,.28),.90,0),
 ('AwningRed','TownPanel',(.62,.18,.18),.90,0),
 ('AwningGreen','TownPanel',(.10,.42,.30),.90,0),
 ('AwningGrey','TownPanel',(.33,.33,.35),.90,0),
 ('AwningBlack','TownPanel',(.07,.07,.08),.90,0),
 ('Oak','TownPaintBrown',(.50,.33,.18),.58,0),
 ('Brass','TownPaintBrown',(.72,.56,.30),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block29_'+key;B29[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block29_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B29

def b29_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block29_names.append(name);return Mesh(name,category)
def b29_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=29;obj['reference_notes']='references/block29-notes.md';obj['osm_way']=osm;return obj
def street(w):
 # The street fronts on Södra Långgatan face south.
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-66
def kagg(w):
 ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and max(w['p'][0],w['q'][0])>-194
def S(L,s):return -L/2+s          # u of a point s metres from the wall's start
def surround(m,x,y,u,b,w,h,a,ma,bw=.19,o=.38):
 # Flat window surround: jambs, head and sill band proud of the render.
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),o,b+h/2,bw,.07,h+2*bw,ma,a)
 facade_box(m,x,y,u,o,b+h+bw/2,w+2*bw,.07,bw,ma,a);facade_box(m,x,y,u,o,b-bw/2,w+2*bw,.07,bw,ma,a)
def iron_bracket(m,x,y,u,z,a):
 # Wrought-iron sign bracket on the band: an arm with a scroll under it.
 town_rod(m,lp(x,y,u,.36,z,a),lp(x,y,u,.95,z,a),.018,IRON,6)
 town_rod(m,lp(x,y,u,.36,z-.40,a),lp(x,y,u,.36,z+.12,a),.016,IRON,6)
 town_rod(m,lp(x,y,u,.36,z-.30,a),lp(x,y,u,.70,z-.02,a),.014,IRON,6)
 for s in (-1,1):facade_box(m,x,y,u+s*.11,.38,z-.18,.12,.02,.12,IRON,a)
def anchor(m,x,y,u,z,a,ma):
 # Iron wall anchor end: a vertical bar with a lily head, over a short tie plate.
 facade_box(m,x,y,u,.40,z,.05,.04,.62,ma,a);facade_box(m,x,y,u,.40,z+.34,.18,.04,.05,ma,a)
 for s in (-1,1):town_rod(m,lp(x,y,u,.40,z+.30,a),lp(x,y,u+s*.12,.40,z+.44,a),.018,ma,6)
def sconce(m,x,y,u,z,a):
 facade_box(m,x,y,u,.42,z,.14,.10,.30,M['Brass'],a);facade_box(m,x,y,u,.49,z+.18,.18,.14,.05,M['Brass'],a)
def half_round(m,x,y,u,z,r,a,frame,trim,bars=5):
 # Half-round light (lunette or fan light) with radiating glazing bars.
 k=16;m.faces([lp(x,y,u,.30,z,a)]+[lp(x,y,u+r*math.cos(math.pi*t/k),.30,z+r*math.sin(math.pi*t/k),a) for t in range(k+1)],[tuple(range(k+2))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.03)*math.cos(math.pi*t/k),.36,z+(r+.03)*math.sin(math.pi*t/k),a) for t in range(k+1)],.04,frame)
 town_path(m,[lp(x,y,u+(r+.14)*math.cos(math.pi*t/k),.42,z+(r+.14)*math.sin(math.pi*t/k),a) for t in range(k+1)],.06,trim)
 facade_box(m,x,y,u,.36,z,2*r+.1,.06,.05,frame,a)
 for t in range(1,bars):ang=math.pi*t/bars;town_rod(m,lp(x,y,u,.34,z,a),lp(x,y,u+r*math.cos(ang),.34,z+r*math.sin(ang),a),.016,frame,6)
def spandrels(m,x,y,u,b,w,h,r,a,ma):
 # Closed wall prisms filling a rectangular opening down to its segmental head.
 R_=(w*w/4+r*r)/(2*r);t0=math.asin(w/2/R_);zc=b+h+r-R_;top=b+h+r;k=6
 for s in (-1,1):
  arc=[(u+s*R_*math.sin(t0*(1-i/k)),zc+R_*math.cos(t0*(1-i/k))) for i in range(k+1)]
  ring=arc+[(u+s*w/2,top)]          # the arc ends at the crown, on the top edge
  if s>0:ring=ring[::-1]
  n=len(ring);vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in ring]
  m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def seg_window(m,x,y,u,b,w,h,r,a,frame,trim):
 # Shop window under a segmental arch of rise r: glass, frame, a transom at the springing and a
 # moulded head on the true circular segment (a flat elliptical head folds its moulding).
 R_=(w*w/4+r*r)/(2*r);t0=math.asin(w/2/R_);k=12;zc=b+h+r-R_
 arc=[(u+R_*math.sin(-t0+2*t0*i/k),zc+R_*math.cos(-t0+2*t0*i/k)) for i in range(k+1)]
 m.faces([lp(x,y,uu,.12,zz,a) for uu,zz in [(u-w/2,b),(u+w/2,b)]+arc[::-1]],[tuple(range(k+3))],GLAZE)
 for s in (-1,1):facade_box(m,x,y,u+s*w/2,.25,b+h/2,.07,.24,h,frame,a)
 for q in (-w/6,w/6):facade_box(m,x,y,u+q,.28,b+h/2,.045,.09,h,frame,a)
 facade_box(m,x,y,u,.27,b,w,.22,.06,frame,a);facade_box(m,x,y,u,.27,b+h,w,.18,.06,frame,a)
 town_path(m,[lp(x,y,uu,.25,zz,a) for uu,zz in arc],.035,frame)
 town_path(m,[lp(x,y,u+(R_+.14)*math.sin(-t0*1.04+2.08*t0*i/k),.40,zc+(R_+.14)*math.cos(-t0*1.04+2.08*t0*i/k),a) for i in range(k+1)],.07,trim)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.12),.39,b+h/2,.20,.08,h+.10,trim,a)
 facade_box(m,x,y,u,.46,b-.07,w+.3,.40,.075,trim,a)
def gable_behind(m,x,y,u,zb,w,rise,a,ma,depth):
 pts=[(u-w/2-.15,zb),(u,zb+rise),(u+w/2+.15,zb)]
 for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
  m.faces([lp(x,y,u0,.55,z0,a),lp(x,y,u1,.55,z1,a),lp(x,y,u1,-depth,z1,a),lp(x,y,u0,-depth,z0,a)],[(0,1,2,3)],ma)
def chimney(m,cx,cy,z,h,ma,cap):box(m,cx,cy,.62,.95,h,z,ma,0,cap)
# Roof insets follow the narrowest range of each zone; the ochre house's roof runs over its main
# range only (the small jogs in the rear line are left under the eaves).
INSET={'sl9':3.2,'sl9r':1.5,'sl161':1.3,'sl11':3.8,'sl11r':2.4,'sl13':6.2,'sl13r':1.1,'kg':5.9,'k189e':4.9,'k189r':2.9}
ROOF={'sl13':[[(-233.45,-68.21),(-204.49,-68.76),(-204.49,-55.57),(-233.6,-54.9)]]}
def hip(zone,ma,ov=.45,top=None):
 H=Z[zone]['height'];ins=INSET[zone];rs=Z[zone]['top']-H
 for g in ROOF.get(zone,Z[zone]['polygons']):inset_roof(m,simplify([tuple(v) for v in g],.8),H,ins,rs,ma,ov,top)
 return rs/(ins+ov)
def rear(m,zone,ma,frame,trim,levels):
 for w in walls(zone):plain(m,w,Z[zone]['height'],ma,frame,trim,levels,.9)

# ---------------------------------------------------------------- Södra Långgatan 9
CR,CW,GR=M['Cream'],M['CreamWhite'],M['GutterRed']
H9=Z['sl9']['height'];G9=Z['sl9']['gable']
m=b29_new('SM_Kvarnholmen_House_92204156','Kvarnholmen/Södra Långgatan north')
for w in walls('sl9'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not street(w):plain(m,w,H9,CR,M['White'],CW,2,.9);continue
 up=[S(L,s) for s in (2.14,4.45,6.51,8.53,10.62)]
 holes=[(u,3.69,1.0,1.39,0) for u in up]
 # Ground floor: west shop window, the arched doorway (door and gate), east shop window.
 holes+=[(S(L,2.40),.97,2.56,1.53,0),(S(L,5.67),.42,2.63,1.66,.50),(S(L,9.52),.50,3.58,1.90,0)]
 bz_wall(m,w['p'],w['q'],0,H9,holes,CR)
 for u,b,ww,hh,r in holes:
  if r>0:
   TRIM_=TRIM;TRIM=CW;arch_door(m,x,y,u,b,ww,hh,r,a,M['Oak']);TRIM=TRIM_
   for k in range(9):uu=u+ww*.12+k*.05;town_rod(m,lp(x,y,uu,.30,b,a),lp(x,y,uu,.30,b+hh+.25,a),.012,IRON,6)
  elif b<1.2:s21_glass(m,x,y,u,b,ww,hh,a,M['White'],2 if ww<3 else 3,.78,False)
  else:s20_window(m,x,y,u,b,ww,hh,a,M['White'],CW);facade_box(m,x,y,u,.40,b-.10,ww+.24,.10,.10,CW,a)
 for u in up:s21_shallow_awning(m,x,y,u,5.32,1.18,a,M['AwningGrey'],.62)
 s21_shallow_awning(m,x,y,S(L,1.95),2.72,3.50,a,M['AwningPurple'],.80)
 s21_shallow_awning(m,x,y,S(L,9.16),2.72,4.50,a,M['AwningRed'],.80)
 facade_box(m,x,y,0,.39,.22,L,.08,.44,M['Plinth'],a)
 # White lesenes at both ends, frieze, red-brown gutter band.
 for s0,s1 in ((0.0,.57),(11.47,12.04)):strip(m,x,y,S(L,s0),S(L,s1),.44,5.80,a,CW,.355,.07)
 strip(m,x,y,-L/2,L/2,5.40,5.72,a,CW,.355,.10);facade_box(m,x,y,0,.52,5.82,L+.3,.34,.22,GR,a)
 # Wall gable over the middle three bays with a lunette; its roof runs back into the main roof.
 gu=S(L,G9[0]);gw=G9[1];rise=G9[2]-H9
 tri=[(gu-gw/2,H9),(gu+gw/2,H9),(gu,G9[2])];vs=[lp(x,y,uu,o,zz,a) for o in (.02,.36) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],CR)
 for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1])):town_rod(m,lp(x,y,u0,.46,z0+.06,a),lp(x,y,u1,.46,z1+.06,a),.10,GR,8)
 half_round(m,x,y,gu,6.82,.42,a,M['White'],CW,4)
 gable_behind(m,x,y,gu,H9+.02,gw,rise,a,M['Tile'],3.2)
sk=hip('sl9',M['Tile'])
rear(m,'sl9r',CR,M['White'],CW,2);hip('sl9r',M['Tile'])
b29_finish(m,'92204156')
m=b29_new('SM_Kvarnholmen_House_92204161','Kvarnholmen/Södra Långgatan north')
rear(m,'sl161',CR,M['White'],CW,2);hip('sl161',M['Tile'])
b29_finish(m,'92204161')

# ---------------------------------------------------------------- Södra Långgatan 11
BE,WH,RF=M['Beige'],M['White'],M['RedFrame']
H11=Z['sl11']['height'];G11=Z['sl11']['gable']
m=b29_new('SM_Kvarnholmen_House_92204198','Kvarnholmen/Södra Långgatan north')
for w in walls('sl11'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not street(w):plain(m,w,H11,BE,RF,WH,2,.9);continue
 up=[S(L,s) for s in (1.82,5.34,7.77,9.63)];ud=S(L,5.45)
 holes=[(u,3.56,1.02,1.89,0) for u in up]
 holes+=[(S(L,1.96),.45,2.27,1.95,0),(ud,.45,2.40,1.68,.23),(S(L,8.93),.45,2.54,1.90,0)]
 bz_wall(m,w['p'],w['q'],0,H11,holes,BE)
 for u,b,ww,hh,r in holes:
  if r>0:
   # Courtyard passage: iron gate leaves in the opening.
   facade_box(m,x,y,u,.10,b+(hh+r)/2,ww,.06,hh+r,M['Dark'],a)
   for k in range(15):uu=u-ww/2+.1+k*(ww-.2)/14;town_rod(m,lp(x,y,uu,.22,b,a),lp(x,y,uu,.22,b+hh+r*.8,a),.014,IRON,6)
  elif b<1:s21_glass(m,x,y,u,b,ww,hh,a,RF,2,.80,False)
  else:s20_window(m,x,y,u,b,ww,hh,a,RF,WH);surround(m,x,y,u,b,ww,hh,a,WH,.18)
 s21_shallow_awning(m,x,y,S(L,2.28),2.66,3.22,a,M['AwningRed'],.80)
 s21_shallow_awning(m,x,y,S(L,9.05),2.66,3.10,a,M['AwningGreen'],.80)
 facade_box(m,x,y,0,.39,.22,L,.08,.44,M['Plinth'],a)
 # Stepped white surround: block jambs and three steps rising to a keystone.
 for s in (-1,1):quoins(m,x,y,ud+s*(2.40/2+.02),.44,2.55,a,WH,s,.40,.46,.30)
 for k,(ww_,zz) in enumerate(((3.25,2.62),(2.55,2.92),(1.85,3.20),(1.05,3.46))):facade_box(m,x,y,ud,.40,zz,ww_,.08,.30 if k<3 else .34,WH,a)
 quoins(m,x,y,S(L,.22),.44,H11-.55,a,WH,1,.42,.42,.26)
 quoins(m,x,y,L/2-.01,.44,H11-.55,a,WH,-1,.42,.46,.30)
 # Moulded cornice broken by the segmental gable over the passage: the cornice pieces stop 0.94 m
 # either side of its axis and the gable's moulding lands on them.
 gu=S(L,G11[0]);gw=G11[1]
 for s0,s1 in ((-L/2-.25,gu-.94),(gu+.94,L/2+.25)):
  cx,cy,_=lp(x,y,(s0+s1)/2,0,0,a);lm_cornice(m,cx,cy,s1-s0,H11-.20,a,WH,False)
 k=16;crest=[(gu+gw/2*math.cos(math.pi*i/k),6.20+(G11[2]-6.20)*math.sin(math.pi*i/k)) for i in range(k+1)]
 outline=[(gu-gw/2,6.10),(gu+gw/2,6.10)]+crest;n=len(outline);vs=[lp(x,y,uu,o,zz,a) for o in (.02,.40) for uu,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],BE)
 town_path(m,[lp(x,y,uu,.46,zz+.06,a) for uu,zz in crest],.10,WH)
 half_round(m,x,y,gu,6.40,.62,a,WH,WH,6)
 # Curved roof behind the gable, following its crest back into the main roof.
 for (u0,z0),(u1,z1) in zip(crest,crest[1:]):
  m.faces([lp(x,y,u1,.40,z1+.04,a),lp(x,y,u0,.40,z0+.04,a),lp(x,y,u0,-2.4,z0+.04,a),lp(x,y,u1,-2.4,z1+.04,a)],[(0,1,2,3)],M['MetalRoof'])
sk=hip('sl11',M['MetalRoof'])
for w in walls('sl11'):
 if street(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for s in (1.82,9.63):roof_dormer(m,x,y,S(L,s),a,H11,sk,.15,.50,.50,M['MetalRoof'],M['MetalRoof'],WH,True)
  cx,cy,_=lp(x,y,S(L,2.3),-3.0,0,a);chimney(m,cx,cy,8.4,1.2,BE,M['Dark'])
rear(m,'sl11r',BE,RF,WH,2);hip('sl11r',M['MetalRoof'])
b29_finish(m,'92204198')

# ---------------------------------------------------------------- the long ochre house
OC,GW,FR=M['Ochre'],M['GreyWhite'],M['Frame']
H13=Z['sl13']['height']
m=b29_new('SM_Kvarnholmen_House_92204187','Kvarnholmen/Södra Långgatan north')
UP13=(2.0,4.33,6.66,8.99,11.32,13.66,16.0,18.6,20.87,23.21,25.53,27.85)
for w in walls('sl13'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox<-.9 and L<1.0:
  # The 0.55 m west end beside Södra Långgatan 11: brown rough render.
  bz_wall(m,w['p'],w['q'],0,H13,[],M['BrownRough']);continue
 if not street(w):plain(m,w,H13,OC,FR,M['White'],2,1.0);continue
 up=[S(L,s) for s in UP13]
 holes=[(u,5.20,1.19,1.73,0) for u in up]
 shops=[(1.1,3.8),(5.2,7.5),(8.0,11.34),(14.11,17.59),(22.25,26.41)];doors=[(4.1,5.0),(12.53,13.47),(27.37,28.25)]
 holes+=[(S(L,(s0+s1)/2),.75,s1-s0,2.30,0) for s0,s1 in shops]+[(S(L,(s0+s1)/2),.10,s1-s0,2.84,0) for s0,s1 in doors]
 gu=S(L,19.73);holes.append((gu,.05,2.04,2.22,1.02))
 # Grey-white shop floor below the band, ochre upper floor.
 bz_wall(m,w['p'],w['q'],0,4.0,[h for h in holes if h[1]<4],GW);bz_wall(m,w['p'],w['q'],4.0,H13,[h for h in holes if h[1]>4],OC)
 for u,b,ww,hh,r in holes:
  if r>0:
   # Carriage gateway: fanlight over a transom, iron gate below, white arched surround.
   p18_win(m,x,y,u,b+1.98,ww,.24,1.02,a,FR,M['White'],1,6)
   facade_box(m,x,y,u,.10,b+.99,ww,.06,1.98,M['Dark'],a)
   for k in range(13):uu=u-ww/2+.1+k*(ww-.2)/12;town_rod(m,lp(x,y,uu,.24,b+.05,a),lp(x,y,uu,.24,b+1.92,a),.014,IRON,6)
   town_path(m,[lp(x,y,u+(ww/2+.16)*math.cos(math.pi*t/16),.42,b+2.22+(r+.16)*math.sin(math.pi*t/16),a) for t in range(17)],.10,M['White'])
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.2),.40,b+1.11,.30,.08,2.22,M['White'],a)
  elif b>5:s20_window(m,x,y,u,b,ww,hh,a,FR,M['White'],.62,True);surround(m,x,y,u,b,ww,hh,a,M['White'],.12)
  elif b<.2:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
  else:s21_glass(m,x,y,u,b,ww,hh,a,FR,3 if ww>3 else 2,.82,False)
 # Grey-white shop floor under the white band, ochre upper floor, brown west strip.
 strip(m,x,y,-L/2,-L/2+.62,.0,H13,a,M['BrownRough'],.355,.025)
 strip(m,x,y,-L/2+.62,L/2,4.0,4.33,a,M['White'],.355,.12)
 quoins(m,x,y,-L/2+.64,4.33,H13-.5,a,M['White'],1,.42,.40,.26)
 facade_box(m,x,y,.31,.39,.20,L-.62,.08,.40,M['LightStone'],a)
 for s in (1.0,3.4,5.5,7.1,9.6,12.3,15.1,17.6,21.85,24.35,26.9):iron_bracket(m,x,y,S(L,s),4.62,a)
 for s0,s1,ma in ((.9,4.3,M['AwningRed']),(5.1,7.8,M['AwningRed']),(7.85,11.6,M['AwningGrey'])):s21_shallow_awning(m,x,y,S(L,(s0+s1)/2),2.95,s1-s0,a,ma,.85)
 lm_cornice(m,x,y,L+.4,H13-.20,a,M['White'],False)
sk=hip('sl13',M['MetalRoof'])
for w in walls('sl13'):
 if street(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for s in (2.2,5.0,23.0,26.5):roof_dormer(m,x,y,S(L,s),a,H13,sk,.30,1.15,1.40,M['RedDormer'],M['RedDormer'],M['White'],False)
  for s in (8.0,17.0):cx,cy,_=lp(x,y,S(L,s),-6.0,0,a);chimney(m,cx,cy,H13+3.0,1.3,OC,M['Dark'])
rear(m,'sl13r',OC,FR,M['White'],2);hip('sl13r',M['MetalRoof'])

# ---------------------------------------------------------------- corner house on Kaggensgatan
SA,ST_,LS=M['Salmon'],M['SalmonTrim'],M['LightStone']
HK=Z['kg']['height']
def kg_face(m,w,x,y,L,a,bays,ground):
 holes=[]
 for s in bays:holes+=[(S(L,s),5.78,1.45,1.87,0),(S(L,s),9.15,1.45,1.85,0)]
 holes+=[(u,b,ww,hh+r,0) for u,b,ww,hh,r in ground];bz_wall(m,w['p'],w['q'],0,HK,holes,SA)
 for u,b,ww,hh,r in ground:
  if r>0:spandrels(m,x,y,u,b,ww,hh,r,a,SA)
 for u,b,ww,hh,r in holes:
  if b>5:s20_window(m,x,y,u,b,ww,hh,a,FR,ST_,.64,True);surround(m,x,y,u,b,ww,hh,a,ST_,.12,.37)
 facade_box(m,x,y,0,.39,.27,L,.10,.55,LS,a)
 strip(m,x,y,-L/2,L/2,4.46,4.88,a,ST_,.355,.07);strip(m,x,y,-L/2,L/2,11.10,HK-.25,a,ST_,.355,.05)
 facade_box(m,x,y,0,.62,HK-.12,L+.9,.62,.18,SA,a);town_rod(m,lp(x,y,-L/2-.4,.95,HK-.25,a),lp(x,y,L/2+.4,.95,HK-.25,a),.07,M['Brass'],8)
 return holes
for w in walls('kg'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if street(w):
  ground=[(S(L,3.17),.80,3.05,2.73,.20),(S(L,7.30),.80,3.00,2.73,.20)]
  holes=kg_face(m,w,x,y,L,a,(2.35,5.43,7.92),ground)
  for u,b,ww,hh,r in ground:seg_window(m,x,y,u,b,ww,hh,r,a,FR,ST_)
  s21_shallow_awning(m,x,y,S(L,7.30),3.45,3.30,a,M['AwningBlack'],1.05)
  for s in (.66,4.0,7.0,10.1):anchor(m,x,y,S(L,s),5.25,a,IRON)
  for s in (.66,4.0,7.0,10.1):anchor(m,x,y,S(L,s),8.55,a,IRON)
  for s in (.95,3.89,6.68):sconce(m,x,y,S(L,s),6.55,a)
  strip(m,x,y,L/2-.40,L/2,.55,HK-.25,a,ST_,.355,.06)
 elif kagg(w):
  # Kaggensgatan: the door with its oculus, two arched shop windows, a small arched door.
  ground=[(S(L,2.0),.35,1.02,2.30,0),(S(L,5.7),.80,2.80,2.72,.20),(S(L,9.2),.80,2.80,2.72,.20),(S(L,11.95),.30,.82,2.05,.41)]
  holes=kg_face(m,w,x,y,L,a,(2.0,5.3,8.5,11.4),ground)
  for u,b,ww,hh,r in ground:
   # Stone steps up to the raised doors (two treads).
   if b>.2:facade_box(m,x,y,u,.66,b/4,ww+.60,.62,b/2,LS,a);facade_box(m,x,y,u,.51,b*.75,ww+.40,.32,b/2,LS,a)
   if ww<.9:
    # Small arched door at the north end: a boarded leaf under a round head.
    s20_door(m,x,y,u,b,ww,hh-.20,a,M['Oak']);p18_win(m,x,y,u,b+hh-.20,ww,.20,r,a,FR,ST_,1,2)
   elif ww<1.2:
    s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
    # Ochre keyhole surround rising round the oculus.
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.16),.40,b+1.55,.30,.09,3.10,M['OchreDoor'],a)
    facade_box(m,x,y,u,.40,b+hh+.12,ww+.62,.09,.24,M['OchreDoor'],a)
    kk=20;town_path(m,[lp(x,y,u+.62*math.cos(math.pi*t/kk),.42,3.35+.62*math.sin(math.pi*t/kk),a) for t in range(kk+1)],.10,M['OchreDoor'])
    oculus(m,x,y,u,3.30,.34,a,FR,M['OchreDoor'])
   else:seg_window(m,x,y,u,b,ww,hh,r,a,FR,ST_)
  for s in (5.7,9.2):s21_shallow_awning(m,x,y,S(L,s),3.45,3.10,a,M['AwningBlack'],1.05)
  for s in (3.7,7.4,10.6):anchor(m,x,y,S(L,s),5.25,a,IRON);anchor(m,x,y,S(L,s),8.55,a,IRON)
  for s in (3.7,7.4):sconce(m,x,y,S(L,s),6.55,a)
  strip(m,x,y,-L/2,-L/2+.40,.55,HK-.25,a,ST_,.355,.06)
 else:plain(m,w,HK,SA,FR,ST_,3,1.0)
sk=hip('kg',M['TileDark'])
for w in walls('kg'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 # Eyebrow dormers rise straight behind the gutter (seen just above it from the street).
 if street(w):roof_dormer(m,x,y,S(L,4.4),a,HK,sk,.0,.90,.60,M['TileDark'],M['TileDark'],FR,True)
 elif kagg(w):roof_dormer(m,x,y,S(L,6.5),a,HK,sk,.0,.90,.60,M['TileDark'],M['TileDark'],FR,True)
cx,cy=-199.5,-61.5;chimney(m,cx,cy,HK+2.6,1.4,SA,M['Dark'])
b29_finish(m,'92204187')

# ---------------------------------------------------------------- Kaggensgatan range
YE=M['Yellow'];HY=Z['k189e']['height']
m=b29_new('SM_Kvarnholmen_House_92204189','Kvarnholmen/Södra Långgatan north')
for w in walls('k189e'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not kagg(w):plain(m,w,HY,YE,FR,M['White'],2,1.0);continue
 us=[S(L,1.3+k*2.63) for k in range(8)]
 holes=[(u,4.35,1.10,1.45,0) for u in us]
 for k,u in enumerate(us):holes.append((u,.10,1.05,2.40,0) if k==6 else (u,.65,1.90,2.20,0))
 bz_wall(m,w['p'],w['q'],0,HY,holes,YE)
 for u,b,ww,hh,r in holes:
  if b>4:s20_window(m,x,y,u,b,ww,hh,a,FR,M['White']);surround(m,x,y,u,b,ww,hh,a,M['White'],.14)
  elif b<.2:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
  else:s21_glass(m,x,y,u,b,ww,hh,a,M['Dark'],2,.80,False)
 for k,u in enumerate(us):
  if k<6:s21_shallow_awning(m,x,y,u,3.25,2.10,a,M['AwningBlack'],.90)
 facade_box(m,x,y,0,.39,.22,L,.08,.44,M['Plinth'],a)
 strip(m,x,y,-L/2,L/2,3.55,3.80,a,M['White'],.355,.10)
 lm_cornice(m,x,y,L+.4,HY-.20,a,M['White'],False)
sk=hip('k189e',M['Tile'])
for w in walls('k189e'):
 if kagg(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for s in (2.6,6.6,10.6,14.6,18.6):roof_dormer(m,x,y,S(L,s),a,HY,sk,.60,.70,.80,M['RedDormer'],M['Tile'],M['White'],False)
rear(m,'k189r',YE,FR,M['White'],2);hip('k189r',M['Tile'])
# Gate wall across the passage between the corner house and the range.
p,q=(-192.72,-56.00),(-192.99,-53.55);x,y,L,a=sf_edge(p,q)
bz_wall(m,p,q,0,3.3,[(0,.02,1.90,2.20,.60)],YE)
for k in range(11):uu=-.85+k*.17;town_rod(m,lp(x,y,uu,.22,.05,a),lp(x,y,uu,.22,2.62,a),.016,IRON,6)
facade_box(m,x,y,0,.50,3.36,L+.2,.30,.12,M['White'],a)
b29_finish(m,'92204189')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Cameras stand their measured distance from the modelled facade surface (0.355 m proud of the
# OSM line; the ochre house and the corner house 0.55 m further out).
SLAB=.355
block29_cameras=[
 sv_camera('163_Block29_Cal_SL9',-245.43,-73.46,2.37,332,30),
 sv_camera('164_Block29_Cal_SL11',-235.27,-73.54,2.39,332,0),
 sv_camera('165_Block29_Cal_Ochre',-217.14,-74.06,2.15,332,28),
 sv_camera('166_Block29_Corner_House',-207.77,-74.60,2.38,345,35),
 sv_camera('167_Block29_Ochre_West',-235.27,-73.54,2.39,5,0),
 ('168_Block29_Aerial',(-168.0,-110.0,48.0),(-222.0,-52.0,4.0),26),
]
print('BLOCK29_GEOMETRY',len(block29_names))
