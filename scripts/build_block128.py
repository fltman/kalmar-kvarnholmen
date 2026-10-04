"""Pass 128: Kalmar slott, the chimneys (corrects pass 127).

Pass 127's ten chimneys (six tall ones about 2 m up the courtyard slopes, placed from a first reading
of the 2017 photograph, and pass 27's four outer ones) are replaced by the fifteen measured or
estimated in scripts/prepare_block128.py (source/block128.json): on the courtyard side the slender
stacks at the SE_w/SE_e bend, above the SE_e eaves, in the east corner, on NE by the east end, two by
the north corner and one by the west corner, the wide stack on the SE_w ridge; on the outer side a row
of four on the SW range, a pair at the NE outer eaves and one on SE_e.
Everything else is pass 127's: build_block127.py runs again in a private namespace with three
asserted single replacements: its chimney list comes from source/block128.json, the mesh is marked as
pass 128's, and the cameras are left to this pass. Only SM_Kalmar_Slott is re-created.
Sources: references/block128-notes.md.
"""
B128D=json.loads((R/'source/block128.json').read_text())
def rep128(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)
def drop_degenerate_faces128(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)

SRC128=(R/'scripts/build_block127.py').read_text()
# The chimney list: pass 128's (same fields as pass 127's: x, y, w, d, ang, z0, z1).
SRC128=rep128(SRC128,"B127D=json.loads((R/'source/block127.json').read_text())\n",
 "B127D=json.loads((R/'source/block127.json').read_text());B127D['chimneys']=B128D['chimneys']   # pass 128\n")
# The re-created mesh is pass 128's.
SRC128=rep128(SRC128," obj['detail_pass']=127;obj['reference_notes']='references/block127-notes.md';obj['osm_way']=osm\n",
 " obj['detail_pass']=128;obj['reference_notes']='references/block128-notes.md';obj['osm_way']=osm\n")
SRC128=rep128(SRC128,"return mark127(obj,'27,124,126',osm)","return mark127(obj,'27,124,126,127',osm)")
# Pass 127's cameras are not defined again.
_cut128='# ================================================================= cameras\n';assert SRC128.count(_cut128)==1
SRC128=SRC128[:SRC128.index(_cut128)]
NS128=dict(globals());NS128['B128D']=B128D
exec(compile(SRC128,'build_block127.py (pass 128 chimneys)','exec'),NS128)
assert NS128['block127_names']==['SM_Kalmar_Slott'],NS128['block127_names']
block128_names=['SM_Kalmar_Slott']
_o128=bpy.data.objects['SM_Kalmar_Slott']
_o128['block128_dropped_faces']=drop_degenerate_faces128(_o128)
_o128['block128_chimneys']=len(B128D['chimneys'])
assert _o128['detail_pass']==128 and _o128['corrects_pass']=='27,124,126,127'
print('BLOCK128_CHIMNEYS',len(B128D['chimneys']),'dropped',_o128['block128_dropped_faces'],len(_o128.data.polygons))

# ================================================================= cameras
def sv_camera128(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_ZC128=json.loads((R/'source/block127.json').read_text())['zc']
block128_cameras=[
 # 695: the 2017 courtyard photograph (Commons, PD), pass 127's resected camera (689): level, horizon
 # at row 1115 of 1309, 61.1 degree field. The SE_w ridge stack and the bend stack are its two chimneys.
 sv_camera128('695_Block128_Cal_Courtyard2017',-861.1,-292.66,_ZC128+1.6,174.9,0,61.1),
 # 696-698: Street View 2014 courtyard views at the resected pano cameras (heading offset applied):
 # pano 1 (zCIfieeXGQUNANmWu_Tg9A) looking east at the NE/SE_e roofs (URL 98h, 100t, 60y) and
 # south-east at SE_w (135h, 108t, 75y); pano 2 (jOXzkLldNOjrveyz1T81wg) looking at SE_e (150h, 105t, 75y).
 sv_camera128('696_Block128_Cal_Pano1_East',-885.06,-306.46,_ZC128+2.1,96.66,10,60),
 sv_camera128('697_Block128_Cal_Pano1_SEw',-885.06,-306.46,_ZC128+2.1,133.66,18,75),
 sv_camera128('698_Block128_Cal_Pano2_SEe',-860.06,-308.67,_ZC128+1.9,147.35,15,75),
 ('699_Block128_Aerial_Chimneys',(-800.0,-370.0,75.0),(-868.0,-305.0,20.0),28),
]
print('BLOCK128_GEOMETRY',len(block128_names))
