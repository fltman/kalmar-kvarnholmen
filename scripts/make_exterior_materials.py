"""Original seamless exterior surface studies; 4 m tiles, OpenGL normals.
These are restrained material approximations, not scans of the cathedral.
"""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter
from PIL import Image
R=Path(__file__).resolve().parents[1];N=2048
rng=np.random.default_rng(1909266)
def noise(sigma):
 a=gaussian_filter(rng.normal(size=(N,N)).astype('float32'),sigma,mode='wrap')
 return a/(a.std()+1e-8)
broad=noise(54);grain=noise(1.0);pores=np.maximum(-noise(2)-1.8,0)
report={}
for name,tint,rough,variation,height in [
 ('ChurchCutStone',(.43,.415,.365),.68,.038,grain*.000045-pores*.00018),
 ('ChurchWindowPaint',(.19,.22,.185),.43,.015,grain*.000008),
 ('ChurchWindowGlass',(.073,.109,.121),.18,.035,noise(28)*.00013+grain*.000001)]:
 color=np.array(tint)[None,None,:]*(1+broad[:,:,None]*variation)
 if name=='ChurchCutStone':color*=1-pores[:,:,None]*.016
 color=np.where(color<=.0031308,12.92*color,1.055*np.maximum(color,0)**(1/2.4)-.055)
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N)
 normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 roughmap=np.clip(rough+broad*.022+grain*.008,0,1)
 for suffix,a in [('BaseColor',color),('Normal',normal*.5+.5),('Roughness',roughmap)]:
  Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(R/'exports/textures'/f'T_{name}_{suffix}.png')
 report[name]={'resolution':N,'tile_metres':4,'height_rms_mm':float(height.std()*1000),'normal_convention':'OpenGL +Y'}
(R/'exports/exterior-material-report.json').write_text(json.dumps(report,indent=2))
print('EXTERIOR_MATERIALS_OK')

exec(compile((R/'scripts/make_exterior_weathering.py').read_text(),str(R/'scripts/make_exterior_weathering.py'),'exec'))
