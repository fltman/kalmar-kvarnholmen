import json,numpy as np
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];specs=json.loads((R/'source/polish15-material-specs.json').read_text());out={}
for name,s in specs.items():
 d={}
 for suffix in ['BaseColor','Normal','Roughness']+(['AO'] if s.get('polish15') else []):
  im=Image.open(R/f'exports/textures/T_{s["texture"]}_{suffix}.png');a=np.asarray(im);d[suffix]={'size':im.size,'mode':im.mode,'min':int(a.min()),'max':int(a.max()),'std':float(a.std())}
  if suffix=='Normal':
   q=a.astype(float)/127.5-1;l=np.linalg.norm(q,axis=2);d[suffix]['length_p01']=float(np.quantile(l,.01));d[suffix]['length_p99']=float(np.quantile(l,.99))
 out[name]=d
ok=all(v['Normal']['length_p01']>.97 and v['Normal']['length_p99']<1.03 and (v['Roughness']['std']>0 or n=='M_Kvarnholmen_Water') and ('AO' not in v or v['AO']['std']>0) for n,v in out.items());(R/'previews/polish15-textures.json').write_text(json.dumps({'status':'passed' if ok else 'failed','materials':out},indent=2));print('TEXTURE_CHECK',ok)
