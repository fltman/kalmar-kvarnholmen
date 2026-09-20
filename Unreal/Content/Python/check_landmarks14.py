import runpy
from pathlib import Path
p=Path(__file__).parent
for name in ['validate_landmarks14.py','audit_landmarks14_render.py','check_landmark_gate_clearances.py']:runpy.run_path(str(p/name))
