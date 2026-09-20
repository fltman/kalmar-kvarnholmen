"""Render-frame integrity plus continuous walking clearance after pass 16."""
from pathlib import Path
P=Path(__file__).resolve().parent
text=(P/'audit_polish15_render.py').read_text().replace('polish15-build.json','street16-build.json').replace('polish15-render-audit.json','street16-render-audit.json')
exec(compile(text,str(P/'audit_polish15_render.py'),'exec'),{'__file__':str(P/'audit_polish15_render.py')})
text=(P/'validate_storgatan.py').read_text().replace('storgatan-collision.json','street16-collision.json')
exec(compile(text,str(P/'validate_storgatan.py'),'exec'),{'__file__':str(P/'validate_storgatan.py')})
text=(P/'walk_storgatan.py').read_text().replace('storgatan-pie-walk.json','street16-pie-walk.json')
exec(compile(text,str(P/'walk_storgatan.py'),'exec'),{'__file__':str(P/'walk_storgatan.py')})
