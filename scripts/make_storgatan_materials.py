"""Original 4m repeat paving materials; physically scaled height-derived OpenGL normals."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';N=2048
for kind,nx,ny,joint,relief in [('StreetSetts',16,24,3,.008),('StreetSlabs',8,8,1.5,.002)]:
 rng=np.random.default_rng(101 if kind=='StreetSetts' else 102)
 base=Image.new('RGB',(N,N),(99,96,88));height=Image.new('L',(N,N),0);d=ImageDraw.Draw(base);h=ImageDraw.Draw(height)
 sx,sy=N/nx,N/ny
 for j in range(-1,ny+1):
  for i in range(-1,nx+1):
   x=i*sx+(j%2)*sx/2;y=j*sy
   shade=rng.normal(0,5 if kind=='StreetSetts' else 2);tone=np.array([143,139,127])+shade+rng.normal(0,1.2,3)
   col=tuple(np.clip(tone,0,255).astype(int));pad=joint+rng.uniform(0,1.5)
   pts=[(x+pad+3,y+pad),(x+sx-pad-4,y+pad+1),(x+sx-pad,y+pad+5),(x+sx-pad-1,y+sy-pad-3),(x+sx-pad-5,y+sy-pad),(x+pad+3,y+sy-pad-1),(x+pad,y+sy-pad-5),(x+pad+1,y+pad+4)]
   # Draw wrapped copies so the normal maps tile without a seam.
   for ox in [-N,0,N]:
    for oy in [-N,0,N]:
     q=[(px+ox,py+oy) for px,py in pts]
     d.polygon(q,fill=col);h.polygon(q,fill=220)
 colors=np.asarray(base).astype(float);noise=rng.normal(0,2.0,(N,N,1));colors=np.clip(colors+noise,0,255)
 Image.fromarray(colors.astype('uint8')).save(out/f'T_{kind}_BaseColor.png')
 z=np.asarray(height.filter(ImageFilter.GaussianBlur(2.5))).astype(float)/255*relief
 grain=rng.normal(0,.00010,(N,N));z+=grain
 dx=(np.roll(z,-1,1)-np.roll(z,1,1))/(8/N);dy=(np.roll(z,-1,0)-np.roll(z,1,0))/(8/N)
 normal=np.stack([-dx,-dy,np.ones_like(z)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 Image.fromarray(np.clip((normal*.5+.5)*255,0,255).astype('uint8')).save(out/f'T_{kind}_Normal.png')
 rough=np.clip(203+rng.normal(0,5,(N,N)),0,255).astype('uint8');Image.fromarray(rough).save(out/f'T_{kind}_Roughness.png')
print('STORGATAN_MATERIALS_OK')
