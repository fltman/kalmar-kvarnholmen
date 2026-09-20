from pathlib import Path
import runpy
P=Path(__file__).resolve().parent
for name in ["validate_polish15.py","audit_polish15_render.py","check_landmark_gate_clearances.py"]:runpy.run_path(str(P/name))
