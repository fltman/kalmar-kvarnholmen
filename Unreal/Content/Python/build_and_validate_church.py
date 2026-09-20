from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'build_stortorget.py').read_text(),str(P/'build_stortorget.py'),'exec'))
normal_report={'status':'checking','materials':{}}
for name,spec in MAN['materials'].items():
 if not str(spec.get('texture','')).startswith('Church'):continue
 mat_asset=u.load_asset(BASE+'/Materials/'+name)
 normal_node=u.MaterialEditingLibrary.get_material_property_input_node(mat_asset,u.MaterialProperty.MP_NORMAL)
 rough_node=u.MaterialEditingLibrary.get_material_property_input_node(mat_asset,u.MaterialProperty.MP_ROUGHNESS)
 tex=normal_node.texture if isinstance(normal_node,u.MaterialExpressionTextureSample) else None
 normal_report['materials'][name]={'normal_connected':tex is not None,'roughness_connected':isinstance(rough_node,u.MaterialExpressionTextureSample),'normal_texture':tex.get_name() if tex else None,'flip_green':tex.get_editor_property('flip_green_channel') if tex else None,'srgb':tex.get_editor_property('srgb') if tex else None,'compression':str(tex.get_editor_property('compression_settings')) if tex else None}
normal_report['status']='passed' if normal_report['materials'] and all(x['normal_connected'] and x['roughness_connected'] and x['flip_green'] and not x['srgb'] and 'NORMALMAP' in x['compression'] for x in normal_report['materials'].values()) else 'failed'
(ROOT/'previews/unreal-church-material-validation.json').write_text(json.dumps(normal_report,indent=2))
exec(compile((P/'validate_interior.py').read_text(),str(P/'validate_interior.py'),'exec'))
