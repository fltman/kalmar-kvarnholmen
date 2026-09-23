"""Pass 27: Kalmar slott on Slottsholmen. The Renaissance castle of Gustav Vasa and his sons in the
silhouette Helgo Zettervall restored in 1885-91: four ranges round the courtyard with the well
house of 1578, the square gate tower Kuretornet with its copper bell roof, lantern and gilded
crown, four round corner towers with copper caps, the chapel's roof turret and the stepped gables of
the south-east front. Around it the dry moat, the earth ramparts with guns, the curtain walls, the
four low round postejer, the north-west lower wall with its berm and gate, the timber bridge with
its drawbridge, the ravelin with the castellan's house and the islets of Slottsfjärden.
Outlines: source/castle27.json (OpenStreetMap). Heights: Google Street View 2014, measured by
inverting the panorama camera, and Zettervall's 1883 west elevation; see references/castle27-notes.md.
"""
import ast,random
from mathutils.geometry import tessellate_polygon
C27=json.loads((R/'source/castle27.json').read_text());HL=C27['levels_h'];CA=C27['castle']
def zh(h):return round(-1.33+h,4)
tree=ast.parse((R/'scripts/build_baronen23.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'lin','ring_offset','bz_wall','inset_roof','roof_dormer','box','street_view_camera'}]
exec(compile(tree,'baronen23_helpers','exec'))
tree=ast.parse((R/'scripts/build_station24.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'poly_lathe'}]
exec(compile(tree,'station24_helpers','exec'))
castle27_names=[];K={}
MEAN={'TownIvory':(.841,.824,.765),'TownLime':(.777,.777,.727),'LandmarkAshlar':(.645,.621,.547),'ChurchCutStone':(.687,.676,.638),
 'Polish15LandmarkRubble':(.636,.572,.480),'Baronen23Brick':(.58,.397,.317),'TownStone':(.648,.628,.59),'ChurchCopperFine':(.318,.489,.432),
 'TownMetalGrey':(.371,.421,.397),'TownPaintGreen':(.311,.401,.347),'TownMetalRed':(.564,.299,.233),'TownPaintBrown':(.471,.355,.281),
 'ChurchGilding':(.868,.758,.507),'Polish15PolishBridgeWood':(.461,.410,.327),'Pass18Grass':(.355,.512,.198),'Cobbles':(.466,.461,.443),
 'SodraRedWood':(.492,.167,.155),'TownTileRed':(.602,.352,.236),'LandmarkRubble':(.489,.490,.460),'ChurchAshlar':(.738,.721,.661),
 'Polish15LandmarkTurf':(.311,.240,.082)}
UVS={'Revet':1.6,'Curtain':1.3,'LowWall':1.0}
for old in [k for k in list(materials) if k.startswith('M_Castle27_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Render','TownIvory',(.82,.70,.58),.88,0),        # sand-ochre outer render (Street View 2014, photographs 2019-22)
 ('RenderTower','TownIvory',(.80,.66,.55),.88,0),
 ('Court','TownLime',(.87,.83,.73),.86,0),          # courtyard render
 ('CourtBlock','ChurchAshlar',(.88,.85,.76),.86,0),  # painted rustication on the courtyard fronts
 ('Trim','ChurchCutStone',(.76,.74,.68),.80,0),
 ('KureStone','Polish15LandmarkRubble',(.62,.57,.51),.88,0),
 ('Rubble','Polish15LandmarkRubble',(.66,.63,.57),.88,0),
 ('Revet','Polish15LandmarkRubble',(.58,.56,.52),.88,0),  # small stones in courses (north-west revetment)
 ('Curtain','LandmarkRubble',(.72,.69,.62),.88,0),
 ('LowWall','Polish15LandmarkRubble',(.63,.58,.49),.90,0),
 ('Brick','Baronen23Brick',(.57,.31,.23),.88,0),
 ('Coping','TownStone',(.56,.56,.54),.85,0),
 ('Gate','ChurchAshlar',(.56,.55,.52),.86,0),
 ('Copper','ChurchCopperFine',(.51,.68,.62),.55,.30),
 ('CopperDark','ChurchCopperFine',(.24,.34,.31),.55,.30),
 ('Roof','TownMetalGrey',(.23,.25,.26),.55,.35),
 ('PostejRoof','TownMetalGrey',(.63,.65,.66),.45,.50),
 ('Chimney','TownIvory',(.86,.62,.52),.88,0),
 ('Frame','TownPaintGreen',(.43,.46,.42),.60,0),
 ('FrameRed','TownMetalRed',(.55,.22,.16),.60,0),
 ('Door','TownPaintBrown',(.37,.26,.17),.60,0),
 ('Dark','TownMetalGrey',(.04,.045,.05),.45,.20),
 ('Gold','ChurchGilding',(.80,.62,.25),.30,.90),
 ('Iron','TownMetalGrey',(.07,.07,.075),.50,.60),
 ('Timber','Polish15PolishBridgeWood',(.42,.36,.29),.85,0),
 ('TimberDark','Polish15PolishBridgeWood',(.20,.16,.12),.85,0),
 ('Grass','Polish15LandmarkTurf',(.36,.46,.22),.95,0),
 ('GrassDry','Polish15LandmarkTurf',(.52,.52,.34),.95,0),
 ('Reed','Polish15LandmarkTurf',(.40,.47,.24),.95,0),
 ('Gravel','TownStone',(.64,.58,.49),.92,0),
 ('Cobbles','Cobbles',(.56,.53,.48),.85,0),
 ('Boulder','Polish15LandmarkRubble',(.53,.51,.47),.90,0),
 ('WellStone','ChurchCutStone',(.55,.52,.47),.85,0),
 ('Villa','TownIvory',(.86,.83,.73),.88,0),
 ('VillaShingle','SodraRedWood',(.52,.26,.19),.80,0),
 ('VillaTile','TownTileRed',(.56,.29,.20),.80,0),
 ]:
 name='M_Castle27_'+key;K[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['castle27_target_srgb']=list(target)
 if key in UVS:
  specs[name]['uv_scale']=UVS[key]
  for nd in materials[name].node_tree.nodes:
   if nd.bl_idname=='ShaderNodeVectorMath' and nd.operation=='SCALE':nd.inputs[3].default_value=UVS[key]
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
SIGN=K['Dark'];TRIM=K['Trim'];GL=GLAZE
rng=random.Random(27)

def c27_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 castle27_names.append(name);return Mesh(name,category)
def c27_finish(m,bevel=True):
 obj=s21_finish(m) if bevel else m.finish();obj['detail_pass']=27;obj['reference_notes']='references/castle27-notes.md'
 # Arch spandrels leave slivers of a few mm2 whose projected UVs collapse, so no tangent frame
 # can be derived at export. Triangulate here and drop those thin slivers (under 20 mm2 and
 # thinner than 1:100); the bevel's own corner and strip faces are much fatter and stay.
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces))
 def sliver(f):
  a=f.calc_area()
  if a<1e-7:return True
  return a<2e-5 and a/max(e.calc_length() for e in f.edges)**2<.01
 bad=[f for f in bm.faces if sliver(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
 bm.to_mesh(obj.data);bm.free();obj.data.update();obj['slivers_removed']=len(bad);return obj
# ---------------------------------------------------------------- geometry helpers
def surf(m,piece,z,ma):
 # Flat polygon with holes; independent upward triangles like district_surface.
 rings=[piece['outer']]+piece.get('holes',[]);flatv=[(x,y) for r in rings for x,y in r]
 for t in tessellate_polygon([[Vector((x,y,0)) for x,y in r] for r in rings]):
  v=[(flatv[i][0],flatv[i][1],z) for i in t]
  if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
  m.faces(v,[(0,1,2)],ma)
def normals(pts,closed):
 # Mitred outward (right-hand) normals of a polyline.
 n=len(pts);out=[]
 for i in range(n):
  a=pts[i-1] if (closed or i>0) else None;b=pts[i];c=pts[(i+1)%n] if (closed or i<n-1) else None
  ds=[]
  for p,q in ((a,b),(b,c)):
   if p is None or q is None:continue
   L=math.dist(p,q);ds.append(((q[1]-p[1])/L,-(q[0]-p[0])/L))
  nx=sum(d[0] for d in ds);ny=sum(d[1] for d in ds);k=math.hypot(nx,ny)
  if len(ds)==2:
   dot=ds[0][0]*ds[1][0]+ds[0][1]*ds[1][1];s=1/max(.35,math.sqrt((1+dot)/2))
  else:s=1
  out.append((nx/k*s,ny/k*s))
 return out
def battered(m,pts,z0,z1,back,batter,ma,closed=False,cap=None,cap_w=.5,cap_h=.18):
 # Solid wall along a polyline: outer face leaning back by 'batter' m per m, rear face 'back' behind.
 ns=normals(pts,closed);n=len(pts);lean=batter*(z1-z0)
 ob=[(p[0]+q[0]*lean,p[1]+q[1]*lean,z0) for p,q in zip(pts,ns)];ot=[(p[0],p[1],z1) for p in pts]
 ib=[(p[0]-q[0]*back,p[1]-q[1]*back,z0) for p,q in zip(pts,ns)];it=[(p[0]-q[0]*back,p[1]-q[1]*back,z1) for p,q in zip(pts,ns)]
 segs=range(n) if closed else range(n-1)
 for i in segs:
  j=(i+1)%n
  m.faces([ob[i],ob[j],ot[j],ot[i]],[(0,1,2,3)],ma);m.faces([ot[i],ot[j],it[j],it[i]],[(0,1,2,3)],ma);m.faces([ib[j],ib[i],it[i],it[j]],[(0,1,2,3)],ma)
 if not closed:
  for i in (0,n-1):m.faces([ob[i],ib[i],it[i],ot[i]],[(0,1,2,3)],ma)
 if cap:
  for i in segs:
   j=(i+1)%n;q=[(pts[k][0]+ns[k][0]*cap_w*.4,pts[k][1]+ns[k][1]*cap_w*.4) for k in (i,j)];r=[(pts[k][0]-ns[k][0]*cap_w*.6,pts[k][1]-ns[k][1]*cap_w*.6) for k in (i,j)]
   v=[(*q[0],z1),(*q[1],z1),(*r[1],z1),(*r[0],z1),(*q[0],z1+cap_h),(*q[1],z1+cap_h),(*r[1],z1+cap_h),(*r[0],z1+cap_h)]
   m.faces(v,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],cap)
def cordon(m,pts,z,r,ma,out=.05):
 ns=normals(pts,False);town_path(m,[(p[0]+q[0]*out,p[1]+q[1]*out,z) for p,q in zip(pts,ns)],r,ma)
def boulder(m,x,y,z,r,ma,flat=.62):
 # Icosahedron with a per-vertex radial jitter; one deterministic stream for all rocks.
 t=(1+math.sqrt(5))/2;vs=[(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
 fs=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
 k=r/math.sqrt(1+t*t);rot=rng.uniform(0,math.tau);co,si=math.cos(rot),math.sin(rot);out=[]
 for a,b,c in vs:
  j=rng.uniform(.75,1.2);a,b,c=a*k*j,b*k*j,c*k*j*flat
  out.append((x+a*co-b*si,y+a*si+b*co,z+c))
 m.faces(out,fs,ma)
def poly_edges(poly,closed=True):return list(zip(poly,poly[1:]+poly[:1])) if closed else list(zip(poly,poly[1:]))
def seg_len(p,q):return math.dist(p,q)
def point_in(p,poly):
 x,y=p;c=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-12)+xi:c=not c
  j=i
 return c
Z0=zh(HL['foot']);ZC=zh(HL['courtyard']);ZE=zh(HL['eaves']);ZR=zh(HL['rampart']);ZW=zh(0.0)

# ================================================================= ground: island, ravelin, islets
m=c27_new('SM_Castle27_Ground','Kalmar slott/Ground')
for q in C27['terreplein']:surf(m,q,ZR,K['Grass'])
for q in C27['dry_moat']:surf(m,q,Z0,K['Grass'])
for sl in C27['slopes']:
 o_,i_=sl['outer'],sl['inner']
 for k in range(len(o_)-1):m.faces([(*o_[k],zh(HL['curtain_top'])+.18),(*o_[k+1],zh(HL['curtain_top'])+.18),(*i_[k+1],ZR),(*i_[k],ZR)],[(0,1,2,3)],K['Grass'])
for side,qs in C27['berms'].items():
 for q in qs:surf(m,q,zh(HL['berm_low']),K['GrassDry'])
for q in C27['nw_walk']:surf(m,q,zh(HL['berm_high']),K['Coping'])
for q in C27['nw_shore']:surf(m,q,zh(.45),K['GrassDry'])
for zone in C27['path_surfaces']:
 for q in zone['pieces']:surf(m,q,zh(zone['h'])+.025,K['Gravel'])
surf(m,{'outer':CA['court'],'holes':[]},ZC,K['Cobbles'])
# The shore: every berm edge drops to the water as a grassed bank under the riprap.
coast=C27['island'][0]['outer'];inset=ring_offset(coast,-2.2);LW=[tuple(p) for p in C27['lower_wall']]
def dseg(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l2=dx*dx+dy*dy or 1;t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/l2));return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
for i in range(len(coast)):
 j=(i+1)%len(coast);mid=((coast[i][0]+coast[j][0])/2,(coast[i][1]+coast[j][1])/2)
 if any(point_in(mid,p['polygon']) for p in C27['postejer'].values()):continue
 top=.45 if dseg(mid,LW[0],LW[-1])<6.0 else HL['berm_low']
 m.faces([(*coast[i],zh(-.6)),(*coast[j],zh(-.6)),(*inset[j],zh(top)),(*inset[i],zh(top))],[(0,1,2,3)],K['GrassDry'])
c27_finish(m)

# ================================================================= fortification walls
m=c27_new('SM_Castle27_Walls','Kalmar slott/Fortifications')
gate_o=tuple(C27['gate']['outer']);gate_i=tuple(C27['gate']['inner'])
for cur in C27['curtains']:
 for run in cur['runs']:
  pts=[tuple(p) for p in run]
  if cur['side']=='NW':
   # Revetment: split at the gate, whose ashlar block stands vertical and slightly proud.
   L=[0.0]
   for p,q in zip(pts,pts[1:]):L.append(L[-1]+math.dist(p,q))
   def at(d):
    for k in range(len(pts)-1):
     if L[k]<=d<=L[k+1]:t=(d-L[k])/(L[k+1]-L[k]);return (pts[k][0]+(pts[k+1][0]-pts[k][0])*t,pts[k][1]+(pts[k+1][1]-pts[k][1])*t)
    return pts[-1]
   dg=min(range(int(L[-1])),key=lambda d:math.dist(at(d),gate_o));w=3.3
   left=[p for p,l in zip(pts,L) if l<dg-w]+[at(dg-w)];right=[at(dg+w)]+[p for p,l in zip(pts,L) if l>dg+w]
   for part in (left,right):
    if len(part)>1:battered(m,part,zh(HL['berm_high'])-.3,ZR+.05,2.0,cur['batter'],K['Revet'],cap=K['Coping'],cap_w=.9,cap_h=.2)
    if len(part)>1:cordon(m,part,ZR-.45,.2,K['Revet'],.02)
   a,b=at(dg-w),at(dg+w);x,y,Lg,ang=sf_edge(a,b);ZB=zh(HL['berm_high']);F=cur['batter']*(ZR+.05-ZB)+.25
   ug=((gate_o[0]-x)*math.cos(ang)+(gate_o[1]-y)*math.sin(ang))
   # Ashlar gate block, vertical and standing proud of the battered foot.
   bz_wall(m,a,b,ZB-.3,ZR+.05,[(ug,ZB,3.4,3.4,1.7)],K['Gate'],-1.8,F)
   facade_box(m,x,y,0,F+.02,ZR+.16,Lg+.3,.4,.22,K['Coping'],ang)
   p18_arch(m,*lp(x,y,ug,0,0,ang)[:2],ZB+3.4,3.4,1.7,.45,F+.07,ang,K['Trim'])
   for s in (-1,1):facade_box(m,x,y,ug+s*1.95,F+.07,ZB+1.7,.5,.16,3.4,K['Trim'],ang)
   # Coat-of-arms tablet above the arch (relief not modelled)
   facade_box(m,x,y,ug,F+.11,ZB+6.1,2.4,.22,2.0,K['Trim'],ang);facade_box(m,x,y,ug,F+.23,ZB+6.1,1.9,.06,1.5,K['KureStone'],ang)
  else:
   battered(m,pts,zh(HL['berm_low'])-.4,zh(HL['curtain_top']),2.0,cur['batter'],K['Curtain'],cap=K['Coping'],cap_w=.9,cap_h=.18)
# North-west lower wall: boulder base, coursed stone above, brick-arched casemate openings.
lw=[tuple(p) for p in C27['lower_wall']];x,y,Lw,ang=sf_edge(lw[0],lw[-1])
holes=[(-Lw/2+(k+.5)*Lw/14,zh(3.0),.95,.75,.45) for k in range(14) if abs(-Lw/2+(k+.5)*Lw/14-((gate_o[0]-x)*math.cos(ang)+(gate_o[1]-y)*math.sin(ang)))>3.5]
bz_wall(m,lw[0],lw[-1],zh(-.6),zh(HL['berm_high']),holes,K['LowWall'],-1.2,.35)
for u,b,w,h,r in holes:
 p18_arch(m,*lp(x,y,u,0,0,ang)[:2],b+h,w,r,.12,.40,ang,K['Brick'])
 facade_box(m,x,y,u,-.9,b+h/2,w,.1,h+r,SIGN,ang)
mb=[tuple(v) for v in C27['bridges']['main']['points']]
def cross_u(p0,p1,x,y,ang):
 # along-wall coordinate where the segment p0-p1 crosses the wall line (None if it does not)
 d0=(p0[0]-x)*math.sin(ang)-(p0[1]-y)*math.cos(ang);d1=(p1[0]-x)*math.sin(ang)-(p1[1]-y)*math.cos(ang)
 if d0*d1>0:return None
 t_=d0/(d0-d1);px,py=p0[0]+(p1[0]-p0[0])*t_,p0[1]+(p1[1]-p0[1])*t_;return (px-x)*math.cos(ang)+(py-y)*math.sin(ang)
ub=next((u for u in (cross_u(p0,p1,x,y,ang) for p0,p1 in zip(mb,mb[1:])) if u is not None),None)
for lo,hi in ([(-Lw/2,ub-2.2),(ub+2.2,Lw/2)] if ub is not None else [(-Lw/2,Lw/2)]):
 if hi-lo>.3:facade_box(m,x,y,(lo+hi)/2,.30,zh(HL['berm_high'])+.08,hi-lo,.9,.16,K['Coping'],ang)
# Dry-moat counterscarp: vertical face toward the moat, a coping level with the rampart.
ringcw=[tuple(p) for p in C27['ring']][::-1]
merged=[ringcw[0]]
for p in ringcw[1:]+[ringcw[0]]:
 if len(merged)>=2:
  a,b=merged[-2],merged[-1];d1=math.atan2(b[1]-a[1],b[0]-a[0]);d2=math.atan2(p[1]-b[1],p[0]-b[0])
  if abs((d2-d1+math.pi)%math.tau-math.pi)<math.radians(4):merged[-1]=p;continue
 merged.append(p)
merged=merged[:-1] if math.dist(merged[0],merged[-1])<.01 else merged
for p,q in poly_edges(merged):
 x,y,L,ang=sf_edge(p,q)
 if L<.3:continue
 hs=[];tex=tuple(C27['tunnel'][-1])
 for pt,w_,h_,r_ in ((tex,3.2,3.1,1.6),(gate_i,1.6,2.4,.8)):
  u=(pt[0]-x)*math.cos(ang)+(pt[1]-y)*math.sin(ang);v=(pt[0]-x)*math.sin(ang)-(pt[1]-y)*math.cos(ang)
  if abs(u)<L/2-w_/2-.2 and abs(v)<1.0:hs.append((u,Z0,w_,h_,r_))
 bz_wall(m,p,q,Z0-.2,ZR,hs,K['Revet'],-.9,0)
 pa=tuple(C27['passage'][0]);pe=[tuple(v) for v in C27['passage']];pmid=min(pe,key=lambda v:(v[0]-x)*math.sin(ang)-(v[1]-y)*math.cos(ang))
 cut=[(v[0]-x)*math.cos(ang)+(v[1]-y)*math.sin(ang) for v in pe if abs((v[0]-x)*math.sin(ang)-(v[1]-y)*math.cos(ang))<1.5]
 spans=[(-L/2-.1,L/2+.1)]
 if cut and max(cut)>-L/2 and min(cut)<L/2:spans=[(-L/2-.1,min(cut)-.2),(max(cut)+.2,L/2+.1)]
 for lo,hi in spans:
  if hi-lo>.3:facade_box(m,x,y,(lo+hi)/2,-.35,ZR+.1,hi-lo,1.1,.2,K['Coping'],ang)
 for uu,b,w,h,r in hs:
  p18_arch(m,*lp(x,y,uu,0,0,ang)[:2],b+h,w,r,.4,.12,ang,K['Trim'])
  if w<2:facade_box(m,x,y,uu,-.45,b+h/2,w,.08,h,K['Door'],ang)   # the door to the stair up the rampart (stair not modelled)
# The gate tunnel under the rampart, along its OSM line from the gate to the counterscarp.
TL=[tuple(v) for v in C27['tunnel']];tn=normals(TL,False)
prof=[(-1.6,Z0-.02),(-1.6,Z0+3.1)]+[(-1.6*math.cos(k*math.pi/10),Z0+3.1+1.6*math.sin(k*math.pi/10)) for k in range(1,10)]+[(1.6,Z0+3.1),(1.6,Z0-.02)]
secs=[[(p_[0]+n_[0]*c,p_[1]+n_[1]*c,z) for c,z in prof] for p_,n_ in zip(TL,tn)]
for s0,s1 in zip(secs,secs[1:]):
 for k in range(len(prof)-1):m.faces([s0[k],s0[k+1],s1[k+1],s1[k]],[(0,1,2,3)],K['Revet'])
 m.faces([s0[0],s0[-1],s1[-1],s1[0]],[(0,1,2,3)],K['Cobbles'])
# Walled gate building on the dry-moat floor beside the entrance walk (OSM: walls 5 m high); the
# dry-moat walk passes through it by a vaulted passage (OSM building_passage).
ps=[tuple(p) for p in C27['passage']]
def merge_edges(poly,tol=15):
 out=[poly[0]]
 for v in poly[1:]+[poly[0]]:
  if len(out)>=2:
   a_,b_=out[-2],out[-1];d1=math.atan2(b_[1]-a_[1],b_[0]-a_[0]);d2=math.atan2(v[1]-b_[1],v[0]-b_[0])
   if abs((d2-d1+math.pi)%math.tau-math.pi)<math.radians(tol):out[-1]=v;continue
  out.append(v)
 return out[:-1] if math.dist(out[0],out[-1])<.01 else out
pm=merge_edges(ps);CD=[tuple(v) for v in C27['corridor_doors']];TX=tuple(C27['tunnel'][-1]);CDOOR=tuple(C27['castle_door'])
for p,q in poly_edges(pm):
 x,y,Lq,ang=sf_edge(p,q);hs=[]
 for d_ in CD:
  u_=(d_[0]-x)*math.cos(ang)+(d_[1]-y)*math.sin(ang);v_=(d_[0]-x)*math.sin(ang)-(d_[1]-y)*math.cos(ang)
  if abs(v_)<1.2 and abs(u_)<Lq/2-1.2:hs.append((u_,Z0,1.8,2.5,.7))
 bz_wall(m,p,q,Z0-.2,Z0+5.0,hs,K['KureStone'],-.5,0)
 facade_box(m,x,y,0,-.2,Z0+5.08,Lq+.2,.7,.16,K['Coping'],ang)
 for uu,b_,w_,h_,r_ in hs:p18_arch(m,*lp(x,y,uu,0,0,ang)[:2],b_+h_,w_,r_,.25,.05,ang,K['Trim'])
m.faces([(p_[0],p_[1],Z0+5.0) for p_ in pm],[tuple(range(len(pm)))],K['Coping'])
x,y,Lp_,ang=sf_edge(CD[0],CD[1])
for s in (-1,1):facade_box(m,x,y,0,s*1.0,Z0+1.6,Lp_+.6,.2,3.2,K['KureStone'],ang)
facade_box(m,x,y,0,0,Z0+3.3,Lp_+.6,2.2,.2,K['KureStone'],ang);facade_box(m,x,y,0,0,Z0+.01,Lp_+.6,2.0,.02,K['Cobbles'],ang)
# Stone bridges across the dry moat to the north-east range and the south tower's landing.
for key,z in (('north_east',ZR-.3),('south',ZR-.2)):
 p,q=[tuple(v) for v in C27['bridges'][key]['points']][:2];x,y,Lb,ang=sf_edge(p,q);wb=C27['bridges'][key]['width']
 facade_box(m,x,y,0,0,z-.35,Lb+1.2,wb,.7,K['Rubble'],ang)
 for s in (-1,1):facade_box(m,x,y,0,s*(wb/2-.2),z+.5,Lb+1.2,.35,1.0,K['Rubble'],ang)
ew=[tuple(p) for p in C27['walls']['east_corner']];eg=tuple(C27['walls']['east_gate'])
def toward(a,b_,d):L_=math.dist(a,b_);return (a[0]+(b_[0]-a[0])*d/L_,a[1]+(b_[1]-a[1])*d/L_)
for part in ([ew[0],toward(eg,ew[0],1.4)],[toward(eg,ew[-1],1.4),ew[-1]]):battered(m,part,Z0-.2,ZR-1.0,.8,0,K['Revet'],cap=K['Coping'],cap_w=1.0)
for side_ in (ew[0],ew[-1]):q_=toward(eg,side_,1.4);m.box((q_[0],q_[1],Z0+1.6),(.5,.5,3.2),K['Trim'])
c27_finish(m)

# ================================================================= the four postejer
m=c27_new('SM_Castle27_Postejer','Kalmar slott/Fortifications')
ZPT=zh(HL['postej_top'])
def opening(m,px,py,z,w,h,ang,arched=True,bars=0):
 facade_box(m,px,py,0,.03,z+h/2,w,.08,h,SIGN,ang)
 if arched:p18_arch(m,px,py,z+h,w,w*.35,.14,.05,ang,K['Rubble'])
 for k in range(bars):town_rod(m,lp(px,py,-w/2+w*(k+1)/(bars+1),.06,z,ang),lp(px,py,-w/2+w*(k+1)/(bars+1),.06,z+h,ang),.018,K['Iron'],6)
for key,p in C27['postejer'].items():
 cx,cy=p['centre'];r=p['radius'];zb=zh(-.6)
 if p['round']:
  m.cylinder(cx,cy,zb,r+.35,ZPT-zb,K['Rubble'],56,r)
  m.lathe(cx,cy,ZPT,[(r+.5,0),(r+.5,.14),(r*.55,1.35),(.35,2.35),(.12,2.42)],K['PostejRoof'],56)
  for k in range(28):
   t=k*math.tau/28;town_rod(m,(cx+(r+.5)*math.cos(t),cy+(r+.5)*math.sin(t),ZPT+.16),(cx+.5*math.cos(t),cy+.5*math.sin(t),ZPT+2.34),.028,K['PostejRoof'],4)
  rad=lambda z:r+.35-.35*(z-zb)/(ZPT-zb)
  for zz,w,h,n,arched,bars,off in ((zh(3.2),.7,.8,9,True,0,0),(zh(6.6),1.0,1.1,11,True,3,.13),(zh(11.2),1.1,.7,13,False,4,.27)):
   for k in range(n):
    t=(k+off)*math.tau/n;rr=rad(zz)+.01;px,py=cx+rr*math.cos(t),cy+rr*math.sin(t);opening(m,px,py,zz,w,h,t+math.pi/2,arched,bars)
 else:
  poly=[tuple(v) for v in p['polygon']]
  battered(m,poly,zb,ZPT,1.4,.03,K['Rubble'],closed=True)
  inset_roof(m,poly,ZPT,3.0,1.4,K['PostejRoof'],.5)
  for a_,b_ in poly_edges(poly):
   x,y,L,ang=sf_edge(a_,b_)
   if L<3:continue
   n=max(1,round(L/4.5))
   for k in range(n):
    u=-L/2+(k+.5)*L/n
    for zz,w,h,arched,bars in ((zh(6.6),1.0,1.1,True,3),(zh(11.2),1.1,.7,False,4)):opening(m,*lp(x,y,u,.02,0,ang)[:2],zz,w,h,ang,arched,bars)
  # Square stair tower on the moat side (photographs 2022).
  near=min(poly,key=lambda v:math.dist(v,(-860.0,-212.5)));i=poly.index(near);a_,b_=poly[i-1],poly[(i+1)%len(poly)]
  L=math.dist(a_,b_);nx,ny=(b_[1]-a_[1])/L,-(b_[0]-a_[0])/L;sx,sy=near[0]+nx*2.4,near[1]+ny*2.4;ang=math.atan2(b_[1]-a_[1],b_[0]-a_[0])
  sq=[(sx+c1*2.3*math.cos(ang)-c2*2.3*math.sin(ang),sy+c1*2.3*math.sin(ang)+c2*2.3*math.cos(ang)) for c1,c2 in ((-1,-1),(1,-1),(1,1),(-1,1))]
  m.prism(sq,zb,zh(9.6),K['Rubble']);inset_roof(m,sq,zh(9.6),2.2,1.3,K['PostejRoof'],.3)
  opening(m,*lp(sx,sy,0,2.32,0,ang+math.pi)[:2],zh(5.4),1.1,2.2,ang+math.pi,True,0)
c27_finish(m)

# ================================================================= the castle
m=c27_new('SM_Kalmar_Slott','Kalmar slott/Castle')
CO=[tuple(p) for p in CA['outer']];CI=[tuple(p) for p in CA['court']];TW_=CA['towers']
RANGES={r['name']:dict(r) for r in CA['ranges']}
RANGES['SE_w']['s1']+=6.0;RANGES['SE_e']['s0']-=6.0   # the two halves of the south-east range overlap across bay 1
def rp(r,s,c,z):o=r['origin'];return (o[0]+r['u'][0]*s+r['n'][0]*c,o[1]+r['u'][1]*s+r['n'][1]*c,z)
def rframe(r,p):o=r['origin'];dx,dy=p[0]-o[0],p[1]-o[1];return dx*r['u'][0]+dy*r['u'][1],dx*r['n'][0]+dy*r['n'][1]
def roof_geom(r):
 half=(r['outer']-r['inner'])/2;rise=min(.93*half,6.0);slope=rise/half;mid=(r['outer']+r['inner'])/2
 return half,rise,slope,mid
def roof_z(r,c):half,rise,slope,mid=roof_geom(r);return ZE+rise-slope*abs(c-mid)
def in_other_range(p,name):
 for nm,r in RANGES.items():
  if nm==name:continue
  s,c=rframe(r,p)
  if r['s0']<=s<=r['s1'] and r['inner']-.4<=c<=r['outer']+.4:return True
 return False
def in_tower(p,pad=.4):
 return any(math.dist(p,t['centre'])<t['radius']+pad for t in TW_.values()) or point_in(p,CA['kure'])
ROOFS=[]
for name,r in RANGES.items():
 half,rise,slope,mid=roof_geom(r);ov=.4;ci_,co_=r['inner']-ov,r['outer']+ov;ze=ZE-ov*slope;zr=ZE+rise;s0,s1=r['s0'],r['s1']
 A,B,C=[rp(r,s0,c,z) for c,z in ((ci_,ze),(mid,zr),(co_,ze))];A2,B2,C2=[rp(r,s1,c,z) for c,z in ((ci_,ze),(mid,zr),(co_,ze))]
 m.faces([A,A2,B2,B],[(0,1,2,3)],K['Roof']);m.faces([B,B2,C2,C],[(0,1,2,3)],K['Roof'])
 m.faces([A,B,C],[(0,1,2)],K['Roof']);m.faces([C2,B2,A2],[(0,1,2)],K['Roof']);m.faces([A,C,C2,A2],[(0,1,2,3)],SIGN)
 town_rod(m,B,B2,.07,K['Roof'],6)
 for c,z in ((ci_,ze),(co_,ze)):town_rod(m,rp(r,s0,c,z-.02),rp(r,s1,c,z-.02),.075,K['Roof'],6)
 # Standing seams every 0.62 m, left off where another range or a tower takes over.
 k=0;s=s0+.31
 while s<s1:
  for c_edge in (ci_,co_):
   top=rp(r,s,mid-(.05 if c_edge<mid else -.05),zr-.05);bot=rp(r,s,c_edge,ze)
   if in_other_range(top[:2],name) or in_tower(top[:2]) or in_tower(bot[:2]):continue
   nz=.028;town_rod(m,(bot[0],bot[1],bot[2]+nz),(top[0],top[1],top[2]+nz),.02,K['Roof'],4)
  s+=.62
 ROOFS.append((name,r))
# Chimneys in salmon render with stone caps (photographs; positions approximate).
for name,f,dc in (('SW',.40,-1.3),('SW',.58,-1.3),('NW',.22,1.6),('NW',.74,1.8),('NE',.26,-2.2),('NE',.52,2.6),('NE',.80,-2.0),('SE_w',.45,-1.6),('SE_e',.55,1.8)):
 r=RANGES[name];half,rise,slope,mid=roof_geom(r);s=r['s0']+(r['s1']-r['s0'])*f;c=mid+dc;x,y,_=rp(r,s,c,0);zt=ZE+rise+1.6
 m.box((x,y,(roof_z(r,c)-.8+zt)/2),(1.0,.72,zt-roof_z(r,c)+.8),K['Chimney'],math.atan2(r['u'][1],r['u'][0]))
 m.box((x,y,zt+.06),(1.16,.88,.12),K['Coping'],math.atan2(r['u'][1],r['u'][0]))
# ---------------------------------------------------------------- outer fronts
def row_holes(L,spacing,b,w,h,r=0,margin=1.6,shift=0.0):
 n=max(1,int((L-2*margin)/spacing)+1) if L>2*margin+w else 0;out=[]
 for k in range(n):
  u=-(n-1)*spacing/2+k*spacing+shift
  if abs(u)+w/2<L/2-.4:out.append((u,b,w,h,r))
 return out
def front(m,p,q,z0,z1,ma,rows,doors=(),cornice=True,dentils=True):
 x,y,L,a=sf_edge(p,q);holes=list(doors)
 for spacing,b,w,h,r,kind in rows:holes+=[(u,b_,w_,h_,r_) for u,b_,w_,h_,r_ in row_holes(L,spacing,b,w,h,r)]
 bz_wall(m,p,q,z0,z1,holes,ma)
 for u,b,w,h,r in holes:
  if b<z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)
  elif r>0:p18_win(m,x,y,u,b,w,h,r,a,K['Frame'],K['Brick'],2,2)
  else:s20_window(m,x,y,u,b,w,h,a,K['Frame'],TRIM,.62)
 if cornice:lm_cornice(m,x,y,L+.4,z1-.2,a,TRIM,dentils)
 return x,y,L,a
def arch_door27(m,x,y,u,b,w,h,r,a):
 facade_box(m,x,y,u,.12,b+h/2,w,.08,h,K['Door'],a)
 kk=16;m.faces([lp(x,y,u+w/2*math.cos(t*math.pi/kk),.12,b+h+r*math.sin(t*math.pi/kk),a) for t in range(kk+1)],[tuple(range(kk+1))],K['Door'])
 if r>0:p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w+.25,r+.12,.22,.40,a,TRIM)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.12),.40,b+h/2,.24,.12,h,TRIM,a)
OUT_ROWS=[(4.4,Z0+7.9,1.15,3.2,0,'main'),(4.4,Z0+13.9,.62,.62,.2,'top'),(5.0,Z0+4.85,.62,1.2,0,'low')]
facade_edges={'SW':[(7,8),(8,9),(9,10)],'SE':[(22,23),(26,27),(30,31),(31,32)],'NE':[(39,40),(40,41),(41,42),(42,43),(43,44),(44,45),(45,46)],'NW':[(55,56),(60,0)]}
for side,edges in facade_edges.items():
 longest=max(edges,key=lambda e:math.dist(CO[e[0]],CO[e[1]]))
 for i,j in edges:
  p,q=CO[i],CO[j];L=math.dist(p,q)
  if L<2.6:bz_wall(m,p,q,Z0,ZE,[],K['Render']);continue
  doors=[(0.0,Z0,1.5,2.9,.55)] if (i,j)==longest else []
  front(m,p,q,Z0,ZE,K['Render'],OUT_ROWS if L>6 else OUT_ROWS[:2],doors)
# The entrance from the walled causeway into the north-west range, at courtyard level.
p,q=CO[56],CO[57];x,y,L,a=sf_edge(p,q);bz_wall(m,p,q,Z0,ZE,[],K['Render'])
lm_cornice(m,x,y,L+.4,ZE-.2,a,TRIM,True)
# ---------------------------------------------------------------- the two south-east bays with stepped gables
def stepped_gable(m,p,q,zb,height,steps,ma,trim,oculus=True):
 # Renaissance stepped gable: steps rising from both ends to a round crown, obelisk finials.
 x,y,L,a=sf_edge(p,q);sw=L/2/(steps+1.3);sh=height/(steps+1.6);left=[(-L/2,zb-.2)]
 for k in range(steps):
  hw=L/2-k*sw;left+=[(-hw,zb+(k+1)*sh),(-(hw-sw),zb+(k+1)*sh)]
 hw=L/2-steps*sw;crest=zb+steps*sh
 crown=[(-hw*math.cos(t*math.pi/12),crest+hw*1.1*math.sin(t*math.pi/12)) for t in range(1,12)]
 outline=left+crown+[(-u,z) for u,z in reversed(left)]
 cleaned=[]
 for v in outline:
  if not cleaned or math.dist(v,cleaned[-1])>.02:cleaned.append(v)
 n=len(cleaned);vs=[lp(x,y,u,o,z,a) for o in (-.15,.42) for u,z in cleaned]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 town_path(m,[lp(x,y,u,.46,z+.05,a) for u,z in cleaned[1:-1]],.075,trim)
 for k in range(steps):
  hw=L/2-k*sw
  for s in (-1,1):poly_lathe(m,*lp(x,y,s*(hw-.12),.14,0,a)[:2],zb+(k+1)*sh,[(.17,0),(.17,.18),(.09,.24),(.02,1.0)],trim,4,a+math.pi/4)
 hc=L/2-steps*sw;poly_lathe(m,*lp(x,y,0,.14,0,a)[:2],crest+hc*1.1,[(.2,0),(.2,.2),(.1,.28),(.02,1.2)],trim,4,a+math.pi/4)
 if oculus:
  k=24;cz=zb+sh*1.5;m.faces([lp(x,y,.55*math.cos(t*math.tau/k),.44,cz+.55*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],GL)
  town_path(m,[lp(x,y,.66*math.cos(t*math.tau/k),.47,cz+.66*math.sin(t*math.tau/k),a) for t in range(k+1)],.07,trim)
for bay in CA['bays']:
 bp=[tuple(v) for v in bay['polygon']]
 for i in range(3):
  p,q=bp[i],bp[i+1];L=math.dist(p,q)
  front(m,p,q,Z0,ZE,K['Render'],[(3.2,Z0+7.9,1.1,3.0,0,'main'),(3.2,Z0+13.9,.62,.62,.2,'top')],cornice=(i!=1))
 p,q=bp[1],bp[2];x,y,L,a=sf_edge(p,q);nx,ny=math.sin(a),-math.cos(a);depth=math.dist(bp[0],bp[1])+7
 stepped_gable(m,p,q,ZE,7.2,4,K['Render'],TRIM)
 ridge=ZE+L/2*.95;pa,pb=(p[0],p[1]),(q[0],q[1]);pm=((p[0]+q[0])/2,(p[1]+q[1])/2)
 back=lambda v:(v[0]-nx*depth,v[1]-ny*depth)
 A=(*pa,ZE-.25);Bv=(*pm,ridge);Cv=(*pb,ZE-.25);A2=(*back(pa),ZE-.25);B2=(*back(pm),ridge);C2=(*back(pb),ZE-.25)
 m.faces([A2,A,Bv,B2],[(0,1,2,3)],K['Roof']);m.faces([B2,Bv,Cv,C2],[(0,1,2,3)],K['Roof']);town_rod(m,Bv,B2,.07,K['Roof'],6)
# A stepped gable over the middle of the north-east front (aerial photographs, 2021).
p,q=CO[45],CO[46];x,y,L,a=sf_edge(p,q);gp,gq=lp(x,y,-3.4,0,0,a)[:2],lp(x,y,3.4,0,0,a)[:2]
stepped_gable(m,gp,gq,ZE,6.4,3,K['Render'],TRIM);nx,ny=math.sin(a),-math.cos(a);pm=lp(x,y,0,0,0,a)[:2]
for s in (-1,1):
 e=lp(x,y,s*3.4,0,0,a)[:2];m.faces([(*e,ZE-.2),(*pm,ZE+3.3),(pm[0]-nx*7,pm[1]-ny*7,ZE+3.3),(e[0]-nx*7,e[1]-ny*7,ZE-.2)][::(1 if s<0 else -1)],[(0,1,2,3)],K['Roof'])
# ---------------------------------------------------------------- courtyard fronts
cw=CI[::-1];court_mats={}
for i in range(len(cw)):
 p,q=cw[i],cw[(i+1)%len(cw)];L=math.dist(p,q);x,y,_,a=sf_edge(p,q)
 ox,oy=math.sin(a),-math.cos(a);ma=K['CourtBlock'] if ox>.6 else K['Court']
 if L<2.5:bz_wall(m,p,q,ZC,ZE,[],ma);continue
 doors=[(0.0,ZC,1.4,2.4,.7)] if L>12 else []
 front(m,p,q,ZC,ZE,ma,[(3.8,ZC+5.6,1.2,2.4,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L>6 else [(3.8,ZC+5.6,1.2,2.4,0,'first')],doors,True,False)
# Dormers with red-painted fronts on the courtyard slopes (courtyard photographs 2022).
for name,f in (('SE_w',.5),('NE',.45),('NW',.35),('SW',.55)):
 r=RANGES[name];half,rise,slope,mid=roof_geom(r);s=r['s0']+(r['s1']-r['s0'])*f
 p=rp(r,s-2,r['inner'],0)[:2];q=rp(r,s+2,r['inner'],0)[:2];x,y,L,a=sf_edge(q,p)
 roof_dormer(m,x,y,0,a,ZE,slope,.9,.95,1.2,K['FrameRed'],K['Roof'],K['Frame'],True)
# The chapel's roof turret over the south-west range (photographs from Kalmarsundsparken).
r=RANGES['SW'];half,rise,slope,mid=roof_geom(r);x,y,_=rp(r,r['s0']+(r['s1']-r['s0'])*.455,mid,0);zr=ZE+rise
poly_lathe(m,x,y,zr-.4,[(.62,0),(.62,1.9),(.76,2.02),(.76,2.12)],K['CopperDark'],8,math.pi/8)
for k in range(8):
 t=math.pi/8+k*math.tau/8+math.tau/16;px,py=x+.6*math.cos(t),y+.6*math.sin(t);facade_box(m,px,py,0,.01,zr+.9,.28,.04,.8,SIGN,t+math.pi/2)
m.lathe(x,y,zr+1.72,[(.76,0),(.5,.35),(.1,3.1),(.04,3.5)],K['Copper'],16);m.lathe(x,y,zr+5.2,[(.03,0),(.13,.05),(.13,.24),(.03,.28)],K['Gold'],10)
# ---------------------------------------------------------------- the well house of 1578
wx,wy=CA['well'];WS=K['WellStone']
poly_lathe(m,wx,wy,ZC,[(2.05,0),(2.05,.15),(1.8,.15),(1.8,1.05),(1.9,1.12),(1.9,1.2)],WS,8,math.pi/8)
for k in range(8):
 t=math.pi/8+k*math.tau/8;px,py=wx+1.5*math.cos(t),wy+1.5*math.sin(t)
 m.cylinder(px,py,ZC+1.2,.15,2.35,WS,10);m.box((px,py,ZC+1.28),(.36,.36,.16),WS);m.box((px,py,ZC+3.5),(.38,.38,.14),WS)
poly_lathe(m,wx,wy,ZC+3.55,[(1.95,0),(1.95,.5),(2.05,.55),(2.05,.62)],WS,8,math.pi/8)
for k in range(4):
 t=k*math.pi/2;px,py=wx+1.85*math.cos(t),wy+1.85*math.sin(t);ang=t+math.pi/2
 m.faces([lp(px,py,-1.1,.05,ZC+4.17,ang),lp(px,py,1.1,.05,ZC+4.17,ang),lp(px,py,0,.05,ZC+4.85,ang),lp(px,py,-1.1,-.4,ZC+4.17,ang),lp(px,py,1.1,-.4,ZC+4.17,ang),lp(px,py,0,-.4,ZC+4.85,ang)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],WS)
poly_lathe(m,wx,wy,ZC+4.17,[(.85,0),(.85,1.4),(1.0,1.5),(1.0,1.6)],WS,8,math.pi/8)
poly_lathe(m,wx,wy,ZC+5.77,[(1.0,0),(.8,.2),(.45,.5),(.18,.72)],WS,8,math.pi/8,True)
m.lathe(wx,wy,ZC+6.49,[(.12,0),(.16,.2),(.1,.45),(.05,.62),(.08,.66),(.03,.7)],WS,8)
c27_finish(m)

# ================================================================= towers, Kuretornet and the copper caps
m=c27_new('SM_Kalmar_Slott_Towers','Kalmar slott/Castle')
CX,CY=sum(p[0] for p in CO)/len(CO),sum(p[1] for p in CO)/len(CO)
def ribbed(m,cx,cy,z,profile,ma,n=48,ribs=16):
 m.lathe(cx,cy,z,profile,ma,n)
 for k in range(ribs):
  t=k*math.tau/ribs;town_path(m,[(cx+(r+.03)*math.cos(t),cy+(r+.03)*math.sin(t),z+h) for r,h in profile[1:-1]],.035,ma)
def lantern8(m,cx,cy,z,r,h,ma,rot=math.pi/8,open_w=.5,open_h=None):
 poly_lathe(m,cx,cy,z,[(r+.15,0),(r+.15,.18),(r,.18),(r,h-.3),(r+.2,h-.15),(r+.2,h)],ma,8,rot)
 oh=open_h or h*.55;ap=r*math.cos(math.pi/8)
 for k in range(8):
  t=rot+math.pi/8+k*math.tau/8;px,py=cx+(ap+.01)*math.cos(t),cy+(ap+.01)*math.sin(t);ang=t+math.pi/2
  facade_box(m,px,py,0,.01,z+.35+oh/2,open_w,.03,oh,SIGN,ang)
  kk=10;m.faces([lp(px,py,open_w/2*math.cos(i*math.pi/kk),.03,z+.35+oh+open_w/2*math.sin(i*math.pi/kk),ang) for i in range(kk+1)],[tuple(range(kk+1))],SIGN)
TOWER_SPEC={
 'W':dict(top=25.3,cap=[('bell',[(0.45,0),(0.35,.2),(0.05,.6),(-.3,1.3),(-.55,2.2),(-.8,3.2),(-1.2,4.3),(-1.9,5.5),(-2.9,6.7),(-3.9,7.7),('a',1.5,8.4),('a',1.15,8.8)]),
   ('neck',8.8,1.05,1.8),('onion',10.6,[(1.2,0),(1.45,.4),(1.6,1.1),(1.45,1.9),(1.0,2.6),(.5,3.2),(.18,3.7),(.12,3.9)]),('finial',14.5,4.4)]),
 'S':dict(top=25.6,cap=[('bell',[(0.45,0),(0.35,.2),(0.05,.6),(-.35,1.3),(-.65,2.2),(-1.0,3.2),(-1.6,4.3),(-2.5,5.4),(-3.6,6.4),(-4.5,7.2),('a',1.7,7.65),('a',1.5,7.9)]),
   ('lantern',7.9,1.45,2.7),('ogee',10.6),('finial',12.4,4.6)]),
 'N':dict(top=24.6,cap=[('bell',[(0.45,0),(0.35,.2),(0.05,.55),(-.35,1.2),(-.7,2.1),(-1.2,3.1),(-2.0,4.1),(-3.0,5.0),(-4.0,5.8),('a',1.5,6.15),('a',1.2,6.4)]),
   ('neck',6.4,1.1,1.35),('onion',7.6,[(1.25,0),(1.5,.45),(1.6,1.2),(1.4,2.0),(.9,2.7),(.4,3.2),(.14,3.4)]),('finial',11.0,4.6)]),
 'E':dict(top=25.3,cap=[('bell',[(0.45,0),(0.35,.2),(0.05,.6),(-.3,1.3),(-.6,2.2),(-.95,3.1),(-1.5,4.2),(-2.3,5.3),(-3.2,6.3),(-3.8,6.95),('a',1.6,7.35),('a',1.4,7.6)]),
   ('lantern',7.6,1.35,2.6),('ogee',10.2),('finial',11.9,4.5)]),
}
for key,spec in TOWER_SPEC.items():
 T=TW_[key];cx,cy=T['centre'];r=T['radius'];z1=zh(spec['top'])
 m.cylinder(cx,cy,Z0-.2,r,z1-Z0+.2,K['RenderTower'],56)
 m.cylinder(cx,cy,z1-.55,r+.24,.55,TRIM,56);m.cylinder(cx,cy,z1-.95,r+.12,.4,TRIM,56)
 for k in range(26):
  t=k*math.tau/26;facade_box(m,cx+(r+.01)*math.cos(t),cy+(r+.01)*math.sin(t),0,.02,z1-1.35,.2,.05,.2,SIGN,t+math.pi/2)
 t0=math.atan2(cy-CY,cx-CX)
 for dt,zz,w,h,arched in ((0,Z0+7.6,1.0,2.4,False),(.62,Z0+11.8,.8,1.3,False),(-.55,Z0+15.4,.62,.9,True),(-.9,Z0+4.4,.55,.9,False),(.95,Z0+16.8,.55,.7,True)):
  t=t0+dt;town_window(m,cx+(r+.02)*math.cos(t),cy+(r+.02)*math.sin(t),zz+h/2,w,h,t+math.pi/2,K['Frame'],arched,2,2,True)
 for part in spec['cap']:
  if part[0]=='bell':
   prof=[((r+v[0]),v[1]) if v[0]!='a' else (v[1],v[2]) for v in part[1]]
   ribbed(m,cx,cy,z1,prof,K['Copper'])
  elif part[0]=='neck':poly_lathe(m,cx,cy,z1+part[1],[(part[2],0),(part[2],part[3]-.2),(part[2]+.2,part[3])],K['Copper'],8,math.pi/8)
  elif part[0]=='onion':m.lathe(cx,cy,z1+part[1],part[2],K['Copper'],24)
  elif part[0]=='lantern':lantern8(m,cx,cy,z1+part[1],part[2],part[3],K['CopperDark'],open_w=.45)
  elif part[0]=='ogee':m.lathe(cx,cy,z1+part[1],[(1.75,0),(1.4,.35),(1.0,.8),(.6,1.3),(.28,1.65),(.12,1.8)],K['Copper'],24)
  elif part[0]=='finial':
   z=z1+part[1];Ht=part[2]
   m.lathe(cx,cy,z,[(.13,0),(.10,.25*Ht/4.4),(.31,.4*Ht/4.4),(.33,.55*Ht/4.4),(.29,.7*Ht/4.4),(.09,.85*Ht/4.4),(.08,.62*Ht),(.2,.66*Ht),(.2,.7*Ht),(.07,.74*Ht),(.045,Ht)],K['CopperDark'],12)
   m.box((cx+.28,cy,z+.9*Ht),(.56,.02,.3),K['Gold'],t0)
# Kuretornet: rubble-stone gate tower, row of small square openings below a corbelled cornice.
kp=[tuple(p) for p in CA['kure']];ZK=zh(32.0)
ek=max(poly_edges(kp),key=lambda e:math.dist(*e));ka=math.atan2(ek[1][1]-ek[0][1],ek[1][0]-ek[0][0])
ku=(math.cos(ka),math.sin(ka));kv=(-ku[1],ku[0]);kcx=sum(p[0] for p in kp)/len(kp);kcy=sum(p[1] for p in kp)/len(kp)
us=[(p[0]-kcx)*ku[0]+(p[1]-kcy)*ku[1] for p in kp];vs=[(p[0]-kcx)*kv[0]+(p[1]-kcy)*kv[1] for p in kp]
kcx,kcy=kcx+ku[0]*(max(us)+min(us))/2+kv[0]*(max(vs)+min(vs))/2,kcy+ku[1]*(max(us)+min(us))/2+kv[1]*(max(vs)+min(vs))/2
hu,hv=(max(us)-min(us))/2,(max(vs)-min(vs))/2
KRECT=[(kcx+ku[0]*a_*hu+kv[0]*b_*hv,kcy+ku[1]*a_*hu+kv[1]*b_*hv) for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))]
for p,q in poly_edges(KRECT):
 x,y,L,a=sf_edge(p,q);ox,oy=math.sin(a),-math.cos(a);nw=(ox*-.7+oy*.7)>.8
 holes=[(-L/2+(k+.5)*L/6,zh(30.35),.5,.62,0) for k in range(6)]
 cd_=tuple(C27['castle_door']);ud=(cd_[0]-x)*math.cos(a)+(cd_[1]-y)*math.sin(a);vd=(cd_[0]-x)*math.sin(a)-(cd_[1]-y)*math.cos(a)
 gate_face=abs(vd)<2.5 and abs(ud)<L/2+.5
 if nw:holes+=[(0,zh(19.2),1.1,2.3,.75),(0,zh(24.2),.6,.9,0)]
 else:holes+=[(-L/4,zh(18.5),.7,1.2,0),(L/5,zh(24.0),.6,.9,0)]
 if gate_face:holes.append((max(-L/2+1.6,min(L/2-1.6,ud)),Z0,2.2,3.0,1.1))
 bz_wall(m,p,q,Z0-.2,ZK,holes,K['KureStone'])
 for u,b,w,h,r in holes:
  if b<Z0+.2:facade_box(m,x,y,u,-1.2,b+(h+r)/2,w,.1,h+r,SIGN,a);p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w+.3,r+.15,.35,.40,a,K['Trim'])
  elif r>0:p18_win(m,x,y,u,b,w,h,r,a,K['Frame'],K['Trim'],3,2)
  else:facade_box(m,x,y,u,.10,b+h/2,w,.06,h,SIGN,a)
 facade_box(m,x,y,0,.30,ZK-.25,L+.6,.6,.5,K['KureStone'],a)
 for k in range(int(L/.9)):facade_box(m,x,y,-L/2+(k+.5)*L/int(L/.9),.18,ZK-.72,.32,.36,.45,K['KureStone'],a)
# Square bell roof in copper: concave flare over the cornice, convex shoulders, four dormers.
KPROF=[(1.00,0.0),(0.93,.3),(0.89,.8),(0.87,1.6),(0.86,2.6),(0.83,3.8),(0.76,5.2),(0.64,6.6),(0.47,7.9),(0.32,8.9),(0.235,9.5),(0.215,9.8)]
EU,EV=hu+.6,hv+.6
def kring(f,dz):return [(kcx+ku[0]*a_*EU*f+kv[0]*b_*EV*f,kcy+ku[1]*a_*EU*f+kv[1]*b_*EV*f,ZK+dz) for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))]
rings=[kring(f,dz) for f,dz in KPROF]
for r0,r1 in zip(rings,rings[1:]):
 for i in range(4):j=(i+1)%4;m.faces([r0[i],r0[j],r1[j],r1[i]],[(0,1,2,3)],K['Copper'])
m.faces(rings[-1],[(0,1,2,3)],K['Copper'])
for i in range(4):j=(i+1)%4;wr=[(*KRECT[i],ZK),(*KRECT[j],ZK)];m.faces([rings[0][j],rings[0][i],wr[0],wr[1]],[(0,1,2,3)],SIGN)
for i in range(4):
 c=rings[0][i];poly_lathe(m,c[0],c[1],ZK,[(.2,0),(.2,.25),(.11,.32),(.02,1.5)],K['CopperDark'],4,ka+math.pi/4)
for side_ in range(4):
 # A dormer in each face, its front flush with the steep lower part of the bell (3.2-5.0 m).
 axis=[(1,0),(0,1),(-1,0),(0,-1)][side_];half=(EU if axis[0] else EV)*.835
 nx_,ny_=ku[0]*axis[0]+kv[0]*axis[1],ku[1]*axis[0]+kv[1]*axis[1];fx,fy=kcx+nx_*(half+.05),kcy+ny_*(half+.05);ang=math.atan2(ny_,nx_)-math.pi/2
 facade_box(m,fx,fy,0,-1.0,ZK+3.9,1.5,2.0,1.9,K['Copper'],ang)
 facade_box(m,fx,fy,0,.02,ZK+3.8,.8,.05,1.1,SIGN,ang);town_border(m,fx,fy,ZK+3.8,.8,1.1,ang,K['CopperDark'],.05,.05)
 kk=12;prof=[(.85*math.cos(t*math.pi/kk),ZK+4.85+.45*math.sin(t*math.pi/kk)) for t in range(kk+1)]
 m.faces([lp(fx,fy,u,.06,z,ang) for u,z in prof],[tuple(range(kk+1))],K['Copper'])
 for (u0,z0),(u1,z1) in zip(prof,prof[1:]):m.faces([lp(fx,fy,u0,.08,z0,ang),lp(fx,fy,u1,.08,z1,ang),lp(fx,fy,u1,-2.0,z1,ang),lp(fx,fy,u0,-2.0,z0,ang)],[(0,1,2,3)],K['Copper'])
ZL=ZK+9.8
lantern8(m,kcx,kcy,ZL,1.9,4.7,K['CopperDark'],ka+math.pi/8,.85,2.4)
poly_lathe(m,kcx,kcy,ZL+4.7,[(2.15,0),(1.95,.3),(1.55,.8),(1.05,1.35),(.6,1.8),(.3,2.1)],K['Copper'],8,ka+math.pi/8,True)
zs=ZL+6.8
m.lathe(kcx,kcy,zs,[(.30,0),(.20,.4),(.16,.9),(.34,1.2),(.34,1.45),(.15,1.75),(.13,4.7),(.35,5.05),(.55,5.4),(.35,5.75),(.13,6.1),(.09,9.5),(.05,9.6)],K['CopperDark'],14)
zc=zs+9.6;m.lathe(kcx,kcy,zc,[(.18,0),(.34,.12),(.34,.3),(.26,.36)],K['Gold'],14)
for k in range(5):
 t=k*math.tau/5;town_rod(m,(kcx+.3*math.cos(t),kcy+.3*math.sin(t),zc+.3),(kcx+.36*math.cos(t),kcy+.36*math.sin(t),zc+.62),.04,K['Gold'],6)
m.lathe(kcx,kcy,zc+.36,[(.03,0),(.12,.06),(.12,.2),(.03,.26)],K['Gold'],10);town_rod(m,(kcx,kcy,zc+.6),(kcx,kcy,zc+1.05),.03,K['Gold'],6)
c27_finish(m)

# ================================================================= timber bridges and the drawbridge
m=c27_new('SM_Castle27_Bridge','Kalmar slott/Bridges')
def plank_deck(m,a,b,za,zb,w,ma):
 # Deck with planks across the bridge: custom UVs (1 UV unit per metre, planks along v).
 L=math.dist(a,b);ux,uy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=uy,-ux;v=[]
 for s,c in ((0,-w/2),(L,-w/2),(L,w/2),(0,w/2)):v.append((a[0]+ux*s+nx*c,a[1]+uy*s+ny*c,za+(zb-za)*s/L))
 m.faces(v,[(3,2,1,0)],ma,uvcoords=[(0,-w/2/1.2),(L/1.2,-w/2/1.2),(L/1.2,w/2/1.2),(0,w/2/1.2)][::-1])
 m.faces([(x,y,z-.1) for x,y,z in v],[(0,1,2,3)],ma)
 for i in range(4):j=(i+1)%4;m.faces([v[i],v[j],(v[j][0],v[j][1],v[j][2]-.1),(v[i][0],v[i][1],v[i][2]-.1)],[(0,1,2,3)],ma)
def timber_bridge(m,pts,za,zb,w,bent=2.7,skip_end=0.0,rails=True):
 Ltot=sum(math.dist(p,q) for p,q in zip(pts,pts[1:]));acc=0.0
 for p,q in zip(pts,pts[1:]):
  L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux;ang=math.atan2(uy,ux)
  z=lambda s:za+(zb-za)*min(1,(acc+s)/Ltot)
  plank_deck(m,p,q,z(0),z(L),w,K['Timber'])
  for c in (-w/2+.35,0,w/2-.35):town_rod(m,(p[0]+nx*c,p[1]+ny*c,z(0)-.28),(q[0]+nx*c,q[1]+ny*c,z(L)-.28),.14,K['TimberDark'],6)
  k=0
  while k*bent<=L+.01:
   s=k*bent;cx_,cy_=p[0]+ux*s,p[1]+uy*s
   if acc+s<=Ltot-skip_end:
    for c in (-w/2+.3,w/2-.3):m.box((cx_+nx*c,cy_+ny*c,(zh(-2.2)+z(s)-.45)/2),(.26,.26,z(s)-.45-zh(-2.2)),K['TimberDark'],ang)
    m.box((cx_,cy_,z(s)-.52),(.3,w+.3,.24),K['TimberDark'],ang)
   k+=1
  if rails:
   for c in (-w/2+.06,w/2-.06):
    nposts=max(1,round(L/1.6))
    for i in range(nposts+1):
     s=L*i/nposts;m.box((p[0]+ux*s+nx*c,p[1]+uy*s+ny*c,z(s)+.55),(.12,.12,1.1),K['Timber'],ang)
    for hz,rw,rh in ((1.08,.10,.14),(.55,.07,.10)):
     a0=(p[0]+nx*c,p[1]+ny*c,z(0)+hz+rh/2);a1=(q[0]+nx*c,q[1]+ny*c,z(L)+hz+rh/2);ln=math.dist(a0,a1)
     m.box(((a0[0]+a1[0])/2,(a0[1]+a1[1])/2,(a0[2]+a1[2])/2),(ln+.1,rw,rh),K['Timber'],ang)
  acc+=L
BR=C27['bridges'];main=[tuple(v) for v in BR['main']['points']];ZD=zh(HL['deck']);ZRV=zh(HL['ravelin'])
timber_bridge(m,main,ZRV,ZD,BR['main']['width'],skip_end=4.5)
# Drawbridge frame near the gate: two posts, a head beam, braces and the two lifting arms with chains.
g=main[-1];pa=main[-2];L=math.dist(pa,g);ux,uy=(g[0]-pa[0])/L,(g[1]-pa[1])/L;nx,ny=uy,-ux;ang=math.atan2(uy,ux)
fx,fy=g[0]-ux*5.8,g[1]-uy*5.8;wb=BR['main']['width']
for c in (-wb/2-.05,wb/2+.05):
 m.box((fx+nx*c,fy+ny*c,ZD+3.4),(.32,.32,6.9),K['TimberDark'],ang)
 town_rod(m,(fx+nx*c-ux*2.2,fy+ny*c-uy*2.2,ZD+.1),(fx+nx*c,fy+ny*c,ZD+3.0),.11,K['TimberDark'],6)
 town_rod(m,(fx+nx*c-ux*1.6+ux*.0,fy+ny*c-uy*1.6,ZD+6.95),(g[0]+nx*c+ux*.3,g[1]+ny*c+uy*.3,ZD+6.95),.15,K['TimberDark'],6)
 town_rod(m,(g[0]+nx*c,g[1]+ny*c,ZD+6.8),(g[0]+nx*c-ux*.2,g[1]+ny*c-uy*.2,ZD+.1),.018,K['Iron'],6)
m.box((fx,fy,ZD+6.95),(.32,wb+.8,.3),K['TimberDark'],ang)
# Ravelin bridge to the park (the park itself lies outside the model; the bridge ends at an abutment).
rvb=[tuple(v) for v in BR['ravelin']['points']];timber_bridge(m,rvb,ZRV-.2,ZRV,BR['ravelin']['width'])
c27_finish(m,False)

# ================================================================= ravelin and the castellan's house
m=c27_new('SM_Castle27_Ravelin','Kalmar slott/Ravelin')
RV=C27['ravelin'];rvp=[tuple(v) for v in RV['polygon']]
battered(m,rvp,zh(-.6),ZRV+.02,1.5,.06,K['LowWall'],closed=True)
lands=[tuple(C27['bridges']['main']['points'][0]),tuple(C27['bridges']['ravelin']['points'][-1])]
for p,q in poly_edges(rvp):
 x,y,L,a=sf_edge(p,q);spans=[(-L/2,L/2)]
 for g_ in lands:
  u=(g_[0]-x)*math.cos(a)+(g_[1]-y)*math.sin(a);v=(g_[0]-x)*math.sin(a)-(g_[1]-y)*math.cos(a)
  if abs(v)<2.5 and -L/2-1<u<L/2+1:spans=[s for lo,hi in spans for s in ((lo,min(hi,u-2.0)),(max(lo,u+2.0),hi)) if s[1]-s[0]>.3]
 for lo,hi in spans:facade_box(m,x,y,(lo+hi)/2,-.2,ZRV+.1,hi-lo,.8,.18,K['Coping'],a)
for q in RV['inner']:surf(m,q,ZRV,K['Grass'])
ZPP=zh(HL['ravelin_parapet'])
for q in RV['parapet']:
 surf(m,q,ZPP,K['Grass'])
 for p1,p2 in poly_edges([tuple(v) for v in q['outer']]):m.faces([(*p1,ZRV-.1),(*p2,ZRV-.1),(*p2,ZPP),(*p1,ZPP)],[(0,1,2,3)],K['Rubble'])
ab=rvb[0];m.box((ab[0],ab[1],ZRV-.2-1.72),(3.6,3.6,3.4),K['LowWall'],math.atan2(rvb[1][1]-ab[1],rvb[1][0]-ab[0]))   # top 2 cm under the deck
vp=[tuple(v) for v in RV['villa']];vh=ZRV+3.3
for p,q in poly_edges(vp):
 x,y,L,a=sf_edge(p,q);n=max(1,round(L/2.6));holes=[(-L/2+(k+.5)*L/n,ZRV+.9,1.0,1.55,0) for k in range(n)]
 if L>9:holes[len(holes)//2]=(holes[len(holes)//2][0],ZRV+.05,1.0,2.2,0)
 bz_wall(m,p,q,ZRV-.3,vh,holes,K['Villa'])
 for u,b,w,h,r in holes:s20_window(m,x,y,u,b,w,h,a,K['Frame'],TRIM,.6) if b>ZRV+.3 else facade_box(m,x,y,u,.12,b+h/2,w,.08,h,K['Door'],a)
 facade_box(m,x,y,0,.30,vh-.15,L+.3,.3,.3,K['Villa'],a)
outer_,inner_=inset_roof(m,vp,vh,.95,2.0,K['VillaShingle'],.45)
short=min(math.dist(p,q) for p,q in poly_edges(inner_));inset_roof(m,inner_,vh+2.0,short/2-.35,1.5,K['VillaTile'],.05)
for p,q in poly_edges(vp):
 x,y,L,a=sf_edge(p,q)
 if L>9:
  for u in (-L/4,L/4):roof_dormer(m,x,y,u,a,vh,2.0/1.4,.55,.8,1.0,K['VillaShingle'],K['VillaShingle'],K['Frame'],False)
vcx,vcy=sum(p[0] for p in vp)/4,sum(p[1] for p in vp)/4;m.box((vcx,vcy,vh+2.4),(.9,.7,4.4),K['Brick'])
c27_finish(m)

# ================================================================= islets, riprap and guns
m=c27_new('SM_Castle27_Islets','Kalmar slott/Ground')
for isl in C27['islets']:
 poly=[tuple(v) for v in isl['polygon']];ins=ring_offset(poly,-1.8)
 surf(m,{'outer':[list(v) for v in ins],'holes':[]},zh(HL['islet']),K['Reed'])
 for i in range(len(poly)):
  j=(i+1)%len(poly);m.faces([(*poly[i],zh(-.6)),(*poly[j],zh(-.6)),(*ins[j],zh(HL['islet'])),(*ins[i],zh(HL['islet']))],[(0,1,2,3)],K['Reed'])
c27_finish(m)
m=c27_new('SM_Castle27_Riprap','Kalmar slott/Ground')
for i in range(len(coast)):
 j=(i+1)%len(coast);a,b=coast[i],coast[j];mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
 if any(point_in(mid,p['polygon']) for p in C27['postejer'].values()):continue
 L=math.dist(a,b);n=max(1,int(L/.95));nx,ny=(b[1]-a[1])/L,-(b[0]-a[0])/L
 for k in range(n):
  t=(k+rng.uniform(.2,.8))/n;x,y=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
  boulder(m,x-nx*.5,y-ny*.5,zh(.05),rng.uniform(.34,.62),K['Boulder'])
  if rng.random()<.55:boulder(m,x-nx*1.5,y-ny*1.5,zh(.55),rng.uniform(.28,.5),K['Boulder'])
for key,p in C27['postejer'].items():
 cx,cy=p['centre'];r=p['radius'];t0=math.atan2(cy-CY,cx-CX)
 for k in range(int(math.pi*(r+1.2)/1.05)):
  t=t0-math.pi/2+k*1.05/(r+1.2);boulder(m,cx+(r+1.1)*math.cos(t),cy+(r+1.1)*math.sin(t),zh(.05),rng.uniform(.35,.6),K['Boulder'])
lw0,lw1=[tuple(v) for v in C27['lower_wall'][:1]+C27['lower_wall'][-1:]];Llw=math.dist(lw0,lw1);ux,uy=(lw1[0]-lw0[0])/Llw,(lw1[1]-lw0[1])/Llw;nx,ny=uy,-ux
for k in range(int(Llw/.8)):
 s=(k+rng.uniform(.2,.8))*.8;boulder(m,lw0[0]+ux*s+nx*.75,lw0[1]+uy*s+ny*.75,zh(.3),rng.uniform(.4,.7),K['Boulder'])
c27_finish(m,False)
m=c27_new('SM_Castle27_Guns','Kalmar slott/Fortifications')
for g in C27['cannons']:
 x,y=g['at'];fx,fy=g['facing'];ang=math.atan2(fy,fx);px,py=-fy,fx
 m.box((x,y,ZR+.42),(1.9,.72,.34),K['TimberDark'],ang)
 for s in (-1,1):
  m.box((x+px*s*.33-fx*.1,y+py*s*.33-fy*.1,ZR+.62),(1.5,.1,.5),K['TimberDark'],ang)
  for d in (-.55,.45):town_rod(m,(x+fx*d+px*s*.42,y+fy*d+py*s*.42,ZR+.3),(x+fx*d+px*s*.56,y+fy*d+py*s*.56,ZR+.3),.3 if d>0 else .26,K['TimberDark'],12)
 zb_=ZR+.92;pts=[(-.95,.27),(-.35,.25),(.3,.2),(1.1,.17),(1.45,.2),(1.5,.15)]
 for (d0,r0),(d1,r1) in zip(pts,pts[1:]):town_rod(m,(x+fx*d0,y+fy*d0,zb_+d0*.07),(x+fx*d1,y+fy*d1,zb_+d1*.07),(r0+r1)/2,K['Iron'],12)
 town_rod(m,(x-fx*1.02,y-fy*1.02,zb_-.07),(x-fx*.95,y-fy*.95,zb_-.066),.1,K['Iron'],8)
c27_finish(m,False)

# ================================================================= cameras
from_local=lambda x,y:(56.66412+(x*math.sin(math.radians(28.2))+y*math.cos(math.radians(28.2)))/111320,16.3656+(x*math.cos(math.radians(28.2))-y*math.sin(math.radians(28.2)))/(111320*math.cos(math.radians(56.66412))))
castle27_cameras=[
 # Street View calibration views (September 2014): rampart, bridge (camera resected), courtyard (resected)
 street_view_camera('144_Castle_Cal_Rampart',56.6575075,16.354454,63,7,75,ZR+1.95,'height'),
 street_view_camera('145_Castle_Cal_Bridge',*from_local(-912.1,-231.86),124,15,75,ZD+2.3,'height'),
 street_view_camera('146_Castle_Cal_Courtyard',*from_local(-862.78,-293.2),161,5,75,ZC+1.9,'height'),
 ('147_Castle_Aerial_SE',(-790.0,-470.0,62.0),(-870.0,-308.0,16.0),24),
 ('148_Castle_From_Station',(-598.0,-302.0,1.75),(-870.0,-306.0,19.0),40),
 ('149_Castle_Aerial_NW',(-1010.0,-150.0,95.0),(-868.0,-300.0,8.0),24),
 ('150_Castle_Kuretornet',(-906.0,-258.0,ZR+1.7),(-879.0,-286.0,zh(34.0)),24),
]
print('CASTLE27_GEOMETRY',len(castle27_names))
