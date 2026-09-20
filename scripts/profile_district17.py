from pathlib import Path
import json,csv,statistics
R=Path(__file__).resolve().parents[1];start=json.loads((R/'previews/district17-performance-start.json').read_text())['time'];files=[p for p in (R/'Unreal/Saved/Profiling/CSV').glob('*.csv') if p.stat().st_mtime>start];p=max(files,key=lambda p:p.stat().st_mtime)
with p.open() as f:rows=list(csv.DictReader(f))
elapsed=0;frames=[];gpu=[];rendered=0
for row in rows:
 try:dt=float(row.get('FrameTime',0));g=float(row.get('GPUTime',0));base=float(row.get('Exclusive/RenderThread/RenderBasePass',0))+float(row.get('Exclusive/AllWorkers/RenderBasePass',0))
 except (ValueError,TypeError):continue
 elapsed+=dt/1000
 if elapsed>8 and dt>0 and g>0 and base>0:frames.append(dt);gpu.append(g);rendered+=1
q=lambda a: {'median_ms':statistics.median(a),'p95_ms':sorted(a)[int(.95*(len(a)-1))]} if a else None
report={'status':'measured_editor_only' if frames else 'invalid_no_rendered_frames','source_csv':str(p.relative_to(R)),'context':'Stationary Fiskaregatan editor viewport; current viewport resolution and scalability, not packaged gameplay or controlled before/after comparison.','warmup_seconds':8,'rendered_frames':rendered,'frame_time':q(frames),'gpu_time':q(gpu),'approx_median_fps':1000/statistics.median(frames) if frames else None};(R/'previews/district17-performance.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
