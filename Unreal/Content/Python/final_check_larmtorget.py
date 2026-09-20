from pathlib import Path
import runpy
folder=Path(__file__).resolve().parent
for name in ['validate_larmtorget_facades.py','audit_larmtorget_render_tangents.py']:
 runpy.run_path(str(folder/name))
