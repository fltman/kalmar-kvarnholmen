"""Bring the working Unreal project up to date with every Blender pass since the last Unreal import (pass 80).

One session instead of 61 per-pass refreshes: many meshes (the castle, pass 98's mainland chunks) were re-created by
several passes, and exports/ holds only their final FBX. Steps, each resumable:
 1. every material in exports/manifest.json missing under /Game/Kalmar/Materials is created (same helper and settings
    as the per-pass materials_blockN.py scripts);
 2. the union of previews/blockN-build.json['changed'] for N in FIRST..LAST is imported through patch_pass18.py;
 3. review cameras 401.. are placed;
 4. the render-buffer audit runs over the union.
Reports: previews/union081-{materials,import,render-audit}.json.
"""
import unreal as u,json,ast,math
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2];BASE='/Game/Kalmar'
FIRST,LAST=81,int(globals().get('union_last',143))
MAN=json.loads((R/'exports/manifest.json').read_text());library=u.EditorAssetLibrary
assets={a['name'] for a in MAN['assets']}
names=[]
for n in range(FIRST,LAST+1):
 for x in json.loads((R/f'previews/block{n}-build.json').read_text())['changed']:
  if x in assets and x not in names:names.append(x)
u.log(f'UNION_NAMES {len(names)}')

# 1. materials
tree=ast.parse((P/'build_stortorget.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'setp','import_task','scalar','material'}]
H={'u':u,'R':R,'ROOT':R,'BASE':BASE,'MAN':MAN,'assets':u.AssetToolsHelpers.get_asset_tools(),'library':library};exec(compile(tree,'material_helpers','exec'),H)
mrep_file=R/'previews/union081-materials.json'
mrep=json.loads(mrep_file.read_text()) if mrep_file.exists() else {'created':[],'existing':0}
for name,spec in MAN['materials'].items():
 if library.does_asset_exist(BASE+'/Materials/'+name):continue
 ma=H['material'](name,spec);ma.set_editor_property('two_sided',True);ma.set_editor_property('used_with_nanite',True)
 u.MaterialEditingLibrary.recompile_material(ma);library.save_loaded_asset(ma)
 mrep['created'].append(name);mrep_file.write_text(json.dumps(mrep,indent=1))
mrep['status']='passed';mrep_file.write_text(json.dumps(mrep,indent=1))
u.log(f'UNION_MATERIALS created {len(mrep["created"])}')

# 2. meshes (patch_pass18 skips meshes already done in the report)
code=(P/'patch_pass18.py').read_text().replace('range(78,91)','range(401,1000)')
exec(compile(code,str(P/'patch_pass18.py'),'exec'),{'__file__':str(P/'patch_pass18.py'),'pass18_import_only':names,'pass18_import_report':'union081-import.json'})

# 4. render audit over the union
result={}
for name in names:
 mesh=u.load_asset(BASE+'/Meshes/'+name);c={'vertices':0,'zero_tangents':0,'zero_normals':0,'nonfinite_vectors':0,'nonunit_vectors':0}
 for i in range(mesh.get_num_sections(0)):
  vs,tris,ns,uvs,ts=u.ProceduralMeshLibrary.get_section_from_static_mesh(mesh,0,i)
  lengths=[v.x*v.x+v.y*v.y+v.z*v.z for v in list(ns)+[t.tangent_x for t in ts]]
  c['nonfinite_vectors']+=sum(not math.isfinite(q) for q in lengths);c['nonunit_vectors']+=sum(math.isfinite(q) and abs(q-1)>.05 for q in lengths)
  c['vertices']+=len(vs);c['zero_tangents']+=sum(t.tangent_x.x**2+t.tangent_x.y**2+t.tangent_x.z**2<1e-8 for t in ts);c['zero_normals']+=sum(n.x*n.x+n.y*n.y+n.z*n.z<1e-8 for n in ns)
 result[name]=c
ok=all(v['vertices']>0 and v['zero_tangents']==0 and v['zero_normals']==0 and v['nonfinite_vectors']==0 and v['nonunit_vectors']==0 for v in result.values())
(R/'previews/union081-render-audit.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','meshes':result},indent=1))
u.log('UNION_DONE '+('passed' if ok else 'review_required'))
