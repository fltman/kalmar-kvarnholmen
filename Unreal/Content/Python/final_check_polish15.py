from pathlib import Path
import runpy,json,time
P=Path(__file__).resolve().parent;R=P.parents[2]
(R/'previews/polish15-check-start.json').write_text(json.dumps({'time':time.time()}))
for filename in ['validate_polish15_materials.py','check_polish15.py']:runpy.run_path(str(P/filename))
if all(json.loads((R/'previews'/f).read_text())['status']=='passed' for f in ['polish15-materials.json','polish15-collision.json','polish15-render-audit.json','landmarks14-gates.json']):
 path=P/'walk_landmarks14.py';exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
