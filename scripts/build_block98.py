"""Pass 98: the mainland between Kvarnholmen and the castle, which until now stood alone in water:
- the ground of the shore between Västerport and Kalmarsundsparken, with a bank down to the water;
- Slottsvägen and the other streets in asphalt, the park and cemetery paths in gravel;
- Stadsparken (the castle park), the Krusenstjernska garden, Kalmarsundsparken and the smaller
  greens, with their trees (the OpenStreetMap trees plus an even scatter);
- Gamla kyrkogården and Södra kyrkogården: lawns, rows of headstones and slabs, clipped hedges along
  their bounds;
- the houses of the blocks round them as plain volumes: storeys from OpenStreetMap, windows per
  storey, hipped roofs on compact plans and flat roofs on large or irregular ones.

This pass is context at street-plan accuracy, not measured architecture: no panorama was used. Data:
source/block98.json (from references/osm-slott98.json, ODbL); see references/block98-notes.md.
"""
import hashlib,random
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
B98D=json.loads((R/'source/block98.json').read_text())
block98_names=[];B98={}
for old in [k for k in list(materials) if k.startswith('M_Block98_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grass','TownStone',(.33,.43,.22),.95,0),('Lawn','TownStone',(.38,.50,.26),.95,0),('Common','TownStone',(.45,.48,.30),.95,0),
 ('Flower','TownStone',(.55,.35,.40),.95,0),('Bank','TownStone',(.40,.44,.30),.95,0),('Asphalt','TownMetalGrey',(.20,.20,.21),.90,0),
 ('Gravel','TownStone',(.62,.58,.52),.95,0),('Stone','TownStone',(.52,.51,.50),.85,0),('StoneDark','TownStone',(.32,.32,.33),.80,0),
 ('Hedge','TownStone',(.18,.30,.15),.95,0),('Bark','TownPaintBrown',(.25,.20,.16),.90,0),('Leaf','TownStone',(.24,.36,.17),.95,0),
 ('LeafLight','TownStone',(.33,.46,.21),.95,0),
 ('Ochre','TownIvory',(.86,.75,.52),.88,0),('White','TownIvory',(.92,.91,.87),.88,0),('PaleYellow','TownIvory',(.92,.86,.64),.88,0),
 ('RedBoard','TownIvory',(.58,.20,.16),.85,0),('Grey','TownIvory',(.66,.66,.64),.88,0),('Brick','TownTileRed',(.55,.30,.22),.90,0),
 ('PaleGreen','TownIvory',(.74,.80,.70),.88,0),('Frame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Tile','TownTileRed',(.62,.32,.24),.80,0),('DarkRoof','TownMetalGrey',(.27,.27,.29),.60,.25),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block98_'+key;B98[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block98_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B98;ZG=0.30
def b98_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block98_names.append(name);return Mesh(name,category)
def drop_degenerate_faces98(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b98_finish(m,osm=''):
 obj=s21_finish(m);drop_degenerate_faces98(obj);obj['detail_pass']=98;obj['reference_notes']='references/block98-notes.md';obj['osm_way']=osm;return obj
def surf98(m,piece,z,ma):
 rings=[piece['outer']]+piece.get('holes',[]);flatv=[(x,y) for r in rings for x,y in r]
 for t in tessellate_polygon([[Vector((x,y,0)) for x,y in r] for r in rings]):
  v=[(flatv[i][0],flatv[i][1],z) for i in t]
  if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
  m.faces(v,[(0,1,2)],ma)

# ---------------------------------------------------------------- ground
m=b98_new('SM_Slott98_Ground','Slottsområdet/Ground')
for p in B98D['land']:surf98(m,p,ZG,M['Grass'])
for sh in B98D['shore']:
 for p,q in zip(sh,sh[1:]):
  L=math.dist(p,q)
  if L<.05:continue
  nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
  m.faces([(*p,ZG),(*q,ZG),(q[0]+nx*2.5,q[1]+ny*2.5,-1.7),(p[0]+nx*2.5,p[1]+ny*2.5,-1.7)],[(0,1,2,3),(3,2,1,0)],M['Bank'])
b98_finish(m,'90822660')
m=b98_new('SM_Slott98_Streets','Slottsområdet/Streets')
for p in B98D['roads']:surf98(m,p,ZG+.03,M['Asphalt'])
for p in B98D['paths']:surf98(m,p,ZG+.025,M['Gravel'])
b98_finish(m)
m=b98_new('SM_Slott98_Greens','Slottsområdet/Parks')
KG={'park':'Lawn','garden':'Lawn','village_green':'Lawn','grass':'Lawn','common':'Common','grassland':'Common','scrub':'Common','flowerbed':'Flower'}
for g in B98D['greens']:
 for p in g['pieces']:surf98(m,p,ZG+(.018 if g['kind']=='flowerbed' else .01),M[KG.get(g['kind'],'Lawn')])
b98_finish(m)

# ---------------------------------------------------------------- the cemeteries
m=b98_new('SM_Slott98_Cemeteries','Slottsområdet/Cemeteries')
for c in B98D['cemeteries']:
 for p in c['pieces']:surf98(m,p,ZG+.012,M['Lawn'])
 for e in c['edge']:
  for p,q in zip(e,e[1:]+e[:1]):
   L=math.dist(p,q)
   if L<.6:continue
   x,y,_,a=sf_edge(p,q);mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2;inx,iny=-math.sin(a)*.6,math.cos(a)*.6
   m.box((mx+inx,my+iny,ZG+.7),(L+.3,1.0,1.4),M['Hedge'],a)
for x,y,ang,kind in B98D['graves']:
 a=math.radians(ang)
 if kind==0:m.box((x,y,ZG+.40),(.62,.14,.80),M['Stone'],a)
 elif kind==1:m.box((x,y,ZG+.50),(.50,.16,1.0),M['StoneDark'],a)
 else:m.box((x,y,ZG+.13),(.95,.55,.26),M['Stone'],a)
b98_finish(m,'24455361')

# ---------------------------------------------------------------- trees
m=b98_new('SM_Slott98_Trees','Slottsområdet/Vegetation')
for i,(x,y,s) in enumerate(B98D['trees']):
 rng=random.Random(98000+i);h=rng.uniform(9.5,13.5)*s;r=rng.uniform(3.4,4.8)*s;trunk=h*.40;z0=ZG
 m.lathe(x,y,z0,[(.24,0),(.20,.4),(.16,trunk*.6),(.13,trunk)],M['Bark'],8)
 cz=z0+trunk+(h-trunk)*.52
 blob79(m,(x,y,cz),(r*.85,r*.85,(h-trunk)*.46),M['Leaf'],10,6)
 for k in range(3):
  a=rng.uniform(0,math.tau);d=rng.uniform(.35,.65)*r;rr=r*rng.uniform(.38,.55)
  blob79(m,(x+math.cos(a)*d,y+math.sin(a)*d,cz+rng.uniform(-.2,.35)*(h-trunk)*.5),(rr,rr,rr*.8),M['LeafLight'] if k%2 else M['Leaf'],8,5)
b98_finish(m)

# ---------------------------------------------------------------- buildings
WALLS=['Ochre','White','PaleYellow','RedBoard','Grey','Brick','PaleGreen','White','Ochre','PaleYellow']
def frame98(ring):
 # Frame of the longest edge: the plan boxed in it, and how much of that box the plan fills.
 e=max(zip(ring,ring[1:]+ring[:1]),key=lambda pq:math.dist(*pq));L=math.dist(*e);d=((e[1][0]-e[0][0])/L,(e[1][1]-e[0][1])/L);n=(-d[1],d[0]);o=e[0]
 ss=[(v[0]-o[0])*d[0]+(v[1]-o[1])*d[1] for v in ring];ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for v in ring]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 ar=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))/2
 ap=sum(ring[i][0]*ring[(i+1)%len(ring)][1]-ring[(i+1)%len(ring)][0]*ring[i][1] for i in range(len(ring)))/2
 if ar<0:r=r[::-1]
 return r,max(ss)-min(ss),max(ts)-min(ts),abs(ap)/max(abs(ar),1e-6)
chunks={}
for b in B98D['buildings']:
 cx=sum(v[0] for v in b['outer'])/len(b['outer']);key='W' if cx<-1150 else ('M' if cx<-850 else 'E')
 chunks.setdefault(key,[]).append(b)
for key,group in sorted(chunks.items()):
 m=b98_new('SM_Slott98_Buildings_'+key,'Slottsområdet/Buildings')
 for b in group:
  ring=[tuple(v) for v in b['outer']];h=int(hashlib.sha256(b['id'].encode()).hexdigest()[:6],16)
  levels=b['levels'];H=b['height'] or (levels*3.0+.5);H=max(2.6,min(H,28.0))
  wm=M[WALLS[h%len(WALLS)]] if b['kind'] not in ('garage','shed','garages') else M['Grey']
  for p,q in zip(ring,ring[1:]+ring[:1]):
   if math.dist(p,q)<.3:continue
   w={'p':list(p),'q':list(q),'z0':0.0}
   if levels<=0 or H<3.2 or b['kind'] in ('garage','garages','shed','roof'):bz_wall(m,w['p'],w['q'],0,H,[],wm)
   else:plain(m,w,H,wm,M['Frame'],M['Frame'],levels,ZG+.9)
  r,Ls,Lt,fill=frame98(ring)
  if fill>.9 and min(Ls,Lt)<16 and len(ring)<=8:
   inset_roof(m,r,H,min(Ls,Lt)/2-.30,min(Ls,Lt)/2*.62,M['Tile'] if h%3 else M['DarkRoof'],.35)
  else:
   m.faces([(*v,H) for v in ring],[tuple(range(len(ring))),tuple(range(len(ring)-1,-1,-1))],M['DarkRoof'])
   for p,q in zip(ring,ring[1:]+ring[:1]):
    L=math.dist(p,q)
    if L<.3:continue
    x,y,_,a=sf_edge(p,q);facade_box(m,x,y,0,.20,H+.3,L+.2,.25,.6,wm,a)
 b98_finish(m)

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block98_cameras=[('486_Block98_Aerial_Castle',(-700.0,-420.0,120.0),(-900.0,-150.0,2.0),24),('487_Block98_Aerial_Park',(-760.0,120.0,90.0),(-900.0,-60.0,2.0),24),
 ('488_Block98_Aerial_Cemetery',(-1000.0,-330.0,70.0),(-1110.0,-170.0,2.0),24)]
print('BLOCK98_GEOMETRY',len(block98_names))
