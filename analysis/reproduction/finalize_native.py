from pathlib import Path
import pcbnew as p,json
r=Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable');h=r/'hardware';n='Compact-Bluetooth-Wearable';b=p.LoadBoard(str(h/(n+'_route-v15.kicad_pcb')))
held=list(b.GetTracks())
for t in held:
 if isinstance(t,p.PCB_VIA) and abs(p.ToMM(t.GetPosition().x)-91.775)<.001 and abs(p.ToMM(t.GetPosition().y)-106.5)<.001:
  a=t.GetPosition();net=t.GetNetCode();b.Remove(t)
  # Preserve the copper junction on its only connected layer, without an unused drill.
  q=p.PCB_TRACK(b);q.SetStart(a);q.SetEnd(p.VECTOR2I(a.x+1000,a.y));q.SetWidth(p.FromMM(.598));q.SetLayer(p.F_Cu);q.SetNetCode(net);b.Add(q)
for f in b.GetFootprints():
 if f.GetReference()=='J1':
  f.SetFPID(p.LIB_ID('Connector_USB','USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal'))
  for a in f.Pads():
   if a.GetNumber()=='S1':a.SetNumber('SH')
 if f.GetReference()=='R19':f.SetValue('0')
 if f.GetReference().startswith('TP'):f.SetAttributes(f.GetAttributes()|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_EXCLUDE_FROM_BOM)
for net in b.GetNetsByNetcode().values():
 if net.GetNetname() and not net.GetNetname().startswith('/'):net.SetNetname('/'+net.GetNetname())
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA) and t.GetWidth()<p.FromMM(.15):t.SetWidth(p.FromMM(.15))
b.GetTitleBlock().SetTitle('Compact Bluetooth Wearable - engineering prototype');b.GetTitleBlock().SetRevision('A-DRAFT');b.GetTitleBlock().SetDate('2026-10-20')
p.SaveBoard(str(h/(n+'.kicad_pcb')),b)
m=json.loads((r/'analysis/design-manifest.json').read_text())
fps={f.GetReference():f for f in b.GetFootprints()}
for a in m:
 f=fps[a['ref']];a['xy']=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)];a['fp']=f.GetFPID().GetLibNickname()+':'+f.GetFPID().GetLibItemName()
 if a['ref']=='J1':a['nets']['SH']=a['nets'].pop('S1',a['nets'].get('SH','GND'))
(r/'analysis/design-manifest.json').write_text(json.dumps(m,indent=2))
print('Promoted candidate to canonical native PCB')
