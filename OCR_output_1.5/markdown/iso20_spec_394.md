while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-2113] After receiving the PowerDeliveryRes with ResponseCode equal to "OK" as a response to a previous PowerDeliveryReq message with ChargeProgress equal to "Standby", the EVCC shall send a ChargeLoopReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-2116] At the point in time when requesting standby by PowerDeliveryReq with parameter ChargeProgress="Standby", the EVCC shall ensure that the applied power level is equal to zero kW (no current drawn by EV or EVSE).

[V2G20-2117] After receiving a PowerDeliveryRes with ResponseCode equal to "OK" as a response to the previous PowerDeliveryReq message with ChargeProgress equal to "Standby", the EVCC shall not process any elements in the ChargeLoopRes except EVSEStatus, ResponseCode, MeterInfo and Receipt, until the next PowerDeliveryReq message with ChargeProgress set to "Start", "Stop", or "Renegotiate" is send.

During standby both EV and EVSE contactors are to stay closed. The standby concept is solely used as communication state within this document and therefore is not reflected in related documents, e.g. IEC 61851-1 or IEC 61851-23.

[V2G20-1391] When the EVCC wants to enter a standby period, after having received ChargeLoopRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Standby", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-1393] When the EVCC wants to exit a standby period, after having received ChargeLoopRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Start", "Stop", or "Renegotiate", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-1394] When the EVCC wants to enter a standby period, after having received MeteringConfirmationRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Standby", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-1395] When the EVCC wants to exit a standby period, after having received MeteringConfirmationRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Start", "Stop", or "Renegotiate", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

The following applies for the SECC during a standby period.

[V2G20-1385] The SECC shall enter standby, after having received PowerDeliveryReq with ChargeProgress set to "Standby", by sending a PowerDeliveryRes with ResponseCode is set to "OK" while V2G_SECC_Sequence_Timer is smaller than V2G_SECC_Sequence_Timeout.

[V2G20-2118] After sending a PowerDeliveryRes with ResponseCode equal to "OK" as a response to the previous PowerDeliveryReq message with ChargeProgress equal to "Standby", the SECC shall not process any elements in the ChargeLoopReq except MeterInfoRequested and DisplayParameters, until the next PowerDeliveryReq message with ChargeProgress set to "Start", "Stop", or "Renegotiate" is received.