[V2G20-1829] The EVSEPowerRampLimitation shall be applied as a %/min factor to either the EVMaximumChargePower or the EVMaximumDischargePower in order to calculate the highest allowed absolute power change rate per minute.

[V2G20-1830] An EVSEPowerRampLimitation value of 0 %/min shall be interpreted as if the parameter was not present. In those cases the SECC does not require any local power ramp limits.

[V2G20-1831] The EVSEPowerRampLimitation shall be respected by the EV when adjusting its power level to external setpoint commands. This includes the reaction to changing maximum power levels as prescribed by the different entries in power schedules or the changes made by the EV user via other input means, like for example a mobile app.

[V2G20-1832] The EVSETargetActivePower control shall be able to override any limitation that was derived from the EVSEPowerRampLimitation. The same shall apply to any technique which implements a grid code requirement that has a higher priority than power ramp limitation.

[V2G20-1826] In scheduled control mode within the context of the AC_ChargeLoopRes the elements EVSETargetActivePower and EVSETargetReactivePower shall only be used by the SECC in situations where the technical requirements of the local grid code mandate such ad-hoc interference with the EV's power profile.

NOTE 3 A typical example is "Active response to frequency deviation - P(f)" which is mandatory in some regions even for adjustable loads when the grid enters a highly critical state (sometimes referred to as "red phase").

###### 8.3.5.4.3 Dynamic_AC_CLReqControlModeType

This type contains all elements of the AC_ChargeLoopReq message that are only required in case the control mode Dynamic is chosen.

[V2G20-1758] The SECC and the EVCC shall implement this type as defined in Table 161 and Figure 170.