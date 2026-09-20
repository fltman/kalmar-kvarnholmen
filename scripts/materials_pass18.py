"""Separate fine-scale materials so corrections do not recolour other houses."""
P18={}
for key,texture,color,rough,metal in [('BrickRed','LandmarkBrickRed',(.32,.09,.04),.83,0),('BrickBuff','LandmarkBrickBuff',(.56,.43,.22),.87,0),('BathCream','TownIvory',(.70,.65,.51),.85,0),('Ashlar','LandmarkAshlar',(.39,.38,.33),.8,0),('Grass','Pass18Grass',(.12,.23,.045),.98,0),('GreenJoinery','TownPaintGreen',(.08,.16,.11),.50,0),('ParkingPaint','Pass18Paint',(.75,.74,.66),.85,0)]:
 name='M_Pass18_'+key
 if name not in materials:mat(name,color,rough,metal,texture)
 P18[key]=name
