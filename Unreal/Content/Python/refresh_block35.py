from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'materials_block35.py').read_text(),str(P/'materials_block35.py'),'exec'),{'__file__':str(P/'materials_block35.py')})
names=json.loads((R/'previews/block35-build.json').read_text())['changed']
code=(P/'patch_pass18.py').read_text().replace('range(78,91)','range(197,205)')
exec(compile(code,str(P/'patch_pass18.py'),'exec'),{'__file__':str(P/'patch_pass18.py'),'pass18_import_only':names,'pass18_import_report':'block35-import.json'})
exec(compile((P/'audit_block35_render.py').read_text(),str(P/'audit_block35_render.py'),'exec'),{'__file__':str(P/'audit_block35_render.py')})
