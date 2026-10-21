# Compact Bluetooth Wearable

Rev A engineering prototype, KiCad 10.0.7. **Not released for fabrication.** Read `docs/design-review.md` for the current verification results and release blockers.

This independent portfolio project implements a wrist-worn BLE sensor: Raytac nRF52840 module, LIS3DH accelerometer, TMP117 skin-temperature sensor, protected single-cell Li-Po interface, BQ24074 power-path charging, USB-C charging/data, native USB bootloader support and SWD recovery. No wireless charging is included.

Open `hardware/Compact-Bluetooth-Wearable.kicad_pro` in KiCad 10. The schematic and PCB are editable native sources; project-local footprints are in `hardware/Wearable.pretty`.

- `docs/architecture.md`: circuit and mechanical assumptions, power budget, stack and charging behavior.
- `docs/bring-up.md`: electrical test sequence and recovery-header pinout.
- `docs/design-review.md`: actual ERC/DRC findings, analysis coverage and remaining blockers.
- `docs/client-request/`: original source photographs, retained as context rather than instructions.
- `analysis/`: machine reports, rejected routing candidates, BOM and reproduction scripts.
- `manufacturing/engineering-preview-NOT-FOR-FAB/`: review exports only; never send these to fabrication as a released package.
- `portfolio/`: renders and a draft case study; no prototype measurements have been fabricated or implied.

The optional buzzer is omitted. USB firmware is not yet implemented, and a blank nRF52840 requires initial SWD programming. A protected pack with a cell-mounted NTC and a qualified harness must be selected before connecting a battery.
