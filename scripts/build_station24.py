"""Pass 24: Kalmar C station house. The two-storey 1874 range (Hjalmar Kumlien) and the
three-storey 1910 block with its round corner tower, clock roof and lantern, the lower south
wing and the platform canopy. References: Google Street View April 2025, Wikimedia Commons
photographs 2008-2025, an orthophoto reprojected into the local frame. Zones: source/station24.json.
Heights and hidden elevations are estimates; see references/station24-notes.md.
Tenant signs are omitted; the dates 1874 and 1910 and the station name are lettered.
"""
import ast
S24=json.loads((R/'source/station24.json').read_text());Z=S24['zones']
FO=tuple(S24['frame']['origin']);FU=tuple(S24['frame']['along']);FN=tuple(S24['frame']['depth'])
def fxy(a,d):return (FO[0]+FU[0]*a+FN[0]*d,FO[1]+FU[1]*a+FN[1]*d)
# Generic joinery and roof helpers written for pass 23.
tree=ast.parse((R/'scripts/build_baronen23.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'lin','ring_offset','walls','outward','bz_wall','bz_sill','inset_roof','roof_dormer','box','street_view_camera'}]
exec(compile(tree,'baronen23_helpers','exec'))
station24_names=[];ST={}
MEAN={'TownIvory':(.841,.824,.765),'TownPaintBlue':(.447,.535,.573),'TownMetalGrey':(.371,.421,.397),'TownPanel':(.776,.782,.726),
 'TownPaintWhite':(.841,.841,.801),'ChurchCopperFine':(.318,.489,.432),'Station24Slate':(.226,.228,.239)}
# Rebuilt every run so colour corrections reach the materials.
for old in [k for k in list(materials) if k.startswith('M_Station24_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Render','TownIvory',(.85,.79,.60),.86,0),
 ('Trim','TownIvory',(.89,.85,.71),.82,0),
 ('Copper','ChurchCopperFine',(.52,.62,.55),.58,.30),
 ('Slate','Station24Slate',(.226,.228,.239),.62,.05),
 ('Door','TownPaintBlue',(.36,.46,.60),.45,0),
 ('Steel','TownMetalGrey',(.17,.22,.28),.45,.50),
 ('Fascia','TownMetalGrey',(.22,.23,.24),.50,.40),
 ('Soffit','TownPanel',(.78,.78,.74),.70,0),
 ('Clock','TownPaintWhite',(.93,.93,.91),.35,0),
 ('Awning','TownPanel',(.06,.18,.52),.90,0),
 ('Sign','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Station24_'+key;ST[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['station24_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
RENDER,TRIM,COPPER,SLATE=ST['Render'],ST['Trim'],ST['Copper'],ST['Slate'];PLINTH=S20['DarkPlinth'];SIGN=ST['Sign'];ALU=TW

def st_new(name,category='Kvarnholmen/Stationen'):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 station24_names.append(name);return Mesh(name,category)
def st_finish(m):
 obj=s21_finish(m);obj['detail_pass']=24;obj['reference_notes']='references/station24-notes.md';obj['osm_way']='90965009;90965025';return obj
def side(w):
 ox,oy=outward(w);dots={'street':-(ox*FN[0]+oy*FN[1]),'track':ox*FN[0]+oy*FN[1],'nw':-(ox*FU[0]+oy*FU[1]),'se':ox*FU[0]+oy*FU[1]}
 return max(dots,key=dots.get)
def fill_corners(m,zone,ma,z0=0.0):
 # bz_wall builds its 35 cm layer outside the outline; add the missing square at convex corners.
 poly=[tuple(p) for p in Z[zone]['polygons'][0]];outer=[w for w in Z[zone]['walls'] if w['kind']=='outer']
 def on_outer(a,b):return any(math.dist(a,w['p'])<.05 and math.dist(b,w['q'])<.05 for w in outer)
 n=len(poly)
 for i in range(n):
  a,b,c=poly[i-1],poly[i],poly[(i+1)%n]
  if not(on_outer(a,b) and on_outer(b,c)):continue
  d1=(b[0]-a[0],b[1]-a[1]);d2=(c[0]-b[0],c[1]-b[1])
  if d1[0]*d2[1]-d1[1]*d2[0]<=1e-6:continue
  x,y,L,ang=sf_edge(a,b);H=min(w['z1'] for w in outer)
  facade_box(m,x,y,L/2+.1775,.18,(z0+H)/2,.355,.35,H-z0,ma,ang)

def arch_door(m,x,y,u,b,w,h,r,a,leaf=None):
 # Panelled leaves under a glazed fanlight, in a stone surround with a keystone.
 leaf=leaf or ST['Door']
 facade_box(m,x,y,u,.10,b+h/2,w,.08,h,leaf,a)
 for side_ in (-1,1):
  for zc,hh in ((b+h*.26,h*.34),(b+h*.70,h*.40)):town_border(m,*lp(x,y,u+side_*w/4,0,0,a)[:2],zc,w*.38,hh,a,leaf,.16,.03)
 facade_box(m,x,y,u,.15,b+h/2,.05,.06,h,leaf,a)
 contour=[(w/2*math.cos(k*math.pi/16),b+h+r*math.sin(k*math.pi/16)) for k in range(17)]
 m.faces([lp(x,y,u+q,.10,z,a) for q,z in contour],[tuple(range(17))],GLAZE)
 p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w,r,.06,.16,a,TW)
 p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w+.2,r+.1,.16,.40,a,TRIM)
 for side_ in (-1,1):facade_box(m,x,y,u+side_*(w/2+.09),.40,b+h/2,.18,.10,h,TRIM,a)
 facade_box(m,x,y,u,.44,b+h+r+.12,.28,.14,.34,TRIM,a)
 bb=max(b,.15);facade_box(m,x,y,u,.60,bb/2,w+.6,.5,bb,TS,a)
def arch_window(m,x,y,u,b,w,h,r,a):
 p18_win(m,x,y,u,b,w,h,r,a,TW,TRIM,3,2)
 facade_box(m,x,y,u,.44,b+h+r+.10,.24,.12,.30,TRIM,a)
def head_window(m,x,y,u,b,w,h,a,kind):
 # Upper-floor casement with a stepped architrave; the head differs by building period.
 s20_window(m,x,y,u,b,w,h,a,TW,TRIM,.72)
 if kind=='cornice':
  facade_box(m,x,y,u,.42,b+h+.25,w+.30,.12,.22,TRIM,a)
  facade_box(m,x,y,u,.47,b+h+.42,w+.52,.24,.10,TRIM,a)
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.15),.44,b+h+.22,.10,.16,.34,TRIM,a)
 elif kind=='lugged':
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.16),.41,b+h-.05,.18,.10,.34,TRIM,a)
  facade_box(m,x,y,u,.41,b+h+.16,w+.50,.10,.14,TRIM,a)
  m.faces([lp(x,y,u+q,.46,b+h+zz,a) for q,zz in ((-.16,.02),(.16,.02),(.21,.40),(-.21,.40))],[(0,1,2,3)],TRIM)
  facade_box(m,x,y,u,.44,b+h+.21,.36,.08,.38,TRIM,a)
 facade_box(m,x,y,u,.40,b-.30,w+.12,.08,.26,TRIM,a)
def pilaster(m,x,y,u,w,z0,z1,a,depth=.10):
 facade_box(m,x,y,u,.355+depth/2,(z0+z1)/2,w,depth,z1-z0,TRIM,a)
 facade_box(m,x,y,u,.355+depth+.03,z1-.10,w+.12,.06,.20,TRIM,a)
def text_on(m,x,y,u,z,a,text,width,ma,out=.49):
 # Raised lettering 15 mm deep: town_text's 4 mm extrusion is thinner than the finishing
 # bevel, and the bevel's overlap clamp then shrinks every bevel in the mesh to nothing.
 curve=bpy.data.curves.new('Temporary facade lettering','FONT');curve.body=text;curve.align_x='CENTER';curve.align_y='CENTER';curve.size=1;curve.extrude=.015;curve.resolution_u=3
 obj=bpy.data.objects.new('Temporary facade lettering',curve);bpy.context.collection.objects.link(obj);bpy.context.view_layer.update()
 scale=width/max(obj.dimensions.x,.01);deps=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(obj.evaluated_get(deps))
 # Font meshes carry coincident points and zero-length edges; merge and triangulate them first.
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-4)
 bmesh.ops.dissolve_degenerate(bm,dist=1e-4,edges=bm.edges);bmesh.ops.triangulate(bm,faces=list(bm.faces))
 bm.to_mesh(me);bm.free()
 xx,yy,_=lp(x,y,u,out,0,a)
 m.faces([facade_point(xx,yy,v.co.x*scale,.02+v.co.z,z+v.co.y*scale,a) for v in me.vertices],[tuple(p.vertices) for p in me.polygons if p.area*scale*scale>1e-8],ma)
 bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(me);bpy.data.curves.remove(curve)

# ---------------------------------------------------------------- 1874 range
def f1874(m,w):
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);sd=side(w)
 ng=3 if sd in ('street','track') else 1;cw,lw=.95,.78
 bounds=[-L/2+k*L/ng for k in range(ng+1)];axes=[]
 for g in range(ng):
  g0=bounds[g]+(cw if g==0 else lw)/2;g1=bounds[g+1]-(cw if g==ng-1 else lw)/2;st=(g1-g0)/3
  axes+=[g0+(k+.5)*st for k in range(3)]
 # Street: the entrance is the first axis of the far group; track: one door per group end.
 if sd=='street':doors={6}
 elif sd=='track':doors={0,4,8}
 else:doors=set()
 holes=[]
 for i,u in enumerate(axes):
  holes.append((u,.15,1.30,2.90,.65) if i in doors else (u,1.05,1.20,2.00,.60))
  holes.append((u,5.30,1.15,2.20,0))
 bz_wall(m,p,q,z0,H,holes,RENDER)
 for u,b,ww,hh,r in holes:
  if b<.5:arch_door(m,x,y,u,b,ww,hh,r,a)
  elif b<3:arch_window(m,x,y,u,b,ww,hh,r,a)
  else:head_window(m,x,y,u,b,ww,hh,a,'cornice')
 s20_plinth(m,x,y,L,a,holes,.5)
 for k,bd in enumerate(bounds):
  wd=cw if k in (0,len(bounds)-1) else lw;u=max(-L/2+wd/2,min(L/2-wd/2,bd))
  pilaster(m,x,y,u,wd,.5,H-.62,a)
 p18_band(m,x,y,L+.7,4.45,a,TRIM,.30)
 if sd=='street':text_on(m,x,y,(bounds[1]+bounds[2])/2,4.38,a,'1874',.46,TRIM)
 facade_box(m,x,y,0,.40,H-.95,L+.25,.08,.30,TRIM,a)
 lm_cornice(m,x,y,L+.9,H-.18,a,TRIM)

def copper_roof(m,corners,H,rise,ov=.45):
 # Hipped at the north-west end, abutting the 1910 block at the south-east end.
 A_,B_,C_,D_=[tuple(c) for c in corners]
 ax=((A_[0]-B_[0]),(A_[1]-B_[1]));Lr=math.hypot(*ax);ax=(ax[0]/Lr,ax[1]/Lr)
 mid_n=((B_[0]+C_[0])/2,(B_[1]+C_[1])/2);mid_s=((A_[0]+D_[0])/2,(A_[1]+D_[1])/2);half=math.dist(B_,C_)/2
 def push(p,frm,d):v=(p[0]-frm[0],p[1]-frm[1]);l=math.hypot(*v);return (p[0]+v[0]/l*d,p[1]+v[1]/l*d)
 out_b=(B_[0]-C_[0],B_[1]-C_[1]);ob=math.hypot(*out_b);out_b=(out_b[0]/ob,out_b[1]/ob)
 eB=(B_[0]+out_b[0]*ov-ax[0]*ov,B_[1]+out_b[1]*ov-ax[1]*ov);eA=(A_[0]+out_b[0]*ov,A_[1]+out_b[1]*ov)
 eD=(D_[0]-out_b[0]*ov,D_[1]-out_b[1]*ov);eC=(C_[0]-out_b[0]*ov-ax[0]*ov,C_[1]-out_b[1]*ov-ax[1]*ov)
 ze=H-ov*rise/half;zr=H+rise
 rN=(mid_n[0]+ax[0]*half,mid_n[1]+ax[1]*half);rS=mid_s
 planes=[([eB,eA,rS,rN],'s'),([eD,eC,rN,rS],'t'),([eC,eB,rN],'h')]
 for pts,_ in planes:
  zs=[ze if p in (eB,eA,eD,eC) else zr for p in pts];m.faces([(p[0],p[1],z) for p,z in zip(pts,zs)],[tuple(range(len(pts)))],COPPER)
 m.faces([(p[0],p[1],ze-.10) for p in (eB,eC,eD,eA)],[(0,1,2,3)],SIGN)
 for e0,e1 in ((eB,eA),(eC,eD),(eC,eB)):town_rod(m,(*e0,ze-.04),(*e1,ze-.04),.07,METAL,8)
 town_rod(m,(*rN,zr+.03),(*rS,zr+.03),.07,COPPER,8)
 for e,r_ in ((eB,rN),(eC,rN)):town_rod(m,(*e,ze+.02),(*r_,zr+.02),.05,COPPER,6)
 # Standing seams every 0.55 m: down the long planes (stopping at the hip lines near the
 # north-west end) and along the long axis on the hip. Frame: s along the ridge from the hip
 # eave, l across it from the ridge line; the plane is at ze on l=lat0 and zr on l=0.
 lat0=half+ov;total=math.dist(eB,eA);n=int(total/.55)
 def pt(s_,l,o):return (mid_n[0]+ax[0]*(s_-ov)+o[0]*l,mid_n[1]+ax[1]*(s_-ov)+o[1]*l)
 for k in range(1,n):
  s_=k*total/n;l1=max(0.0,lat0-s_)
  for sg in (1,-1):
   o=(out_b[0]*sg,out_b[1]*sg);town_rod(m,(*pt(s_,lat0,o),ze+.03),(*pt(s_,l1,o),ze+(zr-ze)*(1-l1/lat0)+.03),.018,COPPER,4)
 nh=int(2*lat0/.55)
 for k in range(1,nh):
  l=-lat0+k*2*lat0/nh;se=lat0-abs(l)
  town_rod(m,(*pt(0,l,out_b),ze+.03),(*pt(se,l,out_b),ze+(zr-ze)*se/lat0+.03),.018,COPPER,4)
 return ze,zr

# ---------------------------------------------------------------- 1910 block
def f1910(m,w,zone='main'):
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);sd=side(w)
 holes=[];plain=w['kind']=='upper' or L<2.5
 if not plain and zone=='main':
  n=7 if L>12 else max(1,round(L/2.6));st=(L-1.3)/n;axes=[-L/2+.65+(k+.5)*st for k in range(n)]
  if sd=='street':doors={n-1,n-2,1}
  elif sd=='track':doors={0,1}
  else:doors=set()
  for i,u in enumerate(axes):
   holes.append((u,.30,1.35,3.12,.675) if i in doors else (u,1.35,1.35,2.07,.675))
   holes.append((u,5.75,1.25,2.20,0));holes.append((u,9.60,1.20,2.06,0))
 elif not plain and zone=='wing':
  n=max(1,round(L/2.6));st=L/n;axes=[-L/2+(k+.5)*st for k in range(n)]
  for u in axes:
   holes.append((u,1.35,1.20,2.05,.60) if sd=='track' else (u,1.35,1.15,2.1,0));holes.append((u,5.75,1.15,2.2,0))
 bz_wall(m,p,q,z0,H,holes,RENDER)
 for u,b,ww,hh,r in holes:
  if b<.5:arch_door(m,x,y,u,b,ww,hh,r,a)
  elif b<3:arch_window(m,x,y,u,b,ww,hh,r,a) if r>0 else head_window(m,x,y,u,b,ww,hh,a,'plain')
  elif b<7:head_window(m,x,y,u,b,ww,hh,a,'lugged' if zone=='main' else 'plain')
  else:head_window(m,x,y,u,b,ww,hh,a,'plain')
 if z0<.5:
  s20_plinth(m,x,y,L,a,holes,.5)
  for s in (-1,1):
   if L>3:pilaster(m,x,y,s*(L/2-.45),.90,.5,H-.62,a,.12)
  p18_band(m,x,y,L+.7,5.50,a,TRIM,.32)
  if zone=='main':p18_band(m,x,y,L+.7,9.36,a,TRIM,.24)
  if sd=='street' and zone=='main':text_on(m,x,y,-L/2+.65+2.5*(L-1.3)/7,5.05,a,'1910',.48,TRIM,.37)
  if sd=='track' and zone=='main':
   # Station name board between ground and first floor, as photographed on the platform side.
   uc=-L/2+.65+4.5*(L-1.3)/7;facade_box(m,x,y,uc,.43,4.95,2.3,.06,.46,SIGN,a);text_on(m,x,y,uc,4.84,a,'Kalmar C',1.5,ST['Clock'],.47)
  if sd=='street' and zone=='main':
   # Flat entrance canopy over the two arched doors, on slender hangers.
   u0,u1=axes[-2],axes[-1];facade_box(m,x,y,(u0+u1)/2,1.05,4.38,u1-u0+1.9,1.4,.14,ST['Fascia'],a)
   for u in (u0-.9,u1+.9):town_rod(m,lp(x,y,u,1.65,4.43,a),lp(x,y,u,.40,5.4,a),.02,METAL,6)
  if sd=='track' and zone=='main':
   for u in axes[:5]:s21_shallow_awning(m,x,y,u,9.60+2.06+.18,1.40,a,ST['Awning'],.95)
 if zone=='main':facade_box(m,x,y,0,.40,H-.95,L+.25,.08,.30,TRIM,a);lm_cornice(m,x,y,L+.9,H-.18,a,TRIM,True)
 else:facade_box(m,x,y,0,.40,H-.80,L+.25,.08,.26,TRIM,a);lm_cornice(m,x,y,L+.9,H-.18,a,TRIM)

def poly_lathe(m,cx,cy,z,profile,ma,n=8,rot=0.0,smooth=False):
 v=[(cx+r*math.cos(rot+i*math.tau/n),cy+r*math.sin(rot+i*math.tau/n),z+h) for r,h in profile for i in range(n)]
 f=[tuple(range(n-1,-1,-1))]
 for j in range(len(profile)-1):
  for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 f.append(tuple(range((len(profile)-1)*n,len(profile)*n)));m.faces(v,f,ma,smooth)

def clock(m,x,y,u,z,a,r=.52,out=.30):
 # White dial, dark bezel, bronze numeral marks and hands.
 k=32;m.faces([lp(x,y,u+r*math.cos(t*math.tau/k),out,z+r*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],ST['Clock'])
 town_path(m,[lp(x,y,u+(r+.035)*math.cos(t*math.tau/k),out+.01,z+(r+.035)*math.sin(t*math.tau/k),a) for t in range(k+1)],.035,SIGN)
 for h_ in range(12):
  t=h_*math.tau/12;facade_box(m,x,y,u+.82*r*math.sin(t),out+.012,z+.82*r*math.cos(t),.035,.012,.10 if h_%3 else .16,SIGN,a)
 for ang,ln,wd in ((math.radians(-60),.62,.035),(math.radians(20),.82,.025)):
  e=(u+ln*r*math.sin(ang),z+ln*r*math.cos(ang));town_rod(m,lp(x,y,u,out+.02,z,a),lp(x,y,e[0],out+.02,e[1],a),wd/2,SIGN,6)

def clock_gable(m,x,y,u,a,H,slope):
 # The clock sits in a slate-hung gable that breaks the steep lower roof band.
 # The body starts where it leaves the band slope, as photographed (dark frame, copper hood).
 d=.10;zf=CLOCK_Z-.85;xx,yy,_=lp(x,y,u,-d,0,a);w=1.7;top=CLOCK_Z;crown=top+.62
 depth=(crown-zf)/slope+.5
 facade_box(m,xx,yy,0,-depth/2,(zf+top)/2,w,depth,top-zf,SLATE,a)
 prof=[(w/2*math.cos(t),top+(crown-top)*math.sin(t)) for t in [k*math.pi/14 for k in range(15)]]
 m.faces([lp(xx,yy,q,0,z,a) for q,z in prof],[tuple(range(len(prof)))],SLATE)
 for (q0,z0_),(q1,z1_) in zip(prof,prof[1:]):
  m.faces([lp(xx,yy,q0,.08,z0_,a),lp(xx,yy,q1,.08,z1_,a),lp(xx,yy,q1,-depth,z1_,a),lp(xx,yy,q0,-depth,z0_,a)],[(0,1,2,3)],COPPER)
 town_path(m,[lp(xx,yy,q,.10,z+.04,a) for q,z in prof],.05,COPPER)
 for s in (-1,1):facade_box(m,xx,yy,s*(w/2-.08),.04,(zf+top)/2,.16,.10,top-zf,COPPER,a)
 clock(m,xx,yy,0,top,a,.55,.07)

def main_roof(m):
 A15=S24['main_frame']['along'];D15=16.75
 rect=[fxy(0,0),fxy(0,D15),fxy(A15,D15),fxy(A15,0)]
 H=Z['main']['height'];band=Z['main']['band'];top=Z['main']['top'];ins=Z['main']['inset']
 inset_roof(m,rect,H,ins,band-H,SLATE,.50)
 inner=ring_offset(rect,-ins)
 cx=sum(p[0] for p in rect)/4;cy=sum(p[1] for p in rect)/4
 half=min(math.dist(inner[0],inner[1]),math.dist(inner[1],inner[2]))/2
 inset_roof(m,inner,band,half-1.25,top-band,SLATE,.14,SLATE)
 # Small square attic lights along the steep band on all four sides; the long street and
 # track sides carry the clock gables, as photographed on both.
 slope=(band-H)/(ins+.50);zc=ATTIC_Z;off=.50-(.50+ins)*((zc-H)/(band-H))
 for p0,p1 in zip(rect,rect[1:]+rect[:1]):
  x,y,L,a=sf_edge(p0,p1);long_side=abs(FU[0]*math.cos(a)+FU[1]*math.sin(a))>.9;count=8 if long_side else 7
  for k in range(count):
   u=-L/2+(k+.5)*L/count
   if long_side and abs(u)<1.6:continue
   facade_box(m,x,y,u,off-.25,zc,.62,.60,.62,SLATE,a);facade_box(m,x,y,u,off+.06,zc,.46,.04,.46,GLAZE,a)
   town_border(m,*lp(x,y,u,0,0,a)[:2],zc,.46,.46,a,TW,off+.08,.05)
  if long_side:clock_gable(m,x,y,0,a,H,slope)
 # Lantern: an octagon with small lights, a flared copper cap and a finial.
 rot=math.atan2(FU[1],FU[0])+math.pi/8;r=1.30
 poly_lathe(m,cx,cy,top-.05,[(r+.10,0),(r+.10,.18),(r,.18),(r,1.55),(r+.16,1.55),(r+.22,1.72)],SLATE,8,rot)
 for k in range(8):
  t=rot+(k+.5)*math.tau/8;ang=t+math.pi/2;rr=r*math.cos(math.pi/8)
  px,py=cx+rr*math.cos(t),cy+rr*math.sin(t);facade_box(m,px,py,0,.02,top+.85,.55,.04,.80,GLAZE,ang);town_border(m,px,py,top+.85,.55,.80,ang,TW,.04,.04)
 poly_lathe(m,cx,cy,top+1.67,[(r+.30,0),(r+.05,.20),(r*.72,.55),(r*.48,.95),(r*.22,1.25),(.10,1.35)],COPPER,8,rot)
 m.lathe(cx,cy,top+2.98,[(.09,0),(.16,.10),(.16,.26),(.06,.36),(.05,.95),(.02,1.0)],COPPER,12)

def tower(m):
 cx,cy=S24['tower']['centre'];r=S24['tower']['radius']*TOWER_SCALE;body=Z['tower']['body'];drum=Z['tower']['height'];top=Z['tower']['top']
 m.cylinder(cx,cy,0,r+.06,.5,PLINTH,32);m.cylinder(cx,cy,.5,r,body-.5,RENDER,32)
 for z,dr,h in ((4.48,.10,.14),(4.62,.16,.10),(body-.34,.08,.14),(body-.20,.16,.10),(body-.10,.24,.12)):m.cylinder(cx,cy,z,r+dr,h,TRIM,32)
 street=(-FN[0],-FN[1]);th0=math.atan2(street[1],street[0])
 def win(theta,b,w,h,kind):
  px,py=cx+r*math.cos(theta),cy+r*math.sin(theta);ang=theta+math.pi/2
  if kind=='door':
   facade_box(m,px,py,0,.06,b+h/2,w,.10,h,ST['Door'],ang)
   for s in (-1,1):facade_box(m,px,py,s*(w/2+.10),.10,b+h/2,.20,.14,h+.1,TRIM,ang)
   facade_box(m,px,py,0,.12,b+h+.14,w+.5,.18,.20,TRIM,ang);facade_box(m,px,py,0,.55,b-.08,w+.6,1.0,.16,TS,ang)
  elif kind=='oval':
   k=24;m.faces([lp(px,py,.34*math.cos(t*math.tau/k),.08,b+.46*math.sin(t*math.tau/k),ang) for t in range(k)],[tuple(range(k))],GLAZE)
   town_path(m,[lp(px,py,.40*math.cos(t*math.tau/k),.12,b+.52*math.sin(t*math.tau/k),ang) for t in range(k+1)],.06,TRIM)
  else:
   town_window(m,px,py,b+h/2,w,h,ang,TW,True,3,2,False)
   facade_box(m,px,py,0,.14,b-.08,w+.3,.30,.10,TRIM,ang)
 win(th0,.15,1.15,2.45,'door');win(th0-.55,2.35,0,0,'oval')
 for dt in (.50,-.55,-1.50):win(th0+dt,5.8,.90,1.60,'arch')
 # Slate-hung upper drum with round-headed lights, then the bell roof and a slim spire.
 rot=math.atan2(FU[1],FU[0])+math.pi/8
 poly_lathe(m,cx,cy,body,[(r*.98,0),(r*.98,drum-body)],SLATE,8,rot)
 for k in (0,1,2,6,7):
  t=rot+(k+.5)*math.tau/8;rr=r*.98*math.cos(math.pi/8);px,py=cx+rr*math.cos(t),cy+rr*math.sin(t)
  town_window(m,px,py,body+.85,.66,.95,t+math.pi/2,TW,True,2,2,False)
 poly_lathe(m,cx,cy,drum,[(r+.34,0),(r+.34,.14),(r+.10,.14),(r*.86,.55),(r*.62,1.35),(r*.46,2.30),(r*.40,2.95)],SLATE,8,rot)
 poly_lathe(m,cx,cy,drum+2.95,[(r*.42,0),(r*.30,.60),(r*.16,2.40),(.05,top-drum-3.25)],SLATE,8,rot)
 m.lathe(cx,cy,top-.30,[(.03,0),(.10,.08),(.10,.22),(.03,.30),(.025,1.05),(.012,1.10)],COPPER,12)
 facade_box(m,cx,cy,.22,0,top+.55,.42,.02,.24,COPPER,rot)

# ---------------------------------------------------------------- build
TOWER_SCALE=1.0
# Measured in the April 2025 front view: clock centre and the row of attic lights.
CLOCK_Z,ATTIC_Z=15.30,14.70
m=st_new('SM_Kvarnholmen_House_90965009')
for w in walls('range1874'):f1874(m,w)
fill_corners(m,'range1874',RENDER)
Hr=Z['range1874']['height'];ze,zr=copper_roof(m,S24['range1874']['corners'],Hr,Z['range1874']['top']-Hr)
slope1874=(Z['range1874']['top']-Hr)/(math.dist(S24['range1874']['corners'][0],S24['range1874']['corners'][3])/2)
for w in walls('range1874','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);sd=side(w)
 if sd=='street':
  g=-L/2+L/6
  for du in (-1.15,1.15):roof_dormer(m,x,y,g+du,a,Hr,slope1874,.55,.80,.95,SLATE,SLATE,TW,True)
 if sd=='track':roof_dormer(m,x,y,L/2-L/6,a,Hr,slope1874,.55,2.6,1.05,COPPER,COPPER,TW,False)
C0,C1,C2,C3=[tuple(c) for c in S24['range1874']['corners']]
# Two pairs of stacks, a copper-capped one beside a dark one, placed from the 205-degree view.
for t,cap in ((.30,True),(.39,False),(.53,True),(.575,False)):
 px=C0[0]+(C1[0]-C0[0])*t;py=C0[1]+(C1[1]-C0[1])*t;mx=(px+C3[0]+(C2[0]-C3[0])*t)/2;my=(py+C3[1]+(C2[1]-C3[1])*t)/2
 box(m,mx,my,.75,.62,1.9,zr-1.0,RENDER if cap else SIGN,math.atan2(C1[1]-C0[1],C1[0]-C0[0]),COPPER if cap else SIGN)
st_finish(m)

m=st_new('SM_Kvarnholmen_House_90965025')
for w in walls('main'):f1910(m,w,'main')
fill_corners(m,'main',RENDER)
main_roof(m)
for w in walls('wing'):f1910(m,w,'wing')
fill_corners(m,'wing',RENDER)
wing=[tuple(p) for p in Z['wing']['polygons'][0]];Hw=Z['wing']['height']
wx=[fxy(*q) for q in ((S24['main_frame']['along'],7.62),(S24['main_frame']['along'],16.06),(23.63,16.06),(23.70,7.62))]
inset_roof(m,wx[::-1] if (wx[1][0]-wx[0][0])*(wx[2][1]-wx[1][1])-(wx[1][1]-wx[0][1])*(wx[2][0]-wx[1][0])<0 else wx,Hw,2.25,Z['wing']['top']-Hw,SLATE,.45)
# Flat deck under the hip covers the strip between block and tower; inset_roof starts its slope
# at the overhang, so its surface on the wall line is ov*slope above the eave.
m.faces([(px,py,Hw+.05) for px,py in wing],[tuple(range(len(wing)))],SLATE)
ws=(Z['wing']['top']-Hw)/(2.25+.45)
tw=[w for w in walls('wing','outer') if side(w)=='track']
if tw:x,y,L,a=sf_edge(tw[0]['p'],tw[0]['q']);roof_dormer(m,x,y,0,a,Hw+.45*ws,ws,.6,.9,.95,SLATE,SLATE,TW,False)
tower(m)
st_finish(m)

# Platform canopy along the 1874 range, from just past its north-west end to the 1910 block.
m=st_new('SM_Station24_Canopy')
x,y,L,a=sf_edge(C2,C3)
u0,u1,dep,zw,zo=-L/2-1.2,L/2,4.3,3.95,4.40
m.faces([lp(x,y,u,o,z,a) for u,o,z in ((u0,.36,zw),(u1,.36,zw),(u1,dep,zo),(u0,dep,zo))],[(0,1,2,3)],ST['Fascia'])
m.faces([lp(x,y,u,o,z-.12,a) for u,o,z in ((u0,.36,zw),(u0,dep,zo),(u1,dep,zo),(u1,.36,zw))],[(0,1,2,3)],ST['Soffit'])
facade_box(m,x,y,(u0+u1)/2,dep,zo-.14,u1-u0+.08,.08,.52,ST['Fascia'],a)
facade_box(m,x,y,u0,(dep+.36)/2,(zw+zo)/2-.12,.08,dep-.36,.40,ST['Fascia'],a)
facade_box(m,x,y,(u0+u1)/2,.42,zw-.10,u1-u0,.14,.18,METAL,a)
ncol=6
for k in range(ncol):
 u=u0+.6+k*(u1-u0-1.2)/(ncol-1);zc=zw+(zo-zw)*(3.85-.36)/(dep-.36)-.14
 facade_box(m,x,y,u,3.85,zc/2,.18,.18,zc,ST['Steel'],a)
 facade_box(m,x,y,u,(3.85+.36)/2,zc-.12,.12,3.49,.22,ST['Steel'],a)
 town_rod(m,lp(x,y,u,3.85,zc-1.1,a),lp(x,y,u,2.7,zc-.2,a),.035,ST['Steel'],6)
 facade_box(m,x,y,u,3.85,.06,.34,.34,.12,TS,a)
st_finish(m)

station24_cameras=[
 street_view_camera('123_Station_Front',56.6618287,16.3603163,190,5),
 street_view_camera('124_Station_Tower',56.661716,16.3606067,240,6),
 street_view_camera('125_Station_Track',56.6614452,16.3596884,110,6,50,1.7),
 ('126_Station_Platform',(-450.0,-116.0,1.7),(-424.0,-100.0,6.5),20),
 ('127_Station_Aerial',(-360.0,-40.0,55.0),(-428.0,-100.0,6.0),28),
 street_view_camera('128_Station_Cal_Front',56.6618287,16.3603163,190,5,match='height'),
 street_view_camera('129_Station_Cal_Tower',56.661716,16.3606067,240,6,match='height'),
]
print('STATION24_GEOMETRY',len(station24_names))
