import runpy
from pathlib import Path
p=Path(__file__).parent
for name in ['validate_sodra_facades.py','audit_sodra_facades_render.py']:runpy.run_path(str(p/name))
