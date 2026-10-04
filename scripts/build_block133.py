"""Pass 133: Kalmar slott, Kyrkportalen (portal F) at its true place, and the way up to Slottskyrkan
(corrects passes 27, 124, 126, 127, 129 and 130).

- Portal F (Kyrkportalen, 1568) moves from the middle of the SW courtyard front (pass 124, s 17.9) to
  the window column 2.4 m from the south corner (s 25.47; Street View 2014 pano 2 square on, the
  2017 courtyard photograph, pass 129), and is rebuilt after Olsson 1957 and the panorama: paired
  fluted Doric columns on pedestals, a triglyph entablature, four herms with the cartouche between
  them, a second entablature and the segmental arms tablet, 4.2 m wide and 4.94 m high.
- SM_Kalmar_Slott: pass 27's middle door on the SW courtyard edge goes; F's door is cut open at the
  portal (1.4 m, springing 1.46 m) and is open. The lower-row window it meets goes (pass 127's
  no-window-over-door rule); the middle-row window over the portal sits on the tablet (0.64 m high, as
  in the panorama and the 2017 photograph). The windows at the old door's place return.
- SM_Castle124_Portals and SM_Castle124_Paving: portal F rebuilt at its place; the slab path follows.
- SM_Castle130_Slottskyrkan: re-created with its two door leaves taken out. The altar door opens on
  the stair hall, the west door on Gröna salen (pass 131's door opposite has no leaf of its own).
- New SM_Castle133_Kyrktrappan: Sydöstra vindelstenen, the stair hall beyond the chapel's altar wall
  (Kalmar läns museum's plan över praktvåningen, room 13), reached from Kyrkportalen through a
  vestibule and a flight under the chancel: 30 risers of 0.176 m (14 along the courtyard wall, a half
  landing, 16 across the range as the museum plan draws them) to a landing at the altar door, level
  with the chancel (z 10.75).
Method: pass 129's composition (build_block129.py's slice, which itself composes passes 124-128) runs
again in a private namespace with this pass's single, asserted replacements; pass 130's shell section
runs again in its own namespace with its materials mapped by name. Sources: references/block133-notes.md.
"""
import re
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B133D=json.loads((R/'source/block133.json').read_text())
block133_names=[];B133={}
for old in [k for k in list(materials) if k.startswith('M_Block133_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownPaintWhite',(.87,.85,.80),.94,0),('Step','TownStone',(.72,.70,.66),.82,0),('Flag','TownStone',(.64,.62,.58),.85,0),
 ('Oak','TownPaintBrown',(.30,.22,.15),.70,0),('Stone','TownStone',(.76,.74,.69),.84,0),
 ('PortalStone','TownStone',(.58,.56,.52),.86,0),('PortalTablet','TownStone',(.50,.48,.45),.86,0),   # Kyrkportalen's weathered grey stone (pano 2, 2017)
 ]:
 name='M_Block133_'+key;B133[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block133_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M133=B133

def rep133(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)
def drop_degenerate_faces133(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark133(obj,corrects):
 obj['block133_dropped_faces']=drop_degenerate_faces133(obj)
 obj['detail_pass']=133;obj['reference_notes']='references/block133-notes.md'
 if corrects:obj['corrects_pass']=corrects
 if obj.name not in block133_names:block133_names.append(obj.name)
 print('BLOCK133_MESH',obj.name,obj.get('corrects_pass',''),'dropped',obj['block133_dropped_faces'],len(obj.data.polygons))
 return obj

PF133=dict(B133D['portal']);DOOR133=tuple(B133D['door']);ST133=B133D['stair']

# ================================================================= pass 129's composition (passes 124-129), re-run
_SRC129=(R/'scripts/build_block129.py').read_text()
NSC133=dict(globals());NSC133.update(B129D=json.loads((R/'source/block129.json').read_text()),B128D=json.loads((R/'source/block128.json').read_text()))
exec(compile(_SRC129[_SRC129.index('def rep129(src,old,new):'):_SRC129.index('NS129=dict(globals());')],'build_block129.py:composition','exec'),NSC133)
SRC133=NSC133['SRC129']
# Marking: the re-created meshes are pass 133's.
SRC133=rep133(SRC133," obj['detail_pass']=129;obj['reference_notes']='references/block129-notes.md';obj['osm_way']=osm\n",
 " obj['detail_pass']=133;obj['reference_notes']='references/block133-notes.md';obj['osm_way']=osm\n")
SRC133=rep133(SRC133,"return mark127(obj,'27,124,126,127,128' if obj.name=='SM_Kalmar_Slott' else '124,126',osm)",
 "return mark127(obj,'27,124,126,127,128,129' if obj.name=='SM_Kalmar_Slott' else '124,126,129',osm)")
# This pass's helpers run in pass 27's namespace after pass 129's.
SRC133=rep133(SRC133,"exec(compile(EXTRA129,'build_block129.py:pass27_helpers','exec'),NS124);",
 "exec(compile(EXTRA129,'build_block129.py:pass27_helpers','exec'),NS124);exec(compile(EXTRA133,'build_block133.py:pass27_helpers','exec'),NS124);")
# Kyrkportalen's door is drawn open (pass 126's open arch, as at portal E).
SRC133=rep133(SRC133,"  if (u,b,w,h,r) in ARCHUP129:arch_door27(m,x,y,u,b,w,h,r,a)\\n",
 "  if (u,b,w,h,r) in OPEN133:arch_open126(m,x,y,u,b,w,h,r,a)\\n  elif (u,b,w,h,r) in ARCHUP129:arch_door27(m,x,y,u,b,w,h,r,a)\\n")
# The middle-row window over the portal stands on its tablet.
SRC133=rep133(SRC133,"holes=filt127(holes) if z0==ZC else holes;","holes=filt133(filt127(holes)) if z0==ZC else holes;")
EXTRA133='''
OPEN133=[tuple(B133D['door'])]
def filt133(holes):
 # On the SW courtyard edge (the one with Kyrkportalen's open door) the middle-row window over the
 # portal starts on the portal's tablet: same head (z 11.10), sill 0.05 m above the tablet.
 if not any(tuple(h) in OPEN133 for h in holes):return holes
 mw=B133D['midwin'];out=[]
 for h in holes:
  if abs(h[0]-mw['u'])<.05 and abs(h[1]-mw['b0'])<.01:h=(h[0],mw['b'],h[2],round(mw['head']-mw['b'],3),h[4])
  out.append(h)
 return out
'''
# Pass 27's courtyard door on SW (its middle-door rule) gives way to Kyrkportalen's door.
B129D133=json.loads((R/'source/block129.json').read_text());B129D133['doors']['%d,%d'%tuple(B133D['edge'])]=[list(DOOR133)]
PORT133='''
def portal_f133(m,x,y,u,z,a):
 # Kyrkportalen (Olsson 1957, fig. 10; pano 2 of 2014, square on): paired fluted Doric columns on
 # pedestals either side of the round-arched door, an entablature with triglyphs, four herms on Ionic
 # capitals with the cartouche of Johan III's initials and 1568 between them, a second entablature,
 # and the segmental tablet with the arms. Heights from the panorama, scaled per front.
 P=PF133;W=P['width']
 ow,oh,orr=P['open_w'],P['open_h'],P['open_r']
 for s in (-1,1):                                                                    # the back plates beside the door
  fb124(m,x,y,u+s*(ow/2+.24+(W-.2-ow-.48)/4),.10,z,z+P['ent1'][0],(W-.2-ow-.48)/2,M133['PortalStone'],a)
 for s in (-1,1):
  for du in P['col_u']:
   uu=u+s*du
   fb124(m,x,y,uu,.48,z,z+P['ped']-.08,.44,M133['PortalStone'],a);fb124(m,x,y,uu,.52,z+P['ped']-.08,z+P['ped'],.50,M133['PortalStone'],a)
   column124(m,x,y,uu,O124+.26,z+P['col'][0],P['col'][1]-P['col'][0],P['col_r'],a,M133['PortalStone'])
 e0,e1=P['ent1'];ent129(m,x,y,u,z+e0,z+e1,W,a,M133['PortalStone'],.48)
 for k in range(7):fb124(m,x,y,u-W/2+.35+k*(W-.7)/6,.46,z+e0+.36*(e1-e0),z+e0+.69*(e1-e0),.15,M133['PortalStone'],a)   # triglyphs
 h0,h1=P['herm']
 fb124(m,x,y,u,.14,z+h0,z+h1,W-.3,M133['PortalStone'],a)                                           # the herm storey's back
 for s in (-1,1):
  for du in P['herm_u']:
   uu=u+s*du
   v=[lp(x,y,uu+su*wd/2,oo,z+zz,a) for oo in (O124+.14,O124+.34) for su,wd,zz in ((-1,.16,h0+.08),(1,.16,h0+.08),(1,.26,h0+.78),(-1,.26,h0+.78))]
   hexa124(m,v[:4],v[4:],M133['PortalStone'])                                                       # the tapering term
   fb124(m,x,y,uu,.30,z+h0,z+h0+.08,.30,M133['PortalStone'],a)
   fb124(m,x,y,uu,.30,z+h0+.78,z+h0+.86,.30,M133['PortalStone'],a);fb124(m,x,y,uu,.26,z+h0+.86,z+h1-.16,.22,M133['PortalStone'],a,O124+.06)   # bust and head
   fb124(m,x,y,uu,.32,z+h1-.16,z+h1,.38,M133['PortalStone'],a)                                     # Ionic capital
 p0,p1=P['panel'];fb124(m,x,y,u,.22,z+p0,z+p1,P['panel_w'],M133['PortalTablet'],a)
 fb124(m,x,y,u,.06,z+p0+.14,z+p1-.14,P['panel_w']-.36,M133['PortalTablet'],a,O124+.22)       # the cartouche's field
 fb124(m,x,y,u,.05,z+p1-.30,z+p1-.16,.36,M133['PortalTablet'],a,O124+.28)                    # the crown over the initials
 f0,f1=P['ent2'];fb124(m,x,y,u,.42,z+f0,z+f1-.08,W-.1,M133['PortalStone'],a);fb124(m,x,y,u,.52,z+f1-.08,z+f1,W+.1,M133['PortalStone'],a)
 c0,c1=P['cap'];cw=P['cap_w']/2;zb=z+c0+.10;hh=c1-c0-.10;Rr=(cw*cw+hh*hh)/(2*hh);th=math.asin(cw/Rr);zo=zb+hh-Rr
 fb124(m,x,y,u,.30,z+c0,zb,P['cap_w']+.1,M133['PortalStone'],a)
 fan_prism124(m,(u,zb),[(u+Rr*math.sin(th-2*th*k/10),zo+Rr*math.cos(th-2*th*k/10)) for k in range(11)],O124,O124+.26,x,y,a,M133['PortalStone'])
 fb124(m,x,y,u,.05,zb+.06,zb+hh-.10,.42,M133['PortalTablet'],a,O124+.26)                     # the arms (a block)
 for s in (-1,1):fb124(m,x,y,u+s*.48,.05,zb+.04,zb+hh*.55,.30,M133['PortalTablet'],a,O124+.26)   # the lions (blocks)
 for s in (-1,1):fb124(m,x,y,u+s*(ow/2+.12),.22,z,z+oh,.24,M133['PortalStone'],a)
 p18_arch(m,*lp(x,y,u,0,0,a)[:2],z+oh,ow,orr,.20,O124+.06,a,M133['PortalStone'])
'''
_EP129=NSC133['edit_portals129']
def edit_portals133(t):
 # After pass 129's edits: portal F stands at its measured place and is rebuilt; the slab path follows.
 t=_EP129(t)
 t=rep133(t,"_doors={",PORT133+"_doors={")
 t=rep133(t," x,y,L,a=sf_edge(p,q);u,z=(PD129['u'],ZC124+PD129['rise']) if key=='D' else (0.0,ZC124)\n",
  " x,y,L,a=sf_edge(p,q);u,z=(PD129['u'],ZC124+PD129['rise']) if key=='D' else ((PF133['u'],ZC124) if key=='F' else (0.0,ZC124))\n")
 i0=t.index(" else:\n  for s in (-1,1):\n   uu=u+s*1.2\n");_e="fb124(m,x,y,u,.08,z+4.38,z+4.62,.5,M124['Tablet'],a,O124+.3)\n";i1=t.index(_e)+len(_e)
 assert t.count(" else:\n  for s in (-1,1):\n   uu=u+s*1.2\n")==1 and t.count(_e)==1 and t[i0:i1].count('\n')==9,t[i0:i1]
 t=t[:i0]+" else:portal_f133(m,x,y,u,z,a)   # pass 133\n"+t[i1:]
 t=rep133(t,"_targets.append(lp(x,y,PD129['u'] if key=='D' else 0,","_targets.append(lp(x,y,PD129['u'] if key=='D' else (PF133['u'] if key=='F' else 0),")
 return t
NSC133['edit_portals129']=edit_portals133
NS133=dict(globals())
NS133.update(B129D=B129D133,B128D=NSC133['B128D'],EXTRA129=NSC133['EXTRA129'],PORT129=NSC133['PORT129'],PC129=NSC133['PC129'],PD129=NSC133['PD129'],
 cut129=NSC133['cut129'],edit_portals129=edit_portals133,rep129=NSC133['rep129'],B133D=B133D,EXTRA133=EXTRA133,PF133=PF133,PORT133=PORT133)
exec(compile(SRC133,'build_block127.py (pass 128+129+133 edits)','exec'),NS133)
assert NS133['block127_names']==['SM_Kalmar_Slott','SM_Castle124_Portals','SM_Castle124_Paving'],NS133['block127_names']
for _n in NS133['block127_names']:
 _o=bpy.data.objects[_n];assert _o['detail_pass']==133,(_n,_o['detail_pass']);mark133(_o,None)
print('BLOCK133_PASS129_REBUILT',NS133['block127_names'])

# ================================================================= pass 130's chapel shell, its doors open
SRC130=(R/'scripts/build_block130.py').read_text()
_m0=SRC130.index("for old in [k for k in list(materials) if k.startswith('M_Block130_')]")
_keys130=re.findall(r"\('(\w+)','Town\w+',\(",SRC130[_m0:SRC130.index('M130=B130\n')]);assert len(_keys130)==41,len(_keys130)
_b=SRC130[SRC130.index('def b130_new(name,category):'):SRC130.index('# ================================================================= the furnishings')]
_b=rep133(_b," obj['detail_pass']=130;obj['reference_notes']='references/block130-notes.md';obj['osm_way']='';return obj\n",
 " obj['detail_pass']=133;obj['reference_notes']='references/block133-notes.md';obj['osm_way']='';obj['corrects_pass']='130';return obj\n")
# The two leaves go (the surrounds stay): the altar door opens on the stair hall, the west door on Gröna salen.
_l0=" bx130(m,leaf-.025,leaf+.025,c-w/2,c+w/2,zb,zb+hh,M130['Door'])\n";_l1=" bx130(m,leaf-sg*.03,leaf-sg*.025,c-w/2+.25,c-w/2+.32,zb+hh*.48,zb+hh*.50,M130['Brass'])\n"
assert _b.count(_l0)==1 and _b.count(_l1)==1
_i0=_b.index(_l0);_i1=_b.index(_l1)+len(_l1);assert _b[_i0:_i1].count('\n')==6,_b[_i0:_i1]
_b=_b[:_i0]+" pass   # pass 133: the leaf is taken out, the door stands open\n"+_b[_i1:]
NS130_133=dict(globals());NS130_133.update(B130D=json.loads((R/'source/block130.json').read_text()),B130={k:'M_Block130_'+k for k in _keys130},block130_names=[])
NS130_133['M130']=NS130_133['B130']
exec(compile(_b,'build_block130.py:shell (pass 133 edits)','exec'),NS130_133)
assert NS130_133['block130_names']==['SM_Castle130_Slottskyrkan'],NS130_133['block130_names']
mark133(bpy.data.objects['SM_Castle130_Slottskyrkan'],'130')

# ================================================================= Sydöstra vindelstenen and its approach
FR133=B133D['frame'];O133,U133,N133=FR133['origin'],FR133['u'],FR133['n']
def W133(s,c):return (O133[0]+U133[0]*s+N133[0]*c,O133[1]+U133[1]*s+N133[1]*c)
def prism133(m,ring,z0,z1,ma):
 # A closed prism over a counter-clockwise ring: triangulated caps (no large n-gons), quad sides.
 pts=[tuple(p) for p in ring];n=len(pts)
 if z1-z0<.002 or n<3:return
 v=[(x,y,z0) for x,y in pts]+[(x,y,z1) for x,y in pts]
 tris=tessellate_polygon([[Vector((x,y,0)) for x,y in pts]])
 fs=[(t[2],t[1],t[0]) for t in tris]+[(t[0]+n,t[1]+n,t[2]+n) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 m.faces(v,fs,ma)
def _ccw133(r):
 a=sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(r,r[1:]+r[:1]));return r if a>0 else r[::-1]
def sb133(m,s0,s1,c0,c1,z0,z1,ma):
 # A box in the SW range frame (s along the range, c outwards).
 prism133(m,_ccw133([W133(s0,c0),W133(s1,c0),W133(s1,c1),W133(s0,c1)]),z0,z1,ma)
def b133_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 return Mesh(name,category)
m=b133_new('SM_Castle133_Kyrktrappan','Kalmar slott/Interiör')
ZC133,ZB133,RS133=B133D['zc'],ST133['zb'],ST133['rise'];ZCH133=B133D['zch']
# The vestibule inside Kyrkportalen: flags at the courtyard level, and a threshold slab through the door.
sb133(m,ST133['s_v0'],ST133['s_v1'],ST133['c_line']+.04,ST133['c_l1'],ZB133,ZC133+.012,M133['Flag'])
_hw=PF133['open_w']/2;sb133(m,PF133['s']-_hw,PF133['s']+_hw,ST133['c_line']-.03,ST133['c_line']+.04,ZB133,ZC133+.012,M133['Step'])
# Flight 1 along the courtyard wall under the chancel, then the half landing; flight 2 across the range;
# the landing at the altar door. Solid steps from the slab up.
for st in B133D['steps']:prism133(m,st['ring'],ZB133,st['top'],M133['Step'])
prism133(m,B133D['land1'],ZB133,ST133['z_l1'],M133['Flag'])
prism133(m,B133D['land2'],ZB133,ZCH133,M133['Flag'])
# Walls: the spine under the chancel and the hall's west end, the stair hall's walls and the spine
# between its flights (full height), the courtyard-side piece at the south corner, ceilings.
sb133(m,ST133['s_v0']-.20,ST133['s_room0'],ST133['c_l1'],ST133['c_l1']+.20,ZB133,ST133['zceil_low']+.15,M133['Plaster'])
sb133(m,ST133['s_v0']-.20,ST133['s_v0'],ST133['c_line']+.04,ST133['c_l1'],ZB133,ST133['zceil_low']+.15,M133['Plaster'])
sb133(m,ST133['s_v0'],ST133['s_room0'],ST133['c_line']+.04,ST133['c_l1'],ST133['zceil_low'],ST133['zceil_low']+.15,M133['Plaster'])
sb133(m,27.90,ST133['s_room0'],ST133['c_cw']-.25,ST133['c_cw'],ZB133,ST133['zceil_low']+.15,M133['Plaster'])
prism133(m,B133D['walls13'],ZB133,ST133['zceil'],M133['Plaster'])
prism133(m,B133D['spine13'],ZB133,ST133['zceil'],M133['Plaster'])
prism133(m,B133D['env13'],ST133['zceil'],ST133['zceil']+.15,M133['Plaster'])
# The altar door from the stair hall's side: a plain stone surround on the altar wall's back.
_DA=NS130_133['B130D']['doors']['altar'];_s0=ST133['s_room0']
for _c0,_c1 in ((_DA['c']-_DA['w']/2-.16,_DA['c']-_DA['w']/2),(_DA['c']+_DA['w']/2,_DA['c']+_DA['w']/2+.16)):sb133(m,_s0,_s0+.05,_c0,_c1,ZCH133,ZCH133+_DA['h']+.16,M133['Stone'])
sb133(m,_s0,_s0+.05,_DA['c']-_DA['w']/2,_DA['c']+_DA['w']/2,ZCH133+_DA['h'],ZCH133+_DA['h']+.16,M133['Stone'])
# Oak handrails on the spine walls along both flights.
_r1=ST133['s_r1'];_c2=ST133['c_r2']
town_rod(m,(*W133(_r1[0],ST133['c_l1']-.06),ZC133+.9),(*W133(ST133['s_l1'],ST133['c_l1']-.06),ST133['z_l1']+.9),.03,M133['Oak'],6)
town_rod(m,(*W133(ST133['s_l1']+.06,_c2[0]),ST133['z_l1']+.9),(*W133(ST133['s_l1']+.06,ST133['c_l2']),ZCH133+.9),.03,M133['Oak'],6)
_o133=s21_finish(m);_o133['osm_way']='';mark133(_o133,None)

# ================================================================= cameras
def sv_camera133(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def look133(name,s,c,h,ds,dc,pitch,vfov):
 x,y=W133(s,c);vx,vy=U133[0]*ds+N133[0]*dc,U133[1]*ds+N133[1]*dc
 return sv_camera133(name,x,y,h,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
block133_cameras=[
 # 720: Street View 2014 pano 2 (jOXzkLldNOjrveyz1T81wg, pass 128's resected camera, heading offset
 # -2.65) at Kyrkportalen square on: URL 207h, 95t, 40y.
 sv_camera133('720_Block133_Cal_Pano2_PortalF',-860.06,-308.67,ZC133+1.9,204.35,5,40),
 # 721: pano 1 (zCIfieeXGQUNANmWu_Tg9A, offset -1.34) along SW to the south corner: URL 162h, 95t, 60y.
 sv_camera133('721_Block133_Cal_Pano1_PortalF',-885.06,-306.46,ZC133+2.1,160.66,5,60),
 look133('722_Block133_Vestibule',25.2,-8.9,ZC133+1.6,1,.08,18,74),
 look133('723_Block133_AltarDoor',25.0,-3.2,ZCH133+1.6,1,.32,4,66),
 ('724_Block133_Aerial_SouthCorner',W133(10,-40)+(48.0,),W133(27,-6)+(8.0,),24),
]
print('BLOCK133_GEOMETRY',len(block133_names))
