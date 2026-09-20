"""Original glazed ceramic PBR tile, 4 m repeat / 32 tiles; OpenGL normals."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';out.mkdir(exist_ok=True)
n=1024;rng=np.random.default_rng(210921)
y,x=np.mgrid[:n,:n];tx=x/32;ty=y/32
edge=np.minimum.reduce([tx%1,1-tx%1,ty%1,1-ty%1])
t=np.clip((edge-.014)/.050,0,1);profile=t*t*(3-2*t)
noise=rng.normal(0,1,(n,n));height=.00125*profile+.000015*noise
variation=rng.uniform(-.018,.018,(32,32))[y//32,x//32]
color=np.array([.46,.475,.49])[None,None,:]+variation[...,None]+.002*noise[...,None]
color=np.where((edge<.03)[...,None],np.array([.29,.29,.275]),color)
rough=.34+.025*noise;rough=np.where(edge<.03,.78,rough)
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/n)
normal=np.stack([-dx,dy,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
for suffix,array in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(array,0,1)*255)).save(out/f'T_Street21Tile_{suffix}.png')
print('STREET21_TEXTURES_READY')
