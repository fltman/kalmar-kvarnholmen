"""Pass 130: Slottskyrkan, the chapel of Kalmar slott (1589-92; Olsson's and Möller's room 86), on the
state floor of the south range (pass 27's 'SW' range), between the west and south courtyard corners.
- SM_Castle130_Slottskyrkan: the room shell. The board, tile and flag floors with the two-step
  chancel; the walls (outer 1.15 m, courtyard 0.85 m, end walls 1.28 and 0.93 m) in their painted
  zones (pale lower zone, band, salmon upper zone; the ochre altar wall); the barrel vault of
  half-elliptic section (Möller 1882: springing 3.14 m, crown 5.43 m over the floor) with a lunette
  over every window niche; the vault's plaster ribs (crown medallions, longitudinal and transverse
  ribs, the lunettes' groin ribs, the diagonals and the wall arches); ten window niches (five on the
  courtyard windows of pass 126/127, four on the outer windows, the plan's sixth courtyard niche
  blind) with their own glazing, the lunette fields with stucco rosettes, the psalm tablets on the
  piers, the sunburst with the dove, the painted drapery and the altarpiece on the altar wall, the
  west door and the door beside the altar (closed).
- SM_Castle130_Inventarier: the furnishings after the plan of c. 1780 (Krigsarkivet 0424:058:212a):
  the altar, the panelled communion rail with its kneeler, the raised pulpit gallery over the
  priest's pew, the stone font, the two commander's pews with their turned, crowned posts, eleven
  rows of closed pews and six of open benches each side of the aisle, the hymn boards, the organ at
  the west end (photographs, not in the 1780 plan) and three crystal chandeliers.
The room is a set of closed solids inside pass 27's hollow range; no existing mesh is changed.
Sources: the 1780 plan (scale in alnar), Möller's 'Profil genom Kyrkan' (1882), Commons photographs
(2009, 2015, 2017). See references/block130-notes.md.
"""
from mathutils import Vector
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B130D=json.loads((R/'source/block130.json').read_text())
block130_names=[];B130={}
for old in [k for k in list(materials) if k.startswith('M_Block130_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Vault','TownPaintWhite',(.88,.86,.82),.92,0),('Rib','TownPaintWhite',(.73,.71,.67),.90,0),('RibLine','TownPaintWhite',(.66,.40,.34),.90,0),
 ('WallUpper','TownPaintWhite',(.86,.67,.59),.92,0),('WallLower','TownPaintWhite',(.88,.86,.80),.92,0),('Band','TownPaintWhite',(.79,.60,.54),.90,0),
 ('EndWall','TownPaintWhite',(.86,.81,.75),.92,0),('AltarWall','TownPaintWhite',(.84,.66,.52),.92,0),('Tympanum','TownPaintWhite',(.42,.46,.52),.90,0),
 ('Rosette','TownPaintWhite',(.93,.92,.89),.85,0),('Tablet','TownPaintWhite',(.30,.33,.37),.80,0),('Drapery','TownPaintWhite',(.93,.91,.86),.90,0),
 ('DraperyGold','TownIvory',(.86,.72,.40),.85,0),('Gilt','TownIvory',(.80,.62,.27),.45,.35),('Painting','TownPaintBrown',(.22,.17,.12),.70,0),
 ('PewGrey','TownPaintWhite',(.56,.64,.65),.75,0),('PewFrame','TownPaintWhite',(.40,.48,.50),.75,0),('PewRail','TownPaintBrown',(.38,.20,.14),.65,0),
 ('Oak','TownPaintBrown',(.52,.40,.27),.70,0),('PulpitGreen','TownPaintGreen',(.52,.62,.60),.70,0),('Dark','TownPaintBrown',(.18,.16,.15),.75,0),
 ('PostShaft','TownPaintGreen',(.30,.38,.38),.65,0),('PostRed','TownPaintBrown',(.50,.20,.16),.60,0),('Marble','TownStone',(.47,.29,.24),.45,0),
 ('Flag','TownStone',(.48,.46,.44),.85,0),('Joint','TownStone',(.30,.29,.28),.90,0),('Tile','TownTileRed',(.38,.23,.18),.80,0),
 ('Boards','TownPaintBrown',(.52,.42,.32),.80,0),('Boards2','TownPaintBrown',(.46,.37,.28),.80,0),('Cloth','TownPaintWhite',(.95,.95,.93),.90,0),
 ('Blue','TownPaintWhite',(.25,.38,.62),.60,0),('Door','TownPaintWhite',(.56,.62,.58),.70,0),('Stone','TownStone',(.72,.71,.67),.85,0),
 ('WinFrame','TownPaintGreen',(.17,.27,.23),.60,0),('Daylight','TownPaintWhite',(.84,.90,.93),.20,0),('Crystal','TownPaintWhite',(.90,.93,.95),.10,0),
 ('Brass','TownIvory',(.78,.62,.30),.40,.60),('OrganCase','TownPaintWhite',(.62,.66,.62),.75,0),('OrganWood','TownPaintBrown',(.74,.60,.42),.70,0),
 ('Pipe','TownMetalGrey',(.74,.75,.76),.35,.70),('Candle','TownIvory',(.94,.92,.85),.80,0),
 ]:
 name='M_Block130_'+key;B130[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block130_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M130=B130

def b130_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block130_names.append(name);return Mesh(name,category)
def drop_degenerate_faces130(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 from collections import Counter
 print('BLOCK130_DROP_BY_MATERIAL',obj.name,Counter(obj.data.materials[f.material_index].name for f in bad).most_common(8))
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b130_finish(m,bevel=True):
 # The shell gets the town's small edge bevel (s21_finish). The furnishings are small, close-set parts
 # on which that bevel only produces collapsed slivers (and frame-less UVs on candle tips), so they are
 # finished without it, with the same world-scale UVs.
 nf=len(m.f)
 if bevel:obj=s21_finish(m)
 else:
  obj=m.finish();obj['massing_only']=False;me=obj.data;uv=me.uv_layers.active.data
  for poly in me.polygons:
   coords=[me.vertices[i].co for i in poly.vertices];normal=Vector((0,0,0))
   for c,d in zip(coords,coords[1:]+coords[:1]):normal+=c.cross(d)
   axis=max(range(3),key=lambda k:abs(normal[k]));axes=[k for k in range(3) if k!=axis]
   for li in poly.loop_indices:
    c=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(c[axes[0]]/4,c[axes[1]]/4)
 print('BLOCK130_FACES',m.name,'authored',nf,'finished',len(obj.data.polygons));obj['block130_dropped_faces']=drop_degenerate_faces130(obj)
 print('BLOCK130_DROPPED',obj.name,obj['block130_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=130;obj['reference_notes']='references/block130-notes.md';obj['osm_way']='';return obj

# ---------------------------------------------------------------- the range frame
# s runs along pass 27's 'SW' range from its origin (by the west tower) towards the south tower, c
# outwards (the courtyard is at c -9.3, the outer front at c 0). The altar is at the +s end.
FR130=B130D['frame'];O130,U130,N130=FR130['origin'],FR130['u'],FR130['n'];ANG130=math.atan2(U130[1],U130[0])
LV130=B130D['levels'];RM130=B130D['room']
FL130=LV130['floor'];SP130=LV130['spring'];CR130=LV130['crown'];AV130=LV130['a'];BV130=LV130['b'];CC130=LV130['cc'];ZT130=LV130['ztop']
SW130,SA130=RM130['s_w'],RM130['s_a'];COI130,CCI130,COO130,CCO130=RM130['c_oi'],RM130['c_ci'],RM130['c_oo'],RM130['c_co']
NI130=B130D['niches'];CH130=B130D['chancel'];ZCH130=FL130+CH130['risers']*CH130['rise']
def P130(s,c,z=0.0):return (O130[0]+U130[0]*s+N130[0]*c,O130[1]+U130[1]*s+N130[1]*c,z)
def bx130(m,s0,s1,c0,c1,z0,z1,ma):
 # An axis-aligned box in the range frame.
 s0,s1=min(s0,s1),max(s0,s1);c0,c1=min(c0,c1),max(c0,c1);z0,z1=min(z0,z1),max(z0,z1)
 if s1-s0<.002 or c1-c0<.002 or z1-z0<.002:return
 x,y,_=P130((s0+s1)/2,(c0+c1)/2);m.box((x,y,(z0+z1)/2),(s1-s0,c1-c0,z1-z0),ma,ANG130)
def hexa130(m,a,b,ma):
 # Closed six-faced solid from two quads a and b, corners in matching order.
 m.faces(list(a)+list(b),[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
def fan130(m,pts,d0,d1,frame,ma,center=None):
 # A flat convex shape given as (a,z) outline points in a vertical plane, extruded across d0..d1, as
 # a triangle fan (no large n-gon): round the first outline point, or round an interior centre.
 # frame(a,d,z) -> world point.
 n=len(pts)
 if center is None:
  v=[frame(a,d,z) for d in (d0,d1) for a,z in pts]
  f=[(0,i,i+1) for i in range(1,n-1)]+[(n,n+i+1,n+i) for i in range(1,n-1)]
 else:
  v=[frame(a,d,z) for d in (d0,d1) for a,z in pts]+[frame(center[0],d0,center[1]),frame(center[0],d1,center[1])]
  f=[(2*n,i,(i+1)%n) for i in range(n)]+[(2*n+1,n+(i+1)%n,n+i) for i in range(n)]
 f+=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 m.faces(v,f,ma)
def circ130(a,z,r,k=16):return [(a+r*math.cos(2*math.pi*q/k),z+r*math.sin(2*math.pi*q/k)) for q in range(k)]
def fc130(c0):return lambda a,d,z:P130(a,c0+d,z)      # plane at constant c: a along s, d along c
def fs130(s0):return lambda a,d,z:P130(s0+d,a,z)      # plane at constant s: a along c, d along s
def lathe130(m,s,c,z,prof,ma,n=12):
 x,y,_=P130(s,c);m.lathe(x,y,z,prof,ma,n)
def strip130(m,lo,hi,d0,d1,frame,ma):
 # The region between two curves lo and hi, given as (a,z) lists sampled at the same a, in a vertical
 # plane, as closed quad slabs.
 for (a0,z0),(a1,z1),(b0,w0),(b1,w1) in zip(lo,lo[1:],hi,hi[1:]):
  if w0-z0<.002 and w1-z1<.002:continue
  hexa130(m,[frame(a0,d0,z0),frame(a1,d0,z1),frame(b1,d0,w1),frame(b0,d0,w0)],[frame(a0,d1,z0),frame(a1,d1,z1),frame(b1,d1,w1),frame(b0,d1,w0)],ma)

# ---------------------------------------------------------------- the intrados
def zmain130(c):
 t=(c-CC130)/AV130
 return SP130 if abs(t)>=1 else SP130+BV130*math.sqrt(1-t*t)
def zlun130(n,s):
 x=(s-n['u_in'])/n['lun_L']
 return None if abs(x)>=1 else SP130+n['lun_R']*math.sqrt(1-x*x)
def zi130(s,c):
 # The vault's underside: the half-elliptic barrel, or a lunette (a horizontal transverse barrel over
 # a niche, on its own half of the vault) where that is higher.
 z=zmain130(c)
 for n in NI130:
  if (n['side']=='court')!=(c<CC130):continue
  zl=zlun130(n,s)
  if zl is not None and zl>z:z=zl
 return z
def nrm130(s,c,h=.02):
 # Unit normal of the intrados pointing into the room (downwards, inwards).
 zs=(zi130(s+h,c)-zi130(s-h,c))/(2*h);zc=(zi130(s,c+h)-zi130(s,c-h))/(2*h)
 vx,vy,_=P130(zs,zc);ox,oy,_=P130(0,0);v=Vector((vx-ox,vy-oy,-1.0));return v.normalized()
def groin130(n,k=40):
 # The groin curve of a lunette: where the lunette meets the main vault, from springing to springing.
 out=[]
 for j in range(k+1):
  th=math.pi*j/k;s=n['u_in']-n['lun_L']*math.cos(th);zl=SP130+n['lun_R']*math.sin(th)
  t=(zl-SP130)/BV130;dc=AV130*math.sqrt(max(0,1-t*t))
  c=CC130-dc if n['side']=='court' else CC130+dc
  out.append((s,c))
 return out

# ================================================================= the room shell
m=b130_new('SM_Castle130_Slottskyrkan','Kalmar slott/Interiör')

# ---- floors: boards under the pews, a tiled aisle, grey flags in the chancel with two steps
PW130=B130D['pews'];AISLE130=(PW130['bottom_c'][0],PW130['top_c'][1])
for c0,c1,ma in ((CCI130,AISLE130[0],None),(AISLE130[0],AISLE130[1],'Tile'),(AISLE130[1],COI130,None)):
 if ma=='Tile':
  # 0.3 m tiles in running rows with dark joints
  bx130(m,SW130,CH130['s']-.44,c0,c1,FL130-.30,FL130-.012,M130['Joint'])
  nr=round((c1-c0)/.30);w=(c1-c0)/nr;s=SW130;k=0
  while s<CH130['s']-.44-.01:
   s1=min(s+.30,CH130['s']-.44)
   for j in range(nr):bx130(m,s+.004,s1-.004,c0+j*w+.004,c0+(j+1)*w-.004,FL130-.012,FL130,M130['Tile'])
   s=s1;k+=1
 else:
  nb=max(1,round((c1-c0)/.26));w=(c1-c0)/nb;bx130(m,SW130,CH130['s']-.44,c0,c1,FL130-.30,FL130-.015,M130['Joint'])
  for j in range(nb):bx130(m,SW130,CH130['s']-.44,c0+j*w+.003,c0+(j+1)*w-.003,FL130-.015,FL130,M130['Boards' if j%2 else 'Boards2'])
# the steps (each riser 0.14 m) and the chancel's flags
for k in range(CH130['risers']):
 bx130(m,CH130['s']-.22*(CH130['risers']-k),CH130['s']-.22*(CH130['risers']-k-1),CCI130,COI130,FL130-.30,FL130+CH130['rise']*(k+1),M130['Stone'])
bx130(m,CH130['s'],SA130,CCI130,COI130,FL130-.30,ZCH130-.012,M130['Joint'])
ns_=round((SA130-CH130['s'])/.62);nc_=round((COI130-CCI130)/.62)
for i in range(ns_):
 for j in range(nc_):
  a0=CH130['s']+(SA130-CH130['s'])*i/ns_;a1=CH130['s']+(SA130-CH130['s'])*(i+1)/ns_;b0=CCI130+(COI130-CCI130)*j/nc_;b1=CCI130+(COI130-CCI130)*(j+1)/nc_
  bx130(m,a0+.004,a1-.004,b0+.004,b1-.004,ZCH130-.012,ZCH130,M130['Flag'])

# ---- walls
BANDS130=[(FL130-.30,FL130+1.75,M130['WallLower']),(FL130+1.75,FL130+2.0,M130['Band']),(FL130+2.0,ZT130,M130['WallUpper'])]
def lwall130(m,c_in,c_out,s0,s1,z0,z1,holes,bands,K=14):
 # A long wall between c_in (room face) and c_out, from s0 to s1, with window niches: each niche has
 # its own axis, half-width, springing and rise at the room face and at the window (splayed and
 # skewed niches), a flat sill and an elliptic head. Built of closed slabs: piers per paint band,
 # the parapet under each sill, and the head over each niche up to the wall's top.
 at_i=at_o=s0
 for h in sorted(holes,key=lambda h:h['u_in'])+[None]:
  li,lo_=(h['u_in']-h['r_in'],h['u_out']-h['r_out']) if h else (s1,s1)
  for za,zb,ma in bands:
   za,zb=max(za,z0),min(zb,z1)
   if zb-za>.002 and li-at_i>.002:
    hexa130(m,[P130(at_i,c_in,za),P130(li,c_in,za),P130(li,c_in,zb),P130(at_i,c_in,zb)],[P130(at_o,c_out,za),P130(lo_,c_out,za),P130(lo_,c_out,zb),P130(at_o,c_out,zb)],ma)
  if h is None:break
  ri,ro=h['u_in']+h['r_in'],h['u_out']+h['r_out']
  for za,zb,ma in bands:
   za,zb=max(za,z0),min(zb,h['zb'])
   if zb-za>.002:hexa130(m,[P130(li,c_in,za),P130(ri,c_in,za),P130(ri,c_in,zb),P130(li,c_in,zb)],[P130(lo_,c_out,za),P130(ro,c_out,za),P130(ro,c_out,zb),P130(lo_,c_out,zb)],ma)
  mah=[ma for za,zb,ma in bands if za<=h['zs_in']<zb][0]
  def A(th,inner):
   return (h['u_in']+h['r_in']*math.cos(th),h['zs_in']+h['h_in']*math.sin(th)) if inner else (h['u_out']+h['r_out']*math.cos(th),h['zs_out']+h['h_out']*math.sin(th))
  for j in range(K):
   t0,t1=math.pi*j/K,math.pi*(j+1)/K;(a0,b0),(a1,b1)=A(t0,True),A(t1,True);(e0,f0),(e1,f1)=A(t0,False),A(t1,False)
   hexa130(m,[P130(a0,c_in,b0),P130(a1,c_in,b1),P130(a1,c_in,z1),P130(a0,c_in,z1)],[P130(e0,c_out,f0),P130(e1,c_out,f1),P130(e1,c_out,z1),P130(e0,c_out,z1)],mah)
  # the sill: a limestone board over the parapet
  hexa130(m,[P130(li+.02,c_in,h['zb']),P130(ri-.02,c_in,h['zb']),P130(ri-.02,c_in,h['zb']+.035),P130(li+.02,c_in,h['zb']+.035)],
   [P130(lo_+.02,c_out,h['zb']),P130(ro-.02,c_out,h['zb']),P130(ro-.02,c_out,h['zb']+.035),P130(lo_+.02,c_out,h['zb']+.035)],M130['Stone'])
  at_i,at_o=ri,ro
SWW130=SW130-RM130['t_w'];SAW130=SA130+RM130['t_a']
lwall130(m,COI130,COO130,SWW130,SAW130,FL130-.30,ZT130,[n for n in NI130 if n['side']=='out'],BANDS130)
lwall130(m,CCI130,CCO130,SWW130,SAW130,FL130-.30,ZT130,[n for n in NI130 if n['side']=='court'],BANDS130)
def ewall130(m,s_in,s_out,z0,z1,doors,bands):
 # An end wall across the range (c from the courtyard face to the outer face) with door openings
 # (centre c, width, bottom, top), of closed boxes split at the bands and the door heads.
 zs=sorted(set([z0,z1]+[v for _,_,b,t in doors for v in (b,t) if z0<v<z1]+[v for a,b,_ in bands for v in (a,b) if z0<v<z1]))
 for lo,hi in zip(zs,zs[1:]):
  mid=(lo+hi)/2;ma=[x for a,b,x in bands if a<=mid<b][0];cuts=sorted((c-w/2,c+w/2) for c,w,b,t in doors if b<mid<t);at=CCI130
  for l,r in cuts+[(COI130,COI130)]:
   if l>at+.001:bx130(m,s_in,s_out,at,l,lo,hi,ma)
   at=max(at,r)
DW130=B130D['doors']
ewall130(m,SW130,SWW130,FL130-.30,ZT130,[(DW130['west']['c'],DW130['west']['w'],FL130,FL130+DW130['west']['h'])],
 [(FL130-.30,FL130+1.75,M130['WallLower']),(FL130+1.75,FL130+2.0,M130['Band']),(FL130+2.0,ZT130+.01,M130['EndWall'])])
ewall130(m,SA130,SAW130,FL130-.30,ZT130,[(DW130['altar']['c'],DW130['altar']['w'],ZCH130,ZCH130+DW130['altar']['h'])],[(FL130-.31,ZT130+.01,M130['AltarWall'])])
# doors: closed panelled leaves set back in the reveal, a plain stone surround on the room side
for s_face,sg,d,zb in ((SW130,-1,DW130['west'],FL130),(SA130,1,DW130['altar'],ZCH130)):
 c,w,hh=d['c'],d['w'],d['h'];leaf=s_face+sg*.42
 bx130(m,leaf-.025,leaf+.025,c-w/2,c+w/2,zb,zb+hh,M130['Door'])
 for k in range(2):
  z0_=zb+.12+k*(hh-.24)/2+(.05 if k else 0);z1_=zb+.12+(k+1)*(hh-.24)/2-(.0 if k else .05)
  for c0_,c1_ in ((c-w/2+.10,c-w/2+.14),(c+w/2-.14,c+w/2-.10)):bx130(m,leaf-sg*.045,leaf-sg*.025,c0_,c1_,z0_,z1_,M130['Stone' if False else 'Door'])
  bx130(m,leaf-sg*.045,leaf-sg*.025,c-w/2+.10,c+w/2-.10,z0_,z0_+.04,M130['Door']);bx130(m,leaf-sg*.045,leaf-sg*.025,c-w/2+.10,c+w/2-.10,z1_-.04,z1_,M130['Door'])
 bx130(m,leaf-sg*.03,leaf-sg*.025,c-w/2+.25,c-w/2+.32,zb+hh*.48,zb+hh*.50,M130['Brass'])
 for c0_,c1_ in ((c-w/2-.16,c-w/2),(c+w/2,c+w/2+.16)):bx130(m,s_face-sg*.05,s_face,c0_,c1_,zb,zb+hh+.16,M130['Stone'])
 bx130(m,s_face-sg*.05,s_face,c-w/2-.16,c+w/2+.16,zb+hh,zb+hh+.16,M130['Stone'])
 bx130(m,s_face-sg*.08,s_face,c-w/2-.22,c+w/2+.22,zb+hh+.16,zb+hh+.24,M130['Stone'])

# ---- the vault: a closed solid from the intrados up to the walls' top
NS130=360;NC130=120
SS130=[SW130+(SA130-SW130)*i/NS130 for i in range(NS130+1)]
CS130=[CC130-AV130*math.cos(math.pi*j/NC130) for j in range(NC130+1)]
CS130[0]=CCI130;CS130[-1]=COI130
vb=[P130(s,c,zi130(s,c)) for s in SS130 for c in CS130];vt=[P130(s,c,ZT130) for s in SS130 for c in CS130]
nc=NC130+1;off=len(vb)
def ix(i,j):return i*nc+j
fb=[(ix(i,j),ix(i,j+1),ix(i+1,j+1),ix(i+1,j)) for i in range(NS130) for j in range(NC130)]
ft=[(ix(i,j),ix(i+1,j),ix(i+1,j+1),ix(i,j+1)) for i in range(NS130) for j in range(NC130)]
sides=[]
for i in range(NS130):
 for j in (0,NC130):sides.append((ix(i,j),ix(i+1,j),off+ix(i+1,j),off+ix(i,j)))
for i in (0,NS130):
 for j in range(NC130):sides.append((ix(i,j),ix(i,j+1),off+ix(i,j+1),off+ix(i,j)))
# The top and sides share the intrados' vertices: one closed solid.
vv=vb+vt;m.faces(vv,fb+[tuple(off+k for k in f) for f in ft]+sides,M130['Vault']);m.sm[len(m.sm)-len(fb)-len(ft)-len(sides):len(m.sm)-len(ft)-len(sides)]=[True]*len(fb)

# ---- ribs: plaster bands on the intrados
def rib130(m,path,w=.24,d=.035,ma=None,line=True):
 # A band along a path of (s,c) points on the intrados, standing d into the room, as closed segments;
 # a thin red line along each edge, as the painted borders of the bands.
 ma=ma or M130['Rib'];P=[Vector(P130(s,c,zi130(s,c))) for s,c in path];Nn=[nrm130(s,c) for s,c in path]
 if len(P)<2:return
 Sd=[]
 for k in range(len(P)):
  t=(P[min(k+1,len(P)-1)]-P[max(k-1,0)]);sd=t.cross(Nn[k])
  Sd.append(sd.normalized() if sd.length>1e-9 else Vector((1,0,0)))
 for k in range(len(P)-1):
  q=lambda kk,a,b:tuple(P[kk]+Sd[kk]*a+Nn[kk]*b)
  hexa130(m,[q(k,-w/2,d),q(k,w/2,d),q(k,w/2,-.02),q(k,-w/2,-.02)],[q(k+1,-w/2,d),q(k+1,w/2,d),q(k+1,w/2,-.02),q(k+1,-w/2,-.02)],ma)
  if line:
   for a in (-w/2-.035,w/2+.005):
    hexa130(m,[q(k,a,.004),q(k,a+.03,.004),q(k,a+.03,-.02),q(k,a,-.02)],[q(k+1,a,.004),q(k+1,a+.03,.004),q(k+1,a+.03,-.02),q(k+1,a,-.02)],M130['RibLine'])
def line130(p,q,k):return [(p[0]+(q[0]-p[0])*i/k,p[1]+(q[1]-p[1])*i/k) for i in range(k+1)]
def down130(s,side,c_top,k=24):
 # From c_top down to the wall springing at constant s, sampled evenly in the ellipse's angle.
 t0=math.acos(max(-1,min(1,(c_top-CC130)/AV130)));t1=0.0 if side=='out' else math.pi
 return [(s,CC130+AV130*math.cos(t0+(t1-t0)*i/k)) for i in range(k+1)]
LR130=1.55   # the longitudinal ribs, 1.55 m either side of the crown
RG130=B130D['rings']
for cl in (CC130-LR130,CC130+LR130):rib130(m,line130((SW130+.12,cl),(SA130-.12,cl),180))
TR130=sorted(set([round(r-1.95,3) for r in RG130]+[round(RG130[-1]+1.95,3)]))
for st in TR130:
 if SW130+.2<st<SA130-.2:rib130(m,line130((st,CC130-LR130),(st,CC130+LR130),24))
for r in RG130:
 ring=[(r+.62*math.cos(2*math.pi*k/40),CC130+.62*math.sin(2*math.pi*k/40)) for k in range(41)];rib130(m,ring,w=.20)
 lst=[t for t in TR130 if t<r];nxt=[t for t in TR130 if t>r]
 if lst:rib130(m,line130((lst[-1],CC130),(r-.72,CC130),10),w=.16)
 if nxt:rib130(m,line130((r+.72,CC130),(nxt[0],CC130),10),w=.16)
for n in NI130:
 g=groin130(n);rib130(m,g)
 apex=g[len(g)//2];sg=-1 if n['side']=='court' else 1;cl=CC130+sg*LR130
 for ds in (-1.95,1.95):
  if SW130+.2<n['u_in']+ds<SA130-.2:rib130(m,line130(apex,(n['u_in']+ds,cl),24))
# pier ribs: between neighbouring lunettes (and next to the end walls), from the springing up to the
# longitudinal rib
for side in ('court','out'):
 ns=sorted((n for n in NI130 if n['side']==side),key=lambda n:n['u_in']);sg=-1 if side=='court' else 1
 cuts=[(ns[k]['u_in']+ns[k]['lun_L']+ns[k+1]['u_in']-ns[k+1]['lun_L'])/2 for k in range(len(ns)-1)]
 for s in cuts:rib130(m,down130(s,side,CC130+sg*LR130)[::-1])
# wall arches at both end walls
for s in (SW130+.13,SA130-.13):rib130(m,[(s,CC130-AV130*math.cos(math.pi*k/60)) for k in range(61)],w=.26)

# ---- lunette fields: grey-blue, with white stucco rosettes, between the niche's arch and the lunette
for n in NI130:
 cw=CCI130 if n['side']=='court' else COI130;sg=1 if n['side']=='court' else -1
 fr=fc130(cw);K=24
 def lunz(a):z=zlun130(n,a);return SP130 if z is None else z
 for a0,a1,arch in ((n['u_in']-n['lun_L']+.01,n['u_in']-n['r_in'],False),(n['u_in']-n['r_in'],n['u_in']+n['r_in'],True),(n['u_in']+n['r_in'],n['u_in']+n['lun_L']-.01,False)):
  xs=[a0+(a1-a0)*k/K for k in range(K+1)]
  lo=[(x,(n['zs_in']+n['h_in']*math.sqrt(max(0,1-((x-n['u_in'])/n['r_in'])**2))) if arch else SP130) for x in xs]
  hi=[(x,lunz(x)-.004) for x in xs]
  strip130(m,lo,hi,0,sg*.008,fr,M130['Tympanum'])
 ztop=SP130+n['lun_R'];zar=n['zs_in']+n['h_in'];zr=(ztop+zar)/2
 for k,(dx,dz,r) in enumerate(((0,0,.16),(-.42,-.10,.11),(.42,-.10,.11))):
  zz=zr+dz
  if zz+r>lunz(n['u_in']+dx)-.05 or zz-r<n['zs_in']+n['h_in']*math.sqrt(max(0,1-(dx/n['r_in'])**2))+.03 and abs(dx)<n['r_in']:continue
  fan130(m,circ130(n['u_in']+dx,zz,r),sg*.008,sg*.03,fr,M130['Rosette'],(n['u_in']+dx,zz))
  fan130(m,circ130(n['u_in']+dx,zz,r*.45,12),sg*.03,sg*.05,fr,M130['Rosette'],(n['u_in']+dx,zz))
  for q in range(8):
   a=2*math.pi*q/8;fan130(m,circ130(n['u_in']+dx+r*.72*math.cos(a),zz+r*.72*math.sin(a),r*.22,8),sg*.03,sg*.042,fr,M130['Rosette'],(n['u_in']+dx+r*.72*math.cos(a),zz+r*.72*math.sin(a)))

# ---- window glazing at the outer end of each niche (the room's own panes; pass 27's glass is behind)
for n in NI130:
 out=n['side']=='out';cg=COO130-.04 if out else CCO130+.04;sg=-1 if out else 1   # sg: towards the room
 u,r,zb,zs,hh=n['u_out'],n['r_out'],n['zb'],n['zs_out'],n['h_out']
 bx130(m,u-r+.02,u+r-.02,cg-.01,cg+.01,zb+.04,zs,M130['Daylight'])
 fan130(m,[(u,zs)]+[(u+(r-.02)*math.cos(math.pi*k/12),zs+(hh-.02)*math.sin(math.pi*k/12)) for k in range(13)],-.01,.01,fc130(cg),M130['Daylight'])
 for a0,a1 in ((u-r,u-r+.07),(u+r-.07,u+r)):bx130(m,a0,a1,cg-.02,cg+sg*.07,zb+.035,zs,M130['WinFrame'])
 bx130(m,u-r,u+r,cg-.02,cg+sg*.07,zb+.035,zb+.10,M130['WinFrame']);bx130(m,u-r,u+r,cg-.02,cg+sg*.07,zs-.05,zs+.02,M130['WinFrame'])
 for k in (1,2):a=u-r+2*r*k/3;bx130(m,a-.025,a+.025,cg-.015,cg+sg*.05,zb+.10,zs,M130['WinFrame'])
 zt=zb+.10+(zs-zb-.10)*.66;bx130(m,u-r,u+r,cg-.015,cg+sg*.06,zt-.035,zt+.035,M130['WinFrame'])
 for k in range(1,4):z=zb+.10+(zt-zb-.10)*k/4;bx130(m,u-r+.07,u+r-.07,cg-.012,cg+sg*.035,z-.012,z+.012,M130['WinFrame'])
 z=(zt+zs)/2;bx130(m,u-r+.07,u+r-.07,cg-.012,cg+sg*.035,z-.012,z+.012,M130['WinFrame'])

# ---- psalm tablets on the piers (dark slate, arched head, light border and lines of text)
def tablet130(m,s,side):
 cw=CCI130 if side=='court' else COI130;sg=1 if side=='court' else -1;fr=fc130(cw)
 z0,w,hr=FL130+2.10,.82,round(SP130+.08-.41-(FL130+2.10),3)
 for d0,d1,ext,ma in ((.002,.012,.05,M130['Rib']),(.012,.022,0,M130['Tablet'])):
  r=w/2+ext;pts=[(s+r*math.cos(math.pi*k/12),z0+hr+r*math.sin(math.pi*k/12)) for k in range(13)]+[(s-r,z0-ext),(s+r,z0-ext)]
  fan130(m,pts,sg*d0,sg*d1,fr,ma,(s,z0+hr*.6))
 for k in range(7):
  zz=z0+.12+k*.15;ww=w*.66 if k else w*.40
  bx130(m,s-ww/2,s+ww/2,cw+sg*.022,cw+sg*.026,zz,zz+.035,M130['Rosette'])
SUN130=B130D['sun']
for side in ('court','out'):
 ns=sorted((n for n in NI130 if n['side']==side),key=lambda n:n['u_in'])
 edges=[SW130]+[v for n in ns for v in (n['u_in']-max(n['r_in'],.85),n['u_in']+max(n['r_in'],.85))]+[SA130]
 for a,b in zip(edges[::2],edges[1::2]):
  span=b-a
  if span<1.25:continue
  k=2 if span>5.0 else 1
  for q in range(k):
   s=a+span*(q+1)/(k+1)
   tablet130(m,s,side)
# ---- the sunburst with the dove, over the pulpit's west end on the courtyard wall
def fvault130(sq,cq,zq):
 # A plane tangent to the intrados at (sq, cq), 0.05 m into the room: a along s, z up the vault, d
 # along the vault's normal (into the room).
 nr=nrm130(sq,cq);e1=Vector(P130(1,0,0))-Vector(P130(0,0,0));e2=nr.cross(e1).normalized()
 if e2.z<0:e2=-e2
 Q=Vector(P130(sq,cq,zi130(sq,cq)))+nr*.05
 return lambda a,d,z:tuple(Q+e1*(a-sq)+e2*(z-zq)+nr*d)
sx_,sz_,sr=SUN130['s'],SUN130['z'],SUN130['r'];fr=fvault130(sx_,CCI130+SUN130['dc'],sz_)
fan130(m,circ130(sx_,sz_,.22,20),0,.04,fr,M130['Gilt'],(sx_,sz_))
for k in range(24):
 a=2*math.pi*k/24;L=sr if k%2 else sr*.72;a0,a1=a-.07,a+.07
 fan130(m,[(sx_+.20*math.cos(a0),sz_+.20*math.sin(a0)),(sx_+L*math.cos(a),sz_+L*math.sin(a)),(sx_+.20*math.cos(a1),sz_+.20*math.sin(a1))],.005,.025,fr,M130['Gilt'])
fan130(m,[(sx_+.11*math.cos(2*math.pi*k/14),sz_-.02+.05*math.sin(2*math.pi*k/14)) for k in range(14)],.04,.07,fr,M130['Rosette'],(sx_,sz_-.02))
for sg in (-1,1):fan130(m,[(sx_,sz_),(sx_+sg*.16,sz_+.12),(sx_+sg*.19,sz_+.02),(sx_+sg*.05,sz_-.04)],.04,.06,fr,M130['Rosette'])

# ---- the altar wall: painted drapery canopy and the altarpiece
AL130=B130D['altar'];cA=(AL130['c0']+AL130['c1'])/2;fa=fs130(SA130)
def tent130(w0,w1,z0,z1,apex):
 return [(cA,apex),(cA-w1,z1),(cA-w0*.92,(z0+z1)/2),(cA-w0,z0),(cA+w0,z0),(cA+w0*.92,(z0+z1)/2),(cA+w1,z1)]
fan130(m,tent130(1.75,.62,ZCH130+1.15,ZCH130+4.35,ZCH130+4.75),-.004,-.010,fa,M130['Drapery'])
fan130(m,tent130(1.00,.34,ZCH130+1.20,ZCH130+3.70,ZCH130+4.05),-.010,-.016,fa,M130['DraperyGold'])
fan130(m,[(cA,ZCH130+5.05),(cA-.38,ZCH130+4.62),(cA+.38,ZCH130+4.62)],-.004,-.012,fa,M130['Drapery'])
zpb=ZCH130+1.00+.40;wp,hp=1.30,1.85
bx130(m,SA130-.13,SA130,cA-wp/2,cA+wp/2,zpb,zpb+hp,M130['Gilt'])
bx130(m,SA130-.15,SA130-.13,cA-wp/2+.12,cA+wp/2-.12,zpb+.12,zpb+hp-.12,M130['Painting'])
fan130(m,[(cA-.45,zpb+hp),(cA+.45,zpb+hp),(cA+.30,zpb+hp+.30),(cA,zpb+hp+.55),(cA-.30,zpb+hp+.30)],-.02,-.12,fa,M130['Gilt'])
fan130(m,[(cA-.55,zpb),(cA-.25,zpb-.32),(cA+.25,zpb-.32),(cA+.55,zpb)],-.02,-.10,fa,M130['Gilt'])
b130_finish(m)

# ================================================================= the furnishings
m=b130_new('SM_Castle130_Inventarier','Kalmar slott/Interiör')
# ---- altar, rail, kneeler, platform
RL130=B130D['rail']
def rail_pt130(th,off=0.0):
 # Half-ellipse round the altar: th -pi/2..pi/2, off outwards (metres, approximately normal).
 s=SA130-RL130['depth']*math.cos(th);c=RL130['c_mid']+RL130['half']*math.sin(th)
 ns,nc=-math.cos(th)/RL130['depth'],math.sin(th)/RL130['half'];L=math.hypot(ns,nc)
 return s+off*ns/L,c+off*nc/L
NR130=28;TH130=[-math.pi/2+math.pi*k/NR130 for k in range(NR130+1)]
pl=[(SA130,RL130['c_mid'])]+[rail_pt130(t,-.06) for t in TH130]
x0,y0=pl[0];m.faces([P130(s,c,z) for z in (ZCH130,ZCH130+RL130['platform']) for s,c in pl],
 [(0,i+1,i) for i in range(1,len(pl)-1)]+[(len(pl),len(pl)+i,len(pl)+i+1) for i in range(1,len(pl)-1)]+[(i,i+1,len(pl)+i+1,len(pl)+i) for i in range(1,len(pl)-1)]+[(0,1,len(pl)+1,len(pl)),(len(pl)-1,0,len(pl),2*len(pl)-1)],M130['Stone'])
def ring130(m,o0,o1,z0,z1,ma,ks=None):
 for k in (ks if ks is not None else range(NR130)):
  t0,t1=TH130[k],TH130[k+1];a=[rail_pt130(t0,o0),rail_pt130(t0,o1),rail_pt130(t1,o1),rail_pt130(t1,o0)]
  hexa130(m,[P130(s,c,z0) for s,c in a],[P130(s,c,z1) for s,c in a],ma)
zr0=ZCH130;zr1=ZCH130+RL130['h']
ring130(m,-.06,.06,zr0,zr1-.07,M130['PulpitGreen']);ring130(m,-.10,.10,zr1-.07,zr1,M130['PewRail']);ring130(m,-.08,.08,zr0,zr0+.10,M130['Dark'])
ring130(m,.08,.42,zr0,zr0+.13,M130['Cloth'])
for k in range(0,NR130,2):
 # a raised panel with a gilt cartouche on the outside of each pair of segments
 ring130(m,.06,.075,zr0+.18,zr1-.15,M130['PewFrame'],[k]);ring130(m,.075,.085,zr0+.30,zr1-.30,M130['Gilt'],[k])
bx130(m,AL130['s0'],AL130['s1'],AL130['c0'],AL130['c1'],ZCH130+RL130['platform'],ZCH130+AL130['h'],M130['Stone'])
bx130(m,AL130['s0']-.04,AL130['s1'],AL130['c0']-.04,AL130['c1']+.04,ZCH130+AL130['h']-.03,ZCH130+AL130['h']+.01,M130['Cloth'])
bx130(m,AL130['s0']-.03,AL130['s0']-.01,AL130['c0']+.05,AL130['c1']-.05,ZCH130+RL130['platform']+.08,ZCH130+AL130['h']-.06,M130['PulpitGreen'])
bx130(m,AL130['s0']-.045,AL130['s0']-.03,(AL130['c0']+AL130['c1'])/2-.35,(AL130['c0']+AL130['c1'])/2+.35,ZCH130+.35,ZCH130+.78,M130['Gilt'])
for dc in (-.85,.85):
 lathe130(m,AL130['s0']+.40,cA+dc,ZCH130+AL130['h']+.01,[(.08,0),(.08,.03),(.035,.06),(.03,.30),(.05,.34),(.03,.40),(.06,.44),(.02,.46)],M130['Blue'],10)
 lathe130(m,AL130['s0']+.40,cA+dc,ZCH130+AL130['h']+.46,[(.018,0),(.018,.30),(.008,.32)],M130['Candle'],8)
bx130(m,AL130['s0']+.35,AL130['s0']+.39,cA-.02,cA+.02,ZCH130+AL130['h'],ZCH130+AL130['h']+.45,M130['Gilt'])
bx130(m,AL130['s0']+.35,AL130['s0']+.39,cA-.13,cA+.13,ZCH130+AL130['h']+.30,ZCH130+AL130['h']+.34,M130['Gilt'])
# hymn boards
for cb in (cA+1.62,cA-1.70):
 bx130(m,SA130-.06,SA130,cb-.30,cb+.30,ZCH130+1.55,ZCH130+2.55,M130['Gilt']);bx130(m,SA130-.075,SA130-.06,cb-.24,cb+.24,ZCH130+1.62,ZCH130+2.48,M130['Tablet'])
 fan130(m,[(cb-.30,ZCH130+2.55),(cb+.30,ZCH130+2.55),(cb+.15,ZCH130+2.75),(cb,ZCH130+2.95),(cb-.15,ZCH130+2.75)],-.02,-.06,fs130(SA130),M130['Gilt'])
 fan130(m,[(cb,ZCH130+1.30),(cb-.30,ZCH130+1.55),(cb+.30,ZCH130+1.55)],-.02,-.05,fs130(SA130),M130['Gilt'])
 for k in range(3):bx130(m,SA130-.085,SA130-.075,cb-.14,cb+.14,ZCH130+1.75+k*.25,ZCH130+1.88+k*.25,M130['Rosette'])
# ---- the pulpit gallery (b, over the priest's pew d): dark panelled base, a deck at 1.2 m, a
# green-grey parapet of panels with gilt cartouches (one glazed), cornices, a book desk and a post
PU130=B130D['pulpit'];zd=ZCH130+PU130['deck'];zp=zd+PU130['parapet'];cf=PU130['c0'];s0p,s1p=PU130['s0'],PU130['s1']
bx130(m,s0p+.60,s1p,cf-.25,CCI130,FL130,zd-.12,M130['Dark'])
for k in range(6):
 a=s0p+.65+(s1p-s0p-.75)*k/6;bx130(m,a+.08,a+(s1p-s0p-.75)/6-.08,cf-.25,cf-.23,FL130+.25,zd-.30,M130['PostRed'])
bx130(m,s0p,s1p,cf-.05,CCI130,zd-.12,zd,M130['PulpitGreen'])
bx130(m,s0p-.04,s1p,cf+.04,cf-.10,zd-.18,zd-.06,M130['Gilt'])
bx130(m,s0p,s1p,cf-.10,cf,zd,zp,M130['PulpitGreen']);bx130(m,s0p,s0p+.10,cf,CCI130,zd,zp,M130['PulpitGreen'])
bx130(m,s0p-.06,s1p,cf+.06,cf-.14,zp,zp+.09,M130['PulpitGreen']);bx130(m,s0p-.06,s0p+.14,cf+.06,CCI130,zp,zp+.09,M130['PulpitGreen'])
NP130=6;pw=(s1p-s0p-.10)/NP130
for k in range(NP130):
 a=s0p+.05+k*pw
 bx130(m,a-.05,a+.05,cf,cf+.04,zd+.02,zp,M130['PulpitGreen'])
 a0,a1=a+.13,a+pw-.13;b0,b1=zd+.14,zp-.12
 for q0,q1,r0,r1 in ((a0,a1,b0,b0+.04),(a0,a1,b1-.04,b1),(a0,a0+.04,b0,b1),(a1-.04,a1,b0,b1)):bx130(m,q0,q1,cf,cf+.025,r0,r1,M130['Gilt'])
 if k==3:bx130(m,a0+.04,a1-.04,cf-.02,cf+.005,b0+.04,b1-.04,M130['Crystal'])
 else:fan130(m,[((a0+a1)/2,b1-.10),(a1-.10,(b0+b1)/2+.05),((a0+a1)/2,b0+.10),(a0+.10,(b0+b1)/2-.05)],cf+.025,cf+.04,fc130(0),M130['Gilt'],((a0+a1)/2,(b0+b1)/2))
 fan130(m,[(a+pw/2,zd-.20),(a+pw/2-.16,zd-.08),(a+pw/2+.16,zd-.08)],cf+.02,cf+.05,fc130(0),M130['Gilt'])
bx130(m,s0p,s1p,cf+.05,cf,zp+.04,zp+.06,M130['Gilt'])
lathe130(m,s0p+.30,cf-.35,FL130,[(.16,0),(.16,.12),(.09,.18),(.07,.6),(.10,.72),(.08,.80),(.08,zd-FL130-.30),(.14,zd-FL130-.16),(.16,zd-FL130-.12)],M130['PulpitGreen'],12)
hexa130(m,[P130(s0p+.15,cf-.05,zp+.09),P130(s0p+.75,cf-.05,zp+.09),P130(s0p+.75,cf-.05,zp+.12),P130(s0p+.15,cf-.05,zp+.12)],
 [P130(s0p+.15,cf-.50,zp+.30),P130(s0p+.75,cf-.50,zp+.30),P130(s0p+.75,cf-.50,zp+.33),P130(s0p+.15,cf-.50,zp+.33)],M130['PulpitGreen'])
bx130(m,s0p+.25,s0p+.65,cf-.40,cf-.12,zp+.20,zp+.26,M130['Cloth'])
# ---- the stone font
FT130=B130D['font'];zf=ZCH130 if FT130['s']>CH130['s'] else FL130
lathe130(m,FT130['s'],FT130['c'],zf,[(.30,0),(.30,.10),(.24,.15),(.19,.22),(.17,.50),(.21,.56),(.21,.60)],M130['Marble'],8)
lathe130(m,FT130['s'],FT130['c'],zf+.60,[(.12,0),(.20,.05),(.28,.16),(.33,.30),(.34,.38),(.31,.40),(.27,.37)],M130['Marble'],16)
# ---- the commander's pews (c), with turned and crowned posts at their corners
def post130(s,c,z):
 # Turned post (photographs 2015/2017): a slender shaft, two red melon knops, a baluster, a gilt crown.
 lathe130(m,s,c,z,[(.06,0),(.06,.10),(.045,.14),(.04,1.0),(.05,1.05)],M130['PostShaft'],12)
 lathe130(m,s,c,z+1.05,[(.05,0),(.085,.06),(.10,.14),(.095,.22),(.06,.28),(.04,.31)],M130['PostRed'],12)
 lathe130(m,s,c,z+1.36,[(.035,0),(.035,.08),(.06,.20),(.035,.32),(.03,.50),(.05,.55),(.035,.58)],M130['PostShaft'],12)
 lathe130(m,s,c,z+1.94,[(.04,0),(.07,.05),(.085,.12),(.08,.19),(.045,.24)],M130['PostRed'],12)
 lathe130(m,s,c,z+2.18,[(.035,0),(.065,.03),(.075,.12),(.05,.14),(.02,.21),(.01,.24)],M130['Gilt'],8)
CPZ130=1.15
for cp in B130D['cpews']:
 s0_=B130D['pews']['closed'][0];s1_=cp['s1'];c0_,c1_=min(cp['c0'],cp['c1']),max(cp['c0'],cp['c1'])
 aisle_c=min((cp['c0'],cp['c1']),key=lambda v:abs(v-CC130));wall_c=max((cp['c0'],cp['c1']),key=lambda v:abs(v-CC130))   # the side facing the aisle
 lo,hi=min(aisle_c,wall_c),max(aisle_c,wall_c)
 bx130(m,s1_-.05,s1_,lo,hi,FL130,FL130+CPZ130,M130['PewGrey'])
 ca=aisle_c;sg=1 if ca>wall_c else -1
 bx130(m,s0_,s1_,ca-sg*.05,ca,FL130,FL130+CPZ130,M130['PewGrey'])
 bx130(m,s1_-.07,s1_+.02,lo,hi,FL130+CPZ130,FL130+CPZ130+.06,M130['PewRail']);bx130(m,s0_,s1_,ca-sg*.07,ca+sg*.02,FL130+CPZ130,FL130+CPZ130+.06,M130['PewRail'])
 bx130(m,s1_-.02,s1_,lo+.08,hi-.08,FL130+CPZ130-.12,FL130+CPZ130-.08,M130['Gilt'])
 bx130(m,s0_+.05,s0_+.48,lo,hi,FL130+.42,FL130+.47,M130['PewGrey'])
 for k in range(3):
  a0=lo+.10+(hi-lo-.20)*k/3;a1=lo+.10+(hi-lo-.20)*(k+1)/3-.08
  bx130(m,s1_,s1_+.012,a0,a1,FL130+.20,FL130+CPZ130-.20,M130['PewFrame'])
 for ps,pc in cp['posts']:post130(ps,pc,FL130)
# ---- closed pews (e) and open benches (f), both sides of the aisle
PZ130=1.05
def pewend130(s0,s1,c,sg):
 # The panelled end of a closed pew at the aisle, with its door: frame, two panels, a hinge strip.
 bx130(m,s0,s1,c-sg*.05,c,FL130,FL130+PZ130,M130['PewGrey'])
 for z0,z1 in ((FL130+.12,FL130+.48),(FL130+.56,FL130+PZ130-.10)):
  for a0,a1,b0,b1 in ((s0+.08,s1-.08,z0,z0+.035),(s0+.08,s1-.08,z1-.035,z1),(s0+.08,s0+.115,z0,z1),(s1-.115,s1-.08,z0,z1)):bx130(m,a0,a1,c,c+sg*.012,b0,b1,M130['PewFrame'])
 bx130(m,s0-.01,s1+.01,c-sg*.07,c+sg*.02,FL130+PZ130,FL130+PZ130+.05,M130['PewRail'])
cl=B130D['pews']['closed'];op=B130D['pews']['open'];ORG130=B130D['organ']
for (c_a,c_w,sg) in ((PW130['top_c'][1],PW130['top_c'][0],1),(PW130['bottom_c'][0],PW130['bottom_c'][1],-1)):
 # sg: +1 for the outer block (c increases from the aisle to the wall), -1 for the courtyard block
 lo,hi=min(c_a,c_w),max(c_a,c_w)
 for s in cl:bx130(m,s-.025,s+.025,lo,hi,FL130,FL130+PZ130,M130['PewGrey']);bx130(m,s-.045,s+.045,lo,hi,FL130+PZ130,FL130+PZ130+.045,M130['PewRail'])
 for s_hi,s_lo in zip(cl,cl[1:]):
  pewend130(s_lo+.025,s_hi-.025,c_a,-sg)
  bx130(m,s_lo+.025,s_lo+.44,lo,hi,FL130+.42,FL130+.465,M130['PewGrey'])
  bx130(m,s_hi-.22,s_hi-.025,lo,hi,FL130+.84,FL130+.86,M130['PewGrey'])
  if sg==1:bx130(m,s_lo+.025,s_hi-.025,c_w,c_w-.04,FL130,FL130+PZ130,M130['PewGrey'])
 for s_hi,s_lo in zip(op,op[1:]):
  if sg==1 and s_lo<ORG130['s']+ORG130['d']+.35:continue      # the organ now stands where the westernmost benches were
  a=s_lo+.03
  bx130(m,a,a+.42,lo,hi,FL130+.42,FL130+.47,M130['Oak']);bx130(m,a,a+.04,lo,hi,FL130+.50,FL130+.92,M130['Oak'])
  for cc in (lo+.02,hi-.02):bx130(m,a-.01,a+.50,cc-.02,cc+.02,FL130,FL130+.95,M130['Oak'])
  for cc in ((lo+hi)/2,):bx130(m,a+.30,a+.36,cc-.03,cc+.03,FL130,FL130+.42,M130['Oak'])
# ---- the organ at the west end, outer side of the door (photographs, 2015)
o_s=ORG130['s'];o_c0,o_c1=ORG130['c0'],ORG130['c1'];o_d=ORG130['d'];oc=(o_c0+o_c1)/2;ow=o_c1-o_c0
bx130(m,o_s,o_s+o_d,o_c0,o_c1,FL130,FL130+1.05,M130['OrganWood'])
bx130(m,o_s+o_d,o_s+o_d+.30,oc-.55,oc+.55,FL130+.70,FL130+.76,M130['OrganWood']);bx130(m,o_s+o_d+.05,o_s+o_d+.25,oc-.50,oc+.50,FL130+.76,FL130+.80,M130['Rosette'])
bx130(m,o_s+o_d+.55,o_s+o_d+.85,oc-.45,oc+.45,FL130+.48,FL130+.52,M130['OrganWood'])
for cc in (oc-.40,oc+.40):bx130(m,o_s+o_d+.58,o_s+o_d+.82,cc-.03,cc+.03,FL130,FL130+.48,M130['OrganWood'])
fields=[(o_c0,o_c0+ow*.32,ORG130['h']-.45),(o_c0+ow*.34,o_c1-ow*.34,ORG130['h']),(o_c1-ow*.32,o_c1,ORG130['h']-.45)]
for a0,a1,top in fields:
 bx130(m,o_s,o_s+o_d-.15,a0,a1,FL130+1.05,FL130+top,M130['OrganCase'])
 bx130(m,o_s+o_d-.20,o_s+o_d-.10,a0,a1,FL130+top-.12,FL130+top,M130['OrganCase'])
 bx130(m,o_s+o_d-.20,o_s+o_d-.10,a0,a0+.06,FL130+1.05,FL130+top,M130['OrganCase']);bx130(m,o_s+o_d-.20,o_s+o_d-.10,a1-.06,a1,FL130+1.05,FL130+top,M130['OrganCase'])
 npip=max(3,int((a1-a0-.14)/.085));mid=(npip-1)/2
 for k in range(npip):
  cc=a0+.07+(a1-a0-.14)*(k+.5)/npip;L=(top-1.45)*(1-.35*abs(k-mid)/max(mid,1))
  x,y,_=P130(o_s+o_d-.16,cc);m.cylinder(x,y,FL130+1.18,.034,L,M130['Pipe'],10)
  lathe130(m,o_s+o_d-.16,cc,FL130+1.05,[(.006,0),(.034,.13)],M130['Pipe'],10)
# ---- chandeliers: crystal, two tiers of arms, hanging from the crown
for sc_ in B130D['chandeliers']:
 cc=CC130;zc=FL130+3.55;x,y,_=P130(sc_,cc)
 m.box((x,y,(zc+.95+CR130)/2),(.012,.012,CR130-(zc+.95)),M130['Brass'],ANG130)
 lathe130(m,sc_,cc,zc-.55,[(.0,0),(.05,.08),(.09,.22),(.06,.36),(.10,.50),(.14,.62),(.09,.74),(.05,.84),(.08,.98),(.05,1.14),(.03,1.30),(.012,1.50)],M130['Crystal'],12)
 for tier,(rr,zz,na) in enumerate(((.52,zc+.05,8),(.32,zc+.55,6))):
  for k in range(na):
   a=2*math.pi*(k+.5*tier)/na;dx,dy=math.cos(a),math.sin(a)
   m.box((x+dx*rr/2,y+dy*rr/2,zz),(rr,.018,.018),M130['Crystal'],a)
   m.box((x+dx*rr*.75,y+dy*rr*.75,zz-.07),(.02,.02,.14),M130['Crystal'],a)
   m.lathe(x+dx*rr,y+dy*rr,zz,[(.0,0),(.045,.03),(.04,.06)],M130['Brass'],8)
   m.cylinder(x+dx*rr,y+dy*rr,zz+.06,.012,.16,M130['Candle'],6)
   m.lathe(x+dx*rr*.55,y+dy*rr*.55,zz-.24,[(.0,0),(.025,.05),(.0,.14)],M130['Crystal'],6)
b130_finish(m,bevel=False)

# ================================================================= cameras
def sv_camera130(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
CAM130_SPECS=[
 # name, s, c, height over the floor, look direction (ds, dc), pitch, vertical fov
 ('705_Block130_Cal_Nave2017',12.80,-4.80,1.91,1,0,12.0,49.4),
 ('706_Block130_Cal_Altar2017',17.60,-4.80,2.45,1,-.03,4.0,58),
 ('707_Block130_Cal_Pulpit2015',26.60,-3.40,1.75,-.25,-1,9.0,62),
 ('708_Block130_WestEnd',23.00,-7.00,2.00,-1,.12,6.0,64),
]
def cam130(name,s,c,dz,ds,dc,pitch,vfov):
 x,y,_=P130(s,c);vx,vy=U130[0]*ds+N130[0]*dc,U130[1]*ds+N130[1]*dc
 return sv_camera130(name,x,y,FL130+dz,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
block130_cameras=[cam130(*a) for a in CAM130_SPECS]+[('709_Block130_Aerial_SouthRange',P130(-6,55,70),P130(17,-6,16),24)]
print('BLOCK130_GEOMETRY',len(block130_names))
