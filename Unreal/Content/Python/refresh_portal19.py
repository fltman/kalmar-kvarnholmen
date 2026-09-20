from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'materials_portal19.py').read_text(),str(P/'materials_portal19.py'),'exec'),{'__file__':str(P/'materials_portal19.py')})
exec(compile((P/'patch_pass18.py').read_text(),str(P/'patch_pass18.py'),'exec'),{'__file__':str(P/'patch_pass18.py'),'pass18_import_only':['SM_Building_92379312'],'pass18_import_report':'portal19-import.json'})
