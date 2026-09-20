"""Reimport revised pass-22 geometry without rebuilding unchanged materials."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
names=json.loads((R/'previews/street22-build.json').read_text())['changed']
code=(P/'patch_pass18.py').read_text().replace('range(78,91)','range(106,112)')
exec(compile(code,str(P/'patch_pass18.py'),'exec'),{'__file__':str(P/'patch_pass18.py'),'pass18_import_only':names,'pass18_import_report':'street22-import.json'})
for filename in ['audit_street22_render.py','validate_street22.py','prepare_public_assets.py']:
 exec(compile((P/filename).read_text(),str(P/filename),'exec'),{'__file__':str(P/filename)})
