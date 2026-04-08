[V2G20-2009] If the PowerDeliveryReq received has ChargeProgress = "Start" and ServiceName = AC or AC_BPT in Table 204 was selected, the next allowed request shall be AC_ChargeLoopReq and the V2G_SECC_Sequence_Timeout is set according to Table 216.

[V2G20-2192] If the PowerDeliveryReq received has ChargeProgress = "Standby" and ServiceName = AC or AC_BPT in Table 204 was selected, the next allowed request shall be AC_ChargeLoopReq and the V2G_SECC_Sequence_Timeout is set according to Table 216.

[V2G20-2012] After receiving the AC_ChargeLoopReq, the SECC shall respond with an AC_ChargeLoopRes with "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 215. The next allowed request shall be AC_ChargeLoopReq or PowerDeliveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 216.

[V2G20-1623] If ServiceName = AC or AC_BPT in Table 204 is used, and the PowerDeliveryReq received has ChargeProgress = "Stop", the next allowed request shall be SessionStopReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1641] The SECC shall be able to set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" only in AC_ChargeLoopRes.

[V2G20-1642] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True" and the SECC decides to perform a ServiceRenegotiation for adapting its service offering, it shall set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" in AC_ChargeLoopRes.

####### 8.6.4.6.3.3 DC message flow

[V2G20-1611] After receiving the ScheduleExchangeReq, the SECC shall respond with a ScheduleExchangeRes with EVSEProcessing set to "Finished" within V2G_SECC_Msg_Performance_Time according to Table 215, if the process is finished. The next allowed request shall be DC_CableCheckReq if ServiceName= DC or DC_BPT in Table 204 was selected. The V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-2003] After receiving the DC_CableCheckReq, the SECC shall respond with a DC_CableCheckRes with EVSEProcessing set to "Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 217, while the cable check process is still ongoing. The next allowed request shall be DC_CableCheckReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-2004] After receiving the DC_CableCheckReq, the SECC shall respond with a DC_CableCheckRes with EVSEProcessing set to "Finished" within V2G_SECC_Msg_Performance_Time according to Table 217, if the cable check process is finished. The next allowed request shall be DC_PreChargeReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-2005] After receiving the DC_PreChargeReq with EVProcessing set to "Ongoing", the SECC shall respond with a DC_PreChargeRes within V2G_SECC_Msg_Performance_Time according to Table 217. The next allowed request shall be DC_PreChargeReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.