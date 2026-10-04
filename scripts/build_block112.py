"""Pass 112: a correction pass. Four meshes that earlier passes built are deleted and re-created:
- 91846945 (pass 109 built it as a generic 9.75 m volume): the block between Larmgatan, Norra
  Långgatan and Västra Vallgatan.
  - The restaurant at 9 Larmgatan: white render over a salmon ground floor and base band, five
    arched upper windows under black dome awnings, a salmon cornice, a low hip roof, the black
    terrace awning on posts with a glass screen, a salmon pilaster at the north end;
  - the range on Norra Långgatan south of it: the east part continues the restaurant's front on
    Larmgatan (one window with a French balcony seen) and turns its salmon gable to Larmgatan
    under a red saddle roof running east-west; the west part, at Västerport, is the cream
    three-storey house with red-brown corner and bay pilasters, a red-brown cornice and string
    course, grouped white windows and a black awning over the ground floor;
  - the cream two-storey house north of the restaurant under a red tile saddle roof;
  - the back parts plain (not seen).
- 91072716 (pass 111): Gamla vattentornet, re-measured on a Google photo of the whole tower and
  checked against a winter photo from the moat. The shaft is not lengthened; the tower stands
  54.0 m to its merlons (see the notes: the Google pano does not allow 65 m). The brick shaft
  stands on a 5 m stone base in place of the rampart the terrain lacks, tapers slightly under a
  wider crown, and has paired narrow windows in eight columns and the bands read in the photos.
- 92204191 (pass 105 modelled it green with an orange saddle): the beige rendered two-storey house
  with a cornice, white window surrounds, a door, a red-brown hip roof and a large box dormer with
  a four-light window towards Kaggensgatan.
- 93238202 (pass 100): the pale grey cottage, unchanged in design, every height 0.5 m lower.

References: four Google Street View photos (three panoramas, resected), view only. Zones:
source/block112.json; see references/block112-notes.md. Signs' lettering, lamps, tables, chairs,
plants, flags and pipes are omitted.
"""
B112D=json.loads((R/'source/block112.json').read_text());Z=B112D['zones']
block112_names=[];B112={}
for old in [k for k in list(materials) if k.startswith('M_Block112_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 # Shared (the keys pass 100's and pass 82's helpers read from M).
 ('White','TownPaintWhite',(.94,.94,.92),.55,0),('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),
 ('Tile','TownTileRed',(.78,.42,.27),.80,0),('Stone','TownStone',(.55,.55,.54),.90,0),('Chimney','TownTileRed',(.55,.32,.26),.85,0),
 ('Zinc','TownMetalGrey',(.36,.37,.38),.55,.25),
 # 91846945.
 ('Render945','TownPaintWhite',(.92,.91,.88),.70,0),('Salmon','TownIvory',(.76,.44,.35),.85,0),('Canvas','TownPaintWhite',(.11,.11,.12),.75,0),
 ('AwnRed','TownPaintBrown',(.72,.16,.16),.65,0),('Post','TownPaintWhite',(.78,.79,.80),.50,0),('Frame945','TownMetalGrey',(.20,.20,.21),.50,.30),
 ('Cream945','TownIvory',(.90,.89,.83),.85,0),('Pilaster','TownIvory',(.62,.37,.30),.85,0),('CreamN','TownIvory',(.88,.85,.76),.85,0),
 ('Plinth945','TownStone',(.45,.44,.42),.90,0),
 # 91072716.
 ('Brick','TownTileRed',(.55,.27,.20),.90,0),('TStone','TownStone',(.70,.66,.58),.90,0),('Cap','TownMetalGrey',(.30,.31,.32),.55,.30),
 # 92204191.
 ('Beige','TownIvory',(.75,.71,.57),.90,0),('Trim191','TownIvory',(.88,.86,.78),.85,0),('Frame191','TownMetalGrey',(.20,.22,.25),.50,.30),
 ('Roof191','TownTileRed',(.52,.26,.21),.80,0),('Plinth191','TownStone',(.42,.41,.38),.90,0),('Door191','TownMetalGrey',(.16,.16,.17),.50,.30),
 # 93238202 (pass 100's colours).
 ('PaleGrey','TownPaintWhite',(.80,.81,.78),.80,0),
 ]:
 name='M_Block112_'+key;B112[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block112_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B112;WH=M['White']

# The corrected meshes and the passes that built them.
CORRECTS112={'91846945':109,'91072716':111,'92204191':105,'93238202':100}
def b112_new(name,category):
 # Unconditional: the object an earlier pass built under this name is removed and re-created.
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block112_names.append(name);return Mesh(name,category)
def drop_degenerate_faces112(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block112_dropped={};block112_samples={}
def b112_finish(m,osm):
 obj=s21_finish(m)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 block112_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),6),len(f.verts)) for f in bm.faces if f.calc_area()<1e-9 or (max(e.calc_length() for e in f.edges)>0 and 2*f.calc_area()/max(e.calc_length() for e in f.edges)<1e-4)][:8]
 bm.free();block112_dropped[obj.name]=drop_degenerate_faces112(obj)
 obj['detail_pass']=112;obj['corrects_pass']=CORRECTS112[osm];obj['reference_notes']='references/block112-notes.md';obj['osm_way']=osm;return obj

def pt112(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def front112(zone,dx,dy):return [w for w in walls(zone,'outer') if outward(w)[0]*dx+outward(w)[1]*dy>.9]
def rest112(m,zone,skip,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, the other outer walls (not in skip) plain.
 H=Z[zone]['height']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  if any(w is s for s in skip):continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
def win112(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.10,sill=None):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40)
 if sill:facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sill,a)
def flatroof112(m,zone,ma,trim,z=None):
 # Flat roof (triangulated: the outlines can be concave) and a coping on the outer walls.
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height'] if z is None else z
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 if trim:
  for w in walls(zone,'outer'):
   x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+.12,L+.06,.12,.24,trim,a)
def dome112(m,x,y,u,zc,R,D,a,ma,k=12,n=4):
 # A dome awning over an arched window: a quarter ellipsoid on the wall face (half-width R,
 # springing at zc, reaching D out), open underneath; rings from the wall to a single tip.
 o0=.36;vs=[]
 for j in range(n):
  ph=j*(math.pi/2)/n;c,s=math.cos(ph),math.sin(ph)
  vs+=[lp(x,y,u+R*c*math.cos(t*math.pi/k),o0+D*s,zc+R*c*math.sin(t*math.pi/k),a) for t in range(k+1)]
 vs.append(lp(x,y,u,o0+D,zc,a));tip=len(vs)-1;fs=[]
 for j in range(n-1):
  for t in range(k):i=j*(k+1)+t;fs.append((i,i+1,i+k+2,i+k+1))
 for t in range(k):i=(n-1)*(k+1)+t;fs.append((i,i+1,tip))
 m.faces(vs,fs+[tuple(reversed(f)) for f in fs],ma)
def hiplid112(m,X,Y,w,d,z,rise,ang,ma):
 # A small hipped lid over a w x d box (w along ang): ridge along w, inset d/2 at each end.
 c,s=math.cos(ang),math.sin(ang);P=lambda du,dv,zz:(X+du*c-dv*s,Y+du*s+dv*c,zz)
 r=max(.05,w/2-d/2)
 vs=[P(-w/2,-d/2,z),P(w/2,-d/2,z),P(w/2,d/2,z),P(-w/2,d/2,z),P(-r,0,z+rise),P(r,0,z+rise)]
 fs=[(0,1,5,4),(2,3,4,5),(1,2,5),(3,0,4)]
 m.faces(vs,fs+[tuple(reversed(f)) for f in fs],ma)

# ==== 91846945. All fronts on Larmgatan use s along the street from the south-east corner
# (-295.37, 75.19) northwards. Measured from the resected panorama r12kdG9 (camera -288.48, 98.83,
# h 2.4, pitch read as 6.5 from the verticals): base band 3.15-3.85, upper window sills 4.9,
# arches and awnings to 7.15, cornice 8.0-8.75; window axes at y 95.3/98.2/101.1/103.9/106.8;
# the restaurant's north end at y 110.55; the window at y 90.1 (4.3-6.3) and the gable rake on
# the south part from the 250-heading view of the same panorama.
SA,SB=(-295.37,75.19),(-295.21,126.98)
m=b112_new('SM_Kvarnholmen_House_91846945','Kvarnholmen/Larmgatan')
RN=M['Render945'];SN=M['Salmon'];FR=M['Frame945'];CV=M['Canvas']
def larm112(w,ups,grounds,H,arched,pil_n=False):
 # A white rendered Larmgatan front over a salmon ground floor. ups: s of the upper windows;
 # grounds: (s, width, bottom, height, door?) ground openings.
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt112(SA,SB,s))
 if arched:hu=[(S(s),4.90,1.25,1.45,.60) for s in ups]
 else:hu=[(S(s),4.30,1.40,2.00,0) for s in ups]
 hg=[(S(s),b,ww,hh,0) for s,ww,b,hh,d in grounds]
 bz_wall(m,w['p'],w['q'],0,3.15,hg,SN);bz_wall(m,w['p'],w['q'],3.15,H,hu,RN)
 for (u,b,ww,hh,r) in hu:
  if arched:
   archwin105(m,x,y,u,b,ww,hh,r,a,WH,None,2)
   dome112(m,x,y,u,b+hh-.05,.72,.62,a,CV);facade_box(m,x,y,u,.40+.62*.55,b+hh+.42,.80,.04,.10,M['AwnRed'],a)
   facade_box(m,x,y,u,.47,b-.05,ww+.24,.16,.06,WH,a)
  else:
   win112(m,x,y,u,b,ww,hh,a,WH,None,3,.10,WH)
   # The French balcony: a black rail across the lower part.
   for zz in (b+.10,b+.95):facade_box(m,x,y,u,.52,zz,ww+.20,.04,.04,M['Dark'],a)
   for k in range(9):facade_box(m,x,y,u-ww/2+k*ww/8,.52,b+.52,.02,.02,.86,M['Dark'],a)
 for (u,b,ww,hh,r),(s,_,_,_,d) in zip(hg,grounds):
  if d:door83(m,x,y,u,b,ww,hh,a,FR,SN,glass=True)
  else:
   facade_box(m,x,y,u,.18,b+hh/2,ww,.02,hh,GLAZE,a)
   for q in (-ww/2+.05,ww/2-.05,0):facade_box(m,x,y,u+q,.22,b+hh/2,.08,.08,hh,FR,a)
   for zz in (b+.04,b+hh-.04):facade_box(m,x,y,u,.22,zz,ww,.08,.08,FR,a)
 facade_box(m,x,y,0,.42,3.50,L+.04,.14,.70,SN,a);facade_box(m,x,y,0,.40,.20,L+.02,.10,.40,M['Plinth945'],a)
 facade_box(m,x,y,0,.42,8.37,L+.04,.14,.75,SN,a);facade_box(m,x,y,0,.58,8.70,L+.30,.42,.12,SN,a)
 if pil_n:
  # The salmon pilaster at the restaurant's north end (y 110.0-110.55).
  facade_box(m,x,y,S(35.08),.45,5.575,.55,.16,4.85,SN,a)
 return x,y,L,a,S
# The restaurant: five arched windows at a 2.88 m pitch round s 25.95 (y 101.14).
R945=front112('r945',1,0)
for w in R945:
 ups=[25.95+k*2.88 for k in (-2,-1,0,1,2)]
 x,y,L,a,S=larm112(w,ups,[(s,1.70,.45,2.30,False) for s in (ups[0],ups[1],ups[3],ups[4])]+[(ups[2],1.40,0,2.60,True)],8.75,True,True)
 # The terrace: a black awning on posts with a glass screen, 3.6 m out.
 RT=(x,y,L,a,S)
rest112(m,'r945',R945,RN,WH,RN,2)
hip82(m,'r945',(-295.32,91.7),(-295.26,110.55),M['Zinc'])
# The south range, east part: the same front continued; one window measured (y 89.4-90.8),
# the others at the restaurant's pitch (estimated); the gable on Larmgatan, ridge east-west.
SE945=front112('se945',1,0)
for w in SE945:
 ups=[14.91-k*2.88 for k in range(5)]
 larm112(w,ups,[(s,1.50,.45,2.30,False) for s in ups[1:]]+[(ups[0],1.20,0,2.50,True)],8.75,False)
SS945=front112('se945',0,-1)
for w in SS945:
 # Norra Långgatan, not seen: the same treatment, estimated.
 x,y,L,a=sf_edge(w['p'],w['q']);n=5;ax=[-L/2+(k+.5)*L/n for k in range(n)]
 bz_wall(m,w['p'],w['q'],0,3.15,[(u,.45,1.50,2.30,0) for u in ax],SN);bz_wall(m,w['p'],w['q'],3.15,8.75,[(u,4.30,1.30,1.90,0) for u in ax],RN)
 for u in ax:win112(m,x,y,u,.45,1.50,2.30,a,FR,None,2);win112(m,x,y,u,4.30,1.30,1.90,a,WH,None,3,.10,WH)
 facade_box(m,x,y,0,.42,3.50,L+.04,.14,.70,SN,a);facade_box(m,x,y,0,.42,8.37,L+.04,.14,.75,SN,a);facade_box(m,x,y,0,.58,8.70,L+.30,.42,.12,SN,a)
rest112(m,'se945',SE945+SS945,RN,WH,RN,2)
saddle82(m,'se945',(-295.37,75.19),(-295.32,91.7),M['Tile'],SN,False,.40)
# The terrace in front of the restaurant (and on along the north house to y 118.5): a black
# awning from 3.1 m at the wall to 2.45 m 3.6 m out, posts and a low glass screen.
x,y,L,a,S=RT
for s0,s1 in ((17.8,35.36),(35.36,43.3)):
 u0,u1=S(s0),S(s1);uc=(u0+u1)/2;ww=abs(u1-u0)
 awning82(m,x,y,uc,2.90,ww,a,CV,.65,3.60);facade_box(m,x,y,uc,.42+3.60,2.20,ww,.03,.30,CV,a)
 n=max(1,round(ww/3.6))
 for k in range(n+1):
  u=uc-ww/2+k*ww/n;facade_box(m,x,y,u,.42+3.55,1.21,.10,.10,2.42,M['Post'],a)
 facade_box(m,x,y,uc,.42+3.55,.62,ww,.02,1.10,GLAZE,a);facade_box(m,x,y,uc,.42+3.55,1.20,ww,.06,.05,M['Post'],a)
# The south range, west part at Västerport (camera lI6Z resected by pass 109, -330.52, 69.57,
# h 2.05). s from the west corner (-325.24, 75.0) eastwards along Norra Långgatan: corner pilaster
# 0-0.5, window 1.46, pilaster 2.6-3.3, a group of three at 4.08/5.66/7.24 (the rest repeated,
# estimated); ground floor and string course to 3.25, windows 3.76-5.18 and 6.06-7.53 (1.0 wide),
# cornice 7.88-9.35, its lip to 9.6 at the corner.
WA,WB=(-325.24,75.0),(-310.1,75.09);CM=M['Cream945'];PL=M['Pilaster']
def west945(w,pils,wins,H):
 x,y,L,a=sf_edge(w['p'],w['q'])
 hs=[(u,b,1.0,1.45,0) for u in wins for b in (3.76,6.07)]
 bz_wall(m,w['p'],w['q'],0,3.10,[(u,.45,1.30,2.30,0) for u in wins[::2]],PL);bz_wall(m,w['p'],w['q'],3.10,H,hs,CM)
 for u,b,ww,hh,r in hs:win112(m,x,y,u,b,ww,hh,a,WH,WH,2,.08,WH)
 for u in wins[::2]:win112(m,x,y,u,.45,1.30,2.30,a,M['Dark'],None,1)
 for u0,u1 in pils:facade_box(m,x,y,(u0+u1)/2,.43,(3.25+7.88)/2,u1-u0,.16,7.88-3.25,PL,a)
 facade_box(m,x,y,0,.43,3.17,L+.04,.16,.16,PL,a)
 facade_box(m,x,y,0,.43,(7.88+H)/2,L+.04,.16,H-7.88,PL,a);facade_box(m,x,y,0,.62,H-.06,L+.36,.45,.18,PL,a)
 awning82(m,x,y,0,2.85,L-.6,a,CV,.55,1.6)
for w in front112('sw945',0,-1):
 S=lambda s:U(w,*pt112(WA,WB,s))
 pils=[(S(0),S(.5)),(S(2.6),S(3.3)),(S(8.35),S(9.05)),(S(14.35),S(15.1))]
 west945(w,pils,[S(s) for s in (1.46,4.08,5.66,7.24,10.13,11.71,13.29)],9.35)
SW945=[w for w in walls('sw945','outer') if outward(w)[0]<-.9 and sf_edge(w['p'],w['q'])[2]>6]
for w in SW945:
 # The west face on Västra Vallgatan (seen edge-on only): the same design, estimated.
 x,y,L,a=sf_edge(w['p'],w['q'])
 west945(w,[(L/2-.5,L/2),(-L/2,-L/2+.5),(-.35,.35)],[-L/2+1.6,-L/2+3.3,L/2-3.3,L/2-1.6],9.35)
rest112(m,'sw945',front112('sw945',0,-1)+SW945,CM,WH,CM,3)
hip82(m,'sw945',WA,WB,M['Tile'])
# The rear piece and the north house's back part: plain, flat (not seen).
rest112(m,'k945',[],RN,WH,RN,2);flatroof112(m,'k945',M['Zinc'],RN)
rest112(m,'nb945',[],M['CreamN'],WH,M['CreamN'],1);flatroof112(m,'nb945',M['Zinc'],M['CreamN'])
# The cream house north of the restaurant (y 110.55-127): upper windows 3.10-4.30, 1.3 wide at
# y 111.3/113.3/115.4/117.4 (on the wall line; the rest at the same pitch, estimated), eaves 5.2,
# a red tile saddle along the street, a chimney at y 113.2. The ground floor is behind the
# terrace awning (estimated).
CN=M['CreamN']
NF=front112('n945',1,0)
for w in NF:
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt112(SA,SB,s))
 ax=[S(36.14+k*2.0) for k in range(8)]
 hu=[(u,3.10,1.30,1.20,0) for u in ax];hg=[(u,.55,1.20,1.75,0) for u in ax[1::2]]+[(ax[0],0,1.10,2.30,0)]
 bz_wall(m,w['p'],w['q'],0,5.2,hu+hg,CN)
 for u,b,ww,hh,r in hu:win112(m,x,y,u,b,ww,hh,a,WH,WH,2,.08,WH)
 for u,b,ww,hh,r in hg[:-1]:win112(m,x,y,u,b,ww,hh,a,WH,WH,2,.08,WH)
 door83(m,x,y,ax[0],0,1.10,2.30,a,M['Dark'],WH,glass=True)
 facade_box(m,x,y,0,.40,.20,L+.02,.10,.40,M['Plinth945'],a);facade_box(m,x,y,0,.45,5.05,L+.06,.18,.30,WH,a)
rest112(m,'n945',NF,CN,WH,CN,2)
saddle82(m,'n945',(-295.26,110.55),(-295.21,126.98),M['Tile'],CN,True,.35)
chimney82(m,-297.9,113.2,6.6,8.6,M['Chimney'])
b112_finish(m,'91846945')

# ==== 91072716: Gamla vattentornet. Re-measured on the photo of the whole tower (pano lI6Z,
# camera resected by pass 109 at -330.52, 69.57, h 2.05, 52.9 m from the axis; the house corner
# 5.4 m away checks the camera): merlon tops 53.4, crown band 48.3, crown windows 44.4-47.6,
# corbel table 39.7-41.9, bands 39.4/38.6/36.0/32.1/30.2, slit windows 33.0-35.6 and 27.6-29.6
# in columns 22.5 degrees either side of the line to the camera. Radius from the silhouette:
# about 5.1-5.4 at 33-36 m, about 6.0 on the crown. Pass 111's other photo gave 54.5 m.
# The shaft is NOT lengthened to 65 m (see the notes); TOP112 is the merlon top.
m=b112_new('SM_Kvarnholmen_House_91072716','Kvarnholmen/Larmtorget');BK=M['Brick'];STN=M['TStone']
TX,TY=-331.30,122.45;TOP112=Z['t716']['top'];CR112=Z['t716']['height']
ST112=39.7;FT112=5.0
# The foot. The model's ground here is flat at z 0 (no rampart), but the winter photo from the
# moat puts the tower's visible foot about 5 m (4.6-5.3) above the street level the Google
# cameras stand on: the tower stands on the rampart. A battered stone base, 0-5.0 m, filling the
# OSM ring (radius 6.8), stands in for that raised ground; the brick shaft starts on it.
# Set FT112=0 to stand the brick shaft on the street level instead.
if FT112>.5:m.lathe(TX,TY,0,[(6.80,0),(6.60,FT112-.30),(6.70,FT112-.30),(6.70,FT112),(6.10,FT112)],STN,48)
# The shaft: radius 6.0 at its foot to 5.2 under the corbel table (lI6Z: 5.1-5.4 at 33-36 m; the
# moat photo: nearly straight, about 0.86-0.9 of the crown's width at 20-30 m).
rz112=lambda z:6.00-.80*(min(max(z,FT112),ST112)-FT112)/(ST112-FT112)
m.lathe(TX,TY,FT112,[(rz112(z),z-FT112) for z in (FT112,15,25,ST112)],BK,48)
# Stone bands: seen at 30.1/32.0/35.9/38.5 (lI6Z); the moat photo shows thin light bands all down
# the shaft, placed every 3.6 m below (estimated).
for z,h in ((8.6,.15),(12.2,.15),(15.8,.15),(19.4,.15),(23.0,.15),(26.6,.15),(30.1,.18),(32.0,.18),(35.9,.18),(38.5,.18)):
 r0=rz112(z);m.lathe(TX,TY,z,[(r0-.10,0),(r0+.08,0),(r0+.08,h),(r0-.10,h)],STN,48)
# Narrow windows in eight columns, each split by a transom into two stacked lights (the crown
# photo from the moat shows paired small windows): seen 33.0-35.6 and 27.6-29.6 (lI6Z); the moat
# photo shows the rows going on down to about 12 m, placed at the same 5.4 m step (estimated).
TH112=math.radians(23.3)
for j in range(8):
 th=TH112+j*math.tau/8;ang=th+math.pi/2
 for b,h in [(b,h) for b,h in ((33.0,2.6),(27.6,2.0),(22.2,2.0),(16.8,2.0),(11.4,2.0),(6.0,2.0)) if b>FT112+.5]:
  r0=rz112(b+h/2);x,y=TX+(r0-.355)*math.cos(th),TY+(r0-.355)*math.sin(th)
  facade_box(m,x,y,0,.37,b+h/2,.42,.03,h,GLAZE,ang)
  for s in (-1,1):facade_box(m,x,y,s*.29,.40,b+h/2,.16,.08,h+.32,STN,ang)
  for zz in (b-.08,b+h/2,b+h+.08):facade_box(m,x,y,0,.40,zz,.74 if zz!=b+h/2 else .42,.09,.16 if zz!=b+h/2 else .10,STN,ang)
# The door facing the annex (east), in a stone surround.
th=math.radians(-25);x,y=TX+(6.80-.355)*math.cos(th),TY+(6.80-.355)*math.sin(th);ang=th+math.pi/2
facade_box(m,x,y,0,.40,1.35,1.30,.10,2.70,M['Dark'],ang);surround36(m,x,y,0,0,1.30,2.70,ang,STN,.20,.42)
# The corbel table: a brick ring flaring out from the shaft (5.20) to the crown over brick corbels
# (the photo shows a brick arcade with light lines), thin stone rings at its foot and top.
m.lathe(TX,TY,ST112,[(5.15,0),(5.30,0),(5.30,.40),(5.97,1.70),(6.05,2.20),(5.80,2.20)],BK,48)
for z,r0 in ((ST112-.05,5.20),(41.72,6.00)):m.lathe(TX,TY,z,[(r0-.08,0),(r0+.10,0),(r0+.10,.16),(r0-.08,.16)],STN,48)
for j in range(32):
 th=j*math.tau/32;ang=th+math.pi/2
 for zz,dd,hh in ((40.15,.18,.40),(40.55,.32,.40),(40.95,.46,.40)):
  x,y=TX+(5.22+dd/2)*math.cos(th),TY+(5.22+dd/2)*math.sin(th);box(m,x,y,.30,dd,hh,zz,BK,ang)
# The brick crown, tall arched windows (44.4-47.6), bands, crenellated parapet, coping, cap.
m.lathe(TX,TY,41.90,[(5.95,0),(5.95,CR112-41.90)],BK,48)
for j in range(8):
 th=TH112+j*math.tau/8;ang=th+math.pi/2;x,y=TX+(5.95-.355)*math.cos(th),TY+(5.95-.355)*math.sin(th)
 facade_box(m,x,y,0,.37,(44.4+47.2)/2,.75,.04,2.80,GLAZE,ang)
 pts=[(.375*math.cos(t*math.pi/8),47.2+.375*math.sin(t*math.pi/8)) for t in range(9)]
 m.faces([lp(x,y,du,.37,zz,ang) for du,zz in pts],[tuple(range(9))],GLAZE)
 town_path(m,[lp(x,y,.47,.42,44.4,ang),lp(x,y,.47,.42,47.2,ang)]+[lp(x,y,.47*math.cos(t*math.pi/8),.42,47.2+.47*math.sin(t*math.pi/8),ang) for t in range(1,8)]+[lp(x,y,-.47,.42,47.2,ang),lp(x,y,-.47,.42,44.4,ang)],.06,STN)
 facade_box(m,x,y,0,.44,44.37,1.10,.14,.08,STN,ang)
 facade_box(m,x,y,0,.40,46.0,.75,.08,.10,STN,ang)
for z,h in ((44.2,.25),(48.2,.30),(CR112-.25,.25)):m.lathe(TX,TY,z,[(5.85,0),(6.06,0),(6.06,h),(5.85,h)],STN,48)
m.lathe(TX,TY,CR112,[(5.95,0),(5.95,.75),(5.55,.75),(5.55,0)],BK,48)
for j in range(24):
 th=(j+.5)*math.tau/24;ang=th+math.pi/2;x,y=TX+5.75*math.cos(th),TY+5.75*math.sin(th)
 box(m,x,y,.78,.40,TOP112-.08-(CR112+.75),CR112+.75,BK,ang);box(m,x,y,.90,.50,.08,TOP112-.08,STN,ang)
m.lathe(TX,TY,CR112+.10,[(5.56,0),(4.0,.50),(.25,1.30),(0,1.30)],M['Cap'],48)
# The annex on the east side: a brick porch with a door and a flat roof (estimated, as pass 111).
for w in walls('a716','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 door=ox>.8 and L>2.5
 bz_wall(m,w['p'],w['q'],0,Z['a716']['height'],[(0,0,1.10,2.30,0)] if door else [],BK)
 if door:door83(m,x,y,0,0,1.10,2.30,a,M['Dark'],STN,glass=True)
 facade_box(m,x,y,0,.42,Z['a716']['height']-.15,L+.06,.16,.30,STN,a)
flatroof112(m,'a716',M['Cap'],None)
b112_finish(m,'91072716')

# ==== 92204191: the beige house. s along the Kaggensgatan front from the south-east corner
# (-190.79, 218.03) northwards. Camera of the 40 Kaggensgatan panorama (pass 108: -184.60,
# 236.50, h 2.40); readings shifted by -0.4 along the front (the NE corner read at 13.85-14.22
# against 13.58) and heights taken above the house's own base (it read at 0.42): plinth 0.30,
# ground windows 1.09-2.54 at 9.96/12.38, the door to 2.46 at 8.35, upper windows 3.68-5.26 at
# 7.39/9.92/12.41, cornice 5.85-6.45. The dormer: front 6.6-9.6, four lights about 7.3-8.4,
# lid to about 9.6 (scaled to a face 1.0 m behind the wall).
A1,B1=(-190.79,218.03),(-190.91,231.61);BG=M['Beige'];T1=M['Trim191'];F1=M['Frame191']
m=b112_new('SM_Kvarnholmen_House_92204191','Kvarnholmen/Kaggensgatan');H=Z['h191']['height']
def front191(w,ups,gws,door=None):
 x,y,L,a=sf_edge(w['p'],w['q'])
 hu=[(u,3.68,1.25,1.58,0) for u in ups];hg=[(u,1.09,1.25,1.45,0) for u in gws]
 hd=[(door,.30,1.15,2.16,0)] if door is not None else []
 bz_wall(m,w['p'],w['q'],0,H,hu+hg+hd,BG)
 for u,b,ww,hh,r in hu+hg:win112(m,x,y,u,b,ww,hh,a,F1,T1,2,.12,T1)
 if door is not None:door83(m,x,y,door,.30,1.15,2.16,a,M['Door191'],T1,glass=False);steps82(m,x,y,door,1.15,.30,a,M['Plinth191'])
 facade_box(m,x,y,0,.40,.15,L+.02,.10,.30,M['Plinth191'],a)
 facade_box(m,x,y,0,.42,H-.30,L+.04,.14,.55,T1,a);facade_box(m,x,y,0,.48,H-.06,L+.16,.26,.10,T1,a)
 return x,y,L,a
for w in front112('h191',1,0):
 S=lambda s:U(w,*pt112(A1,B1,s))
 x,y,L,a=front191(w,[S(s) for s in (2.39,4.89,7.39,9.92,12.41)],[S(s) for s in (2.39,4.89,9.96,12.38)],S(8.35))
 F191=(x,y,L,a,S)
for w in front112('h191',0,-1):
 # Strömgatan (pass 105 read the eaves at about 6.4 here): openings estimated.
 x,y,L,a=sf_edge(w['p'],w['q']);front191(w,[-2.4,0,2.4],[-2.4,0,2.4])
for w in front112('h191',0,1)+front112('h191',-1,0):
 # The north face (seen, blank but for one small high window) and the west face (not seen).
 x,y,L,a=sf_edge(w['p'],w['q'])
 if outward(w)[1]>.9:
  bz_wall(m,w['p'],w['q'],0,H,[(L/2-3.0,4.20,.60,.80,0)],BG);win112(m,x,y,L/2-3.0,4.20,.60,.80,a,F1,T1,1,.08)
  facade_box(m,x,y,0,.40,.15,L+.02,.10,.30,M['Plinth191'],a)
  facade_box(m,x,y,0,.42,H-.30,L+.04,.14,.55,T1,a);facade_box(m,x,y,0,.48,H-.06,L+.16,.26,.10,T1,a)
 else:front191(w,[-3.6,-1.2,1.2,3.6],[-3.6,3.6])
r191,sl191=hip82(m,'h191',A1,B1,M['Roof191'])
x,y,L,a,S=F191
# The dormer: a red-brown box 0.5 m behind the wall face, front s 6.5-9.3 up to 9.25 m, its north
# cheek sloping down to the roof at s 11.6; four lights 6.95-8.05.
u0,u1,u2=S(6.5),S(9.3),S(11.6);zr=H+.25
prism105(m,x,y,0,[(u0,zr),(u2,zr),(u1,9.25),(u0,9.25)] if u2>u0 else [(u2,zr),(u0,zr),(u0,9.25),(u1,9.25)],.355-.5,.355-.5-2.4,M['Roof191'],a)
for k in range(4):
 du=(u0+u1)/2+(k-1.5)*.62*(1 if u1>u0 else -1);facade_box(m,x,y,du,.355-.5+.01,7.50,.52,.02,1.10,GLAZE,a);cas81(m,x,y,du,6.95,.52,1.10,a,F1,.355-.5+.05,2)
facade_box(m,x,y,(u0+u1)/2,.355-.5-1.2,9.31,abs(u1-u0)+.20,2.6,.12,M['Sheet'],a)
X,Y,_=lp(x,y,S(12.6),.355-2.6,0,a);chimney82(m,X,Y,7.2,9.9,M['Chimney'])
b112_finish(m,'92204191')

# ==== 93238202: pass 100's cottage, rebuilt 0.5 m lower (zones g202 1.50/3.35, g202w 1.70/3.70,
# g202m 1.90). Pass 101 found the bpmqiA1 camera to stand about 0.5 m lower than the 2.54 m pass
# 100 used, so every height read from it drops by 0.5: the window too (0.65-1.60). No new photo.
m=b112_new('SM_Kvarnholmen_House_93238202','Kvarnholmen/Östra Vallgatan');PGR=M['PaleGrey'];WF=M['White']
A2,B2=(387.278,44.83),(387.899,50.687);H=Z['g202']['height'];T=Z['g202']['top'];F=fr100(A2,B2)
for w in fronts100(m,'g202',lambda ox,oy,x,y:ox>.9 and x>386.5,PGR,WF,WF,1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(A2,B2,s))
 holes=[(S(1.60),.65,1.00,.95,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,PGR);boards82(m,x,y,L,a,.42,H-.08,holes,PGR)
 win100(m,x,y,S(1.60),.65,1.00,.95,a,WF,WF,2)
 facade_box(m,x,y,0,.39,.20,L+.02,.08,.40,M['Stone'],a)
 for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+.40)/2,.16,.10,H-.40,WF,a)
sL,sR,sm,tface,sl=gable100(m,F,'g202',PGR,M['Tile'],WF);gable_boards100(m,F,sL,sR,sm,H,T,tface,PGR)
s0,s1,t0,t1=rect100(F,'g202');X,Y=P100(F,(s0+s1)/2,t1-2.5);chimney82(m,X,Y,T-.6,T+.9,M['Chimney'])
fronts100(m,'g202w',lambda *_:False,PGR,WF,WF,1);saddle82(m,'g202w',(369.359,44.94),(374.608,43.843),M['Tile'],PGR,along=False)
fronts100(m,'g202m',lambda *_:False,PGR,WF,WF,1);flatroof100(m,'g202m',M['Dark'],PGR)
b112_finish(m,'93238202')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block112_cameras=[
 sv_camera('559_Block112_Cal_Larmgatan9',-288.48,98.83,2.40,255,6.5,90),
 sv_camera('560_Block112_Cal_Vattentornet',-330.52,69.57,2.05,335,25,90),
 sv_camera('561_Block112_Cal_Kaggensgatan',-184.60,236.50,1.98,241,15,90),
 sv_camera('562_Block112_Cal_OstraVallgatan',395.01,42.20,2.05,222,15,90),
 ('563_Block112_Aerial',(-262.0,62.0,45.0),(-312.0,102.0,6.0),24),
]
print('BLOCK112_GEOMETRY',len(block112_names),'dropped',block112_dropped,block112_samples)
