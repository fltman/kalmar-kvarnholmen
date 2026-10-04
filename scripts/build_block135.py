"""Pass 135: Kalmar slott, portal G (the south range's south-west courtyard portal) and Kungsköket,
the king's kitchen (Olsson's room 43, ground floor of the east range; corrects passes 27, 124, 126,
127, 129 and 133).

- SM_Castle124_Portals: portal G, 'sydvästra portalen' (Olsson 1957: fluted Doric columns, masks in
  the metopes, framing the walled-up south gate passage), on the SW courtyard front at the window
  column s 10.27, 4.2 m from the west courtyard corner: pedestals, a fluted column on each side, a
  round arch with a keystone console, an entablature with triglyphs and masks, a projecting cornice
  (3.74 m wide, 4.40 m high; the 1960 museum photograph 021017057393 and Street View 2014 pano 2).
  The passage behind the arch is walled up: a 0.30 m reveal, a double plank door and the blind
  masonry behind it.
- SM_Kalmar_Slott: G's arch is cut through the courtyard skin (pass 126's open arch, as portals E and
  F), the lower-row window it covers goes and the middle-row window over it stands on its cornice;
  SE_w's two small arched courtyard doors (pass 129) are drawn open: they are Kungsköket's exits.
- SM_Castle124_Paving: re-created with the composition (no change).
- New SM_Castle135_Kungskoket: the kitchen in pass 27's SE_w range, from the south tower's corner to
  the wall under Förbrända salen's south end (16.6 x 9.0-10.5 m): cobbled floor at z 5.10, three steps
  down in each exit's niche, whitewashed walls with the niches of the facade's two lower rows (the
  courtyard's low and high windows of the 1969 photographs) and of the outer front's small windows, a
  cross wall with a wide arch, the great hearth under it (a brick stack with arched openings on every
  face and a tapering hood into the arch's crown), a smaller arched fireplace with a hood in the south
  wall, the drain along the north wall, a short stair in the north wall to a closed door, dense dark
  joists and a board ceiling at z 11.18-11.55.
- New SM_Castle135_KungskoketInventarier: iron trammel bars and pot hooks across the hearth's arches,
  cauldrons, the guard rail along the drain (1969 photographs), a work table with benches and a
  stack of firewood.
Method: pass 133's composition (build_block133.py's slice, which re-runs pass 129's composition of
passes 124-129) runs again in a private namespace with this pass's single, asserted replacements.
Sources: references/block135-notes.md.
"""
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B135D=json.loads((R/'source/block135.json').read_text())
block135_names=[];B135={}
for old in [k for k in list(materials) if k.startswith('M_Block135_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Lime','TownPaintWhite',(.80,.78,.73),.95,0),('Reveal','TownPaintWhite',(.86,.84,.79),.95,0),   # whitewashed rubble and brick (1969)
 ('Brick','TownTileRed',(.55,.40,.32),.90,0),('Soot','TownStone',(.16,.15,.14),.95,0),
 ('Cobble','TownStone',(.47,.45,.42),.92,0),('Flag','TownStone',(.62,.60,.56),.86,0),('Drain','TownStone',(.34,.33,.31),.92,0),
 ('Joist','TownPaintBrown',(.22,.17,.12),.80,0),('Board','TownPaintBrown',(.32,.25,.18),.80,0),('Plank','TownPaintBrown',(.38,.29,.20),.78,0),
 ('Frame','TownPaintWhite',(.86,.86,.83),.60,0),('Iron','TownMetalGrey',(.17,.17,.18),.55,.6),('Oak','TownPaintBrown',(.42,.31,.20),.72,0),
 ('Log','TownPaintBrown',(.45,.36,.26),.90,0),
 ('PortalStone','TownStone',(.58,.56,.52),.86,0),('PortalDoor','TownPaintBrown',(.30,.24,.18),.80,0),('Infill','TownStone',(.52,.50,.47),.90,0),
 ]:
 name='M_Block135_'+key;B135[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block135_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M135=B135

def rep135(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)
def drop_degenerate_faces135(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark135(obj,corrects):
 obj['block135_dropped_faces']=drop_degenerate_faces135(obj)
 obj['detail_pass']=135;obj['reference_notes']='references/block135-notes.md'
 if corrects:obj['corrects_pass']=corrects
 if obj.name not in block135_names:block135_names.append(obj.name)
 print('BLOCK135_MESH',obj.name,obj.get('corrects_pass',''),'dropped',obj['block135_dropped_faces'],len(obj.data.polygons))
 return obj
PG135=dict(B135D['portal_g'])

# ================================================================= pass 133's composition (passes 124-129 and 133), re-run
_SRC133=(R/'scripts/build_block133.py').read_text()
_e133="print('BLOCK133_PASS129_REBUILT',NS133['block127_names'])\n"
S135=_SRC133[_SRC133.index('def rep133(src,old,new):'):_SRC133.index(_e133)+len(_e133)]
# Marking: the re-created meshes are pass 135's.
S135=rep135(S135," obj['detail_pass']=133;obj['reference_notes']='references/block133-notes.md'\n if corrects:"," obj['detail_pass']=135;obj['reference_notes']='references/block135-notes.md'\n if corrects:")
S135=rep135(S135,"obj['detail_pass']=133;obj['reference_notes']='references/block133-notes.md';obj['osm_way']=osm","obj['detail_pass']=135;obj['reference_notes']='references/block135-notes.md';obj['osm_way']=osm")
S135=rep135(S135,"'27,124,126,127,128,129' if obj.name=='SM_Kalmar_Slott' else '124,126,129'","'27,124,126,127,128,129,133' if obj.name=='SM_Kalmar_Slott' else '124,126,129,133'")
S135=rep135(S135,"assert _o['detail_pass']==133","assert _o['detail_pass']==135")
S135=rep135(S135,"print('BLOCK133_MESH',","print('BLOCK135_MESH',")
S135=rep135(S135,_e133,"print('BLOCK135_PASS133_REBUILT',NS133['block127_names'])\n")
# Portal G's arch joins Kyrkportalen's door on the SW courtyard edge CI2-CI1.
S135=rep135(S135,"=[list(DOOR133)]\n","=[list(DOOR133),list(B135D['portal_g']['door'])]\n")
# This pass's edits on the composed source, after pass 133's.
S135=rep135(S135,"SRC133=rep133(SRC133,\"holes=filt127(holes) if z0==ZC else holes;\",\"holes=filt133(filt127(holes)) if z0==ZC else holes;\")\n",
 "SRC133=rep133(SRC133,\"holes=filt127(holes) if z0==ZC else holes;\",\"holes=filt133(filt127(holes)) if z0==ZC else holes;\")\nSRC133=EDITSRC135(SRC133)\n")
S135=rep135(S135,"NSC133['edit_portals129']=edit_portals133\n","NSC133['edit_portals129']=EP135(edit_portals133)\n")
S135=rep135(S135,"edit_portals129=edit_portals133,","edit_portals129=EP135(edit_portals133),")
def EDITSRC135(src):
 # SE_w's two courtyard doors (Kungsköket's exits) and portal G's arch are drawn open, as portal E and F.
 src=rep135(src,"  if (u,b,w,h,r) in OPEN133:arch_open126","  if (u,b,w,h,r) in OPEN133 or (u,b,w,h,r) in OPEN135:arch_open126")
 # The middle-row window over portal G stands on its cornice (pass 127's rule removed it with the arch).
 src=rep135(src,"holes=filt133(filt127(holes)) if z0==ZC else holes;","holes=filt135(holes,filt133(filt127(holes))) if z0==ZC else holes;")
 src=rep135(src,"exec(compile(EXTRA133,'build_block133.py:pass27_helpers','exec'),NS124);",
  "exec(compile(EXTRA133,'build_block133.py:pass27_helpers','exec'),NS124);exec(compile(EXTRA135,'build_block135.py:pass27_helpers','exec'),NS124);")
 return src
EXTRA135='''
OPEN135=[tuple(h) for h in B135D['open_doors']]
def filt135(orig,holes):
 # On the SW courtyard edge (portal G's arch), the middle-row window on G's axis returns, its sill on
 # G's cornice (the 1960 photograph); the lower-row window behind the portal stays out.
 g=tuple(B135D['portal_g']['door'])
 if g not in [tuple(h) for h in orig]:return holes
 top=ZC+B135D['portal_g']['top']+.02;have=[tuple(h) for h in holes];out=list(holes)
 for h in orig:
  if tuple(h) in have:continue
  if abs(h[0]-g[0])<.05 and h[1]>top-.1:out.append((h[0],round(max(h[1],top),3),h[2],round(h[1]+h[3]-max(h[1],top),3),h[4]))
 return out
'''
PORT135='''
def prism_uo135(m,prof,o0,o1,x,y,a,ma):
 # A flat (u,z) shape in a facade frame, extruded from out o0 to o1; caps triangulated (no n-gons).
 n=len(prof);v=[lp(x,y,u,o,z,a) for o in (o0,o1) for u,z in prof]
 tris=tessellate_polygon([[Vector((u,z,0)) for u,z in prof]])
 m.faces(v,[(t[0],t[1],t[2]) for t in tris]+[(t[2]+n,t[1]+n,t[0]+n) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def portal_g135(m):
 # Portal G (the 1960 museum photograph 021017057393; Olsson 1957): a fluted column on each side on a
 # tall pedestal, a round arch with impost blocks and a keystone console, an architrave, a frieze of
 # triglyphs with masks between them and a projecting cornice. The passage behind is walled up: a
 # reveal, the double plank door with its boarded head, and the blind masonry behind.
 P=PG135;x,y,L,a=sf_edge(CI124[2],CI124[1]);u=P['u'];z=ZC124;W_=P['width'];S=M135['PortalStone']
 ow,oh,orr=P['open_w'],P['open_h'],P['open_r'];cu=P['col_u']
 arc=lambda r_,k=16:[(u+r_*math.cos(math.pi*i/k),z+oh+r_*math.sin(math.pi*i/k)) for i in range(k+1)]
 zt=z+P['col'][1]
 # the stone field round the arch, from the face to 0.145 out (it covers the facade's own arch trim)
 for s in (-1,1):
  u0,u1=sorted((u+s*(ow/2+.24),u+s*W_/2))
  prism_uo135(m,[(u0,z),(u1,z),(u1,zt),(u0,zt)],O124-.005,O124+.145,x,y,a,S)
 prism_uo135(m,[(u+ow/2+.24,z+oh),(u+ow/2+.24,zt),(u-ow/2-.24,zt),(u-ow/2-.24,z+oh)]+[(px,pz) for px,pz in arc(orr+.24)][1:-1][::-1],O124-.005,O124+.145,x,y,a,S)
 # jambs, imposts and the arch ring (with the voussoirs' face proud of the field)
 for s in (-1,1):
  fb124(m,x,y,u+s*(ow/2+.12),.26,z,z+oh-.14,.24,S,a)
  fb124(m,x,y,u+s*(ow/2+.15),.30,z+oh-.14,z+oh,.34,S,a)
 ring_=arc(orr,20);outer=arc(orr+.24,20)
 prism_uo135(m,outer+ring_[::-1],O124+.10,O124+.24,x,y,a,S)
 fb124(m,x,y,u,.36,z+oh+orr-.08,zt,.30,S,a)                                    # keystone console
 fb124(m,x,y,u,.42,zt-.16,zt,.40,S,a)
 # pedestals, columns and capitals
 for s in (-1,1):
  uu=u+s*cu
  fb124(m,x,y,uu,.62,z,z+P['plinth'],P['ped_w']+.14,S,a)
  fb124(m,x,y,uu,.55,z+P['ped'][0],z+P['ped'][1],P['ped_w'],S,a)
  fb124(m,x,y,uu,.62,z+P['ped_cap'][0],z+P['ped_cap'][1],P['ped_w']+.12,S,a)
  column124(m,x,y,uu,O124+.30,z+P['ped_cap'][1],P['col'][1]-P['ped_cap'][1]-.17,P['col_r'],a,S)
  fb124(m,x,y,uu,.52,zt-.17,zt,.50,S,a)
 # entablature: architrave, frieze with triglyphs and masks, cornice
 a0,a1=P['arch_t'];f0,f1=P['frieze'];c0,c1=P['cornice']
 fb124(m,x,y,u,.50,z+a0,z+a1,W_,S,a);fb124(m,x,y,u,.44,z+f0,z+f1,W_-.10,S,a)
 n=P['triglyphs'];du=(W_-.40)/(n-1)
 for k in range(n):fb124(m,x,y,u-W_/2+.20+k*du,.48,z+f0+.02,z+f1-.02,.17,S,a)
 for k in range(n-1):
  um=u-W_/2+.20+(k+.5)*du;fb124(m,x,y,um,.50,z+f0+.10,z+f1-.10,.17,S,a);fb124(m,x,y,um,.53,z+f0+.15,z+f1-.15,.09,S,a)   # masks
 fb124(m,x,y,u,.62,z+c0,z+c1-.10,W_+.20,S,a);fb124(m,x,y,u,.72,z+c1-.10,z+c1,W_+.34,S,a)
 # the walled-up passage: reveal (jambs and soffit) behind the arch, the blind masonry, the door
 rv,rd,inf=.30,P['recess'],P['infill'];ztop=z+oh+orr+rv
 prism_uo135(m,[(u-ow/2-rv,z),(u-ow/2,z)]+arc(orr)[::-1]+[(u+ow/2,z),(u+ow/2+rv,z),(u+ow/2+rv,ztop),(u-ow/2-rv,ztop)],-rd,.01,x,y,a,S)
 fb124(m,x,y,u,inf,z-.05,ztop,ow+2*rv,M135['Infill'],a,-rd-inf)
 for s in (-1,1):fb124(m,x,y,u+s*(ow/4),.06,z+.02,z+oh,ow/2-.03,M135['PortalDoor'],a,-rd)
 fb124(m,x,y,u,.09,z+oh-.06,z+oh+.04,ow,M135['PortalDoor'],a,-rd)
 fan_prism124(m,(u,z+oh+.04),[(u+(orr-.02)*math.cos(math.pi*i/12),z+oh+.04+(orr-.06)*math.sin(math.pi*i/12)) for i in range(13)],-rd,-rd+.05,x,y,a,M135['PortalDoor'])
 for s in (-1,1):
  for zz in (.45,1.55):fb124(m,x,y,u+s*(ow/4),.02,z+zz,z+zz+.06,ow/2-.20,M135['Iron'],a,-rd+.06)   # strap hinges
'''
def EP135(f):
 def g(t):
  # After pass 133's edits: portal G is drawn with the other portals (no slab path: the passage is walled up).
  t=f(t)
  t=rep135(t,"_doors={",PORT135+"_doors={")
  _w="WX124,WY124=CA124['well']\n";assert t.count(_w)==1
  i=t.index(_w);j=t.rindex("b124_finish(m)\n",0,i)
  return t[:j]+"portal_g135(m)   # pass 135\n"+t[j:]
 return g
NSP135=dict(globals());NSP135.update(block133_names=[],B133D=json.loads((R/'source/block133.json').read_text()))
NSP135['B133']={k:'M_Block133_'+k for k in ('Plaster','Step','Flag','Oak','Stone','PortalStone','PortalTablet')};NSP135['M133']=NSP135['B133']
assert all(v in materials for v in NSP135['B133'].values())
exec(compile(S135,'build_block133.py:composition (pass 135 edits)','exec'),NSP135)
assert NSP135['NS133']['block127_names']==['SM_Kalmar_Slott','SM_Castle124_Portals','SM_Castle124_Paving'],NSP135['NS133']['block127_names']
for _n in NSP135['NS133']['block127_names']:
 _o=bpy.data.objects[_n];assert _o['detail_pass']==135,(_n,_o['detail_pass'])
 if _n not in block135_names:block135_names.append(_n)

# ================================================================= Kungsköket
K135=B135D['kitchen'];FR135=B135D['frame'];O135,U135,N135=FR135['origin'],FR135['u'],FR135['n']
def W135(s,c):return (O135[0]+U135[0]*s+N135[0]*c,O135[1]+U135[1]*s+N135[1]*c)
def _lin135(p,q):return lambda s:p[1]+(q[1]-p[1])*(s-p[0])/(q[0]-p[0])
CL135=_lin135(*K135['cl']);OL135=_lin135(*K135['ol'])
def CF135(s):return CL135(s)+K135['t_cw']
def OF135(s):return OL135(s)-K135['t_ow']
def prism135(m,ring,z0,z1,ma):
 # A closed prism over a ring (world x,y): triangulated caps (no large n-gons), quad sides.
 pts=[tuple(p) for p in ring];n=len(pts)
 if z1-z0<.002 or n<3:return
 v=[(x,y,z0) for x,y in pts]+[(x,y,z1) for x,y in pts]
 tris=tessellate_polygon([[Vector((x,y,0)) for x,y in pts]])
 m.faces(v,[(t[2],t[1],t[0]) for t in tris]+[(t[0]+n,t[1]+n,t[2]+n) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def sb135(m,s0,s1,c0,c1,z0,z1,ma):
 # A box in the SE_w frame; c0/c1 may be functions of s (a wall face).
 f0=c0 if callable(c0) else (lambda s,v=c0:v);f1=c1 if callable(c1) else (lambda s,v=c1:v)
 prism135(m,[W135(s0,f0(s0)),W135(s1,f0(s1)),W135(s1,f1(s1)),W135(s0,f1(s0))],z0,z1,ma)
def plane135(m,prof,axis,a0,a1,ma):
 # A flat shape in a vertical plane of the frame, extruded: axis 's' -> prof is (c,z), extruded over s;
 # axis 'c' -> prof is (s,z), extruded over c. Caps triangulated.
 n=len(prof);P=(lambda h,z,a:(*W135(a,h),z)) if axis=='s' else (lambda h,z,a:(*W135(h,a),z))
 v=[P(h,z,a) for a in (a0,a1) for h,z in prof]
 tris=tessellate_polygon([[Vector((h,z,0)) for h,z in prof]])
 m.faces(v,[(t[0],t[1],t[2]) for t in tris]+[(t[2]+n,t[1]+n,t[0]+n) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def frustum135(m,s0,s1,c0,c1,z0,t0,t1,d0,d1,z1,ma):
 # A tapering hood: base (s0..s1, c0..c1) at z0, top (t0..t1, d0..d1) at z1.
 hexa124(m,[(*W135(s0,c0),z0),(*W135(s1,c0),z0),(*W135(s1,c1),z0),(*W135(s0,c1),z0)],[(*W135(t0,d0),z1),(*W135(t1,d0),z1),(*W135(t1,d1),z1),(*W135(t0,d1),z1)],ma)
def notch135(h0,h1,zb,zs,k=12):
 # A round-headed opening from zb: up the left side, over the semicircle, down the right side.
 r=(h1-h0)/2;hc=(h0+h1)/2
 return [(h0,zb),(h0,zs)]+[(hc-r*math.cos(math.pi*i/k),zs+r*math.sin(math.pi*i/k)) for i in range(1,k)]+[(h1,zs),(h1,zb)]
def b135_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 return Mesh(name,category)
ZF135,ZB135,ZC135=K135['zf'],K135['zb'],B135D['zc']
def kitchen135():
 # Built inside a function so that no short name reaches the shared namespace.
 m=b135_new('SM_Castle135_Kungskoket','Kalmar slott/Interiör')
 # Walls: the four pieces in horizontal bands, with the niches, the exits and the stair cut out.
 for b in K135['bands']:prism135(m,b['ring'],b['z0'],b['z1'],M135['Lime'])
 # Floor: cobbles; the exits' landing and two treads; the drain along the north wall.
 prism135(m,K135['floor'],ZB135,ZF135,M135['Cobble'])
 for st in K135['steps']:prism135(m,st['ring'],ZB135,st['top'],M135['Flag'])
 D=K135['drain'];sb135(m,D['s0'],D['s1'],D['c0'],D['c1'],ZB135,D['z'],M135['Drain'])
 for c0,c1 in ((D['c0'],D['c0']+.10),(D['c1']-.10,D['c1'])):sb135(m,D['s0'],D['s1'],c0,c1,ZB135,ZF135,M135['Flag'])
 # The stair in the north wall: four steps up to a landing and a closed plank door.
 ST=K135['stair'];SN=K135['s'][2]
 for k in range(ST['n']):sb135(m,SN-.03+k*ST['tread'],ST['door_s'],ST['c0'],ST['c1'],ZB135,round(ZF135+(k+1)*ST['rise'],3),M135['Flag'])
 _zl=ZF135+ST['n']*ST['rise'];sb135(m,ST['door_s'],ST['door_s']+.06,ST['c0']+.04,ST['c1']-.04,_zl,_zl+2.05,M135['Plank'])
 # Window frames at the back of each niche (pass 27's glass stands in the skin behind them).
 for ni in K135['niches']:
  s=ni['s'];w=ni['w'];z0,z1=ni['sill'],ni['head']
  if ni['wall']=='court':cb=lambda s_:CL135(s_)+.03;ce=lambda s_:CL135(s_)+.09
  else:cb=lambda s_:OL135(s_)-.09;ce=lambda s_:OL135(s_)-.03
  for s0,s1,zz0,zz1 in ((s-w/2,s-w/2+.07,z0,z1),(s+w/2-.07,s+w/2,z0,z1),(s-w/2,s+w/2,z0,z0+.07),(s-w/2,s+w/2,z1-.07,z1),(s-.03,s+.03,z0,z1),(s-w/2,s+w/2,(z0+z1)/2-.03,(z0+z1)/2+.03)):
   sb135(m,s0,s1,cb,ce,zz0,zz1,M135['Frame'])
 # The exits: the leaf stands open against the niche's side.
 for e in K135['exits']:
  s=e['s']+K135['door_niche_w']/2-.02
  sb135(m,s-.06,s,lambda s_:CL135(s_)+.10,lambda s_:CL135(s_)+.10+e['w']+.05,ZC135+.03,ZC135+2.15,M135['Plank'])
 # The cross wall with its wide arch ('mellanväggens valv'), up to the joists.
 A=K135['arch'];_hw=(A['c1']-A['c0'])/2;_ch=(A['c0']+A['c1'])/2
 _t0=math.atan2(A['spring']-A['zo'],-_hw);_t1=math.atan2(A['spring']-A['zo'],_hw)
 _arc=[(_ch+A['R']*math.cos(_t0+(_t1-_t0)*i/24),A['zo']+A['R']*math.sin(_t0+(_t1-_t0)*i/24)) for i in range(1,24)]
 plane135(m,[(A['cw0'],ZB135),(A['c0'],ZB135),(A['c0'],A['spring'])]+_arc+[(A['c1'],A['spring']),(A['c1'],ZB135),(A['cw1'],ZB135),(A['cw1'],K135['z_ju']),(A['cw0'],K135['z_ju'])],'s',A['s0'],A['s1'],M135['Lime'])
 # The great hearth under the arch: a brick stack with two arched openings on the long faces and one on
 # the short faces, a fire bed inside, the tapering hood into the arch's crown, and the flue in the wall.
 H=K135['hearth'];hs,hc,t=H['hs'],H['hc'],H['t'];SH,CH=H['s'],H['c']
 sb135(m,SH-hs-H['plinth'],SH+hs+H['plinth'],CH-hc-H['plinth'],CH+hc+H['plinth'],ZB135,H['zp'],M135['Flag'])
 _sn=[(CH-hc,H['zp'])]+[p for a0,a1 in H['arches_sn'] for p in notch135(CH+a0,CH+a1,H['zp'],H['spring'])]+[(CH+hc,H['zp']),(CH+hc,H['top']),(CH-hc,H['top'])]
 for s0 in (SH-hs,SH+hs-t):plane135(m,_sn,'s',s0,s0+t,M135['Brick'])
 _ew=[(SH-hs+t,H['zp'])]+notch135(SH+H['arch_ew'][0],SH+H['arch_ew'][1],H['zp'],H['spring_ew'])+[(SH+hs-t,H['zp']),(SH+hs-t,H['top']),(SH-hs+t,H['top'])]
 for c0 in (CH-hc,CH+hc-t):plane135(m,_ew,'c',c0,c0+t,M135['Brick'])
 sb135(m,SH-hs+t,SH+hs-t,CH-hc+t,CH+hc-t,H['zp'],H['bed'],M135['Soot'])
 sb135(m,SH-hs+t,SH+hs-t,CH-hc+t,CH+hc-t,H['top']-.04,H['top'],M135['Soot'])
 frustum135(m,SH-hs,SH+hs,CH-hc,CH+hc,H['top'],SH-H['hood_hs'],SH+H['hood_hs'],CH-H['hood_hc'],CH+H['hood_hc'],H['hood_top'],M135['Lime'])
 sb135(m,SH-H['hood_hs'],SH+H['hood_hs'],CH-H['hood_hc'],CH+H['hood_hc'],H['hood_top']-.02,A['crown']+.10,M135['Lime'])
 # The smaller fireplace in the south wall's west part: an arched breast, a fire bed, a hood to the joists.
 FI=K135['fire'];SS=K135['s'][1];fc,fh=FI['c'],FI['hc']
 plane135(m,[(fc-fh,ZF135)]+notch135(fc+FI['open'][0],fc+FI['open'][1],ZF135,FI['spring'])+[(fc+fh,ZF135),(fc+fh,FI['top']),(fc-fh,FI['top'])],'s',SS-.02,SS+FI['d'],M135['Brick'])
 sb135(m,SS,SS+FI['d']-.05,fc+FI['open'][0]+.05,fc+FI['open'][1]-.05,ZF135-.02,ZF135+.22,M135['Soot'])
 sb135(m,SS-.02,SS+.03,fc+FI['open'][0],fc+FI['open'][1],ZF135+.22,FI['spring']+.8,M135['Soot'])
 frustum135(m,SS-.02,SS+FI['d'],fc-fh,fc+fh,FI['top'],SS-.02,SS+FI['flue_d'],fc-FI['flue_hc'],fc+FI['flue_hc'],K135['z_ju']+.02,M135['Lime'])
 # The ceiling: dense dark joists across the range on the walls and the cross wall, boards above.
 for sj in K135['joists']:sb135(m,sj-.11,sj+.11,lambda s_:CF135(s_)-.05,lambda s_:OF135(s_)+.05,K135['z_ju'],K135['z_bu'],M135['Joist'])
 prism135(m,K135['room'],K135['z_bu'],K135['z_top'],M135['Board'])
 _o=s21_finish(m);_o['osm_way']='';mark135(_o,None)

 return H,D,SH,CH,hs,hc
def furnish135(H,D,SH,CH,hs,hc):
 # ---------------------------------------------------------------- the furnishings
 m=b135_new('SM_Castle135_KungskoketInventarier','Kalmar slott/Interiör')
 # Iron trammel bars across the hearth's arches with pot hooks (1969: 'Spisens södra sida').
 for sg in (-1,1):
  sf=SH+sg*(hs+.04)
  for a0,a1 in H['arches_sn']:
   zb=H['spring']+.04;town_rod(m,(*W135(sf,CH+a0-.06),zb),(*W135(sf,CH+a1+.06),zb),.018,M135['Iron'],6)
   for f in (.3,.7):
    cc=CH+a0+(a1-a0)*f;town_rod(m,(*W135(sf,cc),zb),(*W135(sf,cc),zb-.32),.008,M135['Iron'],6)
    town_rod(m,(*W135(sf,cc),zb-.32),(*W135(sf-sg*.06,cc),zb-.38),.008,M135['Iron'],6)
 # Cauldrons: one on the fire bed, one on the floor by the hearth's east face.
 for (s_,c_,z_,k) in ((SH,CH-.9,H['bed'],1.0),(SH-hs-.75,CH+hc-.45,ZF135,.8)):
  X,Y=W135(s_,c_);poly_lathe(m,X,Y,z_,[(.08*k,0),(.24*k,.03),(.32*k,.16*k),(.32*k,.34*k),(.29*k,.40*k),(.25*k,.40*k)],M135['Iron'],12)
 # The guard rail along the drain (1969 photographs): posts and two rails.
 _rs=D['s0']-.10;_cs=[D['c0']+.15+k*(D['c1']-D['c0']-.3)/4 for k in range(5)]
 for c_ in _cs:sb135(m,_rs-.05,_rs+.05,c_-.05,c_+.05,ZF135,ZF135+1.0,M135['Oak'])
 for zz in (.55,.95):sb135(m,_rs-.03,_rs+.03,_cs[0]-.05,_cs[-1]+.05,ZF135+zz-.04,ZF135+zz+.04,M135['Oak'])
 # A work table with two benches by the outer wall, south of the hearth.
 _tc=lambda s_:OF135(s_)-1.55
 for s0 in (3.4,6.4):
  for dc in (.10,.70):sb135(m,s0,s0+.10,lambda s_,d=dc:_tc(s_)+d,lambda s_,d=dc:_tc(s_)+d+.10,ZF135,ZF135+.80,M135['Oak'])
 sb135(m,3.2,6.7,_tc,lambda s_:_tc(s_)+.90,ZF135+.80,ZF135+.88,M135['Oak'])
 for dc0,dc1 in ((-.55,-.25),(1.15,1.45)):
  sb135(m,3.3,6.6,lambda s_,d=dc0:_tc(s_)+d,lambda s_,d=dc1:_tc(s_)+d,ZF135+.42,ZF135+.47,M135['Oak'])
  for s0 in (3.4,6.4):sb135(m,s0,s0+.08,lambda s_,d=dc0:_tc(s_)+d+.04,lambda s_,d=dc1:_tc(s_)+d-.04,ZF135,ZF135+.42,M135['Oak'])
 # Firewood stacked against the courtyard wall between a window niche and the south exit.
 for row in range(3):
  for k in range(5-row):
   z_=ZF135+.08+row*.14;s_=7.35+row*.07+k*.15
   town_rod(m,(*W135(s_,CF135(s_)+.08),z_),(*W135(s_,CF135(s_)+.68),z_),.07,M135['Log'],7)
 _o=s21_finish(m);_o['osm_way']='';mark135(_o,None)

furnish135(*kitchen135())

# ================================================================= cameras
def sv_camera135(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def look135(name,s,c,h,ds,dc,pitch,vfov):
 x,y=W135(s,c);vx,vy=U135[0]*ds+N135[0]*dc,U135[1]*ds+N135[1]*dc
 return sv_camera135(name,x,y,h,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
_sw=PG135['sw']
def WS135(s,c):return (_sw['origin'][0]+_sw['u'][0]*s+_sw['n'][0]*c,_sw['origin'][1]+_sw['u'][1]*s+_sw['n'][1]*c)
_gx,_gy=WS135(PG135['s'],PG135['line_c']-.355)
_p2=(-860.06,-308.67);_hg=math.degrees(math.atan2(_gx-_p2[0],_gy-_p2[1]))-28.2
# The 1960 photograph's camera, from the projective fit (prepare_block135.py), with its distance set on
# sandbox run 2: 9.6 m in front of the face, 2.6 m beyond the left column (towards the south corner),
# turned 27.8 degrees to the right of square on, 3.1 degrees up, 2.1 m over the paving (the photographer
# stands on snow); f 991 px on the 927 px high scan (vfov 50.1).
_cx,_cy=WS135(PG135['s']+PG135['col_u']+2.64,PG135['line_c']-.355-9.6)
_hn=math.degrees(math.atan2(_sw['n'][0],_sw['n'][1]))
block135_cameras=[
 # 735: Street View 2014 pano 2 (jOXzkLldNOjrveyz1T81wg, pass 128's resected camera, heading offset
 # -2.65) at portal G: URL heading = true heading + 2.65.
 sv_camera135('735_Block135_Cal_Pano2_PortalG',_p2[0],_p2[1],ZC135+1.9,_hg,5,40),
 sv_camera135('736_Block135_Cal_Photo1960_PortalG',_cx,_cy,ZC135+2.1,_hn+27.8-28.2,3.1,50.1),
 # 737: the hearth under the cross wall's arch from the north part (1969: 'Spisens norra del', 090089).
 look135('737_Block135_Kungskoket_Hearth',16.9,-5.0,ZF135+1.5,-1,-.18,9,64),
 # 738: the west (courtyard) wall's south part with the southern exit and both window rows (1969, 090101).
 look135('738_Block135_Kungskoket_WestWall',8.6,-2.4,ZF135+1.5,-.12,-1,8,66),
 ('739_Block135_Aerial_SouthCourtyard',W135(14,-40)+(46.0,),W135(8,-10)+(8.0,),26),
]
print('BLOCK135_GEOMETRY',len(block135_names))
