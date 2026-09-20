"""Fetch selected CC0 material maps through Poly Haven's public asset API."""
from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures,shutil
R=Path(__file__).resolve().parents[1];P=R/'references/polyhaven15';P.mkdir(exist_ok=True)
choices={
'M_Landmark_Rubble':('stone_wall',2.8,None,.20,.23),
'M_Landmark_Ashlar':('stone_wall_02',2.0,[177,173,157],.10,.12),
'M_Landmark_BrickRed':('brick_wall_001',3.0,None,.12,.08),
'M_Landmark_BrickBuff':('brick_wall_003',4.0,[184,166,121],.12,.08),
'M_Landmark_Cream':('plastered_wall_02',2.23,[220,209,180],.07,.08),
'M_Landmark_Turf':('sparse_grass',2.0,None,.22,0),
'M_Town_TileRed':('clay_roof_tiles_02',2.5,None,.13,0),
'M_Storgatan_Setts':('cobblestone_floor_08',2.0,[137,136,125],.15,0),
'M_Kvarnholmen_Asphalt':('asphalt_02',3.0,None,.12,0),
'M_Polish_BridgeWood':('wood_planks_grey',1.5,[118,105,84],.13,.10),
}
for key,c in [('Ivory',[219,213,193]),('Lime',[183,188,169]),('Yellow',[204,186,139]),('Rose',[192,149,128])]:choices['M_Town_'+key]=('plastered_wall_02',2.23,c,.07,.10)
config={k:dict(asset=v[0],metres=v[1],tint=v[2],macro=v[3],damp=v[4]) for k,v in choices.items()}
(R/'source/polish15-materials.json').write_text(json.dumps(config,indent=2))
b=R/'source/backups/detail-pass-14';b.mkdir(exist_ok=True)
paths=[R/'source/Stortorget.blend',R/'exports/manifest.json',R/'Unreal/Content/Kalmar/Maps/Stortorget.umap']
m=json.loads((R/'exports/manifest.json').read_text())
for a in m['assets']:
 if a['category']=='Kvarnholmen/Building massing' or a['name'] in json.loads((R/'previews/landmarks14-build.json').read_text())['changed']:
  paths.extend([R/'exports'/a['file'],R/'Unreal/Content/Kalmar/Meshes'/(a['name']+'.uasset')])
for k in choices:
 paths.append(R/'Unreal/Content/Kalmar/Materials'/(k+'.uasset'))
for f in ['scripts/build_landmarks14.py','scripts/build_kvarnholmen.py','Unreal/Content/Python/build_stortorget.py']:paths.append(R/f)
for p in paths:
 if p.exists():
  dst=b/p.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists():shutil.copy2(p,dst)
def fetch(job):
 asset,kind=job;d=json.loads((P/(asset+'-files.json')).read_text());spec=d[kind]['2k'];info=spec.get('png',spec.get('jpg'));ext='png' if 'png' in spec else 'jpg';out=P/(asset+'-'+kind+'.'+ext)
 if not out.exists():out.write_bytes(urllib.request.urlopen(urllib.request.Request(info['url'],headers={'User-Agent':'KalmarSceneStudy/1.0'}),timeout=120).read())
 if hashlib.md5(out.read_bytes()).hexdigest()!=info['md5']:raise ValueError('Checksum mismatch '+str(out))
 return {'asset':asset,'map':kind,'file':str(out.relative_to(R)),'url':info['url'],'md5':info['md5'],'license':'CC0','page':'https://polyhaven.com/a/'+asset}
jobs=[(a,k) for a in sorted({q['asset'] for q in config.values()}) for k in ['Diffuse','nor_gl','Rough','AO']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:report=list(ex.map(fetch,jobs))
(P/'downloads.json').write_text(json.dumps(report,indent=2));print('POLISH15_DOWNLOADS_OK',len(report),flush=True)
