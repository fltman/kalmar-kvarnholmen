from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
exec(compile((P/'refresh_block31.py').read_text(),str(P/'refresh_block31.py'),'exec'),{'__file__':str(P/'refresh_block31.py')})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
# Pass 31 views: Larmgatan 16.
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':[[c['name'],'block31-'+c['name']+'.png'] for c in json.loads((R/'exports/manifest.json').read_text())['cameras'] if 176<=int(c['name'].split('_')[0])<=178]}))
