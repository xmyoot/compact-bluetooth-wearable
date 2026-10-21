# Rev A design review — 2026-10-20

## Verdict and blockers

**Reviewable routed KiCad 10 engineering prototype. NOT manufacturing-ready.** ERC reports zero violations. Independent KiCad DRC with zone refill reports zero errors and zero unconnected items, with **17 warnings** (10 dangling tracks and 7 vias connected on only one layer). Schematic parity reports zero issues. The raw netlist-to-PCB audit checked 222 physical pads with zero mismatches, including the USB shield and explicit no-connect pins.

| Release blocker | Required action | Evidence / confidence |
|---|---|---|
| Remaining DRC warnings | Review and trim redundant stubs/unused layer transitions while preserving same-layer copper junctions. Re-run refill, DRC and parity. | KiCad `analysis/drc.json`; raw-file, high confidence |
| USB routing and return paths | Review complete connector–ESD–series resistor–MCU paths, coupling, stubs, plane crossings, transition stitching and skew. Validate against the final stack and USB full-speed operation. | EMC heuristics plus visible routing; high confidence that review/testing remain necessary |
| USB current / suspend and input capacitance | Define logic-off charging behavior, host suspend, enumeration policy and input inrush. Two 4.7 uF parts total 9.4 uF nominal, potentially 11.28 uF at +20% tolerance before other contributions; do not assert a 10 uF input-capacitance limit is met by nominal values. | Schematic and capacitor tolerance arithmetic; high confidence; compliance not established |
| Battery and NTC harness | Release a protected 1S pack MPN, permitted charge current, NTC curve/mounting and verified 3-pin harness polarity. No onboard cell-protection IC is fitted. | Schematic and architecture; high confidence |
| Thermal and skin contact | Validate charger/LDO heating, actual exposed-pad ground/thermal layout, sensor settling, enclosure contact and calibration. | Thermal analysis coverage gap and physical reasoning; no measured accuracy |
| Manufacturing / assembly | Choose exact fabricator stack, run DFM, decide fiducials/panel rails, assembly sides, stencil and component sourcing. Confirm every footprint against the selected package drawing. | No fabricator or assembly process released |
| Incomplete STEP assembly | U2's exact VQFN STEP model is missing from the installed library. The exported STEP omits the charger body. Obtain and inspect an exact package model before using the assembly for mechanical sign-off. | CLI STEP export log; high confidence |
| Firmware and physical tests | Implement SWD bring-up, USB bootloader/CDC, USB current controls, sensor drivers and power modes. Execute the bring-up procedure on assembled hardware. | No firmware build or prototype measurements yet |

## Overview and component summary

Native KiCad **10.0.7** project; one A2 schematic; nominal 40 mm diameter circle truncated at the USB edge (approximately 40 x 38 mm outline), four layers, nominal 1.0 mm thickness. Fifty physical footprints: 44 purchase/assembly parts and six unpopulated test pads. The sourcing BOM has 26 grouped lines with MPN/manufacturer fields, but no supplier stock, price or distributor SKU approval. There are 31 functional nets; singleton no-connect nets are represented explicitly for schematic parity.

- U1: Raytac MDBT50Q-1MV2 / nRF52840, BLE + USB full speed.
- U2: BQ24074RGTR, nominal 100 mA single-cell power-path charging.
- U3: TPS7A2030PDBVR, switched-enable 3.0 V logic rail.
- U4: LIS3DHTR accelerometer; I2C 0x18. R19 is a 0 ohm SA0 strap, overriding the sensor's internal pull-up.
- U5: TMP117AIDRVR, underside skin-facing temperature sensor, I2C 0x48; unpasted, floating exposed pad.
- USB-C: charging and firmware data, ESD protection, 27 ohm series resistors and independent CC pull-downs. SWD is the initial-flash and hardware-debug recovery interface.

## Power tree and estimates

USB 5 V -> BQ24074 -> VSYS -> TPS7A2030 -> 3.0 V logic. The protected Li-Po connects to the power-path charger, with a separate cell NTC. The slide switch disables the logic LDO, leaving charger and divider paths connected.

The 1 Mohm / 1 Mohm divider has a 0.5 ratio, about 2.1 uA at 4.2 V, and a 50 ms RC time constant with 100 nF. A planning 200 mAh cell with 80% usable capacity at assumed 0.5–2 mA average implies 80–320 hours; this is sensitivity arithmetic, not measured runtime. The battery is not selected.

An illustrative charger loss of (5−3) V x 0.1 A is about 0.20 W, plus system-path dissipation. BQ24074's datasheet thermal table gives 44.5 C/W on its specified test board, corresponding to roughly 9 C rise for that simplified load. This is not the thermal resistance of this small enclosed PCB. At a 30 mA logic load and 4.4 V VSYS, LDO dissipation is about 42 mW. Both can bias a nearby skin measurement; verify in the actual assembly.

## Layout and raw-file verification basis

- Geometry audit: 868 track segments, 140 through vias; minimum track 0.150 mm. Via dimensions [(0.6, 0.3)] mm (diameter, drill). Board constraints remain 0.15 mm track/clearance, 0.60/0.30 mm vias, 0.25 mm copper-to-edge. No microvias/blind vias are used.
- F.Cu components/signals, In1.Cu main GND reference with local GND bridges, In2.Cu GND fill plus signal escapes, B.Cu signals/skin sensor/test pads. Exact dielectric/copper stack and impedance are pending.
- Decoupling was reprioritized before switches, headers and general passives. Approximate straight supply-pad distances: U1 100 nF 2.6 mm and VBUS 2.5 mm; LDO output about 2.1 mm; charger input about 2.1 mm; TMP117 about 2.6 mm. These are geometric checks, not measured loop impedance or a complete PDN assessment.
- Raytac antenna is at the north edge. An explicit no-track/no-via/no-pour rule area covers all four copper layers through y=85.05 mm, 3.8 mm inward from the module's north body edge at y=81.25 mm, spanning the board width. See Raytac approval sheet section 2.3, printed page 11. Battery/enclosure metal and body loading require physical RF testing.
- TMP117's pad 7 has no paste and no net. TI's TMP117 data sheet recommends leaving its thermal pad unsoldered for rigid-board accuracy; skin contact still requires an insulating, characterized mechanical interface.
- USB shield uses the standard footprint pad name SH and is grounded in both schematic and PCB. Native component fields, explicit no-connect nets and BOM flags were synchronized. Raw `pad-net-crosscheck.csv` is the audit evidence.
- No claim is made that a library's package geometry or every pin's electrical behavior is independently qualified merely because parity and ERC pass. The listed release drawing checks remain necessary.

## Analyses actually run

| Check | Result / scope |
|---|---|
| Native KiCad ERC | 0 violations |
| Native DRC + zone refill | 0 errors, 17 warnings, 0 opens |
| Native schematic parity | 0 issues |
| Raw XML netlist vs PCB pads | 222 physical pads, 0 mismatches; no-connect names normalized only for reporting |
| `analyze_schematic.py` | Final schematic processed |
| `analyze_pcb.py --full` | Final PCB processed, including individual routing coordinates |
| `cross_analysis.py` | Final schematic/PCB cross-domain analysis run |
| `analyze_emc.py` | 48 heuristic findings across 5 evaluated categories; untriaged risk score 40/100 is not a compliance result |
| `analyze_thermal.py` | Invoked at 40 C ambient; **skipped quantification** because no complete per-MPN extraction/power cache was available; zero findings is not a pass |
| `analyze_gerbers.py` | Preview Gerbers/drill processed; 0 errors, 3 heuristic warnings |
| Lifecycle audit | Attempted for 24 MPNs; all statuses unknown. No stock/lifecycle assurance |
| SPICE | No ngspice/LTspice/Xyce command was available; no simulation run |

Manufacturer PDFs for the module and TI ICs are cached in `datasheets/`; ST LIS3DH/USBLC6 primary documentation and C&K's switch drawing were also consulted online. Structured extraction coverage is incomplete. Electrical findings outside those manual checks are consistency-only and must not be presented as a fully verified pin-level or datasheet-qualified design.

Primary references: [Raytac module approval sheet](https://www.raytac.com/download/index.php?index_id=43), [BQ24074](https://www.ti.com/lit/ds/symlink/bq24074.pdf), [TPS7A20](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), [TMP117](https://www.ti.com/lit/ds/symlink/tmp117.pdf), [LIS3DH](https://www.st.com/resource/en/datasheet/CD00274221.pdf), [USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), [PCM12 switch](https://www.ckswitches.com/media/1424/pcm.pdf).

## EMC, false positives and reviewer overrides

- Thermal rule-area KO-001 flags against parts/vias are heuristic false positives where the rule prohibits **zone fills only** and explicitly permits tracks, pads, vias and footprints. Native KiCad DRC is the authority for this rule. Antenna restrictions remain separate and stricter.
- The USB connector's courtyard/body extends beyond the flat board edge intentionally. This does not waive copper/slot clearances, which native DRC checks. Enclosure fit and connector retention remain open.
- Cross-analyzer descriptions of +3V0 and VBUS as split “planes” overstate the topology: those rails are routed as tracks, without power-plane zones. Ground fill continuity and return paths still need review; do not dismiss all plane-gap warnings on that basis.
- Generic 25 ps USB skew thresholds do not establish failure of the nRF52840's 12 Mbps interface. The routed USB topology, stubs, reference changes and ESD return inductance still require a design review and bench validation. Automatic length sums over branched nets are not a substitute for endpoint path lengths.
- Fiducials are absent on the individual PCB. Arrange panel fiducials with the assembler or add board fiducials where suitable. Do not claim assembly readiness.
- Gerber extent warnings arise from copper keepouts/layer coverage differing from the outline. Sparse B.Paste is expected because only a few bottom-side SMD pads need paste; test pads and TMP117 EP do not. Gerber viewer/DFM sign-off is still pending.
- EMC transition stitching and reference-gap findings are retained as release risks, not silently suppressed. No emissions, ESD or RF laboratory testing has occurred.

## Previous-run delta

The initial autorouter result that reduced fabrication features is rejected and archived. The inherited strict pass still had 26 KiCad unconnected items after refill and was also rejected. Placement was corrected for decoupling and the antenna rule area, then routing was rebuilt with fixed limits and manual escapes/ground connections. Final independent DRC now reports zero opens and zero copper errors. Seventeen cleanup warnings and the engineering blockers above remain.

## Deliverables and review limits

Editable native project/schematic/PCB and TMP117 local footprint are canonical under `hardware/`. Preview Gerbers, drills, placement CSV, top/bottom assembly PDFs and STEP are under `manufacturing/engineering-preview-NOT-FOR-FAB/`. The STEP omits U2's missing body model. No production order, public portfolio upload, fabrication release or physical testing was performed. Firmware is a bring-up plan only.

See `architecture.md`, `bring-up.md` and the draft portfolio case study for the next engineering gates. Full component drawing review, supplier confirmation, simulator-backed checks where appropriate, fabricator DFM, exact mechanical assembly and measured prototype characterization are unfinished.
