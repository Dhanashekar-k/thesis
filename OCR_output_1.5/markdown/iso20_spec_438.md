is still ongoing. The next allowed request shall be WPT\_AlignmentCheckReq. The V2G\_SECC\_Sequence\_Timeout is set according to Table 218.

[V2G20-5123] If the PowerDeliveryReq received has ChargeProgress = "Start" and ServiceName = WPT in Table 204 was selected, the next allowed request shall be WPT_ChargeLoopReq or WPT_FinePositioningSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 218.

[V2G20-5124] After receiving the WPT_ChargeLoopReq, the SECC shall respond with a WPT_ChargeLoopRes with "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 218. The next allowed request shall be WPT_ChargeLoopReq or PowerDeliveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-5094] If the PowerDeliveryReq received has ChargeProgress = "Stop", and ServiceName = WPT in Table 204, the next allowed request shall be SessionStopReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-5095] The SECC shall be able to set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" only in WPT_ChargeLoopRes.

[V2G20-5096] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True" and the SECC decides to perform a ServiceRenegotiation for adapting its service offering, it shall set the parameter EVSENotification in EVSEStatus to "ServiceRenegotiation" in WPT_ChargeLoopRes.

8.6.4.6.3.5 ACDP message flow

NOTE 1 The common requirements [V2G20-1483] and [V2G20-1484] apply.

[V2G20-4067] After receiving a SessionSetupReq, the SECC shall respond with a SessionSetupRes within V2G_SECC_Msg_Performance_Time according to Table 215. If the SECC is using "WLAN", the allowed next request shall be ACDP_VehiclePositioningReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4068] If SECC is using ServiceName = DC_ACDP, after receiving the ACDP_VehiclePositioningReq, the SECC shall respond with a ACDP_VehiclePositioningRes with EVSEProcessing set to "Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 215, while the vehicle positioning is still ongoing. The next allowed request shall be ACDP_VehiclePositioningReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4069] After receiving a ACDP_VehiclePositioningReq with EVMobilityStatus set to "EV is immobilized", the SECC shall respond with a ACDP_VehiclePositioningRes with EVSEProcessing set to "Finished" within V2G_SECC_Msg_Performance_Time according to Table 215. The next allowed request shall be AuthorizationSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

NOTE 2 The common requirements apply [V2G20-1971], [V2G20-1970], [V2G20-1975], [V2G20-1973], [V2G20-1976], [V2G20-1972], [V2G20-1977], [V2G20-1978], [V2G20-1979], [V2G20-1980], [V2G20-1981], [V2G20-1983] and [V2G20-1986].

[V2G20-4070] After receiving the ScheduleExchangeReq, the SECC shall respond with a ScheduleExchangeRes with EVSEProcessing set to "Finished" within