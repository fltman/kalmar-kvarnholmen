"""Pass 114: correction of pass 109's round drum at 50 Larmgatan (886305409).
The drum is rebuilt from scratch on the circle fitted to the OSM ring (centre (-255.55, 302.39),
r 8.81) as a regular 66-facet polygon, one facet per facade panel column (about 0.84 m):
- ten panel rows read from the photos: per storey a short mixed row, a tall glass row with a dark
  ledge at its top and an opaque panel row; three storeys, a short glass row under the top band and
  the opaque top band (the top of the coping at 10.2 m);
- glass, dark grey and silver panels in a deterministic chequer (not a cell-by-cell copy);
- thin radial fins at every panel joint, full height, transoms at every row line, the coping;
- the entrance on the Larmgatan side (south-west), a light grey door leaf under a dark transom;
- a flat roof.
References: Google Street View (two panoramas, resected on the drum's silhouette tangents), view
only. Zone: source/block114.json; see references/block114-notes.md.
"""
B114D=json.loads((R/'source/block114.json').read_text());Z=B114D['zones']
block114_names=[];B114={}
for old in [k for k in list(materials) if k.startswith('M_Block114_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('PanelLight','TownMetalGrey',(.72,.74,.75),.40,.35),('PanelDark','TownMetalGrey',(.31,.33,.36),.40,.35),
 ('Fin','TownMetalGrey',(.66,.68,.70),.40,.40),('Ledge','TownMetalGrey',(.19,.20,.21),.45,.40),
 ('Core','TownMetalGrey',(.24,.25,.26),.60,.20),('Door','TownPaintWhite',(.74,.75,.74),.55,.10),
 ('Flat','TownMetalGrey',(.30,.30,.31),.70,.20),
 ]:
 name='M_Block114_'+key;B114[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block114_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B114

def b114_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block114_names.append(name);return Mesh(name,category)
def drop_degenerate_faces114(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block114_dropped={}
def b114_finish(m,osm):
 obj=s21_finish(m);block114_dropped[obj.name]=drop_degenerate_faces114(obj)
 obj['detail_pass']=114;obj['corrects_pass']=109;obj['reference_notes']='references/block114-notes.md';obj['osm_way']=osm;return obj

# ---- 886305409 (50 Larmgatan): the round drum, rebuilt unconditionally.
D114=Z['d886'];CX114,CY114=D114['centre'];N114=D114['facets'];RA114=D114['apothem'];H114=D114['height'];T0114=D114['theta0']
ROWS114=[tuple(r) for r in D114['rows']];STEP114=2*math.pi/N114;RC114=RA114/math.cos(STEP114/2);LF114=2*RC114*math.sin(STEP114/2)
def at114(theta,r,z=0.0):return (CX114+r*math.cos(theta),CY114+r*math.sin(theta),z)
def tbox114(m,theta,r,z0,z1,w,d,ma):
 # A box centred on the facet direction theta: w along the facet, d radial (centred on r).
 x,y,_=at114(theta,r);m.box((x,y,(z0+z1)/2),(w,d,z1-z0),ma,theta+math.pi/2)
def cell114(k,r,kind):
 # Deterministic chequer: tall rows mostly glass, short rows mixed, opaque rows light/dark.
 x=(k*73+r*151+(k*k%17)*29+(k//3)*11)%100
 if kind=='t':return GLAZE if x<64 else M['PanelDark'] if x<81 else M['PanelLight']
 if kind=='s':return GLAZE if x<36 else M['PanelDark'] if x<64 else M['PanelLight']
 return (M['PanelDark'] if (k+r)%2==0 else M['PanelLight']) if x>=14 else (M['PanelLight'] if (k+r)%2==0 else M['PanelDark'])
m=b114_new(D114['mesh'],'Kvarnholmen/Larmgatan')
# Core: the dark wall behind the panels (seen in the mullion gaps) with the flat roof on top.
ZR114=H114-.24;core=[at114(T0114+k*STEP114,RC114-.10)[:2] for k in range(N114)]
m.faces([(x,y,0.0) for x,y in core]+[(x,y,ZR114) for x,y in core],[(i,(i+1)%N114,(i+1)%N114+N114,i+N114) for i in range(N114)]+[tuple(range(N114-1,-1,-1))],M['Core'])
m.faces([(x,y,ZR114) for x,y in core],[tuple(range(N114))],M['Flat'])
DOOR114=math.radians(D114['door_angle_deg'])
def ang_diff114(a,b):return abs((a-b+math.pi)%(2*math.pi)-math.pi)
kdoor=min(range(N114),key=lambda k:ang_diff114(T0114+(k+.5)*STEP114,DOOR114))
for k in range(N114):
 th=T0114+(k+.5)*STEP114;w=LF114-.07
 for r,(z0,z1,kind) in enumerate(ROWS114):
  if k==kdoor and r<2:continue
  tbox114(m,th,RA114+.03,z0+.025,z1-.025,w,.06,cell114(k,r,kind))
 if k==kdoor:
  tbox114(m,th,RA114+.03,0.0,2.05,w,.06,M['Door']);tbox114(m,th,RA114+.03,2.05,2.275,w,.06,M['Ledge'])
 # Transoms at every row line, a dark ledge on top of each tall glass row, the coping.
 for z in sorted({z for z0,z1,_ in ROWS114 for z in (z0,z1)}):
  if z<.01:continue
  tbox114(m,th,RA114+.05,z-.025,z+.025,LF114,.10,M['Fin'])
 for z0,z1,kind in ROWS114:
  if kind=='t':tbox114(m,th,RA114+.11,z1-.045,z1+.045,LF114,.22,M['Ledge'])
 tbox114(m,th,RA114+.14,H114-.12,H114,LF114+.04,.36,M['Fin'])
 tbox114(m,th,RA114+.04,0.0,.06,LF114,.08,M['Ledge'])
# Thin radial fins at every panel joint, full height (radial, not splayed).
for k in range(N114):
 ph=T0114+k*STEP114;x,y,_=at114(ph,RC114+.15);m.box((x,y,(H114-.12)/2),(.30,.05,H114-.12),M['Fin'],ph)
b114_finish(m,'886305409')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block114_cameras=[
 sv_camera('575_Block114_Cal_Drum',-277.02,292.22,1.82,25,15,90),
 sv_camera('576_Block114_Cal_DrumClose',-269.11,308.38,1.93,86,15,90),
 sv_camera('577_Block114_Cal_DrumEdge',-277.02,292.22,1.82,330,12,90),
 ('578_Block114_Aerial',(-290.0,270.0,40.0),(-255.6,302.4,4.0),28),
]
print('BLOCK114_GEOMETRY',len(block114_names),'dropped',block114_dropped)
