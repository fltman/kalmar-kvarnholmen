stone = 'M_Portal19_Stone'
if stone not in materials:
 mat(stone,(.49,.475,.425),.84,0,'Portal19Stone')
 specs[stone]['uv_scale']=8.0
 for node in materials[stone].node_tree.nodes:
  if node.bl_idname=='ShaderNodeVectorMath' and node.operation=='SCALE':node.inputs[3].default_value=8.0

# Darker stone in the incised inscription improves legibility at street distance.
engraving='M_Portal19_Engraving'
if engraving not in materials:
 mat(engraving,(.30,.29,.26),.88,0,'Portal19Stone')
 specs[engraving].update(uv_scale=8.0,street16_tint=[.42,.42,.42])
 nodes=materials[engraving].node_tree.nodes;links=materials[engraving].node_tree.links
 for node in nodes:
  if node.bl_idname=='ShaderNodeVectorMath' and node.operation=='SCALE':node.inputs[3].default_value=8.0
 shader=nodes.get('Principled BSDF');source=shader.inputs['Base Color'].links[0].from_socket
 tint=nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.42,.42,.42,1)
 links.new(source,tint.inputs[1]);links.new(tint.outputs[0],shader.inputs['Base Color'])
