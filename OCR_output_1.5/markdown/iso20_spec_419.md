"OK", the EVCC shall send a ServiceDiscoveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1478] If in the first ServiceDiscoveryRes of the service session the SECC has set ServiceRenegotiationSupported to "False", after waking up from a Pause, the EVCC shall select exactly the same ServiceIDs and ParameterSetIDs it previously selected in the last ServiceSelectionReq. This means it shall not select additional services, deselect previously selected services or change ParameterSetID of a service.

[V2G20-1479] If in the first ServiceDiscoveryRes of the service session the SECC has set ServiceRenegotiationSupported to "True", after waking up from a Pause, the EVCC may select any offered services and parameters independent of the selection in the last ServiceSelectionReq.

[V2G20-1480] The EVCC shall only consider the status of the parameter ServiceRenegotiationSupported sent in the first ServiceDiscoveryRes of the service session.

[V2G20-1661] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "True" and the EVCC decided to perform a ServiceRenegotiation for adapting its service selection, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Stop" after ChargeLoopRes has been received while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

NOTE 5 As the renegotiation of a service requires to properly end the current charging session (energy transfer) the EVCC will process all required messages (depending on currently selected service) to session stop where the request for a ServiceRenegotiation is to be set according to [V2G20-1476].

####### 8.6.4.5.3.2 AC message flow

[V2G20-2097] After receiving the SessionSetupRes with ResponseCode equal to "OK", the EVCC shall send the proper AC_ChargeParameterDiscoveryReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time, in case the EVCC resumes a previously paused V2G communication session.

NOTE 1 In case of a resumed session, the authorization is not required, as authorization details of the previous communication session are valid for the whole service session, see [V2G20-1844].

[V2G20-1596] If EVCC is using ServiceName = AC or AC_BPT in Table 204, after receiving the ScheduleExchangeRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send a PowerDeliveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1437] If EVCC uses ServiceName = AC or AC_ACDP or AC_BPT or AC_ACD_BPT from Table 204, after receiving the PowerDeliveryRes with "ResponseCode = OK" or "ResponseCode = WARNING_PowerToleranceNotConfirmed", the EVCC shall send an AC_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 216 to start the energy transfer, a schedule renegotiation or to enter a standby period.

NOTE 2 During standby both EV and EVSE contactors are to stay closed. The standby concept is solely used as communication state within this documents and therefore is not reflected in related documents, e.g. IEC 61851-1 or IEC 61851-23.

## 414 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.