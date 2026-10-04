"""Pass 79: green areas and the city wall.
- Lawns on the mapped village greens and the common that pass 18 left grey, and on the east
  bastions between the eastern city walls and the shore (untagged in OSM; seen as lawn with trees
  and a playground in the April 2025 Street View panorama at Östra Vallgatan).
- Sand under the three mapped playgrounds.
- Deciduous trees: the 27 mapped trees on land and an estimated planting in the parks and lawns
  (Skeppsbrovallen, Unionsparken, Floras kulle, the greens and the bastions). A tree is kept only if
  the ground under it is open (land, green, parking, street or rampart), so none stands in a house.
- The southern city wall (pass 14) without its inner 4.25 m runs: the rampart's inner side is a
  grass slope, rebuilt here, with a row of pollarded limes on the crest (Södra Vallgatan panoramas).
- The clipped hedge on the crest of the southern city wall along Skeppsbrogatan, where the April 2025
  panoramas show it about 1.3 m above the masonry (the wall itself measured 3.9-4.1 m, as modelled).

References: Google Street View April 2025 (Skeppsbrogatan, Södra Vallgatan, Östra Vallgatan), view
only; OpenStreetMap. Data: source/block79.json; see references/block79-notes.md.
"""
B79D=json.loads((R/'source/block79.json').read_text())
block79_names=[];B79={}
for old in [k for k in list(materials) if k.startswith('M_Block79_')]:bpy.data.materials.remove(materials.pop(old))
MEAN79={'Polish15LandmarkTurf':(.311,.240,.082),'TownPaintBrown':(.471,.355,.281),'TownIvory':(.841,.824,.765),'TownStone':(.648,.628,.59)}
for key,texture,target,rough,metal in [
 ('Lawn','Polish15LandmarkTurf',(.36,.46,.22),.95,0),
 ('Sand','TownIvory',(.78,.70,.55),.95,0),
 ('Kerb','TownStone',(.55,.55,.53),.90,0),
 ('Bark','TownPaintBrown',(.26,.22,.19),.95,0),
 ('Leaf','Polish15LandmarkTurf',(.22,.34,.12),.90,0),
 ('LeafLight','Polish15LandmarkTurf',(.30,.42,.15),.90,0),
 ('Hedge','Polish15LandmarkTurf',(.24,.33,.13),.95,0),
 ]:
 name='M_Block79_'+key;B79[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN79[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block79_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B79

def b79_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block79_names.append(name);return Mesh(name,category)
def b79_finish(m,bevel=True):
 obj=s21_finish(m) if bevel else m.finish();obj['detail_pass']=79;obj['reference_notes']='references/block79-notes.md';return obj
def blob79(m,c,r,ma,n=8,rings=5):
 # A closed low-poly ellipsoid for a crown cluster.
 vs=[(c[0],c[1],c[2]-r[2])]
 for j in range(1,rings):
  t=-math.pi/2+j*math.pi/rings
  for i in range(n):
   a=i*math.tau/n;vs.append((c[0]+r[0]*math.cos(t)*math.cos(a),c[1]+r[1]*math.cos(t)*math.sin(a),c[2]+r[2]*math.sin(t)))
 top=len(vs);vs.append((c[0],c[1],c[2]+r[2]))
 fs=[(0,1+(i+1)%n,1+i) for i in range(n)]
 for j in range(rings-2):fs.extend((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i) for i in range(n))
 fs.extend((1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n,top) for i in range(n))
 m.faces(vs,fs,ma,True)

# Lawns and sand, a hand's breadth above the ground, with a kerb edge.
lawn=b79_new('SM_Kvarnholmen_Green79_Lawns','Kvarnholmen/Green areas')
for row in B79D['surfaces']:
 ma=M['Lawn'] if row['kind']=='lawn' else M['Sand'];z=.035 if row['kind']=='lawn' else .03
 for t in row['triangles']:
  v=[(x,y,z) for x,y in t]
  if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
  lawn.faces(v,[(0,1,2)],ma)
 for p in row['polygons']:
  for ring in [p['outer']]+p['holes']:
   for a,b in zip(ring,ring[1:]+ring[:1]):lawn.faces([(*a,-.11),(*b,-.11),(*b,z),(*a,z)],[(0,1,2,3)],M['Kerb'])
b79_finish(lawn,False)

# The southern city wall without its inner runs (see prepare_block79.py): the pass 14 wall segment,
# with batter and broken coping, on the kept runs only.
RUB='M_Landmark_Rubble'
def wall79(m,p,q,H,W):
 x,y,L,a=sf_edge(p,q);inset=min(.48,H*.11)
 vs=[lp(x,y,u,o,z,a) for u,o,z in [(-L/2,-W/2,-.22),(L/2,-W/2,-.22),(L/2,W/2,-.22),(-L/2,W/2,-.22),(-L/2,-W/2+inset,H),(L/2,-W/2+inset,H),(L/2,W/2-inset,H),(-L/2,W/2-inset,H)]]
 m.faces(vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],RUB)
 n=max(1,round(L/.95))
 for k in range(n):facade_box(m,x,y,-L/2+(k+.5)*L/n,0,H+.075,L/n-.025,max(.35,W-2*inset+.07),.15,RUB,a)
wall=b79_new('SM_Kvarnholmen_Ringmur_Sodra','Kvarnholmen/Fortifications')
for run in B79D['sodra_walls']:
 for p,q in zip(run,run[1:]):wall79(wall,p,q,4.25,1.4)
 for x,y in run[1:-1]:wall.cylinder(x,y,-.23,.7,4.5,RUB,12,max(.18,.7-min(.48,4.25*.11)))
wobj=b79_finish(wall,False);wobj['corrected_from_pass']=14
# The grass slope on the rampart's inner side: from the rampart edge at its top (2.9 m) down to the
# park 5 m out, mitred at the corners.
gl=b79_new('SM_Kvarnholmen_Green79_Glacis','Kvarnholmen/Green areas');TOP=B79D['rampart_top'];RUN=5.0
for g in B79D['glacis']:
 pts=g['points'];sd=-g['rampart_side']
 ns=[]
 for p,q in zip(pts,pts[1:]):
  L=math.dist(p,q);ns.append((-(q[1]-p[1])/L*sd,(q[0]-p[0])/L*sd))
 off=[]
 for i,p in enumerate(pts):
  if i==0:n=ns[0]
  elif i==len(pts)-1:n=ns[-1]
  else:
   n1,n2=ns[i-1],ns[i];c=1+n1[0]*n2[0]+n1[1]*n2[1];n=((n1[0]+n2[0])/c,(n1[1]+n2[1])/c)
   k=math.hypot(*n)
   if k>2.5:n=(n[0]/k*2.5,n[1]/k*2.5)
  off.append((p[0]+n[0]*RUN,p[1]+n[1]*RUN))
 for (p,q),(po,qo) in zip(zip(pts,pts[1:]),zip(off,off[1:])):
  v=[(*p,TOP),(*q,TOP),(*qo,.05),(*po,.05)]
  nz=(v[1][0]-v[0][0])*(v[3][1]-v[0][1])-(v[1][1]-v[0][1])*(v[3][0]-v[0][0])
  gl.faces(v,[(0,1,2,3) if nz>0 else (3,2,1,0)],M['Lawn'])
b79_finish(gl,False)
# Trees: keep only those standing on open ground.
dg=bpy.context.evaluated_depsgraph_get();scene=bpy.context.scene
OPEN=('SM_Kvarnholmen_Land','SM_Kvarnholmen_Surface18','SM_Kvarnholmen_Street','SM_Kvarnholmen_Vall_','SM_Streets','SM_Ground','SM_Storgatan_Ground','SM_Kvarnholmen_Green79')
trees=b79_new('SM_Kvarnholmen_Trees79','Kvarnholmen/Vegetation');kept=[];skipped=[]
for t in B79D['trees']:
 ok,loc,nrm,idx,ob,mx=scene.ray_cast(dg,Vector((t['x'],t['y'],60)),Vector((0,0,-1)))
 if not ok or not ob.name.startswith(OPEN) or loc.z>5:skipped.append((t['source'],ob.name if ok else None));continue
 rng=random.Random(t['seed']);x,y,z0=t['x'],t['y'],max(-.1,loc.z);h=t['h'];r=t['r']
 trunk=h*.42
 trees.lathe(x,y,z0,[(.26,0),(.22,.4),(.17,trunk*.6),(.14,trunk)],M['Bark'],10)
 for k in range(4):
  a=rng.uniform(0,math.tau)+k*math.pi/2;zz=z0+trunk*rng.uniform(.8,1.0)
  town_rod(trees,(x,y,zz),(x+math.cos(a)*r*.55,y+math.sin(a)*r*.55,zz+h*.18),.07,M['Bark'],6)
 cz=z0+trunk+(h-trunk)*.52
 blob79(trees,(x,y,cz),(r*.85,r*.85,(h-trunk)*.46),M['Leaf'],10,6)
 for k in range(7):
  a=rng.uniform(0,math.tau);d=rng.uniform(.35,.7)*r;rr=r*rng.uniform(.38,.55)
  blob79(trees,(x+math.cos(a)*d,y+math.sin(a)*d,cz+rng.uniform(-.2,.35)*(h-trunk)*.5),(rr,rr,rr*.8),M['LeafLight'] if k%2 else M['Leaf'])
 kept.append(t)
# The pollarded limes along the rampart crest: short trunks, knotted heads, compact crowns about
# 3.1 m above the rampart top (measured from the Södra Vallgatan panorama).
for i,t in enumerate(B79D['limes']):
 rng=random.Random(7900+i);x,y=t['x'],t['y'];z0=TOP
 trees.lathe(x,y,z0,[(.20,0),(.17,.3),(.15,1.5),(.22,1.75),(.18,1.95)],M['Bark'],10)
 for k in range(6):
  a=k*math.tau/6+rng.uniform(-.3,.3)
  town_rod(trees,(x,y,z0+1.85),(x+math.cos(a)*.8,y+math.sin(a)*.8,z0+2.5+rng.uniform(0,.3)),.05,M['Bark'],6)
 blob79(trees,(x,y,z0+2.55),(2.1,2.1,.7),M['Leaf'],10,6)
 for k in range(4):
  a=rng.uniform(0,math.tau);blob79(trees,(x+math.cos(a)*.9,y+math.sin(a)*.9,z0+2.6+rng.uniform(-.1,.3)),(.9,.9,.55),M['LeafLight'] if k%2 else M['Leaf'])
tobj=b79_finish(trees,False);tobj['trees_kept']=len(kept);tobj['trees_skipped']=len(skipped)
print('BLOCK79_TREES',len(kept),'kept',len(skipped),'skipped',sorted(set(s[1] or '-' for s in skipped))[:8])

# The hedge on the southern wall's crest (coping top 4.40 m).
hedge=b79_new('SM_Kvarnholmen_Hedge79','Kvarnholmen/Fortifications')
for run in B79D['hedge']:
 for p,q in zip(run,run[1:]):
  x,y,L,a=sf_edge(p,q);n=max(1,round(L/2.2))
  for k in range(n):
   hh=1.30+.08*math.sin(k*1.7+p[0])
   facade_box(hedge,x,y,-L/2+(k+.5)*L/n,0,4.40+hh/2,L/n+.02,.95,hh,M['Hedge'],a)
b79_finish(hedge,False)

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block79_cameras=[
 sv_camera('390_Block79_Cal_Skeppsbrovallen',-103.17,-249.8,2.30,332,5,90),
 sv_camera('391_Block79_Cal_Skeppsbrogatan',-103.17,-249.8,2.30,282,5,90),
 sv_camera('392_Block79_Cal_SodraVallgatan',-98.2,-181.0,2.30,152,5,90),
 sv_camera('393_Block79_Cal_Bastions',394.52,2.59,2.30,62,5,90),
 ('394_Block79_Aerial_South',(-100.0,-300.0,60.0),(-100.0,-200.0,0.0),28),
 ('395_Block79_Aerial_West',(-420.0,20.0,70.0),(-330.0,120.0,0.0),28),
]
print('BLOCK79_GEOMETRY',len(block79_names))
