"""Pass 65: the district volumes 91846981, 91846966 and 91846970 on the north side of Fiskaregatan,
three matching two-storey houses of the 1940s:
- beige roughcast with salmon corner strips and a salmon band over the plinth;
- two axes of white-framed casements in white surrounds on each storey;
- a grey-green plinth with a barred cellar window under each ground window;
- a profiled cornice and a hipped tile roof.
The rear wings keep a plain rhythm.

References: Google Street View April 2025 (four close panoramas on Fiskaregatan, each placed on a
corner of its house and on its base row), view only. Zones: source/block65.json; see
references/block65-notes.md.
"""
B65D=json.loads((R/'source/block65.json').read_text());Z=B65D['zones']
block65_names=[];B65={}
for old in [k for k in list(materials) if k.startswith('M_Block65_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Beige','TownIvory',(.74,.62,.48),.95,0),
 ('Salmon','TownIvory',(.90,.72,.62),.88,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownIvory',(.52,.58,.52),.90,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Cornice','TownIvory',(.80,.80,.78),.85,0),
 ('Tile','TownTileRed',(.58,.32,.24),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block65_'+key;B65[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block65_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B65;WH=M['White'];BG=M['Beige']

def b65_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block65_names.append(name);return Mesh(name,category)
def b65_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=65;obj['reference_notes']='references/block65-notes.md';obj['osm_way']=osm;return obj
def cas65(m,x,y,u,b,w,h,a,o=.16):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['WhiteFrame'],a)
 facade_box(m,x,y,u,.44,b-.04,w+.16,.20,.05,WH,a)
AXES={'f81':(36.7,41.0),'f66':(9.3,13.3),'f70':(-17.36,-12.82)}
OSM={'f81':'91846981','f66':'91846966','f70':'91846970'}
meshes={}
for zone in Z:
 m=meshes[zone]=b65_new(Z[zone]['mesh'],'Kvarnholmen/Fiskaregatan');H=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if w['kind']=='outer' and oy<-.9 and max(w['p'][1],w['q'][1])<146:
   (x0,y0),(x1,y1)=w['p'],w['q']
   S=lambda X:U(w,X,y0+(X-x0)*(y1-y0)/(x1-x0))
   up=[(S(X0),5.25,1.40,1.62,0) for X0 in AXES[zone]];gf=[(S(X0),2.20,1.62,1.65,0) for X0 in AXES[zone]]
   cel=[(S(X0),.28,1.05,.62,0) for X0 in AXES[zone]]
   bz_wall(m,w['p'],w['q'],0,H,up+gf+cel,BG)
   for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);cas65(m,x,y,u,b,ww,hh,a)
   for u,b,ww,hh,r in cel:
    facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a)
    for k in range(1,8):facade_box(m,x,y,u-ww/2+k*ww/8,.46,b+hh/2,.02,.03,hh,M['WhiteFrame'],a)
    for zz in (b+.02,b+hh-.02):facade_box(m,x,y,u,.46,zz,ww+.06,.04,.05,M['WhiteFrame'],a)
    facade_box(m,x,y,u,.46,b-.05,ww+.20,.20,.10,WH,a)
   facade_box(m,x,y,0,.39,.575,L,.08,1.15,M['Plinth'],a);facade_box(m,x,y,0,.40,1.19,L,.10,.08,M['Salmon'],a)
   for s in (-1,1):facade_box(m,x,y,s*(L/2-.08),.40,(1.15+7.0)/2,.16,.08,5.85,M['Salmon'],a)
   facade_box(m,x,y,0,.42,7.08,L+.10,.12,.16,M['Cornice'],a);facade_box(m,x,y,0,.54,7.30,L+.20,.36,.28,M['Cornice'],a);facade_box(m,x,y,0,.68,7.52,L+.30,.60,.14,M['Cornice'],a)
  else:
   if w['kind']=='outer':plain(m,w,H,BG,M['WhiteFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],BG)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,H,min(4.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-H,M['Tile'],.55)
 b65_finish(m,OSM[zone])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block65_cameras=[
 sv_camera('345_Block65_Cal_East',46.94,145.0-.355-4.98,2.30,332,15,90),
 sv_camera('346_Block65_Cal_Middle',14.46,145.27-.355-4.19,2.30,332,15,90),
 sv_camera('347_Block65_Cal_West',-14.01,145.30-.355-4.02,2.30,332,15,90),
 ('348_Block65_Aerial',(12.0,125.0,34.0),(12.0,155.0,4.0),28),
]
print('BLOCK65_GEOMETRY',len(block65_names))
