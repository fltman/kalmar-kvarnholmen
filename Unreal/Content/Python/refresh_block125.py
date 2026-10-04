from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'materials_block125.py').read_text(),str(P/'materials_block125.py'),'exec'),{'__file__':str(P/'materials_block125.py')})
names=json.loads((R/'previews/block125-build.json').read_text())['changed']
code=(P/'patch_pass18.py').read_text().replace('range(78,91)','range(671,679)')
exec(compile(code,str(P/'patch_pass18.py'),'exec'),{'__file__':str(P/'patch_pass18.py'),'pass18_import_only':names,'pass18_import_report':'block125-import.json'})
exec(compile((P/'audit_block125_render.py').read_text(),str(P/'audit_block125_render.py'),'exec'),{'__file__':str(P/'audit_block125_render.py')})
