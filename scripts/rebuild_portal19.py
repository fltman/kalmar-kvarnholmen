from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
head=(R/'scripts/build_pass18.py').read_text();head=head[:head.index("for filename in ['build_pass18_landmarks.py'")];exec(compile(head,'pass18_helpers','exec'))
tree=ast.parse((R/'scripts/build_pass18_extra.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='outside_box'];exec(compile(tree,'clip','exec'))
exec(compile((R/'scripts/build_pass18_gerdas.py').read_text(),'gerdas','exec'))
extension_names=pass18_names;extension_cameras=[('89_Gerdas',(-116.8,1.4,3.5),(-122.8,-8.46,9.0),14.5),('90_Gerdas_Portal',(-122.8,-2.5,2.1),(-122.8,-8.46,3.1),28)]
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','portal19-build.json').replace('POLISH15_BUILD_OK','PORTAL19_BUILD_OK')
exec(compile(tail,'export_gerdas','exec'))
