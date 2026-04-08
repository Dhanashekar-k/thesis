a ServiceSelectionReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1590] After receiving the ServiceSelectionRes with "ResponseCode = OK", the EVCC shall send a ChargeParameterDiscoveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1591] After receiving the ServiceSelectionRes with "ResponseCode = OK", the EVCC may start Internet_Service or ParkingStatus_Service as listed in Table 204.

[V2G20-1592] After receiving the ServiceSelectionRes with "ResponseCode = OK", if there are already existing services, i.e. Internet_Service or ParkingStatus_Service as listed in Table 204, which have not been stopped earlier, these services shall be stopped.

[V2G20-2658] After receiving the ChargeParameterDiscoveryReq, the SECC shall send an ChargeParameterDiscoveryRes within V2G_SECC_Msg_Performance_Time according to Table 215. The next allowed request shall be ScheduleExchangeReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-2659] After receiving the ChargeParameterDiscoveryRes with "ResponseCode = OK", the EVCC shall send a ScheduleExchangeReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1593] After receiving the ScheduleExchangeRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send another ScheduleExchangeReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1436] If the EVCC is not finished calculating the EVPowerProfile, the EVCC shall send a PowerDeliveryReq with EVProcessing set to "Ongoing" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1446] After receiving the PowerDeliveryRes with "ResponseCode = OK" and if the previous PowerDeliveryReq message has ChargeProgress = "Stop", the EVCC shall stop all multiplexed communication.

[V2G20-1463] After receiving the SessionStopRes with "ResponseCode = OK", the EVCC shall terminate the communication according to 7.4.

[V2G20-728] After the EVCC stopped the V2G communication session with an error it shall terminate the communication by applying [V2G20-025].

[V2G20-1610] After receiving a response message from the SECC with EVSENotification set to "Terminate" and the corresponding duration of the NotificationMaxDelay has elapsed, the EVCC shall send a SessionStopReq with parameter "ChargingSession" set to "Terminate" while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-1476] If the first ServiceDiscoveryRes of the service session had the parameter ServiceRenegotiationSupported set to "True" and the EVCC decided to perform a ServiceRenegotiation, the EVCC shall send a SessionStopReq with ChargingSession set to "ServiceRenegotiation".

[V2G20-1477] If the last SessionStopReq in the sequence had ChargingSession set to "ServiceRenegotiation", after receiving the SessionStopRes with ResponseCode set to