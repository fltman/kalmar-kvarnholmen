"""Write a local status page that stays readable during long offline exports."""
from pathlib import Path
import html
import json
import time

R = Path(__file__).resolve().parents[1]
OUT = R.parent / 'Kvarnholmen-media'


def write_progress(data, filename='hq-progress.json'):
    target = R / 'media' / filename
    tmp = target.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(target)
    OUT.mkdir(exist_ok=True)
    rows = []
    for kind, title, total, spec in [
        ('houses', 'Husbilder', 343, '1920 × 1080 · PNG'),
        ('street', 'Flygtur genom gatorna', 2016, '1920 × 1080 · 84 sekunder'),
        ('church', 'Flygtur genom domkyrkan', 1056, '1920 × 1080 · 44 sekunder'),
    ]:
        folder = R / 'media' / (kind + '-frames')
        count = len(list(folder.glob('*.png')))
        rows.append(f'<article><h2>{title}</h2><p>{spec}</p><progress max="{total}" value="{count}"></progress><p>{count} av {total} bilder sparade</p></article>')
    stage = data.get('stage', 'rendering')
    message = {'rendering': 'Renderingen pågår', 'verifying': 'Bildfilerna kontrolleras',
               'encoding': 'Filmen kodas', 'repairing': 'Saknade filmrutor kompletteras', 'packaging': 'Galleriet byggs',
               'rendered_awaiting_visual_review': 'Exporten är renderad och väntar på visuell slutkontroll',
               'failed': 'Exporten har stannat och behöver kontrolleras'}.get(stage, 'Exporten pågår')
    detail = html.escape(str(data.get('error', 'Cinematic · 64 samples · förlustfria bildoriginal')))
    link = '<p><a href="index.html">Öppna husgalleriet</a></p>' if (OUT/'original/0342.png').exists() else ''
    page = f'''<!doctype html><html lang="sv"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="20"><title>Kvarnholmen — exportstatus</title><style>body{{background:#101b20;color:#f4f0e7;font:17px/1.6 system-ui;margin:6vw;max-width:900px}}h1{{font:42px Georgia}}h2{{font-size:22px}}p{{color:#b6c5c8}}article{{padding:14px 24px;margin:18px 0;background:#18282e;border:1px solid #34454a;border-radius:10px}}progress{{width:100%;accent-color:#e6c47e}}a{{color:#e6c47e}}small{{color:#b6c5c8}}</style><h1>{message}</h1><p>{detail}</p>{''.join(rows)}{link}<small>Senaste uppdatering: {time.strftime('%Y-%m-%d %H:%M:%S')} lokal tid. Sidan uppdateras var 20:e sekund. Om tidsstämpeln slutar ändras är statusen inaktuell.</small></html>'''
    dest = OUT / 'export-status.html'
    temp = dest.with_suffix('.tmp')
    temp.write_text(page)
    temp.replace(dest)
