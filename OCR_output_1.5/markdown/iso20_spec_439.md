V2G_SECC_Msg_Performance_Time according to Table 196, if the charge parameter discovery process is finished. The next allowed request shall be ACDP_ConnectReq if  $ ServiceName = DC\_ACDP $, in Table 204 was selected. The V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4071] If SECC is using ServiceName = DC_ACDP, after receiving the ACDP_ConnectReq, the SECC shall respond with a ACDP_ConnectRes with EVSEProcessing set to "Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 215 while the device connection is still ongoing. The next allowed request shall be ACDP_ConnectReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4072] If SECC is using ServiceName = DC_ACDP, after receiving the ACDP_ConnectReq, the SECC shall respond with a ACDP_ConnectRes with EVSEProcessing set to "Finished" within V2G_SECC_Msg_Performance_Time according to Table 215, when the device connection has finished. The next allowed request shall be DC_CableCheckReq if ServiceName = DC_ACDP or DC_ACDP_BPT in Table 204 was selected and the V2G_SECC_Sequence_Timeout is set according to Table 215.

NOTE 3 The following DC requirements apply [V2G20-2003], [V2G20-2004], [V2G20-2005], [V2G20-2006], [V2G20-2007] (common), [V2G20-2008] (common), [V2G20-2013] and [V2G20-919].

NOTE 4 The general requirement [V2G20-1959] applies for an EVSE initiated stop.

[V2G20-4073] If SECC is using ServiceName = DC_ACDP in Table 204, after receiving the PowerDeliveryReq with ChargeProgress set to "Stop", the SECC shall respond with PowerDeliveryRes containing "ResponseCode=OK" within V2G_SECC_Msg_Performance_Time according to Table 215. The allowed next request shall be ACDP_DisconnectReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4074] After receiving the ACDP_DisconnectReq, the SECC shall respond with ACDP_DisconnectRes containing "ResponseCode = OK" and "EVSEProcessing=Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 215, if the processing of the information is successfully passed and the ACDP_Disconnect is ongoing. The allowed next request shall be ACDP_DisconnectReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-4075] After receiving the ACDP_DisconnectReq, the SECC shall respond with ACDP_DisconnectRes containing "ResponseCode = OK" and "EVSEProcessing=Finished" within V2G_SECC_Msg_Performance_Time according to Table 215, if the charging device is in the home position as defined in IEC 61851-23-1. The allowed next request shall be SessionStopReq and V2G_SECC_Sequence_Timeout is set according to Table 215.

NOTE 5 The common requirements [V2G20-1632] and [V2G20-1633] apply.

#### 8.6.5 Multiplexed communication

Besides the regular main stream message flow with EXI encoded V2GTP payload types in the range 0x8001 up to 0x80FF, a multiplexed communication is enabled by making use of other V2GTP payload types (schedule renegotiation V2G messages, ACDP_SystemStatus messages, MeteringConfirmation Messages, ParkingStatus messages (see Table 14)). This subclause refers to communication using EXI encoded messages with V2GTP payload type in the range 0x8101 up to 0x81FF as the side stream.