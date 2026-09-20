"""High-quality offline rendering settings; no reduced quality to meet a time limit."""
import unreal as u
from pathlib import Path
R=Path(__file__).resolve().parents[3]
def build_hq_config(name,folder,width=1920,height=1080,limit=None):
 path='/Game/Media/'+name
 assert not u.EditorAssetLibrary.does_asset_exist(path),path
 cfg=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Media',u.MoviePipelinePrimaryConfig,u.MoviePipelinePrimaryConfigFactory())
 out=cfg.find_or_add_setting_by_class(u.MoviePipelineOutputSetting);out.output_directory=u.DirectoryPath(str(R/'media'/folder));out.output_resolution=u.IntPoint(width,height);out.file_name_format='{frame_number}';out.zero_pad_frame_numbers=5;out.use_custom_frame_rate=True;out.output_frame_rate=u.FrameRate(24,1)
 if limit:out.use_custom_playback_range=True;out.custom_start_frame=0;out.custom_end_frame=limit
 cfg.find_or_add_setting_by_class(u.MoviePipelineDeferredPassBase);cfg.find_or_add_setting_by_class(u.MoviePipelineImageSequenceOutput_PNG)
 aa=cfg.find_or_add_setting_by_class(u.MoviePipelineAntiAliasingSetting);aa.spatial_sample_count=64;aa.temporal_sample_count=1;aa.override_anti_aliasing=True;aa.anti_aliasing_method=u.AntiAliasingMethod.AAM_NONE;aa.engine_warm_up_count=120;aa.render_warm_up_count=64;aa.render_warm_up_frames=True
 game=cfg.find_or_add_setting_by_class(u.MoviePipelineGameOverrideSetting)
 for key in ['cinematic_quality_settings','use_lod_zero','disable_hlo_ds','use_high_quality_shadows','override_view_distance_scale']:game.set_editor_property(key,True)
 game.set_editor_property('view_distance_scale',10)
 for key in ['flush_grass_streaming','flush_streaming_managers','override_grass_cull_distance_scale','override_virtual_texture_feedback_factor']:game.set_editor_property(key,False)
 game.set_editor_property('texture_streaming',u.MoviePipelineTextureStreamingMethod.FULLY_LOAD)
 cvars=cfg.find_or_add_setting_by_class(u.MoviePipelineConsoleVariableSetting)
 for key,value in {'r.ScreenPercentage':100,'r.MotionBlurQuality':0,'r.Tonemapper.Quality':5,'r.Nanite.MaxPixelsPerEdge':0.5,'r.Lumen.Reflections.DownsampleFactor':1,'r.Shadow.Virtual.ResolutionLodBiasDirectional':-2,'t.MaxFPS':0,'t.IdleWhenNotForeground':0}.items():cvars.add_or_update_console_variable(key,value)
 u.EditorAssetLibrary.save_loaded_asset(cfg);return cfg
