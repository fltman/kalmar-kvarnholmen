"""Public snapshot: relative texture paths and neutral canvas in place of the excluded photograph."""
from pathlib import Path
import bpy,json
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
ma=bpy.data.materials.get('M_Altarpiece_Photo')
if ma:
 for n in list(ma.node_tree.nodes):
  if n.type=='TEX_IMAGE':ma.node_tree.nodes.remove(n)
 p=ma.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.23,.17,.10,1);p.inputs['Roughness'].default_value=.88
for im in list(bpy.data.images):
 if 'AltarpiecePhoto' in im.filepath or 'altar-detail' in im.filepath:bpy.data.images.remove(im,do_unlink=True);continue
 if im.source!='FILE':continue
 name=Path(im.filepath).name;candidate=R/'exports/textures'/name
 if candidate.exists():
  if im.packed_file:im.unpack(method='REMOVE')
  im.filepath='//../exports/textures/'+name
 elif not im.users:bpy.data.images.remove(im)
 else:raise RuntimeError('Unresolved public texture: '+name)
m=json.loads((R/'exports/manifest.json').read_text())
for c in m['cameras']:
 o=bpy.data.objects.get(c['name'])
 if o and c['name'].startswith(('85_','86_','89_','90_')):
  from mathutils import Vector
  o.location=c['location'];o.rotation_euler=(Vector(c['target'])-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=c['lens']
(R/'exports/manifest.json').write_text(json.dumps(m,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
print('PUBLIC_BLEND_READY',len(bpy.data.objects),'objects')
