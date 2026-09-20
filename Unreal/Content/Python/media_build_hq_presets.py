"""Create the two cinematic film presets and a short validation preset."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
exec(compile((P/"media_hq_settings.py").read_text(),str(P/"media_hq_settings.py"),"exec"),globals())
report={}
for kind,name,limit in [("street","MasterStreet1080_HQ",None),("church","MasterChurch1080_HQ",None),("hq-probe","MasterProbe1080_HQ",8)]:
 cfg=build_hq_config(name,kind+"-frames",limit=limit);report[kind]=cfg.get_path_name()
(R/"media/hq-presets.json").write_text(json.dumps({"presets":report,"resolution":[1920,1080],"fps":24,"spatial_samples":64,"temporal_samples":1,"quality":"Cinematic","intermediate":"lossless PNG"},indent=2))
