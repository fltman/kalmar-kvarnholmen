from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'review_scene.py').read_text(),str(P/'review_scene.py'),'exec'))
(R/'previews/review-request.json').write_text(json.dumps({'shots':[['04_Domkyrkan','13_Unreal_Church_Detail.png'],['08_Kyrkoportal','14_Unreal_Portal_Detail.png'],['09_Altardetalj','15_Unreal_Altar_Detail.png'],['10_Orgel_Läktare','16_Unreal_Organ_Detail.png'],['11_Taköversikt','17_Unreal_Roof_Detail.png'],['06_Interiör_Orgel','10_Unreal_Organ.png'],['01_Stortorget','04_Unreal_Stortorget.png'],['05_Interiör_Altare','09_Unreal_Interior.png']]}))
