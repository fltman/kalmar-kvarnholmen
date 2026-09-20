"""Resume final street-corner review from saved assets, without reimporting."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
u.SystemLibrary.execute_console_command(world,'t.MaxFPS 30')
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['106_KaggensCorner22','street22-corner-final-unreal.png']]}))
