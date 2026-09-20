"""Original tileable carved-stone PBR texture; no photographic pixels.

One texture repeat represents 0.5 m. Normals are OpenGL (+Y); the UE importer
flips the green channel. Small pores and grain use physical height in metres.
"""
from pathlib import Path
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
out = R / 'exports/textures'
out.mkdir(parents=True, exist_ok=True)
n = 1024
rng = np.random.default_rng(191667)
fy, fx = np.meshgrid(np.fft.fftfreq(n), np.fft.fftfreq(n), indexing='ij')
def noise(sigma):
    spectrum = np.fft.fft2(rng.normal(size=(n, n)))
    a = np.fft.ifft2(spectrum * np.exp(-2*np.pi**2*sigma**2*(fx*fx+fy*fy))).real
    return a / a.std()
cloud, grain, pores = noise(36), noise(1.4), noise(.65)
pits = np.maximum(-pores-1.5, 0)
height = .00015*grain - .00018*pits + .00028*cloud
dx = (np.roll(height, -1, 1)-np.roll(height, 1, 1))/(2*.5/n)
dy = (np.roll(height, -1, 0)-np.roll(height, 1, 0))/(2*.5/n)
normal = np.stack([-dx, dy, np.ones_like(dx)], axis=-1)
normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
color = np.array([.49, .475, .425])[None,None,:] + (.017*cloud+.014*grain-.027*pits)[...,None]
rough = np.clip(.84+.025*grain+.04*pits, .62, .98)
for suffix, array in [('BaseColor',color), ('Normal',normal*.5+.5), ('Roughness',rough)]:
    Image.fromarray(np.uint8(np.clip(array,0,1)*255)).save(out/f'T_Portal19Stone_{suffix}.png')
print('PORTAL19_TEXTURES_OK')
