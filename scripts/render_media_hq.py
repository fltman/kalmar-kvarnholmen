"""Render the saved cinematic presets without keeping an editor open alongside them."""
import argparse,json,os,shutil,subprocess,time
from pathlib import Path
from media_progress import write_progress
R=Path(__file__).resolve().parents[1]
JOBS={
 'hq-probe':('MasterProbe1080_HQ','Flygtur_Kvarnholmen_01',8),
 'street':('MasterStreet1080_HQ','Flygtur_Kvarnholmen_01',2016),
 'church':('MasterChurch1080_HQ','Flygtur_Domkyrkan_02',1056),
}
p=argparse.ArgumentParser();p.add_argument('job',choices=[*JOBS,'all']);p.add_argument('--engine',type=Path,default=os.environ.get('UNREAL_EDITOR','/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'));a=p.parse_args();assert a.engine.is_file(),a.engine
progress=R/'media/hq-progress.json';env=os.environ.copy()
if Path('/Applications/Xcode.app/Contents/Developer').is_dir():env['DEVELOPER_DIR']='/Applications/Xcode.app/Contents/Developer'
for kind in (['street','church'] if a.job=='all' else [a.job]):
 preset,sequence,count=JOBS[kind];folder=R/'media'/(kind+'-frames');folder.mkdir(parents=True,exist_ok=True)
 assert not list(folder.glob('*.png')),'Move previous frames aside before starting a fresh render: '+str(folder)
 log=R/'media'/('standalone-'+kind+'.log');start=time.monotonic();last_complete=None
 cmd=[str(a.engine),str(R/'Unreal/KalmarStortorget.uproject'),'/Game/Kalmar/Maps/Stortorget','-game','-EnablePlugins=MovieRenderPipeline','-LevelSequence=/Game/Media/'+sequence+'.'+sequence,'-MoviePipelineConfig=/Game/Media/'+preset+'.'+preset,'-windowed','-ResX=640','-ResY=360','-NoSound','-NoSplash','-unattended','-log','-abslog='+str(log)]
 with (R/'media'/('standalone-'+kind+'-launch.log')).open('w') as output:
  proc=subprocess.Popen(cmd,cwd=R,env=env,stdout=output,stderr=subprocess.STDOUT)
  while proc.poll() is None:
   done=len(list(folder.glob('*.png')));elapsed=time.monotonic()-start
   write_progress({'stage':'rendering','job':kind,'frames':done,'total':count,'elapsed_seconds':round(elapsed),'pid':proc.pid,'spatial_samples':64})
   if shutil.disk_usage(R).free<2*1024**3:
    proc.terminate();proc.wait(timeout=30);raise RuntimeError('Export stopped before exhausting free disk space')
   text=log.read_text(errors='replace') if log.exists() else ''
   if done==count and 'Engine exit requested' in text and 'Movie Pipeline completed.' in text:
    if last_complete is None:last_complete=time.monotonic()
    elif time.monotonic()-last_complete>30:
     # Only a completed, non-editor render process with all expected output files.
     proc.terminate();proc.wait(timeout=30)
   time.sleep(5)
 text=log.read_text(errors='replace') if log.exists() else '';done=len(list(folder.glob('*.png')))
 success=done==count and 'Movie Pipeline completed.' in text and 'Fatal error:' not in text
 result={'success':success,'frames':done,'expected_frames':count,'sequence':'/Game/Media/'+sequence,'preset':'/Game/Media/'+preset,'spatial_samples':64,'quality':'Cinematic','exit_code':proc.returncode,'elapsed_seconds':round(time.monotonic()-start)}
 (folder/'render-status.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
 if not success:raise RuntimeError('Incomplete render; inspect '+str(log))
progress.write_text(json.dumps({'stage':'complete','job':a.job}))
