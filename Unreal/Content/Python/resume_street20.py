from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'refresh_street20.py').read_text(),str(P/'refresh_street20.py'),'exec'),{'__file__':str(P/'refresh_street20.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['93_Kullzenska20','street20-kullzen.png'],['94_Areskogska20','street20-areskog.png'],['91_Storgatan_South20','street20-south.png'],['92_Storgatan_Orange20','street20-orange.png']]}))
