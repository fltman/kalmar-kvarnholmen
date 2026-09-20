"""Parse an isolated, same-camera before/after editor capture."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
phase=sys.argv[1] if len(sys.argv)>1 else 'after'
assert phase in ['before','after']
text=(R/'scripts/profile_polish15.py').read_text().replace('polish15-performance-start.json',f'street16-performance-{phase}-start.json').replace('polish15-performance.json',f'street16-performance-{phase}.json')
text=text.replace('Stationary Fiskaregatan editor viewport; current viewport resolution and scalability, not packaged gameplay or controlled before/after comparison.','Stationary 36_Storgatan_Kaggensgatan editor viewport, same camera and settings for before/after; no concurrent screenshots or Blender build. Eight-second warmup; not packaged gameplay. Background OS activity may affect comparison.')
exec(compile(text,str(R/'scripts/profile_polish15.py'),'exec'),{'__file__':str(R/'scripts/profile_polish15.py')})
