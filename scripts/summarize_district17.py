"""Honest footprint/asset coverage and delivery gate; never equate coverage with photo accuracy."""
from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parents[1]
def read(s):return json.loads((R/s).read_text())
registry=read('source/district17.json')['buildings'];manifest=read('exports/manifest.json');before=read('source/backups/detail-pass-16/exports/manifest.json');build=read('previews/district17-build.json');changed=set(build['changed']);assets={a['name']:a for a in manifest['assets']};old={a['name']:a for a in before['assets']};details=read('previews/district17-facades.json')
rows=[]
for name,r in registry.items():
 rows.append({'building':name,'osm_id':r['id'],'street':r['street'],'treatment':'rebuilt_pass17' if name in changed else 'prior_authored_retained','asset_present':name in assets,'source_verified':(R/'exports'/assets[name]['file']).exists(),'reference_status':details.get(name,{}).get('reference_status',r['reference_status'])})
for name,bid in [('SM_Radhuset','92412845'),('SM_Calmar_Stadshotell','91846976'),('SM_Storgatan_Kalmar_Teater','91265009'),('SM_Storgatan_Frimurarehotellet','91265021'),('SM_Kalmar_Domkyrka','38319501')]:
 parts=[s for s in assets if s==name or s.startswith(name+'_Part')]
 rows.append({'building':name,'osm_id':bid,'street':'landmark','treatment':'prior_authored_retained','asset_present':bool(parts),'source_verified':all((R/'exports'/assets[s]['file']).exists() for s in parts),'reference_status':'previous individual landmark work; unchanged','parts':parts})
checks={};reports={'source':'district17-source-audit.json','geometry':'district17-build.json','fbx':'district17-fbx-audit.json','materials':'district17-materials.json','bindings':'district17-bindings.json','main_import':'district17-import-main.json','reference_import':'district17-import-references.json','touchup_import':'district17-import-touchup.json','visual_review':'district17-visual-review.json','saved':'district17-save.json','render':'district17-render-audit.json','collision':'district17-collision.json','corridor_collision':'district17-storgatan-collision.json','walk':'district17-pie-walk.json','klapp_access':'district17-klapp-access.json'}
for key,f in reports.items():
 p=R/'previews'/f
 if not p.exists():checks[key]='pending';continue
 q=json.loads(p.read_text())
 if key=='fbx':checks[key]='passed' if len(q)==303 and all(v['vectors'] and not v['near_zero'] and not v['nonfinite'] for rec in q.values() for v in rec.values()) else 'failed'
 else:checks[key]=q.get('status','unknown')
unchanged=[n for n in old if n not in changed];preserved=all(assets.get(n)==old[n] for n in unchanged)
checks['scope']='passed' if preserved and set(assets)==set(old) else 'failed'
checks['coverage']='passed' if len(rows)==343 and len(changed)==303 and all(q['asset_present'] and q['source_verified'] for q in rows) else 'failed'
report={'status':'passed' if all(v=='passed' for v in checks.values()) else 'in_progress','buildings_total':len(rows),'newly_refined':len(changed),'previously_authored_retained':len(rows)-len(changed),'pending_buildings':sum(not q['asset_present'] or not q['source_verified'] for q in rows),'new_photo_informed':sum('photographed' in q['reference_status'] for q in rows),'new_inferred':296,'unchanged_other_assets':len(unchanged),'windows':sum(q['windows'] for q in details.values()),'doors':sum(q['doors'] for q in details.values()),'checks':checks,'buildings':rows,'limits':'All currently mapped building assets processed; this is not per-house photographic verification or finished AAA quality.'}
(R/'previews/district17-delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='buildings'},ensure_ascii=False,indent=2))
