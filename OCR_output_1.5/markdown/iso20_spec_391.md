[V2G20-1774] The EVCC and SECC shall implement the DC timing parameter values defined in Table 223.

<div style="text-align: center;">Table 223 — DC specific EVCC and SECC message sequence and session timing parameter values</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2">Parameter name</td><td rowspan="2">Value [s]</td><td colspan="2">Implementation</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVCC</td><td style='text-align: center; word-wrap: break-word;'>SECC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_DC_CableCheck_Performance_Time</td><td style='text-align: center; word-wrap: break-word;'>38</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_DC_CableCheck_Timeout</td><td style='text-align: center; word-wrap: break-word;'>40</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SECC_DC_PreCharge_Performance_Time</td><td style='text-align: center; word-wrap: break-word;'>9</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_EVCC_DC_PreCharge_Timeout</td><td style='text-align: center; word-wrap: break-word;'>10</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

###### 8.5.5.2.1 EVCC Timing for cable check

The EVCC shall set the timeout V2G_EVCC_DC_CableCheck_Timeout to the value as defined in Table 223, reset the V2G_EVCC_DC_CableCheck_Timer and start monitoring the V2G_EVCC_DC_CableCheck_Timer when sending the message DC_CableCheckReq for the first time in a charging session.

NOTE 1 In this document, sending a request message is described by A-Data.request.

[V2G20-1397] The EVCC shall wait for the cable check of the EVSE to finish indicated by the reception of a DC_CableCheckRes with ResponseCode equal to "OK" and EVSEProcessing equal to "Finished".

NOTE 2 In this document, receiving a response message is described by A-Data.confirmation.

[V2G20-1398] The EVCC shall stop waiting for the Cable check of the EVSE to finish and stop monitoring the V2G_EVCC_DC_CableCheck_Timer when V2G_EVCC_DC_CableCheck_Timer is equal or larger than V2G_EVCC_DC_CableCheck_Timeout. It shall then apply the error handling as defined in 8.6.

[V2G20-1399] The EVCC shall stop waiting for the cable check of the EVSE to finish and stop monitoring the V2G_EVCC_DC_CableCheck_Timer if V2G_EVCC_DC_CableCheck_Timer is smaller than V2G_EVCC_DC_CableCheck_Timeout and a DC_CableCheckRes message with ResponseCode equal to "OK" and EVSEProcessing equal to "Finished" was received. It shall then process the response message as defined in 8.6.

NOTE 3 In this document, receiving a response message is described by A-Data.confirmation.

###### 8.5.5.2.2 EVCC Timing for pre charging

## [V2G20-704]

The EVCC shall set the timeout V2G_EVCC_DC_PreCharge_Timeout to the value as defined in Table 223, reset the V2G_EVCC_DC_PreCharge_Timer and start monitoring the V2G_EVCC_DC_PreCharge_Timer when sending the message DC_PreChargeReq for the first time in a charging session.

NOTE 4 In this document, sending a request message is described by A-Data.request.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.