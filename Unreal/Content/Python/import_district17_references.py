from pathlib import Path
P=Path(__file__).resolve().parent
names=['SM_Kvarnholmen_House_'+bid for bid in ['93238156','90859847','91926329','92379265','92412873','91072716','886305409','92204173','93199604']]
exec(compile((P/'patch_district17.py').read_text(),str(P/'patch_district17.py'),'exec'),{'__file__':str(P/'patch_district17.py'),'district17_import_only':names,'district17_import_report':'district17-import-references.json'})
