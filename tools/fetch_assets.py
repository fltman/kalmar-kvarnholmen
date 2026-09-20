"""Download a tagged release's editable assets, verify SHA-256, and extract safely."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,tempfile,urllib.request,zipfile
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def fetch(bundle,dest,force=False):
 expected=bundle['files'];missing=[]
 for rel,info in expected.items():
  parts=PurePosixPath(rel)
  if parts.is_absolute() or '..' in parts.parts:raise ValueError('Unsafe manifest path')
  target=(dest/rel).resolve()
  if not target.is_relative_to(dest.resolve()):raise ValueError('Path escapes destination')
  if target.exists():
   if sha(target)==info['sha256']:continue
   if not force:raise RuntimeError(f'Local modification: {rel}. Save it elsewhere or explicitly use --force.')
  missing.append(rel)
 if not missing:print(bundle['file']+': already verified');return
 with tempfile.TemporaryDirectory(prefix='kvarnholmen-assets-') as tmp:
  archive=Path(tmp)/bundle['file'];print('Downloading '+bundle['file'],flush=True)
  req=urllib.request.Request(bundle['url'],headers={'User-Agent':'Kalmar-Kvarnholmen-asset-setup/1'})
  with urllib.request.urlopen(req,timeout=90) as response,archive.open('wb') as out:shutil.copyfileobj(response,out,1024*1024)
  if archive.stat().st_size!=bundle['bytes'] or sha(archive)!=bundle['sha256']:raise RuntimeError('Archive checksum mismatch')
  with zipfile.ZipFile(archive) as z:
   if set(z.namelist())!=set(expected):raise RuntimeError('Unexpected archive contents')
   for rel in missing:
    member=z.getinfo(rel)
    if (member.external_attr>>16)&0o170000==0o120000:raise RuntimeError('Symlink archive member')
    target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
    with z.open(member) as src,tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as dst:
     temp=Path(dst.name);shutil.copyfileobj(src,dst,1024*1024)
    try:
     if temp.stat().st_size!=expected[rel]['bytes'] or sha(temp)!=expected[rel]['sha256']:raise RuntimeError('File checksum mismatch: '+rel)
     os.replace(temp,target)
    finally:temp.unlink(missing_ok=True)
  print(bundle['file']+': verified and extracted',flush=True)
def main():
 m=json.loads((R/'assets/manifest.json').read_text());p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--bundle',choices=['all']+list(m['bundles']),default='all');p.add_argument('--output',type=Path,default=R);p.add_argument('--force',action='store_true',help='Replace locally modified asset files; save your work first');a=p.parse_args()
 for key,b in m['bundles'].items():
  if a.bundle=='all' or a.bundle==key:fetch(b,a.output,a.force)
 print('Assets ready. Blender: source/Stortorget.blend | Unreal: Unreal/KalmarStortorget.uproject')
if __name__=='__main__':main()
