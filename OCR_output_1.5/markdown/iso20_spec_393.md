- entry condition: PowerDeliveryRes message with parameter ResponseCode equal to OK after PowerDeliveryReq with ChargeProgress equals "Start";

- exit condition: PowerDeliveryRes with parameter ResponseCode equal to OK after PowerDeliveryReq with ChargeProgress equals "Stop".

Besides the requirements for request-response message pairs and request-response message sequences as defined in 8.6.4, the EVCC and the SECC shall conform to the requirements as defined in 8.5.6.2, 8.5.6.3, and 8.5.6.4.

##### 8.5.6.2 Common requirements for AC and DC

The following requirements apply for the EVCC.

[V2G20-1615] The EVCC shall use the message PowerDeliveryReq with parameter ChargeProgress set to "Start" to start HLC-C based energy transfer.

[V2G20-1616] If [V2G20-1615] applies and the PowerDeliveryRes message has been received with ResponseCode set to OK, the EV shall apply the energy transfer limits according to the V2G messaging.

[V2G20-1310] The EV shall stop the energy transfer (no current drawn by EV) before sending the message PowerDeliveryReq with the parameter ChargeProgress set to "Stop".

[V2G20-1311] The EVCC shall use the message PowerDeliveryReq with parameter ChargeProgress set to "Stop" to stop HLC-C based energy transfer.

In general, the ISO 15118 series is based on the requirements as defined in IEC 61851-1.

[V2G20-843] An ISO 15118-enabled EV shall conform to IEC 61851-1.

[V2G20-731] If [V2G20-1463] applies, the EVCC can establish a new or resumed V2G communication session by applying [V2G20-014].

[V2G20-2200] If [V2G20-728] applies, the EVCC can establish a new V2G communication session by applying [V2G20-014].

Since the V2G session was terminated due to an error, the EVCC has to mitigate the conditions that resulted in the error before establishing a new V2G communication session.

The following requirements apply for the SECC.

[V2G20-1404] ISO 15118-enabled EVSE shall conform to IEC 61851-1.

[V2G20-2030] If [V2G20-1632] applies, the SECC shall be allowed to establish a new or resumed V2G communication session by applying [V2G20-027].

[V2G20-2115] At the point in time when requesting pause by setting the parameter EVSENotification to "Pause" in dynamic control mode, the SECC shall ensure that the applied power level is equal to 0 kW (no current drawn by EV or EVSE).

The following applies for the EVCC during a standby period.

[V2G20-1390] When the EVCC wants to enter a standby period, after having received the ScheduleExchangeRes with parameter "EVSEProcessing" set to "Finished", the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Standby",

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.