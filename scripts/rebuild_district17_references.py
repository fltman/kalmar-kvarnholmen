from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text();marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()"
exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
district17_only=['SM_Kvarnholmen_House_'+bid for bid in ['93238156','90859847','91926329','92379265','92412873']]
exec(compile((R/'scripts/build_district17.py').read_text(),str(R/'scripts/build_district17.py'),'exec'))
extension_names=district17_names;extension_cameras=district17_cameras
tail=(R/'scripts/rebuild_polish15.py').read_text();tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):];tail=tail.replace('polish15-build.json','district17-reference-build.json').replace('POLISH15_BUILD_OK','DISTRICT17_BUILD_OK').replace('EXPORT15','EXPORT17')
exec(compile(tail,str(R/'scripts/rebuild_district17.py'),'exec'))
