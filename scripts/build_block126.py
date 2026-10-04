"""Pass 126: Kalmar slott. The courtyard is lowered to its real level, the west range's windows are
made to agree with the rooms of pass 125, and Kungstrappan (Olsson's room 55) is built from the
courtyard up to Gyllene salen.

- The courtyard floor goes from 9.50 to 6.80 m above the water (z 8.17 -> 5.47): 31 steps (7 + 24,
  kalmarslott.se) to the state floor at z 10.47 give 0.161 m risers; see references/block126-notes.md.
  Everything standing on it moves with it: pass 27's courtyard cobbles (SM_Castle27_Ground) and
  courtyard fronts (SM_Kalmar_Slott), pass 124's portals C-F, well house and courtyard paving, and the
  gate passage, whose ramp falls from 22 % to 10 %.
- The courtyard's first window row is the state floor's row (sill z 11.57, 3.2 m high).
- The outer main-floor windows of the west front between Kungsmakstornet and Kuretornet are at
  s 6.45 and 14.25 (Zettervall 1883; the 2009 panorama), and Kungsmakstornet's main window faces
  Kungsmaket's west niche. Gyllene salen (pass 125) gets its niches on these axes, a second courtyard
  niche (the 1930s photograph) and an open south-east door.
- New SM_Castle126_Kungstrappan: portal E's door opened, an entry hall, a dog-leg stair of 2 x 15
  risers of 0.167 m, the förstuga (55) over the gate passage, and the door into Gyllene salen.
Re-created meshes keep their names and categories. Pass 124's code (which itself re-runs pass 27's
code in a private namespace) and pass 125's code are run again verbatim in private namespaces with
single, asserted string replacements, as pass 124 did with pass 27.
"""
import re
from mathutils import Vector
# Pass 125 leaves its tower position in the shared names TS and TC, which the town helpers read as
# their stone and copper materials (town_window's trim). Restore them before any helper runs.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B126D=json.loads((R/'source/block126.json').read_text())
block126_names=[];B126={}
for old in [k for k in list(materials) if k.startswith('M_Block126_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownPaintWhite',(.87,.85,.80),.94,0),('Flag','TownStone',(.66,.64,.60),.85,0),('Step','TownStone',(.72,.70,.66),.82,0),
 ('Oak','TownPaintBrown',(.30,.22,.15),.70,0),
 ]:
 name='M_Block126_'+key;B126[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block126_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M126=B126

def drop_degenerate_faces126(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark126(obj,corrects,osm=''):
 obj['block126_dropped_faces']=drop_degenerate_faces126(obj);print('BLOCK126_DROPPED',obj.name,obj['block126_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=126;obj['reference_notes']='references/block126-notes.md';obj['osm_way']=osm
 if corrects:obj['corrects_pass']=corrects
 if obj.name not in block126_names:block126_names.append(obj.name)
 return obj
def rep126(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)

ZC126=B126D['zc'];ZS126=B126D['court_row']['sill'];HS126=B126D['court_row']['h']
TWIN126={B126D['tower_window']['key']:(math.atan2(B126D['tower_window']['dir'][1],B126D['tower_window']['dir'][0]),B126D['tower_window']['w'])}
WIN126=B126D['win_out']

# ================================================================= pass 124 (and through it pass 27), re-run
SRC124=(R/'scripts/build_block124.py').read_text()
_m0=SRC124.index("for old in [k for k in list(materials) if k.startswith('M_Block124_')]")
_keys124=re.findall(r"\('(\w+)','Town\w+',\(",SRC124[_m0:SRC124.index('M124=B124\n')])
assert len(_keys124)==9,_keys124
_s=SRC124[SRC124.index('import ast,re'):_m0]
# Pass 124's materials exist already; deleting and re-creating them would strip the pass 124 meshes
# this pass leaves alone (the approach, the bridge), so they are mapped by name.
_s+="B124={k:'M_Block124_'+k for k in %r}\n"%(_keys124,)
_s+=SRC124[SRC124.index('M124=B124\n'):SRC124.index('# ================================================================= the lifted park at the footbridge (pass 98)')]
_s+=SRC124[SRC124.index('# ================================================================= the gate passage (Kuretornet and the west range)'):SRC124.index('def sv_camera124')]
# Every mesh this run makes is marked as pass 126's (pass 124's own marking is replaced).
_s=rep126(_s,"def b124_finish(m,corrects=None,osm=''):return b124_mark(s21_finish(m),corrects,osm)\n",
 "def b124_mark(obj,corrects=None,osm=''):return mark126(obj,'27,124' if corrects==27 and obj.name!='SM_Castle27_Ground' else ('27' if corrects==27 else '124'),osm)\n"
 "def b124_finish(m,corrects=None,osm=''):return b124_mark(s21_finish(m),corrects,osm)\n")
# 1. The courtyard level, for pass 124's parts and for pass 27's code run inside NS124.
_s=rep126(_s,"ZC124=zh124(HL124['courtyard'])","ZC124=ZC126")
_s=rep126(_s,"ZC=zh(HL['courtyard'])","ZC=ZC126")
# 2. Pass 27's walls are not touched by this pass: instead of them, pass 27's ground section is run
#    (the courtyard cobbles stand on the courtyard level).
_s=rep126(_s,"exec(compile(_w,'build_castle27.py:walls (pass 124 edits)','exec'),NS124)",
 "exec(compile(sec124('# ================================================================= ground: island, ravelin, islets','# ================================================================= fortification walls'),'build_castle27.py:ground (pass 126 courtyard level)','exec'),NS124)")
# 3. The courtyard fronts: the first row is the state floor's row; portal E's door is open.
_s=rep126(_s,"rows=lambda L_:[(3.8,ZC+5.6,1.2,2.4,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L_>6 else [(3.8,ZC+5.6,1.2,2.4,0,'first')]",
 "rows=lambda L_:[(3.8,ZS126,1.2,HS126,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L_>6 else [(3.8,ZS126,1.2,HS126,0,'first')]")
_s=rep126(_s,"  if b<ZC+.2:arch_door27(m,x,y,u,b,w,h,r,a)","  if b<ZC+.2:(arch_open126 if abs(u-UE126)<.05 else arch_door27)(m,x,y,u,b,w,h,r,a)")
# 4. Portal E dresses the door on W1-V (Kungstrappan between Kuretornet and the courtyard front,
#    Olsson 1974), not the one on CI0-W1 in front of the south part of the range.
_s=rep126(_s,"'E':(CI124[0],W1_124)","'E':(W1_124,V124)")
# 5. Pass 27's castle and tower sections get this pass's edits before they run.
_s=rep126(_s,"exec(compile(_c,'build_castle27.py:castle (pass 124 edits)','exec'),NS124)",
 "exec(compile(EXTRA126,'build_block126.py:pass27_helpers','exec'),NS124);_c=edit_castle126(_c)\nexec(compile(_c,'build_castle27.py:castle (pass 124+126 edits)','exec'),NS124)")
_s=rep126(_s,"exec(compile(_k,'build_castle27.py:towers (pass 124 edits)','exec'),NS124)",
 "_k=edit_towers126(_k)\nexec(compile(_k,'build_castle27.py:towers (pass 124+126 edits)','exec'),NS124)")
EXTRA126='''
def west126(m,p,q,doors):
 # The outer front 55-56 (Kungsmakstornet to Kuretornet) with its three rows on the window axes of
 # Zettervall's elevation, not on pass 27's even 4.4 m spacing.
 x,y,L,a=sf_edge(p,q);holes=list(doors)
 for spacing,b,w,h,r,kind in OUT_ROWS:holes+=[(s-L/2,b,w,h,r) for s in WIN126]
 bz_wall(m,p,q,Z0,ZE,holes,K['Render'])
 for u,b,w,h,r in holes:
  if b<Z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)
  elif r>0:p18_win(m,x,y,u,b,w,h,r,a,K['Frame'],K['Brick'],2,2)
  else:s20_window(m,x,y,u,b,w,h,a,K['Frame'],TRIM,.62)
 lm_cornice(m,x,y,L+.4,ZE-.2,a,TRIM,True)
def arch_open126(m,x,y,u,b,w,h,r,a):
 # Portal E's door, open: pass 27's arch and jambs without the leaf, and a stone threshold.
 if r>0:p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w+.25,r+.12,.22,.40,a,TRIM)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.12),.40,b+h/2,.24,.12,h,TRIM,a)
 facade_box(m,x,y,u,.18,b+.006,w,.40,.012,TRIM,a)
_xe,_ye,_Le,_ae=sf_edge(CF124['W1'],CF124['N']);UE126=math.dist(CF124['W1'],CF124['V'])/2-_Le/2
'''
def edit_castle126(c):
 c=rep126(c,"  front(m,p,q,Z0,ZE,K['Render'],OUT_ROWS if L>6 else OUT_ROWS[:2],doors)",
  "  (west126(m,p,q,doors) if (i,j)==(55,56) else front(m,p,q,Z0,ZE,K['Render'],OUT_ROWS if L>6 else OUT_ROWS[:2],doors))")
 return c
def edit_towers126(k):
 # Kungsmakstornet's main window turns to face Kungsmaket's west niche (Zettervall 1883 shows it on
 # the tower's west face); the other windows stay on pass 27's directions.
 k=rep126(k," t0=math.atan2(cy-CY,cx-CX)\n"," t0=math.atan2(cy-CY,cx-CX);tw126=TWIN126.get(key)\n")
 k=rep126(k,"  t=t0+dt;town_window(","  t=tw126[0] if (tw126 and dt==0) else t0+dt;w=tw126[1] if (tw126 and dt==0) else w;town_window(")
 return k
NS126=dict(globals())
exec(compile(_s,'build_block124.py (pass 126 edits)','exec'),NS126)
assert NS126['ZC124']==ZC126 and NS126['NS124']['ZC']==ZC126
print('BLOCK126_PASS124_REBUILT',NS126['block124_names'],'ramp %.1f %%'%(100*(ZC126+.012-NS126['Z0_124']-.03)/(NS126['T1_124']-2*NS126['FLAT124'])))
# Pass 125's door passage into Kungsmaket crosses the re-created tower skin again.
cut_tower125();mark126(bpy.data.objects['SM_Kalmar_Slott_Towers'],'27,124,125')

# ================================================================= Gyllene salen (pass 125), re-run
SRC125=(R/'scripts/build_block125.py').read_text()
_g=SRC125[SRC125.index('# ---------------------------------------------------------------- the range frame'):SRC125.index('# ================================================================= Förrum (61a), a stand-in')]
_g=rep126(_g,"wall125(m,'c',GW['e'][1],-.12,gs1,GW['s'][1],FL125-.3,WT,[],M125['Plaster'])",
 "wall125(m,'c',GW['e'][1],-.12,gs1,GW['s'][1],FL125-.3,WT,[(-13.3,1.05,FL125-.3,FL125+2.3)],M125['Plaster'])\n"
 "bx125(m,gs1,GW['s'][1],-13.3-.525,-13.3+.525,FL125-.3,FL125,M125['Stone'])                       # threshold to the förstuga")
_g=rep126(_g,"for u in (-4.6,-13.3):leaf125(fS,u,1.05,2.3)","for u in (-4.6,):leaf125(fS,u,1.05,2.3)")
_B125D=json.loads(json.dumps(B125D));_B125D['windows']['gyllene_outer']=list(WIN126);_B125D['windows']['gyllene_court']=list(B126D['win_gyll_court'])
def _b125_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 return Mesh(name,category)
NS126g=dict(globals());NS126g.update(B125D=_B125D,b125_new=_b125_new,b125_finish=lambda m:mark126(s21_finish(m),'125'))
exec(compile(_g,'build_block125.py:Gyllene salen (pass 126 edits)','exec'),NS126g)

# ================================================================= Kungstrappan and the förstuga (55)
ST=B126D['stair'];W1_126=ST['W1'];E126=ST['E'];IN126=ST['IN'];FL126=B125D['floor']
def Q126(a,b,z=0.0):return (W1_126[0]+E126[0]*a+IN126[0]*b,W1_126[1]+E126[1]*a+IN126[1]*b,z)
(_ka0,_kb0),(_ka1,_kb1)=ST['kure_face']
def bk126(a):
 # The inner edge, clear of Kuretornet's skin; beyond the tower's ends it is held at its end value.
 a=max(_ka0,min(_ka1,a));return _kb0+(_kb1-_kb0)*(a-_ka0)/(_ka1-_ka0)-ST['skin']-.04
def qslab126(m,a0,a1,b0,b1,z0,z1,ma):
 # A prism in the Q frame; b1 may be a function of a (the inner edge along Kuretornet).
 f=b1 if callable(b1) else (lambda a,_b=b1:_b)
 if a1-a0<.002 or z1-z0<.002:return
 bot=[Q126(a0,b0,z0),Q126(a1,b0,z0),Q126(a1,f(a1),z0),Q126(a0,f(a0),z0)];top=[(x,y,z1) for x,y,_ in bot]
 hexa125(m,bot,top,ma)
def strips126(m,a0,a1,b0,b1,z0,z1,ma,step=1.0):
 n=max(1,math.ceil((a1-a0)/step))
 for k in range(n):qslab126(m,a0+(a1-a0)*k/n,a0+(a1-a0)*(k+1)/n,b0,b1,z0,z1,ma)
def b126_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 return Mesh(name,category)
m=b126_new('SM_Castle126_Kungstrappan','Kalmar slott/Interiör')
ZC_126,Rr126,T126=ZC126,ST['riser'],ST['tread'];AD126,AT126,AM126,AE126,AH126=ST['a_door'],ST['a_top'],ST['a_mid'],ST['a_end'],ST['a_hall']
LC0126,LC1126=ST['lane_c'];SP0126,SP1126=ST['spine'];LK0126=ST['lane_k0'];BL126=ST['b_land'];ZCE126=ST['z_ceil'];FLS126=FL126-.30
# The entry hall inside portal E: stone flags at the courtyard level, full width, under the förstuga.
strips126(m,AT126,AH126,0.0,bk126,ZC_126-.30,ZC_126+.012,M126['Flag'])
qslab126(m,AH126,AH126+.20,0.0,bk126,ZC_126-.30,FLS126,M126['Plaster'])                  # its far wall (beyond: the void over the passage)
# Flight 1 along the courtyard front, from the hall towards W1; 15 risers to the half landing.
for i in range(1,ST['risers']):qslab126(m,AT126-i*T126,AT126-(i-1)*T126,LC0126,LC1126,ZC_126-.30,ZC_126+i*Rr126,M126['Step'])
# The half landing beyond Kuretornet's corner, and its walls.
ZM126=ZC_126+ST['risers']*Rr126
qslab126(m,AE126,AM126,0.0,BL126,ZC_126-.30,ZM126,M126['Flag'])
qslab126(m,AE126-.20,AE126,-.05,BL126+.20,ZC_126-.30,ZCE126+.25,M126['Plaster'])            # end wall
qslab126(m,AE126,AM126,BL126,BL126+.20,ZC_126-.30,ZCE126+.25,M126['Plaster'])                   # side wall where Kuretornet stops
# Flight 2 along Kuretornet's face, back towards the hall; 15 risers to the state floor.
for j in range(1,ST['risers']):qslab126(m,AM126+(j-1)*T126,AM126+j*T126,LK0126,bk126,ZC_126-.30,ZM126+j*Rr126,M126['Step'])
# The spine wall between the flights, up to the ceiling.
qslab126(m,AM126,AT126,SP0126,SP1126,ZC_126-.30,ZCE126+.25,M126['Plaster'])
# The förstuga (55) at the state floor: from the top of flight 2 over the entry hall and the gate
# passage to Gyllene salen's south wall, under a plastered ceiling. The flags end inside that wall.
# a where the förstuga meets Gyllene salen's south wall (s 17.0-17.7): its far edge stays in the wall
_sW=(W1_126[0]-P125(0,0)[0])*U125[0]+(W1_126[1]-P125(0,0)[1])*U125[1];_eu=-(E126[0]*U125[0]+E126[1]*U125[1]);_iu=-(IN126[0]*U125[0]+IN126[1]*U125[1])
A_N126=(_sW-17.08-_iu*(bk126(30)+.3))/_eu
strips126(m,AT126,A_N126,0.0,bk126,FLS126,FL126,M126['Flag'])
qslab126(m,AT126-.12,AT126,LC0126,LC1126+.05,FL126,FL126+1.0,M126['Plaster'])            # parapet over flight 1's well
qslab126(m,AT126-.14,AT126+.02,LC0126,LC1126+.05,FL126+1.0,FL126+1.06,M126['Oak'])
strips126(m,AE126-.20,A_N126,-.05,lambda a:bk126(a)+.25 if a>AM126 else BL126+.20,ZCE126,ZCE126+.25,M126['Plaster'],1.5)
# North of Kuretornet's corner the range is hollow (pass 27): a wall closes the förstuga there.
_kn=ST['kure_face'][1];qslab126(m,_kn[0]-.05,A_N126,bk126(A_N126)+.02,bk126(A_N126)+.25,FLS126,ZCE126+.25,M126['Plaster'])
# Gyllene salen's south-east door, seen from the förstuga: a plain stone surround.
_fS=lambda a,d,z:P125(17.70+d,a,z)
for sg in (-1,1):fanplate125(m,[(-13.3+sg*.525,FL126),(-13.3+sg*.72,FL126),(-13.3+sg*.72,FL126+2.5),(-13.3+sg*.525,FL126+2.5)],0,.08,_fS,M126['Step'])
fanplate125(m,[(-13.3-.72,FL126+2.3),(-13.3+.72,FL126+2.3),(-13.3+.72,FL126+2.5),(-13.3-.72,FL126+2.5)],0,.08,_fS,M126['Step'])
# Oak handrails on the spine wall, along both flights.
for b_,a0,a1,z0,z1 in ((SP0126-.06,AT126,AM126,ZC_126+.9,ZM126+.9),(SP1126+.06,AM126,AT126,ZM126+.9,FL126+.9)):
 town_rod(m,Q126(a0,b_,z0),Q126(a1,b_,z1),.03,M126['Oak'],6)
mark126(s21_finish(m),None)

# ================================================================= cameras
def sv_camera126(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def look126(name,p,d,h,pitch,vfov):return sv_camera126(name,p[0],p[1],h,math.degrees(math.atan2(d[0],d[1]))-28.2,pitch,vfov)
_mid=P125(8.02,0);_n=B125D['frame']['n'];_u=B125D['frame']['u']
block126_cameras=[
 # The courtyard photograph of 2017 (Commons, pass 124's position, heading corrected on the corners
 # W1 and N), the 2022 well photograph, the west front square on (Zettervall), the stair.
 # 679: the 2017 photograph has level verticals with the horizon low in the frame (a shifted
 # view); render level with a 102 degree field and compare the upper 59 % of the frame.
 sv_camera126('679_Block126_Cal_Courtyard2017',-869.15,-321.77,ZC126+1.6,325.0,0,102.1),
 sv_camera126('680_Block126_Cal_Well2022',-869.33,-319.28,ZC126+1.6,327.6,12,72),
 look126('681_Block126_WestFront',(_mid[0]+_n[0]*60,_mid[1]+_n[1]*60),(-_n[0],-_n[1]),14.0,1,34),
 look126('682_Block126_PortalE',Q126(AD126,-9.0),IN126,ZC126+1.6,8,70),
 look126('683_Block126_Stair_Entry',Q126(AH126-.4,1.0),(-E126[0],-E126[1]),ZC126+1.6,22,80),
 look126('684_Block126_Stair_Landing',Q126(AE126+.5,2.6),E126,ZM126+1.6,18,80),
 look126('685_Block126_Forstuga',Q126(AT126+1.0,2.6),E126,FL126+1.6,2,74),
 look126('686_Block126_Gyllene_East',P125(15.3,-3.2),(_u[0]*-.32+_n[0]*-.95,_u[1]*-.32+_n[1]*-.95),FL126+1.5,10,62),
 look126('687_Block126_Gyllene_West',P125(10.4,-10.5),_n,FL126+1.6,6,74),
 ('688_Block126_Aerial_Courtyard',(-830.0,-345.0,48.0),(-868.0,-300.0,8.0),24),
]
print('BLOCK126_GEOMETRY',len(block126_names))
