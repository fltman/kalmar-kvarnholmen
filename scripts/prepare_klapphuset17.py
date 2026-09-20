from pathlib import Path
import json,sys

from shapely.geometry import Point,Polygon
from shapely.ops import unary_union,nearest_points
R=Path(__file__).resolve().parents[1];d=json.loads((R/'source/kvarnholmen.json').read_text());land=unary_union([Polygon(p['outer'],p['holes']) for p in d['island_outline']]);w=json.loads((R/'source/district17.json').read_text())['buildings']['SM_Kvarnholmen_House_93199604']['walls'][3];P=[w['p'][i]+(w['q'][i]-w['p'][i])*.25 for i in range(2)];Q=nearest_points(Point(P),land)[1];(R/'source/klapphuset17-shore.json').write_text(json.dumps({'door':P,'shore':[Q.x,Q.y]}))
