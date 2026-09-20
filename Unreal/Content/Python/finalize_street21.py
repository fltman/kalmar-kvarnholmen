from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['refresh_street21.py','validate_street21.py']:
 path=P/name;exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
