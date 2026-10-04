"""Pass 104: Kaggensgatan at Fiskaregatan, the north side of Fiskaregatan and Strömgatan:
- 92204193, east front on Kaggensgatan: the cream boarded house at the Fiskaregatan corner with its
  gable to the street (white corner boards and pilasters, three bays of white casements, a small
  gable window); the white rendered link with the black glazed door and the dark glazed upper
  storey behind a black railing; the tan rendered two-storey house (Gardell) with shop windows, a
  belt course, a cornice and a steep black sheet roof with black box dormers;
- 92379265, west front on Kaggensgatan: the yellow boarded two-storey house with its gable to the
  street (Outnorth: green glazed door, shop windows under pale awnings, the dark sign board, grey
  awnings over the upper windows, a small gable window); the low white boarded shop with the glazed
  gable front and a diamond window; the grey boarded one-storey gable house with a big window and
  a fan light in the gable, red tiled roof;
- 92204176, north front on Fiskaregatan: the pale green stucco two-storey house (a shop window, the
  brown door up a flight of steps, a window, four upper windows, a belt course and a cornice under
  a low grey roof) and the cream house to the east with a red tiled roof and a red dormer;
- 550598948, north front on Strömgatan: the modern block: a red vertically boarded ground storey on
  a concrete plinth with shop windows in red frames, a glazed door and a black barred gate; two
  storeys of red render with white-framed windows, some with French balconies; a grey standing-seam
  metal top storey.
The unseen rest of each outline is kept low and plain with flat roofs (estimated).
References: Google Street View (three panoramas, resected), view only. Zones: source/block104.json;
see references/block104-notes.md. Cars, lamps, drainpipes, signs (except the shop sign boards),
the bicycle stands and the parking signs are omitted.
"""
B104D=json.loads((R/'source/block104.json').read_text());Z=B104D['zones']
block104_names=[];B104={}
for old in [k for k in list(materials) if k.startswith('M_Block104_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.92,.85,.66),.85,0),('White','TownPaintWhite',(.95,.95,.93),.55,0),('Trim','TownPaintWhite',(.93,.92,.88),.60,0),
 ('Tan','TownIvory',(.77,.67,.53),.90,0),('TanTrim','TownIvory',(.86,.80,.70),.85,0),('RoofBlack','TownMetalGrey',(.13,.13,.14),.50,.30),
 ('DormerBlack','TownMetalGrey',(.09,.09,.10),.50,.30),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
 ('Yellow','TownIvory',(.86,.72,.46),.85,0),('DoorGreen','TownPaintGreen',(.56,.65,.50),.60,0),('Awning','TownPaintWhite',(.90,.89,.85),.70,0),
 ('AwningGrey','TownPaintWhite',(.70,.70,.70),.70,0),('Sign','TownMetalGrey',(.17,.19,.24),.50,.20),('ShopRoof','TownMetalGrey',(.78,.78,.78),.55,.20),
 ('GreyBoard','TownPaintWhite',(.74,.75,.72),.80,0),('Tile','TownTileRed',(.80,.40,.27),.80,0),
 ('Stucco','TownIvory',(.73,.77,.70),.88,0),('StuccoTrim','TownIvory',(.80,.83,.77),.85,0),('Frame','TownPaintBrown',(.32,.24,.19),.60,0),
 ('Plinth','TownStone',(.58,.58,.56),.90,0),('RoofGrey','TownMetalGrey',(.33,.33,.35),.60,.20),
 ('Ivory176','TownIvory',(.88,.80,.60),.85,0),('DormerRed','TownPaintBrown',(.60,.22,.18),.60,0),('Gate','TownPaintBrown',(.42,.26,.18),.70,0),
 ('Render','TownIvory',(.56,.23,.17),.90,0),('RedBoard','TownPaintBrown',(.50,.20,.15),.80,0),('Concrete','TownStone',(.72,.71,.68),.90,0),
 ('Metal','TownMetalGrey',(.47,.49,.52),.45,.40),('FrameLight','TownPaintWhite',(.82,.82,.80),.55,0),('ShopFrame','TownPaintBrown',(.62,.27,.16),.60,0),
 ('Rest','TownIvory',(.82,.78,.70),.90,0),('RestWhite','TownPaintWhite',(.88,.88,.86),.80,0),('RoofDark','TownMetalGrey',(.22,.22,.23),.60,.20),('RoofFlat','TownMetalGrey',(.44,.44,.45),.80,.10),
 ('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),('Chimney','TownTileRed',(.60,.34,.27),.85,0),
 ]:
 name='M_Block104_'+key;B104[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block104_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M104=B104;WF104=M104['White']

def b104_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block104_names.append(name);return Mesh(name,category)
def drop_degenerate_faces104(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block104_dropped={};block104_samples={}
def b104_finish(m,osm):
 obj=s21_finish(m)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 block104_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),6),len(f.verts)) for f in bm.faces if f.calc_area()<1e-9 or (max(e.calc_length() for e in f.edges)>0 and 2*f.calc_area()/max(e.calc_length() for e in f.edges)<1e-4)][:5]
 bm.free();block104_dropped[obj.name]=drop_degenerate_faces104(obj)
 obj['detail_pass']=104;obj['reference_notes']='references/block104-notes.md';obj['osm_way']=osm;return obj

def on104(A,B,c,axis):
 # The point of the OSM front A-B at coordinate c along the given axis (0: x, 1: y).
 t=(c-A[axis])/(B[axis]-A[axis]);return (A[0]+(B[0]-A[0])*t,A[1]+(B[1]-A[1])*t)
def front104(zone,test):
 return [w for w in walls(zone,'outer') if test(*outward(w),*sf_edge(w['p'],w['q'])[:2])]
def rest104(m,zone,wall,frame,trim,levels,roof):
 # Unseen parts: plain casements on the outer walls, party walls above lower neighbours, flat roof.
 H=Z[zone]['height']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  plain(m,w,H,wall,frame,trim,levels,.9)
 flatroof102(m,zone,roof,trim)
def win104(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.10):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def glaze104(m,x,y,u,b,w,h,a,frame,o=.16,mull=()):
 # A shop window or glazed door: glass in a slim frame with optional mullions (offsets from u).
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04)+tuple(mull):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.08,frame,a)
KE104=lambda ox,oy,x,y:ox>.9 and x>-191.5           # 92204193: east front on Kaggensgatan
KW104=lambda ox,oy,x,y:ox<-.9 and x<-179.5          # 92379265: west front on Kaggensgatan
FN104=lambda ox,oy,x,y:oy>.9 and y>133.5            # 92204176: north front on Fiskaregatan
SN104=lambda ox,oy,x,y:oy>.9 and y>204.0            # 550598948: north front on Strömgatan

# ---- 92204193: cream gable house, link, tan house (y along the Kaggensgatan front).
A93,B93=(-190.78,146.4),(-190.43,175.91);F93=fr102(A93,B93)
m=b104_new(Z['c193']['mesh'],'Kvarnholmen/Kaggensgatan');CR=M104['Cream'];TR=M104['Trim']
H=Z['c193']['height'];T=Z['c193']['top']
for w in fronts102(m,'c193',KE104,CR,WF104,TR,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda yy:U(w,*on104(A93,B93,yy,1))
 ops=[(S(yy),b,1.42,hh) for yy in (148.8,151.6,154.4) for b,hh in ((.92,1.32),(3.80,1.26))]
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]
 bz_wall(m,w['p'],w['q'],0,H,holes,CR);boards82(m,x,y,L,a,.45,H-.10,holes,CR)
 for u,b,ww,hh in ops:win104(m,x,y,u,b,ww,hh,a,WF104,TR,2,.12)
 facade_box(m,x,y,0,.40,.22,L+.02,.08,.45,M104['Plinth'],a)
 corners102(m,x,y,L,a,.45,H,TR,.30)
 for yy in (150.2,153.0):facade_box(m,x,y,S(yy),.42,(.45+H)/2,.22,.08,H-.45,TR,a)
 facade_box(m,x,y,0,.42,3.30,L+.04,.12,.16,TR,a);facade_box(m,x,y,0,.44,H-.08,L+.10,.14,.18,TR,a)
sL,sR,sm,tface=gable102(m,F93,'c193',CR,M104['RoofDark'],TR)
gable_boards102(m,F93,sL,sR,sm,H,T,tface,CR,holes=[(sm,6.26,1.28,1.06)])
fw=front104('c193',KE104)[0];x,y,L,a=sf_edge(fw['p'],fw['q'])
flush102(m,x,y,U(fw,*on104(A93,B93,151.6,1)),6.26,1.28,1.06,a,WF104,2)
H=Z['l193']['height']
for w in fronts102(m,'l193',KE104,WF104,WF104,TR,1):
 x,y,L,a=sf_edge(w['p'],w['q'])
 bz_wall(m,w['p'],w['q'],0,3.55,[(0,.25,1.35,1.80,0)],WF104)
 glaze104(m,x,y,0,.25,1.35,1.80,a,M104['Dark'],.12,(0,))
 facade_box(m,x,y,0,.40,2.70,L+.02,.10,.30,TR,a)
 # The dark glazed upper storey behind a black railing on the link's roof.
 facade_box(m,x,y,0,.25,3.55+.92,L,.06,1.85,M104['Dark'],a);facade_box(m,x,y,-.15,.29,4.30,.90,.02,1.20,GLAZE,a)
 for zz in (3.62,4.60):facade_box(m,x,y,0,.42,zz,L,.05,.05,M104['Iron'],a)
 for k in range(int(L/.12)):facade_box(m,x,y,-L/2+.06+k*.12,.42,4.10,.02,.02,.95,M104['Iron'],a)
flatroof102(m,'l193',M104['RoofDark'],TR)
H=Z['b193']['height'];TA=M104['Tan'];TT=M104['TanTrim']
for w in fronts102(m,'b193',KE104,TA,WF104,TT,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda yy:U(w,*on104(A93,B93,yy,1))
 ups=[(S(161.26+k*2.46),3.95,1.15,1.35) for k in range(6)]
 shops=[(S(yy),.65,ww,1.65) for yy,ww in ((161.2,1.67),(163.6,1.80),(168.6,1.80),(171.1,1.80))]
 du=S(166.2);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+shops]+[(du,.10,1.20,2.35,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,TA)
 for u,b,ww,hh in ups:win104(m,x,y,u,b,ww,hh,a,WF104,TT,2,.14)
 for u,b,ww,hh in shops:glaze104(m,x,y,u,b,ww,hh,a,M104['Dark'],.16);facade_box(m,x,y,u,.44,b-.05,ww+.10,.16,.08,TT,a)
 door83(m,x,y,du,.10,1.20,2.35,a,M104['Dark'],TT,glass=True)
 facade_box(m,x,y,0,.40,.30,L+.02,.10,.60,M104['Plinth'],a)
 facade_box(m,x,y,0,.44,3.45,L+.04,.16,.18,TT,a)
 facade_box(m,x,y,0,.46,H-.18,L+.10,.22,.36,TT,a);town_rod(m,lp(x,y,-L/2,.72,H+.02,a),lp(x,y,L/2,.72,H+.02,a),.07,M104['Sheet'],8)
r,_,_=rect82('b193',A93,B93);saddle82(m,'b193',A93,B93,M104['RoofBlack'],TA,along=True)
half=min(math.dist(r[0],r[3]),math.dist(r[0],r[1]))/2;sl104=(Z['b193']['top']-H)/half
fw=front104('b193',KE104)[0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for k in range(6):
 dormer82(m,x,y,U(fw,*on104(A93,B93,161.26+k*2.46,1)),a,H,sl104,1.90,1.00,M104['DormerBlack'],WF104,M104['RoofBlack'],back=.55)
X,Y=on104(A93,B93,167.0,1);chimney82(m,X-6.0,Y,Z['b193']['top']-.7,Z['b193']['top']+.7,M104['Chimney'])
rest104(m,'r193',M104['Rest'],WF104,M104['Trim'],2,M104['RoofFlat'])
b104_finish(m,'92204193')

# ---- 92379265: yellow gable house, white glazed shop, grey gable house (y along the front).
A65,B65=(-179.99,170.32),(-180.45,146.51);F65=fr102(A65,B65)
m=b104_new(Z['y265']['mesh'],'Kvarnholmen/Kaggensgatan');YE=M104['Yellow']
H=Z['y265']['height'];T=Z['y265']['top']
for w in fronts102(m,'y265',KW104,YE,WF104,WF104,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda yy:U(w,*on104(A65,B65,yy,1))
 ups=[(S(yy),3.45,1.15,1.20) for yy in (153.2,151.2,149.2)]
 shops=[(S(yy),.60,1.75,1.65) for yy in (150.6,148.3)]
 du=S(153.65);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+shops]+[(du,.32,.95,1.95,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,YE);boards82(m,x,y,L,a,.40,H-.10,holes+[((S(150.6)+S(148.3))/2,2.70,4.4,.62,0)],YE)
 for u,b,ww,hh in ups:win104(m,x,y,u,b,ww,hh,a,WF104,WF104,2,.12);awning82(m,x,y,u,b+hh-.02,ww+.12,a,M104['AwningGrey'],.30,.35)
 for u,b,ww,hh in shops:glaze104(m,x,y,u,b,ww,hh,a,WF104,.16,(0,));surround36(m,x,y,u,b,ww,hh,a,WF104,.12,.40);awning82(m,x,y,u,b+hh+.25,ww+.25,a,M104['Awning'],.55,.80)
 door83(m,x,y,du,.32,.95,1.95,a,M104['DoorGreen'],WF104,glass=True);steps82(m,x,y,du,.95,.32,a,M104['Plinth'])
 # The dark sign board over the shop windows.
 su=(S(152.6)+S(148.0))/2;facade_box(m,x,y,su,.45,3.00,abs(S(152.6)-S(148.0)),.06,.55,M104['Sign'],a)
 facade_box(m,x,y,0,.40,.20,L+.02,.08,.40,M104['Plinth'],a)
 corners102(m,x,y,L,a,.40,H,WF104,.28)
 facade_box(m,x,y,0,.44,H-.12,L+.10,.12,.22,WF104,a)
sL,sR,sm,tface=gable102(m,F65,'y265',YE,M104['Tile'],WF104)
gable_boards102(m,F65,sL,sR,sm,H,T,tface,YE,holes=[(sm,5.45,.80,.85)])
fw=front104('y265',KW104)[0];x,y,L,a=sf_edge(fw['p'],fw['q'])
flush102(m,x,y,U(fw,*P102(F65,sm)),5.45,.80,.85,a,WF104,2)
# The white boarded shop: flat roof at 2.7 m, the glazed gable front (y 156.12-162.04) with its own
# short saddle roof running back 6 m.
H=Z['w265']['height']
for w in fronts102(m,'w265',KW104,WF104,WF104,WF104,1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda yy:U(w,*on104(A65,B65,yy,1))
 gu=(S(156.12)+S(162.04))/2;gw=abs(S(162.04)-S(156.12));du=S(162.45)
 holes=[(gu,.47,gw-.30,H-.47,0),(du,.30,.80,1.95,0),(S(155.85),1.30,.40,.40,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,WF104);boards82(m,x,y,L,a,.40,H-.08,holes,WF104)
 glaze104(m,x,y,gu,.47,gw-.30,H-.47,a,WF104,.20,(-gw/4,0,gw/4))
 facade_box(m,x,y,gu,.20,1.55,gw-.30,.08,.08,WF104,a)
 door83(m,x,y,du,.30,.80,1.95,a,WF104,WF104,glass=False)
 facade_box(m,x,y,S(155.85),.30,1.50,.30,.02,.30,GLAZE,a)
 for s_ in (-1,1):facade_box(m,x,y,gu+s_*(gw/2-.08),.45,H/2,.20,.12,H,WF104,a)
 # The low platform in front of the shop window.
 facade_box(m,x,y,gu,.70,.18,gw+.2,.70,.36,M104['Plinth'],a)
flatroof102(m,'w265',M104['ShopRoof'],WF104)
s0,s1=sorted((F65['L']-(156.12-146.51)*F65['L']/(170.32-146.51),F65['L']-(162.04-146.51)*F65['L']/(170.32-146.51)))
_,_,tq0,tq1=rect102(F65,'w265');He,Hp=2.68,4.61;smid=(s0+s1)/2;tf=tq1+.355+.25;tb=tf-6.3;slw=(Hp-He)/((s1-s0)/2)
for se,sg in ((s0-.25,-1),(s1+.25,1)):
 ze=He-.25*slw
 m.faces([P102(F65,se,tb,ze),P102(F65,smid,tb,Hp+.08),P102(F65,smid,tf,Hp+.08),P102(F65,se,tf,ze)],[(0,1,2,3),(3,2,1,0)],M104['ShopRoof'])
 town_path(m,[P102(F65,se,tf-.03,ze+.05),P102(F65,smid,tf-.03,Hp+.12)],.09,WF104)
for tt,mm in ((tq1+.355,GLAZE),(tb+.25,WF104)):
 prism102(m,F65,[(s0,H),(s1,H),(smid,Hp-.02)],tt-.06 if mm==GLAZE else tt,tt if mm==GLAZE else tt+.06,mm)
for ss in (smid-(s1-s0)/4,smid,smid+(s1-s0)/4):
 zt=Hp-abs(ss-smid)*slw;town_rod(m,P102(F65,ss,tq1+.40,H),P102(F65,ss,tq1+.40,max(H+.05,zt-.05)),.05,WF104,6)
# Glazing bars in the gable triangle: the diagonal braces of the photo.
for sg in (-1,1):town_path(m,[P102(F65,smid+sg*(s1-s0)/2*.85,tq1+.40,H+.05),P102(F65,smid,tq1+.40,Hp-.30)],.05,WF104)
H=Z['g265']['height'];T=Z['g265']['top'];GB=M104['GreyBoard']
for w in fronts102(m,'g265',KW104,GB,WF104,WF104,1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda yy:U(w,*on104(A65,B65,yy,1))
 holes=[(S(165.9),.58,1.65,1.70,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,GB);boards82(m,x,y,L,a,.40,H-.08,holes,GB)
 win104(m,x,y,S(165.9),.58,1.65,1.70,a,WF104,WF104,2,.14)
 facade_box(m,x,y,0,.40,.20,L+.02,.08,.40,M104['Plinth'],a);corners102(m,x,y,L,a,.40,H,WF104,.28)
 facade_box(m,x,y,0,.44,H-.10,L+.10,.12,.20,WF104,a)
sL,sR,sm,tface=gable102(m,F65,'g265',GB,M104['Tile'],WF104)
gable_boards102(m,F65,sL,sR,sm,H,T,tface,GB,holes=[(sm,H+.25,1.10,.55)])
# The fan light: a half disc of glass with white radial bars.
k=12;zc=H+.30;cen=P102(F65,sm,tface+.03,zc)
m.faces([cen]+[P102(F65,sm+.55*math.cos(i*math.pi/k),tface+.03,zc+.55*math.sin(i*math.pi/k)) for i in range(k+1)],[tuple(range(k+2)),tuple(range(k+1,-1,-1))],GLAZE)
for i in range(0,k+1,3):town_path(m,[P102(F65,sm,tface+.06,zc),P102(F65,sm+.55*math.cos(i*math.pi/k),tface+.06,zc+.55*math.sin(i*math.pi/k))],.025,WF104)
town_path(m,[P102(F65,sm+.62*math.cos(i*math.pi/k),tface+.06,zc+.62*math.sin(i*math.pi/k)) for i in range(k+1)],.05,WF104)
rest104(m,'r265',M104['RestWhite'],WF104,M104['Trim'],2,M104['RoofFlat'])
b104_finish(m,'92379265')

# ---- 92204176: the pale green stucco house and the cream house with the red roof (x along the front).
A76,B76=(-132.0,134.34),(-149.76,134.74)
m=b104_new(Z['g176']['mesh'],'Kvarnholmen/Fiskaregatan');ST=M104['Stucco'];SM=M104['StuccoTrim'];FR=M104['Frame']
H=Z['g176']['height']
for w in fronts102(m,'g176',FN104,ST,FR,SM,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda xx:U(w,*on104(A76,B76,xx,0))
 ups=[(S(xx),4.98,1.30,1.85) for xx in (-142.7,-144.7,-146.75,-148.75)]
 low=[(S(-142.8),1.20,1.50,1.90)];shop=(S(-147.7),1.32,2.90,1.80);du=S(-144.9)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+low+[shop]]+[(du,.90,1.25,2.65,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,ST)
 for u,b,ww,hh in ups:win104(m,x,y,u,b,ww,hh,a,FR,SM,3,.12)
 for u,b,ww,hh in low:win104(m,x,y,u,b,ww,hh,a,FR,SM,3,.12)
 glaze104(m,x,y,shop[0],shop[1],shop[2],shop[3],a,FR,.16);surround36(m,x,y,shop[0],shop[1],shop[2],shop[3],a,SM,.10,.40)
 facade_box(m,x,y,shop[0],.47,shop[1]-.05,shop[2]+.24,.16,.06,SM,a)
 door83(m,x,y,du,.90,1.25,2.20,a,FR,FR,glass=True);facade_box(m,x,y,du,.16,3.25,1.05,.02,.40,GLAZE,a)
 surround36(m,x,y,du,.90,1.25,2.65,a,FR,.10,.40);steps82(m,x,y,du,1.25,.90,a,M104['Plinth'])
 facade_box(m,x,y,0,.42,.27,L+.02,.14,.54,M104['Plinth'],a)
 facade_box(m,x,y,0,.46,4.05,L+.06,.22,.26,SM,a);facade_box(m,x,y,0,.43,3.70,L+.04,.14,.10,SM,a)
 facade_box(m,x,y,0,.50,H-.20,L+.12,.30,.40,SM,a);town_rod(m,lp(x,y,-L/2,.75,H+.02,a),lp(x,y,L/2,.75,H+.02,a),.07,M104['Sheet'],8)
 for uu in (-L/2+.25,L/2-.25):facade_box(m,x,y,uu,.43,(.54+H)/2,.50,.12,H-.54,SM,a)
saddle82(m,'g176',A76,B76,M104['RoofGrey'],ST,along=True)
IV=M104['Ivory176'];H=Z['y176']['height']
for w in fronts102(m,'y176',FN104,IV,WF104,TR,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda xx:U(w,*on104(A76,B76,xx,0))
 ups=[(S(xx),3.00,1.25,1.65) for xx in (-133.9,-136.9,-139.9)]
 low=[(S(xx),.90,1.25,1.55) for xx in (-133.9,-136.4)];gu=S(-139.3)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+low]+[(gu,0,2.0,2.05,.55)]
 bz_wall(m,w['p'],w['q'],0,H,holes,IV)
 for u,b,ww,hh in ups+low:win104(m,x,y,u,b,ww,hh,a,FR,TR,3,.12)
 # The arched carriage gate in brown boards.
 facade_box(m,x,y,gu,.10,1.30,2.0,.06,2.60,M104['Gate'],a)
 for k in range(1,9):facade_box(m,x,y,gu-1.0+k*2.0/9,.14,1.10,.03,.02,2.15,FR,a)
 p18_arch(m,x,y,2.05,2.0,.55,.12,.42,a,TR)
 facade_box(m,x,y,0,.42,.30,L+.02,.12,.60,M104['Plinth'],a);facade_box(m,x,y,0,.43,2.75,L+.04,.12,.14,TR,a)
 facade_box(m,x,y,0,.50,H-.20,L+.12,.30,.40,TR,a)
 for uu in (-L/2+.22,L/2-.22):facade_box(m,x,y,uu,.43,(.6+H)/2,.44,.12,H-.6,TR,a)
saddle82(m,'y176',A76,B76,M104['Tile'],IV,along=True)
fw=front104('y176',FN104)[0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for xx in (-140.6,-134.6):dormer102(m,x,y,U(fw,*on104(A76,B76,xx,0)),a,H,1.5,[(0,.85)],M104['DormerRed'],M104['Tile'],WF104,back=.5,dep=2.4,zt=1.45,zp=2.05,wb=.35,wh=.90)
rest104(m,'r176',M104['Rest'],FR,M104['Trim'],2,M104['RoofFlat'])
b104_finish(m,'92204176')

# ---- 550598948: the modern block on Strömgatan (s from the east end of the front).
A48,B48=(-81.68,204.83),(-123.78,205.5)
m=b104_new(Z['m948']['mesh'],'Kvarnholmen/Strömgatan');RD=M104['Render'];RB=M104['RedBoard'];FL=M104['FrameLight'];MT=M104['Metal'];CO=M104['Concrete']
H=Z['m948']['height'];HR=10.70;HB=5.10
WS104=[1.18+k*2.92 for k in range(1,14) if 1.18+k*2.92<41.0]
for w in walls('m948'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],RD if w['z0']<HR else MT);continue
 street=SN104(*outward(w),x,y)
 if street:
  S=lambda s:U(w,*pt102(A48,B48,s))
  ups=[(S(s),b,1.80 if k%2 else 1.50,1.45,k%4==1) for k,s in enumerate(WS104) for b in (5.68,8.53)]
  shops=[(S(s),.63,ww,2.50) for s,ww in ((4.2,2.4),(8.0,2.4),(11.8,2.4),(22.4,2.04),(25.8,2.73),(30.55,2.31),(34.5,2.4),(38.3,2.4))]
  gate=(S(17.8),0,2.80,2.97);door=(S(27.9),.21,1.28,2.89)
  tops=[(S(s),11.30,1.50,1.40) for s in WS104]
 else:
  n=max(1,round(L/3.0));us=[-L/2+(k+.5)*L/n for k in range(n)]
  ups=[(u,b,1.50,1.45,False) for u in us for b in (5.68,8.53)];shops=[(u,1.00,1.40,1.60) for u in us[::2]];gate=None;door=None
  tops=[(u,11.30,1.50,1.40) for u in us]
 # The French balconies: the window runs down to the floor behind a grey bar grille.
 oph=[(u,b-(.55 if fb else 0),ww,hh+(.55 if fb else 0),0) for u,b,ww,hh,fb in ups]
 low=[(u,b,ww,hh,0) for u,b,ww,hh in shops]+([(gate[0],0,gate[2],gate[3],0)] if gate else [])+([(door[0],door[1],door[2],door[3],0)] if door else [])
 bz_wall(m,w['p'],w['q'],0,HB,low,RB);bz_wall(m,w['p'],w['q'],HB,HR,oph,RD);bz_wall(m,w['p'],w['q'],HR,H,[(u,b,ww,hh,0) for u,b,ww,hh in tops],MT)
 boards82(m,x,y,L,a,.63,HB-.08,low,RB,.30)
 for u,b,ww,hh,r in oph:
  glaze104(m,x,y,u,b,ww,hh,a,FL,.20,(0,))
  if hh>1.8:
   for k in range(9):facade_box(m,x,y,u-ww/2+.10+k*(ww-.20)/8,.50,b+.55,.025,.025,1.05,MT,a)
   for zz in (b+.08,b+1.05):facade_box(m,x,y,u,.50,zz,ww,.04,.04,MT,a)
 for u,b,ww,hh in shops:glaze104(m,x,y,u,b,ww,hh,a,M104['ShopFrame'],.18)
 if door:
  glaze104(m,x,y,door[0],door[1],door[2],door[3],a,M104['ShopFrame'],.18);facade_box(m,x,y,door[0],.14,door[1]+2.0,door[2],.08,.08,M104['ShopFrame'],a)
 if gate:
  facade_box(m,x,y,gate[0],.10,gate[3]/2,gate[2],.04,gate[3],M104['Dark'],a)
  for k in range(1,16):facade_box(m,x,y,gate[0]-gate[2]/2+k*gate[2]/16,.15,gate[3]/2,.03,.03,gate[3],M104['Iron'],a)
  facade_box(m,x,y,gate[0],.40,gate[3]+.06,gate[2]+.24,.12,.12,M104['Iron'],a)
 for u,b,ww,hh in tops:glaze104(m,x,y,u,b,ww,hh,a,FL,.20,(0,))
 # Concrete plinth (stepped round the openings), the belt between the boards and the render, the
 # grey standing seams of the top storey and its coping.
 for l0,l1 in [(-L/2,L/2)]:
  cuts=sorted((u-ww/2,u+ww/2) for u,b,ww,hh,r in low if b<.5);at=l0
  for c0,c1 in cuts+[(l1,l1)]:
   if c0>at+.05:facade_box(m,x,y,(at+c0)/2,.45,.32,c0-at,.20,.64,CO,a)
   at=max(at,c1)
 facade_box(m,x,y,0,.40,HB,L+.02,.12,.06,M104['Dark'],a)
 n=int(L/.55)
 for k in range(1,n):
  u=-L/2+k*L/n
  if any(abs(u-tu)<tw/2+.08 for tu,tb,tw,th in tops):
   facade_box(m,x,y,u,.38,HR+.30,.03,.04,.55,MT,a);facade_box(m,x,y,u,.38,H-.35,.03,.04,.55,MT,a)
  else:facade_box(m,x,y,u,.38,(HR+H)/2,.03,.04,H-HR,MT,a)
 facade_box(m,x,y,0,.42,H+.05,L+.10,.16,.14,MT,a)
flatroof102(m,'m948',M104['RoofDark'],MT)
rest104(m,'n948',RD,FL,RD,3,M104['RoofFlat'])
rest104(m,'s948',M104['Rest'],FL,M104['Trim'],3,M104['RoofFlat'])
b104_finish(m,'550598948')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block104_cameras=[
 sv_camera('513_Block104_Cal_KaggensWest',-186.0,157.6,2.25,243,15,90),
 sv_camera('514_Block104_Cal_KaggensEast',-186.0,157.6,2.25,63,15,90),
 sv_camera('515_Block104_Cal_Fiskaregatan',-148.7,139.95,2.25,152,15,90),
 sv_camera('516_Block104_Cal_Stromgatan',-106.48,210.9,2.50,153,15,90),
 ('517_Block104_Aerial',(-150.0,105.0,60.0),(-150.0,165.0,4.0),28),
]
print('BLOCK104_GEOMETRY',len(block104_names),'dropped',block104_dropped,block104_samples)
