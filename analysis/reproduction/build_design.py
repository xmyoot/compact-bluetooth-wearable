import sys,pathlib,re,copy,uuid,json,math,csv
sys.path.insert(0,str(pathlib.Path(__file__).parent/'pythonlibs'))
import sexpdata as sx
import pcbnew as pcb
ROOT=pathlib.Path(r'C:\Users\hecto\Documents\KiCAD_Projects\Compact-Bluetooth-Wearable')
K=pathlib.Path(r'C:\Program Files\KiCad\10.0\share\kicad')
HW=ROOT/'hardware'; HW.mkdir(exist_ok=True)
NAME='Compact-Bluetooth-Wearable'
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'compact-wearable/revA/'+s))
def tag(v): return str(v[0]) if isinstance(v,list) and v else ''
def child(v,k): return next((a for a in v if tag(a)==k),None)
cache={}
def libpart(lib,name):
    key=lib+':'+name
    if key in cache: return copy.deepcopy(cache[key])
    text=(K/'symbols'/f'{lib}.kicad_sym').read_text(encoding='utf8')
    start=text.index('(symbol "'+name+'"')
    depth=0; quote=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': quote=False
        elif c=='"': quote=True
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if not depth: break
    part=sx.loads(text[start:i+1])
    ext=child(part,'extends')
    if ext:
        base=libpart(lib,ext[1])
        own={v[1] for v in part if tag(v)=='property'}
        part=[v for v in part if tag(v)!='extends']
        part += [v for v in base if tag(v)=='symbol' or (tag(v)=='property' and v[1] not in own)]
        for v in part:
            if tag(v)=='symbol': v[1]=v[1].replace(ext[1],name,1)
    cache[key]=copy.deepcopy(part)
    return part
parts=[]
def add(ref,lib,value,fp,nets,xy,sch,mpn='',mfr='',url='',angle=0,side='F',note=''):
    parts.append(dict(ref=ref,lib=lib,value=value,fp=fp,nets={str(k):v for k,v in nets.items()},xy=xy,sch=sch,mpn=mpn,mfr=mfr,url=url,angle=angle,side=side,note=note))
RFP='Resistor_SMD:R_0603_1608Metric'; CFP='Capacitor_SMD:C_0603_1608Metric'
def res(n,val,a,b,xy,sch,angle=0):
    mpns={'0':'RC0603JR-070RL','5.1k':'RC0603FR-075K1L','100k':'RC0603FR-07100KL','4.7k':'RC0603FR-074K7L','8.87k':'RC0603FR-078K87L','3.32k':'RC0603FR-073K32L','1M':'RC0603FR-071ML','27':'RC0603FR-0727RL','1k':'RC0603FR-071KL'}
    add('R'+str(n),'Device:R',val,RFP,{1:a,2:b},xy,sch,mpns[val],'Yageo',angle=angle)
def cap(n,val,a,b,xy,sch,angle=0):
    mpns={'100n':'GRM188R71C104KA01D','1u':'GRM188R61A105KA61D','4.7u':'GRM188R60J475KE19D','10u':'GRM188R60J106ME47D'}
    add('C'+str(n),'Device:C',val,CFP,{1:a,2:b},xy,sch,mpns[val],'Murata',angle=angle)
add('U1','RF_Module:MDBT50Q-1MV2','MDBT50Q-1MV2','RF_Module:Raytac_MDBT50Q',
    {1:'GND',2:'GND',15:'GND',33:'GND',55:'GND',28:'+3V0',30:'+3V0',32:'VBUS',34:'USB_N',35:'USB_P',
     51:'SWDIO',53:'SWCLK',40:'RESET_N',16:'I2C_SCL',19:'I2C_SDA',27:'ACC_INT',29:'TEMP_ALERT',
     36:'LED_STATUS',37:'USER_N',38:'CHG_EN1',39:'CHG_EN2',41:'CHARGE_N',42:'PGOOD_N',11:'BAT_SENSE'},
    (100,89),(95,85),'MDBT50Q-1MV2','Raytac','https://www.raytac.com/download/index.php?index_id=43')
add('U2','Battery_Management:BQ24074RGT','BQ24074RGTR','Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm',
    {1:'BAT_NTC',2:'VBAT',3:'VBAT',4:'GND',5:'CHG_EN2',6:'CHG_EN1',7:'PGOOD_N',8:'GND',9:'CHARGE_N',10:'VSYS',11:'VSYS',12:'ILIM',13:'VBUS',16:'ISET',17:'GND'},
    (91,109),(285,65),'BQ24074RGTR','Texas Instruments','https://www.ti.com/lit/ds/symlink/bq24074.pdf',
    note='TMR floating: default timer. ITERM floating: 10% termination. Battery requires external protection and 10k NTC.')
add('U3','Regulator_Linear:TPS7A20xxxDBV','TPS7A2030PDBVR','Package_TO_SOT_SMD:SOT-23-5',
    {1:'VSYS',2:'GND',3:'POWER_EN',5:'+3V0'},(91,101),(285,130),'TPS7A2030PDBVR','Texas Instruments','https://www.ti.com/lit/ds/symlink/tps7a20.pdf')
add('U4','Sensor_Motion:LIS3DH','LIS3DHTR','Package_LGA:LGA-16_3x3mm_P0.5mm_LayoutBorder3x5y',
    {1:'+3V0',4:'I2C_SCL',5:'GND',6:'I2C_SDA',7:'ACC_SA0',8:'+3V0',10:'GND',11:'ACC_INT',12:'GND',14:'+3V0',13:'GND',15:'GND',16:'GND'},
    (110,99),(465,60),'LIS3DHTR','STMicroelectronics','https://www.st.com/resource/en/datasheet/cd00274221.pdf')
add('U5','Sensor_Temperature:TMP117xxDRV','TMP117AIDRVR','Wearable:TMP117_NoPasteEP',
    {1:'I2C_SCL',2:'GND',3:'TEMP_ALERT',4:'GND',5:'+3V0',6:'I2C_SDA'},(114,104),(465,120),'TMP117AIDRVR','Texas Instruments','https://www.ti.com/lit/ds/symlink/tmp117.pdf',
    side='B',note='Exposed pad unsoldered: no paste aperture. Skin-facing package; enclosure thermal contact requires validation.')
add('J1','Connector:USB_C_Receptacle_USB2.0_16P','USB-C','Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal',
    {'A1':'GND','B12':'GND','A4':'VBUS','B9':'VBUS','A5':'CC1','B5':'CC2','A6':'USB_CONN_P','B6':'USB_CONN_P','A7':'USB_CONN_N','B7':'USB_CONN_N','A9':'VBUS','B4':'VBUS','A12':'GND','B1':'GND','SH':'GND'},
    (101,115.5),(80,210),'USB4105-GF-A','GCT','https://gct.co/files/drawings/usb4105.pdf',angle=0)
add('J2','Connector_Generic:Conn_01x03','BATTERY + / NTC / -','Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical',
    {1:'VBAT',2:'BAT_NTC',3:'GND'},(86,102),(280,192),'B3B-PH-K-S(LF)(SN)','JST',
    note='Use protected 1S 4.2V LiPo >=200mAh, 10k NTC at cell; verify mating harness polarity. Pack MPN not released.',angle=90)
add('J3','Connector_Generic:Conn_01x06','SWD RECOVERY','Connector_PinHeader_1.27mm:PinHeader_1x06_P1.27mm_Vertical',
    {1:'+3V0',2:'SWDIO',3:'SWCLK',4:'GND',5:'RESET_N',6:'GND'},(103,102),(90,300),
    '20021121-00006T4LF','Amphenol',angle=90,note='Optional populated header; debugger must sense target voltage, not power target.')
add('SW1','Switch:SW_SPDT','POWER','Button_Switch_SMD:SW_SPDT_PCM12',
    {1:'VSYS',2:'POWER_EN',3:'GND'},(87,93),(285,250),'PCM12SMTR','C&K',angle=90)
add('SW2','Switch:SW_Push','USER / DFU','Button_Switch_SMD:SW_SPST_TL3342',
    {1:'USER_N',2:'GND'},(111,111),(465,260),'TL3342F160QG','E-Switch')
add('SW3','Switch:SW_Push','RESET','Button_Switch_SMD:SW_SPST_TL3342',
    {1:'RESET_N',2:'GND'},(106,108),(465,300),'TL3342F160QG','E-Switch')
add('D1','Device:LED','STATUS GREEN','LED_SMD:LED_0603_1608Metric',
    {1:'LED_K',2:'+3V0'},(110,91),(465,220),'LTST-C190KGKT','Lite-On')
add('D2','Power_Protection:USBLC6-2SC6','USBLC6-2SC6','Package_TO_SOT_SMD:SOT-23-6',
    {1:'USB_CONN_P',3:'USB_CONN_N',4:'USB_CONN_N',6:'USB_CONN_P',2:'GND',5:'VBUS'},(100,111),(80,260),
    'USBLC6-2SC6','STMicroelectronics','https://www.st.com/resource/en/datasheet/usblc6-2.pdf')
res(1,'5.1k','CC1','GND',(95,115),(130,210))
res(2,'5.1k','CC2','GND',(107,115),(160,210))
res(3,'27','USB_CONN_P','USB_P',(100,100),(130,255),90)
res(4,'27','USB_CONN_N','USB_N',(100,98),(160,255),90)
res(5,'8.87k','ISET','GND',(88,111),(250,95))
res(6,'3.32k','ILIM','GND',(91,113),(280,95))
res(7,'100k','CHG_EN1','GND',(93,110),(310,95))
res(8,'100k','CHG_EN2','GND',(93,108),(340,95))
res(9,'100k','PGOOD_N','+3V0',(95,107),(310,192))
res(10,'100k','CHARGE_N','+3V0',(95,105),(340,192))
res(11,'4.7k','I2C_SCL','+3V0',(107,96),(430,165))
res(12,'4.7k','I2C_SDA','+3V0',(109,96),(460,165))
res(13,'100k','TEMP_ALERT','+3V0',(112,102),(490,165))
res(14,'100k','USER_N','+3V0',(114,109),(500,260))
res(15,'100k','RESET_N','+3V0',(106,105),(500,300))
res(16,'1k','LED_K','LED_STATUS',(110,93),(500,220))
res(17,'1M','VBAT','BAT_SENSE',(98,105),(130,300))
res(18,'1M','BAT_SENSE','GND',(98,107),(160,300))
res(19,'0','ACC_SA0','GND',(112,95),(520,165))
cap(1,'10u','+3V0','GND',(101,100.5),(50,150))
cap(2,'100n','+3V0','GND',(102,98.5),(80,150))
cap(3,'4.7u','VBUS','GND',(105,98),(110,150))
cap(4,'4.7u','VBUS','GND',(91,106),(250,155))
cap(5,'10u','VBAT','GND',(88,107),(280,155))
cap(6,'10u','VSYS','GND',(94,113),(310,155))
cap(7,'1u','VSYS','GND',(90,98.5),(250,220))
cap(8,'1u','+3V0','GND',(94,100),(280,220))
cap(9,'100n','+3V0','GND',(108,98),(430,190))
cap(10,'1u','+3V0','GND',(110,102),(460,190))
cap(11,'100n','+3V0','GND',(113,102),(490,190))
parts[-1]['side']='B'
cap(12,'100n','BAT_SENSE','GND',(98,109),(160,340))
for c in parts:
    if c['ref'] in ['C1','C2','C4']: c['angle']=180
for i,(net,xy) in enumerate([('GND',(89,116)),('VBUS',(94,117)),('VBAT',(84,107)),('VSYS',(85,110)),('+3V0',(90,96)),('ACC_INT',(111,112))],1):
    add('TP'+str(i),'Connector:TestPoint',net,'TestPoint:TestPoint_Pad_D1.0mm',{1:net},xy,(230+i*25,300),note='Unpopulated test pad',side='B')

def q(s): return json.dumps(s)
def effects(size=1.27,extra=''): return f'(effects (font (size {size} {size})) {extra})'
schid=uid('schematic')
symbols=[]; libsyms=[]; seen=set(); extras=[]
for part in parts:
    lib,name=part['lib'].split(':'); definition=libpart(lib,name)
    if part['lib'] not in seen:
        definition[1]=part['lib']
        libsyms.append(sx.dumps(definition)); seen.add(part['lib'])
    x,y=[round(v/1.27)*1.27 for v in part['sch']]; ref=part['ref']
    props={'Reference':ref,'Value':part['value'],'Footprint':part['fp'],'Datasheet':part['url'],'MPN':part['mpn'],'Manufacturer':part['mfr'],'BOM Comments':part['note']}
    props_str=[]
    for i,(key,val) in enumerate(props.items()):
        yy=y-5.08+i*2.54 if i<2 else y
        props_str.append(f'(property {q(key)} {q(val)} (at {x+5.08} {yy} 0) {effects(extra="" if i<2 else "(hide yes)")})')
    pinstr=[]; at_seen={}
    for sub in definition:
        if tag(sub)!='symbol': continue
        for pin in sub:
            if tag(pin)!='pin': continue
            num=str(child(pin,'number')[1]); at=child(pin,'at'); px=round(x+float(at[1]),4); py=round(y-float(at[2]),4)
            pinstr.append(f'(pin {q(num)} (uuid {q(uid(ref+"/pin/"+num))}))')
            net=part['nets'].get(num)
            if (px,py) in at_seen: continue
            at_seen[px,py]=net
            if net:
                a=float(at[3]); length=5.08
                dx=-math.cos(math.radians(a))*length; dy=math.sin(math.radians(a))*length
                ex,ey=round(px+dx,4),round(py+dy,4)
                extras.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {q(uid(ref+"/wire/"+num))}))')
                # labels face away from symbol; small labels on power pins avoid crowds
                la=0 if a in [0,180] else 90
                just='left' if a==180 else 'right'
                extras.append(f'(label {q(net)} (at {ex} {ey} {la}) {effects(1.0,"(justify "+just+" bottom)")} (uuid {q(uid(ref+"/label/"+num))}))')
            else:
                extras.append(f'(no_connect (at {px} {py}) (uuid {q(uid(ref+"/nc/"+num))}))')
    symbols.append(f'(symbol (lib_id {q(part["lib"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid(ref))}) {" ".join(props_str)} {" ".join(pinstr)} (instances (project {q(NAME)} (path {q("/"+schid)} (reference {q(ref)}) (unit 1)))))')
# power flags for externally driven VBUS/GND; component outputs drive other rails
for idx,net in enumerate(['VBUS','GND']):
    definition=libpart('power','PWR_FLAG')
    if idx==0:
        definition[1]='power:PWR_FLAG'; libsyms.append(sx.dumps(definition))
    x,y=[round(v/1.27)*1.27 for v in [250+idx*30,340]]; ref='#FLG0'+str(idx+1)
    symbols.append(f'(symbol (lib_id "power:PWR_FLAG") (at {x} {y} 0) (unit 1) (in_bom no) (on_board yes) (dnp no) (uuid {q(uid(ref))}) (property "Reference" {q(ref)} (at {x} {y} 0) {effects(extra="(hide yes)")}) (property "Value" "PWR_FLAG" (at {x} {y-4} 0) {effects()}) (instances (project {q(NAME)} (path {q("/"+schid)} (reference {q(ref)}) (unit 1)))))')
    extras.append(f'(label {q(net)} (at {x} {y} 0) {effects()} (uuid {q(uid(ref+"label"))}))')
for title,x,y in [('BLE + USB CONTROLLER',35,25),('USB-C / PROGRAMMING',35,175),('CHARGER / POWER PATH',235,25),('3V0 / BATTERY / POWER CONTROL',235,115),('MOTION + SKIN TEMPERATURE',405,25),('USER INTERFACE',405,210),('Rev A engineering prototype - not a fabrication release',35,375),('USB bootloader must be installed over SWD before first USB firmware update.',35,385),('Battery: protected 1S LiPo, >=200mAh, 10k NTC. Charge nominal 100mA; default USB input limit 100mA.',235,365)]:
    extras.append(f'(text {q(title)} (at {x} {y} 0) {effects(1.4,"(justify left)")} (uuid {q(uid(title))}))')
sch=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(schid)}) (paper "A2") (title_block (title "Compact Bluetooth Wearable") (date "2026-10-19") (rev "A-draft") (company "Independent engineering portfolio")) (lib_symbols {" ".join(libsyms)}) {" ".join(extras)} {" ".join(symbols)} (embedded_fonts no))'
(HW/(NAME+'.kicad_sch')).write_text(sch,encoding='utf8')
# Project-local sensor footprint removes EP paste; preserve land geometry and leave pad floating.
local=HW/'Wearable.pretty';local.mkdir(exist_ok=True)
fptxt=(K/'footprints/Package_SON.pretty/WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm.kicad_mod').read_text()
fpobj=sx.loads(fptxt); fpobj[1]='TMP117_NoPasteEP'
for p in fpobj:
    if tag(p)=='pad' and p[1]=='7':
        layers=child(p,'layers')
        if 'F.Paste' in layers: layers.remove('F.Paste')
(local/'TMP117_NoPasteEP.kicad_mod').write_text(sx.dumps(fpobj),encoding='utf8')
(HW/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Wearable")(type "KiCad")(uri "${KIPRJMOD}/Wearable.pretty")(options "")(descr "")))')
board=pcb.BOARD()
board.SetCopperLayerCount(4)
board.GetDesignSettings().SetBoardThickness(pcb.FromMM(1.0))
netnames=sorted({n for p in parts for n in p['nets'].values()})
nets={}
for n in netnames:
    net=pcb.NETINFO_ITEM(board,'/'+n);board.Add(net);nets[n]=net
for part in parts:
    lib,name=part['fp'].split(':')
    path=local if lib=='Wearable' else K/'footprints'/(lib+'.pretty')
    fp=pcb.FootprintLoad(str(path),name)
    if fp is None: raise RuntimeError(part['fp'])
    fp.SetReference(part['ref']);fp.SetValue(part['value']);fp.SetFPID(pcb.LIB_ID(lib,name))
    fp.SetPosition(pcb.VECTOR2I(*[pcb.FromMM(v) for v in part['xy']]))
    fp.SetOrientationDegrees(part['angle'])
    fp.SetPath(pcb.KIID_PATH('/'+schid+'/'+uid(part['ref'])))
    board.Add(fp)
    if part['side']=='B': fp.Flip(fp.GetPosition(),False)
    for pad in fp.Pads():
        if pad.GetNumber() in part['nets']: pad.SetNet(nets[part['nets'][pad.GetNumber()]])
    fp.Reference().SetTextSize(pcb.VECTOR2I(pcb.FromMM(.8),pcb.FromMM(.8)))
    fp.Reference().SetTextThickness(pcb.FromMM(.12))
    fp.Reference().SetLayer(pcb.B_Fab if part['side']=='B' else pcb.F_Fab)
    fp.Value().SetVisible(False)
# Legalize placement using actual courtyard envelopes, preserving RF module and USB anchors.
placed=[]
def bounds(fp):
    items=[g.GetBoundingBox() for g in fp.GraphicalItems() if g.GetLayer() in [pcb.F_CrtYd,pcb.B_CrtYd]]
    if not items: items=[p.GetBoundingBox() for p in fp.Pads()]
    return tuple(pcb.ToMM(v) for v in (min(b.GetLeft() for b in items),min(b.GetTop() for b in items),max(b.GetRight() for b in items),max(b.GetBottom() for b in items)))
fps={f.GetReference():f for f in board.GetFootprints()}
ordered=sorted(parts,key=lambda p:(0 if p['ref']=='U1' else 1 if p['ref']=='J1' else 2 if p['ref'].startswith('U') else 3 if p['ref'].startswith('C') else 4 if p['ref'].startswith(('J','SW')) else 5))
for p in ordered:
    f=fps[p['ref']];x,y=p['xy'];b=bounds(f);offset=(b[0]-x,b[1]-y,b[2]-x,b[3]-y)
    candidates=[(x,y)] if p['ref'] in ['U1','J1'] else sorted([(x+dx*.5,y+dy*.5) for dx in range(-40,41) for dy in range(-40,41)],key=lambda v:(v[0]-x)**2+(v[1]-y)**2)
    for cx,cy in candidates:
        box=(cx+offset[0],cy+offset[1],cx+offset[2],cy+offset[3])
        if p['ref'] not in ['U1','J1']:
            if box[1]<85.3 or box[3]>117.5:continue
            if any((xx-100)**2+(yy-100)**2>19.5**2 for xx in [box[0],box[2]] for yy in [box[1],box[3]]):continue
        if any(p['side']==side and not(box[2]+.25<bb[0] or box[0]-.25>bb[2] or box[3]+.25<bb[1] or box[1]-.25>bb[3]) for bb,side in placed):continue
        f.SetPosition(pcb.VECTOR2I(pcb.FromMM(cx),pcb.FromMM(cy)));p['xy']=(cx,cy);placed.append((box,p['side']));break
    else: raise RuntimeError('No legal placement for '+p['ref']+' '+str(offset)+' placed '+str(placed))
# circle truncated at USB edge y=118; radius 20 centred at 100,100
a=math.asin(18/20); points=[]
for i in range(129):
    t=math.pi-a+(math.pi+2*a)*i/128
    points.append((100+20*math.cos(t),100+20*math.sin(t)))
for p1,p2 in zip(points,points[1:]+points[:1]):
    e=pcb.PCB_SHAPE();e.SetShape(pcb.SHAPE_T_SEGMENT);e.SetStart(pcb.VECTOR2I(*[pcb.FromMM(v) for v in p1]));e.SetEnd(pcb.VECTOR2I(*[pcb.FromMM(v) for v in p2]));e.SetLayer(pcb.Edge_Cuts);e.SetWidth(pcb.FromMM(.05));board.Add(e)
# antenna keepout on ALL copper; module antenna faces north
keep=pcb.ZONE(board);keep.SetIsRuleArea(True)
ls=pcb.LSET()
for layer in [pcb.F_Cu,pcb.In1_Cu,pcb.In2_Cu,pcb.B_Cu]: ls.AddLayer(layer)
keep.SetLayerSet(ls);keep.SetDoNotAllowTracks(True);keep.SetDoNotAllowVias(True);keep.SetDoNotAllowZoneFills(True);keep.SetDoNotAllowPads(False);keep.SetDoNotAllowFootprints(False)
poly=keep.Outline();poly.NewOutline()
for x,y in [(79,78),(121,78),(121,85.05),(79,85.05)]: poly.Append(pcb.FromMM(x),pcb.FromMM(y))
board.Add(keep)
# continuous ground reference on inner layers; thermal island excluded on layer pours
for layer in [pcb.In1_Cu,pcb.In2_Cu]:
    z=pcb.ZONE(board);z.SetLayer(layer);z.SetNet(nets['GND']);z.SetLocalClearance(pcb.FromMM(.2));z.SetThermalReliefGap(pcb.FromMM(.25));z.SetThermalReliefSpokeWidth(pcb.FromMM(.25))
    z.SetPadConnection(pcb.ZONE_CONNECTION_FULL)
    o=z.Outline();o.NewOutline()
    for x,y in [(79,83),(121,83),(121,119),(79,119)]:o.Append(pcb.FromMM(x),pcb.FromMM(y))
    board.Add(z)
# no plane copper immediately beneath skin sensor to reduce board heat conduction
thermal=pcb.ZONE(board);thermal.SetIsRuleArea(True);thermal.SetLayerSet(ls);thermal.SetDoNotAllowZoneFills(True);thermal.SetDoNotAllowTracks(False);thermal.SetDoNotAllowVias(False);thermal.SetDoNotAllowPads(False);thermal.SetDoNotAllowFootprints(False)
o=thermal.Outline();o.NewOutline()
for x,y in [(112,100),(117,100),(117,107),(112,107)]:o.Append(pcb.FromMM(x),pcb.FromMM(y))
board.Add(thermal)
txt=pcb.PCB_TEXT(board);txt.SetText('CBW REV A');txt.SetPosition(pcb.VECTOR2I(pcb.FromMM(100),pcb.FromMM(110)));txt.SetTextSize(pcb.VECTOR2I(pcb.FromMM(.8),pcb.FromMM(.8)));txt.SetTextThickness(pcb.FromMM(.14));txt.SetLayer(pcb.B_SilkS);txt.SetMirrored(True);board.Add(txt)
pcb.SaveBoard(str(HW/(NAME+'.kicad_pcb')),board)
project={'meta':{'filename':NAME+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.15,'min_track_width':.15,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_hole_clearance':.15,'min_copper_edge_clearance':.25},'rule_severities':{},'defaults':{'zones':{'min_clearance':.2}}}},'net_settings':{'classes':[{'name':'Default','clearance':.15,'track_width':.2,'via_diameter':.6,'via_drill':.3,'diff_pair_width':.2,'diff_pair_gap':.15,'diff_pair_via_gap':.25}],'meta':{'version':3}},'text_variables':{'STATUS':'ENGINEERING DRAFT'}}
(HW/(NAME+'.kicad_pro')).write_text(json.dumps(project,indent=2))
(ROOT/'analysis/design-manifest.json').write_text(json.dumps(parts,indent=2))
print('Created',len(parts),'components;',len(nets),'nets')






