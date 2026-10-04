"""Pass 125: the first interior rooms of Kalmar slott, on the state floor of the west range.
- SM_Castle125_GyllenSalen: Gyllene salen (Olsson's room 59, Johan III's hall of the 1570s): the
  coffered ceiling after N. M. Mandelgren's plan of 1848 (four by four large octagonal coffers,
  elongated coffers along every rib, X-shaped node fields with bosses, the pendant at the centre),
  the painted frieze and cornice, rough whitewashed walls, the deep window niches with their small
  coffered soffits, the fireplace between the west windows, the stone door surrounds with pediments,
  closed doors to Kuretornet, the king's förstuga (55) and room 61b, and the wide-board floor.
- SM_Castle125_Kungsmaket: Kungsmaket (room 62, Erik XIV's chamber of about 1560 in Kungsmakstornet,
  tower II): intarsia panelling 2.6 m high with fluted pilasters and an entablature, the painted
  hunting frieze, the dentilled cornice, the coffered ceiling with intarsia framing, the arched west
  window niche with benches, the arched niches to the north and east, the fireplace and a parquet
  floor; and the door passage through the tower wall to room 61a.
- SM_Castle125_Forrum: a plain stand-in for room 61a (Panelade salen, now part of Grå salen), the
  room between the two, with the doors that join them.
- SM_Kalmar_Slott_Towers (pass 27/124's mesh) gets one box cut out of the north tower's closed
  cylinder where Kungsmaket's door passage crosses it. The cut lies inside the west range, under its
  roof; it is idempotent.
The rooms are closed boxes inside pass 27's hollow range; nothing of the exterior is moved.
Sources: Olsson, Fornvännen 1974 (plan, read only) and 1964 (the 1780 plan of room 62, read only);
Mandelgren 1848 and the Olsson plates on DigitaltMuseum (Public Domain Mark); Commons photographs.
See references/block125-notes.md.
"""
from mathutils import Vector
B125D=json.loads((R/'source/block125.json').read_text())
block125_names=[];B125={}
for old in [k for k in list(materials) if k.startswith('M_Block125_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownPaintWhite',(.86,.84,.78),.95,0),('Frieze','TownPaintWhite',(.68,.68,.65),.92,0),('RedLine','TownPaintWhite',(.56,.22,.15),.85,0),
 ('Cream','TownIvory',(.86,.80,.68),.80,0),('Gilt','TownIvory',(.80,.62,.27),.45,.35),('BlueGrey','TownPaintWhite',(.55,.59,.61),.80,0),
 ('Panel','TownPaintBrown',(.40,.29,.17),.65,0),('Boards','TownPaintBrown',(.56,.49,.41),.85,0),('Boards2','TownPaintBrown',(.49,.43,.36),.85,0),
 ('Stone','TownStone',(.72,.71,.67),.85,0),('StoneDark','TownStone',(.30,.29,.28),.90,0),('Door','TownPaintBrown',(.33,.27,.20),.75,0),
 ('Frame','TownPaintWhite',(.86,.86,.83),.60,0),('Daylight','TownPaintWhite',(.84,.90,.93),.20,0),
 ('Intarsia','TownPaintBrown',(.78,.60,.36),.55,0),('IntarsiaDark','TownPaintBrown',(.34,.22,.12),.60,0),('Walnut','TownPaintBrown',(.22,.14,.08),.55,0),
 ('Ebony','TownPaintBrown',(.09,.08,.07),.50,0),('HuntGreen','TownPaintGreen',(.40,.52,.30),.85,0),('HuntSky','TownPaintWhite',(.36,.50,.66),.85,0),
 ('Cushion','TownPaintWhite',(.66,.32,.20),.90,0),('HuntBrown','TownPaintBrown',(.56,.36,.19),.80,0),('HuntTree','TownPaintGreen',(.22,.34,.18),.85,0),('Parquet','TownPaintBrown',(.58,.40,.22),.60,0),('Parquet2','TownPaintBrown',(.36,.24,.14),.60,0),
 ]:
 name='M_Block125_'+key;B125[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block125_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M125=B125

def b125_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block125_names.append(name);return Mesh(name,category)
def drop_degenerate_faces125(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b125_finish(m):
 obj=s21_finish(m);obj['block125_dropped_faces']=drop_degenerate_faces125(obj)
 print('BLOCK125_DROPPED',obj.name,obj['block125_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=125;obj['reference_notes']='references/block125-notes.md';obj['osm_way']='';return obj

# ---------------------------------------------------------------- the range frame
# s runs along pass 27's west ('NW') range from the north tower towards the west tower, c outwards
# (away from the courtyard); pass 27's outer front lies at c 0, its courtyard front at c -17.9.
FR125=B125D['frame'];O125,U125,N125=FR125['origin'],FR125['u'],FR125['n'];ANG125=math.atan2(U125[1],U125[0])
FL125=B125D['floor'];RM125=B125D['rooms'];WN125=B125D['windows'];DR125=B125D['doors'];TW125=B125D['tower']
def P125(s,c,z=0.0):return (O125[0]+U125[0]*s+N125[0]*c,O125[1]+U125[1]*s+N125[1]*c,z)
def bx125(m,s0,s1,c0,c1,z0,z1,ma):
 # An axis-aligned box in the range frame.
 s0,s1=min(s0,s1),max(s0,s1);c0,c1=min(c0,c1),max(c0,c1);z0,z1=min(z0,z1),max(z0,z1)
 if s1-s0<.002 or c1-c0<.002 or z1-z0<.002:return
 x,y,_=P125((s0+s1)/2,(c0+c1)/2);m.box((x,y,(z0+z1)/2),(s1-s0,c1-c0,z1-z0),ma,ANG125)
def hexa125(m,a,b,ma):
 # Closed six-faced solid from two quads a and b, corners in matching order.
 m.faces(list(a)+list(b),[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
def wall125(m,along,a0,a1,t0,t1,z0,z1,holes,ma):
 # A wall along s ('s': a is s, t is c) or along c ('c'), with rectangular holes (centre, width,
 # bottom, top), built of closed boxes as pass 23's bz_wall does.
 zs=sorted(set([z0,z1]+[v for u,w,b,t in holes for v in (b,t) if z0<v<z1]))
 for lo,hi in zip(zs,zs[1:]):
  mid=(lo+hi)/2;cuts=sorted((u-w/2,u+w/2) for u,w,b,t in holes if b<mid<t);at=a0
  for l,r in cuts+[(a1,a1)]:
   l=max(a0,min(a1,l));r=max(a0,min(a1,r))
   if l>at+.001:
    if along=='s':bx125(m,at,l,t0,t1,lo,hi,ma)
    else:bx125(m,t0,t1,at,l,lo,hi,ma)
   at=max(at,r)
def fanplate125(m,pts,d0,d1,frame,ma):
 # A flat shape given in a vertical plane as (a,z) points, extruded across d0..d1; the faces are a
 # triangle fan round the first point (no large n-gon). frame(a,d,z) -> world point.
 n=len(pts);v=[frame(a,d,z) for d in (d0,d1) for a,z in pts]
 f=[(0,i,i+1) for i in range(1,n-1)]+[(n,n+i+1,n+i) for i in range(1,n-1)]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 m.faces(v,f,ma)
def fs125(s_fixed):
 # Frame for a plane at constant s: a runs along c, d along s.
 return lambda a,d,z:P125(s_fixed+d,a,z)
def fc125(c_fixed):
 return lambda a,d,z:P125(a,c_fixed+d,z)
def arch125(m,frame,u0,zsp,r,d0,d1,th,ma,k=12):
 # A semicircular arch ring (radius r, thickness th) in a vertical plane, as closed segments.
 for i in range(k):
  t0,t1=math.pi*i/k,math.pi*(i+1)/k
  q=lambda rr,t,d:frame(u0+rr*math.cos(t),d,zsp+rr*math.sin(t))
  hexa125(m,[q(r,t0,d0),q(r+th,t0,d0),q(r+th,t1,d0),q(r,t1,d0)],[q(r,t0,d1),q(r+th,t0,d1),q(r+th,t1,d1),q(r,t1,d1)],ma)
def spandrel125(m,frame,u0,zsp,r,top,d0,d1,ma,k=12):
 # The two corners between a semicircular arch and the square head above it, as fans.
 for sg in (-1,1):
  pts=[(u0+sg*r,top)]+[(u0+sg*r*math.cos(math.pi/2*j/k),zsp+r*math.sin(math.pi/2*j/k)) for j in range(k+1)]
  if top>zsp+r+1e-4:pts.append((u0,top))
  else:pts[-1]=(u0,top)
  fanplate125(m,pts,d0,d1,frame,ma)
def lathe125(m,s,c,z,prof,ma,n=12):
 x,y,_=P125(s,c);m.lathe(x,y,z,prof,ma,n)
def inset125(poly,d):
 # Convex polygon inset by d (edge offset lines intersected); counter-clockwise or clockwise.
 n=len(poly);area=sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n));sg=1 if area>0 else -1;out=[]
 for i in range(n):
  a,b,c=Vector(poly[i-1]),Vector(poly[i]),Vector(poly[(i+1)%n]);e1=(b-a).normalized();e2=(c-b).normalized()
  n1=Vector((-e1.y,e1.x))*sg;n2=Vector((-e2.y,e2.x))*sg;p1=a+n1*d;p2=b+n2*d
  den=e1.x*e2.y-e1.y*e2.x;t=((p2-p1).x*e2.y-(p2-p1).y*e2.x)/den;q=p1+e1*t;out.append((q.x,q.y))
 return out
def coffer125(m,toW,poly,zs,zt,steps,panel):
 # A recessed coffer: frames (inset, rise, material, sloped) from the soffit up to the panel, each
 # frame a ring of closed segments up to the common top zt; a sloped frame rises across its width
 # (the wide cream bevel of the large coffers), a flat one rises at its inner edge. The panel is a
 # closed prism. Returns the panel's polygon and height.
 cur=poly;z=zs
 for d,rise,ma,slope in steps:
  nxt=inset125(cur,d);n=len(cur);zi=z+rise if slope else z
  for i in range(n):
   j=(i+1)%n;q=[cur[i],cur[j],nxt[j],nxt[i]];zq=[z,z,zi,zi]
   hexa125(m,[toW(*p,zz) for p,zz in zip(q,zq)],[toW(*p,zt) for p in q],ma)
  cur=nxt;z+=rise
 m.prism([toW(*p,0)[:2] for p in cur],z,zt,panel);return cur,z

# ================================================================= Gyllene salen
m=b125_new('SM_Castle125_GyllenSalen','Kalmar slott/Interiör')
G=RM125['gyllene'];GW=B125D['walls']['gyllene'];gs0,gs1,gc0,gc1=G['s0'],G['s1'],G['c0'],G['c1'];ZS=FL125+G['h'];ZT=ZS+.45
SO,TO=B125D['sill_out'],B125D['top_out'];NH=FL125+4.85;NW125=2.2   # niche head under the frieze; niche width
WT=ZT+.15                                                         # walls rise past the ceiling's top
# Floor: wide boards running towards the west windows (panorama 2009, photograph 1930s).
bx125(m,GW['n'][0],GW['s'][0],GW['e'][1],-.05,FL125-.30,FL125-.03,M125['Boards2'])
nb=round((gs1-gs0)/.30)
for k in range(nb):
 a=gs0+(gs1-gs0)*k/nb;b=gs0+(gs1-gs0)*(k+1)/nb-.004
 bx125(m,a,b,gc0,gc1,FL125-.03,FL125,M125['Boards'] if (k*7)%3 else M125['Boards2'])
# The west (outer) wall: two niches on pass 27's window axes, then the window layer with openings of
# pass 27's size and height (1.15 x 3.2 m) and the glazing.
nich=[(s,NW125,FL125-.3,NH) for s in WN125['gyllene_outer']]
wall125(m,'s',GW['n'][0],GW['s'][0],-.28,gc1,FL125-.3,WT,nich,M125['Plaster'])
wall125(m,'s',GW['n'][0],GW['s'][0],-.05,-.28,FL125-.3,WT,[(s,1.15,SO,TO) for s in WN125['gyllene_outer']],M125['Plaster'])
# The east (courtyard) wall: one niche on pass 27's courtyard window axis, same interior height.
cc=GW['e'][1]
nich_e=[(s,NW125,FL125-.3,NH) for s in WN125['gyllene_court']]
wall125(m,'s',GW['n'][0],GW['s'][1],gc0,GW['e'][0],FL125-.3,WT,nich_e,M125['Plaster'])
wall125(m,'s',GW['n'][0],GW['s'][1],GW['e'][0],cc,FL125-.3,WT,[(s,1.15,SO,TO) for s in WN125['gyllene_court']],M125['Plaster'])
def niche125(s,c_room,c_glass,sg):
 # sg: +1 for the outer wall (c rising outwards), -1 for the courtyard wall.
 a,b=sorted((c_room,c_glass))
 hw=NW125/2
 bx125(m,s-hw,s+hw,a,b,FL125-.03,FL125+.18,M125['Stone'])                                     # the raised niche floor
 for k in (-1,0,1):bx125(m,s+k*hw*.62-.03,s+k*hw*.62+.03,a,b,NH-.07,NH,M125['Gilt'])         # small coffers in the soffit
 for f in (.33,.67):cm=a+(b-a)*f;bx125(m,s-hw,s+hw,cm-.03,cm+.03,NH-.07,NH,M125['Gilt'])
 bx125(m,s-hw+.01,s+hw-.01,a,b,NH-.012,NH,M125['Cream'])
 for k in (-1,1):
  for f in (.17,.5,.83):lathe125(m,s+k*hw*.31,a+(b-a)*f,NH-.10,[(.02,0),(.05,.04),(.06,.07),(.05,.08)],M125['Gilt'],8)
 # glazing: a pale pane, a frame, a mullion and two transoms (small panes, photographs)
 g0=c_glass-sg*.17;g1=c_glass-sg*.13
 bx125(m,s-.575,s+.575,g0,g1,SO,TO,M125['Daylight'])
 f0=c_glass-sg*.20;f1=c_glass-sg*.10
 for u in (-.575,.575):bx125(m,s+u-.04,s+u+.04,f0,f1,SO,TO,M125['Frame'])
 for zz in (SO,TO):bx125(m,s-.6,s+.6,f0,f1,zz-.04,zz+.04,M125['Frame'])
 bx125(m,s-.03,s+.03,f0,f1,SO,TO,M125['Frame'])
 for f in (.36,.70):bx125(m,s-.575,s+.575,f0,f1,SO+(TO-SO)*f-.025,SO+(TO-SO)*f+.025,M125['Frame'])
 bx125(m,s-.65,s+.65,f0-sg*.25,f1,SO-.06,SO,M125['Stone'])                                # the window board
for s in WN125['gyllene_outer']:niche125(s,gc1,-.05,1)
for s in WN125['gyllene_court']:niche125(s,gc0,cc,-1)
# The north wall (to 61a) with the open door, the south wall (Kuretornet, the förstuga) with two closed
# doors.
DG=DR125['gyllene_forrum']
wall125(m,'c',GW['e'][1],-.05,GW['n'][0],gs0,FL125-.3,WT,[(DG['c'],DG['w'],FL125-.3,FL125+DG['h'])],M125['Plaster'])
bx125(m,GW['n'][0],gs0,DG['c']-DG['w']/2,DG['c']+DG['w']/2,FL125-.3,FL125,M125['Stone'])            # threshold
wall125(m,'c',GW['e'][1],-.12,gs1,GW['s'][1],FL125-.3,WT,[],M125['Plaster'])
def surround125(frame,u,w,h,ped,ma=None):
 # A stone door surround (photograph of the 1930s): jambs, a frieze, a cornice and, with ped, a
 # triangular pediment with three ball finials. frame(a,d,z): a along the wall, d into the room.
 ma=ma or M125['Stone'];z=FL125
 for sg in (-1,1):fanplate125(m,[(u+sg*(w/2),z),(u+sg*(w/2+.2),z),(u+sg*(w/2+.2),z+h+.3),(u+sg*(w/2),z+h+.3)],0,.07,frame,ma)
 fanplate125(m,[(u-w/2-.26,z+h),(u+w/2+.26,z+h),(u+w/2+.26,z+h+.34),(u-w/2-.26,z+h+.34)],0,.09,frame,ma)
 fanplate125(m,[(u-w/2-.34,z+h+.34),(u+w/2+.34,z+h+.34),(u+w/2+.34,z+h+.44),(u-w/2-.34,z+h+.44)],0,.14,frame,ma)
 if ped:
  fanplate125(m,[(u-w/2-.30,z+h+.44),(u+w/2+.30,z+h+.44),(u,z+h+.88)],0,.10,frame,ma)
  for a,zz in ((u-w/2-.25,z+h+.44),(u+w/2+.25,z+h+.44),(u,z+h+.86)):
   x,y,_=frame(a,.06,0);m.lathe(x,y,zz,[(.05,0),(.09,.06),(.10,.12),(.07,.19),(.03,.22)],ma,10)
def leaf125(frame,u,w,h,ma=None):
 # A closed door: a leaf with two raised fields, slightly proud of the wall.
 ma=ma or M125['Door'];fanplate125(m,[(u-w/2,FL125),(u+w/2,FL125),(u+w/2,FL125+h),(u-w/2,FL125+h)],0,.04,frame,ma)
 for z0,z1 in ((FL125+.25,FL125+h*.45),(FL125+h*.55,FL125+h-.2)):fanplate125(m,[(u-w/2+.14,z0),(u+w/2-.14,z0),(u+w/2-.14,z1),(u-w/2+.14,z1)],.04,.07,frame,ma)
# North wall faces the room at s = gs0 (into the room is +s); south wall at s = gs1 (into the room is -s).
fN=lambda a,d,z:P125(gs0+d,a,z);fS=lambda a,d,z:P125(gs1-d,a,z)
fE=lambda a,d,z:P125(a,gc0+d,z);fW=lambda a,d,z:P125(a,gc1-d,z)
surround125(fN,DG['c'],DG['w'],DG['h'],True)
for u in (-4.6,-13.3):leaf125(fS,u,1.05,2.3)
surround125(fS,-13.3,1.05,2.3,True)                                   # to the king's förstuga (55)
for sg in (-1,1):fanplate125(m,[(-4.6+sg*.525,FL125),(-4.6+sg*.70,FL125),(-4.6+sg*.70,FL125+2.47),(-4.6+sg*.525,FL125+2.47)],0,.012,fS,M125['RedLine'])
fanplate125(m,[(-4.6-.70,FL125+2.3),(-4.6+.70,FL125+2.3),(-4.6+.70,FL125+2.47),(-4.6-.70,FL125+2.47)],0,.012,fS,M125['RedLine'])   # painted surround (panorama)
leaf125(fE,5.5,1.05,2.3);surround125(fE,5.5,1.05,2.3,True)           # to 61b (closed)
# The fireplace between the west windows (panorama 2009; the Olsson plates of 1958): stone jambs, a
# mantel, a sloping hood under a pointed gable with pinnacles; a dark hearth.
sf=sum(WN125['gyllene_outer'])/2;FW=lambda a,d,z:P125(a,gc1-d,z)
fanplate125(m,[(sf-.62,FL125),(sf+.62,FL125),(sf+.62,FL125+1.25),(sf-.62,FL125+1.25)],-.02,.02,FW,M125['StoneDark'])
bx125(m,sf-.75,sf+.75,gc1-.45,gc1,FL125,FL125+.04,M125['Stone'])
for sg in (-1,1):bx125(m,sf+sg*.62,sf+sg*.86,gc1-.40,gc1,FL125,FL125+1.25,M125['Stone'])
bx125(m,sf-.95,sf+.95,gc1-.46,gc1,FL125+1.25,FL125+1.55,M125['Stone'])
fanplate125(m,[(sf-.88,FL125+1.55),(sf+.88,FL125+1.55),(sf+.40,FL125+2.70),(sf-.40,FL125+2.70)],0,.36,FW,M125['Stone'])
fanplate125(m,[(sf-.48,FL125+2.70),(sf+.48,FL125+2.70),(sf,FL125+3.25)],0,.30,FW,M125['Stone'])
for a,z0,h in ((sf-.88,FL125+1.55,.55),(sf+.88,FL125+1.55,.55),(sf,FL125+3.2,.35)):
 bx125(m,a-.05,a+.05,gc1-.40,gc1-.30,z0,z0+h,M125['Stone']);x,y,_=P125(a,gc1-.35);m.lathe(x,y,z0+h,[(.06,0),(.03,.14),(.012,.2)],M125['Stone'],8)
# The painted frieze, its red lines and the moulded cornice round the room (panorama, ceiling photograph).
for frame,L0,L1 in ((fN,gc0,gc1),(fS,gc0,gc1),(fE,gs0,gs1),(fW,gs0,gs1)):
 for z0,z1,d,ma in ((NH,ZS-.14,.015,M125['Frieze']),(NH,NH+.05,.025,M125['RedLine']),(ZS-.19,ZS-.14,.025,M125['RedLine']),(ZS-.14,ZS-.07,.08,M125['Cream']),(ZS-.07,ZS,.15,M125['Gilt'])):
  fanplate125(m,[(L0+.001,z0),(L1-.001,z0),(L1-.001,z1),(L0+.001,z1)],0,d,frame,ma)
# The frieze's painted beasts (red winged creatures every 1.3 m, panorama) and a darker scroll band,
# as thin plates.
for frame,L0,L1 in ((fN,gc0,gc1),(fS,gc0,gc1),(fE,gs0,gs1),(fW,gs0,gs1)):
 zm=(NH+ZS-.19)/2;n=int((L1-L0)/1.3)
 for k in range(n):
  a=L0+(L1-L0)*(k+.5)/n
  fanplate125(m,[(a-.16,zm-.18),(a+.12,zm-.18),(a+.18,zm+.04),(a+.04,zm+.20),(a-.10,zm+.10)],.015,.03,frame,M125['RedLine'])
  fanplate125(m,[(a-.30,zm+.10),(a-.12,zm+.28),(a-.06,zm+.12)],.015,.028,frame,M125['RedLine'])
 for z0 in (zm-.34,zm+.30):fanplate125(m,[(L0+.002,z0),(L1-.002,z0),(L1-.002,z0+.05),(L0+.002,z0+.05)],.015,.022,frame,M125['BlueGrey'])
# The coffered ceiling (Mandelgren 1848; ceiling photograph 2017). Room frame: x along s, y along c.
CE=B125D['ceiling'];smid,cmid=(gs0+gs1)/2,(gc0+gc1)/2
def toG(x,y,z):return P125(smid+x,cmid+y,z)
# From the soffit: a red line, a wide cream bevel, a gilt moulding, a grey-blue step, a gilt fillet,
# the carved panel (dark ground with gilt and red relief: a rosette and four leaves, as simple solids).
OCT=[(.03,0,M125['RedLine'],False),(.14,.10,M125['Cream'],True),(.04,.04,M125['Gilt'],False),(.05,.06,M125['BlueGrey'],False),(.03,.03,M125['Gilt'],False)]
HEX=[(.02,0,M125['RedLine'],False),(.08,.06,M125['Cream'],True),(.03,.03,M125['Gilt'],False)]
for p in CE['octs']:
 pp,zp=coffer125(m,toG,[tuple(q) for q in p],ZS,ZT,OCT,M125['Panel']);cx_=sum(q[0] for q in pp)/len(pp);cy_=sum(q[1] for q in pp)/len(pp)
 X,Y,_=toG(cx_,cy_,0);m.lathe(X,Y,zp-.07,[(.03,0),(.10,.02),(.15,.05),(.16,.07)],M125['Gilt'],12)
 for k in range(4):
  t=math.pi/4+k*math.pi/2;r=.30;X,Y,_=toG(cx_+r*math.cos(t),cy_+r*math.sin(t),0)
  m.box((X,Y,zp-.025),(.30,.09,.05),M125['Gilt'] if k%2 else M125['RedLine'],ANG125+t)
  t2=k*math.pi/2;X,Y,_=toG(cx_+.36*math.cos(t2),cy_+.36*math.sin(t2),0);m.box((X,Y,zp-.02),(.12,.12,.04),M125['Gilt'],ANG125+t2+math.pi/4)
for p in CE['hexs']:
 pp,zp=coffer125(m,toG,[tuple(q) for q in p],ZS,ZT,HEX,M125['Panel']);xs_=[q[0] for q in pp];ys_=[q[1] for q in pp]
 cx_,cy_=sum(xs_)/len(xs_),sum(ys_)/len(ys_);along=(max(xs_)-min(xs_))>(max(ys_)-min(ys_))
 for f in (-.28,0,.28):
  L_=(max(xs_)-min(xs_)) if along else (max(ys_)-min(ys_));X,Y,_=toG(cx_+(f*L_ if along else 0),cy_+(0 if along else f*L_),0)
  m.box((X,Y,zp-.02),(.18 if f else .26,.12,.04),M125['Gilt'],ANG125+(0 if along else math.pi/2))
for t in CE['flat']:m.prism([toG(*q,0)[:2] for q in t],ZS,ZT,M125['Cream'])
# Gilded bosses at the crossings and the carved pendant at the centre.
cen=(CE['xs'][2],CE['ys'][2])
for x,y in CE['nodes']:
 X,Y,_=toG(x,y,0)
 if (x,y)==cen:
  m.lathe(X,Y,ZS-.78,[(.03,0),(.10,.04),(.20,.16),(.26,.34),(.22,.52),(.30,.62)],M125['BlueGrey'],16)
  m.lathe(X,Y,ZS-.18,[(.30,0),(.34,.08),(.30,.14),(.24,.18)],M125['Gilt'],16)
  for k in range(4):t=k*math.pi/2+math.pi/4;m.box((X+.28*math.cos(t),Y+.28*math.sin(t),ZS-.42),(.10,.05,.36),M125['Gilt'],t+math.pi/2)
 else:m.lathe(X,Y,ZS-.13,[(.03,0),(.09,.03),(.15,.08),(.17,.12),(.15,.13)],M125['Gilt'],12)
b125_finish(m)

# ================================================================= Förrum (61a), a stand-in
m=b125_new('SM_Castle125_Forrum','Kalmar slott/Interiör')
F=RM125['forrum'];fs0,fs1,fc0,fc1=F['s0'],F['s1'],F['c0'],F['c1'];DK=DR125['forrum_kungsmak'];FZ=FL125+F['h']
bx125(m,.05,RM125['gyllene']['s0']-1.4,-12.0,-.03,FL125-.30,FL125-.03,M125['Boards2'])
nb=round((fs1-fs0)/.30)
for k in range(nb):
 a=fs0+(fs1-fs0)*k/nb;b=fs0+(fs1-fs0)*(k+1)/nb-.004;bx125(m,a,b,fc0,fc1,FL125-.03,FL125,M125['Boards'] if k%2 else M125['Boards2'])
wall125(m,'s',.05,fs1,fc1,-.03,FL125-.3,FZ+.3,[],M125['Plaster'])
wall125(m,'s',.05,fs1,-12.0,fc0,FL125-.3,FZ+.3,[],M125['Plaster'])
wall125(m,'c',fc0,fc1,.05,fs0,FL125-.3,FZ+.3,[(DK['c'],DK['w'],FL125-.3,FL125+DK['h'])],M125['Plaster'])
bx125(m,fs0,fs1,fc0,fc1,FZ,FZ+.3,M125['Plaster'])
for k in range(1,6):cm=fc0+(fc1-fc0)*k/6;bx125(m,fs0,fs1,cm-.11,cm+.11,FZ-.24,FZ,M125['Door'])   # a beamed ceiling
fF=lambda a,d,z:P125(fs0+d,a,z);surround125(fF,DK['c'],DK['w'],DK['h'],False)
b125_finish(m)

# ================================================================= Kungsmaket
m=b125_new('SM_Castle125_Kungsmaket','Kalmar slott/Interiör')
K=RM125['kungsmak'];ks0,ks1,kc0,kc1=K['s0'],K['s1'],K['c0'],K['c1'];KZ=FL125+K['h'];KT=KZ+.40;TS,TC=TW125['s'],TW125['c']
# The parquet: a two-tone chequer of 0.47 m squares on a slab (the panorama shows a diamond pattern).
bx125(m,ks0-.5,ks1+.5,kc0-.5,kc1+.5,FL125-.30,FL125-.03,M125['Parquet2'])
ns,nc=round((ks1-ks0)/.47),round((kc1-kc0)/.47)
for i in range(ns):
 for j in range(nc):
  a,b=ks0+(ks1-ks0)*i/ns,ks0+(ks1-ks0)*(i+1)/ns;c0_,c1_=kc0+(kc1-kc0)*j/nc,kc0+(kc1-kc0)*(j+1)/nc
  bx125(m,a,b,c0_,c1_,FL125-.03,FL125,M125['Parquet'] if (i+j)%2 else M125['Parquet2'])
# Walls 0.5 m thick lining the tower's masonry; openings: the arched west window niche, the door to
# 61a (+s wall), an arched niche to the north (-s, towards the small tower XII) and the east niche.
NW_W=2.5;NW_R=NW_W/2;NW_Z=FL125+2.6                       # west niche: width, radius, springing at the panelling's top
NN_W=1.4;NN_Z=FL125+2.6;NE_W=1.2;NE_Z=FL125+2.5;NE_S=TS-1.2
wall125(m,'s',ks0-.5,ks1+.5,kc1,kc1+.5,FL125-.3,KT+.1,[(TS,NW_W,FL125-.3,NW_Z+NW_R)],M125['Walnut'])
wall125(m,'s',ks0-.5,ks1+.5,kc0-.5,kc0,FL125-.3,KT+.1,[(NE_S,NE_W,FL125-.3,NE_Z+NE_W/2)],M125['Walnut'])
wall125(m,'c',kc0,kc1,ks1,ks1+.5,FL125-.3,KT+.1,[(DK['c'],DK['w'],FL125-.3,FL125+DK['h'])],M125['Walnut'])
wall125(m,'c',kc0,kc1,ks0-.5,ks0,FL125-.3,KT+.1,[(TC,NN_W,FL125-.3,NN_Z+NN_W/2)],M125['Walnut'])
fKW=lambda a,d,z:P125(a,kc1-d,z)                          # the west wall's room face, d towards the room
fKE=lambda a,d,z:P125(a,kc0+d,z);fKN=lambda a,d,z:P125(ks0+d,a,z);fKS=lambda a,d,z:P125(ks1-d,a,z)
# Arches over the three niches: an arched head (the spandrels filled up to the hole's square top).
spandrel125(m,lambda a,d,z:P125(a,kc1+d,z),TS,NW_Z,NW_R,NW_Z+NW_R,0,.5,M125['Walnut'])
spandrel125(m,lambda a,d,z:P125(ks0-d,a,z),TC,NN_Z,NN_W/2,NN_Z+NN_W/2,0,.5,M125['Walnut'])
spandrel125(m,lambda a,d,z:P125(a,kc0-d,z),NE_S,NE_Z,NE_W/2,NE_Z+NE_W/2,0,.5,M125['Walnut'])
# The west window niche (the Olsson plate of the west niche; the panorama): through the tower wall to
# the glazing near the tower's face, panelled sides with benches and cushions, a painted and gilded
# barrel vault, leaded glazing.
CG=kc1+1.6                                                  # the glazing (the photograph: a niche about 1.6 m deep)
for sg in (-1,1):bx125(m,TS+sg*NW_R,TS+sg*(NW_R+.4),kc1,CG+.3,FL125-.3,NW_Z+NW_R+.4,M125['Walnut'])
bx125(m,TS-NW_R,TS+NW_R,kc1,CG+.3,FL125-.3,FL125+.02,M125['Parquet2'])
for k in range(12):
 t0,t1=math.pi*k/12,math.pi*(k+1)/12;q=lambda rr,t,c:P125(TS+rr*math.cos(t),c,NW_Z+rr*math.sin(t))
 hexa125(m,[q(NW_R,t0,kc1),q(NW_R+.3,t0,kc1),q(NW_R+.3,t1,kc1),q(NW_R,t1,kc1)],[q(NW_R,t0,CG),q(NW_R+.3,t0,CG),q(NW_R+.3,t1,CG),q(NW_R,t1,CG)],M125['HuntSky'] if k%3 else M125['Gilt'])
 for cc_ in (kc1+.5,kc1+1.05):hexa125(m,[q(NW_R-.05,t0,cc_),q(NW_R,t0,cc_),q(NW_R,t1,cc_),q(NW_R-.05,t1,cc_)],[q(NW_R-.05,t0,cc_+.08),q(NW_R,t0,cc_+.08),q(NW_R,t1,cc_+.08),q(NW_R-.05,t1,cc_+.08)],M125['Gilt'])
arch125(m,lambda a,d,z:P125(a,kc1+d,z),TS,NW_Z,NW_R-.08,0,.08,.10,M125['Gilt'])
X_,Y_,_=P125(TS,(kc1+CG)/2);m.lathe(X_,Y_,NW_Z+NW_R-.10,[(.04,0),(.36,.0),(.38,.06),(.30,.10)],M125['Gilt'],20)   # the painted medallion of about 1560
m.lathe(X_,Y_,NW_Z+NW_R-.11,[(.03,0),(.28,0),(.29,.02),(.2,.03)],M125['HuntSky'],20)
for sg in (-1,1):
 bx125(m,TS+sg*(NW_R-.48),TS+sg*NW_R,kc1+.05,CG-.05,FL125,FL125+.40,M125['IntarsiaDark'])
 bx125(m,TS+sg*(NW_R-.46),TS+sg*(NW_R-.02),kc1+.07,CG-.07,FL125+.40,FL125+.50,M125['Cushion'])
 bx125(m,TS+sg*(NW_R-.05),TS+sg*NW_R,kc1,CG,FL125+.50,NW_Z,M125['Intarsia'])
 for f in (.25,.75):cm=kc1+(CG-kc1)*f;bx125(m,TS+sg*(NW_R-.07),TS+sg*(NW_R-.05),cm-.28,cm+.28,FL125+.75,NW_Z-.25,M125['IntarsiaDark'])
 bx125(m,TS+sg*(NW_R-.09),TS+sg*NW_R,kc1,CG,NW_Z-.12,NW_Z,M125['Walnut'])
# The window wall: a leaded window 1.4 x 2.3 m with a cross of mullion and transom, panelling beside it.
WZ0,WZ1=FL125+.95,FL125+3.25
wall125(m,'s',TS-NW_R,TS+NW_R,CG,CG+.3,FL125-.3,NW_Z+NW_R+.4,[(TS,1.4,WZ0,WZ1)],M125['Walnut'])
bx125(m,TS-NW_R,TS+NW_R,CG-.04,CG,FL125,WZ0-.05,M125['IntarsiaDark'])
for sg in (-1,1):bx125(m,TS+sg*.78,TS+sg*(NW_R-.08),CG-.03,CG,WZ0+.1,NW_Z-.1,M125['Intarsia'])
bx125(m,TS-.78,TS+.78,CG-.14,CG+.02,WZ0-.06,WZ0,M125['Walnut'])
bx125(m,TS-.7,TS+.7,CG+.12,CG+.15,WZ0,WZ1,M125['Daylight'])
for u in (-.7,0,.7):bx125(m,TS+u-.04,TS+u+.04,CG+.06,CG+.21,WZ0,WZ1,M125['Walnut'])
for zz in (WZ0,(WZ0+WZ1)/2+.25,WZ1):bx125(m,TS-.73,TS+.73,CG+.06,CG+.21,zz-.04,zz+.04,M125['Walnut'])
# Lead cames on the diagonal (the panorama shows small lozenge panes), clipped to the window.
fG=lambda a,d,z:P125(a,CG+d,z)
for sgn in (-1,1):
 for k in range(-16,25):
  a0=TS-.7+k*.16
  # line: a = a0 + sgn*(z-WZ0); clip to a in [TS-.7,TS+.7], z in [WZ0,WZ1]
  zlo,zhi=WZ0,WZ1
  if sgn>0:zlo=max(zlo,WZ0+(TS-.7-a0));zhi=min(zhi,WZ0+(TS+.7-a0))
  else:zlo=max(zlo,WZ0+(a0-(TS+.7)));zhi=min(zhi,WZ0+(a0-(TS-.7)))
  if zhi-zlo<.08:continue
  A=(a0+sgn*(zlo-WZ0),zlo);B=(a0+sgn*(zhi-WZ0),zhi);w=.009
  fanplate125(m,[(A[0]-w,A[1]),(A[0]+w,A[1]),(B[0]+w,B[1]),(B[0]-w,B[1])],.105,.115,fG,M125['Walnut'])
# The north niche (towards tower XII): a shallow arched niche closed by a door; the east niche (the
# privy, "cloaque" on the plan of 1780) with its painted vault.
for (u0,w,zsp,frame0,depth) in ((TC,NN_W,NN_Z,lambda a,d,z:P125(ks0-.5-d,a,z),.8),(NE_S,NE_W,NE_Z,lambda a,d,z:P125(a,kc0-.5-d,z),.8)):
 r=w/2
 for sg in (-1,1):fanplate125(m,[(u0+sg*r,FL125-.3),(u0+sg*(r+.3),FL125-.3),(u0+sg*(r+.3),zsp+r+.3),(u0+sg*r,zsp+r+.3)],0,depth,frame0,M125['Walnut'])
 fanplate125(m,[(u0-r,FL125-.3),(u0+r,FL125-.3),(u0+r,FL125),(u0-r,FL125)],0,depth,frame0,M125['Parquet2'])
 fanplate125(m,[(u0-r-.3,FL125-.3),(u0+r+.3,FL125-.3),(u0+r+.3,zsp+r+.3),(u0-r-.3,zsp+r+.3)],depth,depth+.2,frame0,M125['HuntSky'])
 for k in range(10):
  t0,t1=math.pi*k/10,math.pi*(k+1)/10;q=lambda rr,t,d:frame0(u0+rr*math.cos(t),d,zsp+rr*math.sin(t))
  hexa125(m,[q(r,t0,0),q(r+.3,t0,0),q(r+.3,t1,0),q(r,t1,0)],[q(r,t0,depth),q(r+.3,t0,depth),q(r+.3,t1,depth),q(r,t1,depth)],M125['HuntSky'] if k%2 else M125['Gilt'])
 fanplate125(m,[(u0-r+.12,FL125),(u0+r-.12,FL125),(u0+r-.12,zsp),(u0-r+.12,zsp)],depth-.05,depth,frame0,M125['Walnut'])
# The door passage to 61a through the tower wall: floor, lined sides and a flat head.
for c0_,c1_ in ((DK['c']-DK['w']/2-.2,DK['c']-DK['w']/2),(DK['c']+DK['w']/2,DK['c']+DK['w']/2+.2)):bx125(m,ks1+.5,RM125['forrum']['s0']-.25,c0_,c1_,FL125-.3,FL125+DK['h']+.25,M125['Plaster'])
bx125(m,ks1+.5,RM125['forrum']['s0']-.25,DK['c']-DK['w']/2,DK['c']+DK['w']/2,FL125+DK['h'],FL125+DK['h']+.25,M125['Plaster'])
bx125(m,ks1,RM125['forrum']['s0']-.25,DK['c']-DK['w']/2,DK['c']+DK['w']/2,FL125-.3,FL125,M125['Boards2'])
# Panelling (the panorama; about 2.6 m high): a dado, intarsia fields between fluted pilasters, an
# entablature with a gilt fillet; then the painted hunting frieze and the dentilled cornice.
def ell125(cx,cz,rx,rz,k=12):return [(cx+rx*math.cos(t*math.tau/k),cz+rz*math.sin(t*math.tau/k)) for t in range(k)]
def hunt125(frame,a,z,kind):
 # The painted stucco hunting frieze of 1572-73 (panorama): running deer, hares and trees in low
 # relief, as convex plates 2-4 cm proud of the painted landscape.
 P_=lambda pts,ma,d=.045:fanplate125(m,pts,.02,d,frame,ma)
 if kind=='tree':
  P_([(a-.04,z-.05),(a+.04,z-.05),(a+.03,z+.45),(a-.03,z+.45)],M125['Walnut'])
  P_(ell125(a,z+.72,.30,.36),M125['HuntTree'],.035);P_(ell125(a-.12,z+.55,.16,.14),M125['HuntTree'],.04)
 elif kind=='hare':
  P_(ell125(a,z+.16,.20,.09),M125['HuntBrown']);P_(ell125(a+.20,z+.24,.07,.06),M125['HuntBrown'])
  for dx in (.17,.22):P_([(a+dx,z+.27),(a+dx+.03,z+.27),(a+dx-.04,z+.47),(a+dx-.07,z+.46)],M125['HuntBrown'])
  for x0_,x1_ in ((a+.12,a+.30),(a-.15,a-.32)):P_([(x0_,z+.10),(x0_+.03,z+.13),(x1_,z+.05),(x1_-.02,z+.03)],M125['HuntBrown'])
 else:
  P_(ell125(a,z+.40,.34,.13),M125['HuntBrown'])
  P_([(a+.20,z+.42),(a+.30,z+.40),(a+.42,z+.66),(a+.33,z+.70)],M125['HuntBrown'])
  P_([(a+.32,z+.64),(a+.56,z+.60),(a+.40,z+.74)],M125['HuntBrown'])
  for x0_,x1_,z1_ in ((a+.22,a+.48,z+.12),(a+.14,a+.36,z+.05),(a-.22,a-.46,z+.10),(a-.14,a-.30,z+.02)):P_([(x0_-.03,z+.34),(x0_+.03,z+.34),(x1_+.02,z1_),(x1_-.02,z1_)],M125['HuntBrown'])
  for dx,tip in ((.34,(.26,1.0)),(.38,(.46,1.02))):P_([(a+dx,z+.70),(a+dx+.03,z+.70),(a+tip[0]+.02,z+tip[1]),(a+tip[0],z+tip[1])],M125['Walnut'],.04)
def panelled125(frame,L0,L1,gaps):
 # gaps: (a0,a1,zmax) stretches left free (openings, the fireplace) up to zmax.
 def free(z):
  iv=[(L0,L1)]
  for a0,a1,zm in gaps:
   if z<zm:iv=[(x0,x1) for x0,x1 in [(p,min(q,a0)) for p,q in iv]+[(max(p,a1),q) for p,q in iv] if x1-x0>.05]
  return iv
 for x0,x1 in free(1.0):
  fanplate125(m,[(x0,FL125),(x1,FL125),(x1,FL125+.65),(x0,FL125+.65)],0,.08,frame,M125['IntarsiaDark'])
  n=max(1,round((x1-x0)/1.3));w=(x1-x0)/n
  for k in range(n):
   a=x0+k*w;fanplate125(m,[(a+.17,FL125+.75),(a+w-.17,FL125+.75),(a+w-.17,FL125+2.25),(a+.17,FL125+2.25)],0,.06,frame,M125['Intarsia'])
   fanplate125(m,[(a+.32,FL125+.95),(a+w-.32,FL125+.95),(a+w-.32,FL125+2.05),(a+.32,FL125+2.05)],.06,.075,frame,M125['IntarsiaDark'])
  for k in range(n+1):
   a=min(max(x0+k*w,x0+.11),x1-.11)
   fanplate125(m,[(a-.11,FL125+.65),(a+.11,FL125+.65),(a+.11,FL125+2.25),(a-.11,FL125+2.25)],0,.13,frame,M125['Walnut'])
   for f in (-.05,0,.05):fanplate125(m,[(a+f-.012,FL125+.8),(a+f+.012,FL125+.8),(a+f+.012,FL125+2.1),(a+f-.012,FL125+2.1)],.13,.145,frame,M125['Walnut'])
   fanplate125(m,[(a-.14,FL125+2.1),(a+.14,FL125+2.1),(a+.14,FL125+2.27),(a-.14,FL125+2.27)],0,.16,frame,M125['Gilt'])     # capital
  fanplate125(m,[(x0,FL125+2.27),(x1,FL125+2.27),(x1,FL125+2.60),(x0,FL125+2.60)],0,.17,frame,M125['Walnut'])
  fanplate125(m,[(x0,FL125+2.40),(x1,FL125+2.40),(x1,FL125+2.44),(x0,FL125+2.44)],.17,.18,frame,M125['Gilt'])
 for x0,x1 in free(3.0):
  fanplate125(m,[(x0,FL125+2.6),(x1,FL125+2.6),(x1,FL125+3.25),(x0,FL125+3.25)],0,.02,frame,M125['HuntGreen'])
  fanplate125(m,[(x0,FL125+3.25),(x1,FL125+3.25),(x1,FL125+3.95),(x0,FL125+3.95)],0,.02,frame,M125['HuntSky'])
  n=int((x1-x0)/1.25)
  for k in range(n):hunt125(frame,x0+(x1-x0)*(k+.5)/n,FL125+2.72,('deer','tree','hare','deer','tree')[(k+int(x0*7))%5])
 fanplate125(m,[(L0,FL125+3.95),(L1,FL125+3.95),(L1,KZ),(L0,KZ)],0,.12,frame,M125['Walnut'])
 fanplate125(m,[(L0,KZ-.20),(L1,KZ-.20),(L1,KZ-.02),(L0,KZ-.02)],.12,.22,frame,M125['Walnut'])
 for k in range(int((L1-L0)/.16)):a=L0+.08+k*.16;fanplate125(m,[(a-.04,KZ-.30),(a+.04,KZ-.30),(a+.04,KZ-.20),(a-.04,KZ-.20)],.12,.2,frame,M125['Gilt'])
FP=(TC+1.75)                                                    # the fireplace on the +s wall, by the window wall
panelled125(fKW,ks0,ks1,[(TS-NW_R-.25,TS+NW_R+.25,9)])
panelled125(fKE,ks0,ks1,[(NE_S-NE_W/2-.25,NE_S+NE_W/2+.25,9)])
panelled125(fKN,kc0,kc1,[(TC-NN_W/2-.25,TC+NN_W/2+.25,9)])
panelled125(fKS,kc0,kc1,[(DK['c']-DK['w']/2-.15,DK['c']+DK['w']/2+.15,2.5),(FP-.85,FP+.85,2.8)])
# The fireplace (panorama: black carved, with caryatids): jambs with figures, a frieze, an overmantel
# with a cartouche, a cornice; a dark hearth.
fanplate125(m,[(FP-.5,FL125),(FP+.5,FL125),(FP+.5,FL125+1.3),(FP-.5,FL125+1.3)],0,.01,fKS,M125['StoneDark'])
for sg in (-1,1):
 fanplate125(m,[(FP+sg*.5,FL125),(FP+sg*.8,FL125),(FP+sg*.8,FL125+1.3),(FP+sg*.5,FL125+1.3)],0,.34,fKS,M125['Ebony'])
 x,y,_=fKS(FP+sg*.65,.40,0);m.lathe(x,y,FL125+.15,[(.10,0),(.12,.3),(.09,.7),(.11,.95),(.07,1.0),(.08,1.05),(.06,1.15)],M125['Ebony'],10)
 x,y,_=fKS(FP+sg*.65,.40,0);m.lathe(x,y,FL125+1.17,[(.03,0),(.07,.03),(.075,.09),(.05,.13)],M125['Ebony'],10)
fanplate125(m,[(FP-.85,FL125+1.3),(FP+.85,FL125+1.3),(FP+.85,FL125+1.62),(FP-.85,FL125+1.62)],0,.42,fKS,M125['Ebony'])
fanplate125(m,[(FP-.62,FL125+1.62),(FP+.62,FL125+1.62),(FP+.62,FL125+2.55),(FP-.62,FL125+2.55)],0,.24,fKS,M125['Ebony'])
fanplate125(m,[(FP-.35,FL125+1.8),(FP+.35,FL125+1.8),(FP+.35,FL125+2.35),(FP-.35,FL125+2.35)],.24,.28,fKS,M125['Gilt'])
fanplate125(m,[(FP-.75,FL125+2.55),(FP+.75,FL125+2.55),(FP+.75,FL125+2.75),(FP-.75,FL125+2.75)],0,.32,fKS,M125['Ebony'])
# The ceiling (Olsson plate of the ceiling; panorama): flat intarsia bands framing sunk rectangular
# coffers with carved gilt panels and bosses, four by four.
bx125(m,ks0,ks1,kc0,kc1,KZ+.22,KT,M125['Panel'])
nsx,ncx=4,4;bw=.30
for i in range(nsx+1):
 a=ks0+(ks1-ks0)*i/nsx;bx125(m,max(ks0,a-bw/2),min(ks1,a+bw/2),kc0,kc1,KZ,KZ+.22,M125['Intarsia'])
for j in range(ncx+1):
 a=kc0+(kc1-kc0)*j/ncx;bx125(m,ks0,ks1,max(kc0,a-bw/2),min(kc1,a+bw/2),KZ,KZ+.22,M125['Intarsia'])
# Moresque inlay in the bands (Olsson's plate: three patterns), as a dark centre line and lozenges.
for i in range(nsx+1):
 a=ks0+(ks1-ks0)*i/nsx;bx125(m,max(ks0,a-.025),min(ks1,a+.025),kc0,kc1,KZ-.006,KZ,M125['IntarsiaDark'])
for j in range(ncx+1):
 a=kc0+(kc1-kc0)*j/ncx;bx125(m,ks0,ks1,max(kc0,a-.025),min(kc1,a+.025),KZ-.006,KZ,M125['IntarsiaDark'])
for i in range(nsx+1):
 for j in range(ncx+1):
  X_,Y_,_=P125(ks0+(ks1-ks0)*i/nsx,kc0+(kc1-kc0)*j/ncx);m.box((X_,Y_,KZ-.004),(.16,.16,.012),M125['Walnut'],ANG125+math.pi/4)
for i in range(nsx):
 for j in range(ncx):
  a0,a1=ks0+(ks1-ks0)*i/nsx+bw/2,ks0+(ks1-ks0)*(i+1)/nsx-bw/2;b0,b1=kc0+(kc1-kc0)*j/ncx+bw/2,kc0+(kc1-kc0)*(j+1)/ncx-bw/2
  for (p0,p1,q0,q1) in ((a0,a1,b0,b0+.05),(a0,a1,b1-.05,b1),(a0,a0+.05,b0,b1),(a1-.05,a1,b0,b1)):bx125(m,p0,p1,q0,q1,KZ+.12,KZ+.22,M125['Gilt'])
  X_,Y_,_=P125((a0+a1)/2,(b0+b1)/2);m.lathe(X_,Y_,KZ+.13,[(.03,0),(.08,.02),(.13,.05),(.16,.08),(.14,.09)],M125['Gilt'],14)   # carved boss
  for t in range(4):
   ang=t*math.pi/2;X_,Y_,_=P125((a0+a1)/2+.30*math.cos(ang)*(a1-a0)/1.0,(b0+b1)/2+.30*math.sin(ang)*(b1-b0)/1.0);m.box((X_,Y_,KZ+.19),(.20,.10,.05),M125['Gilt'] if t%2 else M125['Walnut'],ANG125+ang)
b125_finish(m)

# ================================================================= the cut in the north tower's skin
def cut_tower125():
 # Pass 27 builds the north tower as one closed cylinder (radius 6.35 m). Kungsmaket's door passage to
 # 61a crosses its skin inside the west range. The faces inside the passage's box are cut out: the
 # skin is split by four planes and the pieces inside are deleted. A second run finds nothing to cut.
 import bmesh
 obj=bpy.data.objects.get('SM_Kalmar_Slott_Towers')
 if obj is None:print('BLOCK125_CUT no tower mesh');return 0
 assert all(abs(obj.matrix_world[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4))
 CT=B125D['cut'];me=obj.data;bm=bmesh.new();bm.from_mesh(me)
 def sc(co):dx,dy=co.x-O125[0],co.y-O125[1];return dx*U125[0]+dy*U125[1],dx*N125[0]+dy*N125[1]
 def region():
  out=[]
  for f in bm.faces:
   c=f.calc_center_median();s,cc=sc(c);zs=[v.co.z for v in f.verts]
   if CT['s0']-1.5<s<CT['s1']+1.5 and CT['c0']-1.5<cc<CT['c1']+1.5 and min(zs)<CT['z1']+.01 and max(zs)>CT['z0']-.01:out.append(f)
  return out
 nx,ny=N125
 # Cut only while the skin still passes through the box: sample points on the cylinder inside the
 # box (inset 0.1 m from its edges) and look for the nearest surface. After the cut the nearest is
 # the hole's edge, at least 0.1 m away, so a second run changes nothing.
 from mathutils.bvhtree import BVHTree
 bm.faces.ensure_lookup_table();tree=BVHTree.FromBMesh(bm)
 def _pt(cc,z):ss=TW125['s']+math.sqrt(max(0,TW125['r']**2-(cc-TW125['c'])**2));return Vector(P125(ss,cc,z))
 hits=0
 for i in range(5):
  for j in range(5):
   q=_pt(CT['c0']+.1+(CT['c1']-CT['c0']-.2)*i/4,CT['z0']+.1+(CT['z1']-CT['z0']-.2)*j/4);loc,_,_,dist=tree.find_nearest(q)
   if loc is not None and dist<.05:hits+=1
 if hits==0:
  bm.free();print('BLOCK125_CUT already open');return 0
 for co,no in (((0,0,CT['z0']),(0,0,1)),((0,0,CT['z1']),(0,0,1)),(P125(0,CT['c0'],0),(nx,ny,0)),(P125(0,CT['c1'],0),(nx,ny,0))):
  fs=region()
  if not fs:break
  geom=list(fs)+list({e for f in fs for e in f.edges})+list({v for f in fs for v in f.verts})
  bmesh.ops.bisect_plane(bm,geom=geom,plane_co=co,plane_no=no,dist=1e-5)
 gone=[]
 for f in region():
  c=f.calc_center_median();s,cc=sc(c)
  if CT['s0']<s<CT['s1'] and CT['c0']<cc<CT['c1'] and CT['z0']<c.z<CT['z1']:gone.append(f)
 if gone:bmesh.ops.delete(bm,geom=gone,context='FACES')
 bm.to_mesh(me);bm.free();me.update()
 obj['block125_cut_faces']=obj.get('block125_cut_faces',0)+len(gone);obj['block125_dropped_faces']=drop_degenerate_faces125(obj)
 obj['block125_cut']='Kungsmaket door passage, see references/block125-notes.md'
 print('BLOCK125_CUT',len(gone),'faces; dropped',obj['block125_dropped_faces']);return len(gone)
cut_tower125()
block125_names.append('SM_Kalmar_Slott_Towers')

# ================================================================= cameras
def sv_camera125(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def cam125(name,s,c,dz,ds,dc,pitch,vfov):
 # A camera in the range frame looking along (ds,dc).
 x,y,_=P125(s,c);vx,vy=U125[0]*ds+N125[0]*dc,U125[1]*ds+N125[1]*dc
 return sv_camera125(name,x,y,FL125+dz,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
block125_cameras=[
 # Photograph matches: Gyllene salen's panorama looking west (Baboş 2009), the room looking east
 # (Olsson plate, 1930s), the ceiling (Commons 2017); Kungsmaket's panorama towards the west niche
 # (Baboş 2009) and its ceiling; the door from Gyllene salen to 61a.
 cam125('671_Block125_Cal_GyllenePano',10.8,-10.5,1.6,0,1,6,74),
 cam125('672_Block125_Cal_GylleneEast',15.3,-3.2,1.5,-.32,-.95,10,62),
 cam125('673_Block125_Cal_GylleneCeiling',7.4,-4.0,1.6,.55,-.83,42,66),
 cam125('674_Block125_Cal_KungsmaketPano',TS,TC-2.5,1.5,0,1,6,82),
 cam125('675_Block125_Cal_KungsmaketCeiling',TS,TC,1.5,0,1,70,80),
 cam125('676_Block125_Forrum',1.6,-10.8,1.6,0,1,0,70),
 cam125('677_Block125_Gyllene_DoorNorth',11.9,-9.0,1.6,-1,-.1,4,70),
 ('678_Block125_Aerial_WestRange',P125(-30,40,60),P125(8,-8,12),24),
]
print('BLOCK125_GEOMETRY',len(block125_names))
