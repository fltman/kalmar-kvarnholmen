"""Flush stale virtual-shadow pages following the long batch reimport; restore prior setting."""
import unreal as u,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();old=u.SystemLibrary.get_console_variable_int_value('r.Shadow.Virtual.Cache');ticks=0
u.SystemLibrary.execute_console_command(world,'r.Shadow.Virtual.Cache 0')
def restore_shadow_cache(dt):
 global ticks
 ticks+=1
 if ticks>=6:
  u.SystemLibrary.execute_console_command(world,'r.Shadow.Virtual.Cache '+str(old));u.unregister_slate_post_tick_callback(shadow_handle);(R/'previews/district17-shadow-refresh.json').write_text(json.dumps({'status':'passed','original_cache':old,'restored_cache':u.SystemLibrary.get_console_variable_int_value('r.Shadow.Virtual.Cache'),'time':time.time()}))
shadow_handle=u.register_slate_post_tick_callback(restore_shadow_cache)
