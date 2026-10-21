import sys,pathlib,math
sys.path.insert(0,str(pathlib.Path('work/pythonlibs').resolve()))
from shapely.geometry import Point,LineString,Polygon,box
from shapely.strtree import STRtree
import pcbnew as p
r=pathlib.Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable\hardware');n='Compact-Bluetooth-Wearable';b=p.LoadBoard(str(r/(n+'_ground-joined.kicad_pcb')))
target={'I2C_SDA','I2C_SCL'};held=list(b.GetTracks());removed=[]
for t in held:
 if t.GetNetname() in target:b.Remove(t);removed.append(t)
 elif not isinstance(t,p.PCB_VIA) and t.GetWidth()<p.FromMM(.15):t.SetWidth(p.FromMM(.15))
def xy(a):return p.ToMM(a.x),p.ToMM(a.y)
def v(a):return p.VECTOR2I(*[p.FromMM(z) for z in a])
for f in b.GetFootprints():
 if f.GetReference()=='TP6':f.SetPosition(v((111,112)))
pads=[a for f in b.GetFootprints() for a in f.Pads()];geoms=[];meta=[]
for a in pads:
 l=p.F_Cu if a.IsOnLayer(p.F_Cu) else p.B_Cu;poly=a.GetEffectivePolygon(l);c=poly.COutline(0);g=Polygon([xy(c.CPoint(i)) for i in range(c.PointCount())]);geoms.append(g);meta.append((a,'pad',a.GetNetname(),l))
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);kind='via';l=-1
 else:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);kind='track';l=t.GetLayer()
 geoms.append(g);meta.append((t,kind,t.GetNetname(),l))
tree=STRtree(geoms);new=[];gone=set();fails=[];count=0
for a in pads:
 net=a.GetNetname()
 if net not in target:continue
 x,y=xy(a.GetPosition());l=p.F_Cu if a.IsOnLayer(p.F_Cu) else p.B_Cu
 cs=sorted([(x+i*.1,y+j*.1) for i in range(-35,36) for j in range(-35,36) if i or j],key=lambda q:(q[0]-x)**2+(q[1]-y)**2)
 for q in cs:
  cx,cy=q
  if cy<85.5 or cy>117.3 or (cx-100)**2+(cy-100)**2>19.3**2:continue
  cg=Point(q).buffer(.3);sg=LineString([(x,y),q]).buffer(.075);cb=cg.buffer(.16);sb=sg.buffer(.16)
  vi=tree.query(cb,predicate='intersects')
  if any(meta[i][1]=='pad' or (meta[i][2]!=net and not(meta[i][1]=='track' and meta[i][2]=='GND' and meta[i][3]==p.In1_Cu)) for i in vi):continue
  valid_path=None
  for path in [[(x,y),q],[(x,y),(x,cy),q],[(x,y),(cx,y),q]]:
   sg=LineString(path).buffer(.075);sb=sg.buffer(.16);si=tree.query(sb,predicate='intersects')
   if any(meta[i][2]!=net and meta[i][3] in [l,-1] for i in si):continue
   if any(nn!=net and (cb.intersects(gg) or (ll in [l,-1] and sb.intersects(gg))) for gg,nn,ll in new):continue
   valid_path=path;break
  if valid_path is None:continue
  if any(nn!=net and (cb.intersects(gg) or (ll in [l,-1] and sb.intersects(gg))) for gg,nn,ll in new):continue
  for i in set(vi)|set(si):
   obj,kind,nn,ll=meta[i]
   if net!='GND' and i not in gone and kind!='pad' and nn=='GND' and (cb.intersects(geoms[i]) or (ll in [l,-1] and sb.intersects(geoms[i]))):b.Remove(obj);removed.append(obj);gone.add(i)
  for aa,bb in zip(valid_path,valid_path[1:]):
   if aa==bb:continue
   tr=p.PCB_TRACK(b);tr.SetStart(v(aa));tr.SetEnd(v(bb));tr.SetLayer(l);tr.SetWidth(p.FromMM(.15));tr.SetNetCode(a.GetNetCode());b.Add(tr)
  via=p.PCB_VIA(b);via.SetPosition(v(q));via.SetWidth(p.FromMM(.6));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNetCode(a.GetNetCode());b.Add(via)
  new.extend([(cg,net,-1),(sg,net,l)]);count+=1;print(a.GetParentFootprint().GetReference(),a.GetNumber(),q,flush=True);break
 else:fails.append(a.GetParentFootprint().GetReference()+'.'+a.GetNumber())
p.SaveBoard(str(r/(n+'_escapes.kicad_pcb')),b);(r/(n+'_escapes.kicad_pro')).write_text((r/(n+'.kicad_pro')).read_text());print('ESCAPES',count,'FAILS',fails,'GND items removed',len(gone))









