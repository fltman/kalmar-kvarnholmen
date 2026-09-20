"""Deterministic physically-scaled PBR textures, authored for this model.
OpenGL tangent normals; Unreal import flips G. 4 m tiles; height in metres.
No photographs are used to generate these material maps.
"""
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter,zoom
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];OUT=R/'exports/textures';OUT.mkdir(exist_ok=True)
N=2048;rng=np.random.default_rng(1660);y,x=np.mgrid[0:N,0:N].astype(np.float32)/N

def noise(scale,seed=0):
 rr=np.random.default_rng(1660+seed+scale);a=rr.normal(size=(scale,scale)).astype(np.float32)
 a=np.pad(a,((0,1),(0,1)),mode='wrap');a=zoom(a,N/scale,order=3,mode='wrap')[:N,:N]
 a=(a-a.mean())/(a.std()+1e-6);return a
macro=noise(8);meso=noise(64);micro=noise(512);grain=rng.normal(0,1,(N,N)).astype(np.float32)

def srgb(a):return np.where(a<=.0031308,a*12.92,1.055*np.power(np.maximum(a,0),1/2.4)-.055)
def save(name,col,h,rough):
 col=np.broadcast_to(col,(N,N,3));rough=np.broadcast_to(rough,(N,N))
 Image.fromarray(np.uint8(np.clip(srgb(col),0,1)*255)).save(OUT/f'T_{name}_BaseColor.png')
 # Central differences in metres; handedness documented for each engine.
 du=(np.roll(h,-1,1)-np.roll(h,1,1))/(8/N);dv=(np.roll(h,-1,0)-np.roll(h,1,0))/(8/N)
 v=np.stack([-du,-dv,np.ones_like(du)],axis=-1);v/=np.linalg.norm(v,axis=-1,keepdims=True)
 Image.fromarray(np.uint8(np.clip(v*.5+.5,0,1)*255)).save(OUT/f'T_{name}_Normal.png')
 Image.fromarray(np.uint8(np.clip(rough,0,1)*255)).save(OUT/f'T_{name}_Roughness.png')
 print(name,flush=True)
 report[name]={'resolution':N,'tile_metres':4,'height_range_mm':float(np.ptp(h)*1000),'normal_convention':'OpenGL +Y'}
report={}
for name,color,relief in [('ChurchOchre',(.68,.37,.145),.00055),('ChurchLime',(.76,.755,.70),.00019)]:
 h=relief*(micro*.7+meso*.5+grain*.09)
 c=np.array(color)[None,None,:]*(1+macro[...,None]*.034+meso[...,None]*.016+micro[...,None]*.012)
 save(name,c,h,.84+meso*.02+micro*.02)
# Limestone ashlar: 0.8 x 0.286 m courses with fine recessed mortar joints.
row=np.floor(y*14);tx=(x*5+(row%2)*.5)%1;ty=(y*14)%1
edge=np.minimum(np.minimum(tx,1-tx)*.8,np.minimum(ty,1-ty)*(4/14))
joint=1-np.clip(edge/.0045,0,1);joint=gaussian_filter(joint,.8,mode='wrap')
ids=(np.floor(x*5+(row%2)*.5)%5+row*5).astype(int)
tones=np.random.default_rng(97).uniform(-.05,.05,70)[ids]
h=.0004*micro+.00020*meso-joint*.0035
c=np.array([.51,.485,.40])[None,None,:]*(1+tones[...,None]+macro[...,None]*.04+micro[...,None]*.015)
c=c*(1-joint[...,None]*.23)
save('ChurchAshlar',c,h,.77+micro*.026+joint*.08)
# Uncoursed foundation rubble uses wrapped nearest Voronoi cells.
from scipy.spatial import cKDTree
pts=rng.random((115,2));pts=np.concatenate([pts+np.array([dx,dy]) for dx in [-1,0,1] for dy in [-1,0,1]])
dist,idx=cKDTree(pts).query(np.stack([x.ravel(),y.ravel()],axis=1),k=2,workers=4)
delta=(dist[:,1]-dist[:,0]).reshape(N,N);mortar=np.exp(-delta/.0013);tone=rng.uniform(-.18,.18,115)[idx[:,0]%115].reshape(N,N)
h=.0015*meso+.00055*micro-.011*mortar
c=np.array([.18,.18,.155])[None,None,:]*(1+tone[...,None]+micro[...,None]*.05)
c=c*(1-mortar[...,None])+np.array([.36,.34,.29])[None,None,:]*mortar[...,None]
save('ChurchRubble',c,h,.88+micro*.02)
# Sheet-metal tiles: folded seams, subtle oil-canning, patchy patina.
for name,color in [('ChurchCopper',(.13,.29,.235)),('ChurchRoof',(.075,.090,.083))]:
 u=x*8;v=y*5;eu=np.minimum(u%1,1-u%1);ev=np.minimum(v%1,1-v%1)
 seam=np.exp(-(eu/.016)**2)*.004+np.exp(-(ev/.012)**2)*.0018
 h=seam+meso*.00006+np.sin(u*np.pi*2)*np.sin(v*np.pi*2)*.00045
 pat=np.clip((macro+1.0)/3,0,1)
 c=np.array(color)[None,None,:]*(.88+pat[...,None]*.23+meso[...,None]*.014)
 save(name,c,h,.48+pat*.24+micro*.015)
# Painted wood, oriented grain, wear and shallow tool marks.
woodgrain=noise(128)*.22+np.sin(x*(2*np.pi*175)+noise(16)*5)
for name,color in [('ChurchPew',(.36,.385,.36)),('ChurchDoor',(.042,.079,.058)),('ChurchOak',(.22,.105,.041))]:
 h=woodgrain*.00007+micro*.000045
 c=np.array(color)[None,None,:]*(1+woodgrain[...,None]*.045+macro[...,None]*.04)
 save(name,c,h,.55+meso*.045+woodgrain*.04)
# Painted marble: branching fractured veins, rather than uniform sine stripes.
rock=noise(16,19)+.42*noise(64,21)+.10*noise(256,28)
vein=np.exp(-(rock/.065)**2)
fine=np.exp(-((noise(64,41)+.30*noise(256,43))/.045)**2)
c=np.array([.048,.020,.016])[None,None,:]*(1+macro[...,None]*.25+meso[...,None]*.065)
c+=vein[...,None]*np.array([.28,.26,.22])[None,None,:]*.36+fine[...,None]*.013
save('ChurchMarble',c,vein*.000018+micro*.000008,.29+macro*.030+vein*.065)
# Worn Öland limestone slabs, preserving the geometry's real tile joints.
vein2=np.exp(-(np.sin(x*49-y*23+noise(16)*.8)/.12)**2)
for name,col in [('ChurchFloor',(.25,.235,.208)),('ChurchFloorB',(.30,.265,.238))]:
 c=np.array(col)[None,None,:]*(1+macro[...,None]*.08+meso[...,None]*.04)+vein2[...,None]*.024
 save(name,c,micro*.00005+meso*.000025-vein2*.00003,.47+macro*.07+meso*.025)
save('ChurchGilding',np.array([.67,.45,.13])[None,None,:]*(1+meso[...,None]*.03),micro*.000016+meso*.00002,.30+micro*.028+macro*.018)
(R/'exports/church-material-report.json').write_text(json.dumps(report,indent=2))
