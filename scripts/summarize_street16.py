from pathlib import Path
import json,time
R=Path(__file__).resolve().parents[1];P=R/'previews'
files={'build':'street16-build.json','scope':'street16-scope.json','import':'street16-import.json','roof':'street16-roof-import.json','materials':'street16-materials.json','render':'street16-render-audit.json','collision':'street16-collision.json','walk':'street16-pie-walk.json'}
reports={k:json.loads((P/f).read_text()) for k,f in files.items()}
files['arch']='street16-arch-import.json';reports['arch']=json.loads((P/files['arch']).read_text())
checks={k:v.get('status')=='passed' for k,v in reports.items()}
fbx=json.loads((P/'street16-fbx-audit.json').read_text())
checks['fbx']=all(x['vectors'] and not x['near_zero'] and not x['nonfinite'] for v in fbx.values() for x in v.values())
checks['no_review_error']=not any((P/f).exists() for f in ['hero-review-error.txt','hero-review-command-error.txt'])
start=json.loads((P/'street16-after-shots-start.json').read_text())['time']
images=['99_Street16_Middle.png','100_Street16_Entrance.png','101_Street16_Portal.png','102_Street16_South.png']
checks['fresh_images']=all((P/f).stat().st_mtime>=start for f in images)
facades=json.loads((P/'street16-facades.json').read_text())
report={'status':'passed' if all(checks.values()) else 'review_required','time':time.time(),'checks':checks,'reports':files,'buildings':9,'frontages':sum(v['fronts'] for v in facades.values()),'upper_windows':sum(v['windows'] for v in facades.values()),'commercial_bays':sum(v['shops'] for v in facades.values()),'entrances':sum(v['doors'] for v in facades.values()),'unchanged_geometry_assets':553,'new_plaster_materials':3,'images':images,'limits':['Nine western Storgatan houses revised; eastern corridor and previously detailed square landmarks preserved.','June 2020 panorama and May 2022 photo references; heights, obscured sides and fine ornaments are visual estimates.','Further vegetation, retail interiors, street life and performance work remain; not finished AAA quality.']}
for phase in ['before','after']:
 f=P/f'street16-performance-{phase}.json'
 if f.exists():report['performance_'+phase]=json.loads(f.read_text())
(P/'street16-delivery.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
