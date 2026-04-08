
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Physical unit</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>PowerTolerance</td><td style='text-align: center; word-wrap: break-word;'>W</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>RemainingTimeToFullSOC</td><td style='text-align: center; word-wrap: break-word;'>s</td></tr></table>

NOTE 1 The maximum and minimum transmittable values are calculated using the boundaries of the RationalNumberType. They are given through the signed 16-bit Integer (Range: -32 768 to +32 767) of the value and the exponent.

NOTE 2 Values from -32 768 – +32 767 can be changed till the last digit, but when the exponent is used the changeable amount changes. For example if an exponent of 1 is used the changes can only be made until the 10 digit range or if the exponent of 2 is used the number can only be changed till 100 digit range.

NOTE 3 The transmittable range is not the range of allowed values for the used system. It is important that these ranges are implemented according to the limits of the implementation and the corresponding IEC documents, to follow safety regulations.

###### 8.3.5.2.1 Common rules for physical values

[V2G20-1034] For all applications a positive value for elements with the physical unit "W", "Wh" and "A" shall represent a power transfer from the EVSE to the EV (charging mode).

[V2G20-1035] Negative values shall be used to define energy transfer from the EV to the EVSE (discharging mode).

[V2G20-1783] For all applications in AC power transfer the elements with the physical unit:

– "V" and "A" shall be interpreted as root mean square values;

– "V" shall always be measured between one phase and neutral, unless stated otherwise;

– "W" shall be based on the assumption of a purely resistive AC circuit with a power factor of 1.0;

– for the "VA reactive" unit positive values shall represent inductive and negative values shall represent capacitive reactive power.

Equipment with other characteristics shall apply proper adjustments during related value calculations.

In the case of AC (dis)charging the EVSETargetActivePower and EVSETargetReactive elements serve two purposes. In dynamic control mode they are the normal means of operation while in Scheduled control mode they should only be used as a technique to guarantee that the mandatory local technical requirements from the grid code or urgent local requirements can be satisfied.

[V2G20-1823]

EVSETargetActivePower and EVSETargetReactivePower shall always be based on EVSENominalVoltage.



NOTE From the perspective of the EV the EVSETargetActivePower and EVSETargetReactivePower elements therefore primarily communicate target setpoints for the active and reactive currents and the resulting phi angle ("power factor") as the grids voltage can and will be fluctuating, even during the delay resulting from the communication processing.

[V2G20-1824] For the EVSETargetReactivePower positive values shall represent inductive and negative values shall represent capacitive reactive power.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.