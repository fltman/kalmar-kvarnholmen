from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
head=(R/'scripts/build_pass18.py').read_text();head=head[:head.index("for filename in ['build_pass18_landmarks.py'")];exec(compile(head,'pass18_helpers','exec'))
exec(compile((R/'scripts/bathhouse19_helpers.py').read_text(),'bathhouse19_helpers.py','exec'))
body=(R/'scripts/build_pass18_landmarks.py').read_text();body=body[body.index('# Varmbadhuset:'):]
exec(compile(body,'bathhouse19','exec'))
extension_names=pass18_names;extension_cameras=[]
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','bathhouse19-build.json').replace('POLISH15_BUILD_OK','BATHHOUSE19_BUILD_OK')
exec(compile(tail,'export_gerdas','exec'))
