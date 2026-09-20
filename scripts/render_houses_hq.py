"""Render houses in isolated Unreal processes, retaining the saved 1080p/64-sample preset."""
import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from PIL import Image
from media_progress import write_progress

R = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--engine', type=Path, default=os.environ.get('UNREAL_EDITOR', '/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'))
p.add_argument('--probe', action='store_true', help='Render only the second house into a separate validation folder')
a = p.parse_args()
assert a.engine.is_file(), a.engine
kind = 'house-isolated-probe' if a.probe else 'houses'
folder = R / 'media' / (kind + '-frames')
folder.mkdir(exist_ok=True)
logs = R / 'media' / (kind + '-logs')
logs.mkdir(exist_ok=True)
indices = [1] if a.probe else range(343)
env = os.environ.copy()
if Path('/Applications/Xcode.app/Contents/Developer').is_dir():
    env['DEVELOPER_DIR'] = '/Applications/Xcode.app/Contents/Developer'
started = time.monotonic()

def verify(path):
    with Image.open(path) as image:
        assert image.size == (1920, 1080), (path, image.size)
        image.verify()

for index in indices:
    target = folder / f'{index:05d}.png'
    report = logs / f'{index:05d}.json'
    if report.exists() and target.exists():
        result = json.loads(report.read_text())
        assert result['success'] and result['spatial_samples'] == 64, result
        verify(target)
        continue
    assert not target.exists(), f'Inspect unverified output before resuming: {target}'
    assert shutil.disk_usage(R).free > 2 * 1024**3, 'Not enough free disk space'
    log = logs / f'{index:05d}.log'
    cmd = [str(a.engine), str(R / 'Unreal/KalmarStortorget.uproject'), '/Game/Kalmar/Maps/Stortorget',
           '-game', '-EnablePlugins=MovieRenderPipeline',
           '-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor',
           '-ExecutorPythonClass=/Engine/PythonTypes.KvarnholmenFrameExecutor',
           '-LevelSequence=/Game/Media/Houses_HQ_01.Houses_HQ_01',
           '-MoviePipelineConfig=/Game/Media/MasterStreet1080_HQ.MasterStreet1080_HQ',
           f'-MediaFrameStart={index}', f'-MediaFrameEnd={index + 1}',
           '-MediaOutputDirectory=' + str(folder), '-windowed', '-ResX=640', '-ResY=360',
           '-NoSound', '-NoSplash', '-unattended', '-log', '-abslog=' + str(log)]
    start = time.monotonic()
    completion = None
    with (logs / f'{index:05d}-launch.log').open('w') as output:
        proc = subprocess.Popen(cmd, cwd=R, env=env, stdout=output, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            if shutil.disk_usage(R).free < 2 * 1024**3:
                proc.terminate()
                try: proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
                raise RuntimeError('Export stopped before exhausting free disk space')
            text = log.read_text(errors='replace') if log.exists() else ''
            progress = {'stage': 'rendering', 'job': kind, 'frames': len(list(folder.glob('*.png'))),
                        'current_index': index, 'total': len(indices), 'pid': proc.pid,
                        'elapsed_seconds': round(time.monotonic() - started), 'spatial_samples': 64,
                        'resolution': [1920, 1080], 'isolated_process_per_house': True}
            write_progress(progress)
            if 'Kvarnholmen frame render success: True' in text and 'Engine exit requested' in text:
                if completion is None:
                    completion = time.monotonic()
                elif time.monotonic() - completion > 30:
                    proc.terminate()
                    try: proc.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        proc.kill(); proc.wait()
            elif 'LogPython: Error:' in text or 'Fatal error:' in text:
                proc.terminate()
                try: proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
                raise RuntimeError('Render startup failed; inspect ' + str(log))
            time.sleep(5)
    text = log.read_text(errors='replace') if log.exists() else ''
    assert target.is_file() and 'Kvarnholmen frame render success: True' in text, str(log)
    verify(target)
    result = {'success': True, 'index': index, 'spatial_samples': 64, 'quality': 'Cinematic',
              'resolution': [1920, 1080], 'elapsed_seconds': round(time.monotonic() - start)}
    report.write_text(json.dumps(result, indent=2))
    print(json.dumps(result), flush=True)
result = {'success': True, 'frames': len(indices), 'expected_frames': len(indices),
          'sequence': '/Game/Media/Houses_HQ_01', 'preset': '/Game/Media/MasterStreet1080_HQ',
          'spatial_samples': 64, 'quality': 'Cinematic', 'resolution': [1920, 1080],
          'isolated_process_per_house': True, 'elapsed_seconds': round(time.monotonic() - started)}
(folder / 'render-status.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result), flush=True)
