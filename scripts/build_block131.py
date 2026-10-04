"""Pass 131: Gröna salen and Förbrända salen, two state-floor halls of Kalmar slott.
- SM_Castle131_GronaSalen: Gröna salen (Olsson's room 87, 'Stora västra salen'; Möller's
  'Unions-salen'), in the west range between Kuretornet and the west round tower (Rödkullatornet), with
  its far end in the corner where the chapel (pass 130) begins. A long hall with a wide-board floor; an
  exposed ceiling of grey-washed beams on boards (Möller 1882: beams' underside 6.55 m over the floor),
  which fan at the far end where the courtyard wall bends; deep rectangular window niches (five on the
  courtyard, four on the outer front, one plus a blind one in the far end wall) with painted soffits and
  their own glazing; the west tower's round wall bulging into the far corner with a pedimented door;
  a pedimented door in the east wall and opposite the chapel's west door; a hooded fireplace by131 the east
  wall.
- SM_Castle131_GronaInventarier: the funeral escutcheons on the piers and the east wall, and the large
  crucifix on the outer wall (photographs 2015, 2017; 1929).
- SM_Castle131_ForbrandaSalen: Förbrända salen (Olsson's rooms 74 and 76, 'Stora östra salen'), in
  the east range between the bays of Olsson's towers VI and VII. The hall as restored in 1923 and as it
  is now: plastered walls with tall round-arched window niches (five on the courtyard, three on the
  outer front; Möller 1882: niche crowns 5.6 m over the floor), a board ceiling on flat cross beams
  (underside about 6.2 m), a wide-board floor, a hooded fireplace on the outer wall (1923 photograph)
  and a stone fireplace with a crest panel in the north wall (2017 photograph), plank doors in both end
  walls.
The rooms are closed solids inside pass 27's hollow ranges; no existing mesh is changed. Positions and
footprints come from scripts/prepare_block131.py (source/block131.json). See references/block131-notes.md.
"""
from mathutils import Vector
from mathutils.geometry import tessellate_polygon as tess131
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B131D=json.loads((R/'source/block131.json').read_text())
block131_names=[];B131={}
for old in [k for k in list(materials) if k.startswith('M_Block131_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownPaintWhite',(.80,.72,.64),.93,0),('Reveal','TownPaintWhite',(.90,.88,.84),.92,0),('PlasterF','TownPaintWhite',(.78,.72,.65),.93,0),
 ('RevealF','TownPaintWhite',(.86,.82,.76),.92,0),('Beam','TownPaintBrown',(.50,.47,.42),.85,0),('CeilBoard','TownPaintBrown',(.62,.59,.54),.85,0),
 ('CeilF','TownPaintBrown',(.55,.42,.31),.80,0),('BeamF','TownPaintBrown',(.47,.35,.25),.80,0),('Boards','TownPaintBrown',(.80,.73,.62),.80,0),
 ('Boards2','TownPaintBrown',(.76,.69,.58),.80,0),('Joint','TownStone',(.30,.29,.28),.90,0),('Stone','TownStone',(.74,.72,.67),.85,0),
 ('Soffit','TownPaintWhite',(.70,.72,.66),.88,0),('SoffitPanel','TownPaintWhite',(.88,.86,.79),.88,0),('SoffitLine','TownPaintWhite',(.48,.50,.46),.88,0),
 ('WinFrame','TownPaintGreen',(.44,.50,.44),.60,0),('Daylight','TownPaintWhite',(.84,.90,.93),.20,0),('Door','TownPaintBrown',(.40,.34,.27),.70,0),
 ('DoorF','TownPaintBrown',(.26,.19,.14),.75,0),('Soot','TownPaintBrown',(.12,.10,.09),.90,0),('Iron','TownMetalGrey',(.20,.20,.20),.55,.5),
 ('Gilt','TownIvory',(.74,.58,.28),.45,.35),('EscWood','TownPaintBrown',(.30,.22,.16),.70,0),('EscRed','TownPaintBrown',(.50,.16,.13),.65,0),
 ('EscBlue','TownPaintWhite',(.24,.32,.48),.65,0),('EscSilver','TownMetalGrey',(.70,.71,.70),.40,.5),('Oak','TownPaintBrown',(.55,.43,.30),.70,0),
 ('Brick','TownTileRed',(.52,.30,.22),.85,0),
 ]:
 name='M_Block131_'+key;B131[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block131_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M131=B131

def b131_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block131_names.append(name);return Mesh(name,category)
def drop_degenerate_faces131(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 from collections import Counter
 print('BLOCK131_DROP_BY_MATERIAL',obj.name,Counter(obj.data.materials[f.material_index].name for f in bad).most_common(8))
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b131_finish(m,bevel=True):
 # The halls get the town's small edge bevel (s21_finish). The furnishings are small parts on which
 # that bevel only makes collapsed slivers (pass 130), so they get the same world-scale UVs without it.
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
 print('BLOCK131_FACES',m.name,'authored',nf,'finished',len(obj.data.polygons));obj['block131_dropped_faces']=drop_degenerate_faces131(obj)
 print('BLOCK131_DROPPED',obj.name,obj['block131_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=131;obj['reference_notes']='references/block131-notes.md';obj['osm_way']='';return obj

# ---------------------------------------------------------------- generic solids
def hexa131(m,a,b,ma):
 # Closed six-faced solid from two quads a and b, corners in matching order.
 m.faces(list(a)+list(b),[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
def setmat131(m,k,ma):
 if ma not in m.mats:m.mats.append(ma)
 m.mi[k]=m.mats.index(ma)
def prism131(m,ring,z0,zt,ma,tags=None,tagmat=None):
 # A closed prism over a simple polygon (x, y) with its top at zt (one value or one per vertex); the
 # caps are triangulated (no large n-gons); side faces may take their own material by131 edge tag.
 n=len(ring);zt=zt if isinstance(zt,(list,tuple)) else [zt]*n
 v=[(x,y,z0) for x,y in ring]+[(x,y,z) for (x,y),z in zip(ring,zt)]
 tris=tess131([[Vector((x,y,0)) for x,y in ring]])
 f=[(c,b,a) for a,b,c in tris]+[(n+a,n+b,n+c) for a,b,c in tris]
 side0=len(f);f+=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 base=len(m.f);m.faces(v,f,ma)
 if tags and tagmat:
  for i,t in enumerate(tags):
   if t in tagmat:setmat131(m,base+side0+i,tagmat[t])
def fan131(m,pts,d0,d1,frame,ma,center=None):
 # A flat convex shape given as (a,z) outline points in a vertical plane, extruded across d0..d1, as
 # a triangle fan (no large n-gon). frame(a,d,z) -> world point.
 n=len(pts)
 if center is None:
  v=[frame(a,d,z) for d in (d0,d1) for a,z in pts]
  f=[(0,i,i+1) for i in range(1,n-1)]+[(n,n+i+1,n+i) for i in range(1,n-1)]
 else:
  v=[frame(a,d,z) for d in (d0,d1) for a,z in pts]+[frame(center[0],d0,center[1]),frame(center[0],d1,center[1])]
  f=[(2*n,i,(i+1)%n) for i in range(n)]+[(2*n+1,n+(i+1)%n,n+i) for i in range(n)]
 f+=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 m.faces(v,f,ma)
def circ131(a,z,r,k=16):return [(a+r*math.cos(2*math.pi*q/k),z+r*math.sin(2*math.pi*q/k)) for q in range(k)]
def lframe131(p,t,nrm):
 # A local frame at the point p on a wall face: a along the wall (t), d into the wall (nrm), z up.
 # nrm is made square to t, so that boxes in the frame are true boxes (the town bevel collapses the
 # corners of slightly skewed ones).
 L=math.hypot(t[0],t[1]);t=(t[0]/L,t[1]/L);k=nrm[0]*t[0]+nrm[1]*t[1];nrm=(nrm[0]-k*t[0],nrm[1]-k*t[1]);L=math.hypot(*nrm);nrm=(nrm[0]/L,nrm[1]/L)
 return lambda a,d,z:(p[0]+t[0]*a+nrm[0]*d,p[1]+t[1]*a+nrm[1]*d,z)
def lbox131(m,fr,a0,a1,d0,d1,z0,z1,ma):
 a0,a1=min(a0,a1),max(a0,a1);d0,d1=min(d0,d1),max(d0,d1);z0,z1=min(z0,z1),max(z0,z1)
 if a1-a0<.002 or d1-d0<.002 or z1-z0<.002:return
 hexa131(m,[fr(a0,d0,z0),fr(a1,d0,z0),fr(a1,d1,z0),fr(a0,d1,z0)],[fr(a0,d0,z1),fr(a1,d0,z1),fr(a1,d1,z1),fr(a0,d1,z1)],ma)
def beam131(m,p,q,w,z0,z1,ma):
 d=Vector((q[0]-p[0],q[1]-p[1],0));L=d.length;d/=L;s=Vector((-d.y,d.x,0))*w/2
 P=Vector((p[0],p[1],0));Q=Vector((q[0],q[1],0))
 a=[P-s,P+s,Q+s,Q-s];hexa131(m,[(v.x,v.y,z0) for v in a],[(v.x,v.y,z1) for v in a],ma)

# ---------------------------------------------------------------- shared furnishings of the walls
def pediment_door131(m,fr,w,h,z,leaf_d=None,leafmat=None,depth=.30):
 # A door in a wall face: a stone surround with an entablature and a triangular pediment with three
 # ball finials (photographs 2015/2017), and, if leaf_d, a closed panelled leaf set back in the reveal.
 S=M131['Stone'];jw=.14
 for a0,a1 in ((-w/2-jw,-w/2),(w/2,w/2+jw)):lbox131(m,fr,a0,a1,-.06,0,z,z+h,S)
 lbox131(m,fr,-w/2-jw,w/2+jw,-.06,0,z+h,z+h+.14,S)
 lbox131(m,fr,-w/2-jw-.08,w/2+jw+.08,-.12,0,z+h+.14,z+h+.26,S)
 hw=w/2+jw+.04;fan131(m,[(-hw,z+h+.26),(hw,z+h+.26),(0,z+h+.26+.46)],-.10,0,fr,S)
 for a,zz in ((-hw+.05,z+h+.26),(hw-.05,z+h+.26),(0,z+h+.70)):
  x,y,_=fr(a,-.06,0);m.lathe(x,y,zz,[(.012,0),(.05,.02),(.075,.08),(.065,.14),(.012,.17)],S,10)
 if leaf_d is not None:
  L=leafmat or M131['Door']
  lbox131(m,fr,-w/2,w/2,leaf_d-.025,leaf_d+.025,z,z+h,L)
  for k in range(2):
   z0_=z+.14+k*(h-.28)/2+(.05 if k else 0);z1_=z+.14+(k+1)*(h-.28)/2-(0 if k else .05)
   for a0,a1,b0,b1 in ((-w/2+.10,w/2-.10,z0_,z0_+.045),(-w/2+.10,w/2-.10,z1_-.045,z1_),(-w/2+.10,-w/2+.145,z0_,z1_),(w/2-.145,w/2-.10,z0_,z1_)):
    lbox131(m,fr,a0,a1,leaf_d-.045,leaf_d-.025,b0,b1,L)
  lbox131(m,fr,w/2-.24,w/2-.17,leaf_d-.05,leaf_d-.025,z+h*.47,z+h*.49,M131['Iron'])
def window131(m,fr,a0,a1,zb,zs,zh,ma_frame,bars=(1,2)):
 # Glazing in a vertical plane: a pane, a frame, mullions and transoms, glazing bars, and a head
 # board up to zh (the niche head). fr(a,d,z): d < 0 towards the room.
 F=ma_frame;lbox131(m,fr,a0+.02,a1-.02,-.01,.01,zb+.04,zs,M131['Daylight'])
 for b0,b1 in ((a0,a0+.07),(a1-.07,a1)):lbox131(m,fr,b0,b1,-.07,.02,zb,zh,F)
 lbox131(m,fr,a0,a1,-.07,.02,zb,zb+.08,F);lbox131(m,fr,a0,a1,-.07,.02,zs-.04,zh,F)
 nm,nt=bars
 for k in range(1,nm+1):a=a0+(a1-a0)*k/(nm+1);lbox131(m,fr,a-.03,a+.03,-.06,.015,zb+.08,zs,F)
 for k in range(1,nt+1):z=zb+.08+(zs-zb-.08)*k/(nt+1);lbox131(m,fr,a0+.07,a1-.07,-.06,.015,z-.03,z+.03,F)
 # thin glazing bars (small panes)
 na=(nm+1)*2;nz=(nt+1)*3
 for k in range(1,na):
  if k%2==0:continue
  a=a0+(a1-a0)*k/na;lbox131(m,fr,a-.008,a+.008,-.03,.012,zb+.08,zs,F)
 for k in range(1,nz):
  if k%3==0:continue
  z=zb+.08+(zs-zb-.08)*k/nz;lbox131(m,fr,a0+.07,a1-.07,-.03,.012,z-.008,z+.008,F)

# ================================================================= Gröna salen
G131=B131D['gron'];LG131=G131['levels'];FLG131=LG131['floor']
m=b131_new('SM_Castle131_GronaSalen','Kalmar slott/Interiör')
# ---- walls: the pieces (east, courtyard, chapel lining, end, tower lining, outer) in bands, niches
# and doors open in their bands; reveal faces whiter
for wb in G131['wallbands']:
 prism131(m,wb['ring'],wb['z0'],wb['zt'] if wb['z1']==LG131['ztop'] else wb['z1'],M131['Plaster'],wb['tags'],{'r':M131['Reveal']})
# ---- floor: bedding and wide boards along the range
prism131(m,G131['room'],LG131['z0'],FLG131-.015,M131['Joint'])
for b in G131['boards']:prism131(m,b['ring'],FLG131-.015,FLG131,M131['Boards2' if b['k'] else 'Boards'])
# ---- ceiling: boards on the beams; the beams across the hall, fanning at the far end
prism131(m,G131['room'],LG131['board_under'],LG131['ztop'],M131['CeilBoard'])
for p,q in G131['beams']:beam131(m,p,q,.24,LG131['beam_under'],LG131['board_under'],M131['Beam'])
# ---- niches: the parapet under the window, the window, the painted soffit
for n in G131['niches']:
 f0,f1,b1,b0=[Vector((x,y,0)) for x,y in n['foot']]     # face left/right, back right/left
 dep131=n['depth']+(0 if n['blind'] else .05)
 def NP131(t,side,f0=f0,f1=f1,b0=b0,b1=b1,dep131=dep131):
  # point at depth t (metres from the room face) on the niche's left (0) or right (1) side
  a=(f0 if side==0 else f1);b=(b0 if side==0 else b1);return a+(b-a)*(t/dep131)
 tg131=n['depth']-.04 if not n['blind'] else n['depth']-.02
 tp131=max(.0,tg131-.55)
 # parapet (sill block) at the back of the niche, up to the facade's sill
 q=[NP131(tp131,0),NP131(tp131,1),NP131(tg131+.04 if not n['blind'] else tg131+.02,1),NP131(tg131+.04 if not n['blind'] else tg131+.02,0)]
 hexa131(m,[(v.x,v.y,LG131['niche_floor']) for v in q],[(v.x,v.y,LG131['sill']) for v in q],M131['Reveal'])
 bx131,by131=[(NP131(tp131,0).x+NP131(tp131,1).x)/2,(NP131(tp131,0).y+NP131(tp131,1).y)/2]
 # the window in the plane at tg131
 pl131,pr131=NP131(tg131,0),NP131(tg131,1);t=(pr131-pl131);w=t.length;t/=w;nr131=Vector(n['nrm']+[0])
 fr=lframe131((pl131.x,pl131.y),(t.x,t.y),(nr131.x,nr131.y))
 window131(m,fr,.0,w,LG131['sill'],LG131['glass_top'],LG131['niche_head']-.005,M131['WinFrame'])
 # the painted soffit: a grey-green plate with 2 x 3 light fields (photographs: grisaille ornament)
 zs0131=LG131['niche_head']-.012
 sq131=[NP131(.02,0),NP131(.02,1),NP131(tg131-.08,1),NP131(tg131-.08,0)]
 hexa131(m,[(v.x,v.y,zs0131) for v in sq131],[(v.x,v.y,LG131['niche_head']) for v in sq131],M131['Soffit'])
 for i in range(3):
  for j in range(2):
   u0131,u1131=.02+(tg131-.10)*i/3+.06,.02+(tg131-.10)*(i+1)/3-.06
   def SP131(u,v):a=NP131(u,0);b=NP131(u,1);return a+(b-a)*v
   pq131=[SP131(u0131,j/2+.05),SP131(u0131,(j+1)/2-.05),SP131(u1131,(j+1)/2-.05),SP131(u1131,j/2+.05)]
   hexa131(m,[(v.x,v.y,zs0131-.012) for v in pq131],[(v.x,v.y,zs0131) for v in pq131],M131['SoffitPanel'])
   cq131=[SP131((u0131+u1131)/2-.06,j/2+.18),SP131((u0131+u1131)/2-.06,(j+1)/2-.18),SP131((u0131+u1131)/2+.06,(j+1)/2-.18),SP131((u0131+u1131)/2+.06,j/2+.18)]
   hexa131(m,[(v.x,v.y,zs0131-.024) for v in cq131],[(v.x,v.y,zs0131-.012) for v in cq131],M131['SoffitLine'])
# ---- doors: pedimented stone surrounds; leaves closed (east, tower); the chapel's own leaf is pass 130's
for d in G131['doors']:
 fr=lframe131(d['p'],d['t'],d['nrm'])
 pediment_door131(m,fr,d['w'],LG131['door_head']-FLG131,FLG131,leaf_d=(d['depth']-.06) if d['leaf'] else None)
 # threshold stone
 lbox131(m,fr,-d['w']/2,d['w']/2,-.08,d['depth'],FLG131-.01,FLG131+.012,M131['Stone'])
# ---- the hooded fireplace by131 the east wall (panorama 2015): a stone surround, a plastered breast and a
# pointed hood up to 4.3 m
fp131=G131['feat']['fireplace'];ed131=next(d for d in G131['doors'] if d['name']=='east')
fr=lframe131(fp131['p'],ed131['t'],ed131['nrm']);W131f=fp131['w'];P131f=fp131['proj']
lbox131(m,fr,-W131f/2,W131f/2,-P131f,0,FLG131,FLG131+2.55,M131['Plaster'])
hexa131(m,[fr(-W131f/2,-P131f,FLG131+2.55),fr(W131f/2,-P131f,FLG131+2.55),fr(W131f/2,0,FLG131+2.55),fr(-W131f/2,0,FLG131+2.55)],
 [fr(-.12,-.10,FLG131+4.30),fr(.12,-.10,FLG131+4.30),fr(.12,0,FLG131+4.30),fr(-.12,0,FLG131+4.30)],M131['Plaster'])
lbox131(m,fr,-.48,.48,-P131f-.005,-P131f+.05,FLG131+.05,FLG131+1.10,M131['Soot'])
for a0,a1 in ((-.68,-.48),(.48,.68)):lbox131(m,fr,a0,a1,-P131f-.06,-P131f+.02,FLG131,FLG131+1.30,M131['Stone'])
lbox131(m,fr,-.72,.72,-P131f-.08,-P131f+.02,FLG131+1.30,FLG131+1.46,M131['Stone']);lbox131(m,fr,-.80,.80,-P131f-.14,-P131f+.02,FLG131+1.46,FLG131+1.54,M131['Stone'])
lbox131(m,fr,-.80,.80,-P131f-.55,-P131f,FLG131,FLG131+.04,M131['Stone'])
b131_finish(m)

# ---------------------------------------------------------------- furnishings: escutcheons, crucifix
m=b131_new('SM_Castle131_GronaInventarier','Kalmar slott/Interiör')
def wallframe131(p,wall):
 # the frame of a wall face at p: t along the wall, nrm into it
 if wall=='east':d=ed131;return lframe131(p,d['t'],d['nrm'])
 nw=G131['frame'];u,nn=nw['u'],nw['n']
 if wall=='out':return lframe131(p,u,nn)
 return lframe131(p,(-u[0],-u[1]),(-nn[0],-nn[1]))
def escutcheon131(m,fr,zc,k):
 # A funeral escutcheon (begravningsvapen): a carved cartouche with a painted shield, a helmet with
 # mantling and a crest, hanging on an iron rod over a pole (photographs 2015/2017, 1929; simplified).
 E=M131['EscWood'];GILT131=M131['Gilt'];cols=[M131['EscRed'],M131['EscBlue'],M131['EscSilver']]
 car=[(.0,zc+.62),(.30,zc+.52),(.46,zc+.22),(.50,zc-.10),(.40,zc-.42),(.18,zc-.62),(.0,zc-.70),(-.18,zc-.62),(-.40,zc-.42),(-.50,zc-.10),(-.46,zc+.22),(-.30,zc+.52)]
 fan131(m,car,-.10,-.02,fr,E,(0,zc-.05))
 sh=[(-.26,zc+.30),(.26,zc+.30),(.26,zc-.12),(.16,zc-.34),(.0,zc-.42),(-.16,zc-.34),(-.26,zc-.12)]
 fan131(m,sh,-.13,-.10,fr,cols[k%3],(0,zc))
 fan131(m,[(-.26,zc+.05),(.26,zc+.05),(.26,zc-.03),(-.26,zc-.03)],-.145,-.13,fr,GILT131)
 for a in (-.42,.42):fan131(m,circ131(a,zc+.10,.10,10),-.14,-.06,fr,GILT131,(a,zc+.10))
 fan131(m,[(-.16,zc+.62),(.16,zc+.62),(.20,zc+.80),(.10,zc+.94),(-.10,zc+.94),(-.20,zc+.80)],-.16,-.04,fr,M131['EscSilver'],(0,zc+.78))
 fan131(m,[(-.12,zc+.94),(.12,zc+.94),(.16,zc+1.10),(.0,zc+1.26),(-.16,zc+1.10)],-.12,-.06,fr,cols[(k+1)%3],(0,zc+1.08))
 for sg in (-1,1):fan131(m,[(sg*.18,zc+.70),(sg*.55,zc+.45),(sg*.62,zc+.05),(sg*.40,zc+.30)],-.09,-.03,fr,cols[(k+1)%3])
 lbox131(m,fr,-.02,.02,-.05,-.01,zc-2.40,zc-.68,M131['Iron'])
 lbox131(m,fr,-.015,.015,-.03,0,zc+1.26,LG131['beam_under']-.05,M131['Iron'])
for k,e in enumerate(G131['feat']['escutcheons']):escutcheon131(m,wallframe131(e['p'],e['wall']),e['zc'],k)
def crucifix131(m,fr,zc,k=1.0):
 # The large carved crucifix (photographs 2015/2017), simplified: the cross with its end blocks and the corpus.
 O131w=M131['Oak'];fr0=fr;fr=lambda a,d,z:fr0(a*k,d,zc+(z-zc)*k)
 lbox131(m,fr,-.07,.07,-.14,-.02,zc-1.55,zc+1.15,O131w);lbox131(m,fr,-.80,.80,-.14,-.02,zc+.42,zc+.56,O131w)
 for sg in (-1,1):lbox131(m,fr,sg*.80-.09,sg*.80+.09,-.15,-.02,zc+.38,zc+.60,O131w)
 lbox131(m,fr,-.09,.09,-.15,-.02,zc+1.08,zc+1.26,O131w)
 # the corpus: torso, loincloth, legs, arms, head
 fan131(m,[(-.14,zc+.38),(.14,zc+.38),(.12,zc-.18),(-.12,zc-.18)],-.30,-.14,fr,O131w)
 fan131(m,[(-.16,zc-.18),(.16,zc-.18),(.12,zc-.42),(-.12,zc-.42)],-.31,-.14,fr,O131w)
 fan131(m,[(-.09,zc-.42),(.07,zc-.42),(.03,zc-1.20),(-.06,zc-1.20)],-.26,-.14,fr,O131w)
 for sg in (-1,1):fan131(m,[(sg*.12,zc+.34),(sg*.12,zc+.44),(sg*.74,zc+.56),(sg*.74,zc+.48)],-.24,-.14,fr,O131w)
 x,y,_=fr(0,-.22,0);m.lathe(x,y,zc+.40*k,[(r*k,h*k) for r,h in [(.01,0),(.07,.03),(.10,.12),(.09,.22),(.05,.28),(.01,.30)]],O131w,10)
crucifix131(m,wallframe131(G131['feat']['crucifix']['p'],G131['feat']['crucifix']['wall']),G131['feat']['crucifix']['zc'])
ce131=G131['feat']['crucifix_end'];crucifix131(m,lframe131(ce131['p'],ce131['t'],ce131['nrm']),ce131['zc'],ce131['scale'])
b131_finish(m,bevel=False)

# ================================================================= Förbrända salen
FB131=B131D['forb'];LF131=FB131['levels'];FLF131=LF131['floor'];RF131=FB131['room']
OFb131,UFb131,NFb131=FB131['frame']['origin'],FB131['frame']['u'],FB131['frame']['n'];ANGF131=math.atan2(UFb131[1],UFb131[0])
def PF131(a,b,z=0.0):return (OFb131[0]+UFb131[0]*a+NFb131[0]*b,OFb131[1]+UFb131[1]*a+NFb131[1]*b,z)
def bxF131(m,a0,a1,b0,b1,z0,z1,ma):
 a0,a1=min(a0,a1),max(a0,a1);b0,b1=min(b0,b1),max(b0,b1);z0,z1=min(z0,z1),max(z0,z1)
 if a1-a0<.002 or b1-b0<.002 or z1-z0<.002:return
 x,y,_=PF131((a0+a1)/2,(b0+b1)/2);m.box((x,y,(z0+z1)/2),(a1-a0,b1-b0,z1-z0),ma,ANGF131)
def bob131(a):o=RF131['bo'];return o[1]+o[2]*(a-o[0])-.10
AS131,AN131,TE131=RF131['a_s'],RF131['a_n'],RF131['t_end'];BCI131,BOI131,BCB131=RF131['bci'],RF131['boi'],RF131['bcb'];ZTF131=LF131['ztop']
m=b131_new('SM_Castle131_ForbrandaSalen','Kalmar slott/Interiör')
def lwall131(m,c_in,c_out,s0,s1,z0,z1,holes,ma,mr,K=16):
 # A long wall between c_in (room face) and c_out(s) (back), from s0 to s1, with round-arched window
 # niches (pass 130's method): piers, the parapet under each niche's floor, and the head over each
 # niche as a fan of slabs up to the wall's top. Reveal faces in mr.
 at_i=at_o=s0
 for h in sorted(holes,key=lambda h:h['u_in'])+[None]:
  li,lo_=(h['u_in']-h['r_in'],h['u_out']-h['r_out']) if h else (s1,s1)
  if li-at_i>.002:
   hexa131(m,[PF131(at_i,c_in,z0),PF131(li,c_in,z0),PF131(li,c_in,z1),PF131(at_i,c_in,z1)],[PF131(at_o,c_out(at_o),z0),PF131(lo_,c_out(lo_),z0),PF131(lo_,c_out(lo_),z1),PF131(at_o,c_out(at_o),z1)],ma)
   if h is not None:setmat131(m,len(m.f)-3,mr)      # the jamb towards the next niche
   if at_i>s0+1e-6:setmat131(m,len(m.f)-1,mr)        # the jamb of the niche before
  if h is None:break
  ri,ro=h['u_in']+h['r_in'],h['u_out']+h['r_out']
  hexa131(m,[PF131(li,c_in,z0),PF131(ri,c_in,z0),PF131(ri,c_in,h['zb']),PF131(li,c_in,h['zb'])],[PF131(lo_,c_out(lo_),z0),PF131(ro,c_out(ro),z0),PF131(ro,c_out(ro),h['zb']),PF131(lo_,c_out(lo_),h['zb'])],ma)
  setmat131(m,len(m.f)-2,mr)                          # the niche's floor
  def A(th,inner):
   return (h['u_in']+h['r_in']*math.cos(th),h['zs_in']+h['h_in']*math.sin(th)) if inner else (h['u_out']+h['r_out']*math.cos(th),h['zs_out']+h['h_out']*math.sin(th))
  # straight jambs from the niche floor to the springing are the piers' faces; the arch as slabs
  for j in range(K):
   t0,t1=math.pi*j/K,math.pi*(j+1)/K;(a0,b0),(a1,b1)=A(t0,True),A(t1,True);(e0,f0),(e1,f1)=A(t0,False),A(t1,False)
   hexa131(m,[PF131(a0,c_in,b0),PF131(a1,c_in,b1),PF131(a1,c_in,z1),PF131(a0,c_in,z1)],[PF131(e0,c_out(e0),f0),PF131(e1,c_out(e1),f1),PF131(e1,c_out(e1),z1),PF131(e0,c_out(e0),z1)],ma)
   setmat131(m,len(m.f)-4,mr)                         # the arch's soffit
  at_i,at_o=ri,ro
cof131=lambda s:BCB131
oof131=lambda s:bob131(s)
holes_c131=[n for n in FB131['niches'] if n['wall']=='court'];holes_o131=[n for n in FB131['niches'] if n['wall']=='out']
lwall131(m,BCI131,cof131,AS131-TE131,AN131+TE131,LF131['z0'],ZTF131,holes_c131,M131['PlasterF'],M131['RevealF'])
lwall131(m,BOI131,oof131,AS131-TE131,AN131+TE131,LF131['z0'],ZTF131,holes_o131,M131['PlasterF'],M131['RevealF'])
# niche parapets (sill blocks at the back) and glazing
for n in FB131['niches']:
 out=n['wall']=='out';sg=1 if out else -1;c_in=BOI131 if out else BCI131
 cb=(bob131(n['u_out']) if out else BCB131)
 cg=cb-sg*.04;dep131=abs(cb-c_in)
 # parapet: the last 0.6 m of the niche, from its floor to the facade's sill (12 mm short of the back,
 # which runs 0.5 deg off this frame on the outer side)
 r=n['r_out'];bxF131(m,n['u_out']-r,n['u_out']+r,cb-sg*.012,cb-sg*.60,n['zb'],LF131['sill'],M131['RevealF'])
 # frame: a along the wall, d < 0 towards the room
 fr=(lambda cg,sg:(lambda a,d,z:PF131(a,cg+sg*d,z)))(cg,sg)
 zs=LF131['glass_top']
 window131(m,fr,n['u_out']-r+.01,n['u_out']+r-.01,LF131['sill'],zs,zs+.10,M131['WinFrame'],bars=(1,3))
 # the arched head over the window: a fan of glass and a frame up to the niche's arch at the back
 u=n['u_out'];rr131=r-.02;zsp131=n['zs_out']
 if zsp131>zs+.10:lbox131(m,fr,u-rr131,u+rr131,-.01,.01,zs+.10,zsp131,M131['Daylight'])
 fan131(m,[(u,zsp131)]+[(u+rr131*math.cos(math.pi*k/12),zsp131+(n['h_out']-.02)*math.sin(math.pi*k/12)) for k in range(13)],-.01,.01,fr,M131['Daylight'])
 for k in range(12):
  a0,a1=math.pi*k/12,math.pi*(k+1)/12
  p0=[(u+rr131*math.cos(a0),zsp131+(n['h_out']-.02)*math.sin(a0)),(u+r*math.cos(a0),zsp131+n['h_out']*math.sin(a0))]
  p1=[(u+rr131*math.cos(a1),zsp131+(n['h_out']-.02)*math.sin(a1)),(u+r*math.cos(a1),zsp131+n['h_out']*math.sin(a1))]
  if zsp131+(n['h_out'])*math.sin(a0)<zs and zsp131+(n['h_out'])*math.sin(a1)<zs:continue
  fan131(m,[p0[0],p0[1],p1[1],p1[0]],-.06,.015,fr,M131['WinFrame'])
 lbox131(m,fr,u-.03,u+.03,-.06,.015,zs+.10,zsp131+n['h_out']-.04,M131['WinFrame'])
 for zz in (zs+.05,zsp131):lbox131(m,fr,u-r,u+r,-.06,.015,zz-.03,zz+.03,M131['WinFrame'])
# end walls with doors (plank leaves, closed)
def ewall131(m,a_in,a_out,door):
 c,w,hh=door['b'],door['w'],door['h'];zh=FLF131+hh
 bxF131(m,a_in,a_out,BCI131,BOI131,LF131['z0'],FLF131,M131['PlasterF'])
 bxF131(m,a_in,a_out,BCI131,c-w/2,FLF131,zh,M131['PlasterF']);bxF131(m,a_in,a_out,c+w/2,BOI131,FLF131,zh,M131['PlasterF'])
 bxF131(m,a_in,a_out,BCI131,BOI131,zh,ZTF131,M131['PlasterF'])
 sg=1 if a_out>a_in else -1;leaf=a_in+sg*.30
 bxF131(m,leaf-.03,leaf+.03,c-w/2,c+w/2,FLF131,zh,M131['DoorF'])
 for k in range(5):bxF131(m,leaf-sg*.05,leaf-sg*.03,c-w/2+.05+k*(w-.10)/5+.01,c-w/2+.05+(k+1)*(w-.10)/5-.01,FLF131+.05,zh-.05,M131['DoorF'])
 for z0_ in (FLF131+.35,zh-.55):bxF131(m,leaf-sg*.07,leaf-sg*.05,c-w/2+.05,c+w/2-.05,z0_,z0_+.12,M131['DoorF'])
 bxF131(m,leaf-sg*.08,leaf-sg*.05,c+w/2-.20,c+w/2-.14,FLF131+1.0,FLF131+1.06,M131['Iron'])
 bxF131(m,a_in-sg*.01,a_out,c-w/2,c+w/2,FLF131-.01,FLF131+.012,M131['Stone'])
for d in FB131['doors']:
 if d['wall']=='south':ewall131(m,AS131,AS131-TE131,d)
 else:ewall131(m,AN131,AN131+TE131,d)
# floor: bedding and wide boards along the hall
bxF131(m,AS131,AN131,BCI131,BOI131,LF131['z0'],FLF131-.015,M131['Joint'])
nb131=round((BOI131-BCI131)/.32);wbd131=(BOI131-BCI131)/nb131
for j in range(nb131):bxF131(m,AS131,AN131,BCI131+j*wbd131+.003,BCI131+(j+1)*wbd131-.003,FLF131-.015,FLF131,M131['Boards2' if j%2 else 'Boards'])
# ceiling: boards along the hall with thin cross battens, and a sloping board cove along both long walls
# (photographs 1923, 2017)
bxF131(m,AS131,AN131,BCI131,BOI131,LF131['board_under'],ZTF131,M131['CeilF'])
for bw131,sg131 in ((BCI131,1),(BOI131,-1)):
 zl131=LF131['board_under']-.55;bi131=bw131+sg131*.85
 hexa131(m,[PF131(AS131,bw131,zl131),PF131(AN131,bw131,zl131),PF131(AN131,bi131,LF131['board_under']),PF131(AS131,bi131,LF131['board_under'])],
  [PF131(AS131,bw131,zl131+.07),PF131(AN131,bw131,zl131+.07),PF131(AN131,bi131+sg131*.07,LF131['board_under']+.0),PF131(AS131,bi131+sg131*.07,LF131['board_under']+.0)],M131['CeilF'])
 for k in range(1,round((AN131-AS131)/.30)):
  a=AS131+(AN131-AS131)*k/round((AN131-AS131)/.30)
  hexa131(m,[PF131(a-.006,bw131+sg131*.01,zl131-.012),PF131(a+.006,bw131+sg131*.01,zl131-.012),PF131(a+.006,bi131,LF131['board_under']-.012),PF131(a-.006,bi131,LF131['board_under']-.012)],
   [PF131(a-.006,bw131+sg131*.01,zl131+.002),PF131(a+.006,bw131+sg131*.01,zl131+.002),PF131(a+.006,bi131,LF131['board_under']+.002),PF131(a-.006,bi131,LF131['board_under']+.002)],M131['BeamF'])
nc131=round((AN131-AS131)/.30)
for k in range(1,nc131):a=AS131+(AN131-AS131)*k/nc131;bxF131(m,a-.006,a+.006,BCI131,BOI131,LF131['board_under']-.012,LF131['board_under'],M131['BeamF'])
for a in FB131['feat']['beams']:bxF131(m,a-.07,a+.07,BCI131+.6,BOI131-.6,LF131['board_under']-.06,LF131['board_under'],M131['BeamF'])
# the hooded fireplace on the outer wall (1923): hearth, stone jambs and mantel, a pointed hood
hd131=FB131['feat']['hood'];a=hd131['a'];w=hd131['w'];pj=hd131['proj']
bxF131(m,a-w/2-.10,a+w/2+.10,BOI131-pj-.25,BOI131,FLF131,FLF131+.06,M131['Brick'])
bxF131(m,a-w/2+.20,a+w/2-.20,BOI131-.04,BOI131,FLF131+.06,FLF131+1.20,M131['Soot'])
for sg in (-1,1):bxF131(m,a+sg*(w/2-.10),a+sg*(w/2),BOI131-pj,BOI131,FLF131,FLF131+1.25,M131['Stone'])
bxF131(m,a-w/2-.05,a+w/2+.05,BOI131-pj-.06,BOI131,FLF131+1.25,FLF131+1.40,M131['Stone'])
hexa131(m,[PF131(a-w/2,BOI131-pj,FLF131+1.40),PF131(a+w/2,BOI131-pj,FLF131+1.40),PF131(a+w/2,BOI131,FLF131+1.40),PF131(a-w/2,BOI131,FLF131+1.40)],
 [PF131(a-.16,BOI131-.08,FLF131+4.40),PF131(a+.16,BOI131-.08,FLF131+4.40),PF131(a+.16,BOI131,FLF131+4.40),PF131(a-.16,BOI131,FLF131+4.40)],M131['PlasterF'])
# the north wall's stone fireplace with a crest panel above it (2017 photograph)
fn131=FB131['feat']['fireplace_north'];c=fn131['b'];w=fn131['w'];aw131=AN131
bxF131(m,aw131-.06,aw131,c-w/2+.18,c+w/2-.18,FLF131+.02,FLF131+1.12,M131['Soot'])
for sg in (-1,1):bxF131(m,aw131-.16,aw131,c+sg*(w/2-.09)-.09,c+sg*(w/2-.09)+.09,FLF131,FLF131+1.30,M131['Stone'])
bxF131(m,aw131-.18,aw131,c-w/2,c+w/2,FLF131+1.30,FLF131+1.52,M131['Stone']);bxF131(m,aw131-.26,aw131,c-w/2-.08,c+w/2+.08,FLF131+1.52,FLF131+1.62,M131['Stone'])
bxF131(m,aw131-.55,aw131,c-w/2-.05,c+w/2+.05,FLF131,FLF131+.05,M131['Stone'])
frn131=lambda a_,d,z:PF131(aw131+d,c+a_,z)
fan131(m,[(-.45,FLF131+2.30),(.45,FLF131+2.30),(.45,FLF131+2.95),(0,FLF131+3.25),(-.45,FLF131+2.95)],-.05,0,frn131,M131['Stone'],(0,FLF131+2.70))
fan131(m,[(-.28,FLF131+2.88),(.28,FLF131+2.88),(.28,FLF131+2.62),(.16,FLF131+2.46),(0,FLF131+2.40),(-.16,FLF131+2.46),(-.28,FLF131+2.62)],-.08,-.05,frn131,M131['EscRed'],(0,FLF131+2.65))
b131_finish(m)

# ================================================================= cameras
def sv_camera131(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
GF131=G131['frame']
def PG131(s,c):o,u,n=GF131['origin'],GF131['u'],GF131['n'];return (o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c)
def camG131(name,s,c,dz,ds,dc,pitch,vfov):
 x,y=PG131(s,c);u,n=GF131['u'],GF131['n'];vx,vy=u[0]*ds+n[0]*dc,u[1]*ds+n[1]*dc
 return sv_camera131(name,x,y,FLG131+dz,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
def camF131(name,a,b,dz,da,db,pitch,vfov):
 x,y,_=PF131(a,b);vx,vy=UFb131[0]*da+NFb131[0]*db,UFb131[1]*da+NFb131[1]*db
 return sv_camera131(name,x,y,FLF131+dz,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
CAM131_SPECS=[
 # name, frame, position, height over the floor, look direction, pitch, vertical fov
 ('710_Block131_Cal_Grona2017','G',38.0,-13.6,1.55,1,.42,8.0,45.6),
 ('711_Block131_Cal_Grona1929','G',44.5,-9.8,1.40,1,.0,2.0,70.0),
 ('712_Block131_Cal_Forbranda1923','F',19.7,-8.6,1.50,-1,.0,1.0,64.0),
 ('713_Block131_Cal_Forbranda2017','F',0.5,-11.7,1.45,1,.12,9.0,45.6),
]
block131_cameras=[camG131(n,*a) if f=='G' else camF131(n,*a) for n,f,*a in CAM131_SPECS]
block131_cameras.append(('714_Block131_Aerial_WestAndEast',PG131(48,-60)+(75,),PG131(50,-30)+(12,),22))
print('BLOCK131_GEOMETRY',len(block131_names))
