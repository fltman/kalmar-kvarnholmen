"""Pass 63: the district volumes 91970370 and 91970388 on the west side of Östra Sjögatan:
- number 17 (91970370): pale yellow vertical boarding between four white pilasters, three axes of
  white casements on both storeys, a grey plinth with cellar vents, the eaves, and a tile roof with
  a gabled dormer and a snow rail;
- number 19 (91970388): grey-green boarding, five upper and four ground white casements, the central
  grey-green boarded gateway (19) between fluted pilasters under a cornice, a scalloped frieze under
  the eaves, and three red dormers (the middle one pedimented).
The courtyard wings keep a plain two-storey rhythm.

References: Google Street View April 2025 (two panoramas on Östra Sjögatan, each resected on its
house's corners and number 19's centred gateway), view only. Zones: source/block63.json; see
references/block63-notes.md.
"""
B63D=json.loads((R/'source/block63.json').read_text());Z=B63D['zones']
block63_names=[];B63={}
for old in [k for k in list(materials) if k.startswith('M_Block63_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.92,.85,.62),.80,0),
 ('Green','TownIvory',(.74,.78,.72),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownStone',(.45,.46,.47),.88,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Gate','TownPaintWhite',(.55,.66,.64),.60,0),
 ('RedDormer','TownPaintBrown',(.55,.15,.12),.60,0),
 ('Tile','TownTileRed',(.55,.30,.23),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block63_'+key;B63[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block63_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B63;WH=M['White']

def b63_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block63_names.append(name);return Mesh(name,category)
def b63_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=63;obj['reference_notes']='references/block63-notes.md';obj['osm_way']=osm;return obj
def xe63(Y):return 48.586+(Y-99.87)*(48.618-48.586)/(121.743-99.87)
def street63(w):ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and max(w['p'][0],w['q'][0])>48.4
def cas63(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h/3,b+2*h/3):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['WhiteFrame'],a)
 facade_box(m,x,y,u,.44,b-.05,w+.20,.18,.06,WH,a)

meshes={nm:b63_new(nm,'Kvarnholmen/Östra Sjögatan') for nm in ('SM_Building_91970370','SM_Building_91970388')}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height'];wall=M['Yellow'] if zone=='g17' else M['Green']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda Y:U(w,xe63(Y),Y)
  if zone=='g17' and street63(w):
   up=[(S(Y0),4.36,1.20,1.90,0) for Y0 in (101.29,105.54,107.88)];gf=[(S(Y0),1.55,1.20,1.74,0) for Y0 in (101.2,105.57,107.93)]
   bz_wall(m,w['p'],w['q'],0,HZ,up+gf,wall);boards35(m,x,y,L,a,.97,7.1,up+gf,wall,.22)
   for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas63(m,x,y,u,b,ww,hh,a)
   for u,b,ww,hh,r in up+gf:facade_box(m,x,y,u,.46,b+hh+.18,ww+.36,.14,.06,WH,a)
   for Y0,ww in ((100.1,.46),(103.35,.40),(106.7,.40),(109.5,.46)):facade_box(m,x,y,S(Y0),.42,(.97+7.2)/2,ww,.12,6.23,WH,a);facade_box(m,x,y,S(Y0),.46,.95,ww+.12,.18,.30,WH,a)
   facade_box(m,x,y,0,.39,.43,L,.08,.85,M['Plinth'],a);facade_box(m,x,y,0,.44,.93,L,.14,.12,WH,a)
   for Y0 in (100.1,105.0,108.8):facade_box(m,x,y,S(Y0),.44,.45,.45,.04,.42,M['Dark'],a)
   facade_box(m,x,y,0,.42,7.25,L,.10,.26,WH,a);facade_box(m,x,y,0,.56,7.52,L+.10,.40,.16,WH,a)
   town_rod(m,lp(x,y,-L/2,.76,7.58,a),lp(x,y,L/2,.76,7.58,a),.07,WH,8)
   sl=(Z[zone]['top']-HZ)/3.5
   roof_dormer(m,x,y,S(104.6),a,HZ+.4*sl,sl,.20,1.10,1.30,wall,M['Tile'],M['WhiteFrame'],False)
   for zz in (8.3,8.55):town_rod(m,lp(x,y,-L/2+.2,-.7,zz,a),lp(x,y,L/2-.2,-.7,zz,a),.02,M['Iron'],6)
  elif zone=='g19' and street63(w):
   up=[(S(Y0),4.12,1.28,1.77,0) for Y0 in (110.58,112.81,115.76,118.71,120.94)]
   gf=[(S(Y0),1.41,1.40,1.73,0) for Y0 in (110.96,112.96,118.56,120.56)]
   gate=(S(115.76),.30,2.40,2.80,0)
   bz_wall(m,w['p'],w['q'],0,HZ,up+gf+[gate],wall);boards35(m,x,y,L,a,.62,6.0,up+gf+[gate],wall,.22)
   for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas63(m,x,y,u,b,ww,hh,a)
   for u,b,ww,hh,r in gf:facade_box(m,x,y,u,.46,b+hh+.16,ww+.36,.14,.06,WH,a)
   u,b,ww,hh,r=gate
   for s in (-1,1):
    facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['Gate'],a)
    for k in range(1,14):facade_box(m,x,y,u+s*ww/4,.14,b+k*hh/14,ww/2-.06,.02,.02,M['Plinth'],a)
    facade_box(m,x,y,u+s*(ww/2+.16),.44,(b+hh)/2+.1,.26,.14,hh+.2,WH,a)
   facade_box(m,x,y,u,.46,b+hh+.28,ww+.70,.18,.36,WH,a);facade_box(m,x,y,u,.52,b+hh+.50,ww+.90,.26,.10,WH,a)
   facade_box(m,x,y,0,.39,.30,L,.08,.60,M['Plinth'],a);facade_box(m,x,y,0,.44,.63,L,.14,.08,WH,a)
   for Y0,ww in ((109.95,.30),(121.55,.34)):facade_box(m,x,y,S(Y0),.42,(.62+6.6)/2,ww,.12,5.98,WH,a)
   facade_box(m,x,y,0,.42,6.10,L,.10,.22,WH,a)
   n=int(L/.22)
   for k in range(n):facade_box(m,x,y,-L/2+(k+.5)*L/n,.46,5.94,.12,.06,.10,WH,a)
   facade_box(m,x,y,0,.52,6.55,L+.10,.34,.60,WH,a);facade_box(m,x,y,0,.62,6.88,L+.20,.52,.10,M['RedDormer'],a)
   sl=(Z[zone]['top']-HZ)/3.5
   for Y0,wd,arched in ((112.6,1.0,True),(118.9,1.0,True)):roof_dormer(m,x,y,S(Y0),a,HZ+.4*sl,sl,.25,wd,.85,M['RedDormer'],M['RedDormer'],M['WhiteFrame'],arched)
   roof_dormer(m,x,y,S(115.76),a,HZ+.4*sl,sl,.25,1.6,.90,M['RedDormer'],M['RedDormer'],M['WhiteFrame'],False)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['WhiteFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
for zone in Z:
 m=meshes[Z[zone]['mesh']]
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(3.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],M['Tile'],.40)
box(meshes['SM_Building_91970370'],43.0,104.0,.55,.75,1.0,Z['g17']['top']-.6,M['Tile'],0,M['Dark'])
box(meshes['SM_Building_91970388'],43.0,116.0,.55,.75,1.0,Z['g19']['top']-.6,M['Tile'],0,M['Dark'])
b63_finish(meshes['SM_Building_91970370'],'91970370');b63_finish(meshes['SM_Building_91970388'],'91970388')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block63_cameras=[
 sv_camera('339_Block63_Cal_Seventeen',xe63(104.85)+.355+5.26,104.85,2.60,242,20,90),
 sv_camera('340_Block63_Cal_Nineteen',xe63(115.54)+.355+5.74,115.54,2.60,242,20,90),
 ('341_Block63_Aerial',(62.0,110.0,24.0),(38.0,110.0,4.0),28),
]
print('BLOCK63_GEOMETRY',len(block63_names))
