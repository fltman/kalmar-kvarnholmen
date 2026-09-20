from pathlib import Path
import sys

import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];N=1024;rng=np.random.default_rng(180);y,x=np.mgrid[0:N,0:N];u=x/N;v=y/N
for k,col in [('Grass',[91,131,51]),('Paint',[221,218,194])]:
 n=rng.normal(0,1,(N,N));large=np.sin(2*np.pi*(u*3+v*2))*np.sin(2*np.pi*(u*7-v*5));grain=np.sin(u*2*np.pi*131+np.sin(v*2*np.pi*57)*3)
 h=n*(.0013 if k=='Grass' else .00015)+grain*.00025
 dx=(np.roll(h,-1,1)-np.roll(h,1,1))/(8/N);dy=(np.roll(h,-1,0)-np.roll(h,1,0))/(8/N);norm=np.stack([-dx,-dy,np.ones_like(dx)],2);norm/=np.linalg.norm(norm,axis=2,keepdims=True)
 color=np.asarray(col)+(n*5+large*9+grain*2)[...,None];rough=np.ones_like(n)*(245 if k=='Grass' else 210)+n*3
 for suffix,a in [('BaseColor',color),('Normal',(norm*.5+.5)*255),('Roughness',rough)]:Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/f'exports/textures/T_Pass18{k}_{suffix}.png')
