[V2G20-2006] After receiving the DC_PreChargeReq with EVProcessing set to "Finished", the SECC shall respond with a DC_PreChargeRes within V2G_SECC_Msg_Performance_Time according to Table 217. The next allowed request shall be PowerDeliveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-2010] If the PowerDeliveryReq received has ChargeProgress = "Start" and ServiceName = DC or DC_BPT in Table 204 was selected, the next allowed request shall be DC_ChargeLoopReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-2013] After receiving the DC_ChargeLoopReq, the SECC shall respond with a DC_ChargeLoopRes with "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 217. The next allowed request shall be DC_ChargeLoopReq or PowerDeliveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-2020] If ServiceName = DC or DC_BPT in Table 204 is used, and the PowerDeliveryReq received has ChargeProgress = "Stop", the next allowed request shall be DC_WeldingDetectionReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-1630] After receiving the DC_WeldingDetectionReq with EVProcessing set to "Ongoing", the SECC shall respond with a DC_WeldingDetectionRes within V2G_SECC_Msg_Performance_Time according to Table 217. The next allowed request shall be DC_WeldingDetectionReq and the V2G_SECC_Sequence_Timeout is set according to Table 217.

[V2G20-1631] After receiving the DC_WeldingDetectionReq with EVProcessing set to "Finished", the SECC shall respond with a DC_WeldingDetectionRes within V2G_SECC_Msg_Performance_Time according to Table 217. The next allowed request shall be SessionStopReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1598] The SECC shall be able to set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" only in DC_ChargeLoopRes.

[V2G20-1599] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True" and the SECC decides to perform a ServiceRenegotiation for adapting its service offering, it shall set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" in DC_ChargeLoopRes.

####### 8.6.4.6.3.4 WPT message flow

[V2G20-5043] After receiving a SessionSetupReq, the SECC shall respond with a SessionSetupRes within V2G_SECC_Msg_Performance_Time according to Table 215. If the WPT module is applied, the allowed next request shall be WPT_FinePositioningSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-5085] After receiving a WPT_FinePositioningSetupReq, the SECC shall respond with a WPT_FinePositioningSetupRes within V2G_SECC_Msg_Performance_Time according to Table 218. The allowed next request shall be WPT_FinePositioningReq or WPT_FinePositioningSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 218.