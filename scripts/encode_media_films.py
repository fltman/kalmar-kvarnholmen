"""Encode Unreal frames into portable, silent H.264 films."""
from pathlib import Path
import json,subprocess,shutil,argparse,tempfile,os,time
from media_progress import write_progress
from PIL import Image
R=Path(__file__).resolve().parents[1];OUT=R.parent/'Kvarnholmen-media'/'filmer'
parser=argparse.ArgumentParser()
parser.add_argument('film',choices=['street','church','all'],default='all',nargs='?')
parser.add_argument('--available-frames',action='store_true',help='Explicitly skip missing frames and concatenate the available originals at 24 fps')
args=parser.parse_args()
ffmpeg=shutil.which('ffmpeg');ffprobe=shutil.which('ffprobe');assert ffmpeg and ffprobe,'Install ffmpeg first'
OUT.mkdir(parents=True,exist_ok=True)
for kind,title,expected,poster,poster_frame in [('street','Kvarnholmen-gator',2016,'gator',400),('church','Kalmar-domkyrka',1056,'domkyrkan',250)]:
 if args.film not in ['all',kind]:continue
 folder=R/'media'/f'{kind}-frames';status=json.loads((folder/'render-status.json').read_text())
 assert status['spatial_samples']==64 and status['quality']=='Cinematic',status
 frames=sorted(p for p in folder.glob('*.png') if p.stem.isdigit() and 0<=int(p.stem)<expected)
 missing=[i for i in range(expected) if not (folder/f'{i:05d}.png').exists()]
 if not args.available_frames:
  assert status['success'] and not missing and len(frames)==expected,status
 assert frames,'No frames to encode'
 for path in frames:
  with Image.open(path) as im:
   assert im.size==(1920,1080),(path,im.size)
   im.verify()
 count=len(frames);target=OUT/(title+'.mp4');temporary_target=OUT/(title+'.encoding.mp4')
 with tempfile.TemporaryDirectory(prefix=kind+'-encode-',dir=R/'media') as temp:
  sequence=Path(temp)
  for n,src in enumerate(frames):os.link(src,sequence/f'{n:05d}.png')
  encoder_progress=R/'media'/(kind+'-encoder-progress.txt')
  proc=subprocess.Popen([ffmpeg,'-progress',str(encoder_progress),'-nostats','-hide_banner','-loglevel','warning','-y','-framerate','24','-start_number','0','-i',str(sequence/'%05d.png'),'-frames:v',str(count),'-c:v','libx264','-threads','4','-preset','veryslow','-crf','14','-pix_fmt','yuv420p','-movflags','+faststart','-metadata','title='+title,'-metadata','comment=Kalmar Kvarnholmen project | CC BY 4.0 | Map data OpenStreetMap contributors',str(temporary_target)])
  while proc.poll() is None:
   values=dict(line.split('=',1) for line in encoder_progress.read_text().splitlines() if '=' in line) if encoder_progress.exists() else {}
   write_progress({'stage':'encoding','job':kind,'encoded_frames':int(values.get('frame',0)),'frames':count,'total':expected,'mode':'available_frames' if args.available_frames else 'complete_sequence'},'export-status.json')
   time.sleep(5)
  if proc.returncode: raise subprocess.CalledProcessError(proc.returncode,proc.args)
 info=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(temporary_target)]));video=next(s for s in info['streams'] if s['codec_type']=='video')
 assert (video['width'],video['height'],video['nb_frames'])==(1920,1080,str(count)),video
 assert abs(float(info['format']['duration'])-count/24)<.05
 subprocess.run([ffmpeg,'-v','error','-i',str(temporary_target),'-f','null','-'],check=True)
 temporary_target.replace(target)
 info['format']['filename']=str(target)
 poster_source=min(frames,key=lambda p:abs(int(p.stem)-poster_frame))
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(poster_source),'-frames:v','1','-q:v','2',str(OUT/(poster+'-poster.jpg'))],check=True)
 (R/'media'/f'{kind}-video-verification.json').write_text(json.dumps(info,indent=2))
 (R/'media'/f'{kind}-encoding.json').write_text(json.dumps({'success':True,'mode':'available_frames' if args.available_frames else 'complete_sequence','source_frames':[int(p.stem) for p in frames],'frames':count,'expected_frames':expected,'missing_frames':missing,'duration_seconds':count/24,'resolution':[1920,1080],'fps':24,'spatial_samples':64,'file':str(target)},indent=2))
 print('VERIFIED',target,'frames',count,'seconds',count/24,flush=True)
