NOTE 3 The ISO 15118 series does not require a specific implementation for controlling the contactor in an EVSE. Control of the power contactor depends on the EVSE architecture.

##### 8.5.6.4 DC specific requirements

The following requirements apply for the EVCC.

[V2G20-912] After receiving a ScheduleExchangeRes with EVSEProcessing set to "Finished" and before sending a DC_CableCheckReq message, the EVCC shall change to CP State C or D as defined in IEC 61851-1.

[V2G20-913] After sending a PowerDeliveryReq message with ChargeProgress equal to "Stop" and receiving the corresponding PowerDeliveryRes message, the EVCC shall change to CP State B as defined in IEC 61851-1 before sending the next request message.

[V2G20-914] If [V2G20-912] applies and no error has been identified, the EVCC shall not change the CP State until [V2G20-913] applies.

The following applies for the EVCC during a standby period.

[V2G20-1380] When the EVCC wants to enter a standby period, after having received DC_PreChargeRes with ResponseCode equal to "OK" and if the EVCC determines that the EVSE output voltage, as measured inside the EV, has sufficiently been adjusted to the EV RESS voltage, the EVCC shall send a PowerDeliveryReq with ChargeProgress equal to "Standby, while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-2119] After receiving a PowerDeliveryRes with ResponseCode equal to "OK" as a response to the previous PowerDeliveryReq message with ChargeProgress equal to "Standby", and if EVCC selected the service parameter MobilityNeedsMode set to 2, the EVCC shall process the elements TargetSOC, MinimumSOC, DepartureTime and AckMaxDelay in the DC_ChargeLoopRes messages.

[V2G20-1381] When the EVCC wants to enter a standby period, after having received DC_ChargeLoopRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress equal to "Standby", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-1383] When the EVCC wants to exit a standby period, after having received DC_ChargeLoopRes, the EVCC shall send a PowerDeliveryReq while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time according to Table 215.

NOTE The SECC handles the DC_PreChargeReq as described in [V2G20-858], [V2G20-861], [V2G20-862].

The following requirements apply for the SECC.

[V2G20-1408] The SECC shall apply a CP duty cycle of 5% from start of data link setup until end of V2G communication session.

The SECC waits for positive authorization and availability of energy before entering the charging loop.

[V2G20-916] After receiving a DC_CableCheckReq message, the SECC shall monitor the CP State and start the V2G_SECC_Msg_Performance_Timer.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.