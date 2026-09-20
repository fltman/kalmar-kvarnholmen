"""Build versioned, checksummed asset bundles for GitHub Releases (no LFS required)."""
from pathlib import Path
import argparse,hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--version',default='v0.1.0');p.add_argument('--output',type=Path,required=True);args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
groups={'blender-source':[R/'source/Stortorget.blend'],'unreal-assets':sorted((R/'Unreal/Content').rglob('*.uasset'))+sorted((R/'Unreal/Content').rglob('*.umap')),'fbx-meshes':sorted((R/'exports/meshes').glob('*.fbx')),'textures':sorted(p for p in (R/'exports/textures').iterdir() if p.is_file()),'texture-sources':sorted(p for d in (R/'references').glob('polyhaven*') if d.is_dir() for p in d.rglob('*') if p.suffix in ['.png','.jpg','.exr'])}
licenses=[R/'LICENSE',R/'THIRD_PARTY.md']+sorted((R/'LICENSES').glob('*.txt'))
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
 return h.hexdigest()
manifest={'version':args.version,'repository':'fltman/kalmar-kvarnholmen','bundles':{}}
for key,paths in groups.items():
 out=args.output/(key+'.zip');files={}
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
  for f in paths+licenses:
   assert f.exists(),f
   rel=f.relative_to(R).as_posix();assert 'AltarpiecePhoto' not in rel
   z.write(f,rel);files[rel]={'bytes':f.stat().st_size,'sha256':sha(f)}
 assert out.stat().st_size<2_000_000_000,'Split oversized release asset'
 manifest['bundles'][key]={'file':out.name,'url':f'https://github.com/fltman/kalmar-kvarnholmen/releases/download/{args.version}/{out.name}','bytes':out.stat().st_size,'sha256':sha(out),'files':files}
 print(key,len(paths),out.stat().st_size,flush=True)
(R/'assets/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(args.output/'SHA256SUMS').write_text(''.join(v['sha256']+'  '+v['file']+'\n' for v in manifest['bundles'].values()))
print('BUNDLES_READY',flush=True)
