"""Lighting and presentation shared by generation and subsequent iteration.
Software Lumen and Nanite/VSM are used on this Apple Silicon project.
"""
import unreal as u,json,math
from pathlib import Path
R=globals().get('R') or Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);le=u.get_editor_subsystem(u.LevelEditorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
def prop(o,k,v):o.set_editor_property(k,v)
def point(x,y,z):return u.Vector(x*100,-y*100,z*100)
for a in list(ae.get_all_level_actors()):
 label=a.get_actor_label()
 if isinstance(a,u.PointLight) or label=='Soft sky fill' or label.startswith('Window daylight') or label.startswith('Chandelier glow'):ae.destroy_actor(a);continue
 if isinstance(a,u.DirectionalLight):
  a.set_actor_rotation(u.Rotator(pitch=-37,yaw=-50,roll=0),False);c=a.light_component;c.set_intensity(18000);prop(c,'light_source_angle',2.5);prop(c,'use_temperature',True);prop(c,'temperature',5400);prop(c,'indirect_lighting_intensity',1.0)
 if isinstance(a,u.SkyLight):a.light_component.set_intensity(1.0);a.light_component.recapture_sky()
 if isinstance(a,u.ExponentialHeightFog):
  c=a.get_component_by_class(u.ExponentialHeightFogComponent);prop(c,'fog_density',.001);prop(c,'enable_volumetric_fog',True)
 if isinstance(a,u.PostProcessVolume):
  a.unbound=True;s=a.settings
  values={'auto_exposure_method':u.AutoExposureMethod.AEM_HISTOGRAM,'auto_exposure_min_brightness':3.5,'auto_exposure_max_brightness':14.0,'auto_exposure_bias':.35,'auto_exposure_speed_up':3.0,'auto_exposure_speed_down':1.5,'auto_exposure_apply_physical_camera_exposure':False,'white_temp':5800.0,'bloom_intensity':.16,'vignette_intensity':.15,'lumen_scene_lighting_quality':2.0,'lumen_scene_detail':2.0,'lumen_final_gather_quality':2.0,'lumen_scene_view_distance':18000.0,'lumen_max_trace_distance':18000.0,'ambient_occlusion_intensity':.45,'ambient_occlusion_radius':60.0}
  for key,val in values.items():prop(s,'override_'+key,True);prop(s,key,val)
  a.settings=s
# Daylit glazing must remain luminous at the interior exposure level.
glazing=u.load_asset('/Game/Kalmar/Materials/M_Interior_Daylight')
if glazing:
 emission=u.MaterialEditingLibrary.create_material_expression(glazing,u.MaterialExpressionConstant3Vector,-300,-200)
 emission.constant=u.LinearColor(600,650,700,1)
 u.MaterialEditingLibrary.connect_material_property(emission,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 u.MaterialEditingLibrary.recompile_material(glazing);u.EditorAssetLibrary.save_loaded_asset(glazing)
# Window-sized area emitters just inside the glazing. They cast shadows and
# feed indirect light, replacing the previous shadowless point-light wash.
windows=[]
for x in [-13.7,34.0]:
 for y in [38.7,50.1]:windows.append(((x,y,7.1),(10.1,y,7.1),240,680))
for y in [28.1,60.7]:windows.append(((10.1,y,18.0),(10.1,44.4,10),260,540))
for i,(loc,target,w,h) in enumerate(windows):
 lamp=ae.spawn_actor_from_class(u.RectLight,point(*loc),u.MathLibrary.find_look_at_rotation(point(*loc),point(*target)))
 lamp.set_actor_label('Window daylight '+str(i));lamp.set_folder_path('Stortorget/Lighting')
 c=lamp.light_component;c.set_mobility(u.ComponentMobility.MOVABLE);prop(c,'intensity_units',u.LightUnits.LUMENS);c.set_intensity(18000)
 prop(c,'source_width',w);prop(c,'source_height',h);prop(c,'attenuation_radius',4200);prop(c,'cast_shadows',True);prop(c,'use_temperature',True);prop(c,'temperature',6100);prop(c,'indirect_lighting_intensity',1.0)
for i,x in enumerate([-2.9,10.1,27.1]):
 lamp=ae.spawn_actor_from_class(u.PointLight,point(x,44.4,10.8),u.Rotator());lamp.set_actor_label('Chandelier glow '+str(i));lamp.set_folder_path('Stortorget/Lighting')
 c=lamp.light_component;c.set_mobility(u.ComponentMobility.MOVABLE);prop(c,'intensity_units',u.LightUnits.LUMENS);c.set_intensity(1400);prop(c,'use_temperature',True);prop(c,'temperature',2700);prop(c,'source_radius',65);prop(c,'attenuation_radius',1100);prop(c,'cast_shadows',True)
for cmd in ['r.DynamicGlobalIlluminationMethod 1','r.ReflectionMethod 1','r.Lumen.HardwareRayTracing 0','r.AntiAliasingMethod 4','r.ScreenPercentage 85','sg.GlobalIlluminationQuality 3','sg.ReflectionQuality 3','sg.ShadowQuality 3','r.Shadow.Virtual.Enable 1']:
 u.SystemLibrary.execute_console_command(world,cmd)
le.save_current_level()
request_path=R/'previews/hero-review-request.json'
qa_request=json.loads(request_path.read_text()) if request_path.exists() else {}
quality=qa_request.get('quality','high')
percentage={'high':85,'balanced':67,'walkthrough':50}.get(quality,85)
for cmd in ['r.Editor.Viewport.ScreenPercentageMode.RealTime 0','r.Editor.Viewport.ScreenPercentage '+str(percentage),'r.ScreenPercentage '+str(percentage)]:
 u.SystemLibrary.execute_console_command(world,cmd)
if quality in ('balanced','walkthrough'):
 for cmd in ['sg.GlobalIlluminationQuality 2','sg.ReflectionQuality 2','sg.ShadowQuality 2']:u.SystemLibrary.execute_console_command(world,cmd)
(R/'previews/hero-lighting-config.json').write_text(json.dumps({'gi':'Lumen software','reflections':'Lumen','virtual_shadow_maps':True,'sun_lux':18000,'window_rect_lights':len(windows),'window_lumens':18000,'auto_exposure_EV_bounds':[3.5,14],'screen_percentage':percentage,'quality':quality},indent=2))
