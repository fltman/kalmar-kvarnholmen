original_finish=getattr(Mesh,'_finish_before_polish15',Mesh.finish)
Mesh._finish_before_polish15=original_finish
def finish15(self):
 obj=original_finish(self)
 if obj and self.category in ['Kvarnholmen/Landmarks','Kvarnholmen/Fortifications']:
  bpy.context.view_layer.objects.active=obj;obj.select_set(True)
  bevel=obj.modifiers.new('Crafted edge highlights','BEVEL');bevel.width=.009 if 'House' in self.name else .018;bevel.segments=2;bevel.limit_method='ANGLE';bevel.angle_limit=.65;bevel.harden_normals=True
  bpy.ops.object.modifier_apply(modifier=bevel.name)
 if obj:
  me=obj.data;uv=me.uv_layers.active.data
  for poly in me.polygons:
   if me.materials[poly.material_index].name=='M_Town_TileRed' and .2<poly.normal.z<.999:
    n=poly.normal;ua=Vector((n.y,-n.x,0)).normalized();va=n.cross(ua).normalized()
    for li in poly.loop_indices:
     co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co.dot(ua)/4,co.dot(va)/4)
 return obj
Mesh.finish=finish15
