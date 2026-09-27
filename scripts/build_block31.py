"""Pass 31: Larmgatan 16 (OSM 92204162).

A yellow two-storey front between white rusticated lesenes: two shop windows under awnings, two
doors on steps and the arched carriage passage with an iron gate under a cartouche carrying the
house number; a white moulded cornice over the shop floor; five upper windows in white surrounds
under cornice heads, a pediment on the middle one; a dentilled main cornice; a steep red-tiled roof
with three red dormers. Two lower courtyard wings behind. References: Google Street View April 2025
(registered on the house's two joints), view only. Zones: source/block31.json; see
references/block31-notes.md. Tenant names on the awnings are omitted.
"""
B31D=json.loads((R/'source/block31.json').read_text());Z=B31D['zones'];Z31=Z['front']
block31_names=[];B31={}
for old in [k for k in list(materials) if k.startswith('M_Block31_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.88,.72,.44),.90,0),
 ('White','TownIvory',(.93,.92,.88),.82,0),
 ('Frame','TownPaintBrown',(.30,.20,.15),.55,0),
 ('Plinth','TownStone',(.36,.35,.34),.80,0),
 ('Tile','TownTileRed',(.62,.30,.20),.80,0),
 ('Dormer','TownMetalRed',(.62,.22,.18),.55,.20),
 ('Awning','TownPanel',(.45,.12,.14),.90,0),
 ('Oak','TownPaintBrown',(.42,.27,.16),.58,0),
 ]:
 name='M_Block31_'+key;B31[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block31_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B31;YE,WH,FR,PL,TI=(M[k] for k in ('Yellow','White','Frame','Plinth','Tile'))
H=Z31['height'];BR=Z31['break_'];TOP=Z31['top'];CG=Z31['cornice_ground'];WZ=Z31['windows']

def b31_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block31_names.append(name);return Mesh(name,category)
def b31_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=31;obj['reference_notes']='references/block31-notes.md';obj['osm_way']=osm;return obj

m=b31_new('SM_Kvarnholmen_House_92204162','Kvarnholmen/Larmgatan')
UPS=[1.42,3.47,5.84,8.16,10.20]
for w in walls('front'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if not (w['kind']=='outer' and ox<-.9):
  plain(m,w,H,YE,FR,WH,2,1.0,w['kind']=='outer');continue
 S=lambda s:-L/2+s
 gf=[(S(2.10),.60,2.30,2.45,0),(S(4.24),.30,.86,2.20,0),(S(5.80),0,1.68,2.30,.59),(S(7.42),.30,.86,2.20,0),(S(9.55),.60,2.30,2.45,0)]
 up=[(S(s),WZ[0],1.05,WZ[1]-WZ[0],0) for s in UPS]
 bz_wall(m,w['p'],w['q'],0,H,gf+up,YE)
 for u,b,ww,hh,r in gf:
  if r>0:
   # Carriage passage: an arched opening with an iron gate and a white arched surround.
   facade_box(m,x,y,u,-.60,(hh+r)/2,ww,.06,hh+r,M['Oak'],a)
   for k in range(11):uu=u-ww/2+.1+k*(ww-.2)/10;town_rod(m,lp(x,y,uu,.24,.05,a),lp(x,y,uu,.24,hh+r*math.sqrt(max(0,1-(2*(uu-u)/ww)**2))-.06,a),.016,IRON,6)
   town_path(m,[lp(x,y,u+(ww/2+.12)*math.cos(math.pi*t/16),.40,hh+(r+.12)*math.sin(math.pi*t/16),a) for t in range(17)],.09,WH)
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.12),.40,hh/2,.20,.08,hh,WH,a)
  elif ww<1:
   s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
   for k,(dd,zz) in enumerate(((.80,.10),(.55,.20))):facade_box(m,x,y,u,.355+dd/2,zz,ww+.50-k*.2,dd,.10,PL,a)
   facade_box(m,x,y,u,.40,b+hh+.10,ww+.30,.10,.20,WH,a)
  else:
   s21_glass(m,x,y,u,b,ww,hh,a,FR,3,.80,False);facade_box(m,x,y,u,.40,b-.06,ww+.10,.14,.12,PL,a)
   s21_shallow_awning(m,x,y,u,b+hh+.05,ww+.20,a,M['Awning'],.75)
 for i,(u,b,ww,hh,r) in enumerate(up):
  s20_window(m,x,y,u,b,ww,hh,a,FR,WH,.70,False)
  for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.08),.39,b+hh/2,.16,.07,hh+.16,WH,a)
  facade_box(m,x,y,u,.44,b-.08,ww+.36,.16,.10,WH,a);facade_box(m,x,y,u,.40,b+hh+.10,ww+.30,.08,.16,WH,a)
  if i==2:
   tri=[(u-ww/2-.25,b+hh+.22),(u+ww/2+.25,b+hh+.22),(u,7.68)];vs=[lp(x,y,uu,o,zz,a) for o in (.36,.52) for uu,zz in tri]
   m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],WH)
  else:facade_box(m,x,y,u,.46,7.40,ww+.50,.22,.16,WH,a);facade_box(m,x,y,u,.42,7.22,ww+.36,.12,.20,WH,a)
 # Plinth, lesenes, the shop-floor cornice, the cartouche and the dentilled main cornice.
 cuts=[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.5];at=-L/2
 for l,r_ in sorted(cuts)+[(L/2,L/2)]:
  if l>at+.02:facade_box(m,x,y,(at+l)/2,.40,.25,l-at,.10,.50,PL,a)
  at=max(at,r_)
 for s0,s1 in ((0.0,.79),(10.76,11.56)):
  uc=S((s0+s1)/2);z=.5
  while z<7.8:
   facade_box(m,x,y,uc,.41,min(z+.21,7.8)-.12,s1-s0,.10,.34,WH,a);z+=.42
 strip(m,x,y,-L/2,L/2,CG[0],CG[1],a,WH,.355,.12);p18_band(m,x,y,L+.1,CG[1]-.10,a,WH,.26)
 k=24;cz=(3.09+3.64)/2;uc=S(5.83)
 m.faces([lp(x,y,uc+.36*math.cos(t*math.tau/k),.44,cz+.27*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],WH)
 town_path(m,[lp(x,y,uc+.42*math.cos(t*math.tau/k),.48,cz+.33*math.sin(t*math.tau/k),a) for t in range(k+1)],.05,WH)
 lm_cornice(m,x,y,L+.2,H-.14,a,WH,True)
# Roof: the steep lower slope and the low upper slope; the party-wall faces are rendered.
RF=Z31['roof'];outer,r1,r2,fw=RF['outer'],RF['r1'],RF['r2'],RF['firewall']
def stage(ra,rb,z0,z1,ma):
 n=len(ra)
 for i in range(n):
  j=(i+1)%n;m.faces([(*ra[i],z0),(*ra[j],z0),(*rb[j],z1),(*rb[i],z1)],[(0,1,2,3)],YE if fw[i] else ma)
stage(outer,r1,H,BR,TI);stage(r1,r2,BR,TOP,TI);m.faces([(*p,TOP) for p in r2],[tuple(range(len(r2)))],TI)
slope=(BR-H)/1.2
for w in walls('front'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox<-.9:
  # Three dormers, the outer two between the window axes (measured 2.40, 5.87 and 9.26 m).
  # They stand close behind the cornice with tall windows (top about 10.9 in the pitched view).
  for s in (2.40,5.87,9.26):roof_dormer(m,x,y,-L/2+s,a,H,slope,.30,1.0,1.20,M['Dormer'],M['Dormer'],WH,False)
for zone in ('wing_n','wing_s'):
 for w in walls(zone):plain(m,w,Z[zone]['height'],YE,FR,WH,2,1.0)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(1.9,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],TI,.35)
b31_finish(m,'92204162')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The camera keeps its measured distance from the modelled facade (0.355 m proud of the OSM line).
block31_cameras=[
 sv_camera('176_Block31_Cal_Front',-290.77,-37.05,2.48,62,0),
 sv_camera('177_Block31_Cal_Roof',-290.77,-37.05,2.48,62,28),
 ('178_Block31_Aerial',(-318.0,-52.0,30.0),(-278.0,-37.0,6.0),28),
]
print('BLOCK31_GEOMETRY',len(block31_names))
