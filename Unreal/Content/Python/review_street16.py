"""Resume visual QA without rebuilding materials or resetting lighting."""
from pathlib import Path
import unreal as u,json,time
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/street16-before-start.json').write_text(json.dumps({'time':time.time()}))
(R/'previews/hero-review-request.json').write_text(json.dumps({'view':'36_Storgatan_Kaggensgatan','performance':True,'shots':[['36_Storgatan_Kaggensgatan','97_Street16_Before_Middle.png'],['37_Larmtorget_Storgatan','98_Street16_Before_Entrance.png']]}))
