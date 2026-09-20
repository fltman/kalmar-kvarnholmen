"""Prepare measured-scale CC0 scans and controlled color variants; preserve source maps."""
from pathlib import Path
import numpy as np,json,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'references/polyhaven15';cfg=json.loads((R/'source/polish15-materials.json').read_text());M=json.loads((R/'exports/manifest.json').read_text());rows=[]
for name,c in cfg.items():
 texture='Polish15'+name.removeprefix('M_').replace('_','');source=c['asset']
 for kind,suffix in [('Diffuse','BaseColor'),('nor_gl','Normal'),('Rough','Roughness'),('AO','AO')]:
  f=next(P.glob(source+'-'+kind+'.*'));raw=Image.open(f)
  if suffix in ['Roughness','AO'] and raw.mode.startswith('I'):
   im=Image.fromarray(np.uint8(np.clip(np.asarray(raw,dtype=np.float32)/257,0,255)))
  else:im=raw.convert('RGB' if suffix in ['BaseColor','Normal'] else 'L')
  if suffix=='Normal':
   a=np.asarray(im,dtype=np.float32)/127.5-1;length=np.linalg.norm(a,axis=2,keepdims=True);a/=np.maximum(length,.0001);im=Image.fromarray(np.uint8(np.clip((a*.5+.5)*255,0,255)))
  if suffix=='BaseColor' and c['tint']:
   a=np.asarray(im,dtype=np.float32);mean=a.mean(axis=(0,1));a=a/mean*np.array(c['tint']);im=Image.fromarray(np.uint8(np.clip(a,0,255)))
  im.save(R/'exports/textures'/('T_'+texture+'_'+suffix+'.png'))
 spec=M['materials'].get(name,{'color':[.25,.22,.17],'roughness':.82,'metallic':0})
 spec.update(texture=texture,uv_scale=4/c['metres'],normal_strength=1.0,polish15={'ao':True,'macro':c['macro'],'damp':c['damp'],'physical_tile_metres':c['metres'],'source':'https://polyhaven.com/a/'+source})
 M['materials'][name]=spec
# A nonperiodic-looking, seamless multiscale field: not baked directional shadow.
N=1024;rng=np.random.default_rng(1515);yy,xx=np.mgrid[0:N,0:N];field=np.zeros((N,N),np.float32)
for _ in range(80):
 kx=int(rng.integers(1,28));ky=int(rng.integers(-27,28));weight=1/max(1,np.hypot(kx,ky))**1.2;field+=weight*np.sin(2*np.pi*(kx*xx+ky*yy)/N+rng.uniform(0,2*np.pi))
field=128+38*field/max(float(field.std()),.001)
Image.fromarray(np.uint8(np.clip(field,0,255))).save(R/'exports/textures/T_Polish15Macro.png')
(R/'exports/manifest.json').write_text(json.dumps(M,indent=2));print('POLISH15_MATERIALS_OK',len(cfg))
