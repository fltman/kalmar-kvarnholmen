"""Seal the three mapped flat roofs; author the previously generic old water tower."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()"
exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
exec(compile((R/'scripts/materials_district17.py').read_text(),'materials_district17.py','exec'))
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']}
for fn in ['build_larmtorget_facades.py','build_sodra_facades.py','build_district17.py']:
 tree=ast.parse((R/'scripts'/fn).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(tree,fn,'exec'))
district17_audit={};district17_cameras=[]
exec(compile((R/'scripts/build_water_tower17.py').read_text(),'build_water_tower17.py','exec'))
D={b['id']:b for b in json.loads((R/'source/kvarnholmen.json').read_text())['buildings']}
extension_names=['SM_Kvarnholmen_House_91072716'];extension_cameras=district17_cameras
for bid in ['886305409','92204173']:
 name='SM_Kvarnholmen_House_'+bid;obj=bpy.data.objects[name];b=D[bid];m=Mesh('RoofRepair17','Temporary')
 for tri in b['triangles']:
  vs=[(x,y,b['height']+.025) for x,y in tri]
  if (Vector(vs[1])-Vector(vs[0])).cross(Vector(vs[2])-Vector(vs[0])).z<0:vs.reverse()
  m.faces(vs,[(0,1,2)],METAL)
 cap=m.finish();bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);cap.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.join();extension_names.append(name)
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','district17-roof-build.json').replace('POLISH15_BUILD_OK','DISTRICT17_ROOF_OK').replace('EXPORT15','EXPORT17_ROOF')
# Atomic replacement: a simultaneously running importer sees either complete FBX version.
tail=tail.replace("export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))", "export_district_fbx(obj,R/'exports/meshes'/(name+'.pending.fbx'));(R/'exports/meshes'/(name+'.pending.fbx')).replace(R/'exports/meshes'/(name+'.fbx'))")
exec(compile(tail,str(R/'scripts/repair_district17_roofs.py'),'exec'))
a=json.loads((R/'previews/district17-facades.json').read_text());a.update(district17_audit)
for bid in ['886305409','92204173']:a['SM_Kvarnholmen_House_'+bid]['roof']='sealed flat roof following mapped footprint and courtyard rings'
(R/'previews/district17-facades.json').write_text(json.dumps(a,indent=2,ensure_ascii=False))
