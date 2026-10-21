from pathlib import Path
import xml.etree.ElementTree as E,json,csv
import pcbnew as p
r=Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable');b=p.LoadBoard(str(r/'hardware/Compact-Bluetooth-Wearable.kicad_pcb'))
x=E.parse(r/'analysis/schematic.xml');expected={}
for net in x.findall('.//nets/net'):
 for a in net.findall('node'):expected[(a.get('ref'),a.get('pin'))]=net.get('name').lstrip('/')
errors=[];rows=[];physical={}
for f in b.GetFootprints():
 for a in f.Pads():
  if not a.GetNumber():continue
  key=(f.GetReference(),a.GetNumber());actual=a.GetNetname().lstrip('/');exp=expected.get(key,'')
  # KiCad generates individual unconnected net names for explicit no-connect pins.
  if exp.startswith('unconnected-'):exp='';actual='' if actual.startswith('unconnected-') else actual
  rows.append([*key,exp,actual, 'match' if exp==actual else 'mismatch'])
  physical[key]=actual
  if exp!=actual:errors.append([*key,exp,actual])
for key,net in expected.items():
 if not key[0].startswith('#') and not net.startswith('unconnected-') and key not in physical:errors.append([*key,net,'physical pad missing'])
with (r/'analysis/pad-net-crosscheck.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Pad','Schematic net','PCB net','Result']);w.writerows(rows)
(r/'analysis/pad-net-crosscheck.json').write_text(json.dumps({'physical_pads_checked':len(rows),'mismatches':errors},indent=2));print('PAD NET CHECK',len(rows),'mismatches',errors)

