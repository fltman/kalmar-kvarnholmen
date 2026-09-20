from pathlib import Path
import runpy
folder=Path(__file__).resolve().parent
for name in ['validate_kvarnholmen.py','audit_kvarnholmen_render.py']:
 runpy.run_path(str(folder/name))
