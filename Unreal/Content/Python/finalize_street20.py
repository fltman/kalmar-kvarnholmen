from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['refresh_street20.py','validate_street20.py']:
 path=P/name;exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
