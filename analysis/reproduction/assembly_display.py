import pcbnew as p
from pathlib import Path
r=Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable');b=p.LoadBoard(str(r/'hardware/Compact-Bluetooth-Wearable.kicad_pcb'));held=[]
for f in b.GetFootprints():
 gs=list(f.GraphicalItems());held.extend(gs)
 for g in gs:
  if isinstance(g,p.PCB_TEXT) and ('REFERENCE' in g.GetText() or g.GetText()=='%R'):f.Remove(g)
 ref=f.Reference();ref.SetVisible(True);ref.SetPosition(f.GetPosition());ref.SetLayer(p.B_Fab if f.IsFlipped() else p.F_Fab)
 size=.6 if f.GetReference().startswith(('R','C')) else .85
 ref.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));ref.SetTextThickness(p.FromMM(.09));ref.SetTextAngle(p.EDA_ANGLE(f.GetOrientationDegrees()%180 if f.GetReference().startswith(('R','C')) else 0,p.DEGREES_T))
p.SaveBoard(str(Path('work/assembly-display.kicad_pcb').resolve()),b)
