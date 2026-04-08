for parameter DiagStatus equal to "Finished with EVSEID" or parameter DiagStatus equal to "Finished without EVSEID".

[V2G20-2296] If [V2G20-2295] applies, the EVCC shall stop and then restart the SDP process when V2G_EVCC_Ongoing_Timer is equal or larger than V2G_EVCC_Ongoing_Timeout and no parameter EVSE_Processing equal to "Finished" has been received.

[V2G20-2298] The EVCC shall set the timeout V2G_EVCC_CommunicationSetup_Timeout to the value as defined in Table 221, reset the V2G_EVCC_CommunicationSetup_Timer and start monitoring the V2G_EVCC_CommunicationSetup_Timer when a successful TCP/TLS connection has been established.

[V2G20-447] The EVCC shall wait for the SessionSetupRes message.

[V2G20-448] The EVCC shall stop waiting for the SessionSetupRes message and stop monitoring the V2G_EVCC_CommunicationSetup_Timer when V2G_EVCC_CommunicationSetup_Timer is equal or larger than V2G_EVCC_CommunicationSetup_Timeout and no SessionSetupRes message was received. It shall then stop the V2G communication session.

NOTE 1 In this document receiving the response message "SessionSetupRes" is described by A-Data.confirmation (SessionSetupRes).

[V2G20-449] The EVCC shall stop waiting for the SessionSetupRes message and stop monitoring the V2G_EVCC_CommunicationSetup_Timer when V2G_EVCC_CommunicationSetup_Timer is smaller than V2G_EVCC_CommunicationSetup_Timeout and a SessionSetupRes message was received. It shall then process the response message as defined in 8.6.

NOTE 2 In this document receiving the response message "SessionSetupRes" is described by A-Data.confirmation (SessionSetupRes).

###### 8.5.5.1.2 SECC Timing for communication session setup

[V2G20-2303] The SECC shall set the timeout V2G_SECC_CommunicationSetup_Performance_Time the value as defined in Table 221, reset the V2G_SECC_CommunicationSetup_Timer and start monitoring the V2G_SECC_CommunicationSetup_Timer when a successful TCP/TLS connection has been established.

[V2G20-715] The SECC shall wait for the SessionSetupReq message.

[V2G20-2300] The SECC shall stop waiting for SessionSetupReq and stop monitoring the V2G_SECC_CommunicationSetup_Timer when V2G_SECC_CommunicationSetup_Timer is smaller than V2G_SECC_CommunicationSetup_Performance_Time and a SessionSetupRes message was received. It shall then process the response message as defined in 8.6.

[V2G20-716] The SECC shall stop waiting for SessionSetupReq and stop monitoring the V2G_SECC_CommunicationSetup_Timer when V2G_SECC_CommunicationSetup_Timer is equal or larger than V2G_SECC_CommunicationSetup_Performance_Time and no SessionSetupRes message was sent. It shall then apply [V2G20-034].

NOTE In this document sending the response message "SessionSetupRes" is described by A-Data.response(SessionSetupRes).

###### 8.5.5.1.3 EVCC Timing for EVSEProcessing parameter

## 384 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.