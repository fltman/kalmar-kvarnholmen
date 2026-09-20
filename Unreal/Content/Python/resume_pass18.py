from pathlib import Path
import unreal as u,json
P=Path(__file__).resolve().parent;R=P.parents[2]
for script in ['materials_pass18.py','patch_pass18.py']:
 exec(compile((P/script).read_text(),str(P/script),'exec'),{'__file__':str(P/script)})
exec(compile((P/'review_hero.py').read_text(),str(P/'review_hero.py'),'exec'),globals())
shots=[[c['name'],'pass18-'+c['name']+'.png'] for c in json.loads((R/'exports/manifest.json').read_text())['cameras'] if c['name'].startswith(tuple(str(i)+'_' for i in range(78,90))) ]
(R/'previews/hero-review-request.json').write_text(json.dumps({'shots':shots}))
