"""Explicit UV-derivative fallback for Mikk's degenerate skinny-triangle frames.
Only replaces zero exporter vectors; preserves every triangle, UV and normal.
Exporter uses native mesh axes because bake_space_transform=False.
"""
from io_scene_fbx import export_fbx_bin
from mathutils import Vector
import numpy as np

def export_district_fbx(obj, filepath):
 me=obj.data;me.calc_loop_triangles();me.calc_tangents(uvmap=me.uv_layers.active.name)
 uv=me.uv_layers.active.data
 # Double precision, batched UV derivatives avoid float32 cancellation on tiny bevels.
 positions=np.empty(len(me.vertices)*3,dtype=np.float64);me.vertices.foreach_get('co',positions);positions=positions.reshape((-1,3))
 indices=np.empty(len(me.loops),dtype=np.int32);me.loops.foreach_get('vertex_index',indices)
 coords=np.empty(len(me.loops)*2,dtype=np.float64);uv.foreach_get('uv',coords);coords=coords.reshape((-1,2))
 triangles=np.empty(len(me.loop_triangles)*3,dtype=np.int32);me.loop_triangles.foreach_get('loops',triangles);triangles=triangles.reshape((-1,3))
 p=positions[indices[triangles]];q=coords[triangles];a,b=p[:,1]-p[:,0],p[:,2]-p[:,0];d,e=q[:,1]-q[:,0],q[:,2]-q[:,0];det=d[:,0]*e[:,1]-d[:,1]*e[:,0]
 valid=np.abs(det)>1e-15;safe=np.where(valid,det,1)[:,None]
 ts=(a*e[:,1,None]-b*d[:,1,None])/safe;bs=(b*d[:,0,None]-a*e[:,0,None])/safe
 normals=np.empty(len(me.loops)*3,dtype=np.float64);me.corner_normals.foreach_get('vector',normals);normals=normals.reshape((-1,3))
 ids=triangles.reshape(-1);n=normals[ids];t=np.repeat(ts,3,axis=0);bt=np.repeat(bs,3,axis=0);v=t-n*np.sum(t*n,axis=1)[:,None];lengths=np.linalg.norm(v,axis=1);v/=np.maximum(lengths,1e-30)[:,None]
 cross=np.cross(n,v);sign=np.where(np.sum(cross*bt,axis=1)<0,-1,1)
 tangent=np.zeros_like(normals);bitangent=np.zeros_like(normals);validloops=(lengths>1e-12)&np.repeat(valid,3)
 tangent[ids[validloops]]=v[validloops];bitangent[ids[validloops]]=cross[validloops]*sign[validloops,None]
 original=export_fbx_bin.elem_data_single_float64_array;fixed={'Tangents':0,'Binormals':0}
 def write(parent,key,values):
  if key in [b'Tangents',b'Binormals']:
   values=np.array(values,copy=True);vectors=values.reshape((-1,3));fallback=tangent if key==b'Tangents' else bitangent
   missing=np.sum(vectors*vectors,axis=1)<1e-8
   invalid=missing&(np.sum(fallback*fallback,axis=1)<.5)
   if np.any(invalid):raise RuntimeError(f'{obj.name}: no UV-derived frame for loop {int(np.flatnonzero(invalid)[0])}')
   vectors[missing]=fallback[missing];fixed[key.decode()]+=int(np.sum(missing))
   if not np.isfinite(values).all():raise RuntimeError('Nonfinite tangent frame')
  return original(parent,key,values)
 export_fbx_bin.elem_data_single_float64_array=write
 try:
  import bpy
  bpy.ops.export_scene.fbx(filepath=str(filepath),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',use_tspace=True,add_leaf_bones=False,path_mode='AUTO')
 finally:export_fbx_bin.elem_data_single_float64_array=original
 return fixed
