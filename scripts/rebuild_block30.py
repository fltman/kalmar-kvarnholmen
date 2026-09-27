from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
head=(R/'scripts/build_pass18.py').read_text();head=head[:head.index("for filename in ['build_pass18_landmarks.py'")];exec(compile(head,'pass18_helpers','exec'))
tree=ast.parse((R/'scripts/build_pass18_extra.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='outside_box'];exec(compile(tree,'clip','exec'))
code=(R/'scripts/build_street22.py').read_text();exec(compile(code[:code.index('# Pale three-storey Kaggensgatan/Fiskaregatan corner')],'street22_joinery','exec'))
# Pass 30 reuses the pass 26, 28 and 29 helpers, which rebuild those houses unchanged, then adds the
# Larmgatan corner building. Only the pass 30 mesh is exported.
exec(compile((R/'scripts/build_larm26.py').read_text(),'build_larm26.py','exec'))
exec(compile((R/'scripts/build_block28.py').read_text(),'build_block28.py','exec'))
exec(compile((R/'scripts/build_block29.py').read_text(),'build_block29.py','exec'))
exec(compile((R/'scripts/build_block30.py').read_text(),'build_block30.py','exec'))
# The rebuilt pass 26/28/29 meshes get the same export preparation as before (so the saved blend
# matches their repeatability hashes), but only the pass 30 mesh is written out.
extension_names=larm26_names+block28_names+block29_names+block30_names;extension_cameras=block30_cameras
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','block30-build.json').replace('POLISH15_BUILD_OK','BLOCK30_BUILD_OK')
cut="audit[name]['export_frame_repairs']=export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))"
assert cut in tail
tail=tail.replace(cut,"if name not in block30_names:continue\n "+cut)
exec(compile(tail,'export_block30','exec'))
report=json.loads((R/'previews/block30-build.json').read_text())
report['assets']={k:v for k,v in report['assets'].items() if k in block30_names};report['changed']=block30_names
report['prepared_unchanged']=larm26_names+block28_names+block29_names
(R/'previews/block30-build.json').write_text(json.dumps(report,indent=2))
