"""Original tileable asphalt and water maps; metre-scaled height-derived normals."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';N=2048
rng=np.random.default_rng(3192026);yy,xx=np.mgrid[0:N,0:N];u,v=xx/N,yy/N
for name in ['DistrictAsphalt','DistrictWater']:
 if name=='DistrictAsphalt':
  grain=rng.normal(0,1,(N,N));broad=sum(np.sin(2*np.pi*(u*i+v*j)+rng.uniform(0,6.28)) for i,j in [(1,2),(3,-2),(5,3),(8,5)])/4
  col=np.array([65,68,70])[None,None,:]+(grain*3+broad*2)[:,:,None]
  height=grain*.00018;rough=228+rng.normal(0,3,(N,N))
 else:
  wave=.014*np.sin(2*np.pi*(u*3+v*2))+.006*np.sin(2*np.pi*(u*9-v*5))+.0015*np.sin(2*np.pi*(u*37+v*13))
  height=wave;col=np.zeros((N,N,3))+[33,71,84];col+=np.sin(2*np.pi*(u+v))[:,:,None]*2;rough=np.zeros((N,N))+86
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N)
 normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 for suffix,data in [('BaseColor',col),('Roughness',rough),('Normal',(normal*.5+.5)*255)]:Image.fromarray(np.clip(data,0,255).astype('uint8')).save(out/f'T_{name}_{suffix}.png')
print('KVARNHOLMEN_MATERIALS_OK')
