# Compact Bluetooth Wearable — engineering case study draft

**Status: design prototype under review. No assembled hardware results yet.**

## Problem and scope

Develop a compact wrist-worn BLE board from an open-ended client-style brief. The work emphasizes electrical design, power management, RF-aware PCB placement, sensor positioning and native KiCad 10 deliverables. USB-C serves charging and firmware data; wireless charging and a buzzer are excluded.

## Decisions worth presenting

- A module-based nRF52840 architecture provides BLE and native USB while keeping RF design tractable. Explicit antenna keepouts constrain every copper layer.
- Power-path charging separates system supply from battery charging, and logic power control permits charging while the main logic is off. USB source-current and suspend handling require an explicit firmware/hardware review.
- The skin sensor is separated from charger heat and placed on the underside. The design distinguishes local skin temperature from core-body estimates and leaves mechanical thermal-contact validation as an experiment.
- Initial autorouting was rejected when it reduced fabrication feature sizes. Later passes enforce 0.15 mm track/clearance and 0.60/0.30 mm through vias; independent KiCad DRC remains the acceptance check.
- Placement gives supply decoupling priority. SWD recovery remains available even before a USB bootloader is installed.

## Evidence to include

Architecture, readable native schematic/PDF, PCB top/bottom and layer plots, ERC/DRC reports, BOM provenance, open-issue log and a documented bring-up sequence. Add fabricated-board photographs, measured charge/current traces, sensor calibration and BLE results after actual testing.

## Claims intentionally pending

Manufacturing release, battery runtime, skin-temperature accuracy, USB/EMC compliance, enclosure/wearability, assembly yield and firmware functionality have not been demonstrated. Describe those as planned validation, not finished results.
