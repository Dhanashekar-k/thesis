[V2G20-1617] The EVCC shall signal CP State B before sending the first PowerDeliveryReq with ChargeProgress equals "Start" within V2G communication session.

[V2G20-847] The EVCC shall signal CP State C or D no later than 250 ms after sending the first PowerDeliveryReq with ChargeProgress equals "Start" within V2G communication session.

[V2G20-848] The EVCC shall signal CP State B no later than 250 ms after sending PowerDeliveryReq with ChargeProgress equals "Stop".

[V2G20-849] If [V2G20-847] applies and no error has been identified, the EVCC shall not change the CP State until [V2G20-848] applies.

The following applies for the EVCC during a standby period.

NOTE 2 In case of schedule renegotiation, the contactor stays closed to allow energy transfer based on the existing energy transfer limits during schedule renegotiation.

[V2G20-2120] After receiving a PowerDeliveryRes with ResponseCode equal to "OK" as a response to the previous PowerDeliveryReq message with ChargeProgress equal to "Standby", and if EVCC selected the service parameter MobilityNeedsMode set to 2, the EVCC shall process the elements TargetSOC, MinimumSOC, DepartureTime and AckMaxDelay in the AC_ChargeLoopRes messages.

The following requirements apply for the SECC supply equipment. The SECC contactor is closed before sending the PowerDeliverRes message.

[V2G20-858] After receiving a PowerDeliveryReq with parameter ChargeProgress equal to "Start" the SECC shall monitor the Contactor status and start the V2G_SECC_Msg_Performance_Timer.

[V2G20-1317] In case of High-level communication based energy transfer, the SECC shall not close the Contactor before receiving PowerDeliveryReq(ChargeProgress = Start).

[V2G20-860] If no error is detected, the SECC shall close the Contactor no later than 3s after measuring CP State C or D.

[V2G20-861] The SECC shall respond with PowerDeliveryRes containing "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 215, if the SECC measures a closed Contactor and [V2G20-858] has applied before.

[V2G20-862] The SECC shall respond with PowerDeliveryRes containing "ResponseCode = FAILED_ContactorError" if V2G_SECC_Msg_Timer is equal or larger than V2G_SECC_Msg_Performance of "PowerDelivery" according to Table 215 and SECC measures opened Contactor.

[V2G20-863] After receiving a PowerDeliveryReq with parameter ChargeProgress equal to "Stop", the SECC shall monitor the Contactor status and start the V2G_SECC_Msg_Performance_Timer.

[V2G20-864] The SECC shall respond with PowerDeliveryRes containing "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 215, if the SECC measures an open Contactor and [V2G20-863] has applied before.