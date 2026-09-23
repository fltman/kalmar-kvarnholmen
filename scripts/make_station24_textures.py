"""Original rhombic slate PBR for the 1910 station roof and tower; 4 m repeat, 0.40 m
diamonds laid on the diagonal, OpenGL normals. Interprets the photographed roof; not a scan."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';n=2048
rng=np.random.default_rng(240923);y,x=np.mgrid[:n,:n]
# Ten diamonds per repeat in each direction: a diagonal grid of unit cells in (s,t).
s=(x+y)/(n/10);t=(x-y)/(n/10)
cs=np.floor(s).astype(int);ct=np.floor(t).astype(int);fs=s%1;ft=t%1
# Each slate overlaps the one below: the lower tip is raised, the upper edge sinks under.
lap=np.clip(1-(fs+ft)/2,0,1)
edge=np.minimum.reduce([fs,1-fs,ft,1-ft])
groove=np.clip(edge/.035,0,1);groove=groove*groove*(3-2*groove)
key=((cs*73+ct*151)%4096+4096)%4096;tone=rng.normal(0,1,4096)[key];rust=rng.random(4096)[key]<.05
noise=rng.normal(0,1,(n,n))
height=.006*lap*groove+.0012*groove+noise*.00004
color=np.array([.235,.238,.25])[None,None,:]*(1+.07*tone[...,None])+.010*noise[...,None]
color=np.where(rust[...,None],color*np.array([1.10,1.03,.95]),color)
color=color*(.55+.45*groove[...,None])
rough=.58+.05*tone+.02*noise;rough=np.where(groove<.5,.82,rough)
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/n)
normal=np.stack([-dx,dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
for suffix,a in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/f'T_Station24Slate_{suffix}.png')
print('STATION24_TEXTURES_READY')
