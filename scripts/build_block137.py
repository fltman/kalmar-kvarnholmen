"""Pass 137: Kalmar slott, corrections from the project's own sources (corrects passes 27, 127, 131 and 135).

- SM_Castle135_Kungskoket (re-created): the great hearth after the 1969 photographs (DigitaltMuseum
  021017090086, -090089, -090090): a brick stack with rounded corners (quarter rings, radius 0.70 m),
  two round-headed openings on each long face and one on each short face, a projecting top course and
  a rounded, convex hood lofted from the stack's outline to a circle under the cross wall's arch, its
  lower third in brick; a round flue into the wall over the crown. Everything else is pass 135's.
- SM_Castle135_KungskoketInventarier (re-created): pass 135's furnishings; the trammel bars follow the
  hearth's new openings.
- SM_Kalmar_Slott (re-created): the second state-floor window of Gröna salen's end wall on the SW
  range's outer front at SW s 1.55 (Commons 'Kalmar Slott 9', resected), and the painted rustication
  extended to the NE courtyard front (the 2022 photograph; pass 127's RUST127 gains 'NE').
- SM_Castle124_Portals, SM_Castle124_Paving: re-created by the composition (no change).
- SM_Castle131_GronaSalen (re-created): pass 131's blind niche at SW s 1.55 runs through to the new
  facade window, with its own window like the other niches (pass 131's prepare re-run with blind off).
Not changed: the north tower's wall top (the 1882 and 1885 Möller sheets disagree; see the notes).
Method: pass 135's composition (build_block135.py's slice, which re-runs pass 133's composition of
passes 124-129 and 133) and pass 135's kitchen run again in a private namespace with this pass's
single, asserted replacements; pass 131's Gröna salen section runs again in its own namespace with
pass 131's materials mapped by name. Sources: references/block137-notes.md.
"""
import re
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
# Pass 125 leaves numbers in the shared names TS/TC that the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B137D=json.loads((R/'source/block137.json').read_text())
block137_names=[]

def rep137(src,old,new,n=1):
 assert src.count(old)==n,('source changed',src.count(old),n,old[:80]);return src.replace(old,new)
def drop_degenerate_faces137(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def finish137(name,corrects):
 # After the re-created code's own finish: this pass's degenerate-face filter, marking, the name list.
 obj=bpy.data.objects[name];obj['block137_dropped_faces']=drop_degenerate_faces137(obj)
 obj['detail_pass']=137;obj['reference_notes']='references/block137-notes.md';obj['corrects_pass']=corrects
 if name not in block137_names:block137_names.append(name)
 print('BLOCK137_MESH',name,corrects,'dropped',obj['block137_dropped_faces'],len(obj.data.polygons))
def mats137(path,prefix):
 # The material keys of an earlier pass's setup loop, mapped by name (the materials are not re-created).
 t=(R/path).read_text();i=t.index('for key,texture,target,rough,metal in [');j=t.index(' ]:',i)
 keys=re.findall(r"\('(\w+)','Town",t[i:j]);d={k:prefix+k for k in keys}
 assert keys and all(v in materials for v in d.values()),(path,[v for v in d.values() if v not in materials])
 return d

# ================================================================= pass 135's composition and kitchen, re-run
_S135src137=(R/'scripts/build_block135.py').read_text()
T137=_S135src137[_S135src137.index('def rep135(src,old,new):'):_S135src137.index('furnish135(*kitchen135())\n')+len('furnish135(*kitchen135())\n')]
# Marking: the re-created meshes are pass 137's (pass 135's mark, the composition's marks and asserts).
T137=rep137(T137,"obj['detail_pass']=135;obj['reference_notes']='references/block135-notes.md'","obj['detail_pass']=137;obj['reference_notes']='references/block137-notes.md'",3)
T137=rep137(T137,"'27,124,126,127,128,129,133' if obj.name=='SM_Kalmar_Slott' else '124,126,129,133'","'27,124,126,127,128,129,133,135' if obj.name=='SM_Kalmar_Slott' else '124,126,129,133,135'")
T137=rep137(T137,"assert _o['detail_pass']==135","assert _o['detail_pass']==137",2)
T137=rep137(T137,"BLOCK135_MESH","BLOCK137_MESH",2)
T137=rep137(T137,"BLOCK135_PASS133_REBUILT","BLOCK137_PASS133_REBUILT")
T137=rep137(T137,"_o=s21_finish(m);_o['osm_way']='';mark135(_o,None)","_o=s21_finish(m);_o['osm_way']='';mark135(_o,'135')",2)
# This pass's edits on the composed source, after pass 135's.
T137=rep137(T137,"SRC133=EDITSRC135(SRC133)\\n","SRC133=EDITSRC137(EDITSRC135(SRC133))\\n")
# The kitchen: the hearth's data and its form are this pass's.
T137=rep137(T137,"K135=B135D['kitchen'];","K135=dict(B135D['kitchen'],hearth=B137D['hearth']);")
_hA137=" H=K135['hearth'];hs,hc,t=H['hs'],H['hc'],H['t'];SH,CH=H['s'],H['c']\n";_hB137="H['hood_top']-.02,A['crown']+.10,M135['Lime'])\n"
assert T137.count(_hA137)==1 and T137.count(_hB137)==1
T137=T137[:T137.index(_hA137)]+_hA137+" hearth137(m,H,A)   # pass 137\n"+T137[T137.index(_hB137)+len(_hB137):]
def EDITSRC137(src):
 # Pass 27's helpers get this pass's (after pass 135's); NE joins the rusticated fronts; pass 27's outer
 # front rule gets the extra window on SW's first outer edge (CO7 -> CO8).
 src=rep137(src,"exec(compile(EXTRA135,'build_block135.py:pass27_helpers','exec'),NS124);",
  "exec(compile(EXTRA135,'build_block135.py:pass27_helpers','exec'),NS124);exec(compile(EXTRA137,'build_block137.py:pass27_helpers','exec'),NS124);")
 src=rep137(src,"RUST127=('NW','SW')\n","RUST127=('NW','SW','NE')   # pass 137: NE is painted with the rustication by 2022\n")
 # NE's last straight edge by the east corner (CI5-CI6, collinear with NE; pass 127's nearest-range test gives it to SE_e)
 src=rep137(src,"def cmat127(p,q):return M127['Joint'] if crange127(p,q,True) in RUST127 else M127['Lime']",
  "def cmat127(p,q):return M127['Joint'] if crange127(p,q,True) in RUST127 or rust137(p,q) else M127['Lime']")
 src=rep137(src," if crange127(p,q,True) not in RUST127:return"," if crange127(p,q,True) not in RUST127 and not rust137(p,q):return")
 src=rep137(src," return c\nNS127=dict(NSP127);",
  " c=rep127(c,\"  doors=[(0.0,Z0,1.5,2.9,.55)] if (i,j)==longest else []\",\"  doors=([(0.0,Z0,1.5,2.9,.55)] if (i,j)==longest else [])+OUTWIN137.get((i,j),[])\")\n return c\nNS127=dict(NSP127);")
 return src
_fw137=B137D['facade_window']
EXTRA137='''
# Pass 137: Gröna salen's second end-wall window (Commons 'Kalmar Slott 9', resected), main row, on the
# SW outer edge CO7 -> CO8; it is drawn by pass 27's front() like the other main-row windows.
OUTWIN137={%r:[%r]}
def rust137(p,q):
 # NE's straight courtyard line runs on over CI5-CI6 to the east corner (pass 129); it is rusticated too.
 a,b=CI[%r],CI[%r];return (math.dist(p,a)<.01 and math.dist(q,b)<.01) or (math.dist(p,b)<.01 and math.dist(q,a)<.01)
'''%(tuple(_fw137['edge']),tuple(_fw137['hole']),5,6)
HEARTH137='''
def wring137(pts):
 # Frame points (s,c) to a world ring, counter-clockwise (the frame is left-handed in plan).
 w=[W135(s,c) for s,c in pts];a=sum(w[i][0]*w[(i+1)%len(w)][1]-w[(i+1)%len(w)][0]*w[i][1] for i in range(len(w)))
 return w if a>0 else w[::-1]
def rr137(s0,s1,c0,c1,r,k=6):
 pts=[]
 for cs_,cc_,a0 in ((s1-r,c0+r,-90),(s1-r,c1-r,0),(s0+r,c1-r,90),(s0+r,c0+r,180)):
  for i in range(k+1):a=math.radians(a0+90*i/k);pts.append((cs_+r*math.cos(a),cc_+r*math.sin(a)))
 return pts
def hearth137(m,H,A):
 # The great hearth (1969: 090086, 090089, 090090): a brick stack with rounded corners, round-headed
 # openings on the faces, a fire bed, a projecting top course, a convex hood into the arch, a round flue.
 hs,hc,t,r=H['hs'],H['hc'],H['t'],H['r'];SH,CH=H['s'],H['c'];zp,top=H['zp'],H['top'];p=H['plinth']
 prism135(m,wring137(rr137(SH-hs-p,SH+hs+p,CH-hc-p,CH+hc+p,r+p)),ZB135,zp,M135['Flag'])
 # the long faces (two openings each) and the short faces (one), between the rounded corners
 _sn=[(CH-hc+r,zp)]+[q for a0,a1 in H['arches_sn'] for q in notch135(CH+a0,CH+a1,zp,H['spring'])]+[(CH+hc-r,zp),(CH+hc-r,top),(CH-hc+r,top)]
 for s0 in (SH-hs,SH+hs-t):plane135(m,_sn,'s',s0,s0+t,M135['Brick'])
 _ew=[(SH-hs+r,zp)]+notch135(SH+H['arch_ew'][0],SH+H['arch_ew'][1],zp,H['spring_ew'])+[(SH+hs-r,zp),(SH+hs-r,top),(SH-hs+r,top)]
 for c0 in (CH-hc,CH+hc-t):plane135(m,_ew,'c',c0,c0+t,M135['Brick'])
 # the rounded corners: quarter rings, outer radius r, inner r - t
 for ss,sc,a0 in ((1,1,0),(-1,1,90),(-1,-1,180),(1,-1,270)):
  cs_,cc_=SH+ss*(hs-r),CH+sc*(hc-r);k=8
  pts=[(cs_+r*math.cos(math.radians(a0+90*i/k)),cc_+r*math.sin(math.radians(a0+90*i/k))) for i in range(k+1)]
  pts+=[(cs_+(r-t)*math.cos(math.radians(a0+90*i/k)),cc_+(r-t)*math.sin(math.radians(a0+90*i/k))) for i in range(k,-1,-1)]
  prism135(m,wring137(pts),zp,top,M135['Brick'])
 # the fire bed and the sooty underside of the top, inside the walls
 inner=rr137(SH-hs+t,SH+hs-t,CH-hc+t,CH+hc-t,r-t)
 prism135(m,wring137(inner),zp,H['bed'],M135['Soot']);prism135(m,wring137(inner),top-.04,top,M135['Soot'])
 # the projecting top course
 L_=H['ledge'];prism135(m,wring137(rr137(SH-hs-L_,SH+hs+L_,CH-hc-L_,CH+hc+L_,r+L_)),top,H['hood_z0'],M135['Reveal'])
 # the hood: lofted rings (prepare_block137.py), the lower third brick, the rest whitewashed
 rings=[(z,wring137(pts)) for z,pts in H['hood']];n=len(rings[0][1])
 for i in range(len(rings)-1):
  (z0,a),(z1,b)=rings[i],rings[i+1]
  v=[(x,y,z0) for x,y in a]+[(x,y,z1) for x,y in b]
  m.faces(v,[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],M135['Brick'] if i<2 else M135['Lime'])
 for (z,ring_),flip in ((rings[0],True),(rings[-1],False)):
  tris=tessellate_polygon([[Vector((x,y,0)) for x,y in ring_]]);v=[(x,y,z) for x,y in ring_]
  m.faces(v,[((tr[2],tr[1],tr[0]) if flip else (tr[0],tr[1],tr[2])) for tr in tris],M135['Lime'])
 # the round flue from the hood's top into the cross wall over the arch's crown
 fr=H['flue_r'];prism135(m,wring137([(SH+fr*math.cos(2*math.pi*i/24),CH+fr*math.sin(2*math.pi*i/24)) for i in range(24)]),H['hood_top']-.02,A['crown']+.10,M135['Lime'])
'''
NSP137=dict(globals())
_mat135_137=mats137('scripts/build_block135.py','M_Block135_')
NSP137.update(B135D=json.loads((R/'source/block135.json').read_text()),B137D=B137D,B135=_mat135_137,M135=_mat135_137,block135_names=[],
 EDITSRC137=EDITSRC137,EXTRA137=EXTRA137,Vector=Vector,tessellate_polygon=tessellate_polygon)
exec(compile(HEARTH137,'build_block137.py:hearth','exec'),NSP137)
exec(compile(T137,'build_block135.py:composition and kitchen (pass 137 edits)','exec'),NSP137)
assert NSP137['block135_names']==['SM_Kalmar_Slott','SM_Castle124_Portals','SM_Castle124_Paving','SM_Castle135_Kungskoket','SM_Castle135_KungskoketInventarier'],NSP137['block135_names']
for _n137,_c137 in (('SM_Kalmar_Slott','27,124,126,127,128,129,133,135'),('SM_Castle124_Portals','124,126,129,133,135'),('SM_Castle124_Paving','124,126,129,133,135'),
 ('SM_Castle135_Kungskoket','135'),('SM_Castle135_KungskoketInventarier','135')):
 assert bpy.data.objects[_n137]['detail_pass']==137,(_n137,bpy.data.objects[_n137]['detail_pass'])
 finish137(_n137,_c137)

# ================================================================= Gröna salen (pass 131), re-run with the end niche open
_S131src137=(R/'scripts/build_block131.py').read_text()
G137=_S131src137[_S131src137.index('def b131_new(name,category):'):_S131src137.index('# ---------------------------------------------------------------- furnishings: escutcheons, crucifix')]
G137=rep137(G137,"obj['detail_pass']=131;obj['reference_notes']='references/block131-notes.md';obj['osm_way']='';return obj",
 "obj['detail_pass']=137;obj['reference_notes']='references/block137-notes.md';obj['osm_way']='';return obj")
_B131D137=json.loads((R/'source/block131.json').read_text());_B131D137['gron']=B137D['gron']
_mat131_137=mats137('scripts/build_block131.py','M_Block131_')
NSG137=dict(globals());NSG137.update(B131D=_B131D137,B131=_mat131_137,M131=_mat131_137,block131_names=[],tess131=tessellate_polygon,Vector=Vector)
exec(compile(G137,'build_block131.py:Gröna salen (pass 137 edits)','exec'),NSG137)
assert NSG137['block131_names']==['SM_Castle131_GronaSalen'],NSG137['block131_names']
finish137('SM_Castle131_GronaSalen','131')

# ================================================================= cameras
def sv_camera137(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def look137(name,s,c,h,ds,dc,pitch,vfov):
 # A camera in Kungsköket's frame (SE_w): position (s,c), looking along (ds,dc).
 F_=NSP137['B135D']['frame'];o,u,n=F_['origin'],F_['u'],F_['n']
 x,y=o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c;vx,vy=u[0]*ds+n[0]*dc,u[1]*ds+n[1]*dc
 return sv_camera137(name,x,y,h,math.degrees(math.atan2(vx,vy))-28.2,pitch,vfov)
_zf137=NSP137['B135D']['kitchen']['zf'];_cam690_137=json.loads((R/'source/block129.json').read_text())['camera690'];_zc137=NSP137['B135D']['zc']
block137_cameras=[
 # 750: the hearth under the cross wall's arch from the north part's outer side, its outer short face on
 # the left and its north face on the right (1969, 090089 'Spisens norra del'), by eye.
 look137('750_Block137_Cal_Hearth1969North',16.6,-3.4,_zf137+1.5,-4.65,-3.3,10,66),
 # 751: the hearth's south side with its two openings (1969, 090090 'Spisens södra sida'), by eye.
 look137('751_Block137_Cal_Hearth1969South',6.6,-6.7,_zf137+1.5,1,0,15,64),
 # 752: the SW range's outer front from the west (Commons 'Kalmar Slott 9'), camera resected on six
 # points (postejer W and S, towers W, S and N, Kuretornet; f 1649 px on 1280 x 857, 1.5 px residual).
 sv_camera137('752_Block137_Cal_SWFront_GronaWindows',-1107.3,-354.2,2.0,54.6,5.1,29.14),
 # 753: the 2022 well photograph (pass 129's camera 690): NE rusticated on the left.
 sv_camera137('753_Block137_Cal_Well2022_NE',_cam690_137['x'],_cam690_137['y'],_zc137+_cam690_137['h'],_cam690_137['heading'],_cam690_137['pitch'],_cam690_137['vfov']),
 ('754_Block137_Aerial_Castle',(-960.0,-380.0,62.0),(-878.0,-312.0,12.0),24),
]
print('BLOCK137_GEOMETRY',len(block137_names))
