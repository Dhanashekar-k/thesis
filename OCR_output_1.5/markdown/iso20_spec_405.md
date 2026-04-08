PowerDeliveryReq message violates a power limitation provided in ScheduleExchangeRes.

[V2G20-479] The message "PowerDeliveryRes" shall contain the ResponseCode "FAILED_TariffSelectionInvalid" if the content of element "EVPowerProfile" in the PowerDeliveryReq message contains a SelectedScheduleTupleID which was not contained in the "ScheduleList" element provided in ScheduleExchangeRes.

[V2G20-1411] The message "PowerDeliveryRes" shall contain the ResponseCode "FAILED_PowerDeliveryNotApplied" if the EVSE is not able to deliver energy.

[V2G20-1944] The message PowerDeliveryRes shall contain the ResponseCode "OK_PowerToleranceConfirmed" if the EVCC has sent a PowerDeliveryReq containing the parameter PowerToleranceAcceptance with the value set to "PowerToleranceConfirmed".

[V2G20-1945] The message PowerDeliveryRes shall contain the ResponseCode "FAILED_PowerToleranceNotConfirmed" if the EVCC has sent a PowerDeliveryReq containing the parameter PowerToleranceAcceptance with the value set to "PowerToleranceNotConfirmed" and based on this the SECC intends to stop the V2G communication session, according to [V2G20-1402].

[V2G20-1946] The message PowerDeliveryRes shall contain the ResponseCode "WARNING_PowerToleranceNotConfirmed" if the EVCC has sent a PowerDeliveryReq containing the parameter PowerToleranceAcceptance with the value set to "PowerToleranceNotConfirmed" and based on this the SECC intends to initiate a schedule renegotiation according to [V2G20-1601].

[V2G20-1953] The EVCC shall interpret the response code "WARNING_EVPowerProfileViolation" as Information that the EVSE has detected an immediate unacceptable deviation from the EVPowerProfile. The EV is expected to correct the power transfer within the timing limitations according to [V2G20-1865] or the V2G communication session will be terminated accordingly.

NOTE 8 The response code "WARNING_EVPowerProfileViolation" is sent continuously by the SECC as long as an immediate unacceptable deviation from the EVPowerProfile is detected. However, the timing requirements as specified in [V2G20-1865] are always considered based on the first SECC sent "WARNING_EVPowerProfileViolation" response code in a sequence.

[V2G20-1954] If the response code "WARNING_PowerToleranceNotConfirmed" has been sent, and EVSENotification in EVSEStatus has been set to "ScheduleRenegotiation" in the latest PowerDeliveryRes message the EVCC shall initiate a schedule renegotiation.

[V2G20-1955] The message "SessionStopRes" shall contain the ResponseCode "FAILED_NoServiceRenegotiationSupported" if a SessionStopReq with ChargingSession set to "ServiceRenegotiation" is received, and the first ServiceDiscoveryRes message of the service session had the ServiceRenegotiationSupported set to "False".

[V2G20-1956] The message "ServiceSelectionRes" shall contain the ResponseCode "FAILED_NoServiceRenegotiationSupported" if the first ServiceDiscoveryRes message of the service session had the ServiceRenegotiationSupported set to "False" and the EVCC, after waking up from a Pause, is selecting a different set of ServiceIDs or ParameterSetIDs from the first ServiceSelectionReq of the service session.