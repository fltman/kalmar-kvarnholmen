"""Selective source/export update, preserving all other authored scene objects."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
base=(R/'scripts/rebuild_larmtorget.py').read_text()
marker="exec(compile((R/'scripts/build_larmtorget_facades.py').read_text()"
exec(compile(base[:base.index(marker)],str(R/'scripts/rebuild_larmtorget.py'),'exec'))
exec(compile((R/'scripts/build_street16.py').read_text(),str(R/'scripts/build_street16.py'),'exec'))
extension_names=street16_names;extension_cameras=street16_cameras
(R/'previews/street16-facades.json').write_text(json.dumps(street16_audit,indent=2))
tail=(R/'scripts/rebuild_polish15.py').read_text()
tail=tail[tail.index("exec(compile((R/'scripts/district_tangent_export.py')"):]
tail=tail.replace('polish15-build.json','street16-build.json').replace('POLISH15_BUILD_OK','STREET16_BUILD_OK').replace('EXPORT15','EXPORT16')
exec(compile(tail,str(R/'scripts/rebuild_street16.py'),'exec'))
