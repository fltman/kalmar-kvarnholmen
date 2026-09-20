"""Create editable camera sequences for the standalone Movie Render Queue export."""
import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem)
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def make_sequence(name,frames,fov=78):
 path='/Game/Media/'+name
 if u.EditorAssetLibrary.does_asset_exist(path):
  raise RuntimeError('Choose a new sequence name rather than overwrite an existing sequence: '+path)
 seq=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Media',u.LevelSequence,u.LevelSequenceFactoryNew());seq.set_display_rate(u.FrameRate(24,1));seq.set_playback_start(0);seq.set_playback_end(len(frames))
 actor=ae.spawn_actor_from_class(u.CameraActor,vec(frames[0]['location']));actor.set_actor_label('Media temporary camera');actor.camera_component.set_field_of_view(fov);actor.camera_component.set_editor_property('aspect_ratio',16/9);actor.camera_component.set_editor_property('constrain_aspect_ratio',False)
 actor.set_actor_rotation(u.MathLibrary.find_look_at_rotation(vec(frames[0]['location']),vec(frames[0]['target'])),False)
 binding=seq.add_spawnable_from_instance(actor);ae.destroy_actor(actor)
 section=binding.add_track(u.MovieScene3DTransformTrack).add_section();section.set_range(0,len(frames));channels=section.get_all_channels();previous=None
 for frame,s in enumerate(frames):
  p=vec(s['location']);rot=u.MathLibrary.find_look_at_rotation(p,vec(s['target']));angles=[rot.roll,rot.pitch,rot.yaw]
  if previous:
   for j in range(3):
    while angles[j]-previous[j]>180:angles[j]-=360
    while angles[j]-previous[j]<-180:angles[j]+=360
  previous=angles;values=[p.x,p.y,p.z,*angles,1,1,1]
  for channel,value in zip(channels,values):channel.add_key(u.FrameNumber(frame),value,interpolation=u.MovieSceneKeyInterpolation.LINEAR)
 cut=seq.add_track(u.MovieSceneCameraCutTrack).add_section();cut.set_range(0,len(frames));bid=u.MovieSceneObjectBindingID();bid.set_editor_property('guid',binding.get_id());cut.set_camera_binding_id(bid)
 u.EditorAssetLibrary.save_loaded_asset(seq);return seq

def make_stills(name,items):
 path='/Game/Media/'+name
 assert not u.EditorAssetLibrary.does_asset_exist(path),path
 seq=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Media',u.LevelSequence,u.LevelSequenceFactoryNew());seq.set_display_rate(u.FrameRate(24,1));seq.set_playback_start(0);seq.set_playback_end(len(items));cuts=seq.add_track(u.MovieSceneCameraCutTrack)
 for i,item in enumerate(items):
  p=vec(item['location']);rot=u.MathLibrary.find_look_at_rotation(p,vec(item['target']));a=ae.spawn_actor_from_class(u.CameraActor,p,rot);a.camera_component.set_field_of_view(item['fov']);a.camera_component.set_editor_property('aspect_ratio',16/9);a.camera_component.set_editor_property('constrain_aspect_ratio',False);a.set_actor_label(str(item.get('index',i)))
  binding=seq.add_spawnable_from_instance(a);ae.destroy_actor(a);s=binding.add_track(u.MovieScene3DTransformTrack).add_section();s.set_range(i,i+1)
  for ch,val in zip(s.get_all_channels(),[p.x,p.y,p.z,rot.roll,rot.pitch,rot.yaw,1,1,1]):ch.set_default(val)
  cut=cuts.add_section();cut.set_range(i,i+1);bid=u.MovieSceneObjectBindingID();bid.set_editor_property('guid',binding.get_id());cut.set_camera_binding_id(bid)
 u.EditorAssetLibrary.save_loaded_asset(seq);return seq
