[V2G20-1440] If the EVCC wants to continue the energy transfer and received the AC_ChargeLoopRes with "ResponseCode = OK", the EVCC shall send another AC_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 216.

[V2G20-1443] If the EVCC wants to stop the energy transfer and received the AC_ChargeLoopRes with "ResponseCode = OK, the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Stop" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-2193] If the EVCC wants to enter a standby phase and received the AC_ChargeLoopRes with "ResponseCode = OK, the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Standby" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1969] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "True" and the EVCC decided to perform a ServiceRenegotiation for adapting its service selection, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Stop" after AC_ChargeLoopRes has been received while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

NOTE 3 As the renegotiation of a service requires to properly end the current charging session (energy transfer) the EVCC will process all required messages (depending on currently selected service) to SessionStopReq where the request for a ServiceRenegotiation is to be set according to [V2G20-1476].

8.6.4.5.3.3 DC message flow

[V2G20-2098] After receiving the SessionSetupRes with ResponseCode equal to "OK", the EVCC shall send the proper DC_ChargeParameterDiscoveryReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time, in case the EVCC resumes a previously paused V2G communication session.

NOTE In case of a resumed session, the authorization is not required, as authorization details of the previous communication session are valid for the whole service session, see [V2G20-1844].

[V2G20-1594] If EVCC is using ServiceName= DC or DC_BPT in Table 204, after receiving the ScheduleExchangeRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send a DC_CableCheckReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217.

[V2G20-1431] After receiving the DC_CableCheckRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send another DC_CableCheckReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217.

[V2G20-1432] After receiving the DC_CableCheckRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send a DC_PreChargeReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217.

[V2G20-1433] After receiving the DC_PreChargeRes with "ResponseCode = OK", the EVCC shall send a DC_PreChargeReq with EVProcessing set to "Ongoing" within V2G_EVCC_Sequence_Performance_Timeout according to Table 217 while the precharge process is not finished.