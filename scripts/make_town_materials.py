"""Original 2K town surfaces. Four-metre repeats, linear colour, OpenGL normals."""
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter
from PIL import Image
R=Path(__file__).resolve().parents[1];N=2048;rng=np.random.default_rng(8019)
def noise(s):
 a=gaussian_filter(rng.normal(size=(N,N)).astype('float32'),s,mode='wrap');return a/(a.std()+1e-8)
large=noise(65);grain=noise(.9);mid=noise(8);y,x=np.mgrid[0:N,0:N]/N
report={}
def save(name,base,h,rough,variation=None):
 color=np.array(base)[None,None,:]*(1+(large*.024+grain*.006 if variation is None else variation)[:,:,None])
 color=np.clip(color,0,1);color=np.where(color<=.0031308,12.92*color,1.055*color**(1/2.4)-.055)
 dx=(np.roll(h,-1,1)-np.roll(h,1,1))/(8/N);dy=(np.roll(h,-1,0)-np.roll(h,1,0))/(8/N)
 n=np.stack([-dx,-dy,np.ones_like(dx)],2);n/=np.linalg.norm(n,axis=2,keepdims=True)
 for suffix,a in [('BaseColor',color),('Normal',n*.5+.5),('Roughness',np.clip(rough,0,1))]:
  Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(R/'exports/textures'/f'T_{name}_{suffix}.png')
 report[name]={'resolution':N,'tile_metres':4,'normal_convention':'OpenGL +Y','height_rms_mm':float(h.std()*1000)}
for name,c in [('TownIvory',(.68,.65,.55)),('TownLime',(.57,.57,.49)),('TownYellow',(.63,.43,.19)),('TownRose',(.49,.32,.25)),('TownStone',(.38,.355,.31))]:
 save(name,c,grain*.00006+mid*.000035,.79+grain*.015)
for name,c in [('TownPaintWhite',(.68,.68,.61)),('TownPaintBlue',(.17,.25,.29)),('TownPaintGreen',(.08,.135,.10)),('TownPaintBrown',(.19,.105,.065))]:
 save(name,c,grain*.000013+mid*.000009,.48+mid*.025+grain*.015)
# Vertical timber joints on Nelson's plaster-imitating boards (four metres / 22).
seam=np.exp(-(np.minimum((x*22)%1,1-(x*22)%1)/.023)**2)
save('TownPanel',(.57,.58,.49),grain*.000035-seam*.0018,.73+grain*.012,seam*-.075+large*.025)
# Shallow pantile relief, separated by overlapping courses; real roof silhouette is geometry.
u=(x*20)%1;v=(y*13)%1;lap=np.exp(-(np.minimum(v,1-v)/.028)**2)
roll=np.cos(u*2*np.pi)*.006;h=roll-lap*.007+grain*.000045
tiles=rng.uniform(-.12,.12,(13,20))[np.floor(y*13).astype(int),np.floor(x*20).astype(int)]
for name,c in [('TownTileRed',(.33,.105,.047)),('TownTileDark',(.105,.070,.043))]:
 save(name,c,h,.78+grain*.015,tiles+large*.025-lap*.24)
save('TownMetalRed',(.28,.074,.045),grain*.000014+mid*.00002,.55+large*.025)
save('TownMetalGrey',(.115,.15,.132),grain*.000015+mid*.000018,.59+large*.018)
save('TownGlass',(.045,.078,.09),mid*.00004,.20+mid*.009,large*.035)
(R/'exports/town-material-report.json').write_text(json.dumps(report,indent=2));print('TOWN_MATERIALS_OK')
