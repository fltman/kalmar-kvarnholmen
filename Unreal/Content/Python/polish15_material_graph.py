"""Low-frequency world-space variation and localized dampening, without baked illumination."""
import unreal as u
from pathlib import Path
def enhance(m,spec,root,importer):
 e=u.MaterialEditingLibrary;c=spec['polish15'];texname=spec['texture'];nodes={}
 def node(cls,x=0,y=0):return e.create_material_expression(m,cls,x,y)
 def connect(a,b,key,output=''):
  pins=list(e.get_material_expression_input_names(b))
  if key in ['Input','Coordinates'] and key not in pins:key=pins[0]
  if not e.connect_material_expressions(a,output,b,key):raise RuntimeError('Cannot connect '+b.get_class().get_name()+' pin '+key+'; pins='+str(pins))
 def scalar(v):
  n=node(u.MaterialExpressionConstant);n.set_editor_property('r',v);return n
 base=e.get_material_property_input_node(m,u.MaterialProperty.MP_BASE_COLOR)
 uv=node(u.MaterialExpressionTextureCoordinate,-1300,800);uv.u_tiling=uv.v_tiling=spec.get('uv_scale',1)
 ao=importer(Path(root)/'exports/textures'/('T_'+texname+'_AO.png'),'/Game/Kalmar/Textures','T_'+texname+'_AO');ao.set_editor_property('srgb',False);u.EditorAssetLibrary.save_loaded_asset(ao)
 sample=node(u.MaterialExpressionTextureSample,-1100,800);sample.texture=ao;sample.sampler_type=u.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR;connect(uv,sample,'Coordinates');e.connect_material_property(sample,'R',u.MaterialProperty.MP_AMBIENT_OCCLUSION)
 world=node(u.MaterialExpressionWorldPosition,-1700,1100)
 mask=node(u.MaterialExpressionComponentMask,-1500,1100);mask.set_editor_property('r',True);mask.set_editor_property('g',True);mask.set_editor_property('b',False);mask.set_editor_property('a',False);connect(world,mask,'Input')
 # Vertical materials use a diagonal horizontal coordinate and height to avoid bands.
 if c.get('damp',0)>0:
  x=node(u.MaterialExpressionComponentMask);x.set_editor_property('r',True);x.set_editor_property('g',False);x.set_editor_property('b',False);connect(world,x,'Input')
  yz=node(u.MaterialExpressionComponentMask);yz.set_editor_property('r',False);yz.set_editor_property('g',True);yz.set_editor_property('b',True);connect(world,yz,'Input')
  blend=node(u.MaterialExpressionAdd);connect(yz,blend,'A');connect(x,blend,'B');mask=blend
 divide=node(u.MaterialExpressionDivide);divide.set_editor_property('const_b',1800);connect(mask,divide,'A')
 tex=importer(Path(root)/'exports/textures/T_Polish15Macro.png','/Game/Kalmar/Textures','T_Polish15Macro');tex.set_editor_property('srgb',False);u.EditorAssetLibrary.save_loaded_asset(tex)
 noise=node(u.MaterialExpressionTextureSample,-1100,1100);noise.texture=tex;noise.sampler_type=u.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR;connect(divide,noise,'Coordinates')
 mult=node(u.MaterialExpressionMultiply);mult.set_editor_property('const_b',c['macro']*2);connect(noise,mult,'A','R')
 add=node(u.MaterialExpressionAdd);add.set_editor_property('const_b',1-c['macro']);connect(mult,add,'A')
 result=node(u.MaterialExpressionMultiply,-350,0);connect(base,result,'A','RGB');connect(add,result,'B')
 if c.get('damp',0)>0:
  z=node(u.MaterialExpressionComponentMask);z.set_editor_property('r',False);z.set_editor_property('g',False);z.set_editor_property('b',True);connect(world,z,'Input')
  div=node(u.MaterialExpressionDivide);div.set_editor_property('const_b',120);connect(z,div,'A')
  clamp=node(u.MaterialExpressionClamp);clamp.set_editor_property('min_default',0);clamp.set_editor_property('max_default',1);connect(div,clamp,'Input')
  lerp=node(u.MaterialExpressionLinearInterpolate);lerp.set_editor_property('const_a',1-c['damp']);lerp.set_editor_property('const_b',1);connect(clamp,lerp,'Alpha')
  final=node(u.MaterialExpressionMultiply,-100,0);connect(result,final,'A');connect(lerp,final,'B');result=final
 e.connect_material_property(result,'',u.MaterialProperty.MP_BASE_COLOR)
