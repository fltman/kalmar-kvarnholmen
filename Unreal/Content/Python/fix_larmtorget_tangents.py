"""Preserve explicit tangent frames on the detailed Frimurarhuset and its fallback mesh."""
import unreal as u,json,math,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3]
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem);mesh=u.load_asset('/Game/Kalmar/Meshes/SM_Storgatan_Frimurarehotellet')
report={'status':'updating'}
try:
 n=smes.get_nanite_settings(mesh);report['before']={'explicit_tangents':n.explicit_tangents,'fallback_relative_error':n.fallback_relative_error}
 build=smes.get_lod_build_settings(mesh,0);build.recompute_tangents=True;build.use_mikk_t_space=True;smes.set_lod_build_settings(mesh,0,build)
 n.fallback_target=type(n.fallback_target).RELATIVE_ERROR
 n.explicit_tangents=True;n.generate_fallback=type(n.generate_fallback).ENABLED;n.fallback_relative_error=0.0
 smes.set_nanite_settings(mesh,n,True);u.EditorAssetLibrary.save_loaded_asset(mesh)
 report['after']={'explicit_tangents':smes.get_nanite_settings(mesh).explicit_tangents,'fallback_relative_error':smes.get_nanite_settings(mesh).fallback_relative_error}
 report['status']='saved';report['sections']=[]
 if hasattr(u,'ProceduralMeshLibrary'):
  for i in range(mesh.get_num_sections(0)):
   vs,tris,ns,uvs,ts=u.ProceduralMeshLibrary.get_section_from_static_mesh(mesh,0,i)
   lengths=[math.sqrt(t.tangent_x.x**2+t.tangent_x.y**2+t.tangent_x.z**2) for t in ts]
   report['sections'].append({'section':i,'vertices':len(vs),'zero_tangents':sum(v<1e-4 for v in lengths),'minimum_length':min(lengths) if lengths else None})
  report['status']='passed' if report['sections'] and not any(s['zero_tangents'] for s in report['sections']) else 'failed'
except Exception:report['status']='error';report['error']=traceback.format_exc()
(R/'previews/larmtorget-tangents-unreal.json').write_text(json.dumps(report,indent=2))
