####### 8.6.4.5.3.4 WPT message flow

[V2G20-5042] If the EVCC is using the WPT module, after receiving the SessionSetupRes with "ResponseCode = OK", the EVCC shall send a WPT_FinePositioningSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5046] After receiving the SessionSetupRes with ResponseCode equal to "OK", the EVCC shall send a WPT_ChargeParameterDiscoveryReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time, in case EVCC resumes a previously paused V2G communication session.

NOTE In case of a resumed session, the authorization is not required, as authorization details of the previous communication session are valid for the whole service session, see [V2G20-1844].

[V2G20-5067] After receiving one of the messages WPT_FinePositioningSetupRes, WPT_FinePositioningRes, WPT_PairingRes, WPT_AlignmentCheckRes, WPT_ChargeLoopRes with ResponseCode = FAILED the EVCC shall send a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218 to terminate the session.

[V2G20-5024] After receiving a WPT_FinePositioningSetupRes with "ResponseCode = OK", the EVCC shall send a WPT_FinePositioningReq or a WPT_FinePositioningSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5025] After receiving a WPT_FinePositioningRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send a WPT_FinePositioningReq with EVProcessing set to "Ongoing" while the vehicle positioning is still ongoing within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5026] After receiving a WPT_FinePositioningRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send a WPT_FinePositioningReq with EVProcessing set to "Finished" when the vehicle positioning is finished within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5027] After sending a WPT_FinePositioningReq with EVProcessing set to "Finished", and receiving the next response message with "ResponseCode = OK", the EVCC shall send a WPT_PairingReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5029] After receiving a WPT_FinePositioningRes with "ResponseCode = OK" and EVSEProcessing set to "Finished", the EVCC shall send a WPT_PairingReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5055] After receiving a WPT_FinePositioningRes with "ResponseCode = WARNING_WPT" and EVSEProcessing set to "Finished", the EVCC shall send a WPT_FinePositioningSetupReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5030] After receiving a WPT_PairingRes with "ResponseCode = OK" and EVSEProcessing = "Ongoing", the EVCC shall send a WPT_PairingReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218. While the pairing process is still on-going, the EVCC shall send the WPT_PairingReq with EVProcessing set to "Ongoing".