[V2G20-2007] After receiving the PowerDeliveryReq with EVProcessing set to "Ongoing" and ResponseCode starting with "OK", the SECC shall ignore the other contents of the PowerDeliveryReq and respond with a PowerDeliveryRes within V2G_SECC_Msg_Performance_Time according to Table 215. The next allowed request shall be PowerDeliveryReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-2008] After receiving the PowerDeliveryReq with EVProcessing set to "Finished", the SECC shall respond with a PowerDeliveryRes within V2G_SECC_Msg_Performance_Time according to Table 215.

[V2G20-1601] In case the SECC intends to renegotiate after having received a PowerDeliveryReq with PowerToleranceAcceptance set to "PowerToleranceNotConfirmed", the SECC shall send the response code "WARNING_PowerToleranceNotConfirmed" in PowerDeliveryRes and set EVSENotification in EVSEStatus to "Renegotiation"

NOTE 12 Based on local supply, or other boundary conditions the SECC can renegotiate the applicable power tolerance for a particular charging session.

[V2G20-2018] If the PowerDeliveryReq received has ChargeProgress = "Renegotiate", the SECC shall respond with a PowerDeliveryRes with ResponseCode = "FAILED_SequenceError".

[V2G20-1632] After receiving the SessionStopReq, the SECC shall respond with a SessionStopRes within V2G_SECC_Msg_Performance_Time according to Table 215.

[V2G20-1633] After sending a SessionStopRes, the SECC shall wait at least 5s before closing the TCP connection.

[V2G20-1643] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True", after receiving the SessionStopReq with ChargingSession set to "ServiceRenegotiation" the SECC shall respond with a SessionStopRes with ResponseCode set to "OK" within V2G_SECC_Sequence_Timeout according to Table 215. The next allowed request shall be ServiceDiscoveryReq within V2G_SECC_Sequence_Timeout according to Table 215.

[V2G20-1644] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "False", after waking up from a Pause, the SECC shall only offer the ServiceIDs and ParameterSetIDs that were selected by the EVCC in the first ServiceSelectionReq of the service session.

[V2G20-1645] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True", after waking up from a Pause, the SECC shall offer all available services, independent of what the EVCC selected previously.

Details of "WARNING_StandbyNotAllowed" are provided in 8.5.6.2.

8.6.4.6.3.2 AC message flow

[V2G20-1989] After receiving the ScheduleExchangeReq, the SECC shall respond with a ScheduleExchangeRes with EVSEProcessing set to "Finished" within V2G_SECC_Msg_Performance_Time according to Table 215, if the process is finished. The next allowed request shall be PowerDeliveryReq if ServiceName= AC or AC_BPT in Table 204 was selected. The V2G_SECC_Sequence_Timeout is set according to Table 215.