import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'));M=json.loads((R/'exports/manifest.json').read_text());M['materials'].update(json.loads((R/'source/polish15-extra-materials.json').read_text()))
for name,sp in json.loads((R/'source/polish15-extra-materials.json').read_text()).items():
 ma=bpy.data.materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;nodes.clear();p=nodes.new('ShaderNodeBsdfPrincipled');out=nodes.new('ShaderNodeOutputMaterial');links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Metallic'].default_value=sp['metallic'];uv=nodes.new('ShaderNodeTexCoord');scale=nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=sp['uv_scale'];links.new(uv.outputs['UV'],scale.inputs[0])
 for suf,socket in [('BaseColor','Base Color'),('Normal','Normal'),('Roughness','Roughness')]:
  n=nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/f'exports/textures/T_{sp["texture"]}_{suf}.png'),check_existing=True);links.new(scale.outputs[0],n.inputs['Vector'])
  if suf!='BaseColor':n.image.colorspace_settings.name='Non-Color'
  if suf=='Normal':nm=nodes.new('ShaderNodeNormalMap');links.new(n.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs[0],p.inputs['Normal'])
  else:links.new(n.outputs['Color'],p.inputs[socket])
# Store complete recipes separately so full-scene regeneration can reproduce the pass.
C=json.loads((R/'source/polish15-materials.json').read_text());C.update(json.loads((R/'source/polish15-extra-materials.json').read_text()));recipes={n:M['materials'][n] for n in C};(R/'source/polish15-material-specs.json').write_text(json.dumps(recipes,indent=2));(R/'exports/manifest.json').write_text(json.dumps(M,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'));print('POLISH15_SOURCE_FINALIZED')
