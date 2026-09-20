from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()";exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
exec(compile((R/'scripts/build_pass18.py').read_text(),str(R/'scripts/build_pass18.py'),'exec'))
extension_names=pass18_names;extension_cameras=pass18_cameras
# The same narrow export/audit stage used by the established incremental builds.
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','pass18-build.json').replace('POLISH15_BUILD_OK','PASS18_BUILD_OK').replace('EXPORT15','EXPORT18')
exec(compile(tail,str(R/'scripts/rebuild_pass18.py'),'exec'))
