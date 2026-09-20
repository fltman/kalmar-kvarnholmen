from pathlib import Path
import unreal as u,json,time
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'touchup_street16_roof.py').read_text(),str(P/'touchup_street16_roof.py'),'exec'),{'__file__':str(P/'touchup_street16_roof.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/street16-after-shots-start.json').write_text(json.dumps({'time':time.time()}))
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['36_Storgatan_Kaggensgatan','99_Street16_Middle.png'],['37_Larmtorget_Storgatan','100_Street16_Entrance.png'],['69_Storgatan_Portal','101_Street16_Portal.png'],['70_Storgatan_Sodra','102_Street16_South.png']]}))
