import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
obj=u.get_default_object(u.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
result={}
for name in ['throttle_cpu_when_not_foreground','bThrottleCPUWhenNotForeground','ThrottleCPUWhenNotForeground']:
 try:
  v=obj.get_editor_property(name);obj.set_editor_property(name,v);result[name]={'value':v,'writable':True}
 except Exception as e:result[name]={'error':str(e)}
(R/'previews/qa-setting-probe.json').write_text(json.dumps(result,indent=2))
u.log('QA_SETTINGS_PROBED')
