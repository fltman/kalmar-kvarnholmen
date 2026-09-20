"""Original exterior surfaces: restrained patina and coursed pilaster stone.
No photographed pixels. The metal maps deliberately contain no fake tile grid;
sheet seams are modeled in geometry. Four metre tiles, OpenGL normals.
"""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter
from PIL import Image
R=Path(__file__).resolve().parents[1];N=2048;rng=np.random.default_rng(190927)
def noise(s):
 a=gaussian_filter(rng.normal(size=(N,N)).astype('float32'),s,mode='wrap')
 return a/(a.std()+1e-8)
large=noise(90);medium=noise(18);fine=noise(1.1)
streak=noise((35,2.5));report={}
def save(name,color,height,rough):
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N)
 dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N)
 normal=np.stack([-dx,-dy,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 color=np.clip(color,0,1);color=np.where(color<=.0031308,12.92*color,1.055*color**(1/2.4)-.055)
 for suffix,a in [('BaseColor',color),('Normal',normal*.5+.5),('Roughness',rough)]:
  Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(R/'exports/textures'/f'T_{name}_{suffix}.png')
 report[name]={'resolution':N,'tile_metres':4,'height_rms_mm':float(height.std()*1000),'normal_convention':'OpenGL +Y','roughness_range':[float(rough.min()),float(rough.max())]}
patina=np.clip(.55+large*.10+medium*.035,0,1)
color=np.array([.082,.205,.158])[None,None,:]*(1+large[:,:,None]*.06+streak[:,:,None]*.012)
color+=np.maximum(-large-.65,0)[:,:,None]*np.array([.006,-.008,-.009])
save('ChurchCopperFine',color,fine*.000018+medium*.00006+large*.00015,np.clip(.69+patina*.11+fine*.008,.62,.84))
color=np.array([.052,.062,.054])[None,None,:]*(1+large[:,:,None]*.045+medium[:,:,None]*.014)
save('ChurchRoofFine',color,fine*.000020+medium*.00004,np.clip(.65+large*.022+fine*.008,.57,.77))
y,x=np.mgrid[0:N,0:N]/N;row=np.floor(y*13).astype(int);fy=(y*13)%1
joint=np.exp(-(np.minimum(fy,1-fy)/.0065)**2)
block=np.floor(x*5).astype(int);tones=rng.uniform(-.10,.10,(13,5))[row,block]
color=np.array([.405,.371,.305])[None,None,:]*(1+tones[:,:,None]+large[:,:,None]*.028+fine[:,:,None]*.012)
color=color*(1-joint[:,:,None]*.25)
save('ChurchPierStone',color,fine*.00006+medium*.00005-joint*.0014,np.clip(.70+fine*.020+joint*.09,.59,.89))
(R/'exports/exterior-weathering-report.json').write_text(json.dumps(report,indent=2))
print('EXTERIOR_WEATHERING_OK')
