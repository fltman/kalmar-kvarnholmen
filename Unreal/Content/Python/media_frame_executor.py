"""Render a selected still frame without retaining GPU allocations between houses."""
import unreal as u
import math


@u.uclass()
class KvarnholmenFrameExecutor(u.MoviePipelinePythonHostExecutor):
    active_pipeline = u.uproperty(u.MoviePipeline)

    def _post_init(self):
        self.active_pipeline = None

    @u.ufunction(override=True)
    def execute_delayed(self, in_pipeline_queue):
        _, _, args = u.SystemLibrary.parse_command_line(u.SystemLibrary.get_command_line())
        sequence = args['LevelSequence']
        preset = u.load_asset(args['MoviePipelineConfig'])
        if not preset:
            raise RuntimeError('Render preset could not be loaded')
        self.pipeline_queue = u.new_object(u.MoviePipelineQueue, outer=self)
        job = self.pipeline_queue.allocate_new_job(u.MoviePipelineExecutorJob)
        job.sequence = u.SoftObjectPath(sequence)
        # Framing was reviewed at 16:10. Preserve that vertical coverage at 16:9.
        sequence_asset = u.load_asset(sequence)
        for binding in sequence_asset.get_spawnables():
            camera = binding.get_object_template()
            if isinstance(camera, u.CameraActor):
                component = camera.camera_component
                old_fov = component.get_editor_property('field_of_view')
                fov = math.degrees(2 * math.atan(math.tan(math.radians(old_fov) / 2) * (10 / 9)))
                component.set_field_of_view(fov)
        config = job.get_configuration()
        config.copy_from(preset)
        output = config.find_or_add_setting_by_class(u.MoviePipelineOutputSetting)
        output.output_resolution = u.IntPoint(1920, 1080)
        output.use_custom_playback_range = True
        output.custom_start_frame = int(args['MediaFrameStart'])
        output.custom_end_frame = int(args['MediaFrameEnd'])
        output.output_directory = u.DirectoryPath(args['MediaOutputDirectory'])
        aa = config.find_or_add_setting_by_class(u.MoviePipelineAntiAliasingSetting)
        assert aa.spatial_sample_count == 64
        assert (output.output_resolution.x, output.output_resolution.y) == (1920, 1080)
        game = config.find_or_add_setting_by_class(u.MoviePipelineGameOverrideSetting)
        assert game.get_editor_property('cinematic_quality_settings')
        assert game.get_editor_property('texture_streaming') == u.MoviePipelineTextureStreamingMethod.FULLY_LOAD
        config.initialize_transient_settings()
        self.active_pipeline = u.new_object(self.target_pipeline_class, outer=self.get_last_loaded_world(), base_type=u.MoviePipeline)
        self.active_pipeline.on_movie_pipeline_work_finished_delegate.add_function_unique(self, 'finished')
        self.active_pipeline.initialize(job)

    @u.ufunction(override=True)
    def is_rendering(self):
        return self.active_pipeline is not None

    @u.ufunction(ret=None, params=[u.MoviePipelineOutputData])
    def finished(self, results):
        u.log('Kvarnholmen frame render success: ' + str(results.success))
        self.active_pipeline = None
        if not results.success:
            self.on_executor_errored_impl(None, True, 'Still-frame render failed')
        self.on_executor_finished_impl()
