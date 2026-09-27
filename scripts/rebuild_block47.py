from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
head=(R/'scripts/build_pass18.py').read_text();head=head[:head.index("for filename in ['build_pass18_landmarks.py'")];exec(compile(head,'pass18_helpers','exec'))
tree=ast.parse((R/'scripts/build_pass18_extra.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='outside_box'];exec(compile(tree,'clip','exec'))
code=(R/'scripts/build_street22.py').read_text();exec(compile(code[:code.index('# Pale three-storey Kaggensgatan/Fiskaregatan corner')],'street22_joinery','exec'))
# Pass 47 reuses the pass 26 and 28-46 helpers, which rebuild those houses unchanged, then adds
# 92379306 and 92379253 on the north side of Ölandsgatan. Only the pass 47 meshes are exported.
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
# The rebuilt pass 26/28-46 meshes get the same export preparation as before (so the saved blend
# matches their repeatability hashes), but only the pass 47 meshes are written out.
extension_names=larm26_names+block28_names+block29_names+block30_names+block31_names+block32_names+block33_names+block34_names+block35_names+block36_names+block37_names+block38_names+block39_names+block40_names+block41_names+block42_names+block43_names+block44_names+block45_names+block46_names+block47_names;extension_cameras=block47_cameras
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','block47-build.json').replace('POLISH15_BUILD_OK','BLOCK47_BUILD_OK')
cut="audit[name]['export_frame_repairs']=export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))"
assert cut in tail
tail=tail.replace(cut,"if name not in block47_names:continue\n "+cut)
exec(compile(tail,'export_block47','exec'))
report=json.loads((R/'previews/block47-build.json').read_text())
report['assets']={k:v for k,v in report['assets'].items() if k in block47_names};report['changed']=block47_names
report['prepared_unchanged']=larm26_names+block28_names+block29_names+block30_names+block31_names+block32_names+block33_names+block34_names+block35_names+block36_names+block37_names+block38_names+block39_names+block40_names+block41_names+block42_names+block43_names+block44_names+block45_names+block46_names
(R/'previews/block47-build.json').write_text(json.dumps(report,indent=2))
