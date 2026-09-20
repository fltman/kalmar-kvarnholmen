"""Encode verified Unreal frame sequences into portable, silent H.264 films."""
from pathlib import Path
import json,subprocess,shutil,argparse
R=Path(__file__).resolve().parents[1];OUT=R.parent/'Kvarnholmen-media'/'filmer'
parser=argparse.ArgumentParser();parser.add_argument('film',choices=['street','church','all'],default='all',nargs='?');args=parser.parse_args()
ffmpeg=shutil.which('ffmpeg');ffprobe=shutil.which('ffprobe');assert ffmpeg and ffprobe,'Install ffmpeg first'
OUT.mkdir(parents=True,exist_ok=True)
for kind,title,count,poster,poster_frame in [('street','Kvarnholmen-gator',2016,'gator',400),('church','Kalmar-domkyrka',1056,'domkyrkan',250)]:
 if args.film not in ['all',kind]:continue
 folder=R/'media'/f'{kind}-frames';status=json.loads((folder/'render-status.json').read_text())
 assert status['success'] and status['frames']==count and status['spatial_samples']==64 and status['quality']=='Cinematic',status
 assert all((folder/f'{i:05d}.png').is_file() for i in range(count)),'Missing frames'
 target=OUT/(title+'.mp4')
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','warning','-y','-framerate','24','-start_number','0','-i',str(folder/'%05d.png'),'-frames:v',str(count),'-c:v','libx264','-threads','4','-preset','veryslow','-crf','14','-pix_fmt','yuv420p','-movflags','+faststart','-metadata','title='+title,'-metadata','comment=Kalmar Kvarnholmen project | CC BY 4.0 | Map data OpenStreetMap contributors',str(target)],check=True)
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(folder/f'{poster_frame:05d}.png'),'-frames:v','1','-q:v','2',str(OUT/(poster+'-poster.jpg'))],check=True)
 info=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(target)]));video=next(s for s in info['streams'] if s['codec_type']=='video')
 assert (video['width'],video['height'],video['nb_frames'])==(1920,1080,str(count)),video
 assert abs(float(info['format']['duration'])-count/24)<.05
 subprocess.run([ffmpeg,'-v','error','-i',str(target),'-f','null','-'],check=True)
 (R/'media'/f'{kind}-video-verification.json').write_text(json.dumps(info,indent=2))
 print('VERIFIED',target,flush=True)
