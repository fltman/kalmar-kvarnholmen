"""Remove collapsed pole/tip faces before Unreal builds Nanite and distance fields."""
import bmesh
def clean_sculpture_mesh(me):
 before=(len(me.vertices),len(me.polygons))
 bm=bmesh.new();bm.from_mesh(me)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.000001)
 bad=[f for f in bm.faces if f.calc_area()<1e-12]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(me);bm.free();me.update()
 return {'before':before,'after':(len(me.vertices),len(me.polygons))}
