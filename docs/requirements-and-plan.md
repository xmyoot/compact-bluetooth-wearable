# Requirements and execution status

Updated 2026-10-20. Current detailed design decisions are in `architecture.md`; the original planning draft is preserved as `planning-history.md`.

| Item | Current decision / status |
|---|---|
| CAD | Native KiCad 10 project, schematic, PCB and local footprints |
| Product | Wrist-worn engineering prototype, skin-temperature trends |
| Board | 40 mm near-circle with USB flat, four layers, nominal 1.0 mm |
| BLE | Raytac MDBT50Q-1MV2 / nRF52840 with chip antenna |
| Motion | LIS3DH accelerometer, I2C 0x18, motion interrupt; no gyro |
| Temperature | TMP117, I2C 0x48, underside placement, unpasted exposed pad |
| Power | Protected 1S 4.2 V Li-Po interface + external cell NTC; pack/harness pending |
| Charging | USB-C only; BQ24074, nominal 100 mA charging, power-path output |
| USB data | Full-speed USB for bootloader and CDC logs; SWD for first flash and hardware debug |
| User controls | Slide regulator-enable switch, user/reset buttons, green LED |
| Omitted | Magnetic/inductive/Qi charging and optional buzzer |
| Schematic | Implemented; see latest ERC report |
| PCB | Placed and routed candidate under review; see latest DRC report |
| Software | Bring-up plan and pin map only; no compiled firmware or USB compliance claim |
| Manufacturing | Preview exports; release held by the design review blockers |
| Portfolio | Draft case study and renders; public publishing not performed |

Release gates: zero unconnected items and unresolved DRC errors; reviewed pinouts/footprints for every populated MPN; qualified battery/NTC/harness; exact fabricator stack/DFM; current stock and supplier identifiers; USB current/suspend policy; mechanical clearance and sensor contact; validated thermal/EMC behavior; recovered bootloader and hardware test plan. Functional performance is established only by prototype measurements after fabrication.
