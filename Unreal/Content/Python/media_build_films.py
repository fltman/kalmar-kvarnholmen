from pathlib import Path
P=Path(__file__).resolve().parent
exec(compile((P/'media_movie_helpers.py').read_text(),str(P/'media_movie_helpers.py'),'exec'),globals())
routes=json.loads((R/'media/routes.json').read_text());checks=json.loads((R/'media/routes-validation.json').read_text());assert all(v['status']=='passed' for v in checks.values())
result={}
for key,name in [('street','Flygtur_Kvarnholmen_01'),('church','Flygtur_Domkyrkan_02')]:
 seq=make_sequence(name,routes[key]['frames'],routes[key]['fov']);result[key]=seq.get_path_name()
(R/'media/film-sequences.json').write_text(json.dumps(result,indent=2))
