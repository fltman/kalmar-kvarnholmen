"""Run the complete high-quality export and package it for offline viewing.

Completed jobs are reusable after verification; partial render folders require
manual inspection instead of being overwritten. Nothing is uploaded by this tool.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image
from media_progress import write_progress

R = Path(__file__).resolve().parents[1]
MEDIA = R / 'media'
OUT = R.parent / 'Kvarnholmen-media'
JOBS = [('houses', 343, (1920, 1080)), ('street', 2016, (1920, 1080)),
        ('church', 1056, (1920, 1080))]
STATUS = MEDIA / 'export-status.json'


def record(stage, **details):
    data = {'stage': stage, 'updated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), **details}
    write_progress(data, 'export-status.json')
    print(json.dumps(data), flush=True)


def run(script, *args):
    subprocess.run([sys.executable, str(R / 'scripts' / script), *args], cwd=R, check=True)


def verify_frames(kind, count, size):
    folder = MEDIA / (kind + '-frames')
    result = json.loads((folder / 'render-status.json').read_text())
    assert result['success'] and result['frames'] == count, result
    assert result['spatial_samples'] == 64 and result['quality'] == 'Cinematic', result
    assert len(list(folder.glob('*.png'))) == count, folder
    for i in range(count):
        path = folder / f'{i:05d}.png'
        with Image.open(path) as image:
            assert image.size == size, (path, image.size)
            image.verify()
    (MEDIA / (kind + '-image-verification.json')).write_text(json.dumps({
        'success': True, 'count': count, 'resolution': size,
        'png_integrity': 'passed', 'visual_review': 'pending',
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', help='Path to the Unreal Editor executable')
    parser.add_argument('--film', choices=['street','church'], help='Process only one film')
    parser.add_argument('--available-frames', action='store_true', help='Encode existing frames without filling gaps, when explicitly requested')
    args = parser.parse_args()
    MEDIA.mkdir(exist_ok=True)
    for kind, count, size in JOBS:
        if args.film and kind != args.film: continue
        report = MEDIA / (kind + '-frames') / 'render-status.json'
        engine_args = ['--engine', args.engine] if args.engine else []
        if kind == 'houses':
            if not report.exists():
                record('rendering', job=kind)
                run('render_houses_hq.py', *engine_args)
        else:
            folder = MEDIA / (kind + '-frames')
            if not report.exists() and not list(folder.glob('*.png')):
                record('rendering', job=kind)
                try:
                    run('render_media_hq.py', kind, *engine_args)
                except subprocess.CalledProcessError:
                    # A completed engine run can still omit frames; repair the gaps.
                    if not report.exists() or not list(folder.glob('*.png')):
                        raise
            complete = report.exists() and json.loads(report.read_text()).get('success')
            if not complete and not args.available_frames:
                record('repairing', job=kind)
                run('repair_film_frames.py', kind, *engine_args)
        record('verifying', job=kind)
        if kind == 'houses' or not args.available_frames:
            verify_frames(kind, count, size)
        if kind != 'houses':
            record('encoding', job=kind)
            run('encode_media_films.py', kind, *(['--available-frames'] if args.available_frames else []))
            run('build_media_gallery.py')
        else:
            for start in range(0, count, 50):
                run('media_contact_sheet.py', str(MEDIA / 'houses-frames'),
                    str(MEDIA / f'houses-hq-review-{start:03d}.jpg'),
                    '--start', str(start), '--end', str(min(start + 50, count)))
    record('packaging')
    run('build_media_gallery.py')
    record('rendered_awaiting_visual_review', gallery=str(OUT / 'index.html'),
           house_images=343, house_resolution=[1920, 1080],
           film_resolution=[1920, 1080], films_seconds=[json.loads((MEDIA/(k+'-encoding.json')).read_text())['duration_seconds'] if (MEDIA/(k+'-encoding.json')).exists() else None for k in ['street','church']])


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        record('failed', error=str(error))
        raise
