<div style="text-align: center;">Table 216 — AC EVCC and SECC timeouts and performance times</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Name</td><td style='text-align: center; word-wrap: break-word;'>MessageType</td><td style='text-align: center; word-wrap: break-word;'>Value [s]</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_Msg_Timeout(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>AC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_Msg_Performance_Time(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>AC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_Sequence_Performance_Time</td><td style='text-align: center; word-wrap: break-word;'>AC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_Sequence_Timeout</td><td style='text-align: center; word-wrap: break-word;'>AC_ChargeLoopRes</td><td style='text-align: center; word-wrap: break-word;'>0,5</td></tr></table>

##### 8.5.4.3 DC specific message sequence and session timing

[V2G20-1501] The EVCC shall implement the EVCC specific DC timeouts and performance times defined in Table 217.

[V2G20-1502] The SECC shall implement the SECC specific DC timeouts and performance times defined in Table 217.

<div style="text-align: center;">Table 217 — DC EVCC and SECC timeouts and performance times</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Name</td><td style='text-align: center; word-wrap: break-word;'>MessageType</td><td style='text-align: center; word-wrap: break-word;'>Value [s]</td></tr><tr><td rowspan="4">V2G_EVCC_Msg_Timeout(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>DC_CableCheckReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_PreChargeReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0.5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_WeldingDetectionReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td rowspan="4">V2G_SECC_Msg_Performance_Time(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>DC_CableCheckReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_PreChargeReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DC_WeldingDetectionReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_Sequence_Performance_Time</td><td style='text-align: center; word-wrap: break-word;'>DC_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_Sequence_Timeout</td><td style='text-align: center; word-wrap: break-word;'>DC_ChargeLoopRes</td><td style='text-align: center; word-wrap: break-word;'>0,5</td></tr></table>

##### 8.5.4.4 WPT specific message sequence and session timing

[V2G20-5069] The EVCC shall implement the EVCC specific WPT timeouts and performance times defined in Table 218.

[V2G20-5070] The SECC shall implement the SECC specific WPT timeouts and performance times defined in Table 218.

<div style="text-align: center;">Table 218 — WPT EVCC and SECC timeouts and performance times</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Name</td><td style='text-align: center; word-wrap: break-word;'>MessageType</td><td style='text-align: center; word-wrap: break-word;'>Value [s]</td></tr><tr><td rowspan="4">V2G_EVCC_Msg_Timeout(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>WPT_FinePositioningSetupReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_FinePositioningReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_PairingReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_AlignmentCheckReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr></table>

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.