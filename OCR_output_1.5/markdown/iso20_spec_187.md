
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Scheduled_AC_CLReqControlMode</td><td style='text-align: center; word-wrap: break-word;'>complexType:Scheduled_AC_CLReqControlModeTyperefer to 8.3.5.4.4</td><td style='text-align: center; word-wrap: break-word;'>This element is used by the EVCC for offering and setting parameters for scheduled control mode energy transfer.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BPT_Scheduled_AC_CLReqControlMode</td><td style='text-align: center; word-wrap: break-word;'>complexType:BPT_Scheduled_AC_CLReqControlModeTyperefer to 8.3.5.4.7.4</td><td style='text-align: center; word-wrap: break-word;'>This element is used by the EVCC for offering and setting parameters for scheduled control mode BPT.</td></tr></table>

[V2G20-1810] The absolute value of the following elements, if provided within any AC energy transfer control loop message, shall be less than or equal to the absolute value of the same element provided earlier in the AC_ChargeParameterDiscovery message pair:

– EVMaximumChargePower

– EVMaximumDischargePower

[V2G20-1812] The absolute value of the following elements, if provided within any AC energy transfer control loop message, shall be higher than or equal to the absolute value of the same element provided earlier in the AC_ChargeParameterDiscovery message pair:

– EVMinimumChargePower

– EVMinimumDischargePower

####### 8.3.4.4.3.3 AC_ChargeLoopRes

After receiving the AC_ChargeLoopReq from the EVCC, the SECC sends the AC_ChargeLoopRes.

[V2G20-1278] The EVCC and the SECC shall implement the message elements as defined in Table 57 and Figure 61.