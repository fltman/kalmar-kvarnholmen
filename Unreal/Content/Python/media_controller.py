"""Local media-export dispatcher; keeps render callbacks alive in the current editor."""
import unreal as u,json,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent
u.EditorPythonScripting.set_keep_python_script_alive(True)
media_runs=[];media_stamp=None;media_last=0
def media_tick(dt):
 global media_stamp,media_last
 if time.monotonic()-media_last<.4:return
 media_last=time.monotonic();p=R/'media/request.json'
 if not p.exists() or p.stat().st_mtime_ns==media_stamp:return
 media_stamp=p.stat().st_mtime_ns
 try:
  d=json.loads(p.read_text());s=(P/d['execute']).resolve();assert s.parent==P.resolve()
  ns={'__file__':str(s)};media_runs.append(ns);exec(compile(s.read_text(),str(s),'exec'),ns)
  (R/'media/command-status.json').write_text(json.dumps({'status':'started','script':s.name}))
 except Exception:(R/'media/command-status.json').write_text(json.dumps({'status':'error','traceback':traceback.format_exc()}))
media_handle=u.register_slate_post_tick_callback(media_tick)
(R/'media/controller-ready.json').write_text(json.dumps({'ready':True}))
