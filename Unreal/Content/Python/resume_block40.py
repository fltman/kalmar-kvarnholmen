from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'refresh_block40.py').read_text(),str(P/'refresh_block40.py'),'exec'),{'__file__':str(P/'refresh_block40.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
# Pass 40 views: the white corner house at Östra Sjögatan.
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[[c['name'],'block40-'+c['name']+'.png'] for c in json.loads((R/'exports/manifest.json').read_text())['cameras'] if 235<=int(c['name'].split('_')[0])<=240]}))
