"""Low red boarded Klapphuset with high multipane windows and supported timber access.
Photo source kalmarkusten.se/platser/klapphuset; dimensions visually estimated on OSM footprint.
"""
name='SM_Kvarnholmen_House_93199604';old=bpy.data.objects.get(name)
if old:bpy.data.objects.remove(old,do_unlink=True)
r=json.loads((R/'source/district17.json').read_text())['buildings'][name];m=Mesh(name,'Kvarnholmen/Completed facades');red='M_Sodra_RedWood';timber='M_Polish_BridgeWood';dark=town_mats['MetalGrey'];H=2.95;nwin=0
for wi,w in enumerate(r['walls']):
 x,y,L,a=sf_edge(w['p'],w['q']);x,y,_=lp(x,y,0,-.30,0,a);bays=max(1,round(L/4));holes=[]
 for j in range(bays):
  u=-L/2+(j+.5)*L/bays
  if wi==3 and j==0:holes.append((u,.15,1.1,2.1,'door'))
  else:holes.append((u,1.68,min(2.45,L/bays*.72),.87,'window'))
 d17_wall(m,x,y,L,a,.12,H,holes,red)
 for u,b,ww,h,k in holes:
  if k=='door':town_door(m,*lp(x,y,u,.03,0,a)[:2],b,ww,h,a,town_mats['PaintGreen'],True)
  else:sf_modern(m,x,y,u,b,ww,h,a,TW,TW,3,6);nwin+=1
 for z in [.22+i*.15 for i in range(18)]:d17_band(m,x,y,L,a,z,holes,red,.027,.025)
 facade_box(m,x,y,0,.45,H-.07,L,.35,.18,dark,a)
 # Closely spaced vertical foundation boards continue into the water.
 for j in range(max(1,round(L/.15))):
  u=-L/2+(j+.5)*L/max(1,round(L/.15));facade_box(m,x,y,u,.29,-.24,.125,.17,.74,timber,a)
 for u in [-L/2+.25,L/2-.25]:town_rod(m,lp(x,y,u,.19,-1.2,a),lp(x,y,u,.19,.20,a),.11,timber,10)
x,y,L,W,a=r['roof_rectangle'];aa=L/2+.28;bb=W/2+.28;inset=bb*.7;rise=1.25
vs=[lp(x,y,u,-v,H+z,a) for u,v,z in [(-aa,-bb,0),(aa,-bb,0),(aa,bb,0),(-aa,bb,0),(-aa+inset,0,rise),(aa-inset,0,rise)]]
m.faces(vs,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],dark)
for u in [-L*.25,L*.25]:
 xx,yy,_=lp(x,y,u,0,0,a);m.box((xx,yy,H+rise+.23),(.85,.65,.46),dark,a)
 for z in [H+rise+.13,H+rise+.28]:facade_box(m,xx,yy,0,.37,z,.76,.055,.052,TW,a)
 m.box((xx,yy,H+rise+.48),(1.08,.87,.12),dark,a)
# Narrow deck to the closest mapped shoreline, fully supported; no invented road under the water.
s=json.loads((R/'source/klapphuset17-shore.json').read_text());P=s['door'];Q=s['shore'];xx,yy,ll,ang=sf_edge(P,Q)
facade_box(m,xx,yy,0,0,.13,ll,1.50,.18,timber,ang)
for j in range(max(1,round(ll/.16))):facade_box(m,xx,yy,-ll/2+(j+.5)*ll/max(1,round(ll/.16)),0,.228,.025,1.48,.016,timber,ang)
for side in [-1,1]:
 for j in range(max(2,round(ll/2.4))+1):
  at=-ll/2+j*ll/max(2,round(ll/2.4));facade_box(m,xx,yy,at,side*.70,.37,.12,.12,1.76,timber,ang)
 for z in [.74,1.15]:facade_box(m,xx,yy,0,side*.70,z,ll,.095,.075,timber,ang)
obj=m.finish();obj['osm_id']='93199604';obj['detail_pass']=17;obj['eaves_height']=H;obj['massing_only']=False;obj['reference_status']='photographed boathouse; footprint mapped, heights and access details estimated'
district17_audit[name]={'windows':nwin,'doors':1,'frontages':5,'rear_segments':0,'roof':'low hipped dark roof with two ventilators','street':'Kattrumpan','reference_status':obj['reference_status'],'reference':'https://www.kalmarkusten.se/platser/klapphuset/'}
district17_cameras.append(('77_Klapphuset',(415,110,2.5),(436,127,1.8),30))
