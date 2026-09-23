"""Original white trapezoidal sheet PBR for Baronen's gym box and Bryggan; 4 m repeat,
250 mm profile pitch, OpenGL normals. Interprets photographed cladding; not a scan."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';n=2048
rng=np.random.default_rng(230923);y,x=np.mgrid[:n,:n];t=(x/(n/16))%1
# Crest 38 %, webs 14 % each, pan 34 % of the 250 mm pitch; 32 mm deep profile.
crest=np.clip((np.abs(t-.5)-.19)/.14,0,1);height=.032*(1-crest*crest*(3-2*crest))
seam=(np.abs((y/(n/2))%1-.5)>.4985)
noise=rng.normal(0,1,(n,n));streak=np.repeat(rng.normal(0,1,(1,n)),n,0)
height=height-.0006*seam+noise*.00002
color=np.array([.74,.76,.76])[None,None,:]+.012*streak[...,None]+.006*noise[...,None]-.05*seam[...,None]
rough=.40+.03*noise+.06*seam
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/n)
normal=np.stack([-dx,dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
for suffix,a in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/f'T_Baronen23Profiled_{suffix}.png')
# Factory brick: machine-made orange-red brick in cross bond (stretcher and header courses
# alternate, stretcher courses offset by half a brick), 238 x 65 mm faces, 12 mm light joints,
# 52 courses and 16 stretchers per 4 m tile. Interprets the April 2025 photographs; not a scan.
rng=np.random.default_rng(230924);cy=y/(n/52);row=cy.astype(int);fy=cy%1
header=row%2==1;offset=np.where(row%4==2,.5,0.0)
cx=np.where(header,x/(n/32),x/(n/16)+offset);col=np.floor(cx).astype(int);fx=cx%1
jx=np.where(header,12/125,12/250);jy=12/77
edge=np.minimum.reduce([fx/jx,(1-fx)/jx,fy/jy,(1-fy)/jy])
face=np.clip((edge-.5)/.7,0,1);face=face*face*(3-2*face)
key=(row*131+col*17)%4096;tone=rng.normal(0,1,4096)[key];burnt=rng.random(4096)[key]<.12
noise=rng.normal(0,1,(n,n))
brick=np.array([.58,.30,.20])[None,None,:]*(1+.085*tone[...,None])+.012*noise[...,None]
brick=np.where(burnt[...,None],brick*np.array([.72,.68,.70]),brick)
mortar=np.array([.62,.60,.55])[None,None,:]+.02*noise[...,None]
color=brick*face[...,None]+mortar*(1-face[...,None])
height=.008*face+noise*.00006*face-.0004*np.abs(noise)*(1-face)
rough=.80*face+.93*(1-face)+.02*noise
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/n)
normal=np.stack([-dx,dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
for suffix,a in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/f'T_Baronen23Brick_{suffix}.png')
print('BARONEN23_TEXTURES_READY')
