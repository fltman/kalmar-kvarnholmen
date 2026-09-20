"""Fine continuous plaster for this street; shared district materials are preserved."""
street16_material_map={}
for key,base,target in [('Yellow',(.63,.43,.19),(.70,.45,.145)),('Rose',(.49,.32,.25),(.54,.32,.295)),('Ivory',(.68,.65,.55),(.72,.69,.60))]:
 name='M_Street16_'+key
 if name not in materials:
  mat(name,target,.79,0,'Town'+key)
  ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links
  bsdf=nodes.get('Principled BSDF');source=bsdf.inputs['Base Color'].links[0].from_socket
  multiply=nodes.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1;multiply.inputs[2].default_value=(*[t/b for t,b in zip(target,base)],1)
  links.new(source,multiply.inputs[1]);links.new(multiply.outputs[0],bsdf.inputs['Base Color'])
  specs[name]['street16_tint']=[t/b for t,b in zip(target,base)]
 street16_material_map['M_Town_'+key]=name
