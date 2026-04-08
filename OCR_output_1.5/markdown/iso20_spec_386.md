
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>WPT_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,5</td></tr><tr><td rowspan="5">V2G_SECC_Msg_Performance_Time(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>WPT_FinePositioningSetupReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_FinePositioningReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_PairingReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_AlignmentCheckReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_Sequence_Performance_Time</td><td style='text-align: center; word-wrap: break-word;'>WPT_ChargeLoopReq</td><td style='text-align: center; word-wrap: break-word;'>0,25</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_Sequence_Timeout</td><td style='text-align: center; word-wrap: break-word;'>WPT_ChargeLoopRes</td><td style='text-align: center; word-wrap: break-word;'>0,5</td></tr></table>

##### 8.5.4.5 ACDP specific message sequence and session timing

[V2G20-4020] The EVCC shall implement the EVCC specific ACDP timeouts and performance times defined in Table 219.

[V2G20-4021] The SECC shall implement the SECC specific ACDP timeouts and performance times defined in Table 219.

<div style="text-align: center;">Table 219 — ACDP EVCC and SECC timeouts and performance times</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Name</td><td style='text-align: center; word-wrap: break-word;'>MessageType</td><td style='text-align: center; word-wrap: break-word;'>Value [s]</td></tr><tr><td rowspan="4">V2G_EVCC_Msg_Timeout(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>ACDP_VehiclePositioningReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_ConnectReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_DisconnectReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_SystemStatusReq</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td rowspan="4">V2G_SECC_Msg_Performance_Time(MessageType)</td><td style='text-align: center; word-wrap: break-word;'>ACDP_VehiclePositioningReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_ConnectReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_DisconnectReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_SystemStatusReq</td><td style='text-align: center; word-wrap: break-word;'>1,5</td></tr></table>

8.5.5 Session setup and ready to charge

##### 8.5.5.1 Common

Timing parameters applicable to the common communication session setup and ready to charge time defined in this document are shown in Table 220. Table 221 defines the values for the related common performance times and the timeouts.

<div style="text-align: center;">Table 220 — Common EVCC and SECC V2G communication session setup timing parameters</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2">Parameter name</td><td rowspan="2">Definition</td><td colspan="2">Implementation</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVCC</td><td style='text-align: center; word-wrap: break-word;'>SECC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_CommunicationSetup_Timer</td><td style='text-align: center; word-wrap: break-word;'>Communication setup timer in the EVCC</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_CommunicationSetup_Timer</td><td style='text-align: center; word-wrap: break-word;'>Communication setup timer in the SVCC</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr></table>