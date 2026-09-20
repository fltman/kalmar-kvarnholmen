from pathlib import Path
import unreal as u,json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'repair_polish15_materials.py').read_text(),str(P/'repair_polish15_materials.py'),'exec'),{'__file__':str(P/'repair_polish15_materials.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['59_TrippTrappTrull','88_Polish_Trio.png']]}))
