"""Cheap source-only checks; also runs in CI with LFS pointers instead of assets."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bundles=json.loads((R/'assets/manifest.json').read_text())['bundles'];inventory={p for b in bundles.values() for p in b['files']}
def available(p):return p.exists() or p.relative_to(R).as_posix() in inventory
m=json.loads((R/'exports/manifest.json').read_text());names=[a['name'] for a in m['assets']]
assert len(names)==len(set(names)), 'Duplicate asset names'
missing=[]
for a in m['assets']:
 if not available(R/'exports'/a['file']):missing.append(a['file'])
 for material in a['materials']:
  if material not in m['materials']:missing.append(material)
for name,spec in m['materials'].items():
 if spec.get('texture'):
  for suffix in ['BaseColor','Normal','Roughness']:
   p=R/'exports/textures'/('T_'+spec['texture']+'_'+suffix+'.png')
   if not available(p):missing.append(str(p.relative_to(R)))
assert not missing, 'Missing manifest files/materials: '+str(missing[:20])
assert 'photo' not in m['materials']['M_Altarpiece_Photo'], 'Excluded photo still referenced'
assert not (R/'exports/textures/T_AltarpiecePhoto.jpg').exists()
for p in (R/'Unreal/Config').glob('*.ini'):
 assert not re.search(r'(?im)^\s*(SecurityToken|Password|ApiKey)\s*=\s*\S+',p.read_text()), 'Credential-like config in '+str(p)
for folder in ['LICENSES','scripts','source','Unreal','exports']:
 assert (R/folder).is_dir(),folder
assert available(R/'source/Stortorget.blend')
print(f'Repository manifest OK: {len(names)} assets, {len(m["materials"])} materials')
