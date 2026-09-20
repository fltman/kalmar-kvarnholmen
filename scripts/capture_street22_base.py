"""Capture a fixed pre-pass geometry base; deliberately refuses to overwrite it."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=R/'source/street22-base.json'
if out.exists():raise RuntimeError('The authored street22 base already exists; preserve it.')
names=json.loads((R/'source/street22-scope.json').read_text())['names']
with bpy.data.libraries.load(str(R/'source/Stortorget.blend'),link=False) as (a,b):b.objects=names
result={'license':'CC BY 4.0 original geometry; OSM-derived footprints retain ODbL attribution.','purpose':'Stable pre-pass-22 geometry, used to retain unaffected facades and roof footprints.','meshes':{}}
for obj in b.objects:
 assert obj is not None
 result['meshes'][obj.name]={'vertices':[[float(v) for v in obj.matrix_world@p.co] for p in obj.data.vertices],'materials':[m.name for m in obj.data.materials],'faces':[[list(f.vertices),f.material_index,f.use_smooth] for f in obj.data.polygons]}
out.write_text(json.dumps(result,separators=(',',':'))+'\n');print('STREET22_BASE_READY')
