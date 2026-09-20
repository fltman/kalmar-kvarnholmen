from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
if not (R/'previews/district17-materials.json').exists():exec(compile((P/'materials_district17.py').read_text(),str(P/'materials_district17.py'),'exec'),{'__file__':str(P/'materials_district17.py')})
excluded={'93238156','90859847','91926329','92379265','92412873'}
names=[n for n in json.loads((R/'previews/district17-build.json').read_text())['changed'] if n.split('_')[-1] not in excluded]
exec(compile((P/'patch_district17.py').read_text(),str(P/'patch_district17.py'),'exec'),{'__file__':str(P/'patch_district17.py'),'district17_import_only':names,'district17_import_report':'district17-import-main.json'})
