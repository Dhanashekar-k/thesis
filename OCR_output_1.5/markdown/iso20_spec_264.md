NOTE 2 The EVCC assumes that the hard capability limits communicated in an EVSEMaximumChargePower [L2,L3] value always will overrule any matching values provided within a PowerSchedule.

[V2G20-1012] If a secondary actor provided a PowerSchedule for discharging, the SECC shall ensure that no Power value within the PowerSchedule exceeds the matching EVSEMaximumDischargePower limit.

NOTE 3 The EVCC assumes that the hard capability limits communicated in an EVSEMaximumDischargePower[_L2,L3] value always will overrule any matching values provided within a PowerDischargeSchedule.

[V2G20-1562] The sum of the individual time intervals described in the PowerSchedule and PowerSchedule for Discharge (refer to 8.3.5.3.19) and PriceSchedule provided in the ScheduleExchangeRes message should match the period of time indicated by the EVCC in the message element DepartureTime of the ScheduleExchangeReq message.

[V2G20-1563] If the EVCC did not provide a DepartureTime Target Setting (refer to 8.3.4.4.2.2 and 8.3.5.4.1) in the ScheduleExchangeReq message, the sum of the individual time intervals described in the PowerSchedule and PriceSchedule provided in the ScheduleExchangeRes message, shall be greater or equal to 24 h.

[V2G20-1564] If the PriceSchedule or PowerSchedule provided by the secondary actor(s) are not covering the entire period of time until DepartureTime, the target setting EVTargetEnergyRequest (refer to 8.3.4.4.2.2 and 8.3.5.4.1) has not been met and the communication session has not been finished, it is the responsibility of the EVCC to request a new ScheduleTuple as soon as the last element of PowerSchedule or PriceSchedule becomes active by triggering a schedule renegotiation.

NOTE 4 The EVCC can request an update of tariff information by applying the schedule renegotiation process at any time during the charging loop.

[V2G20-1565] If the number of PriceSchedule elements provided by the secondary actor is not covering the entire time period until the EV has reached its mobility needs, it is in the responsibility of the EVCC to optimize the schedule based on the available information.

NOTE 5 The algorithm for optimizing the energy transfer profile is out of the scope of this document.

NOTE 6 Independent of the selected authorization mode of PnC or EIM, the secondary actor can decide to sign the PriceSchedule. This is not mandatory, as security is expected to provide through the CSMS, CSO, and EVSE trust chain. It is not in the scope of this document whether signing a PriceSchedule and/or validating an attached signature is mandatory or not. This can be defined by the legislative or other entities.

[V2G20-1567] The SECC shall not change the signature attached to the PriceSchedule, when receiving a signed PriceSchedule from a secondary actor.

NOTE 7 This presumes that the data structure used by the secondary actor for the provisioning of the PriceSchedule is identical with the data structure defined in this document.

[V2G20-2130] If the SA provided a PriceSchedule along with a signature, the SECC shall include the PriceSchedule along with the signature in the ScheduleExchangeRes.

[V2G20-1568] If the PriceSchedule is signed, it shall be signed by the same private key that was used to issue the leaf contract certificate that the EVCC used during this V2G communication session during the Authorization phase.