"""Pass 143: Rutsalen and Drottningsalen, two state-floor rooms of Kalmar slott in the queen's apartment
(Drottningvåningen) of the north range (pass 27's 'NE' range).
- SM_Castle143_Rutsalen: Rutsalen (Olsson's room 63; Möller 1882: 'Profil genom s.k. "Rut-salen"'), the
  room shell: a two-tone square parquet ('Parkettgolf', Möller), a flat whitewashed board ceiling with a
  moulded cornice (Möller: underside 6.28 m over the floor), three courtyard window niches reaching the
  floor with sloping flat heads (Möller), each on its facade window with its own glazing, the deep
  niche in the spine wall with a closed door at its back into the (unbuilt) outer rooms (Möller), the
  open door to Drottningsalen through the 0.45 m partition (Olsson's text), a closed door to Grå salen
  (61b) in the west wall.
- SM_Castle143_RutsalenPaneler: the intarsia panelling ('det rika boiseriet', Möller) to 3.04 m round the
  room: plinth, panelled pedestal course, paired fluted columns on pedestals with a narrow inlaid field
  between them, wide fields with an octagonal inlaid picture and an arabesque frieze panel, an
  entablature with triglyph blocks and a cornice (photographs, early 20th century; view only).
- SM_Castle143_Drottningsalen: Drottningsalen (Olsson's room 65), the room shell: wide boards on the floor
  and the ceiling, three round-arched courtyard niches one step up on the facade windows, two round-arched
  niches in the spine wall (one with a closed door at its back, one with a bench), a closed door in the
  east wall towards Drottningtrappan (66), the cornice.
- SM_Castle143_DrottningDekor: the stone fireplace in the spine wall (KMB 1922: scroll consoles, triglyph
  lintel, shelf, overmantel with an oval cartouche), its painted pediment and pinnacles, the painted
  pedimented surrounds of the two doors (trompe-l'oeil), the painted draped dado and the painted scroll
  frieze under the ceiling (photographs 1922/1933, PDM), as flat colours.
The rooms are closed solids inside pass 27's hollow range; no existing mesh is changed. Positions and
footprints come from scripts/prepare_block143.py (source/block143.json). See references/block143-notes.md.
"""
from mathutils import Vector
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B143D=json.loads((R/'source/block143.json').read_text())
block143_names=[];B143={}
for old in [k for k in list(materials) if k.startswith('M_Block143_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownPaintWhite',(.90,.88,.83),.93,0),('Reveal','TownPaintWhite',(.94,.93,.89),.92,0),('PlasterD','TownPaintWhite',(.91,.90,.86),.93,0),
 ('Ceil','TownPaintWhite',(.92,.91,.88),.90,0),('CeilBoard','TownPaintBrown',(.50,.44,.37),.85,0),('CeilBoard2','TownPaintBrown',(.45,.39,.33),.85,0),
 ('Parq1','TownPaintBrown',(.62,.47,.32),.70,0),('Parq2','TownPaintBrown',(.44,.31,.20),.70,0),('Boards','TownPaintBrown',(.70,.63,.52),.80,0),
 ('Boards2','TownPaintBrown',(.65,.58,.48),.80,0),('Joint','TownStone',(.30,.29,.28),.90,0),('Stone','TownStone',(.76,.73,.67),.85,0),
 ('Stone2','TownStone',(.68,.65,.60),.85,0),('PanelDark','TownPaintBrown',(.30,.21,.14),.62,0),('PanelMid','TownPaintBrown',(.47,.34,.22),.62,0),
 ('Intarsia','TownIvory',(.78,.68,.50),.60,0),('Intarsia2','TownPaintBrown',(.62,.50,.34),.62,0),('Column','TownPaintBrown',(.40,.29,.19),.55,0),
 ('WinFrame','TownPaintWhite',(.80,.78,.72),.60,0),('Daylight','TownPaintWhite',(.84,.90,.93),.20,0),('Door','TownPaintBrown',(.36,.27,.19),.70,0),
 ('Soot','TownPaintBrown',(.12,.10,.09),.90,0),('Iron','TownMetalGrey',(.20,.20,.20),.55,.5),('Drape','TownPaintWhite',(.84,.84,.82),.90,0),
 ('DrapeLine','TownPaintWhite',(.62,.64,.66),.90,0),('Frieze','TownPaintWhite',(.70,.70,.68),.90,0),('FriezeLine','TownPaintWhite',(.40,.40,.40),.90,0),
 ('PaintGrey','TownPaintWhite',(.74,.73,.70),.90,0),('Coffer','TownPaintWhite',(.58,.58,.57),.90,0),
 ]:
 name='M_Block143_'+key;B143[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block143_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M143=B143

def b143_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block143_names.append(name);return Mesh(name,category)
def drop_degenerate_faces143(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b143_finish(m,bevel=True):
 # The shells get the town's small edge bevel (s21_finish). Panelling and painted work are small parts
 # on which that bevel only makes collapsed slivers (passes 130/131): world-scale UVs without it.
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
 obj['block143_dropped_faces']=drop_degenerate_faces143(obj)
 print('BLOCK143_FACES',m.name,'authored',nf,'finished',len(obj.data.polygons),'dropped',obj['block143_dropped_faces'])
 obj['detail_pass']=143;obj['reference_notes']='references/block143-notes.md';obj['osm_way']='';return obj

# ---------------------------------------------------------------- frame and generic solids
F143=B143D['frame'];O143,U143,N143=F143['origin'],F143['u'],F143['n']
LV143=B143D['levels'];FL143=LV143['floor'];Z0143=LV143['z0'];ZT143=LV143['ztop'];BU143=LV143['board_under']
WL143=B143D['walls'];BCB143,BCI143,BOI143,BOB143=WL143['bcb'],WL143['bci'],WL143['boi'],WL143['bob']
def PF143(a,b,z=0.0):return (O143[0]+U143[0]*a+N143[0]*b,O143[1]+U143[1]*a+N143[1]*b,z)
def hexa143(m,a,b,ma):
 # Closed six-faced solid from two quads a and b, corners in matching order.
 m.faces(list(a)+list(b),[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
def setmat143(m,k,ma):
 if ma not in m.mats:m.mats.append(ma)
 m.mi[k]=m.mats.index(ma)
def bx143(m,a0,a1,b0,b1,z0,z1,ma):
 a0,a1=min(a0,a1),max(a0,a1);b0,b1=min(b0,b1),max(b0,b1);z0,z1=min(z0,z1),max(z0,z1)
 if a1-a0<.002 or b1-b0<.002 or z1-z0<.002:return
 hexa143(m,[PF143(a0,b0,z0),PF143(a1,b0,z0),PF143(a1,b1,z0),PF143(a0,b1,z0)],[PF143(a0,b0,z1),PF143(a1,b0,z1),PF143(a1,b1,z1),PF143(a0,b1,z1)],ma)
def lframe143(p,t,nrm):
 # A local frame at the point p on a wall face: a along the wall (t), d into the wall (nrm), z up.
 return lambda a,d,z:(p[0]+t[0]*a+nrm[0]*d,p[1]+t[1]*a+nrm[1]*d,z)
def lbox143(m,fr,a0,a1,d0,d1,z0,z1,ma):
 a0,a1=min(a0,a1),max(a0,a1);d0,d1=min(d0,d1),max(d0,d1);z0,z1=min(z0,z1),max(z0,z1)
 if a1-a0<.002 or d1-d0<.002 or z1-z0<.002:return
 hexa143(m,[fr(a0,d0,z0),fr(a1,d0,z0),fr(a1,d1,z0),fr(a0,d1,z0)],[fr(a0,d0,z1),fr(a1,d0,z1),fr(a1,d1,z1),fr(a0,d1,z1)],ma)
def fan143(m,pts,d0,d1,fr,ma,center=None):
 # A flat convex shape of (a,z) outline points in a vertical plane, extruded across d0..d1, as a
 # triangle fan (no large n-gon).
 n=len(pts)
 if center is None:
  v=[fr(a,d,z) for d in (d0,d1) for a,z in pts]
  f=[(0,i,i+1) for i in range(1,n-1)]+[(n,n+i+1,n+i) for i in range(1,n-1)]
 else:
  v=[fr(a,d,z) for d in (d0,d1) for a,z in pts]+[fr(center[0],d0,center[1]),fr(center[0],d1,center[1])]
  f=[(2*n,i,(i+1)%n) for i in range(n)]+[(2*n+1,n+(i+1)%n,n+i) for i in range(n)]
 f+=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 m.faces(v,f,ma)
# the four wall faces of a room (a0..a1 x BCI..BOI): frames with d < 0 towards the room
def faces143(a0,a1):
 U,N=U143,N143;mU=(-U[0],-U[1]);mN=(-N[0],-N[1])
 return dict(court=(lframe143(PF143(a0,BCI143),U,mN),a1-a0),spine=(lframe143(PF143(a1,BOI143),mU,N),a1-a0),
  east=(lframe143(PF143(a0,BOI143),mN,mU),BOI143-BCI143),west=(lframe143(PF143(a1,BCI143),N,U),BOI143-BCI143))
def leaf143(m,fr,w,h,z,d):
 # A closed panelled door leaf in its opening at depth d of a frame (two fields, a handle).
 L=M143['Door'];lbox143(m,fr,-w/2,w/2,d-.025,d+.025,z,z+h,L)
 for k in range(2):
  z0_=z+.14+k*(h-.28)/2+(.05 if k else 0);z1_=z+.14+(k+1)*(h-.28)/2-(0 if k else .05)
  for a0,a1,b0,b1 in ((-w/2+.10,w/2-.10,z0_,z0_+.045),(-w/2+.10,w/2-.10,z1_-.045,z1_),(-w/2+.10,-w/2+.145,z0_,z1_),(w/2-.145,w/2-.10,z0_,z1_)):
   lbox143(m,fr,a0,a1,d-.045,d-.025,b0,b1,L)
 lbox143(m,fr,w/2-.24,w/2-.17,d-.05,d-.025,z+h*.47,z+h*.49,M143['Iron'])
def window143(m,fr,a0,a1,zb,zs,zh,ma_frame,bars=(1,2)):
 # Glazing in a vertical plane: a pane, a frame, mullions and transoms, small glazing bars, a head
 # board up to zh. fr(a,d,z): d < 0 towards the room.
 F=ma_frame;lbox143(m,fr,a0+.02,a1-.02,-.01,.01,zb+.04,zs,M143['Daylight'])
 for b0,b1 in ((a0,a0+.07),(a1-.07,a1)):lbox143(m,fr,b0,b1,-.07,.02,zb,zh,F)
 lbox143(m,fr,a0,a1,-.07,.02,zb,zb+.08,F);lbox143(m,fr,a0,a1,-.07,.02,zs-.04,zh,F)
 nm,nt=bars
 for k in range(1,nm+1):a=a0+(a1-a0)*k/(nm+1);lbox143(m,fr,a-.03,a+.03,-.06,.015,zb+.08,zs,F)
 for k in range(1,nt+1):z=zb+.08+(zs-zb-.08)*k/(nt+1);lbox143(m,fr,a0+.07,a1-.07,-.06,.015,z-.03,z+.03,F)
 na=(nm+1)*2;nz=(nt+1)*3
 for k in range(1,na):
  if k%2==0:continue
  a=a0+(a1-a0)*k/na;lbox143(m,fr,a-.008,a+.008,-.03,.012,zb+.08,zs,F)
 for k in range(1,nz):
  if k%3==0:continue
  z=zb+.08+(zs-zb-.08)*k/nz;lbox143(m,fr,a0+.07,a1-.07,-.03,.012,z-.008,z+.008,F)

# ---------------------------------------------------------------- long walls with niches
CBT143=B143D['court_back_top']
def cbt143(a):
 # the courtyard wall's back follows the roof's underside less 0.10 m where that is lower than the ceiling's top
 for (a0,z0),(a1,z1) in zip(CBT143,CBT143[1:]):
  if a0<=a<=a1:return z0+(z1-z0)*(a-a0)/(a1-a0)
 return CBT143[0][1] if a<CBT143[0][0] else CBT143[-1][1]
def lwall143(m,b_in,b_out,zt_out,a0,a1,holes,ma,mr,K=16):
 # A long wall between b_in (room face) and b_out (back), from a0 to a1: piers, the slab under each
 # niche's floor, and the head over each niche: a flat sloping slab ('rect') or a fan of slabs over a
 # round arch ('arch'), up to the wall's top (ZT143 at the face, zt_out(a) at the back). Reveal faces in mr.
 z0,z1=Z0143,ZT143
 def Q(a_i,a_o,zb_i,zb_o,zt_i=None):
  return [PF143(a_i[0],b_in,zb_i[0]),PF143(a_i[1],b_in,zb_i[1]),PF143(a_i[1],b_in,z1 if zt_i is None else zt_i[1]),PF143(a_i[0],b_in,z1 if zt_i is None else zt_i[0])],\
         [PF143(a_o[0],b_out,zb_o[0]),PF143(a_o[1],b_out,zb_o[1]),PF143(a_o[1],b_out,zt_out(a_o[1])),PF143(a_o[0],b_out,zt_out(a_o[0]))]
 at_i=at_o=a0
 for h in sorted(holes,key=lambda h:h['u_in'])+[None]:
  li,lo_=(h['u_in']-h['r_in'],h['u_out']-h['r_out']) if h else (a1,a1)
  if li-at_i>.002:
   qa,qb=Q((at_i,li),(at_o,lo_),(z0,z0),(z0,z0));hexa143(m,qa,qb,ma)
   if h is not None:setmat143(m,len(m.f)-3,mr)
   if at_i>a0+1e-6:setmat143(m,len(m.f)-1,mr)
  if h is None:break
  ri,ro=h['u_in']+h['r_in'],h['u_out']+h['r_out'];zb=h['zb']
  hexa143(m,[PF143(li,b_in,z0),PF143(ri,b_in,z0),PF143(ri,b_in,zb),PF143(li,b_in,zb)],[PF143(lo_,b_out,z0),PF143(ro,b_out,z0),PF143(ro,b_out,zb),PF143(lo_,b_out,zb)],ma)
  setmat143(m,len(m.f)-2,mr)
  if h['kind']=='rect':
   zi,zo=h['head']['z_in'],h['head']['z_out']
   qa,qb=Q((li,ri),(lo_,ro),(zi,zi),(zo,zo));hexa143(m,qa,qb,ma);setmat143(m,len(m.f)-4,mr)
  else:
   zsi,zso=h['head']['zs_in'],h['head']['zs_out']
   def A(th,inner):
    return (h['u_in']+h['r_in']*math.cos(th),zsi+h['r_in']*math.sin(th)) if inner else (h['u_out']+h['r_out']*math.cos(th),zso+h['r_out']*math.sin(th))
   for j in range(K):
    t0,t1=math.pi*j/K,math.pi*(j+1)/K;(e0,f0),(e1,f1)=A(t0,True),A(t1,True);(g0,k0),(g1,k1)=A(t0,False),A(t1,False)
    hexa143(m,[PF143(e1,b_in,f1),PF143(e0,b_in,f0),PF143(e0,b_in,z1),PF143(e1,b_in,z1)],[PF143(g1,b_out,k1),PF143(g0,b_out,k0),PF143(g0,b_out,zt_out(g0)),PF143(g1,b_out,zt_out(g1))],ma)
    setmat143(m,len(m.f)-4,mr)
  at_i,at_o=ri,ro
def plug143(m,h,b0,b1,ma):
 # The back of a spine-wall niche: a solid from b0 to b1 that fills the niche's outline, with a door
 # opening if the niche has one.
 u,r,zb=h['u_in'],h['r_in'],h['zb'];d=h.get('door')
 if h['kind']=='rect':ztop=h['head']['z_out']
 else:ztop=h['head']['zs_in']
 if d:
  w2=d['w']/2;zd=zb+d['h']
  bx143(m,u-r,u-w2,b0,b1,zb,ztop,ma);bx143(m,u+w2,u+r,b0,b1,zb,ztop,ma);bx143(m,u-w2,u+w2,b0,b1,zd,ztop,ma)
 else:bx143(m,u-r,u+r,b0,b1,zb,ztop,ma)
 if h['kind']=='arch':
  zs=h['head']['zs_in'];fr=lambda a,dd,z:PF143(a,b0+dd,z)
  # a fan from the springing point (a centre on the chord would make zero-area triangles, which stop the bevel)
  fan143(m,[(u+r*math.cos(math.pi*k/16),zs+r*math.sin(math.pi*k/16)) for k in range(17)],0,b1-b0,fr,ma)
def endwall143(m,a_in,a_out,door,ma):
 # An end wall across the room (BCI..BOI) from Z0 to the top, with a door opening (or none).
 bx143(m,a_in,a_out,BCI143,BOI143,Z0143,FL143,ma)
 if door:
  b,w=door['b'],door['w'];zh=FL143+door['h']
  bx143(m,a_in,a_out,BCI143,b-w/2,FL143,zh,ma);bx143(m,a_in,a_out,b+w/2,BOI143,FL143,zh,ma);bx143(m,a_in,a_out,BCI143,BOI143,zh,ZT143,ma)
  bx143(m,a_in,a_out,b-w/2,b+w/2,FL143-.01,FL143+.012,M143['Stone'])
 else:bx143(m,a_in,a_out,BCI143,BOI143,FL143,ZT143,ma)
def court_window143(m,n,parapet_mat):
 # the parapet (the last 0.55 m of the niche, up to the facade's sill) and the window at the niche's back
 r=n['r_out'];u=n['u_out'];cb=BCB143;sill=LV143['sill'];zg=LV143['glass_top']
 bx143(m,u-r,u+r,cb+.012,cb+.60,n['zb'],sill,parapet_mat)
 fr=(lambda a,d,z:PF143(a,cb+.04-d,z))
 if n['kind']=='rect':
  window143(m,fr,u-r+.01,u+r-.01,sill,zg,n['head']['z_out']-.005,M143['WinFrame'],bars=(1,3))
 else:
  window143(m,fr,u-.60,u+.60,sill,zg,zg+.05,M143['WinFrame'],bars=(1,3))
  zh=zg+.05;zs=n['head']['zs_out'];rr=r-.02;th0=math.asin(min(1,(zh-zs)/rr))
  pts=[(u+rr*math.cos(th0+(math.pi-2*th0)*k/12),zs+rr*math.sin(th0+(math.pi-2*th0)*k/12)) for k in range(13)]
  fan143(m,pts,-.01,.01,fr,M143['Daylight'])
  lbox143(m,fr,u-.03,u+.03,-.06,.015,zh,zs+rr-.03,M143['WinFrame'])

NI143=B143D['niches'];DO143={d['name']:d for d in B143D['doors']}
RUT143=B143D['rut'];DRO143=B143D['dro']

# ================================================================= Rutsalen
A0R143,A1R143=RUT143['a'];E0R143,E1R143=RUT143['env'];PA143=RUT143['part']
m=b143_new('SM_Castle143_Rutsalen','Kalmar slott/Interiör')
hr143=[n for n in NI143 if n['room']=='rut']
lwall143(m,BCI143,BCB143,cbt143,E0R143,E1R143,[n for n in hr143 if n['wall']=='court'],M143['Plaster'],M143['Reveal'])
lwall143(m,BOI143,BOB143,lambda a:ZT143,E0R143,E1R143,[n for n in hr143 if n['wall']=='spine'],M143['Plaster'],M143['Reveal'])
endwall143(m,PA143[0],PA143[1],DO143['rut_dro'],M143['Plaster'])
endwall143(m,A1R143,E1R143,DO143['rut_west'],M143['Plaster'])
for n in hr143:
 if n['wall']=='court':court_window143(m,n,M143['PanelMid'])
 else:
  plug143(m,n,BOI143+n['depth'],BOB143,M143['Plaster'])
  if n.get('door'):
   fr=lframe143(PF143(n['u_in'],BOI143+n['depth']),U143,N143)
   leaf143(m,fr,n['door']['w'],n['door']['h'],n['zb'],.15)
# west door: closed leaf in the middle of the wall's thickness, threshold
dw143=DO143['rut_west'];frw143=lframe143(PF143((A1R143+E1R143)/2,dw143['b']),N143,U143)
leaf143(m,frw143,dw143['w'],dw143['h'],FL143,0)
# floor: bedding and a two-tone square parquet ('Parkettgolf', Möller 1882; the pattern is estimated)
bx143(m,A0R143,A1R143,BCI143,BOI143,Z0143,FL143-.015,M143['Joint'])
SQ143=.60;na143=round((A1R143-A0R143)/SQ143);nb143=round((BOI143-BCI143)/SQ143)
for i in range(na143):
 for j in range(nb143):
  a0=A0R143+(A1R143-A0R143)*i/na143;a1=A0R143+(A1R143-A0R143)*(i+1)/na143;b0=BCI143+(BOI143-BCI143)*j/nb143;b1=BCI143+(BOI143-BCI143)*(j+1)/nb143
  bx143(m,a0+.002,a1-.002,b0+.002,b1-.002,FL143-.015,FL143,M143['Parq1' if (i+j)%2 else 'Parq2'])
# ceiling: whitewashed boards ('hvitlimmad underpanel'), a moulded cornice round the room
bx143(m,A0R143,A1R143,BCI143,BOI143,BU143,ZT143,M143['Ceil'])
zc143=LV143['cornice']
for a0,a1,b0,b1 in ((A0R143,A1R143,BCI143,BCI143+.18),(A0R143,A1R143,BOI143-.18,BOI143),(A0R143,A0R143+.18,BCI143,BOI143),(A1R143-.18,A1R143,BCI143,BOI143)):
 bx143(m,a0,a1,b0,b1,zc143+.08,BU143,M143['Plaster'])
for a0,a1,b0,b1 in ((A0R143,A1R143,BCI143,BCI143+.10),(A0R143,A1R143,BOI143-.10,BOI143),(A0R143,A0R143+.10,BCI143,BOI143),(A1R143-.10,A1R143,BCI143,BOI143)):
 bx143(m,a0,a1,b0,b1,zc143,zc143+.08,M143['Plaster'])
b143_finish(m)

# ---------------------------------------------------------------- Rutsalen's panelling
m=b143_new('SM_Castle143_RutsalenPaneler','Kalmar slott/Interiör')
def panel143(m,fr,t0,t1,zf):
 # Panelling to 3.04 m between t0 and t1 along a wall face (d < 0 towards the room).
 L=t1-t0
 if L<.25:return
 D,Mi,I1,I2,C=M143['PanelDark'],M143['PanelMid'],M143['Intarsia'],M143['Intarsia2'],M143['Column']
 lbox143(m,fr,t0,t1,-.04,0,zf,zf+3.04,Mi)
 lbox143(m,fr,t0,t1,-.12,-.04,zf,zf+.12,D);lbox143(m,fr,t0,t1,-.10,-.04,zf+.12,zf+.78,D);lbox143(m,fr,t0,t1,-.16,-.04,zf+.78,zf+.86,D)
 lbox143(m,fr,t0,t1,-.14,-.04,zf+2.62,zf+2.74,D);lbox143(m,fr,t0,t1,-.12,-.04,zf+2.74,zf+2.90,Mi);lbox143(m,fr,t0,t1,-.28,-.04,zf+2.90,zf+3.04,D)
 def field(x0,x1,octagon=True):
  if x1-x0<.3:return
  lbox143(m,fr,x0+.04,x1-.04,-.07,-.04,zf+.20,zf+.70,Mi)                      # pedestal field
  lbox143(m,fr,x0+.03,x1-.03,-.075,-.04,zf+.94,zf+1.10,I2)                     # base panel
  lbox143(m,fr,x0+.03,x1-.03,-.075,-.04,zf+2.18,zf+2.52,I2)                    # arabesque frieze panel
  lbox143(m,fr,x0+.10,x1-.10,-.08,-.075,zf+2.24,zf+2.46,I1)
  lbox143(m,fr,x0+.03,x1-.03,-.065,-.04,zf+1.16,zf+2.12,D)                     # the picture field
  if octagon:
   rr=min((x1-x0)*.42,.46);cx=(x0+x1)/2;cz=zf+1.64
   fan143(m,[(cx+rr*math.cos(math.pi/8+k*math.pi/4),cz+rr*math.sin(math.pi/8+k*math.pi/4)) for k in range(8)],-.075,-.065,fr,I1,(cx,cz))
   # the inlaid picture: a building under a gable (the photographs show architecture, e.g. Kalmar cathedral)
   fan143(m,[(cx-.3*rr,cz-.4*rr),(cx+.3*rr,cz-.4*rr),(cx+.3*rr,cz+.05*rr),(cx,cz+.35*rr),(cx-.3*rr,cz+.05*rr)],-.08,-.075,fr,I2)
 def column(xc):
  lbox143(m,fr,xc-.13,xc+.13,-.30,-.04,zf+.12,zf+.86,D);lbox143(m,fr,xc-.13,xc+.13,-.30,-.04,zf+2.62,zf+2.90,D)
  lbox143(m,fr,xc-.15,xc+.15,-.34,-.04,zf+2.90,zf+3.04,D)
  for k in range(3):lbox143(m,fr,xc-.09+k*.06,xc-.06+k*.06,-.155,-.12,zf+2.76,zf+2.89,D)
  x,y,_=fr(xc,-.17,0)
  m.lathe(x,y,zf+.86,[(.115,0),(.115,.05),(.09,.09),(.085,.14),(.075,1.62),(.10,1.66),(.12,1.72),(.12,1.76)],C,10)
 if L<2.2:
  field(t0,t1,L>.9);return
 n=max(1,round((L-.8)/2.4))
 while n>1 and (L-(n+1)*.8)/n<.9:n-=1
 W=(L-(n+1)*.8)/n
 for k in range(n+1):
  x=t0+k*(.8+W);column(x+.13);column(x+.67)
  lbox143(m,fr,x+.26,x+.54,-.075,-.04,zf+1.10,zf+2.30,I2);lbox143(m,fr,x+.30,x+.50,-.08,-.075,zf+1.25,zf+2.15,I1)   # the narrow inlaid field
  if k<n:field(x+.8,x+.8+W)
FC143=faces143(A0R143,A1R143)
def gaps143(L,spans):
 # the parts of 0..L not covered by the opening spans
 out=[];at=0.0
 for s0,s1 in sorted(spans):
  if s0>at:out.append((at,s0))
  at=max(at,s1)
 if at<L:out.append((at,L))
 return out
fr,L=FC143['court'];panel_spans=[(n['u_in']-n['r_in']-A0R143,n['u_in']+n['r_in']-A0R143) for n in hr143 if n['wall']=='court']
for t0,t1 in gaps143(L,panel_spans):panel143(m,fr,t0,t1,FL143)
fr,L=FC143['spine'];panel_spans=[(A1R143-(n['u_in']+n['r_in']),A1R143-(n['u_in']-n['r_in'])) for n in hr143 if n['wall']=='spine']
for t0,t1 in gaps143(L,panel_spans):panel143(m,fr,t0,t1,FL143)
d=DO143['rut_dro'];fr,L=FC143['east'];bpos=BOI143-d['b']
for t0,t1 in gaps143(L,[(bpos-d['w']/2-.10,bpos+d['w']/2+.10)]):panel143(m,fr,t0,t1,FL143)
lbox143(m,fr,bpos-d['w']/2-.10,bpos-d['w']/2,-.08,0,FL143,FL143+d['h']+.10,M143['PanelDark']);lbox143(m,fr,bpos+d['w']/2,bpos+d['w']/2+.10,-.08,0,FL143,FL143+d['h']+.10,M143['PanelDark'])
lbox143(m,fr,bpos-d['w']/2-.10,bpos+d['w']/2+.10,-.08,0,FL143+d['h'],FL143+d['h']+.10,M143['PanelDark'])
d=DO143['rut_west'];fr,L=FC143['west'];bpos=d['b']-BCI143
for t0,t1 in gaps143(L,[(bpos-d['w']/2-.10,bpos+d['w']/2+.10)]):panel143(m,fr,t0,t1,FL143)
for a0,a1,z0,z1 in ((bpos-d['w']/2-.10,bpos-d['w']/2,FL143,FL143+d['h']+.10),(bpos+d['w']/2,bpos+d['w']/2+.10,FL143,FL143+d['h']+.10),(bpos-d['w']/2-.10,bpos+d['w']/2+.10,FL143+d['h'],FL143+d['h']+.10)):
 lbox143(m,fr,a0,a1,-.08,0,z0,z1,M143['PanelDark'])
b143_finish(m,bevel=False)

# ================================================================= Drottningsalen
A0D143,A1D143=DRO143['a'];E0D143,E1D143=DRO143['env']
m=b143_new('SM_Castle143_Drottningsalen','Kalmar slott/Interiör')
hd143=[n for n in NI143 if n['room']=='dro']
lwall143(m,BCI143,BCB143,cbt143,E0D143,E1D143,[n for n in hd143 if n['wall']=='court'],M143['PlasterD'],M143['Reveal'])
lwall143(m,BOI143,BOB143,lambda a:ZT143,E0D143,E1D143,[n for n in hd143 if n['wall']=='spine'],M143['PlasterD'],M143['Reveal'])
endwall143(m,E0D143,A0D143,DO143['dro_east'],M143['PlasterD'])
for n in hd143:
 if n['wall']=='court':court_window143(m,n,M143['Reveal'])
 else:
  plug143(m,n,BOI143+n['depth'],BOB143,M143['PlasterD'])
  fr=lframe143(PF143(n['u_in'],BOI143+n['depth']),U143,N143)
  if n.get('door'):leaf143(m,fr,n['door']['w'],n['door']['h'],n['zb'],.15)
  if n.get('bench'):lbox143(m,fr,-n['r_in']+.02,n['r_in']-.02,-n['bench']['d'],0,n['zb'],n['zb']+n['bench']['h'],M143['Reveal'])
de143=DO143['dro_east'];leaf143(m,lframe143(PF143((E0D143+A0D143)/2,de143['b']),N143,U143),de143['w'],de143['h'],FL143,0)
# floor: bedding and wide boards across the room (photograph 1922)
bx143(m,A0D143,A1D143,BCI143,BOI143,Z0143,FL143-.015,M143['Joint'])
nb143=round((A1D143-A0D143)/.30)
for j in range(nb143):
 a0=A0D143+(A1D143-A0D143)*j/nb143;a1=A0D143+(A1D143-A0D143)*(j+1)/nb143
 bx143(m,a0+.003,a1-.003,BCI143,BOI143,FL143-.015,FL143,M143['Boards2' if j%2 else 'Boards'])
# ceiling: boards across the room (photograph 1933), a small cornice
bx143(m,A0D143,A1D143,BCI143,BOI143,BU143,ZT143,M143['CeilBoard'])
for j in range(round((A1D143-A0D143)/.28)):
 nj=round((A1D143-A0D143)/.28);a0=A0D143+(A1D143-A0D143)*j/nj;a1=A0D143+(A1D143-A0D143)*(j+1)/nj
 bx143(m,a0+.003,a1-.003,BCI143+.10,BOI143-.10,BU143-.02,BU143,M143['CeilBoard2' if j%2 else 'CeilBoard'])
for a0,a1,b0,b1 in ((A0D143,A1D143,BCI143,BCI143+.10),(A0D143,A1D143,BOI143-.10,BOI143),(A0D143,A0D143+.10,BCI143,BOI143),(A1D143-.10,A1D143,BCI143,BOI143)):
 bx143(m,a0,a1,b0,b1,BU143-.10,BU143,M143['PlasterD'])
b143_finish(m)

# ---------------------------------------------------------------- Drottningsalen's painted work and fireplace
m=b143_new('SM_Castle143_DrottningDekor','Kalmar slott/Interiör')
FD143=faces143(A0D143,A1D143)
FI143=B143D['fire']
def spans_d143(face):
 # opening spans on a face of Drottningsalen (in the face's own t, from its start)
 if face=='court':return [(n['u_in']-n['r_in']-A0D143,n['u_in']+n['r_in']-A0D143) for n in hd143 if n['wall']=='court']
 if face=='spine':return [(A1D143-(n['u_in']+n['r_in']),A1D143-(n['u_in']-n['r_in'])) for n in hd143 if n['wall']=='spine']+[(A1D143-FI143['a']-FI143['w']/2-.05,A1D143-FI143['a']+FI143['w']/2+.05)]
 if face=='east':d=DO143['dro_east'];b=BOI143-d['b'];return [(b-d['w']/2-.25,b+d['w']/2+.25)]
 d=DO143['rut_dro'];b=d['b']-BCI143;return [(b-d['w']/2-.25,b+d['w']/2+.25)]
ZD143=FL143+1.28;ZF0143=BU143-.80;ZF1143=BU143-.10
for face,(fr,L) in FD143.items():
 # the painted draped dado (photographs 1922/1933): a pale band with darker folds and a top line
 for t0,t1 in gaps143(L,spans_d143(face)):
  if t1-t0<.05:continue
  lbox143(m,fr,t0,t1,-.004,0,FL143+.02,ZD143,M143['Drape']);lbox143(m,fr,t0,t1,-.006,-.004,ZD143-.06,ZD143,M143['DrapeLine'])
  k=1
  while t0+k*.50<t1-.05:
   x=t0+k*.50;lbox143(m,fr,x-.012,x+.012,-.005,-.004,FL143+.05,ZD143-.18,M143['DrapeLine'])
   fan143(m,[(x-.25,ZD143-.06),(x+.25,ZD143-.06),(x,ZD143-.24)],-.005,-.004,fr,M143['DrapeLine']);k+=1
 # the painted scroll frieze under the cornice (1933; detail 021017081519)
 lbox143(m,fr,0,L,-.004,0,ZF0143,ZF1143,M143['Frieze'])
 lbox143(m,fr,0,L,-.006,-.004,ZF0143,ZF0143+.04,M143['FriezeLine']);lbox143(m,fr,0,L,-.006,-.004,ZF1143-.04,ZF1143,M143['FriezeLine'])
 k=0
 while .30+k*.60<L-.30:
  x=.30+k*.60;cz=(ZF0143+ZF1143)/2
  fan143(m,[(x+.20*math.cos(math.pi*q/6),cz+.20*math.sin(math.pi*q/6)) for q in range(12)],-.005,-.004,fr,M143['FriezeLine'],(x,cz));k+=1
def painted_door143(m,fr,c,w,h):
 # a painted pedimented surround with three pinnacles (trompe-l'oeil; photographs 021016468882, 021017088983)
 G=M143['PaintGrey'];zf=FL143;d0,d1=-.008,-.004
 for a0,a1 in ((c-w/2-.22,c-w/2-.02),(c+w/2+.02,c+w/2+.22)):lbox143(m,fr,a0,a1,d0,d1,zf,zf+h+.05,G)
 lbox143(m,fr,c-w/2-.30,c+w/2+.30,d0,d1,zf+h+.05,zf+h+.30,G)
 fan143(m,[(c-w/2-.32,zf+h+.30),(c+w/2+.32,zf+h+.30),(c,zf+h+.92)],d0,d1,fr,G)
 for a,zb,ht in ((c-w/2-.22,zf+h+.30,.85),(c+w/2+.22,zf+h+.30,.85),(c,zf+h+.92,.55)):
  fan143(m,[(a-.07,zb),(a+.07,zb),(a+.02,zb+ht),(a,zb+ht+.06),(a-.02,zb+ht)],d0-.002,d1,fr,M143['FriezeLine'])
fr,L=FD143['east'];d=DO143['dro_east'];painted_door143(m,fr,BOI143-d['b'],d['w'],d['h'])
fr,L=FD143['west'];d=DO143['rut_dro'];painted_door143(m,fr,d['b']-BCI143,d['w'],d['h'])
# the fireplace (KMB 1922 'Spiseln med rest av överstycke i kalkmålning'): plinths, scroll consoles with
# fluted fronts, a triglyph lintel, a shelf, an overmantel with an oval cartouche, a top cornice; the
# pediment and pinnacles above are lime painting (1933)
frf=lframe143(PF143(FI143['a'],BOI143),U143,N143);S,S2,zf=M143['Stone'],M143['Stone2'],FL143
ow=FI143['open_w']/2;W2=FI143['w']/2;pj=FI143['proj']
lbox143(m,frf,-W2-.05,W2+.05,-pj-.20,0,zf,zf+.04,S)
lbox143(m,frf,-ow,ow,-.02,0,zf+.04,zf+FI143['open_h'],M143['Soot'])
for sg in (-1,1):
 a0,a1=sorted((sg*ow,sg*W2))
 lbox143(m,frf,a0,a1,-pj-.03,0,zf+.04,zf+.30,S);lbox143(m,frf,a0+.02,a1-.02,-pj,0,zf+.30,zf+1.12,S)
 lbox143(m,frf,a0,a1,-pj-.04,0,zf+1.12,zf+FI143['open_h'],S)
 for k in range(3):x=a0+.06+k*(a1-a0-.12)/2;lbox143(m,frf,x-.012,x+.012,-pj-.006,-pj,zf+.36,zf+1.06,M143['Joint'])
lbox143(m,frf,-ow,ow,-pj+.06,-.02,zf+FI143['open_h']-.02,zf+FI143['open_h'],M143['Soot'])
lbox143(m,frf,-W2,W2,-pj,0,zf+FI143['open_h'],zf+1.63,S)
for k in range(6):x=-W2+.15+k*(2*W2-.30)/5;lbox143(m,frf,x-.05,x+.05,-pj-.02,-pj,zf+1.40,zf+1.58,S2)
lbox143(m,frf,-W2-.07,W2+.07,-pj-.08,0,zf+1.63,zf+1.71,S)
lbox143(m,frf,-W2+.07,W2-.07,-.24,0,zf+1.71,zf+2.17,S)
fan143(m,[(.26*math.cos(math.pi*q/8),zf+1.94+.15*math.sin(math.pi*q/8)) for q in range(16)],-.27,-.24,frf,S2,(0,zf+1.94))
for sg in (-1,1):
 a0,a1=sorted((sg*.36,sg*(W2-.15)));lbox143(m,frf,a0,a1,-.255,-.24,zf+1.79,zf+2.09,S2)
lbox143(m,frf,-W2-.01,W2+.01,-.30,0,zf+2.17,zf+2.26,S)
fan143(m,[(-W2+.05,zf+2.26),(W2-.05,zf+2.26),(0,zf+2.95)],-.006,-.002,frf,M143['PaintGrey'])
for a,zb,ht in ((-W2+.12,zf+2.26,.85),(W2-.12,zf+2.26,.85),(0,zf+2.95,.70)):
 fan143(m,[(a-.08,zb),(a+.08,zb),(a+.02,zb+ht),(a,zb+ht+.07),(a-.02,zb+ht)],-.008,-.004,frf,M143['FriezeLine'])
# the painted coffers of the courtyard niches' vaults (detail 021017081516, 1922): grey squares on the soffit
for n in [n for n in hd143 if n['wall']=='court']:
 K=16;dep=BCI143-BCB143
 for j in range(2,K-2,2):
  t=math.pi*(j+.5)/K
  for q in range(1,4):
   f=q/4.0;u=n['u_in']+(n['u_out']-n['u_in'])*f;r=n['r_in']+(n['r_out']-n['r_in'])*f-.006;zs=n['head']['zs_in']
   b=BCI143-dep*f;a=u+r*math.cos(t);z=zs+r*math.sin(t)
   ta=(-math.sin(t),math.cos(t))
   p=[(a+ta[0]*s*.07,z+ta[1]*s*.07) for s in (-1,1)]
   hexa143(m,[PF143(p[0][0],b-.07,p[0][1]),PF143(p[1][0],b-.07,p[1][1]),PF143(p[1][0],b+.07,p[1][1]),PF143(p[0][0],b+.07,p[0][1])],
    [PF143(p[0][0]-.004*math.cos(t),b-.07,p[0][1]-.004*math.sin(t)),PF143(p[1][0]-.004*math.cos(t),b-.07,p[1][1]-.004*math.sin(t)),PF143(p[1][0]-.004*math.cos(t),b+.07,p[1][1]-.004*math.sin(t)),PF143(p[0][0]-.004*math.cos(t),b+.07,p[0][1]-.004*math.sin(t))],M143['Coffer'])
b143_finish(m,bevel=False)

# ================================================================= cameras
def sv_camera143(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def cam143(name,a,b,dz,da,db,pitch,vfov):
 x,y,_=PF143(a,b);vx,vy=U143[0]*da+N143[0]*db,U143[1]*da+N143[1]*db
 return sv_camera143(name,x,y,FL143+dz,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
CAM143_SPECS=[
 # name, position (a, b), height over the floor, look direction (a, b), pitch, vertical fov
 ('800_Block143_Cal_Drottningsalen1933NE',15.9,BOI143-7.96,1.50,-.565,.825,9.0,52.0),
 ('801_Block143_Cal_Drottningsalen_DoorRutsalen',PA143[0]-8.0,B143D['bmid'],1.60,1.0,0.0,-1.0,52.0),
 ('802_Block143_Cal_RutsalenWindows',A1R143-1.2,BOI143-1.4,1.55,A0R143-(A1R143-1.2),BCI143-(BOI143-1.4),3.0,55.0),
 ('803_Block143_Cal_RutsalenPanel',21.6,BCI143+3.2,1.55,0.0,1.0,6.0,50.0),
]
block143_cameras=[cam143(*s) for s in CAM143_SPECS]
_x143,_y143,_=PF143(16.0,-40.0);_tx143,_ty143,_=PF143(17.0,-11.0)
block143_cameras.append(('804_Block143_Aerial_NorthRange',(round(_x143,2),round(_y143,2),70.0),(round(_tx143,2),round(_ty143,2),12.0),22))
print('BLOCK143_GEOMETRY',len(block143_names))
