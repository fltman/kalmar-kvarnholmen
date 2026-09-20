"""Cold-reopen pass-5 visual review, without reimport or relighting."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[3]
path=R/'Unreal/Content/Python/review_hero.py'
exec(compile(path.read_text(),str(path),'exec'))
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['14_Bänksnickeri','33_Unreal_Joinery.png'],['15_Joniskt_Kapitäl','34_Unreal_Ionic.png'],['05_Interiör_Altare','35_Unreal_Interior_Pass5.png']]}))
