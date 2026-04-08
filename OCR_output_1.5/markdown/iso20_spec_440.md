For example, while in the message exchange loop of AC_ChargeLoopReq/Res, if either the EVCC or the SECC would like to change the EVPowerProfile, they can trigger a schedule renegotiation without interruption of the existing energy transfer message exchange. The schedule renegotiation is done in a parallel side stream with V2GTP payload type ScheduleRenegotiationPayloadID. Refer to Annex F for the message sequence on EVCC triggered and SECC triggered schedule renegotiation.

[V2G20-1040] The conditions defined for the CP state and PWM within the message sequence requirements shall only apply to the main stream EXI encoded messages with V2GTP payload types in the range 0x8001 up to 0x80FF.

[V2G20-1041] The timeout of the messages in the side stream shall be independent of the timeout of the messages in the main stream.

[V2G20-1042] All timeout requirements that apply for the main stream shall be accordingly applied for the side stream messages.

##### 8.6.5.1 Schedule Renegotiation

[V2G20-1043] If SessionStopRes with ResponseCode set to "OK" is encountered, then all communication shall terminate.

[V2G20-1045] For all schedule renegotiation related messages, V2GTP payload type ScheduleRenegotiationPayloadID shall be applied.

The following requirements apply to EVCC triggered schedule renegotiation.

[V2G20-1046] The EVCC shall use the message ChargeParameterDiscoveryReq on V2GTP payload type ScheduleRenegotiationPayloadID as the first message of a schedule renegotiation message flow.

[V2G20-1846] The EVCC shall send ChargeParameterDiscoveryReq on V2GTP payload type ScheduleRenegotiationPayloadID only after having sent at least one ChargeLoopReq message depending on the selected energy transfer services.

[V2G20-1047] The SECC shall respond to the ChargeParameterDiscoveryReq with ChargeParameterDiscoveryRes on V2GTP payload type ScheduleRenegotiationPayloadID V2G messages.

[V2G20-1048] After receiving the ChargeParameterDiscoveryRes, the EVCC shall send a ScheduleExchangeReq on V2GTP payload type ScheduleRenegotiationPayloadID.

[V2G20-2316] If the SECC needs more time to provide the PowerSchedule and optionally a PriceSchedule, the SECC shall respond to the ScheduleExchangeReq with ScheduleExchangeRes with EVSEProcessing set to "Ongoing" on V2GTP payload type ScheduleRenegotiationPayloadID.

[V2G20-2713] If the SECC is ready to provide the PowerSchedule and optionally a PriceSchedule, the SECC shall respond to the ScheduleExchangeReq with ScheduleExchangeRes with EVSEProcessing set to "Finished" on V2GTP payload type ScheduleRenegotiationPayloadID.

[V2G20-2714] After receiving the ScheduleExchangeRes with EVSEProcessing set to "Ongoing", the EVCC shall send another unaltered ScheduleExchangeReq on V2GTP payload type ScheduleRenegotiationPayloadID.