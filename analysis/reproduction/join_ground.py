import sys,pathlib,math,heapq
sys.path.insert(0,str(pathlib.Path('work/pythonlibs').resolve()))
import numpy as np
import shapely as sh
from shapely.geometry import Point,LineString,Polygon
import pcbnew as p
r=pathlib.Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable\hardware');n='Compact-Bluetooth-Wearable';b=p.LoadBoard(str(r/(n+'_clean.kicad_pcb')));gnd=b.FindNet('GND').GetNetCode();step=.05;ox=80;oy=85.4;nx=801;ny=650
pads=[a for f in b.GetFootprints() for a in f.Pads()]
def xy(q):return p.ToMM(q.x),p.ToMM(q.y)
def v(q):return p.VECTOR2I(*[p.FromMM(z) for z in q])
def raster(layer):
 gs=[]
 for a in pads:
  if a.GetNetCode()==gnd or not a.IsOnLayer(layer):continue
  pol=a.GetEffectivePolygon(layer)
  if not pol.OutlineCount():continue
  c=pol.COutline(0);gs.append(Polygon([xy(c.CPoint(i)) for i in range(c.PointCount())]))
 for t in b.GetTracks():
  if t.GetNetCode()==gnd:continue
  if isinstance(t,p.PCB_VIA):gs.append(Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2))
  elif t.GetLayer()==layer:gs.append(LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2))
 obs=sh.union_all(gs).buffer(.227)
 xx,yy=np.meshgrid(ox+np.arange(nx)*step,oy+np.arange(ny)*step)
 return sh.intersects_xy(obs,xx,yy)|((xx-100)**2+(yy-100)**2>19.5**2),obs
cache={}
def route(start,goals,layer):
 if layer not in cache:cache[layer]=raster(layer)
 blocked,obs=cache[layer]
 def node(q):return round((q[0]-ox)/step),round((q[1]-oy)/step)
 def point(q):return (ox+q[0]*step,oy+q[1]*step)
 st=node(start);gn=[node(q) for q in goals];endset=set(gn)
 def h(q):return min(math.hypot(q[0]-z[0],q[1]-z[1]) for z in gn)
 heap=[(h(st),0,st)];cost={st:0};came={};it=0;end=None
 while heap and it<250000:
  _,g,q=heapq.heappop(heap)
  if g!=cost.get(q):continue
  it+=1
  if q in endset:end=q;break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
   z=(q[0]+dx,q[1]+dy)
   if not(0<=z[0]<nx and 0<=z[1]<ny) or blocked[z[1],z[0]]:continue
   if dx and dy and (blocked[q[1],z[0]] or blocked[z[1],q[0]]):continue
   ng=g+math.hypot(dx,dy)
   if ng<cost.get(z,1e20):cost[z]=ng;came[z]=q;heapq.heappush(heap,(ng+h(z),ng,z))
 if end is None:print('NO ROUTE',start,layer,it,flush=True);return False
 path=[end]
 while path[-1]!=st:path.append(came[path[-1]])
 coords=[start]+[point(q) for q in reversed(path)]+[goals[gn.index(end)]]
 # Collapse collinear grid runs.
 clean=[]
 for q in coords:
  if clean and math.dist(clean[-1],q)<1e-6:continue
  if len(clean)>=2:
   aa,bb=clean[-2:]
   if abs((bb[0]-aa[0])*(q[1]-bb[1])-(bb[1]-aa[1])*(q[0]-bb[0]))<1e-8:clean[-1]=q;continue
  clean.append(q)
 for aa,bb in zip(clean,clean[1:]):
  if sh.intersects(LineString([aa,bb]).buffer(.075),obs.buffer(-.077)):raise RuntimeError('Exact collision in proposed ground route')
  t=p.PCB_TRACK(b);t.SetStart(v(aa));t.SetEnd(v(bb));t.SetWidth(p.FromMM(.15));t.SetLayer(layer);t.SetNetCode(gnd);b.Add(t)
 print('GND route',start,'to',goals[gn.index(end)],'layer',layer,'segments',len(clean)-1,flush=True);return True
route((109.6,98.6),[(110,102.8)],p.In1_Cu)
vs=[xy(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetCode()==gnd and 106<xy(t.GetPosition())[0]<115 and 95<xy(t.GetPosition())[1]<106]

# Give the isolated left ground pad its own drop without encircling the SCL pad.
via_obstacles=[]
for a in pads:
 layer=p.F_Cu if a.IsOnLayer(p.F_Cu) else p.B_Cu;ps=a.GetEffectivePolygon(layer)
 if ps.OutlineCount():
  c=ps.COutline(0);via_obstacles.append(Polygon([xy(c.CPoint(i)) for i in range(c.PointCount())]))
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):via_obstacles.append(Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2))
 elif t.GetNetCode()!=gnd:via_obstacles.append(LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2))
vu=sh.union_all(via_obstacles).buffer(.462)
for a in pads:
 if a.GetParentFootprint().GetReference()!='U4' or a.GetNumber() not in ['5','12','13']:continue
 if a.GetNumber()!='5':route(xy(a.GetPosition()),vs,p.F_Cu);continue
 candidates=sorted([(106+i*.1,99+j*.1) for i in range(35) for j in range(20)],key=lambda q:math.dist(q,xy(a.GetPosition())))
 for q in candidates:
  if vu.intersects(Point(q)) or math.dist(q,(107.975,99.5))<.78:continue
  if not route(xy(a.GetPosition()),[q],p.F_Cu):continue
  vv=p.PCB_VIA(b);vv.SetPosition(v(q));vv.SetWidth(p.FromMM(.6));vv.SetDrill(p.FromMM(.3));vv.SetLayerPair(p.F_Cu,p.B_Cu);vv.SetViaType(p.VIATYPE_THROUGH);vv.SetNetCode(gnd);b.Add(vv)
  route(q,[(110,102.8)],p.In1_Cu);print('Added isolated-pad GND drop',q,flush=True);break
 else:print('Could not place isolated-pad drop')
p.SaveBoard(str(r/(n+'_ground-joined.kicad_pcb')),b);(r/(n+'_ground-joined.kicad_pro')).write_text((r/(n+'.kicad_pro')).read_text())

