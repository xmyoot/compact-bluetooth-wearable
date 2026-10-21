# Bring-up and verification plan

Do not attach the prototype to a person during initial electrical tests. Use a current-limited supply and a battery simulator first.

1. Inspect polarity, solder bridges, module antenna region and TMP117 underside. Confirm exact pack and harness pinout before plugging in a cell.
2. With logic off, apply 5 V with a low current limit. Measure VBUS, VSYS, charger status, no-battery behavior and NTC hot/cold inhibition with known resistors.
3. Enable logic. Confirm 3.0 V, startup and reset. Use the SWD header: 1=3V0 sense, 2=SWDIO, 3=SWCLK, 4=GND, 5=RESET_N, 6=GND. The debugger must not back-power the target.
4. Flash a minimal SWD image. Verify I2C addresses 0x18 and 0x48, accelerometer WHO_AM_I, axis polarity, motion interrupt, TMP117 identity/configuration, alert, LED and user button.
5. Install a recoverable USB bootloader over SWD. Test USB enumeration, CDC logs and firmware update in both USB-C orientations. Retain SWD recovery access.
6. Verify USB input current before/after enumeration and suspend, including logic off and depleted/no battery. Exercise EN1/EN2 truth table. No 500 mA assumption before host permission.
7. Test charging with the released protected pack, cell NTC, current logging and temperature monitoring. Measure CC/CV voltage, termination, recharge, load sharing and unplug transitions.
8. Measure sleep, advertising, connected, acquisition and off currents. Record actual runtime and low-battery behavior.
9. Characterize skin sensor settling and charger/MCU self-heating against a traceable reference on a controlled thermal fixture. Repeat with enclosure and contact pressure variations. Suppress or flag readings while charging if bias is excessive.
10. Test BLE range with assembled enclosure, battery and representative wrist loading; assess ESD and emissions with appropriate lab equipment. Review battery/charging safety and product compliance before public release.

The firmware is not implemented or compiled in this revision. Default GPIO mappings are recorded in the native schematic and design-manifest.json; they must be reflected in the eventual board definition.
