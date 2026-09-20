from pathlib import Path
import unreal as u,json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['48_Norra_Langgatan','103_District17_Before_Norra.png'],['49_Fiskaregatan','104_District17_Before_Fiskaregatan.png'],['50_Ostra_Kvarnholmen','105_District17_Before_Ostra.png']]}))
