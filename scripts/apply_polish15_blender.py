"""Shared Blender material setup for pass 15, synchronized with the Unreal importer."""
polish15_configs=json.loads((R/'source/polish15-materials.json').read_text())
if (R/'source/polish15-extra-materials.json').exists():
 for name,sp in json.loads((R/'source/polish15-extra-materials.json').read_text()).items():
  specs[name]=sp;polish15_configs[name]={'metres':32,'asset':None}
for name,c in polish15_configs.items():
 sp=specs[name];ma=materials.get(name)
 if ma is None:mat(name,sp['color'],sp['roughness'],sp['metallic'],sp['texture']);ma=materials[name]
 specs[name]=sp
 ma.use_nodes=True;nodes=ma.node_tree.nodes;links=ma.node_tree.links;nodes.clear();p=nodes.new('ShaderNodeBsdfPrincipled');out=nodes.new('ShaderNodeOutputMaterial');links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Metallic'].default_value=sp['metallic']
 texcoord=nodes.new('ShaderNodeTexCoord');scale=nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=sp['uv_scale'];links.new(texcoord.outputs['UV'],scale.inputs[0])
 for suffix,socket in [('BaseColor','Base Color'),('Roughness','Roughness'),('Normal','Normal')]:
  tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/f'exports/textures/T_{sp["texture"]}_{suffix}.png'),check_existing=True);links.new(scale.outputs[0],tex.inputs['Vector'])
  if suffix!='BaseColor':tex.image.colorspace_settings.name='Non-Color'
  if suffix=='Normal':
   nm=nodes.new('ShaderNodeNormalMap');links.new(tex.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],p.inputs['Normal'])
  else:links.new(tex.outputs['Color'],p.inputs[socket])
 ma['physical_tile_metres']=c['metres'];ma['source']=('https://polyhaven.com/a/'+c['asset']) if c['asset'] else 'Original procedural waves';ma['license']='CC0'
