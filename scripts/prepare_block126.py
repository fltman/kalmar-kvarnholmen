"""Pass 126: Kalmar slott, the courtyard level, the west range's windows and Kungstrappan.

Decisions (see references/block126-notes.md for the evidence):
- The courtyard floor is 6.80 m above the water (z 5.47), not pass 27's 9.50 (z 8.17): 2.70 m lower.
  31 steps (7 from the courtyard to the entrance, 24 by Drottningtrappan, kalmarslott.se) up to the
  state floor at z 10.47 give a riser of 0.161 m. Pass 27's own courtyard measurement (eaves 12.2 m
  above the courtyard floor) then puts the courtyard eaves at z 17.7, 2.6 m under the outer eaves,
  which is what the courtyard photographs show (state-floor window heads about 2-2.5 m under the
  courtyard eaves).
- The courtyard's first window row is the state floor's row: sill z 11.57, 3.2 m high, as the outer
  main row (pass 27) and as Gyllene salen's courtyard windows in the 1930s photograph.
- Outer main-floor windows of the west front 55-56 at s 6.45 and 14.25 (Zettervall's west elevation
  of 1883: s 6.4 and 14.5; the 2009 panorama of Gyllene salen: s 6.5 and 14.0).
- Gyllene salen's courtyard wall: two niches, at s 10.4 (the 1930s photograph) and s 15.36 (pass 27's
  courtyard window, on the courtyard).
- Kungsmakstornet's main window turns to face Kungsmaket's west niche (+c), as in Zettervall.
- Kungstrappan (55): a dog-leg stair of 2 x 15 risers between Kuretornet's courtyard face and the
  courtyard front, entered by portal E (pass 27's door at the middle of the front piece W1-V), up to
  the förstuga at the state floor, which runs over the gate passage to Gyllene salen's south-east door.
Output: source/block126.json. Run: python3 scripts/prepare_block126.py (no Shapely needed).
"""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());B125=json.loads((R/'source/block125.json').read_text())
HL=C27['levels_h'];CA=C27['castle']
def zh(h):return round(-1.33+h,4)
FL=B125['floor'];Z0=zh(HL['foot'])

# ---------------------------------------------------------------- the courtyard level
STEPS=7+24                                   # kalmarslott.se, tillgänglighet
H_COURT=6.80                                 # m above the water
ZC=zh(H_COURT);RISER=(FL-ZC)/STEPS
EAVES_COURT=ZC+12.2                          # pass 27: courtyard eaves 12.2 m above the courtyard floor
assert .155<=RISER<=.170,RISER
assert abs(EAVES_COURT-zh(HL['eaves']))>2.0  # the courtyard eaves are not the outer eaves
# ---------------------------------------------------------------- frames
O,U,N=B125['frame']['origin'],B125['frame']['u'],B125['frame']['n']
def F(p):dx,dy=p[0]-O[0],p[1]-O[1];return (dx*U[0]+dy*U[1],dx*N[0]+dy*N[1])
CI=[tuple(p) for p in CA['court']];W1,V,NC=CI[10],CI[9],CI[8]
L=math.dist(W1,NC);E=((NC[0]-W1[0])/L,(NC[1]-W1[1])/L);IN=(-E[1],E[0])       # Q frame: a from W1 towards N, b inwards
# inwards must point away from the courtyard (towards the outer front, c rising)
if IN[0]*N[0]+IN[1]*N[1]<0:IN=(E[1],-E[0])
def Q(a,b):return (W1[0]+E[0]*a+IN[0]*b,W1[1]+E[1]*a+IN[1]*b)
A_DOOR=math.dist(W1,V)/2                     # pass 27's door at the middle of W1-V: portal E
# Kuretornet's courtyard face (pass 27's fitted rectangle) and its 0.355 m skin
kp=[tuple(p) for p in CA['kure']];ek=max(zip(kp,kp[1:]+kp[:1]),key=lambda e:math.dist(*e));ka=math.atan2(ek[1][1]-ek[0][1],ek[1][0]-ek[0][0])
ku=(math.cos(ka),math.sin(ka));kv=(-ku[1],ku[0]);cx=sum(p[0] for p in kp)/len(kp);cy=sum(p[1] for p in kp)/len(kp)
us=[(p[0]-cx)*ku[0]+(p[1]-cy)*ku[1] for p in kp];vs=[(p[0]-cx)*kv[0]+(p[1]-cy)*kv[1] for p in kp]
cx,cy=cx+ku[0]*(max(us)+min(us))/2+kv[0]*(max(vs)+min(vs))/2,cy+ku[1]*(max(us)+min(us))/2+kv[1]*(max(vs)+min(vs))/2
hu,hv=(max(us)-min(us))/2,(max(vs)-min(vs))/2
KR=[(cx+ku[0]*a_*hu+kv[0]*b_*hv,cy+ku[1]*a_*hu+kv[1]*b_*hv) for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))]
kface=min(zip(KR,KR[1:]+KR[:1]),key=lambda e:F(e[0])[1]+F(e[1])[1])
def b_of(p):return (p[0]-W1[0])*IN[0]+(p[1]-W1[1])*IN[1]
def a_of(p):return (p[0]-W1[0])*E[0]+(p[1]-W1[1])*E[1]
k0,k1=kface;ka0,ka1=sorted([(a_of(k0),b_of(k0)),(a_of(k1),b_of(k1))])
def bkure(a):return ka0[1]+(ka1[1]-ka0[1])*(a-ka0[0])/(ka1[0]-ka0[0])-.36   # the skin's face
# ---------------------------------------------------------------- Kungstrappan
T=.30;NR=15                                   # tread; risers per flight (2 x 15 = 30)
R2=(FL-ZC)/(2*NR)
A_TOP=A_DOOR-1.23                             # the flights end where the entry hall begins
A_MID=A_TOP-(NR-1)*T                          # first riser of flight 2 / last of flight 1
LANE_C=(0.0,1.70);SPINE=(1.70,1.90);LANE_K0=1.90
B_LAND=3.55                                   # the landing's inner edge (Kuretornet ends near here)
A_END=.40                                     # the stair hall's end wall
A_HALL=A_DOOR+1.40                            # the entry hall's far wall (under the förstuga)
Z_CEIL=15.20
assert R2>=.15 and R2<=.19,R2
w_k=min(bkure(a) for a in (A_MID,A_TOP))-LANE_K0-.04
assert w_k>=1.5,('flight 2 too narrow',w_k)
assert A_MID-A_END>=1.6,('mid landing too short',A_MID-A_END)
# the gate passage's vault (pass 124: walls 2.4, radius 1.5, 0.3 m thick) at the courtyard end
vault_top=ZC+.012+2.4+1.5+.3
assert vault_top<FL-.3,('the förstuga floor would cut the passage vault',vault_top)
# ---------------------------------------------------------------- windows
WIN_OUT=[6.45,14.25]                          # front 55-56, s in pass 125's frame (front starts at s 0)
WIN_GYLL_COURT=[10.4,15.361]
SILL=Z0+7.9;HWIN=3.2
out=dict(source='pass 126: kalmarslott.se step counts, pass 27 measurements, Zettervall 1883, photographs; see references/block126-notes.md',
 h_court=H_COURT,zc=ZC,zc_pass27=zh(HL['courtyard']),riser_31=round(RISER,4),eaves_court=round(EAVES_COURT,3),
 court_row=dict(sill=SILL,h=HWIN,w=1.2),win_out=WIN_OUT,win_gyll_court=WIN_GYLL_COURT,
 tower_window=dict(key='N',dir=N,w=1.4),
 stair=dict(a_door=round(A_DOOR,4),a_top=round(A_TOP,4),a_mid=round(A_MID,4),a_end=A_END,a_hall=round(A_HALL,4),tread=T,risers=NR,riser=round(R2,5),
  lane_c=LANE_C,spine=SPINE,lane_k0=LANE_K0,b_land=B_LAND,z_ceil=Z_CEIL,W1=W1,E=E,IN=IN,
  kure_face=[list(ka0),list(ka1)],skin=.36),
 checks=dict(vault_top=round(vault_top,3),flight2_width=round(w_k,3),passage_rise=round(ZC-Z0,3)))
(R/'source/block126.json').write_text(json.dumps(out,indent=1))
print('BLOCK126_PREPARE_OK courtyard z',ZC,'(was',zh(HL['courtyard']),') riser31',round(RISER,4),'stair riser',round(R2,4),
 'door a',round(A_DOOR,2),'mid',round(A_MID,2),'top',round(A_TOP,2),'flight2 width',round(w_k,2),'vault top',round(vault_top,2),'courtyard eaves',round(EAVES_COURT,2))
