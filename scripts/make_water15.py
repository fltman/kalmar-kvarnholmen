from pathlib import Path
import numpy as np,json
from PIL import Image
R=Path(__file__).resolve().parents[1];N=1024;y,x=np.mgrid[0:N,0:N];rng=np.random.default_rng(1599);h=np.zeros((N,N))
for i in range(65):
 kx=int(rng.integers(3,45));ky=int(rng.integers(-18,19));freq=np.hypot(kx,ky);amp=.018*(12/freq)**1.2/8;h+=amp*np.sin(2*np.pi*(kx*x+ky*y)/N+rng.uniform(0,2*np.pi))
dx=(np.roll(h,-1,1)-np.roll(h,1,1))/(64/N);dy=(np.roll(h,-1,0)-np.roll(h,1,0))/(64/N);normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
for key,a in [('Normal',(normal*.5+.5)*255),('Roughness',np.full((N,N),64)),('BaseColor',np.zeros((N,N,3))+[30,66,68])]:Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/f'exports/textures/T_Polish15Water_{key}.png')
sp={'color':[.013,.054,.058],'roughness':.25,'metallic':0,'texture':'Polish15Water','uv_scale':.125,'normal_strength':1.0}
(R/'source/polish15-extra-materials.json').write_text(json.dumps({'M_Kvarnholmen_Water':sp},indent=2))
