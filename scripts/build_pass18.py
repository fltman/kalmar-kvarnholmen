"""Final reference corrections override older generative approximations."""
import ast
D18=json.loads((R/'source/pass18.json').read_text());pass18_names=[]
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];CU=TC;RS="M_Landmark_Rubble"
SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']}
for filename in ['build_town_details.py','town_detail_helpers.py','build_larmtorget_facades.py','build_sodra_facades.py','build_landmarks14.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(tree,filename,'exec'))
exec(compile((R/'scripts/materials_pass18.py').read_text(),'materials_pass18.py','exec'))
exec(compile((R/'scripts/pass18_helpers.py').read_text(),'pass18_helpers.py','exec'))
exec(compile((R/'scripts/materials_portal19.py').read_text(),'materials_portal19.py','exec'))
for filename in ['build_pass18_landmarks.py','build_pass18_gates.py','build_pass18_extra.py','build_pass18_gerdas.py','build_pass18_surfaces.py']:
 exec(compile((R/'scripts'/filename).read_text(),str(R/'scripts'/filename),'exec'))
pass18_names=list(dict.fromkeys(pass18_names))
pass18_cameras=[('78_Riskvarnen',(378,-205,4),(327,-127,17),26),('79_Riskvarnen_West',(285,-170,4),(321,-115,15),23),('80_Varmbadhuset',(367,-119,3),(404,-79,7.5),25),('81_Badhusportal',(383,-77,2.2),(395.6,-77,3.8),28),('82_Jordbroporten',(-187.7,-220,2.0),(-187.7,-194.5,3.0),26),('83_Kavaljeren',(51.3,-192,2.0),(51.3,-165.8,3.0),30),('84_Vasterport',(-375,112,2.1),(-348.3,92.3,4.4),29),('85_Witt_Rear',(73,-143,2.2),(73,-132,4.5),23),('86_Barometern',(-35,-49,2.1),(-40,-49,2.5),18),('87_Torget_Husgrans',(-8,-10,3),(-8,-35,5),25),('88_Markytor',(400,-270,150),(200,-60,0),29)]

pass18_cameras.append(('89_Gerdas',(-116.8,1.4,3.5),(-122.8,-8.46,9.0),14.5))

pass18_cameras.append(('90_Gerdas_Portal',(-122.8,-2.5,2.1),(-122.8,-8.46,3.1),28))
