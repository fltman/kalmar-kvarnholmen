"""Unattended wrapper: run import_union_081_143.py with its own __file__, save, then quit the editor."""
import unreal as u,traceback
from pathlib import Path
P=Path(__file__).resolve().parent
try:
 exec(compile((P/'import_union_081_143.py').read_text(),str(P/'import_union_081_143.py'),'exec'),{'__file__':str(P/'import_union_081_143.py')})
 u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level();u.log('UNION_WRAPPER_OK')
except Exception:
 u.log_error('UNION_WRAPPER_FAILED\n'+traceback.format_exc())
finally:
 u.SystemLibrary.quit_editor()
