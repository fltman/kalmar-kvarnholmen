"""Prepare high-resolution stills and save all export assets before standalone rendering."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
exec(compile((P/'media_movie_helpers.py').read_text(),str(P/'media_movie_helpers.py'),'exec'),globals())
items=json.loads((R/'media/houses-plan.json').read_text())['items']
seq=make_stills('Houses_HQ_01',items)
assert u.EditorAssetLibrary.does_asset_exist('/Game/Media/MasterStreet1080_HQ')
assert u.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
(R/'media/hq-houses.json').write_text(json.dumps({'sequence':seq.get_path_name(),'base_preset':'/Game/Media/MasterStreet1080_HQ','resolution':[1920,1080],'count':len(items),'spatial_samples':64,'saved':True},indent=2))
u.log('HQ house assets saved. Close the editor before starting the standalone renderer.')
