import unreal as u,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[3]
report=json.loads((R/'previews/kvarnholmen-render-audit.json').read_text())
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
changed=[]
for name,v in report['meshes'].items():
 if not v['zero_tangents']:continue
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name)
 build=smes.get_lod_build_settings(mesh,0);build.recompute_tangents=True;build.use_mikk_t_space=False
 smes.set_lod_build_settings(mesh,0,build);u.EditorAssetLibrary.save_loaded_asset(mesh);changed.append(name)
(R/'previews/kvarnholmen-tangent-fixes.json').write_text(json.dumps(changed,indent=2))
runpy.run_path(str(R/'Unreal/Content/Python/audit_kvarnholmen_render.py'))
