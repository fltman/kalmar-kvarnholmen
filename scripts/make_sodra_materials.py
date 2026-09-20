from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];N=2048;rng=np.random.default_rng(1313);yy,xx=np.mgrid[0:N,0:N];u,v=xx/N,yy/N
for name,color,wood in [('SodraCream',[196,183,144],False),('SodraSand',[192,170,145],False),('SodraRedWood',[126,43,40],True),('SodraOchreWood',[181,143,83],True),('SodraDarkTile',[91,67,45],False)]:
 noise=rng.normal(0,1,(N,N));broad=np.sin(2*np.pi*(u*3+v*2))*np.sin(2*np.pi*(u*7-v*5));grain=np.sin(2*np.pi*(u*120+.5*np.sin(v*2*np.pi))) if wood else 0
 height=noise*.00012+broad*.00035+grain*.00017
 if name=='SodraDarkTile':
  tx,ty=(u*20)%1,(v*16)%1;seam=(tx<.025)|(ty<.022);height=.007*np.sin(np.pi*tx)+.004*(1-ty);height[seam]-=.003
  broad=np.sin(2*np.pi*(np.floor(u*20)/20*3+np.floor(v*16)/16*5))*2+np.sin(np.pi*tx)*2
 col=np.zeros((N,N,3))+color;col+=(noise*1.3+broad*2+grain*1.5)[:,:,None];rough=202+noise*3
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N);normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 for suffix,a in [('BaseColor',col),('Roughness',rough),('Normal',(normal*.5+.5)*255)]:Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/f'exports/textures/T_{name}_{suffix}.png')
print('SODRA_MATERIALS_OK')
