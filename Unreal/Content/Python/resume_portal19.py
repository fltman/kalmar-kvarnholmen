from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'refresh_portal19.py').read_text(),str(P/'refresh_portal19.py'),'exec'),{'__file__':str(P/'refresh_portal19.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['90_Gerdas_Portal','portal19-close.png'],['89_Gerdas','portal19-facade.png']]}))
