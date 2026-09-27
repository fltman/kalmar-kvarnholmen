from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
head=(R/'scripts/build_pass18.py').read_text();head=head[:head.index("for filename in ['build_pass18_landmarks.py'")];exec(compile(head,'pass18_helpers','exec'))
tree=ast.parse((R/'scripts/build_pass18_extra.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='outside_box'];exec(compile(tree,'clip','exec'))
code=(R/'scripts/build_street22.py').read_text();exec(compile(code[:code.index('# Pale three-storey Kaggensgatan/Fiskaregatan corner')],'street22_joinery','exec'))
# Pass 55 reuses the pass 26 and 28-54 helpers, which rebuild those houses unchanged, then adds
# 92379255 on the corner of Storgatan and Västra Sjögatan. Only the pass 55 mesh is exported.
exec(compile((R/'scripts/build_larm26.py').read_text(),'build_larm26.py','exec'))
exec(compile((R/'scripts/build_block28.py').read_text(),'build_block28.py','exec'))
exec(compile((R/'scripts/build_block29.py').read_text(),'build_block29.py','exec'))
exec(compile((R/'scripts/build_block30.py').read_text(),'build_block30.py','exec'))
exec(compile((R/'scripts/build_block31.py').read_text(),'build_block31.py','exec'))
exec(compile((R/'scripts/build_block32.py').read_text(),'build_block32.py','exec'))
exec(compile((R/'scripts/build_block33.py').read_text(),'build_block33.py','exec'))
exec(compile((R/'scripts/build_block34.py').read_text(),'build_block34.py','exec'))
exec(compile((R/'scripts/build_block35.py').read_text(),'build_block35.py','exec'))
exec(compile((R/'scripts/build_block36.py').read_text(),'build_block36.py','exec'))
exec(compile((R/'scripts/build_block37.py').read_text(),'build_block37.py','exec'))
exec(compile((R/'scripts/build_block38.py').read_text(),'build_block38.py','exec'))
exec(compile((R/'scripts/build_block39.py').read_text(),'build_block39.py','exec'))
exec(compile((R/'scripts/build_block40.py').read_text(),'build_block40.py','exec'))
exec(compile((R/'scripts/build_block41.py').read_text(),'build_block41.py','exec'))
exec(compile((R/'scripts/build_block42.py').read_text(),'build_block42.py','exec'))
exec(compile((R/'scripts/build_block43.py').read_text(),'build_block43.py','exec'))
exec(compile((R/'scripts/build_block44.py').read_text(),'build_block44.py','exec'))
exec(compile((R/'scripts/build_block45.py').read_text(),'build_block45.py','exec'))
exec(compile((R/'scripts/build_block46.py').read_text(),'build_block46.py','exec'))
exec(compile((R/'scripts/build_block47.py').read_text(),'build_block47.py','exec'))
exec(compile((R/'scripts/build_block48.py').read_text(),'build_block48.py','exec'))
exec(compile((R/'scripts/build_block49.py').read_text(),'build_block49.py','exec'))
exec(compile((R/'scripts/build_block50.py').read_text(),'build_block50.py','exec'))
exec(compile((R/'scripts/build_block51.py').read_text(),'build_block51.py','exec'))
exec(compile((R/'scripts/build_block52.py').read_text(),'build_block52.py','exec'))
exec(compile((R/'scripts/build_block53.py').read_text(),'build_block53.py','exec'))
exec(compile((R/'scripts/build_block54.py').read_text(),'build_block54.py','exec'))
exec(compile((R/'scripts/build_block55.py').read_text(),'build_block55.py','exec'))
# The rebuilt pass 26/28-54 meshes get the same export preparation as before (so the saved blend
# matches their repeatability hashes), but only the pass 55 mesh is written out.
extension_names=larm26_names+block28_names+block29_names+block30_names+block31_names+block32_names+block33_names+block34_names+block35_names+block36_names+block37_names+block38_names+block39_names+block40_names+block41_names+block42_names+block43_names+block44_names+block45_names+block46_names+block47_names+block48_names+block49_names+block50_names+block51_names+block52_names+block53_names+block54_names+block55_names;extension_cameras=block55_cameras
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','block55-build.json').replace('POLISH15_BUILD_OK','BLOCK55_BUILD_OK')
cut="audit[name]['export_frame_repairs']=export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))"
assert cut in tail
tail=tail.replace(cut,"if name not in block55_names:continue\n "+cut)
exec(compile(tail,'export_block55','exec'))
report=json.loads((R/'previews/block55-build.json').read_text())
report['assets']={k:v for k,v in report['assets'].items() if k in block55_names};report['changed']=block55_names
report['prepared_unchanged']=larm26_names+block28_names+block29_names+block30_names+block31_names+block32_names+block33_names+block34_names+block35_names+block36_names+block37_names+block38_names+block39_names+block40_names+block41_names+block42_names+block43_names+block44_names+block45_names+block46_names+block47_names+block48_names+block49_names+block50_names+block51_names+block52_names+block53_names+block54_names
(R/'previews/block55-build.json').write_text(json.dumps(report,indent=2))
