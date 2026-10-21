# Requirements and execution plan

Prepared: 2026-10-19. Status: draft for discussion.

## Confirmed direction

The user's priorities are PCB design and layout, KiCad 10 native deliverables, a board that can be manufactured and built, and a portfolio suitable for electrical design engineering applications. Use the named project directory as the canonical workspace. Save both source photos in `docs/client-request/`.

## Current agreed scope

- USB-C is the sole charging interface. Magnetic contacts, inductive wireless charging, Qi compatibility, receiver coils, and charging pucks are out of scope following the user's latest decision.
- USB-C also supports USB data for programming/debugging. Select a USB-capable controller and define bootloader/recovery behavior; retain separate hardware debug access for bring-up and recovery.
- Wrist-worn packaging is a working assumption. The user agreed to assume temperature measurement of the wearer; implement this as wrist skin-temperature sensing and trend tracking. Core body temperature and clinical accuracy are not established requirements or demonstrated capabilities.
- Battery capacity, runtime, board dimensions, temperature accuracy target, and prototype budget remain open. The earlier 30–35 mm suggestion is unverified.
- Define USB input protection, charger/system power-path behavior, battery protection, temperature monitoring, and charge-current limits from the selected battery and IC documentation.
- The photographed brief below is preserved as source context. This current scope supersedes its charging alternatives and earlier discussion of wireless charging.

## Requirements extracted from the photographs

| ID | Requirement | Verification / evidence |
|---|---|---|
| R01 | Bluetooth Low Energy connectivity | Connection and data-transfer test; document range test conditions |
| R02 | Rechargeable Li-Po battery | Selected battery specifications, protection implementation, charge/discharge tests |
| R03 | USB-C or magnetic charging | Select interface; verify input, charging, and powered-use behavior |
| R04 | Accelerometer / IMU | Select sensing axes and operating modes; read identity, data, and interrupt |
| R05 | Temperature sensor | Define measured quantity and accuracy; compare against reference |
| R06 | LED status indication | Firmware-controlled functional test; include current in power budget |
| R07 | Push-button or sliding power control | Document off/sleep/wake behavior; measure quiescent current |
| R08 | Optional buzzer or small acoustic transducer | Decide fitted, optional footprint, or omitted; test if fitted |
| R09 | Compact circular or near-circular multilayer PCB | Agree envelope and stackup; inspect dimensions and mechanical fit |
| R10 | Antenna placement, power integrity, sensor positioning | Datasheet-backed placement and layout review |
| R11 | Low-power operation | Mode-by-mode current budget and measured runtime/current |
| R12 | Programming/debug access | Document connector/pads, pinout, voltage, reset, and access with assembly |

Requested deliverables: complete schematic; native PCB design files; Gerbers and drills; pick-and-place; BOM with supplier part numbers; assembly drawings; STEP assembly model; programming/debug connector details. Basic verification firmware is preferred. Scope also includes architecture refinement, readily available components, battery charging/protection, ERC/DRC, manufacturing documentation, prototype fabrication support, and initial debugging.

## Decisions needed before schematic freeze

1. Define wrist skin-temperature accuracy, sampling rate, trend-reporting behavior, skin-contact arrangement, and reference measurement method. The motion/activity application remains to be defined.
2. Mechanical envelope: maximum diameter, total thickness including battery, attachment method, enclosure material, connector access, and battery position.
3. Battery life and behavior: expected active duty cycle, sample rate, BLE traffic, recharge interval, charging time, and operation while charging.
4. Prototype budget, board quantity, assembly approach, and preferred manufacturer.
5. BLE module versus discrete radio/antenna design; accelerometer versus six-axis IMU.

## Proposed starting point — assumptions, not approved specifications

A motion/activity demonstration with wrist skin-temperature telemetry; a roughly 30–35 mm circular or near-circular four-layer PCB; USB-C charging/data; a single-cell Li-Po; a BLE module with integrated antenna; an IMU, separate temperature sensor, LED, user button, and accessible debug pads. These are starting options for a feasibility study. Battery capacity, runtime, temperature accuracy, BLE range, layer stackup, and component MPNs remain unset.

Compare a module and discrete RF implementation before selection. A module can focus the first revision on board integration and verification; a discrete implementation adds RF matching and antenna validation work. Either choice needs antenna keepouts and an assessment of the battery, body, and enclosure. No certification claim follows from choosing a module.

Proposed functional chain:

`charging input -> input protection / charger with appropriate power path -> protected battery and system supply -> BLE controller + sensors + indicators`

Battery temperature monitoring, charge-current limits, regulation, off-state behavior, and protection responsibilities must be resolved from the selected cell and IC documentation. Plan a skin-facing thermal path for the temperature sensor and limit thermal coupling from the charger, regulator, controller, and battery. Review PCB copper, sensor location, enclosure contact surface, and fit together. Validate sensor response and bias against an appropriate reference at the skin-contact interface, including changes in ambient conditions and device activity. Define whether readings during charging are suppressed or flagged. Report measured skin temperature without implying core-temperature or clinical validation.

## Milestones and exit criteria

### 1. Requirements and architecture

Agree operating scenario, mechanical envelope, runtime target, budget, and sensing intent. Produce a block diagram, preliminary power budget, mechanical placement study, and decision log. Select actual battery and connector geometry before locking the board outline.

### 2. Component and schematic development

Compare candidate parts with current datasheets and sourcing information. Record MPNs and supplier identifiers on symbols. Verify package pinouts, recommended circuits, charger configuration, protection, voltage compatibility, pull-ups, boot states, debug access, and test points. Save local libraries where needed. Review the complete schematic and resolve ERC findings with documented reasons for any exclusions.

### 3. PCB placement and routing

Agree a fabricator stackup and fabrication limits before setting impedance or design rules. Place mechanical constraints and antenna first, then power circuits, sensors, controller, decoupling, and support circuitry. Protect antenna keepouts and maintain return paths.

Route sensitive RF, switching-current loops, decoupling, and any controlled-impedance interfaces deliberately. Evaluate KiCadRoutingTools for remaining routes on a copy of the board. Save tool version, command/configuration, and before/after DRC reports. Refill zones and review actual copper, connectivity, ground return paths, and physical access after automated routing.

### 4. Design review and fabrication release

Verify symbols and footprints against exact package drawings. Cross-check schematic and PCB. Run ERC/DRC with no unresolved errors or unexplained exclusions; verify no unintended unrouted nets. Include applicable power, thermal, EMC, and simulation checks with explicit limitations.

Inspect generated Gerbers/drills independently, confirm outline, stackup, solder mask/paste, polarity, orientation, BOM/CPL agreement, assembly drawings, and STEP fit. Save an immutable revision-specific manufacturing package with a manifest and review record. Do not label preliminary exports manufacturing-ready.

### 5. Prototype bring-up

Prepare a current-limited power-up sequence and measurements before hardware arrives. Test supply rails, programming, charge behavior, battery protection integration, sensors, BLE, indications, and sleep/wake. Measure current by operating mode, assess temperature bias during charging, and evaluate RF in the intended enclosure/wear configuration. Record failures and revision decisions.

### 6. Portfolio case study

Present requirements, engineering tradeoffs, power budget, annotated schematic sections, placement rationale, return paths, antenna keepouts, manufacturing constraints, renders, and assembly documentation. Add actual board photographs, current traces, test results, and lessons from revisions once available.

Clearly separate calculated expectations, simulated results, and measured performance. Describe the project as independent work based on a reference brief unless a real client relationship is established. Draft publication materials after release; upload destination remains to be selected.

## Tooling baseline and open items

- Installed CLI reports KiCad **10.0.7**. Sandbox registry access emitted warnings during the version check; file-generation and GUI workflow remain to be tested.
- Local routing checkout: `C:\Users\hecto\Documents\KiCAD_Projects\_tools\KiCadRoutingTools`, VERSION **0.23.1**. Runtime/build readiness has not been tested.
- Upstream README advertises KiCad 9/10 support: https://github.com/drandyhaas/KiCadRoutingTools (checked 2026-10-19). Compatibility does not establish board quality or guaranteed token savings.
- Installed `kicad` and `bom` skills are available. The user-mentioned `kicad-happy` / `kicacd-happy` skill has not yet been located.
- No parts have been selected, schematic created, routing performed, or fabrication checks passed at this planning stage.




