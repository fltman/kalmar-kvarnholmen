import bpy,json,numpy as np,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'));reg=json.loads((R/'source/district17.json').read_text())['buildings'];report={}
for name,r in reg.items():
 o=bpy.data.objects.get(name)
 if not o:report[name]={'exists':False};continue
 me=o.data;co=np.empty(len(me.vertices)*3,dtype=np.float64);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
 normals=np.empty(len(me.polygons)*3,dtype=np.float64);me.polygons.foreach_get('normal',normals);normals=normals.reshape(-1,3)
 H=o.get('eaves_height',r['H']);areas=np.empty(len(me.polygons));me.polygons.foreach_get('area',areas)
 roof=0
 for p in me.polygons:
  if abs(p.normal.z)>.15 and min(me.vertices[i].co.z for i in p.vertices)>=H-.05:roof+=p.area*abs(p.normal.z)
 report[name]={'exists':True,'detail_pass':o.get('detail_pass'),'vertices':len(me.vertices),'materials':len(me.materials),'finite_positions':bool(np.isfinite(co).all()),'finite_normals':bool(np.isfinite(normals).all()),'roof_projected_area':roof,'footprint_area':r['area'],'roof_coverage':roof/r['area'],'eaves':H}
bad=[n for n,v in report.items() if not v['exists'] or not v['finite_positions'] or not v['finite_normals'] or not v['materials']]
missing_roof=[n for n,v in report.items() if reg[n]['action']=='rebuild' and v['roof_coverage']<.80]
(R/'previews/district17-source-audit.json').write_text(json.dumps({'status':'passed' if not bad and not missing_roof else 'review_required','bad':bad,'roof_review':missing_roof,'buildings':report},indent=2));print('SOURCE_AUDIT',len(report),'BAD',bad,'ROOFS',missing_roof)
