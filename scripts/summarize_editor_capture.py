"""Read native Unreal CSV timing; reject captures without rendered geometry."""
import csv,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1]
path=max((R/'Unreal/Saved/Profiling/CSV').glob('*.csv'),key=lambda p:p.stat().st_mtime)
with path.open() as f:rows=list(csv.DictReader(f))
elapsed=0;frames=[];draws=[];gpu=[]
gpu_keys=[k for k in rows[0] if k and (k=='GPUTime' or ('gpu' in k.lower() and ('frame' in k.lower() or k.lower()=='gpu')))]
for row in rows:
 try:dt=float(row.get('FrameTime',''));draw=float(row.get('RHI/DrawCalls','0'))
 except (TypeError,ValueError):continue
 if dt<=0:continue
 elapsed+=dt
 if elapsed<8000:continue
 # Metal does not populate the RHI draw-call counters in this editor build.
 # Require an actual scene base pass plus native GPU timing in that case.
 basepass=float(row.get('Exclusive/RenderThread/RenderBasePass','0') or 0)
 native_gpu=float(row.get('GPUTime','0') or 0)
 if draw>0 or (basepass>0 and native_gpu>0):
  frames.append(dt);draws.append(draw)
  for key in gpu_keys:
   try:v=float(row[key])
   except (TypeError,ValueError):continue
   if v>0:gpu.append(v);break
def summary(values):
 return {'median_ms':statistics.median(values),'p95_ms':sorted(values)[int(.95*(len(values)-1))]} if values else None
config=json.loads((R/'previews/hero-lighting-config.json').read_text())
result={'status':'measured_editor_only' if len(frames)>30 else 'inconclusive','source_csv':str(path.relative_to(R)),'context':'Unreal 5.8 editor viewport, fixed altar camera, background CPU throttle disabled; not packaged gameplay','warmup_seconds':8,'rendered_frames':len(frames),'frame_time':summary(frames),'gpu_time':summary(gpu),'median_draw_calls':statistics.median(draws) if draws and max(draws)>0 else None,'requested_screen_percentage':config['screen_percentage'],'quality':config.get('quality','original'),'note':'Metal draw counters are unavailable; rendering checked by native GPUTime and scene base-pass events. No packaged performance guarantee.'}
(R/'previews/hero-native-performance.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
