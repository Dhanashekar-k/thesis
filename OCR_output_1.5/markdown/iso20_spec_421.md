[V2G20-1434] After receiving the DC_PreChargeRes with "ResponseCode = OK", the EVCC shall send a DC_PreChargeReq with EVProcessing set to "Finished" within V2G_EVCC_Sequence_Performance_Timeout according to Table 217 when the precharge process is finished.

[V2G20-1435] After receiving the DC_PreChargeRes message with "ResponseCode = OK", the EVCC shall send a PowerDeliveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1438] If EVCC uses ServiceName = DC or DC_BPT from Table 204, after receiving the PowerDeliveryRes with "ResponseCode = OK" or "ResponseCode = WARNING_PowerToleranceNotConfirmed", the EVCC shall send a DC_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217 to start the energy transfer, a schedule renegotiation or enter a standby period.

During standby both EV and EVSE contactors are to stay closed. The standby concept is solely used as communication state within this document and therefore is not reflected in related documents, e.g. IEC 61851-1 or IEC 61851-23.

[V2G20-1441] If the EVCC wants to continue the energy transfer and received the DC_ChargeLoopRes with "ResponseCode = OK", the EVCC shall send another DC_ChargeLoopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217.

[V2G20-1444] If the EVCC wants to stop the energy transfer and received the DC_ChargeLoopRes with "ResponseCode = OK", the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Stop" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-2195] If the EVCC wants to enter a standby phase and received the DC_ChargeLoopRes with "ResponseCode = OK", the EVCC shall send a PowerDeliveryReq with ChargeProgress = "Standby" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1448] If the EVCC is using ServiceName = DC or DC_BPT in Table 204, after receiving the PowerDeliveryRes with "ResponseCode = OK" and if the previous PowerDeliveryReq message has ChargeProgress = "Stop", the EVCC shall send a DC_WeldingDetectionReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 217.

[V2G20-1573] After receiving the DC_WeldingDetectionRes with "ResponseCode = OK", the EVCC shall send a DC_WeldingDetectionReq with EVProcessing set to "Ongoing" within V2G_EVCC_Sequence_Performance_Timeout according to Table 217 while the welding detection process is not finished.

[V2G20-1461] After receiving the DC_WeldingDetectionRes with "ResponseCode = OK", the EVCC shall send a DC_WeldingDetectionReq with EVProcessing set to "Finished" within V2G_EVCC_Sequence_Performance_Timeout according to Table 217 when the welding detection process is finished.

[V2G20-1462] After receiving the DC_WeldingDetectionRes message with "ResponseCode = OK", the EVCC shall send a SessionStopReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.