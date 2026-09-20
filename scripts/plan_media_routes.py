"""Deterministic street and cathedral camera paths in the project metre coordinates."""
import json,math,bisect
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def lerp(a,b,t):return [x+(y-x)*t for x,y in zip(a,b)]
def dist(a,b):return math.dist(a,b)
def rounded(points,radius=2.3):
 out=[points[0]]
 for i in range(1,len(points)-1):
  a,b,c=points[i-1:i+2];d=min(radius,dist(a,b)*.2,dist(b,c)*.2);p=lerp(b,a,d/dist(a,b));q=lerp(b,c,d/dist(b,c));out.append(p)
  for j in range(1,17):
   t=j/16;out.append(lerp(lerp(p,b,t),lerp(b,q,t),t))
 out.append(points[-1]);return out
def sample_line(points):
 acc=[0]
 for a,b in zip(points,points[1:]):acc.append(acc[-1]+dist(a,b))
 def at(d):
  d=max(0,min(acc[-1],d));i=min(len(points)-2,bisect.bisect_right(acc,d)-1);return lerp(points[i],points[i+1],(d-acc[i])/(acc[i+1]-acc[i]))
 return at,acc[-1]
points=[[-19,-2,9],[-33.5,-2.64,6],[-290.09,-1.045,6],[-289.27,69.61,6],[-186,69.84,6],[-185.422,141.042,6],[-31.59,140.295,8],[-32.5,45,10],[-28,13,14],[-6,0,18]]
at,total=sample_line(rounded(points));duration=84;street=[]
for i in range(duration*24):
 t=i/(duration*24-1);d=total*t;p=at(d);target=at(min(total,d+11));target[2]=p[2]+1
 if t>.92:
  a=(t-.92)/.08;a=a*a*(3-2*a);target=lerp(target,[10,44,12],a)
 street.append({'location':p,'target':target})
anchors=[(0,[-10,44.4,2.8],[32,44.4,8]),(8,[5,44.4,3],[32,44.4,8]),(16,[21.8,44.4,3.5],[32,44.4,8]),(23,[19,44.4,4],[18.2,50.7,6.4]),(30,[10,44.4,4.3],[18.2,50.7,6.4]),(38,[-4,44.4,4],[-12,44.4,10]),(44,[0,44.4,5.5],[5,50,17])]
def spline(t,index):
 i=min(len(anchors)-2,bisect.bisect_right([a[0] for a in anchors],t)-1);a,b=anchors[i:i+2];prev=anchors[max(i-1,0)];nex=anchors[min(i+2,len(anchors)-1)];f=(t-a[0])/(b[0]-a[0]);h=b[0]-a[0];out=[]
 for axis in range(3):
  v0,v1=a[index][axis],b[index][axis];m0=(b[index][axis]-prev[index][axis])/(b[0]-prev[0]);m1=(nex[index][axis]-a[index][axis])/(nex[0]-a[0]);out.append((2*f**3-3*f*f+1)*v0+(f**3-2*f*f+f)*h*m0+(-2*f**3+3*f*f)*v1+(f**3-f*f)*h*m1)
 return out
church=[{'location':spline(44*i/(44*24-1),1),'target':spline(44*i/(44*24-1),2)} for i in range(44*24)]
(R/'media/routes.json').write_text(json.dumps({'fps':24,'street':{'duration':84,'fov':84,'frames':street},'church':{'duration':44,'fov':82,'frames':church}},indent=2));print('Street',len(street),'Church',len(church),'frames')
