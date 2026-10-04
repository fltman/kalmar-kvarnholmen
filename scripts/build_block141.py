"""Pass 141: Kalmar slott, the north tower's height (corrects passes 27 and 132 on SM_Kalmar_Slott_Towers).

Pass 27 put the north tower's (Kungsmakstornet, key N) wall top, the eaves where the copper starts,
at z 23.27 by eye. Möller's survey section of 1882 (PK006-00041) reads z 22.63, his roof drawing of
1885 (PK006-00049) 13.5 fot over an adjoining cornice, z 24.28 on the range's outer eaves. Three
views with resected cameras (the -wuppertaler photograph of 2022, two Street View panoramas of 2014,
viewed only) put the tower's eaves 4.0-4.4 m over the range eaves next to it, mean z 24.53. Möller
1885 and the views agree within 0.25 m; Möller 1882 is 1.9 m off both. The wall top goes to z 24.28
(scripts/prepare_block141.py -> source/block141.json).

The mesh is re-created the way pass 132 did it: pass 132's composition (pass 126's composition of
pass 124's code, which re-runs pass 27's towers section with pass 132's caps) runs in a private
namespace, with single, asserted replacements:
- pass 27's TOWER_SPEC: N's 'top' 24.6 -> 25.61 (z 23.27 -> 24.28). Wall, cornice, corbel row and
  pass 132's cap (Möller's bell, drum, onion, ball, fleur and vane) all hang off this one value, so
  the cap moves up with the wall top;
- after N's cap a flashing collar (collar141): pass 127 cut the range roofs against pass 27's bell,
  so between the old wall top and 0.6 m above it the roofs stop up to 0.3 m outside the wall. Where
  a roof stands in that band, the collar (tower render) fills the slot out to pass 27's bell less
  0.05 m, as pass 132's bell did above it;
- pass 132's marking becomes this pass's.
Pass 125's cut for Kungsmaket's door passage is applied again, as in pass 132. Nothing else changes.
Sources: references/block141-notes.md.
"""
import json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
# Pass 125 leaves numbers in the shared names TS and TC, which the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B141D=json.loads((R/'source/block141.json').read_text())
block141_names=[]

def drop_degenerate_faces141(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark141(obj):
 obj['block141_dropped_faces']=drop_degenerate_faces141(obj);print('BLOCK141_DROPPED',obj.name,obj['block141_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=141;obj['reference_notes']='references/block141-notes.md'
 obj['osm_way']=','.join(t['osm_way'] for t in json.loads((R/'source/castle27.json').read_text())['castle']['towers'].values())
 obj['corrects_pass']='27,124,125,126,132'
 obj['block141_n_wall_top']=B141D['decision']['z_new']
 if obj.name not in block141_names:block141_names.append(obj.name)
 return obj
def rep141(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)

# The range roofs as they stand now (pass 137's SM_Kalmar_Slott), for the collar and pass 132's bulge.
def _roof_tree141():
 import bmesh
 o=bpy.data.objects['SM_Kalmar_Slott'];bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world)
 t=BVHTree.FromBMesh(bm);bm.free();return t
ROOF141=_roof_tree141()
def under_roof141(x,y,z):
 loc,_,_,_=ROOF141.ray_cast(Vector((x,y,z)),Vector((0,0,1)),20.0);return loc is not None

# The roofs' cut-edge vertices round N between the old wall top and 0.6 m above it, outside the wall.
def _cutv141():
 import numpy as np
 o=bpy.data.objects['SM_Kalmar_Slott'];T=json.loads((R/'source/castle27.json').read_text())['castle']['towers']['N']
 cx,cy=T['centre'];r=T['radius'];z0=B141D['collar']['z_old'];mw=o.matrix_world;out=[]
 for v in o.data.vertices:
  w=mw@v.co;d=math.hypot(w.x-cx,w.y-cy)
  if z0-.05<w.z<z0+B141D['collar']['h_top'] and r-.02<d<r+.45:out.append((math.atan2(w.y-cy,w.x-cx),w.z))
 return out
CUTV141=_cutv141();print('BLOCK141_CUTV',len(CUTV141))
# ---------------------------------------------------------------- the flashing collar (runs inside NS124)
EXTRA141=r'''
def collar141(m,key,cx,cy,r):
 # Pass 127's roofs stop at pass 27's bell less 0.15 m (rold132): above the old wall top z0 that is
 # up to 0.3 m outside the wall, which now rises to the new wall top. Where a roof's cut edge lies in
 # that band (CUTV141) the collar fills the slot, from 0.3 m under the edge up to z0+0.6 (where pass
 # 27's bell comes back inside the wall), out to pass 27's bell less 0.05 m.
 C=B141D['collar'];z0=C['z_old'];zt=z0+C['h_top'];n=int(round(360/C['step_deg']));MA=K['RenderTower']
 def ro(z):return r+.40 if z<z0 else max(r-.02,rold132(key,z)-.05)
 S=[.0,.12,.25,.40,.55,.70,.85,1.0]
 def ring(t,zb):
  out=[]
  for s in S:
   z=zb+(zt-zb)*s;rr=ro(z);out.append((cx+rr*math.cos(t),cy+rr*math.sin(t),z))
  ri=r-C['depth']
  return out+[(cx+ri*math.cos(t),cy+ri*math.sin(t),zt),(cx+ri*math.cos(t),cy+ri*math.sin(t),zb)]
 # The roofs' cut-edge vertices in the band, binned by azimuth (one bin each side added); a bin's
 # collar starts 0.30 m under the lowest of them.
 low=[None]*n
 for t,z in CUTV141:
  b=int((t%math.tau)/(math.tau/n))%n
  for bb in (b-1,b,b+1):
   bb%=n;low[bb]=z if low[bb] is None else min(low[bb],z)
 def zb(i):
  v=[low[j%n] for j in (i-1,i) if low[j%n] is not None];return min(v)-.30
 runs=[];cur=[]
 for i in range(n):
  if low[i] is not None:cur.append(i)
  elif cur:runs.append(cur);cur=[]
 if cur:runs.append(cur)
 if len(runs)>1 and runs[0][0]==0 and runs[-1][-1]==n-1:runs[0]=runs.pop()+runs[0]
 for run in runs:
  idx=run+[(run[-1]+1)%n]
  rings=[ring(i*math.tau/n,zb(i)) for i in idx]
  V=[];F=[];L=len(rings[0])
  for rg in rings:V.extend(rg)
  for a in range(len(rings)-1):
   for k in range(L):F.append((a*L+k,a*L+(k+1)%L,(a+1)*L+(k+1)%L,(a+1)*L+k))
  for a,flip in ((0,True),(len(rings)-1,False)):
   rg=rings[a];c=(sum(p[0] for p in rg)/L,sum(p[1] for p in rg)/L,sum(p[2] for p in rg)/L);ci=len(V);V.append(c)
   F+=[(ci,a*L+(k+1)%L,a*L+k) if flip else (ci,a*L+k,a*L+(k+1)%L) for k in range(L)]
  m.faces(V,F,MA);COLLAR141.append(len(run))
COLLAR141=[]
'''

def edit_towers141(k):
 # N's wall top (pass 27's TOWER_SPEC); everything of the tower above it hangs off z1.
 k=rep141(k,"'N':dict(top=24.6,","'N':dict(top=%r,"%B141D['decision']['top_new'])
 k=rep141(k," caps132(m,key,cx,cy,r,z1,t0)\n"," caps132(m,key,cx,cy,r,z1,t0)\n if key=='N':collar141(m,key,cx,cy,r)\n")
 return k

# ================================================================= pass 132's composition, re-run
SRC132_141=(R/'scripts/build_block132.py').read_text()
_c141=SRC132_141[SRC132_141.index("# ================================================================= pass 126's composition of pass 124"):SRC132_141.index("# ================================================================= cameras")]
_c141=rep141(_c141,"_k=edit_towers132(edit_towers126(_k))\\nexec(compile(EXTRA132,'build_block132.py:caps','exec'),NS124)\\n",
 "_k=edit_towers141(edit_towers132(edit_towers126(_k)))\\nexec(compile(EXTRA132,'build_block132.py:caps','exec'),NS124)\\nexec(compile(EXTRA141,'build_block141.py:collar','exec'),NS124)\\n")
_c141=rep141(_c141,"cut_tower125();mark132(bpy.data.objects['SM_Kalmar_Slott_Towers'])","cut_tower125();mark141(bpy.data.objects['SM_Kalmar_Slott_Towers'])")
_c141=rep141(_c141,"print('BLOCK132_BULGED',","print('BLOCK141_COLLAR',NSP132['NS124']['COLLAR141']);print('BLOCK141_BULGED',")
NSP141=dict(globals());NSP141['under_roof132']=under_roof141
exec(compile(_c141,'build_block132.py composition (pass 141 edits)','exec'),NSP141)
assert NSP141['NSP132']['NS124']['castle27_names']==['SM_Kalmar_Slott_Towers']
assert NSP141['NSP132']['NS124']['TOWER_SPEC']['N']['top']==B141D['decision']['top_new']
assert sum(NSP141['NSP132']['NS124']['COLLAR141'])>0,'no roof meets the north tower in the collar band'

# ================================================================= cameras
def sv_camera141(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block141_cameras=[
 # 785: the -wuppertaler photograph of 2022 (castle27/swe-kalmar-slott-004.jpg), resected (f 1444 px).
 sv_camera141('785_Block141_Cal_Photo2022_NorthTower',-898.89,-176.26,2.0,140.3,9.2,52.97),
 # 786: Street View 2014 on the castle bridge, zoomed on the north tower (40y, 92h).
 sv_camera141('786_Block141_Cal_SV2014_Bridge',-915.14,-231.90,6.0,92.0,15.9,40.0),
 # 787: Street View 2014 on the north-east rampart, the north tower and the NE range (45y, 222h).
 sv_camera141('787_Block141_Cal_SV2014_Rampart',-823.68,-252.79,12.3,219.3,16.5,45.0),
 # 788: the roof joints round the north tower, from the north-west at roof height.
 sv_camera141('788_Block141_NorthTower_Joint',-872.0,-238.0,23.0,129.0,-8.0,40.0),
 ('789_Block141_Aerial_NorthTower',(-800.0,-200.0,70.0),(-855.8,-262.0,22.0),35),
]
print('BLOCK141_GEOMETRY',len(block141_names))
