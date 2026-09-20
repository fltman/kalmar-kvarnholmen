"""Stortorget PoC. Geometry in metres in a square-aligned local frame.
X: ENE (28.2 deg from east). Y: NNW. See source/site.json for WGS84 origin.
OSM footprints are measured data; facade heights/details are visual approximations.
"""
import bpy, bmesh, math, json, random, sys
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
R=Path(__file__).resolve().parents[1]
random.seed(24)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for datablock in list(bpy.data.materials):bpy.data.materials.remove(datablock)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
materials={};specs={}
CHURCH_TEXTURES={'M_Cathedral_Ochre':'ChurchOchre','M_Limestone':'ChurchAshlar','M_Aged_Copper':'ChurchCopper','M_Dark_Roof':'ChurchRoof','M_Door_Green':'ChurchDoor','M_Foundation':'ChurchRubble','M_Gold':'ChurchGilding','M_Interior_Lime':'ChurchLime','M_Pew_Grey':'ChurchPew','M_Pew_Inset':'ChurchPewInset','M_Column_Dark':'ChurchMarble','M_Interior_Stone_A':'ChurchFloor','M_Interior_Stone_B':'ChurchFloorB','M_Bench_Oak':'ChurchOak'}
def mat(name,color,rough=.75,metal=0,texture=None):
 texture=CHURCH_TEXTURES.get(name,texture)
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 specs[name]={'color':color,'roughness':rough,'metallic':metal,'texture':texture}
 settings={'ChurchLime':(2.0,.35),'ChurchOchre':(2.0,.5),'ChurchMarble':(1.0,.18),'ChurchFloor':(1.0,.45),'ChurchFloorB':(1.0,.45)}
 uvscale,_=settings.get(texture,(1.0,1.0));strength=1.0
 specs[name].update(uv_scale=uvscale,normal_strength=strength)
 if texture:
  coords=m.node_tree.nodes.new('ShaderNodeTexCoord');scale=m.node_tree.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=uvscale;m.node_tree.links.new(coords.outputs['UV'],scale.inputs[0])
 if texture:
  for suffix,socket in [('BaseColor','Base Color'),('Roughness','Roughness'),('Normal','Normal')]:
   n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/f'exports/textures/T_{texture}_{suffix}.png'));m.node_tree.links.new(scale.outputs[0],n.inputs['Vector'])
   if suffix!='BaseColor':n.image.colorspace_settings.name='Non-Color'
   if suffix=='Normal':
    nm=m.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=strength;m.node_tree.links.new(n.outputs['Color'],nm.inputs['Color']);m.node_tree.links.new(nm.outputs['Normal'],p.inputs[socket])
   else:m.node_tree.links.new(n.outputs['Color'],p.inputs[socket])
 materials[name]=m;return name
OCHRE=mat('M_Cathedral_Ochre',(.72,.38,.145));STONE=mat('M_Limestone',(.60,.55,.43));CREAM=mat('M_Warm_Limewash',(.80,.74,.55));WHITE=mat('M_OffWhite',(.78,.77,.66))
COPPER=mat('M_Aged_Copper',(.17,.34,.29),.62,.35);DARKROOF=mat('M_Dark_Roof',(.095,.11,.11),.82,.2);TILE=mat('M_Terracotta',(.34,.12,.064));RED=mat('M_Red_Plaster',(.43,.23,.16))
GLASS=mat('M_Window_Glass',(.075,.125,.14),.23,.25);FRAME=mat('M_Window_Frame',(.68,.68,.57));GREEN=mat('M_Door_Green',(.045,.105,.079));IRON=mat('M_Iron',(.055,.067,.067),.52,.6);GOLD=mat('M_Gold',(.74,.53,.22),.34,1.0)
BASE=mat('M_Foundation',(.28,.29,.26));WOOD=mat('M_Bench_Oak',(.30,.18,.085));LEAF=mat('M_Leaves',(.20,.28,.10));GRANITE=mat('M_Granite',(.55,.54,.48),texture='Granite');COBBLE=mat('M_Cobbles',(.53,.51,.45),texture='Cobbles');PATH=mat('M_Smooth_Granite',(.52,.50,.44));GROUND=mat('M_Ground',(.32,.34,.30));AWNING=mat('M_Awning_Green',(.035,.13,.09));PLASTER=mat('M_Pale_Yellow',(.73,.62,.38));PINK=mat('M_Dusty_Rose',(.63,.43,.34));GREY=mat('M_Grey_Plaster',(.57,.60,.55))
class Mesh:
 def __init__(self,name,category):self.name=name;self.category=category;self.v=[];self.f=[];self.mi=[];self.mats=[];self.sm=[];self.fuv=[]
 def faces(self,verts,faces,ma,smooth=False,uvcoords=None):
  off=len(self.v);self.v.extend(verts)
  self.fuv.extend([[uvcoords[i] for i in f] if uvcoords is not None else None for f in faces])
  if ma not in self.mats:self.mats.append(ma)
  ix=self.mats.index(ma)
  self.f.extend([tuple(off+i for i in f) for f in faces]);self.mi.extend([ix]*len(faces));self.sm.extend([smooth]*len(faces))
 def box(self,center,size,ma,angle=0):
  x,y,z=center;a,b,c=[v/2 for v in size];co,si=math.cos(angle),math.sin(angle)
  v=[(x+u*co-v*si,y+u*si+v*co,z+w) for u,v,w in [(-a,-b,-c),(a,-b,-c),(a,b,-c),(-a,b,-c),(-a,-b,c),(a,-b,c),(a,b,c),(-a,b,c)]]
  self.faces(v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ma)
 def prism(self,p,z0,z1,ma):
  n=len(p);v=[(x,y,z) for z in [z0,z1] for x,y in p]
  self.faces(v,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 def cylinder(self,x,y,z,r,h,ma,segments=16,r2=None):
  if r2 is None:r2=r
  vs=[(x+rr*math.cos(2*math.pi*i/segments),y+rr*math.sin(2*math.pi*i/segments),zz) for zz,rr in [(z,r),(z+h,r2)] for i in range(segments)]
  n=segments;self.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma);self.sm[-n:]=[True]*n
 def lathe(self,x,y,z,profile,ma,n=16):
  v=[(x+r*math.cos(i*2*math.pi/n),y+r*math.sin(i*2*math.pi/n),z+h) for r,h in profile for i in range(n)]
  f=[tuple(range(n-1,-1,-1))]
  for j in range(len(profile)-1):
   for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
  f.append(tuple(range((len(profile)-1)*n,len(profile)*n)));self.faces(v,f,ma,True);self.sm[-len(f)]=False;self.sm[-1]=False
 def finish(self):
  if not self.v:return
  me=bpy.data.meshes.new(self.name);me.from_pydata(self.v,[],self.f);me.update()
  for ma in self.mats:me.materials.append(materials[ma])
  for p,mi,sm in zip(me.polygons,self.mi,self.sm):p.material_index=mi;p.use_smooth=sm
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
  uv=me.uv_layers.new(name='UVMap')
  for poly in me.polygons:
   if self.fuv[poly.index] is not None:
    for li,coord in zip(poly.loop_indices,self.fuv[poly.index]):uv.data[li].uv=coord
    continue
   normal=poly.normal; dominant=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=dominant]
   for li in poly.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]/4,co[axes[1]]/4)
  obj=bpy.data.objects.new(self.name,me);bpy.context.collection.objects.link(obj);obj['category']=self.category
  if self.name.startswith(('SM_Domkyrka','SM_Kalmar_Domkyrka')) and self.name not in {'SM_Domkyrka_Altar_Carving','SM_Domkyrka_Interior_Carving','SM_Domkyrka_Chandeliers','SM_Domkyrka_Exterior_Details','SM_Domkyrka_Ionic_Details'}:
   bevel=obj.modifiers.new('Small crafted edge bevels','BEVEL');bevel.width=.008;bevel.segments=2;bevel.limit_method='ANGLE';bevel.angle_limit=.58;bevel.harden_normals=True
   bpy.context.view_layer.objects.active=obj;obj.select_set(True)
   bpy.ops.object.modifier_apply(modifier=bevel.name)
  if self.name=='SM_Kalmar_Domkyrka':
   # Fix bevel-generated UV corners only when their triangle UV area collapses.
   me.calc_loop_triangles();uv=me.uv_layers.active.data;bad=set()
   for tri in me.loop_triangles:
    a,b,c=[uv[i].uv for i in tri.loops];d=b-a;e=c-a
    if abs(d.x*e.y-d.y*e.x)<1e-12:bad.add(tri.polygon_index)
   for pi in bad:
    poly=me.polygons[pi];dominant=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=dominant]
    for li in poly.loop_indices:
     co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co[axes[0]]/4,co[axes[1]]/4)
  return obj
# Facade frame: u runs along wall, v points out from wall; local y thickness.
def wallbox(m,x,y,z,w,d,h,ma,angle=0):m.box((x,y,z),(w,d,h),ma,angle)
def window(m,x,y,z,w,h,angle=0,arched=False,trim=WHITE,grids=2):
 co,si=math.cos(angle),math.sin(angle)
 def b(u,v,zz,ww,dd,hh,ma):m.box((x+u*co-v*si,y+u*si+v*co,zz),(ww,dd,hh),ma,angle)
 b(0,0,z,w+.30,.16,h+.30,trim);b(0,-.10,z,w,.08,h,GLASS)
 b(-w/2,-.17,z,.075,.10,h,FRAME);b(w/2,-.17,z,.075,.10,h,FRAME)
 b(0,-.17,z+h/2,w,.1,.09,FRAME);b(0,-.17,z-h/2,w+.16,.20,.10,trim)
 for i in range(1,grids):b(-w/2+w*i/grids,-.17,z,.045,.10,h,FRAME)
 for i in range(1,max(2,round(h/.65))):b(0,-.17,z-h/2+h*i/max(2,round(h/.65)),w,.10,.04,FRAME)
 if arched:
  # semicircular head and separate stone surround
  for ma,r,off in [(trim,w/2+.15,.02),(GLASS,w/2,-.1)]:
   pts=[(-r,z+h/2),(r,z+h/2)]+[(r*math.cos(t*math.pi/16),z+h/2+r*math.sin(t*math.pi/16)) for t in range(17)]
   vs=[(x+u*co-off*si,y+u*si+off*co,zz) for u,zz in pts];m.faces(vs,[tuple(range(len(vs)))],ma)
  b(0,-.18,z+h/2+w/4,.045,.10,w/2,FRAME)
def hip(m,x,y,w,d,z,h,ma):
 a=w/2+.3;b=d/2+.3
 if w>=d:v=[(x-a,y-b,z),(x+a,y-b,z),(x+a,y+b,z),(x-a,y+b,z),(x-a+b*.7,y,z+h),(x+a-b*.7,y,z+h)];f=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(3,2,1,0)]
 else:v=[(x-a,y-b,z),(x+a,y-b,z),(x+a,y+b,z),(x-a,y+b,z),(x,y-b+a*.7,z+h),(x,y+b-a*.7,z+h)];f=[(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5),(3,2,1,0)]
 m.faces(v,f,ma)
def pediment(m,x,y,z,w,h,ma=OCHRE,angle=0):
 c,s=math.cos(angle),math.sin(angle)
 def p(u,v,zz):return(x+u*c-v*s,y+u*s+v*c,zz)
 m.faces([p(-w/2,0,z),p(w/2,0,z),p(0,0,z+h)],[(0,1,2)],ma)
 m.box((x,y,z),(w+.4,.4,.28),STONE,angle)
 for sign in [-1,1]:
  # sloped cornice, a rectangular prism transformed in facade plane
  a=Vector(p(sign*w/2,-.15,z));b=Vector(p(0,-.15,z+h));edge=b-a;side=Vector((-s,c,0))*.22;perp=edge.cross(side).normalized()*.14
  m.faces([tuple(q) for q in [a-side-perp,a+side-perp,b+side-perp,b-side-perp,a-side+perp,a+side+perp,b+side+perp,b-side+perp]],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(0,3,7,4),(1,5,6,2)],STONE)
def roundwindow(m,x,y,z,r,angle=0,clock=False):
 co,si=math.cos(angle),math.sin(angle)
 for radius,dep,ma in [(r+.16,0,STONE),(r,-.09,IRON if clock else GLASS)]:
  m.faces([(x+radius*math.cos(i*math.tau/32)*co-dep*si,y+radius*math.cos(i*math.tau/32)*si+dep*co,z+radius*math.sin(i*math.tau/32)) for i in range(32)],[tuple(range(32))],ma)
 for i in range(12 if clock else 2):
  a=i*math.tau/12 if clock else i*math.pi/2
  if clock:
   u=.78*r*math.sin(a);zz=z+.78*r*math.cos(a);m.box((x+u*co+.15*si,y+u*si-.15*co,zz),(.06,.08,.15),GOLD,angle)
  else:m.box((x+.14*si,y-.14*co,z),(r*1.9 if i else .07,.08,.07 if i else r*1.9),FRAME,angle)
 if clock:
  m.box((x+.16*si,y-.16*co,z+r*.23),(.07,.08,r*.55),GOLD,angle)
  m.box((x+r*.20*co+.16*si,y+r*.20*si-.16*co,z),(r*.45,.08,.07),GOLD,angle)
site=json.load(open(R/'source/site.json'));buildings={b['id']:b for b in site['buildings']}
# Ground and square, kept separate so collision never seals off the plaza.
m=Mesh('SM_Ground','Ground');m.box((0,5,-.38),(290,290,.6),GROUND);m.finish()
m=Mesh('SM_Stortorget_Paving','Ground');m.box((9.5,20,-.12),(99,106,.20),COBBLE)
# Precisely flush smooth walking strips, as seen crossing the rough stone fields.
for x,w in [(-31,2.8),(10,3.5),(51,2.8)]:m.box((x,19,.005),(w,105,.08),PATH)
for y,w in [(-24,3),(17,3),(68,3)]:m.box((9.5,y,.01),(99,w,.08),PATH)
# Very fine transverse drainage courses.
for y in [-27,-4,20,67]:m.box((9.5,y,.035),(96,.12,.025),BASE)
m.finish()
m=Mesh('SM_Streets','Ground')
for x in [-33,53]:m.box((x,10,-.072),(10,245,.16),GRANITE)
for y in [-4,68,-75]:m.box((0,y,-.071),(270,9,.16),GRANITE)
for x in [-38,58]:m.box((x,8,.01),(1.2,125,.22),PATH)
for y in [-32,73]:m.box((7,y,.01),(91,1.2,.22),PATH)
m.finish()
# Cathedral-specific stone and fenestration; preserve the other buildings.
exec(compile((R/'scripts/exterior_helpers.py').read_text(),str(R/'scripts/exterior_helpers.py'),'exec'))
ordinary_window,ordinary_roundwindow,ordinary_stone=window,roundwindow,STONE
ordinary_copper,ordinary_roof=COPPER,DARKROOF
COPPER,DARKROOF=CHURCHCOPPER,CHURCHROOF
window,roundwindow,STONE=church_window,church_roundwindow,CHURCHSTONE
# Cathedral footprint: sourced from OpenStreetMap.
cat=Mesh('SM_Kalmar_Domkyrka','Landmarks');p=buildings['38319501']['polygon'];cat.prism(p,0,1.3,BASE);# Hollow perimeter walls with a traversable south doorway.
for i,(ax,ay) in enumerate(p):
 bx,by=p[(i+1)%len(p)];dx,dy=bx-ax,by-ay;ln=math.hypot(dx,dy);ang=math.atan2(dy,dx)
 if ay<26 and by<26:
  for l,r in [(ax,8.65),(11.55,bx)]:
   if r>l:cat.box(((l+r)/2,(ay+by)/2+.40,7.25),(r-l,.8,11.9),OCHRE)
  cat.box((10.1,(ay+by)/2+.40,9.8),(2.9,.8,6.8),OCHRE)
 else:cat.box(((ax+bx)/2-dy/ln*.4,(ay+by)/2+dx/ln*.4,7.25),(ln,.8,11.9),OCHRE,ang)
cx,cy=10.1,44.4
# Lower facade trims follow actual footprint.
for i,a in enumerate(p):
 b=p[(i+1)%len(p)];dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy);ang=math.atan2(dy,dx)
 for z,t in ([(11.8,.45),(13,.45)] if a[1]<26 and b[1]<26 else [(1.4,.3),(11.8,.45),(13,.45)]):cat.box(((a[0]+b[0])/2,(a[1]+b[1])/2,z),(ln+.12,.4,t),STONE,ang)
# Cross-shaped upper church and intersecting gable roof, verified against aerial reference.
# The upper cross is a shell, keeping the 23 m interior clear.
for side in [-1,1]:
 cat.box((cx,cy+side*17.375,18.45),(22,.65,10.5),OCHRE)
 cat.box((cx+side*25.075,cy,18.45),(.65,16,10.5),OCHRE)
 for other in [-1,1]:
  cat.box((cx+side*10.675,cy+other*12.85,18.45),(.65,9.7,10.5),OCHRE)
  cat.box((cx+side*18.2,cy+other*7.675,18.45),(14.4,.65,10.5),OCHRE)
ze,zr=23.8,27.8
# Eight non-overlapping roof planes meet at the central crossing.
for sign in [-1,1]:
 yy=cy+sign*18.0
 for side in [-1,1]:
  xx=cx+side*11.35
  cat.faces([(cx,cy,zr),(cx,yy,zr),(xx,yy,ze),(xx,cy+sign*8.3,ze)],[(0,1,2,3)],DARKROOF)
 xx=cx+sign*25.7
 for side in [-1,1]:
  yy=cy+side*8.3
  cat.faces([(cx,cy,zr),(xx,cy,zr),(xx,yy,ze),(cx+sign*11.35,yy,ze)],[(0,1,2,3)],DARKROOF)
# Narrow seams and ridge caps make the roof construction readable.
cat.box((cx,cy,zr+.03),(.12,36.1,.10),DARKROOF)
cat.box((cx,cy,zr+.03),(51.5,.12,.10),DARKROOF)
# Curved lower side roofs follow the measured facade instead of floating
# trapezoids. Their outer eaves land exactly on the footprint.
def footprint_y_at(x):
 hits=[]
 for i,(ax,ay) in enumerate(p):
  bx,by=p[(i+1)%len(p)]
  if min(ax,bx)<=x<=max(ax,bx) and abs(bx-ax)>.0001:hits.append(ay+(by-ay)*(x-ax)/(bx-ax))
 return min(hits),max(hits)
for sx in [-1,1]:
 for sy in [-1,1]:
  verts=[];nu,nv=40,22
  for i in range(nu+1):
   x=cx+sx*(11.05+(25.5-11.05)*i/nu);bounds=footprint_y_at(x);outer=bounds[0] if sy<0 else bounds[1]
   for j in range(nv+1):
    t=j/nv;y=(cy+sy*8.0)*(1-t)+outer*t;z=13.35+9.95*(1-t)**.60
    verts.append((x,y,z))
  cat.faces(verts,[(i*(nv+1)+j,(i+1)*(nv+1)+j,(i+1)*(nv+1)+j+1,i*(nv+1)+j+1) for i in range(nu) for j in range(nv)],DARKROOF,True)
  # Close the narrow returns between the upper front and tower piers.
  cat.box((cx+sx*11.13,cy+sy*16.9,18.45),(.65,2.1,10.3),OCHRE)
# Curved roofs above the projecting east/west apses, following each
# polygon segment. These close the last exposed interior ceiling ledges.
for sign in [-1,1]:
 for k,(ax,ay) in enumerate(p):
  bx,by=p[(k+1)%len(p)]
  if min(sign*(ax-cx),sign*(bx-cx))<25.3:continue
  verts=[];nu,nv=8,22
  for i in range(nu+1):
   q=i/nu;xo=ax+(bx-ax)*q;yo=ay+(by-ay)*q;yi=cy+max(-7.9,min(7.9,yo-cy))
   for j in range(nv+1):
    t=j/nv;verts.append(((cx+sign*25.25)*(1-t)+xo*t,yi*(1-t)+yo*t,13.35+1.10*(1-t)**.60))
  cat.faces(verts,[(i*(nv+1)+j,(i+1)*(nv+1)+j,(i+1)*(nv+1)+j+1,i*(nv+1)+j+1) for i in range(nu) for j in range(nv)],DARKROOF,True)
# East/west upper gables, with fenestration instead of exposed roof wedges.
for side in [-1,1]:
 xx=cx+side*25.4;aa=-math.pi/2 if side==-1 else math.pi/2
 for yy in [cy-5.4,cy,cy+5.4]:window(cat,xx,yy,18.0,2.2,5.6,aa,True,STONE,3)
 for yy in [cy-7.4,cy-2.8,cy+2.8,cy+7.4]:cat.box((xx,yy,18.5),(.5,.65,9.2),STONE)
 pediment(cat,xx+side*.1,cy,23.8,16.8,4.0,OCHRE,aa)
# South and north fronts, paired pilasters and tall window stacks.
for side in [-1,1]:
 y=25.85 if side==-1 else 62.9;angle=0 if side==-1 else math.pi
 for x in [cx-10.5,cx-6,cx+6,cx+10.5]:
  cat.box((x,y,7),(0.80,.56,10.6),CHURCHPIER);cat.box((x,y,1.8),(1.1,.72,.45),STONE);cat.box((x,y,11.9),(1.25,.78,.5),STONE)
 for x in [cx-7.7,cx+7.7]:window(cat,x,y+side*.16,5.4,2.0,5.1,angle,False,STONE,3);window(cat,x,y+side*.16,10.1,1.65,1.65,angle,False,STONE,3)
 if side==1:cat.box((cx,y+side*.30,3.6),(2.45,.40,4.7),GREEN)
 else:
  # Open double door leaves, folded inward against the jambs.
  for door_side in [-1,1]:cat.box((cx+door_side*1.38,y+.8,3.75),(.13,1.35,4.7),GREEN)
 for x in [cx-1.65,cx+1.65]:cat.box((x,y+side*.25,3.5),(.45,.7,5.2),STONE)
 cat.box((cx,y+side*.25,6.2),(4.0,.7,.48),STONE);roundwindow(cat,cx,y+side*.22,9.4,1.25,angle)
 for i in range(7):cat.box((cx,y+side*(.5+i*.35),.095*(7-i)),(4.6+i*.12,.72,.19*(7-i)),STONE)
 upper_y=cy+side*17.55
 for x in [cx-10.3,cx-4,cx+4,cx+10.3]:
  cat.box((x,upper_y,18.5),(.7,.6,9.3),STONE);cat.box((x,upper_y,22.9),(1.15,.8,.45),STONE)
 for x in [cx-7,cx,cx+7]:
  if x==cx:window(cat,x,upper_y+side*.1,18.15,3.4,5.7,angle,True,STONE,4)
  elif side==-1:
   # Contemporary south photographs show glazed side bays; the historic
   # elevation depicts their former blind niches.
   window(cat,x,upper_y+side*.1,17.8,2.08,4.4,angle,True,STONE,4,arch_rise=1.04)
   cat.box((x,upper_y+side*.26,21.72),(1.5,.21,.37),STONE)
   cat.box((x,upper_y+side*.29,21.72),(1.17,.23,.15),OCHRE)
  else:
   # Blind arched niches, verified in the 1910 south elevation and photographs.
   cat.box((x,upper_y+side*.21,17.8),(2.45,.13,4.7),STONE)
   cat.box((x,upper_y+side*.29,17.8),(2.08,.08,4.40),OCHRE)
   for r,ma,depth in [(1.23,STONE,.21),(1.04,OCHRE,.3)]:
    cat.faces([(x+r*math.cos(i*math.pi/32),upper_y+side*depth,20.10+r*math.sin(i*math.pi/32)) for i in range(33)],[tuple(range(33))],ma)
   cat.box((x,upper_y+side*.28,22.02),(2.6,.45,.25),STONE)
   cat.box((x,upper_y+side*.26,21.55),(1.5,.21,.42),STONE)
 cat.box((cx,upper_y,23.5),(23.2,.8,.6),STONE);pediment(cat,cx,upper_y+side*.1,23.8,23,4.0,angle=angle)
 # Profiled urns on square plinths replace the provisional conical spikes.
 for x in [cx-11.5,cx,cx+11.5]:
  z=24.0 if x!=cx else 27.85
  facade_finial(cat,x,upper_y,z,1.0)
# Four characteristic squat corner towers with green copper lanterns.
for x in [cx-14.4,cx+14.4]:
 for y in [cy-13.1,cy+13.1]:
  cat.box((x,y,18),(6.5,6.5,9.3),OCHRE)
  for xx in [x-3,x+3]:
   for yy in [y-3,y+3]:cat.box((xx,yy,18),(.6,.6,9.4),STONE)
  for z in [13.5,22.55]:cat.box((x,y,z),(7.2,7.2,.5),STONE)
  for side in [-1,1]:
   yy=y+side*3.32;aa=0 if side==-1 else math.pi
   window(cat,x,yy,17,1.65,2.8,aa,False,STONE,2);roundwindow(cat,x,yy,20.6,.8,aa,clock=(side==-1 and x<cx and y<cy))
  copper_lantern(cat,x,y)
  pass # Detailed flaming urns are added in build_church_details.py.
# Lower side wings and apses, with windows anchored to each actual facade segment.
for i,(x1,y1) in enumerate(p):
 x2,y2=p[(i+1)%len(p)];dx,dy=x2-x1,y2-y1;length=math.hypot(dx,dy)
 if length<3 or (-2<(x1+x2)/2<22 and length>15):continue
 angle=math.atan2(dy,dx);nx,ny=math.sin(angle),-math.cos(angle)
 # The cathedral OSM ring is counterclockwise.
 for t in [.12,.88]:
  xx=x1+t*dx+nx*.10;yy=y1+t*dy+ny*.10
  cat.box((xx,yy,6.4),(.55,.42,9.9),CHURCHPIER,angle)
  cat.box((xx,yy,11.5),(.8,.6,.4),STONE,angle)
 xx=(x1+x2)/2+nx*.12;yy=(y1+y2)/2+ny*.12
 window(cat,xx,yy,5.1,min(1.75,length*.28),4.8,angle,False,STONE,3)
 window(cat,xx,yy,10,min(1.5,length*.24),1.25,angle,False,STONE,3)
# Stone foundation blocks as actual joints.
for i in range(25):
 x=cx-24+i*2
 for z in [.38,.92]:cat.box((x,cy-13.7,z),(1.85,.18,.45),STONE if i%4==0 else BASE)
roof_seams(cat)
curved_roof_seams(cat)
cat.finish()
window,roundwindow,STONE=ordinary_window,ordinary_roundwindow,ordinary_stone
COPPER,DARKROOF=ordinary_copper,ordinary_roof
exec(compile((R/'scripts/build_interior.py').read_text(),str(R/'scripts/build_interior.py'),'exec'))
exec(compile((R/'scripts/build_church_details.py').read_text(),str(R/'scripts/build_church_details.py'),'exec'))
# Surrounding buildings; detailed street frontages replace their initial masses.
exec(compile((R/'scripts/build_town_base.py').read_text(),str(R/'scripts/build_town_base.py'),'exec'))
exec(compile((R/'scripts/build_town_details.py').read_text(),str(R/'scripts/build_town_details.py'),'exec'))
# Street furniture; all independent from building collisions.
m=Mesh('SM_Street_Furniture','Props')
for x,y in [(-24,19),(35,19),(-25,-18),(38,-18),(-23,65),(41,65)]:
 for xx in [-1.5,1.5]:m.box((x+xx,y,.40),(.12,.55,.8),IRON)
 for i in range(5):m.box((x,y-.30+i*.15,.85),(3.4,.12,.10),WOOD)
 for i in range(3):m.box((x,y+.36,1.08+i*.16),(3.4,.09,.12),WOOD)
for x in [-28,48]:
 for y in [-26,-14,-2,10,22,66]:m.cylinder(x,y,0,.12,.82,IRON,12);m.cylinder(x,y,.77,.17,.08,IRON,12)
# Three tall slender lighting masts, one of the square's distinctive contemporary features.
for x,y in [(-11,-11),(33,-9),(45,19)]:
 m.cylinder(x,y,0,.10,13,STONE,12,r2=.06);m.cylinder(x,y,13,.32,.24,IRON,12);m.cylinder(x,y,13.24,.16,.7,WHITE,12,r2=.08)
# Traditional lanterns around the rim.
for x,y in [(-32,-26),(-32,9),(-32,62),(52,-27),(52,62)]:
 m.lathe(x,y,0,[(.22,0),(.22,.4),(.12,.55),(.085,3.8),(.22,3.9),(.3,4.1),(.25,4.6),(.4,4.7),(.05,5.0)],IRON,12)
 m.box((x,y,4.33),(.35,.35,.5),CREAM)
for x,y in [(-29,-20),(-29,3),(-29,26),(47,-22),(47,1)]:
 m.box((x,y,.5),(1.0,1.0,1.0),IRON)
 m.lathe(x,y,1.0,[(.1,0),(.58,.12),(.63,.5),(.50,.9),(.05,1.1)],LEAF,12)
# Flush stone wells/drains, no invented ornamental fountain.
for x,y in [(-9,7),(30,2)]:
 m.cylinder(x,y,.046,.75,.055,BASE,32);m.cylinder(x,y,.11,.55,.014,IRON,32)
 for i in range(-3,4):m.box((x+i*.12,y,.13),(.025,.85,.018),BASE)
m.finish()
# Café furniture at hotel entrance.
m=Mesh('SM_Cafe_Terrace','Props')
for x in [51,54]:
 for y in [-22,-17,-12]:
  m.cylinder(x,y,.72,.5,.055,WOOD,20);m.cylinder(x,y,0,.045,.75,IRON,8)
  for dy in [-.85,.85]:
   m.box((x,y+dy,.43),(.40,.42,.06),WOOD)
   for dx in [-.16,.16]:m.box((x+dx,y+dy,.22),(.045,.36,.44),IRON)
m.finish()
# Scene assembly and exports.
exec(compile((R/'scripts/clean_sculpture_mesh.py').read_text(),str(R/'scripts/clean_sculpture_mesh.py'),'exec'))
clean_sculpture_mesh(bpy.data.objects['SM_Domkyrka_Altar_Carving'].data)
exec(compile((R/'scripts/partition_for_lumen.py').read_text(),str(R/'scripts/partition_for_lumen.py'),'exec'))
# Expand the authored square only when the corridor source is available.
if (R/'source/storgatan.json').exists():
 exec(compile((R/'scripts/build_storgatan.py').read_text(),str(R/'scripts/build_storgatan.py'),'exec'))
if (R/'source/kvarnholmen.json').exists():
 exec(compile((R/'scripts/build_kvarnholmen.py').read_text(),str(R/'scripts/build_kvarnholmen.py'),'exec'))
objects=[o for o in scene.objects if o.type=='MESH'];exports=R/'exports/meshes';exports.mkdir(exist_ok=True)
manifest={'units':'metres','origin_wgs84':site['origin'],'rotation_degrees':28.2,'assets':[],'materials':specs,'cameras':[]}
for obj in objects:
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 # Explicit geometry stays in world coordinates. UE uses X=local X, Y=-local Y, Z=up.
 if obj.name.startswith('SM_Kvarnholmen_') or obj.name in globals().get('sodra_names',[])+globals().get('street16_names',[])+globals().get('district17_names',[]):
  exec(compile((R/'scripts/district_tangent_export.py').read_text(),'district_tangent_export.py','exec'))
  export_district_fbx(obj,exports/(obj.name+'.fbx'))
 else:
  bpy.ops.export_scene.fbx(filepath=str(exports/(obj.name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',use_tspace=obj.name in globals().get('larm_names',[]),add_leaf_bones=False,path_mode='AUTO')
 manifest['assets'].append({'name':obj.name,'file':'meshes/'+obj.name+'.fbx','category':obj['category'],'materials':[m.name for m in obj.data.materials],'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons)})
# Sun, ambient sky and three review cameras.
world=bpy.data.worlds.new('Kalmar_Daylight');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.62,.75,1,1);world.node_tree.nodes['Background'].inputs[1].default_value=.55;scene.world=world
bpy.ops.object.light_add(type='SUN',location=(0,0,80));sun=bpy.context.object;sun.name='Sun_Afternoon';sun.rotation_euler=(math.radians(35),math.radians(-25),math.radians(-35));sun.data.energy=3.0;sun.data.angle=.10
bpy.ops.object.light_add(type='AREA',location=(10,-25,50));bpy.context.object.data.energy=2500;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=80
cameras=[('01_Stortorget',(-22,-24,2.0),(10,42,12),24),('02_Overview',(-83,-101,82),(8,18,5),46),('03_Radhuset',(4,15,2.1),(21,-34,7),24),('04_Domkyrkan',(5,-7,1.75),(10,44,13),24),('05_Interiör_Altare',(-8,44.4,3.1),(34,44.4,9),20),('06_Interiör_Orgel',(20,44.4,3.1),(-12,44.4,10),20),('07_Stadshotellet',(17,-4,2.0),(59,-8,11),25),('08_Kyrkoportal',(8,18,2.0),(10.1,25.4,4.8),33),('09_Altardetalj',(20,39,5.8),(32.4,44.4,9.5),22),('10_Orgel_Läktare',(4,43,3.5),(-12,44.4,9),24),('11_Taköversikt',(-33,2,48),(10,44,16),40),('12_Altarskulptur',(27,49.8,4.5),(31.8,48.8,4.5),42),('13_Predikstol',(10,41,4.1),(18.2,50.7,6.4),28)]
cameras += [('20_Sydportal',(6.9,16.5,2.3),(10.1,25.4,5.3),31),('21_Fasad_Stenverk',(-3,18,8.2),(2.4,25.6,9.3),38),('22_Sydfasad',(6,-21,2.8),(10.1,39,14.7),30),('16_Predikstol_Infästning',(10,45,3.2),(19.2,52.3,7),23),('17_Psalmtavla_Infästning',(-2.6,47.3,5.9),(-.5,51.8,6.15),42),('18_Exteriör_Fasad',(-14,3,5.0),(10,40,16),38),('19_Tornhuv',(-18,14,31),(-4.3,31.3,25.8),50),('14_Bänksnickeri',(-5.8,44.1,2.40),(-3.5,42.7,2.02),48),('15_Joniskt_Kapitäl',(18.7,46.5,13.5),(20.7,51.65,14.05),52)]
cameras += town_cameras
if 'extension_cameras' in globals():cameras += extension_cameras
if 'district_cameras' in globals():cameras += district_cameras
for name,loc,target,lens in cameras:
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name=name;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.data.clip_end=1500
 manifest['cameras'].append({'name':name,'location':loc,'target':target,'lens':lens})
manifest['total_vertices']=sum(x['vertices'] for x in manifest['assets']);manifest['total_polygons']=sum(x['polygons'] for x in manifest['assets'])
json.dump(manifest,open(R/'exports/manifest.json','w'),indent=2)
scene.render.engine='CYCLES';scene.render.threads_mode='FIXED';scene.render.threads=6;scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
scene.camera=bpy.data.objects['01_Stortorget']
# Save a usable material-preview viewport.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_distance=140;area.spaces.active.region_3d.view_location=(10,18,3);area.spaces.active.clip_end=2000
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
if '--no-render' not in sys.argv:
 for name,_,_,_ in (cameras[4:] if '--interior-render' in sys.argv else cameras[:3]):
  scene.camera=bpy.data.objects[name];scene.render.filepath=str(R/'previews'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('STORTORGET_BUILD_OK',len(objects),manifest['total_vertices'],manifest['total_polygons'])
