"""Incremental corridor build: preserve all existing authored objects outside its scope."""
import bpy,bmesh,math,json,ast,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/polish15-working.blend'))
scene=bpy.context.scene;materials={m.name:m for m in bpy.data.materials}
manifest=json.loads((R/'source/polish15-working.json').read_text())['manifest'];specs=manifest['materials'];CHURCH_TEXTURES={}
tree=ast.parse((R/'scripts/build_blender.py').read_text())
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='mat':
  for target in n.targets:
   if isinstance(target,ast.Name):globals()[target.id]=ast.literal_eval(n.value.args[0])
tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in {'mat','Mesh','wallbox','window','hip','pediment','roundwindow'}]
exec(compile(tree,'production_core','exec'))
town_mats={name.removeprefix('M_Town_'):name for name in materials if name.startswith('M_Town_') and '.' not in name}
TI,TL,TY,TS=[town_mats[k] for k in ['Ivory','Lime','Yellow','Stone']]
TW,TB,TG,TT,TC=[town_mats[k] for k in ['PaintWhite','PaintBlue','PaintGreen','TileRed','Copper']]
for filename in ['build_town_details.py','town_detail_helpers.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 exec(compile(tree,filename,'exec'))

BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];lp=facade_point
for filename in ['build_larmtorget_facades.py','build_sodra_facades.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(tree,filename,'exec'))
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];lp=facade_point
SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']};OW='M_Landmark_OliveWood'
exec(compile((R/'scripts/build_facades15.py').read_text(),'build_facades15.py','exec'))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/polish15-working.blend'))
exec(compile((R/'scripts/export_polish15.py').read_text(),str(R/'scripts/export_polish15.py'),'exec'))
