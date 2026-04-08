NOTE 2 If the SECC sees, that the EVPresentVoltage exceeds one of the limits then there is the risk of a termination of the charging session due to the EV enforcing safety protection measures.

If, for example, the EV is measuring voltage via the BMS inside the battery and is also using a DC-DC converter between the battery and the DC inlet then the EVCC shall apply a meaningful mathematical transformation to the actual measured voltage values. It is important that the EVPresentVoltage multiplied with EVSEPresentCurrent does not contradict any power limitations communicated by the EV because the SECC might use that as a plausibility check to validate its charging strategy.

## [V2G20-2198]

The absolute value of the following elements, if provided within any DC energy transfer control loop message, shall be less than or equal to the absolute value of the same element provided earlier in the DC_ChargeParameterDiscovery message pair:

EVMaximumChargeCurrent

EVMaximumDischargeCurrent

EVMaximumChargePower

EVMaximumDischargePower

– EVMaximumVoltage

## [V2G20-2199]

The absolute value of the following elements, if provided within any DC energy transfer control loop message, shall be higher than or equal to the absolute value of the same element provided earlier in the DC_ChargeParameterDiscovery message pair:

EVMinimumChargeCurrent

EVMinimumDischargeCurrent

– EVMinimumChargePower

– EVMinimumDischargePower

– EVMinimumVoltage

####### 8.3.4.5.5.3 DC_ChargeLoopRes

After receiving the DC_ChargeLoopReq from the EVCC the SECC sends the DC_ChargeLoopRes informing the EV about the EVSE status and the present EVSE output voltage and current.

[V2G20-1284]

The EVCC and the SECC shall implement the message elements as defined in Table 65 and Figure 69.

