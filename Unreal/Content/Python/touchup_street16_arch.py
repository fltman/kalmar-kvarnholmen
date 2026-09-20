from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'patch_street16.py').read_text(),str(P/'patch_street16.py'),'exec'),{'__file__':str(P/'patch_street16.py'),'street16_import_only':['SM_Building_92204194'],'street16_import_report':'street16-arch-import.json'})
