"""Register the optional standalone still-frame executor only when requested."""
import unreal
if '-MediaFrameStart=' in unreal.SystemLibrary.get_command_line():
    import media_frame_executor
