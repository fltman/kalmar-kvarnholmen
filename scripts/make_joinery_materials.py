"""Smooth painted joinery, physically shallow relief instead of exposed timber.
Own deterministic seamless maps, 4 m tile, OpenGL normals. No photo texture.
"""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter
from PIL import Image
R=Path(__file__).resolve().parents[1];N=2048
rng=np.random.default_rng(190926)
def field(sigma):
 a=gaussian_filter(rng.normal(size=(N,N)).astype('float32'),sigma,mode='wrap');return a/(a.std()+1e-8)
broad=field(48);brush=gaussian_filter(field(1.2),(1,16),mode='wrap');brush/=brush.std()
micro=field(.8);height=brush*.000009+micro*.000003
dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N)
n=np.stack([-dx,-dy,np.ones_like(dx)],2);n/=np.linalg.norm(n,axis=2,keepdims=True)
report={}
for name,tint in [('ChurchPew',(.34,.355,.325)),('ChurchPewInset',(.305,.321,.293)),('ChurchPewTrim',(.40,.415,.379))]:
 color=np.array(tint)[None,None,:]*(1+broad[:,:,None]*.014+brush[:,:,None]*.003)
 color=np.where(color<=.0031308,12.92*color,1.055*np.maximum(color,0)**(1/2.4)-.055)
 rough=np.clip(.40+broad*.018+brush*.008,.33,.47)
 for suffix,a in [('BaseColor',color),('Normal',n*.5+.5),('Roughness',rough)]:Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(R/'exports/textures'/f'T_{name}_{suffix}.png')
 report[name]={'resolution':N,'tile_metres':4,'height_rms_mm':float(height.std()*1000),'roughness_range':[float(rough.min()),float(rough.max())],'normal_max_tilt_degrees':float(np.degrees(np.arccos(n[:,:,2])).max()),'normal_convention':'OpenGL +Y'}
(R/'exports/joinery-material-report.json').write_text(json.dumps(report,indent=2))
print('JOINERY_MATERIALS_OK')
