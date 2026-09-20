import unreal as u,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[3]
exec(compile((R/'Unreal/Content/Python/review_hero.py').read_text(),str(R/'Unreal/Content/Python/review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'execute':'check_kvarnholmen.py','shots':[['46_Kvarnholmen_Hela','67_Kvarnholmen_Overview.png'],['47_Sodra_Langgatan','68_Sodra_Langgatan.png'],['49_Fiskaregatan','69_Fiskaregatan.png'],['50_Ostra_Kvarnholmen','70_Ostra_Kvarnholmen.png'],['52_Skeppsbron','71_Skeppsbron.png'],['53_Kvarnholmen_Fagelvy','72_Kvarnholmen_East_Overview.png']]}))
