[V2G20-5061] If EVCC uses ServiceName = WPT from Table 204, after receiving the PowerDeliveryRes with "ResponseCode = WARNING_WPT", the EVCC shall send a WPT_FinePositioningSetupReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5058] After receiving a WPT_ChargeLoopRes with "ResponseCode = WARNING_WPT", the EVCC shall send a WPT_AlignmentCheckReq or a WPT_PairingReq or terminate by sending a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5039] If the EVCC wants to continue the energy transfer and received the WPT_ChargeLoopRes with "ResponseCode = OK", the EVCC shall send another WPT_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 218.

[V2G20-5082] If the EVCC wants to stop the energy transfer and received the WPT_ChargeLoopRes with "ResponseCode = OK" the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Stop" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5129] If the EVCC wants to enter a standby phase and received the WPT_ChargeLoopRes with "ResponseCode = OK" the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Standby" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-5040] If EVCC is using ServiceName = WPT in Table 204, after receiving the PowerDeliveryRes with "ResponseCode = OK", and if the previous PowerDeliveryReq message has ChargeProgress = "Stop", the EVCC shall send a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

8.6.4.5.3.5 ACDP message flow

[V2G20-4045] The following requirement is not applicable when using ServiceName = DC_ACDP: [V2G20-1446].

NOTE 1 The common requirements [V2G20-1746] and [V2G20-1747] apply.

[V2G20-4046] If the EVCC is using WLAN, after receiving the SessionSetupRes with "ResponseCode = OK", the EVCC shall send a ACDP_VehiclePositioningReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-4047] After receiving the ACDP_VehiclePositioningRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send another ACDP_VehiclePositioningReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-4048] When the EV has determined that it is sufficiently well positioned to meet the requirement 201.1 of IEC 61851-23, and is immobilized, the EVCC shall send a ACDP_VehiclePositioningReq with EVMobilityStatus set to "EV is immobilized", within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-4049] After receiving the ACDP_VehiclePositioningRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send an AuthorizationSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.