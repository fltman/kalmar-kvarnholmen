"""Pass 32: Larmgatan 22 and 24 (OSM 92204181, 92204160).

Larmgatan 22: pale green render; two wide segmental-arched shop windows and a round-arched door;
a plain frieze over the shop floor (the historic shop lettering is omitted); five upper windows in
beige surrounds; a cornice with a low iron railing; two arched dormers. Larmgatan 24: white-grey
render; shop fronts; seven window axes; balconies with wrought-iron railings on consoles over the
middle three axes on both upper floors; pediments over the middle first-floor windows, cornice
heads over the others and panels with roundels under them; a dentilled main cornice; three attic
dormers. References: Google Street View April 2025 (registered on the houses' OSM joints), view
only. Zones: source/block32.json; see references/block32-notes.md. Tenant signs are omitted.
"""
B32D=json.loads((R/'source/block32.json').read_text());Z=B32D['zones']
block32_names=[];B32={}
for old in [k for k in list(materials) if k.startswith('M_Block32_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Green','TownIvory',(.64,.73,.69),.90,0),
 ('Beige','TownIvory',(.80,.73,.58),.84,0),
 ('GreenTrim','TownIvory',(.88,.89,.86),.82,0),
 ('White','TownIvory',(.86,.86,.84),.88,0),
 ('WhiteTrim','TownIvory',(.93,.93,.91),.82,0),
 ('Frame','TownPaintBrown',(.30,.20,.15),.55,0),
 ('FrameLight','TownPaintWhite',(.84,.84,.82),.55,0),
 ('DormerRed','TownPaintBrown',(.50,.22,.18),.58,0),
 ('Plinth','TownStone',(.52,.52,.50),.82,0),
 ('RoofDark','TownMetalGrey',(.24,.25,.26),.55,.30),
 ('Tile','TownTileRed',(.58,.30,.21),.80,0),
 ('Oak','TownPaintBrown',(.44,.28,.16),.58,0),
 ]:
 name='M_Block32_'+key;B32[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block32_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B32

def b32_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block32_names.append(name);return Mesh(name,category)
def b32_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=32;obj['reference_notes']='references/block32-notes.md';obj['osm_way']=osm;return obj
def street32(w):
 ox,oy=outward(w);return w['kind']=='outer' and ox<-.9 and min(w['p'][0],w['q'][0])<-284.5
def surround32(m,x,y,u,b,w,h,a,ma,bw=.13):
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),.38,b+h/2,bw,.07,h+2*bw,ma,a)
 facade_box(m,x,y,u,.38,b+h+bw/2,w+2*bw,.07,bw,ma,a);facade_box(m,x,y,u,.42,b-.05,w+2*bw+.10,.14,.08,ma,a)
def seg_dormer(m,x,y,u,a,H,slope,d,w,h,body,hood,frame,t0=math.radians(35)):
 # Dormer under a segmental arched roof (the two on Larmgatan 22): a round-headed window, the body
 # running back into the main roof. Based on roof_dormer, with a segmental instead of a round hood.
 zf=H+d*slope;xx,yy,_=lp(x,y,u,-d,0,a);zc=zf+.25+h/2;zs=zf+.25+h
 c=w/2+.26;r=c/math.cos(t0);zo=zs+.16-r*math.sin(t0)
 prof=[(r*math.cos(t),zo+r*math.sin(t)) for t in [math.pi-t0-(math.pi-2*t0)*k/12 for k in range(13)]]
 zt=max(v for _,v in prof);depth=(zt-zf)/slope+.25
 facade_box(m,xx,yy,0,-depth/2,(zf-.2+zs+.16)/2,w+.32,depth,zs+.36-zf,body,a)
 town_window(m,xx,yy,zc,w,h,a,frame,True,2,2,False)
 facade_box(m,xx,yy,0,.12,zf+.10,w+.40,.34,.08,body,a)
 for (u0,z0),(u1,z1) in zip(prof,prof[1:]):
  m.faces([lp(xx,yy,u0,.24,z0,a),lp(xx,yy,u1,.24,z1,a),lp(xx,yy,u1,-depth,z1,a),lp(xx,yy,u0,-depth,z0,a)],[(0,1,2,3)],hood)
 m.faces([lp(xx,yy,uu,.02,zz,a) for uu,zz in prof],[tuple(range(len(prof)))],body)
def roof32(m,zone,ma,wall):
 # Two slopes (street and courtyard) and a flat top; the fire-wall faces are rendered.
 RF=Z[zone]['roof'];outer,r1,fw=RF['outer'],RF['r1'],RF['firewall'];H=Z[zone]['height'];T=Z[zone]['top']
 n=len(outer)
 for i in range(n):
  j=(i+1)%n;m.faces([(*outer[i],H),(*outer[j],H),(*r1[j],T),(*r1[i],T)],[(0,1,2,3)],wall if fw[i] else ma)
 m.faces([(*p,T) for p in r1],[tuple(range(n))],ma)
 return (T-H)/RF['inset']
def wings32(m,zone,wall,frame,trim,roof):
 for w in walls(zone):
  if w['kind']=='outer':plain(m,w,Z[zone]['height'],wall,frame,trim,2,1.0)
  else:bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(2.4,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],roof,.35)

# ---------------------------------------------------------------- Larmgatan 22
GR,BE,GT,FR=M['Green'],M['Beige'],M['GreenTrim'],M['Frame']
H22=Z['l22']['height']
m=b32_new('SM_Kvarnholmen_House_92204181','Kvarnholmen/Larmgatan north')
for w in walls('l22'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H22,[],GR);continue
 if not street32(w):plain(m,w,H22,GR,FR,GT,2,1.0);continue
 S=lambda s:-L/2+s
 # Segmental-arched shop windows (sill 0.85, springing 2.76, crown 3.57) and the round-arched door.
 arches=[(S(2.70),.85,2.96,1.91,.81),(S(7.03),.85,2.94,1.91,.81)];door=(S(10.60),0,1.29,2.60,.645)
 up=[(S(s),4.90,1.0,1.70,0) for s in (1.77,3.64,6.04,8.05,10.62)]
 bz_wall(m,w['p'],w['q'],0,H22,[(u,b,ww,hh+r,0) for u,b,ww,hh,r in arches]+[door]+up,GR)
 for u,b,ww,hh,r in arches:
  spandrels(m,x,y,u,b,ww,hh,r,a,GR);seg_window(m,x,y,u,b,ww,hh,r,a,FR,GT)
 u,b,ww,hh,r=door;arch_door(m,x,y,u,b,ww,hh,r,a,M['Oak'])
 for u,b,ww,hh,r in up:s20_window(m,x,y,u,b,ww,hh,a,FR,GR,.66,False);surround32(m,x,y,u,b,ww,hh,a,BE)
 facade_box(m,x,y,0,.39,.22,L,.08,.44,M['Plinth'],a)
 strip(m,x,y,-L/2,L/2,3.72,3.88,a,GT,.355,.12);strip(m,x,y,-L/2,L/2,3.97,4.49,a,GR,.355,.04);strip(m,x,y,-L/2,L/2,4.49,4.60,a,GT,.355,.08)
 lm_cornice(m,x,y,L+.2,H22-.14,a,GT,False)
 # Low iron railing along the cornice.
 for zz in (H22+.08,H22+.33):town_rod(m,lp(x,y,-L/2,.62,zz,a),lp(x,y,L/2,.62,zz,a),.015,IRON)
 for k in range(round(L/.6)+1):uu=-L/2+k*L/round(L/.6);town_rod(m,lp(x,y,uu,.62,H22,a),lp(x,y,uu,.62,H22+.36,a),.018,IRON)
sl=roof32(m,'l22',M['RoofDark'],GR)
for w in walls('l22'):
 if street32(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  # Dormers set back behind the railing (3.70 and 7.94 m from the north joint): 1.5 m wide under
  # red-brown segmental roofs, tops about 9.45 (the calibration views put round-topped ones 0.6 m high).
  for s in (3.70,7.94):seg_dormer(m,x,y,-L/2+s,a,H22,sl,.80,1.0,.60,M['DormerRed'],M['DormerRed'],FR)
box(m,-282.6,27.6,.60,.90,2.6,H22+.6,GR,0,M['RoofDark'])
wings32(m,'l22r',GR,FR,GT,M['Tile'])
b32_finish(m,'92204181')

# ---------------------------------------------------------------- Larmgatan 24
WH,WT,FL=M['White'],M['WhiteTrim'],M['FrameLight']
H24=Z['l24']['height'];AX=[1.55,3.46,5.77,7.87,9.99,12.30,14.20]
m=b32_new('SM_Kvarnholmen_House_92204160','Kvarnholmen/Larmgatan north')
for w in walls('l24'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H24,[],WH);continue
 if not street32(w):plain(m,w,H24,WH,FL,WT,3,1.0);continue
 S=lambda s:-L/2+s
 # Narrow piers are kept between the openings that touch in the panorama.
 gf=[(S(1.78),.50,1.58,2.40,0),(S(3.40),0,1.00,2.90,0),(S(4.88),.50,1.64,2.40,0),(S(8.42),0,2.75,2.90,0),(S(12.75),0,5.40,2.93,0)]
 up1=[(S(s),5.10,1.05,2.02,0) for s in AX];up2=[(S(s),8.94,1.05,2.17,0) for s in AX]
 bz_wall(m,w['p'],w['q'],0,H24,gf+up1+up2,WH)
 for u,b,ww,hh,r in gf:
  s21_glass(m,x,y,u,b,ww,hh,a,M['Frame'],max(1,round(ww/1.4)),.80,b<.1)
  if b>0:facade_box(m,x,y,u,.40,b/2,ww+.10,.08,b,M['Plinth'],a)
 for i,(u,b,ww,hh,r) in enumerate(up1):
  s20_window(m,x,y,u,b,ww,hh,a,FL,WH,.68,False);surround32(m,x,y,u,b,ww,hh,a,WT,.14)
  if 2<=i<=4:
   tri=[(u-ww/2-.30,b+hh+.24),(u+ww/2+.30,b+hh+.24),(u,7.93)];vs=[lp(x,y,uu,o,zz,a) for o in (.36,.54) for uu,zz in tri]
   m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],WT)
  else:
   facade_box(m,x,y,u,.46,7.55,ww+.55,.22,.14,WT,a);facade_box(m,x,y,u,.42,7.38,ww+.40,.12,.20,WT,a)
   # Panel with a roundel under the window.
   facade_box(m,x,y,u,.38,4.66,ww+.40,.06,.62,WT,a);kk=16
   town_path(m,[lp(x,y,u+.20*math.cos(t*math.tau/kk),.42,4.66+.20*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.03,WT)
 for u,b,ww,hh,r in up2:
  s20_window(m,x,y,u,b,ww,hh,a,FL,WH,.68,False);surround32(m,x,y,u,b,ww,hh,a,WT,.12)
  facade_box(m,x,y,u,.44,11.46,ww+.40,.18,.12,WT,a)
 # Balconies over the middle three axes: a stone slab on consoles and a wrought-iron railing.
 # Measured on the facade plane, the projecting slabs and railings read high; set 0.15-0.2 m lower
 # after the calibration views.
 for zb,wb in ((4.25,5.80),(8.30,5.90)):
  uc=S(7.84);facade_box(m,x,y,uc,.355+.45,zb,wb,.90,.16,WT,a)
  for k in range(5):facade_box(m,x,y,uc-wb/2+.35+k*(wb-.7)/4,.355+.30,zb-.30,.18,.55,.42,WT,a)
  for zz in (zb+.12,zb+.85):town_rod(m,lp(x,y,uc-wb/2+.05,1.15,zz,a),lp(x,y,uc+wb/2-.05,1.15,zz,a),.02,IRON)
  for k in range(round(wb/.12)+1):
   uu=uc-wb/2+.05+k*(wb-.10)/round(wb/.12);town_rod(m,lp(x,y,uu,1.15,zb+.08,a),lp(x,y,uu,1.15,zb+.87,a),.008,IRON,4)
  for sgn in (-1,1):town_rod(m,lp(x,y,uc+sgn*(wb/2-.05),.40,zb+.12,a),lp(x,y,uc+sgn*(wb/2-.05),1.15,zb+.12,a),.02,IRON);town_rod(m,lp(x,y,uc+sgn*(wb/2-.05),.40,zb+.85,a),lp(x,y,uc+sgn*(wb/2-.05),1.15,zb+.85,a),.02,IRON)
 facade_box(m,x,y,0,.39,.20,L,.08,.40,M['Plinth'],a)
 strip(m,x,y,-L/2,L/2,3.80,4.32,a,WT,.355,.12);p18_band(m,x,y,L+.2,4.18,a,WT,.26)
 strip(m,x,y,-L/2,L/2,11.62,12.10,a,WH,.355,.04)
 lm_cornice(m,x,y,L+.3,H24-.14,a,WT,True)
sl=roof32(m,'l24',M['RoofDark'],WH)
for w in walls('l24'):
 if street32(w):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
  # Attic dormers: they show above the cornice from the street (caps at 15.2 on the sight line over
  # the cornice), so they stand just behind the wall line and run back to the flat top. A wide one
  # with three lights over the middle axes, one light each over the outer ones.
  AT=Z['l24']['top'];dep=(AT-H24)/sl-.10
  for sc,ww,nl in ((2.33,2.50,1),(7.84,5.20,3),(13.30,2.50,1)):
   xx,yy,_=lp(x,y,S(sc),-.10,0,a)
   facade_box(m,xx,yy,0,-dep/2,(H24+AT)/2,ww,dep,AT-H24,WH,a)
   facade_box(m,xx,yy,0,-dep/2+.12,AT+.06,ww+.24,dep+.24,.12,M['RoofDark'],a)
   facade_box(m,xx,yy,0,.08,AT-.30,ww+.12,.16,.22,WT,a)
   for k in range(nl):
    uu=-ww/2+(k+.5)*ww/nl;town_window(m,*lp(xx,yy,uu,.02,0,a)[:2],14.75,min(1.05,ww/nl-.35),1.15,a,FL,False,2,2,False)
box(m,-278.5,42.8,.70,1.00,4.4,H24+.6,WH,0,M['RoofDark'])
wings32(m,'l24r',WH,FL,WT,M['Tile'])
b32_finish(m,'92204160')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block32_cameras=[
 sv_camera('179_Block32_Cal_L22',-292.44,24.74,2.48,62,0),
 sv_camera('180_Block32_Cal_L22_Roof',-292.44,24.74,2.48,62,28),
 sv_camera('181_Block32_Cal_L24',-292.35,34.81,2.48,62,0),
 sv_camera('182_Block32_Cal_L24_Roof',-292.35,34.81,2.48,62,35),
 ('183_Block32_Aerial',(-318.0,52.0,34.0),(-278.0,30.0,6.0),28),
]
print('BLOCK32_GEOMETRY',len(block32_names))
