During standby both EV and EVSE contactors are to stay closed. The standby concept is solely used as communication state within this document and therefore is not reflected in related documents, e.g. IEC 61851-1 or IEC 61851-23.

[V2G20-1386] The SECC shall exit standby, after having received PowerDeliveryReq with ChargeProgress set to "Start", "Stop", or "Renegotiate", by sending a PowerDeliveryRes with ResponseCode set to "OK", while V2G_SECC_Sequence_Timer is smaller than V2G_SECC_Sequence_Timeout.

[V2G20-1700] The message PowerDeliveryRes shall contain the ResponseCode "WARNING_StandbyNotAllowed" if the EVCC has sent a PowerDeliveryReq containing the parameter ChargeProgress set to "Standby" and the SECC does not allow for a standby period. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message.

The following applies if the EVCC is unable to enter a standby period.

[V2G20-1396] After receiving the message "PowerDeliveryRes" with ResponseCode equal to "WARNING_StandbyNotAllowed", the EVCC shall ignore all other parameters of the response message and shall do one (1) of the following.

Proceed with the initially agreed EVPowerProfile or in dynamic control mode follow the demand of the SECC within V2G_EVCC_Sequence_Performance_Timeout according to Table 215. The next allowed message shall be the ChargeLoopReq message. Refer to 8.3.1 and 8.3.4.1 for details of requesting standby of the V2G session.

- Request schedule renegotiation within V2G_EVCC_Sequence_Performance_Timeout according to Table 215. Refer to Annex F for further details.

- Stop the V2G communication according to requirements defined 7.4.

The following applies if the SECC declines a request to enter a standby period from the EVCC.

## [V2G20-1387]

After receiving the PowerDeliveryReq with ChargeProgress set to "Standby", the SECC shall send a PowerDeliveryRes with ResponseCode set to "WARNING_StandbyNotAllowed" while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Timeout, if the SECC does not allow a standby period. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message.

NOTE After declining a standby request from the EVCC, the SECC expects the EVCC to proceed according to [V2G20-1396].

##### 8.5.6.3 AC specific requirements

The following requirements apply for the EVCC.

## [V2G20-930]

The EVCC shall measure a PWM of 5% duty cycle before sending the message ChargeParameterDiscoveryReq.

NOTE 1 In the case of AC energy transfer, the HLC can be started with using a 5 % PWM or a 100 % PWM (static current).

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.