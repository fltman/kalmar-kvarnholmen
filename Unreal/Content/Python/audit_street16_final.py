from pathlib import Path
P=Path(__file__).resolve().parent
text=(P/'audit_polish15_render.py').read_text().replace('polish15-build.json','street16-build.json').replace('polish15-render-audit.json','street16-render-audit.json')
exec(compile(text,str(P/'audit_polish15_render.py'),'exec'),{'__file__':str(P/'audit_polish15_render.py')})
