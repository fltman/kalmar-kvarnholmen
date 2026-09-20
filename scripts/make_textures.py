from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]; out=ROOT/'exports/textures';out.mkdir(exist_ok=True)
rng=np.random.default_rng(24); N=1024
# Seamless 4 x 4 metre granite setts; height field also produces a tangent-space normal.
base=Image.new('RGB',(N,N),(88,84,75)); height=Image.new('L',(N,N),30)
d=ImageDraw.Draw(base); h=ImageDraw.Draw(height)
for j in range(-1,24):
 for i in range(-1,19):
  x=i*60+(j%2)*30; y=j*46
  inset=int(rng.integers(3,6)); tone=int(rng.integers(116,175)); tint=rng.integers(-12,12,3)
  color=tuple(np.clip(tone+tint,0,255).tolist()); rect=(x+inset,y+inset,x+58-inset,y+44-inset)
  d.rounded_rectangle(rect,radius=8,fill=color);h.rounded_rectangle(rect,radius=8,fill=int(rng.integers(160,230)))
a=np.asarray(base).astype(float);noise=rng.normal(0,4,(N,N,1));a=np.clip(a+noise,0,255).astype('uint8')
Image.fromarray(a).save(out/'T_Granite_BaseColor.png')
z=np.asarray(height.filter(ImageFilter.GaussianBlur(2.0))).astype(float)/255
x=(np.roll(z,-1,1)-np.roll(z,1,1))*1.9;y=(np.roll(z,-1,0)-np.roll(z,1,0))*1.9
normal=np.stack([-x,-y,np.ones_like(x)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(out/'T_Granite_Normal.png')
rough=np.clip(210+rng.normal(0,8,(N,N)),0,255).astype('uint8');Image.fromarray(rough).save(out/'T_Granite_Roughness.png')
# Smaller irregular rounded cobbles for the broad fields, rather than rectangular road paving.
base=Image.new('RGB',(N,N),(83,80,69)); height=Image.new('L',(N,N),25);d=ImageDraw.Draw(base);h=ImageDraw.Draw(height)
for j in range(-1,25):
 for i in range(-1,22):
  x=i*50+(j%2)*25+int(rng.integers(-4,5));y=j*44+int(rng.integers(-3,4))
  tone=int(rng.integers(120,183)); tint=rng.integers(-14,12,3);col=tuple(np.clip(tone+tint,0,255).tolist())
  pts=[(x+5,y+13),(x+13,y+4),(x+35,y+5),(x+45,y+15),(x+43,y+31),(x+30,y+40),(x+12,y+37),(x+4,y+28)]
  d.polygon(pts,fill=col);h.polygon(pts,fill=int(rng.integers(155,230)))
a=np.asarray(base).astype(float)+rng.normal(0,5,(N,N,1));Image.fromarray(np.clip(a,0,255).astype('uint8')).save(out/'T_Cobbles_BaseColor.png')
z=np.asarray(height.filter(ImageFilter.GaussianBlur(2.2))).astype(float)/255
x=(np.roll(z,-1,1)-np.roll(z,1,1))*2;y=(np.roll(z,-1,0)-np.roll(z,1,0))*2
normal=np.stack([-x,-y,np.ones_like(x)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(out/'T_Cobbles_Normal.png')
Image.fromarray(rough).save(out/'T_Cobbles_Roughness.png')
print('Textures created')
