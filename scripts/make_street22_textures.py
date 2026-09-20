"""Original red basket-bond clinker PBR; 4 m repeat, 250 mm groups, OpenGL normals."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';n=2048
rng=np.random.default_rng(220920);y,x=np.mgrid[:n,:n];gx=x/(n/16);gy=y/(n/16)
ix=gx.astype(int);iy=gy.astype(int);flip=(ix+iy)%2==0
u=np.where(flip,gx%1,gy%1);v=np.where(flip,(gy%1)*3,(gx%1)*3)
bu=u%1;bv=v%1;edge=np.minimum.reduce([bu*.25,(1-bu)*.25,bv*.25/3,(1-bv)*.25/3])
profile=np.clip((edge-.0016)/.0028,0,1);profile=profile*profile*(3-2*profile)
noise=rng.normal(0,1,(n,n));tone=rng.uniform(-.045,.045,(16,16,3))[iy,ix,np.where(flip,(gy%1*3).astype(int),(gx%1*3).astype(int))]
height=.0032*profile+noise*.000035*profile
color=np.array([.43,.235,.155])[None,None,:]+tone[...,None]+noise[...,None]*.009
color=np.where((edge<.0022)[...,None],np.array([.30,.29,.26]),color)
rough=np.where(edge<.0022,.93,.76+noise*.025)
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/n)
normal=np.stack([-dx,dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
for suffix,a in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/f'T_Street22Clinker_{suffix}.png')
print('STREET22_TEXTURES_READY')
