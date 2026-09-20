"""Continuous fine plaster and painted timber; original texture maps, no photo projection."""
D17MAT={}
for key,texture,base,target in [
 ('Ivory','TownIvory',(.68,.65,.55),(.68,.65,.56)),('Yellow','TownYellow',(.63,.43,.19),(.64,.46,.23)),('Rose','TownRose',(.49,.32,.25),(.51,.34,.28)),('Lime','TownLime',(.57,.57,.49),(.48,.51,.44)),('Grey','TownIvory',(.68,.65,.55),(.57,.59,.58)),
 ('RedJoinery','TownPaintBrown',(.19,.105,.065),(.23,.058,.032)),('SageWood','TownPanel',(.57,.58,.49),(.38,.40,.31)),('OchreWood','TownPanel',(.57,.58,.49),(.66,.47,.23))]:
 name='M_District17_'+key
 if name not in materials:
  mat(name,target,.76 if 'Joinery' not in key else .48,0,texture)
  ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');source=bsdf.inputs['Base Color'].links[0].from_socket
  multiply=nodes.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1;multiply.inputs[2].default_value=(*[t/b for t,b in zip(target,base)],1)
  links.new(source,multiply.inputs[1]);links.new(multiply.outputs[0],bsdf.inputs['Base Color']);specs[name]['street16_tint']=[t/b for t,b in zip(target,base)]
 D17MAT[key]=name
