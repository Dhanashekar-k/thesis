NOTE 2 The common requirements [V2G20-1577], [V2G20-1576], [V2G20-1580], [V2G20-1581], [V2G20-1578], [V2G20-1579], [V2G20-1582], [V2G20-1583], [V2G20-1584], [V2G20-1585], [V2G20-1586], [V2G20-1587], [V2G20-1590] and [V2G20-1593] apply.

[V2G20-4050] If EVCC is using ServiceName = DC_ACDP, in Table 204, after receiving the ScheduleExchangeRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send a ACDP_ConnectReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-4051] If EVCC is using ServiceName = DC_ACDP, after receiving the ACDP_ConnectRes with "ResponseCode = OK" and EVSEProcessing set to "Ongoing", the EVCC shall send another ACDP_ConnectReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-4052] If EVCC is using ServiceName = DC_ACDP, after receiving the ACDP_ConnectRes with "ResponseCode = OK", and EVSEProcessing set to "Finished", the EVCC shall send a DC_CableCheckReq if ServiceName = DC_ACDP or DC_ACDP_BPT in Table 204 was selected within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

NOTE 3 The DC requirements [V2G20-1431], [V2G20-1432], [V2G20-1433], [V2G20-1434], [V2G20-1435], [V2G20-1436], [V2G20-1438], [V2G20-1441], [V2G20-1444] and [V2G20-913] apply.

NOTE 4 The general requirement [V2G20-1416] applies for an EVSE initiated stop.

When the EV intends to stop the charge session it is recommended to request 0A in the DC_ChargeLoopReq, to allow the EVSE to ramp down the current with the minimum rate of 100A/s (as defined in IEC 61851-23).

[V2G20-4053] If EVCC is using ServiceName = DC_ACDP in Table 204, after receiving the PowerDeliveryRes as a response to a previous PowerDeliveryReq message with ChargeProgress equal to "Stop", the EVCC shall send a ACDP_DisconnectReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-4054] After receiving the ACDP_DisconnectRes with ResponseCode = "OK" and "EVSEProcessing = Ongoing", the EVCC shall send a ACDP_DisconnectReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-4055] After receiving the ACDP_DisconnectRes with "ResponseCode = OK" and with parameter "EVSEProcessing" set to "Finished", the EVCC shall send a SessionStopReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-4056] If EVCC is using ServiceName = DC_ACDP after receiving the SessionStopRes with "ResponseCode = OK" the EVCC shall stop all multiplexed communication.

NOTE 5 The common requirement [V2G20-1463] applies.

##### 8.6.4.6 SECC

###### 8.6.4.6.1 General

The following clauses contain the SECC behavior, which defines all valid request-response message sequences.

###### 8.6.4.6.2 Error handling

## 420 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.