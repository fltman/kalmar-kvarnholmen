"""Pass 25: tracks, platforms and railway equipment at Kalmar C, from OpenStreetMap
(source/rail25.json by prepare_rail25.py). Rails (1435 mm gauge, 172 mm profile) on timber
sleepers every 0.6 m in a ballast bed cut into the island surface; platforms 0.58 m above rail
top with the edge zoning photographed on platforms 2b and 3; dwarf main signals on their mapped
side, facing their mapped direction; buffer stops; lattice portals and cantilever masts for the
overhead line; a rubber-panel pedestrian crossing with barriers. The island surface and one
street chunk are rebuilt around the cut. Positions follow OSM; equipment design is generic and
interpreted from photographs (references/rail25-notes.md).
"""
import ast
RD=json.loads((R/'source/rail25.json').read_text());LV=RD['levels']
RT,PT,BAL=LV['rail_top'],LV['platform_top'],LV['ballast'];RAIL_H=.172;RAIL_BASE=RT-RAIL_H;PLATE=.016;SLEEPER_TOP=RAIL_BASE-PLATE
tree=ast.parse((R/'scripts/build_baronen23.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'lin','box','street_view_camera'}]
exec(compile(tree,'baronen23_helpers','exec'))
# Cleaned lettering (merged, triangulated font mesh) from pass 24.
tree=ast.parse((R/'scripts/build_station24.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='text_on'];exec(compile(tree,'station24_text','exec'))
KD=json.loads((R/'source/kvarnholmen.json').read_text())
rail25_names=[];RM={}
MEAN={'TownStone':(.648,.628,.59),'TownMetalGrey':(.371,.421,.397),'TownPaintWhite':(.841,.841,.801),'TownPaintBlue':(.447,.535,.573),
 'TownPanel':(.776,.782,.726),'TownPaintBrown':(.471,.355,.281),'StreetSlabs':(.551,.534,.487),'Rail25Ballast':(.342,.307,.287),
 'Rail25Tactile':(.791,.791,.771),'Rail25Warning':(.796,.796,.776),'Rail25Timber':(.364,.316,.272)}
for old in [k for k in list(materials) if k.startswith('M_Rail25_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Ballast','Rail25Ballast',(.40,.37,.35),.95,0),
 ('BallastSlope','Rail25Ballast',(.38,.35,.33),.95,0),
 ('Gravel','Rail25Ballast',(.44,.41,.38),.95,0),
 ('Sleeper','Rail25Timber',(.27,.23,.20),.88,0),
 ('Rail','TownMetalGrey',(.25,.19,.15),.62,.55),
 ('RailTop','TownPaintWhite',(.62,.63,.64),.22,.95),
 ('Edge','TownStone',(.72,.72,.70),.80,0),
 ('Warning','Rail25Warning',(.80,.80,.78),.78,0),
 ('Slab','StreetSlabs',(.50,.50,.49),.82,0),
 ('Tactile','Rail25Tactile',(.70,.66,.56),.72,0),
 ('Wall','TownStone',(.60,.60,.57),.88,0),
 ('Rubber','TownStone',(.055,.055,.055),.92,0),
 ('Red','TownPanel',(.58,.07,.05),.55,0),
 ('Pole','TownMetalGrey',(.16,.18,.19),.50,.50),
 ('Galv','TownPaintWhite',(.56,.58,.59),.40,.80),
 ('Wire','TownMetalGrey',(.20,.15,.11),.45,.80),
 ('Blue','TownPaintBlue',(.12,.33,.66),.40,0),
 ('Roof','TownPaintWhite',(.74,.75,.75),.45,.30),
 ('Dial','TownPaintWhite',(.93,.93,.91),.35,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ('Yellow','TownPanel',(.93,.74,.06),.45,0),
 ('Lens','TownPaintWhite',(.09,.10,.10),.12,0),
 ('Insulator','TownPaintBrown',(.33,.17,.10),.25,0),
 ]:
 name='M_Rail25_'+key;RM[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['rail25_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)

def rl_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 rail25_names.append(name);return Mesh(name,category)
def rl_finish(m):
 # No crafted bevel here: thin rods and wires collapse its overlap clamp into zero-area faces,
 # and the platform tile courses and sleeper grain keep their authored UVs.
 obj=m.finish();obj['detail_pass']=25;obj['massing_only']=False;obj['reference_notes']='references/rail25-notes.md';return obj
def aligned(p,axis):
 # World-scale UVs turned to a platform's long axis: u across, v along (ribs run along v).
 c,s_=math.cos(axis),math.sin(axis);return ((-p[0]*s_+p[1]*c)/4,(p[0]*c+p[1]*s_)/4)
def tris(m,triangles,z,ma,axis=None):
 for t in triangles:
  v=[(p[0],p[1],p[2] if len(p)>2 else z) for p in t]
  if (Vector(v[1])-Vector(v[0])).cross(Vector(v[2])-Vector(v[0])).z<0:v.reverse()
  m.faces(v,[(0,1,2)],ma,uvcoords=None if axis is None else [aligned(p,axis) for p in v])
def quad(m,v,ma,out,uv=None):
 # A single face wound to look along `out` (the builder's normal pass leaves lone faces as wound).
 if (Vector(v[1])-Vector(v[0])).cross(Vector(v[2])-Vector(v[0])).dot(Vector(out))<0:v=v[::-1];uv=uv[::-1] if uv else None
 m.faces(v,[tuple(range(len(v)))],ma,uvcoords=uv)
def ring_walls(m,ring,z0,z1,ma):
 for p,q in zip(ring,ring[1:]+ring[:1]):m.faces([(p[0],p[1],z0),(q[0],q[1],z0),(q[0],q[1],z1),(p[0],p[1],z1)],[(0,1,2,3)],ma)
def wall_both(m,a,b,z0,z1a,z1b,ma):
 # A retaining face seen from both sides (crossing edges, the trimmed footway's cut edge).
 v=[(a[0],a[1],z0),(b[0],b[1],z0),(b[0],b[1],z1b),(a[0],a[1],z1a)];m.faces(v,[(0,1,2,3)],ma);m.faces(v[::-1],[(0,1,2,3)],ma)
def rod(m,a,b,r,ma,n=6):
 if math.dist(a,b)>.01:town_rod(m,a,b,r,ma,n)
def sweep(m,pts,profile,z,mats):
 # Extrude a closed cross-section (lateral u, height h) along a plan polyline with mitred frames.
 n=len(pts);frames=[]
 for i in range(n):
  a=pts[max(0,i-1)];b=pts[min(n-1,i+1)];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy) or 1;frames.append((-dy/l,dx/l))
 k=len(profile);v=[(pts[i][0]+frames[i][0]*u,pts[i][1]+frames[i][1]*u,z+h) for i in range(n) for u,h in profile]
 base=len(m.v);m.v.extend(v)
 for j in range(k):
  ma=mats[j]
  if ma not in m.mats:m.mats.append(ma)
  ix=m.mats.index(ma)
  for i in range(n-1):
   m.f.append((base+i*k+j,base+i*k+(j+1)%k,base+(i+1)*k+(j+1)%k,base+(i+1)*k+j));m.mi.append(ix);m.sm.append(False);m.fuv.append(None)
 for cap,order in ((0,range(k-1,-1,-1)),(n-1,range(k))):
  ma=mats[0];ix=m.mats.index(ma);m.f.append(tuple(base+cap*k+j for j in order));m.mi.append(ix);m.sm.append(False);m.fuv.append(None)
def inside(pt,poly):
 x,y=pt;c=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-12)+xi:c=not c
  j=i
 return c
def ground_at(pt):
 # Standing level for a mast or post: platform top, ballast inside the cut, else the island.
 if any(inside(pt,pl['polygon']) for pl in RD['platforms']):return PT
 if any(inside(pt,c['outer']) and not any(inside(pt,h) for h in c['holes']) for c in RD['cut']):return BAL
 return -.115
# Flat-bottom rail: foot 150 mm, web 16 mm, head 72 mm; the head's top face carries the polished steel.
RAIL=[(-.075,0),(.075,0),(.075,.013),(.009,.030),(.009,.127),(.036,.135),(.036,.172),(-.036,.172),(-.036,.135),(-.009,.127),(-.009,.030),(-.075,.013)]
RAIL_MATS=[RM['Rail']]*6+[RM['RailTop']]+[RM['Rail']]*5
def sleeper(m,x,y,a,k,dz):
 # Timber sleeper 2.6 x 0.26 x 0.16 m with its grain along the length; each takes its own patch.
 c,s_=math.cos(a),math.sin(a);ou,ov=(k*.6180339)%1*4,(k*.4142136)%1*4;P,Q=.13,1.3;z0,z1=SLEEPER_TOP-.16+dz,SLEEPER_TOP+dz
 W=lambda p,q,h:(x+p*c-q*s_,y+p*s_+q*c,h);D=lambda p,q:(p*c-q*s_,p*s_+q*c,0)
 quad(m,[W(-P,-Q,z1),W(P,-Q,z1),W(P,Q,z1),W(-P,Q,z1)],RM['Sleeper'],(0,0,1),[((q+ou)/4,(p+ov)/4) for p,q in ((-P,-Q),(P,-Q),(P,Q),(-P,Q))])
 for p in (-P,P):quad(m,[W(p,-Q,z0),W(p,Q,z0),W(p,Q,z1),W(p,-Q,z1)],RM['Sleeper'],D(p,0),[((q+ou)/4,(h+ov)/4) for q,h in ((-Q,z0),(Q,z0),(Q,z1),(-Q,z1))])
 for q in (-Q,Q):quad(m,[W(-P,q,z0),W(P,q,z0),W(P,q,z1),W(-P,q,z1)],RM['Sleeper'],D(0,q),[((p+ou)/4,(h+ov)/4) for p,h in ((-P,z0),(P,z0),(P,z1),(-P,z1))])

# ---------------------------------------------------------------- ground rebuilt around the cut
m=rl_new('SM_Kvarnholmen_Land','Kvarnholmen/Ground')
tris(m,RD['land_triangles'],-.115,'M_Ground')
for p in KD['island_outline']:
 for ring in [p['outer']]+p.get('holes',[]):ring_walls(m,ring,-1.25,-.115,TS)
rl_finish(m)
levels={'asphalt':(.013,'M_Kvarnholmen_Asphalt'),'stone':(.013,'M_Storgatan_Setts'),'path':(.015,'M_Storgatan_Slabs'),'sidewalk':(.105,'M_Storgatan_Slabs'),'curb':(.12,TS)}
m=rl_new('SM_Kvarnholmen_Street_07_09','Kvarnholmen/Streets')
for key,triangles in RD['street_07_09']['layers'].items():
 z,ma=levels[key];tris(m,triangles,z,ma)
 for poly in RD['street_07_09']['edges'].get(key,[]):
  for ring in [poly['outer']]+poly.get('holes',[]):ring_walls(m,ring,.008,z,ma)
# The footway surface stops at the cut: a face from below the island level up to it.
for a_,b_ in RD['street_07_09']['cut_walls']['path']:wall_both(m,a_,b_,-.13,.015,.015,levels['path'][1])
rl_finish(m)

# ---------------------------------------------------------------- bed and crossing
m=rl_new('SM_Rail25_Bed','Kvarnholmen/Järnväg')
tris(m,RD['bed_triangles'],BAL,RM['Ballast']);tris(m,RD['band_triangles'],BAL,RM['BallastSlope']);tris(m,RD['yard_triangles'],-.115,RM['Gravel'])
# Rubber panels between the outer rails, asphalt ramps beyond them (heights from prepare_rail25).
tris(m,RD['crossing_triangles']['flat'],None,RM['Rubber']);tris(m,RD['crossing_triangles']['ramp'],None,'M_Kvarnholmen_Asphalt')
for a_,b_ in RD['crossing_walls']:wall_both(m,a_,b_,BAL,a_[2],b_[2],RM['Wall'])
rl_finish(m)

# ---------------------------------------------------------------- rails and sleepers
groups={'SM_Rail25_Tracks_North':[],'SM_Rail25_Tracks_South':[]}
for t in RD['tracks']:
 xm=sum(p[0] for p in t['points'])/len(t['points']);groups['SM_Rail25_Tracks_North' if xm<-470 else 'SM_Rail25_Tracks_South'].append(t)
for name,group in groups.items():
 m=rl_new(name,'Kvarnholmen/Järnväg');k=0
 for t in group:
  # Where turnouts overlap two tracks' sleepers, a 1.5 mm step per track keeps the tops apart.
  dz=(RD['tracks'].index(t)%3)*.0015
  for r in t['rails']:
   if len(r)>=2:sweep(m,r,RAIL,RAIL_BASE,RAIL_MATS)
  for x,y,a in t['sleepers']:
   sleeper(m,x,y,a,k,dz);k+=1
   for sgn in (1,-1):
    # Tie plate under each rail foot.
    ox,oy=-math.sin(a)*sgn*RD['dimensions']['rail_offset'],math.cos(a)*sgn*RD['dimensions']['rail_offset']
    m.box((x+ox,y+oy,(SLEEPER_TOP+dz+RAIL_BASE)/2),(.20,.34,PLATE-dz),RM['Rail'],a)
 rl_finish(m)

# ---------------------------------------------------------------- platforms and furniture
m=rl_new('SM_Rail25_Platforms','Kvarnholmen/Järnväg')
ZONES=(('edge',RM['Edge']),('warning',RM['Warning']),('slabs',RM['Slab']),('tactile',RM['Tactile']))
for pl in RD['platforms']:
 tris(m,pl['zones']['surface'],PT,'M_Kvarnholmen_Asphalt')
 for key,ma in ZONES:tris(m,pl['zones'][key],PT,ma,pl['axis'])
 ring_walls(m,pl['polygon'],BAL,PT,RM['Wall'])
# Tall galvanised lighting columns with a slim luminaire, one row down the middle of each group of
# touching platforms (prepare_rail25 platform_groups).
for gr in RD['platform_groups']:
 for x,y,a,w in gr['lamps']:
  m.cylinder(x,y,PT,.085,8.2,RM['Galv'],12,.05);m.cylinder(x,y,PT,.16,.45,RM['Galv'],12)
  m.box((x,y,PT+8.25),(.62,.20,.09),RM['Galv'],a);m.box((x,y,PT+8.198),(.56,.15,.015),RM['Dial'],a)
# Island furniture on its centre line between lamps: two glass shelters on blue columns under a
# curved roof, the name board and the platform clock on its own column (platform 2b photograph).
island=next((gr for gr in RD['platform_groups'] if '2b' in gr['refs']),None)
ROOF=[(u,.05+.26*(1-(u/1.15)**2)) for u in [-1.15+2.3*i/10 for i in range(11)]]
ROOF=ROOF+[(u,h-.05) for u,h in reversed(ROOF)]
def between(i):
 (x0,y0,a,_),(x1,y1,_,_)=island['lamps'][i],island['lamps'][i+1];return (x0+x1)/2,(y0+y1)/2,a
if island and len(island['lamps'])>=5:
 k=len(island['lamps'])//2
 for cx,cy,a in (between(k),between(k-2)):
  ca,sa=math.cos(a),math.sin(a);L_=lambda du,dv:(cx+ca*du-sa*dv,cy+sa*du+ca*dv)
  for du in (-2.1,2.1):
   for dv in (-.8,.8):m.cylinder(*L_(du,dv),PT,.06,2.52,RM['Blue'],12)
  sweep(m,[L_(-2.35,0),L_(2.35,0)],ROOF,PT+2.5,[RM['Roof']]*len(ROOF))
  m.box((*L_(0,.84),PT+1.3),(4.2,.02,2.1),GLAZE,a)
  for du in (-2.12,2.12):m.box((*L_(du,.05),PT+1.3),(.02,1.55,2.1),GLAZE,a)
  m.box((*L_(0,.55),PT+.46),(3.2,.40,.05),RM['Pole'],a);m.box((*L_(0,.74),PT+.75),(3.2,.04,.40),RM['Pole'],a)
  for du in (-1.4,1.4):m.box((*L_(du,.55),PT+.22),(.05,.36,.44),RM['Pole'],a)
 bx,by,a=between(k-1);ca,sa=math.cos(a),math.sin(a)
 for du in (-.95,.95):m.cylinder(bx+ca*du,by+sa*du,PT,.045,2.9,RM['Galv'],10)
 m.box((bx,by,PT+2.6),(2.3,.06,.42),RM['Dark'],a)
 for aa in (a,a+math.pi):text_on(m,bx,by,0,PT+2.52,aa,'Kalmar C',1.5,RM['Dial'],.02)
 x,y,a=between(k+1);ca,sa=math.cos(a),math.sin(a);zc=PT+3.95
 m.cylinder(x,y,PT,.06,zc-.36-PT,RM['Galv'],12);m.cylinder(x,y,zc-.40,.035,.06,RM['Galv'],10)
 # Two-faced clock across the platform axis, dark rim, hands at ten past ten on both faces.
 rod(m,(x-ca*.045,y-sa*.045,zc),(x+ca*.045,y+sa*.045,zc),.34,RM['Dial'],24);rod(m,(x-ca*.035,y-sa*.035,zc),(x+ca*.035,y+sa*.035,zc),.37,RM['Dark'],24)
 for sgn in (1,-1):
  fx_,fy_=x+ca*sgn*.05,y+sa*sgn*.05;rx,ry=-sa*sgn,ca*sgn
  for deg,ln,r in ((60,.25,.011),(-60,.17,.016)):
   t=math.radians(deg);rod(m,(fx_,fy_,zc),(fx_+rx*ln*math.sin(t),fy_+ry*ln*math.sin(t),zc+ln*math.cos(t)),r,RM['Dark'],4)
rl_finish(m)

# ---------------------------------------------------------------- buffer stops, signals, overhead line, barriers
m=rl_new('SM_Rail25_Equipment','Kvarnholmen/Järnväg')
def track_dir_at(pt):
 best=None
 for t in RD['tracks']:
  ps=t['points']
  for a_,b_ in zip(ps,ps[1:]):
   dx,dy=b_[0]-a_[0],b_[1]-a_[1];l2=dx*dx+dy*dy or 1;u=max(0,min(1,((pt[0]-a_[0])*dx+(pt[1]-a_[1])*dy)/l2))
   d=math.dist(pt,(a_[0]+u*dx,a_[1]+u*dy))
   if best is None or d<best[0]:best=(d,math.atan2(dy,dx),t,a_,b_)
 return best
for bs in RD['buffer_stops']:
 d,ang,t,a_,b_=track_dir_at(bs['point']);x,y=bs['point']
 # Face the stop towards the track: pick the direction that points back along the rails.
 s0=math.dist(bs['point'],t['points'][0])<math.dist(bs['point'],t['points'][-1]);ang=ang+(0 if s0 else math.pi)
 fx,fy=math.cos(ang),math.sin(ang)
 m.box((x,y,RT+.95),(.34,2.3,.36),RM['Red'],ang);m.box((x+fx*.18,y+fy*.18,RT+.95),(.02,1.1,.12),RM['Dial'],ang)
 for sgn in (1,-1):
  ox,oy=-fy*sgn*.7535,fx*sgn*.7535
  rod(m,(x+ox,y+oy,RT+.78),(x+ox-fx*1.9,y+oy-fy*1.9,RAIL_BASE),.06,RM['Pole'],8)
  rod(m,(x+ox,y+oy,RT+.78),(x+ox-fx*.2,y+oy-fy*.2,RAIL_BASE),.06,RM['Pole'],8)
 m.box((x-fx*1.2,y-fy*1.2,BAL+.25),(1.6,2.6,.5),RM['Wall'],ang)
# Dwarf main signals (OSM railway:signal:main:height=dwarf) as photographed at Kac 14: a dark
# body with five lamp positions under visors, the red lamp top left, a yellow identity plate.
SIG={}
for sg in RD['signals']:
 x,y=sg['point'];wd=sg.get('way_dir')
 if wd is None:wd=track_dir_at(sg['point'])[1]
 travel=wd if sg['tags'].get('railway:signal:direction','forward')=='forward' else wd+math.pi
 side=-1 if sg['tags'].get('railway:signal:position','right')=='right' else 1
 px,py=x-math.sin(travel)*side*1.35,y+math.cos(travel)*side*1.35
 fx,fy=-math.cos(travel),-math.sin(travel);ang=math.atan2(fy,fx);rx,ry=-fy,fx;zb,zt=BAL+.50,BAL+1.32
 m.box((px,py,BAL+.04),(.30,.34,.10),RM['Wall'],ang);m.box((px,py,BAL+.30),(.10,.10,.42),RM['Dark'],ang)
 # Yellow only as a rim round the back, as on the photographed signal.
 m.box((px,py,(zb+zt)/2),(.18,.46,zt-zb),RM['Dark'],ang);m.box((px-fx*.08,py-fy*.08,(zb+zt)/2),(.04,.48,zt-zb+.02),RM['Yellow'],ang)
 m.box((px-fx*.101,py-fy*.101,(zb+zt)/2),(.006,.40,zt-zb-.06),RM['Dark'],ang)
 SIG[sg['tags'].get('ref','')]=(px,py,fx,fy,rx,ry)
 for row,hz in enumerate((.64,.42,.20)):
  for col,lat in enumerate((side*.11,-side*.11)):
   if (row,col)==(2,1):continue
   cx,cy,cz=px+fx*.09+rx*lat,py+fy*.09+ry*lat,zb+hz
   rod(m,(cx,cy,cz),(cx+fx*.03,cy+fy*.03,cz),.062,RM['Red'] if (row,col)==(0,0) else RM['Lens'],12)
   m.box((cx+fx*.05,cy+fy*.05,cz+.075),(.10,.15,.012),RM['Dark'],ang)
 m.box((px+fx*.055,py+fy*.055,zb-.10),(.01,.24,.16),RM['Yellow'],ang)
# Overhead line: lattice portals across tracks 1-3 (box girders of four chords with zigzag lacing
# on lattice masts), cantilever masts along track 1 elsewhere, contact and messenger wires.
CW,MW=RT+5.5,RT+6.8;GIRDER=MW+.55
def lattice_mast(x,y,z0,z1,ang):
 c,s_=math.cos(ang),math.sin(ang);h=.18;cs=[(x+c*du-s_*dv,y+s_*du+c*dv) for du,dv in ((-h,-h),(h,-h),(h,h),(-h,h))]
 for cx,cy in cs:m.box((cx,cy,(z0+z1)/2),(.055,.055,z1-z0),RM['Galv'],ang)
 n=max(2,round((z1-z0)/.55))
 for f in range(4):
  a_,b_=cs[f],cs[(f+1)%4]
  for i in range(n):
   p0,p1=(a_,b_) if i%2==0 else (b_,a_);rod(m,(p0[0],p0[1],z0+(z1-z0)*i/n),(p1[0],p1[1],z0+(z1-z0)*(i+1)/n),.014,RM['Galv'],6)
 m.box((x,y,z0+.02),(.52,.52,.04),RM['Galv'],ang)
 if z0==BAL:m.box((x,y,BAL+.15),(.7,.7,.3),RM['Wall'],ang)
def truss(p,q,z,ang):
 L=math.dist(p,q);c,s_=math.cos(ang),math.sin(ang);nx_,ny_=-s_,c;n=max(2,round(L/.9))
 for off in (-.25,.25):
  for zz in (z,z+.6):m.box(((p[0]+q[0])/2+nx_*off,(p[1]+q[1])/2+ny_*off,zz),(L,.06,.06),RM['Galv'],ang)
  for i in range(n):
   a_=(p[0]+c*L*i/n+nx_*off,p[1]+s_*L*i/n+ny_*off);b_=(p[0]+c*L*(i+1)/n+nx_*off,p[1]+s_*L*(i+1)/n+ny_*off)
   rod(m,(a_[0],a_[1],z+(.6 if i%2 else 0)),(b_[0],b_[1],z+(0 if i%2 else .6)),.016,RM['Galv'],6)
 for i in range(0,n+1,2):
  for zz in (z,z+.6):m.box((p[0]+c*L*i/n,p[1]+s_*L*i/n,zz),(.05,.5,.05),RM['Galv'],ang)
for pt in RD['portals']:
 (ix,iy),(ox_,oy_)=pt['inner'],pt['outer'];ang=math.atan2(oy_-iy,ox_-ix);c,s_=math.cos(ang),math.sin(ang)
 for x,y in ((ix,iy),(ox_,oy_)):lattice_mast(x,y,ground_at((x,y)),GIRDER+.6,ang)
 truss((ix-c*.2,iy-s_*.2),(ox_+c*.2,oy_+s_*.2),GIRDER,ang)
 for wx,wy in pt['wires']:
  rod(m,(wx,wy,GIRDER),(wx,wy,MW+.35),.03,RM['Galv'],8);rod(m,(wx,wy,MW+.35),(wx,wy,MW-.05),.055,RM['Insulator'],10)
  rod(m,(wx,wy,MW-.05),(wx,wy,CW+.02),.018,RM['Galv'],6)
portal_pts=[p['wires'][0] for p in RD['portals']]
for t in [t for t in RD['tracks'] if t['tags'].get('railway:track_ref')=='1']:
 ps=t['points'];acc=0.0
 for a_,b_ in zip(ps,ps[1:]):
  seg=math.dist(a_,b_);ang=math.atan2(b_[1]-a_[1],b_[0]-a_[0]);s=(45.0-acc%45.0)
  while s<seg:
   x=a_[0]+math.cos(ang)*s;y=a_[1]+math.sin(ang)*s
   if all(math.dist((x,y),q)>20 for q in portal_pts):
    lx,ly=-math.sin(ang),math.cos(ang);mx,my=x+lx*3.1,y+ly*3.1;base=ground_at((mx,my))
    # H-section mast, horizontal arm and diagonal strut with insulators at the mast.
    for off in (-.11,.11):m.box((mx+lx*off,my+ly*off,(base+MW+.6)/2),(.24,.02,MW+.6-base),RM['Galv'],ang)
    m.box((mx,my,(base+MW+.6)/2),(.02,.22,MW+.6-base),RM['Galv'],ang)
    if base==BAL:m.box((mx,my,BAL+.15),(.6,.6,.3),RM['Wall'],ang)
    rod(m,(mx-lx*.12,my-ly*.12,MW+.35),(x-lx*.1,y-ly*.1,MW+.35),.035,RM['Galv'],8)
    rod(m,(mx-lx*.12,my-ly*.12,CW-.1),(x+lx*.4,y+ly*.4,MW+.3),.03,RM['Galv'],8)
    for zz,dz in ((MW+.35,0),(CW-.1,(MW+.4-CW)/2.6*.4)):rod(m,(mx-lx*.15,my-ly*.15,zz),(mx-lx*.55,my-ly*.55,zz+dz),.05,RM['Insulator'],10)
    rod(m,(x,y,MW+.35),(x,y,CW+.02),.016,RM['Galv'],6)
   s+=45.0
  acc+=seg
for w in RD['wires']:
 ps=w['points'];acc=0.0;nxt=4.5
 for a_,b_ in zip(ps,ps[1:]):
  seg=math.dist(a_,b_)
  if seg<.05:continue
  rod(m,(*a_,CW),(*b_,CW),.007,RM['Wire'],6);rod(m,(*a_,MW),(*b_,MW),.008,RM['Wire'],6)
  # Droppers every 9 m of run.
  while nxt<acc+seg:
   f=(nxt-acc)/seg;x=a_[0]+(b_[0]-a_[0])*f;y=a_[1]+(b_[1]-a_[1])*f;rod(m,(x,y,MW),(x,y,CW),.004,RM['Wire'],4);nxt+=9.0
  acc+=seg
# Full barriers at the crossing (OSM crossing:barrier=full): a post at the top of each ramp on the
# approach's right, the red-and-white boom raised, two red lamps towards the path.
fw=RD['crossing_line'];CP=RD['crossing_profile'];ux,uy=fw[-1][0]-fw[0][0],fw[-1][1]-fw[0][1];ul=math.hypot(ux,uy);ux,uy=ux/ul,uy/ul;nx,ny=-uy,ux
for s,lat,facing in ((CP['s_lo']+.35,-1.55,-1),(CP['s_hi']-.35,1.55,1)):
 bx,by=fw[0][0]+ux*s+nx*lat,fw[0][1]+uy*s+ny*lat;top=CP['top_lo'] if facing<0 else CP['top_hi'];ang=math.atan2(uy,ux)
 m.box((bx,by,(BAL+top+1.15)/2),(.22,.22,top+1.15-BAL),RM['Dial'],ang)
 m.box((bx+ux*facing*.16,by+uy*facing*.16,top+1.0),(.10,.34,.20),RM['Dark'],ang)
 for dl in (-.09,.09):rod(m,(bx+ux*facing*.21+nx*dl,by+uy*facing*.21+ny*dl,top+1.0),(bx+ux*facing*.24+nx*dl,by+uy*facing*.24+ny*dl,top+1.0),.045,RM['Red'],10)
 m.box((bx-nx*lat/abs(lat)*.2,by-ny*lat/abs(lat)*.2,top+.85),(.16,.12,.30),RM['Dark'],ang)
 for k in range(9):m.box((bx-nx*lat/abs(lat)*.2,by-ny*lat/abs(lat)*.2,top+1.05+k*.31+.155),(.07,.07,.31),RM['Red'] if k%2==0 else RM['Dial'],ang)
rl_finish(m)

px,py,fx,fy,rx,ry=SIG.get('Kas 14',next(iter(SIG.values())))
rail25_cameras=[
 ('130_Rail_Platforms',(-470.0,-112.0,1.7),(-420.0,-150.0,2.5),20),
 ('131_Rail_Station',(-452.0,-128.0,1.7),(-432.0,-102.0,5.0),18),
 ('132_Rail_Crossing',(round(fw[0][0]+ux*(CP['s_lo']-1.6),3),round(fw[0][1]+uy*(CP['s_lo']-1.6),3),1.75),(round(fw[0][0]+ux*(CP['s_hi']+2),3),round(fw[0][1]+uy*(CP['s_hi']+2),3),.2),20),
 ('133_Rail_Buffers',(-395.0,-190.0,1.8),(-345.0,-222.0,1.0),24),
 ('134_Rail_Aerial',(-330.0,-250.0,32.0),(-480.0,-80.0,0.0),24),
 ('135_Rail_North',(-520.0,-48.0,1.8),(-560.0,-8.0,1.0),22),
 ('136_Rail_Signal',(round(px+fx*3.6-rx*.9,3),round(py+fy*3.6-ry*.9,3),round(BAL+1.25,3)),(round(px,3),round(py,3),round(BAL+.75,3)),28),
]
print('RAIL25_GEOMETRY',len(rail25_names))
