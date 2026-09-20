"""Original seamless 4-metre material maps, not photographic facade textures."""
from pathlib import Path
import numpy as np
import math
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];N=2048;rng=np.random.default_rng(1414);yy,xx=np.mgrid[0:N,0:N];u,v=xx/N,yy/N
for key,color,kind in [('Ashlar',[166,160,141],'ashlar'),('BrickRed',[145,85,60],'brick'),('BrickBuff',[194,175,125],'brick'),('Rubble',[131,129,113],'stone'),('Cream',[221,205,158],'plaster'),('OliveWood',[107,117,69],'wood'),('SashOchre',[165,125,57],'wood'),('CopperRoof',[69,101,88],'metal'),('Turf',[79,94,48],'grass')]:
 noise=rng.normal(0,1,(N,N));broad=np.sin(2*np.pi*(u*3+v*2))*np.sin(2*np.pi*(u*7-v*5));height=noise*.00012+broad*.0004;col=np.zeros((N,N,3))+color;rough=195+noise*4
 if kind=='ashlar':
  row=np.floor(v*16);bx=(u*8+(row%2)*.5)%1;by=(v*16)%1;edge=np.minimum(np.minimum(bx,1-bx)*.5,np.minimum(by,1-by)*.25);f=np.clip(edge/.009,0,1);height+=.005*f;col+=(np.sin(np.floor(u*8+(row%2)*.5)*21.13+row*4.91)*9)[:,:,None];col=col*f[:,:,None]+np.array([145,139,122])*(1-f[:,:,None])
 elif kind=='brick':
  row=np.floor(v*50);bx=(u*16+(row%2)*.5)%1;by=(v*50)%1;edge=np.minimum(np.minimum(bx,1-bx)*.25,np.minimum(by,1-by)*.08);joint=edge<.006
  field=np.sin(np.floor(u*16+(row%2)*.5)*21.13+row*4.91)*5
  height+=.004*np.clip(edge/.006,0,1);col+=field[:,:,None];col[joint]=[171,164,144];height+=noise*.00035
 elif kind=='stone':
  # Uneven hand-laid courses, chipped polygon corners and fine lime joints.
  ci=Image.new('RGB',(N,N),(146,143,131));hi=Image.new('L',(N,N),0);dc=ImageDraw.Draw(ci);dh=ImageDraw.Draw(hi)
  sizes=rng.uniform(.8,1.3,10);ys=np.r_[0,np.cumsum(sizes/sizes.sum()*N)]
  palette=np.array([[116,120,112],[132,127,116],[104,112,108],[145,135,128],[138,141,133]])
  for row in range(10):
   count=int(rng.integers(5,9));ws=rng.uniform(.65,1.4,count);xs=np.r_[0,np.cumsum(ws/ws.sum()*N)];shift=(row%2)*125
   for j in range(count):
    x0,x1=xs[j]+shift+4,xs[j+1]+shift-4;y0,y1=ys[row]+4,ys[row+1]-4;c=float(rng.uniform(8,22));z=int(rng.integers(180,245));col=tuple(int(v) for v in palette[int(rng.integers(0,5))]+rng.uniform(-5,5))
    pts=[(x0+c,y0),(x1-c*.7,y0+float(rng.uniform(-2,2))),(x1,y0+c),(x1-2,y1-c*.8),(x1-c,y1),(x0+c*.5,y1-2),(x0,y1-c),(x0+2,y0+c*.7)]
    for shiftx in [-N,0,N]:
     poly=[(xx+shiftx,yy) for xx,yy in pts];dc.polygon(poly,fill=col);dh.polygon(poly,fill=z)
  col=np.asarray(ci).astype(float);field=np.asarray(hi.filter(ImageFilter.GaussianBlur(1.5))).astype(float)/255
  cloud=np.sin(u*math.tau*13+np.sin(v*math.tau*9))*np.sin(v*math.tau*17+np.sin(u*math.tau*5))
  height=.005*field+cloud*.0005+noise*.00013;col+=cloud[:,:,None]*4+broad[:,:,None]*4;rough+=12
 elif kind=='wood':
  grain=np.sin(2*np.pi*(u*160+.5*np.sin(v*2*np.pi)));height+=grain*.00025;col+=grain[:,:,None]*2
 elif kind=='metal':
  seam=(u*8)%1;height+=.002*np.exp(-((np.minimum(seam,1-seam))/.016)**2);col+=broad[:,:,None]*4;rough=148+noise*2+broad*12
 elif kind=='grass':height=noise*.00065;rough+=30;col+=noise[:,:,None]*6+broad[:,:,None]*9
 col+=(noise*1.3+broad*2)[:,:,None];dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N);normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 for suffix,a in [('BaseColor',col),('Roughness',rough),('Normal',(normal*.5+.5)*255)]:Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/f'exports/textures/T_Landmark{key}_{suffix}.png')
print('LANDMARK_MATERIALS_OK')
