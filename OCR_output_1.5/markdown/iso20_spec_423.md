[V2G20-5031] After receiving the WPT_PairingRes with "ResponseCode = OK" and EVSEProcessing = "Ongoing", the EVCC shall send a WPT_PairingReq with EVProcessing set to "Finished" within V2G_EVCC_Sequence_Performance_Timeout according to Table 190 if the pairing process is finished (see also [V2G20-5012]).

[V2G20-5032] After sending a WPT_PairingReq with EVProcessing set to "Finished", and receiving the next response message with ResponseCode = "OK", the EVCC shall send an AuthorizationSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5033] After receiving a WPT_PairingRes with ResponseCode = "OK" and EVSEProcessing set to "Ongoing", the EVCC shall send a WPT_PairingReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5034] After receiving a WPT_PairingRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send an AuthorizationSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5054] After receiving a WPT_PairingRes with ResponseCode = "WARNING_WPT", and EVSEProcessing set to "Finished", the EVCC shall send a WPT_FinePositioningSetupSetupReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5045] After receiving a ScheduleExchangeRes with ResponseCode = "OK" and EVSEProcessing set to "Finished" the EVCC shall send a WPT_AlignmentCheckReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5062] After receiving a WPT_ChargeParameterDiscoveryRes with ResponseCode = "WARNING_WPT" the EVCC shall send a WPT_FinePositioningSetupReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5041] If the EVCC is using ServiceName = WPT, after receiving the ServiceSelectionRes with "ResponseCode = OK", the EVCC shall send a WPT_ChargeParameterDiscoveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5035] After receiving a WPT_AlignmentCheckRes with ResponseCode = "OK", and EVSEProcessing set to "Ongoing", the EVCC shall send a WPT_AlignmentCheckReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5057] After receiving a WPT_AlignmentCheckRes with ResponseCode = "WARNING_WPT", and EVSEProcessing set to "Finished", the EVCC shall send a WPT_FinePositioningSetupReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5036] After sending a WPT_AlignmentCheckReq with EVProcessing set to "Finished", and received the next response message with "ResponseCode = OK", the EVCC shall send a PowerDeliveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5037] If EVCC uses ServiceName = WPT from Table 204, after receiving the PowerDeliveryRes with "ResponseCode = OK", the EVCC shall send an WPT_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218 to start the energy transfer.