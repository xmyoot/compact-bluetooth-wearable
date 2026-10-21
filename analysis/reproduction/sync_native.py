from pathlib import Path
import sys,json,xml.etree.ElementTree as E
sys.path.insert(0,str(Path('work/pythonlibs').resolve()))
import sexpdata as s,pcbnew as p
r=Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable');h=r/'hardware';n='Compact-Bluetooth-Wearable';b=p.LoadBoard(str(h/(n+'.kicad_pcb')))
d=s.loads((h/(n+'.kicad_sch')).read_text());props={}
for a in d:
 if isinstance(a,list) and a and str(a[0])=='symbol':
  pp={v[1]:v[2] for v in a if isinstance(v,list) and v and str(v[0])=='property'}
  props[pp['Reference']]=pp
expected={}
for net in E.parse(r/'analysis/schematic.xml').findall('.//nets/net'):
 for a in net.findall('node'):expected[(a.get('ref'),a.get('pin'))]=net.get('name')
netmap={a.GetNetname():a for a in b.GetNetsByNetcode().values()}
for f in b.GetFootprints():
 for k,val in props[f.GetReference()].items():
  if k in ['Reference','Value','Footprint']:continue
  f.SetField(k,val);f.GetField(k).SetVisible(False)
 for a in f.Pads():
  exp=expected.get((f.GetReference(),a.GetNumber()))
  if exp and exp.startswith('unconnected-'):
   if exp not in netmap:netmap[exp]=p.NETINFO_ITEM(b,exp);b.Add(netmap[exp])
   a.SetNet(netmap[exp])
p.SaveBoard(str(h/(n+'.kicad_pcb')),b)
m=json.loads((r/'analysis/design-manifest.json').read_text());fps={f.GetReference():f for f in b.GetFootprints()}
for a in m:
 f=fps[a['ref']];a['xy']=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)];a['fp']=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())
 if a['ref']=='J1':a['nets']['SH']=a['nets'].pop('S1',a['nets'].get('SH','GND'))
(r/'analysis/design-manifest.json').write_text(json.dumps(m,indent=2));print('Synced properties, no-connect nets and manifest')
