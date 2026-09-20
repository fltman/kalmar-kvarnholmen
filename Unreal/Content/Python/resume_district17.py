from pathlib import Path
import unreal as u,json
P=Path(__file__).resolve().parent;R=P.parents[2]
for script in ['import_district17_batch.py','import_district17_references.py']:
 exec(compile((P/script).read_text(),str(P/script),'exec'),{'__file__':str(P/script)})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[['48_Norra_Langgatan','106_District17_Norra.png'],['49_Fiskaregatan','107_District17_Fiskaregatan.png'],['50_Ostra_Kvarnholmen','108_District17_Ostra.png'],['71_District_93238156','109_District17_Norra84.png'],['72_District_90859847','110_District17_Fiskaregatan3.png'],['73_District_91926329','111_District17_Bokbindaren.png'],['74_District_92379265','112_District17_Gesallen.png'],['75_District_92412873','113_District17_Wahlberg.png'],['35_Storgatan_Östra','114_District17_Storgatan.png'],['52_Skeppsbron','115_District17_Skeppsbron.png']]}))
