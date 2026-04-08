[V2G20-1979] After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode set to "OK" within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has completed successfully and the received contractcertificate will expire in more than 14 days. The next allowed request shall be ServiceDiscoveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-2234] After receiving the AuthorizationReq with SelectedAuthorizationService set to "EIM", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode starting with "OK" within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has completed successfully. The next allowed request shall be ServiceDiscoveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1980] After receiving the ServiceDiscoveryReq, the SECC shall respond with a ServiceDiscoveryRes within V2G_SECC_Msg_Performance_Time according to Table 215, the allowed next request shall be ServiceDetailReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1957] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "False" and, after waking up from a Pause, if the SECC does not offer the same ServiceIDs and parameterSetIDs that were selected previously by the EV, then EVCC shall stop the session by sending the message SessionStopReq with parameter ChargingSession equal to "Terminate".

[V2G20-1981] After receiving the ServiceDetailReq the SECC shall respond with a ServiceDetailRes within V2G_SECC_Msg_Performance_Time according to Table 215. The allowed next requests shall be either ServiceDetailReq or ServiceSelectionReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1983] After receiving the ServiceSelectionReq, the SECC shall respond with ServiceSelectionRes within V2G_SECC_Msg_Performance_Time according to Table 215.

[V2G20-1984] After sending the ServiceSelectionRes with ResponseCode = "OK", the SECC shall be ready to offer any of the value added services it may support, i.e. Internet_Service, ParkingStatus_Service, and/or ACDP_SystemStatus_Service as listed in Table 204.

[V2G20-1985] After receiving the ServiceSelectionReq, if there are already existing services, i.e. Internet_Service, ParkingStatus_Service, and/or ACDP_SystemStatus_Service as listed in Table 204 which have not been stopped earlier, these services shall be stopped.

[V2G20-1986] After receiving the ScheduleExchangeReq, the SECC shall respond with a ScheduleExchangeRes with EVSEProcessing set to "Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 215, while the process is still ongoing. The next allowed request shall be ScheduleExchangeReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1987] After receiving the ScheduleExchangeReq, the SECC shall respond with a ScheduleExchangeRes with EVSEProcessing set to "Finished" and ResponseCode starting with "OK" within V2G_SECC_Msg_Performance_Time according to Table 215, if all parameters are available.