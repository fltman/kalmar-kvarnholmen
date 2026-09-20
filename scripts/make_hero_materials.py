"""Production surface preparation from credited CC0 scan maps.
Plaster retained at its authored scale; a joint-free marble sample is used as
microstructure for painted marble and worn limestone. These are material studies,
not claimed to be scans of Kalmar Cathedral itself.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import gaussian_filter
R=Path(__file__).resolve().parents[1];OUT=R/'exports/textures';N=2048

def read(asset,channel,crop=None):
 im=Image.open(R/'references/polyhaven'/asset/(channel+'.png')).convert('RGB')
 if crop:
  w,h=im.size;im=im.crop(tuple(int(v*q) for v,q in zip(crop,[w,h,w,h])))
 return np.asarray(im.resize((N,N),Image.Resampling.LANCZOS),dtype=np.float32)/255

def linear(c):return np.where(c<=.04045,c/12.92,((c+.055)/1.055)**2.4)
def srgb(c):return np.where(c<=.0031308,c*12.92,1.055*np.maximum(c,0)**(1/2.4)-.055)
def periodic(a):
 # Mirror a scan sample in both directions to avoid visible boundary discontinuities.
 small=np.asarray(Image.fromarray(np.uint8(np.clip(a,0,1)*255)).resize((N//2,N//2),Image.Resampling.LANCZOS),dtype=np.float32)/255
 return np.concatenate([np.concatenate([small,small[:,::-1]],axis=1),np.concatenate([small[::-1],small[::-1,::-1]],axis=1)],axis=0)
def out(name,col,norm,rough):
 strength={'ChurchLime':.35,'ChurchOchre':.5,'ChurchMarble':.18,'ChurchFloor':.45,'ChurchFloorB':.45}.get(name,1)
 v=norm*2-1;v[:,:,:2]*=strength;v/=np.maximum(np.linalg.norm(v,axis=2,keepdims=True),1e-6);norm=v*.5+.5
 for suffix,data in [('BaseColor',srgb(col)),('Normal',norm),('Roughness',rough)]:
  Image.fromarray(np.uint8(np.clip(data,0,1)*255)).save(OUT/f'T_{name}_{suffix}.png')
# Use source scans with a neutral paint tint. Preserve color mottling, reduce the
# overly strong photographic exposure variation before adding physically small normals.
base=linear(read('white_plaster_02','diff'));lum=base.mean(2);variation=np.clip(lum/(np.median(lum)+1e-6),.78,1.15)
norm=read('white_plaster_02','nor_gl');rough=read('white_plaster_02','rough').mean(2)
for name,col in [('ChurchLime',(.64,.624,.574)),('ChurchOchre',(.57,.30,.109))]:
 out(name,variation[:,:,None]**.55*np.array(col),norm,.74+.16*rough)
# Crop inside a single slab; no tile joints may appear on column shafts.
crop=(.35,.30,.63,.63)
diff=periodic(read('marble_01','diff',crop));lin=linear(diff);lum=lin.mean(2);broad=gaussian_filter(lum,36,mode='wrap');detail=lum-broad
vein=np.clip(-detail*14,0,1);mottle=np.clip((lum-np.median(lum))*2,-.20,.20)
# Normals derived from the same periodic microrelief, using metre units.
height=detail*.0006
nx=-(np.roll(height,-1,1)-np.roll(height,1,1))/(8/N);ny=-(np.roll(height,-1,0)-np.roll(height,1,0))/(8/N)
v=np.stack([nx,ny,np.ones_like(nx)],2);v/=np.linalg.norm(v,axis=2,keepdims=True);nm=v*.5+.5
color=np.array([.045,.013,.007])[None,None,:]*(1+mottle[:,:,None]*1.5)+vein[:,:,None]*np.array([.075,.040,.020])
out('ChurchMarble',color,nm,.30+vein*.065+mottle*.05)
for name,col in [('ChurchFloor',(.23,.218,.190)),('ChurchFloorB',(.27,.238,.205))]:
 color=np.array(col)[None,None,:]*(1+mottle[:,:,None]*.8-vein[:,:,None]*.09)
 out(name,color,nm,.43+vein*.12+mottle*.12)
# Gold leaf: micro abrasion, highly metallic but broad and varied roughness.
gold=linear(np.asarray(Image.open(OUT/'T_ChurchGilding_BaseColor.png').convert('RGB'),dtype=np.float32)/255)
gold=gold/gold.mean(axis=(0,1))*np.array([.74,.53,.23])
out('ChurchGilding',gold,np.asarray(Image.open(OUT/'T_ChurchGilding_Normal.png'),dtype=np.float32)/255,np.clip(.34+mottle*.16+vein*.035,.23,.48))
(R/'exports/hero-material-report.json').write_text(json.dumps({'resolution':2048,'sources':['https://polyhaven.com/a/white_plaster_02','https://polyhaven.com/a/marble_01'],'license':'CC0','unused_download':'stone_floor; rejected because its joints and weathering do not match the church interior','normal_convention':'OpenGL','plaster_tile_metres':2,'marble_sample_crop':crop},indent=2))
print('HERO_MATERIALS_OK')

# Smooth painted pew finish is the last surface override.
exec(compile((R/'scripts/make_joinery_materials.py').read_text(),str(R/'scripts/make_joinery_materials.py'),'exec'))

# Dedicated exterior stone and painted window surfaces.
exec(compile((R/'scripts/make_exterior_materials.py').read_text(),str(R/'scripts/make_exterior_materials.py'),'exec'))

exec(compile((R/'scripts/make_town_materials.py').read_text(),str(R/'scripts/make_town_materials.py'),'exec'))

exec(compile((R/'scripts/make_storgatan_materials.py').read_text(),str(R/'scripts/make_storgatan_materials.py'),'exec'))
