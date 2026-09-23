"""Original PBR maps for pass 25, 4 m repeat, OpenGL normals.
Ballast: crushed granite, 30-60 mm stones packed with smaller fill (Voronoi cells).
Tactile: 400 mm concrete tiles with raised ribs along u (guidance strip).
Warning: 400 mm light concrete tiles with a 6 x 6 grid of truncated studs.
Timber: creosoted sleeper wood weathered grey-brown, grain and drying checks along u."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'exports/textures';n=2048
def save(name,color,rough,height,scale):
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(2*scale/n);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(2*scale/n)
 normal=np.stack([-dx,dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
 for suffix,a in [('BaseColor',color),('Roughness',rough),('Normal',normal*.5+.5)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(out/f'T_{name}_{suffix}.png')
rng=np.random.default_rng(250923)
# Ballast: crushed granite, ~45 mm stones on a wrap-around Voronoi, each with its own granite tint
# and a tilted facet, shadowed voids between them holding ~20 mm fill stones.
def voronoi(cells,seed):
 r=np.random.default_rng(seed);jit=r.random((cells,cells,2))
 y,x=np.mgrid[:n,:n]/n*cells;best=np.full((n,n),9.0);second=np.full((n,n),9.0);owner=np.zeros((n,n,2),dtype=int);off=np.zeros((n,n,2))
 iy,ix=np.floor(y).astype(int),np.floor(x).astype(int)
 for oy in (-1,0,1):
  for ox in (-1,0,1):
   cy=(iy+oy)%cells;cx=(ix+ox)%cells;py=iy+oy+jit[cy,cx,0];px=ix+ox+jit[cy,cx,1]
   d=np.hypot(y-py,x-px);closer=d<best;second=np.where(closer,best,np.minimum(second,d));best=np.where(closer,d,best)
   owner[...,0]=np.where(closer,cy,owner[...,0]);owner[...,1]=np.where(closer,cx,owner[...,1])
   off[...,0]=np.where(closer,y-py,off[...,0]);off[...,1]=np.where(closer,x-px,off[...,1])
 return best,second,owner,off
cells=80;best,second,owner,off=voronoi(cells,1);o0,o1=owner[...,0],owner[...,1]
edge=np.clip((second-best)/.55,0,1);body=np.clip((edge-.25)/.75,0,1)
pal=np.array([[.52,.50,.48],[.58,.48,.44],[.47,.40,.35],[.38,.37,.37],[.62,.60,.57],[.54,.45,.41]])
pick=rng.integers(0,len(pal),(cells,cells));tone=1+.08*rng.normal(0,1,(cells,cells));ang=rng.random((cells,cells))*2*np.pi;tilt=.4+.4*rng.random((cells,cells))
facet=(np.cos(ang)[o0,o1]*off[...,1]+np.sin(ang)[o0,o1]*off[...,0])*tilt[o0,o1]
stone=pal[pick[o0,o1]]*tone[o0,o1][...,None]*(1+.30*facet[...,None])*(.45+.55*np.sqrt(body)[...,None])
b2,s2,w2,_=voronoi(210,2);e2=np.clip((s2-b2)/.45,0,1);fill=pal[rng.integers(0,len(pal),(210,210))[w2[...,0],w2[...,1]]]*(.14+.36*np.sqrt(e2)[...,None])
mask=np.clip((edge-.22)/.18,0,1);noise=rng.normal(0,1,(n,n))
color=stone*mask[...,None]+fill*(1-mask[...,None])+.012*noise[...,None]
height=(.030*np.sqrt(body)+.008*facet)*mask+.011*np.sqrt(e2)*(1-mask)+.0015*noise*mask
rough=.86+.04*noise*.5+.06*(1-mask)
save('Rail25Ballast',color,rough,height,4.0)
# Tactile strip: ten 400 mm tiles across 4 m, each with six raised ribs along the platform edge.
u=(np.mgrid[:n,:n][1]/n*10)%1;v=(np.mgrid[:n,:n][0]/n*10)%1
joint=np.minimum.reduce([u,1-u,v,1-v])<.012
rib=np.clip(1-np.abs(((u*6)%1)-.5)/.22,0,1);rib=rib*rib*(3-2*rib)
height=.005*rib*(~joint)+rng.normal(0,1,(n,n))*.00005
color=np.array([.80,.80,.78])[None,None,:]*(1-.18*joint[...,None])+.01*rng.normal(0,1,(n,n))[...,None]
rough=np.where(joint,.90,.72-.06*rib)
save('Rail25Tactile',color,rough,height,4.0)
# Warning tiles: studs about 30 mm across on a 67 mm grid, tile joints every 400 mm.
tu,tv=(np.mgrid[:n,:n][1]/n*10)%1,(np.mgrid[:n,:n][0]/n*10)%1
joint=np.minimum.reduce([tu,1-tu,tv,1-tv])<.012
r=np.hypot((tu*6)%1-.5,(tv*6)%1-.5);dome=np.clip(1-(r/.23)**2,0,1)
height=.004*np.sqrt(dome)*(~joint)+rng.normal(0,1,(n,n))*.00005
color=np.array([.80,.80,.78])[None,None,:]*(1-.16*joint[...,None])+.05*dome[...,None]+.01*rng.normal(0,1,(n,n))[...,None]
rough=np.where(joint,.90,.76-.10*dome)
save('Rail25Warning',color,rough,height,4.0)
# Timber: grain as row noise (constant along u) bent by a slow wave, weathered patches, checks.
rows=np.convolve(rng.normal(0,1,n+64),np.ones(7)/7,'same')[32:32+n];fine=np.convolve(rng.normal(0,1,n+16),np.ones(2)/2,'same')[8:8+n]
uu,vv=np.mgrid[:n,:n][1]/n,np.mgrid[:n,:n][0]
bend=(vv+3*np.sin(2*np.pi*(uu*2+vv/n*2))+1.5*np.sin(2*np.pi*(uu*7+vv/n*5))).astype(int)%n
grain=rows[bend]*.8+fine[bend]*.4
low=np.zeros((n,n))
for _ in range(6):
 fy,fx,ph=rng.integers(1,4),rng.integers(1,5),rng.random()*6.3;low+=np.sin(2*np.pi*(fx*uu+fy*vv/n)+ph)
low=(low-low.min())/(low.max()-low.min())
checks=np.zeros((n,n))
for _ in range(90):
 r0=rng.integers(0,n);c0=rng.integers(0,n);ln=rng.integers(n//12,n//3);w=rng.integers(1,4)
 cols=(c0+np.arange(ln))%n;taper=np.sin(np.linspace(0,np.pi,ln))
 for k in range(w):checks[(r0+k)%n,cols]=np.maximum(checks[(r0+k)%n,cols],taper)
brown=np.array([.33,.27,.22]);grey=np.array([.47,.45,.42])
color=(brown*(1-.55*low[...,None])+grey*.55*low[...,None])*(1+.10*grain[...,None])
color=color*(1-.65*checks[...,None])+.008*rng.normal(0,1,(n,n))[...,None]
height=.0012*grain-.004*checks
rough=.86+.04*grain*.5-.05*low
save('Rail25Timber',color,rough,height,4.0)
from PIL import Image as _I
for name in ('Rail25Ballast','Rail25Tactile','Rail25Warning','Rail25Timber'):
 a=np.asarray(_I.open(out/f'T_{name}_BaseColor.png').convert('RGB')).astype(float)/255;print('MEAN',name,[round(float(x),3) for x in a.reshape(-1,3).mean(0)])
print('RAIL25_TEXTURES_READY')
