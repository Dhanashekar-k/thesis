[V2G20-1621] If the parameter EVSENotification in EVSEStatus is equal to MeteringConfirmation, the EVCC shall send a MeteringConfirmationReq using the multiplexed communication within the number of seconds provided in NotificationMaxDelay.

[V2G20-1622] The parameter EVSENotification in EVSEStatus shall only use MeteringConfirmation after the exchange of the first ChargeLoop Messages.

[V2G20-1850] In the case the SECC wants to initiate a pause, it shall trigger the EVCC via EVSEStatus Parameter EVSENotification set to "Pause" and NotificationMaxDelay set to 60s. The EVCC shall then either initiate a pause period according to [V2G20-1540] or enter a standby period according to [V2G20-1380], [V2G20-1381], and [V2G20-1394].

[V2G20-1854] In the case the SECC wants to exit a standby period, it shall trigger the EVCC via EVSEStatus Parameter EVSENotification set to "ExitStandby". The EVCC shall then exit a standby period according to [V2G20-1393], [V2G20-1383] and [V2G20-1395].

[V2G20-1959] The EVSE shall set EVSENotification to "Terminate" while decreasing the power at the same time, if it wants to stop charging in dynamic control mode.

[V2G20-1960] If the parameter EVSENotification in EVSEStatus is equal to "Terminate", the EVC shall initiate a shutdown sequence and finally send a SessionStopReq with ChargingSession set to "Terminate".

[V2G20-1698] In case the SECC wants to end the service session, the SECC shall notify the EVCC by setting EVSENotification in EVSEStatus to "Terminate."

[V2G20-2644] If the EVCC wishes to stop the session for a non-critical reason (e.g. user interaction, errors which are not emergency related) after having sent a SessionSetupReq message and before having sent a PowerDeliveryReq message with ChargeProgress = "Start", the EVCC shall send a SessionStopReq message with parameter "ChargingSession" set to "Terminate" and the optional EVTerminationCode within V2G_EVCC_Sequence_Performance_Timeout according to Table 215, if not otherwise specified within this document. It shall then wait for a SessionStopRes message and proceed according to [V2G20-1463], [V2G20-728] and [V2G20-025] afterwards.

[V2G20-2645] In case the SECC receives a SessionStopReq after having sent a SessionSetupRes message and before having received a PowerDeliveryReq message with ChargeProgress = "Start", the SECC shall proceed according to [V2G20-1632] and [V2G20-1633].

##### 8.6.4.2 AC requirements

[V2G20-1961] For AC charging with WiFi communication only WiFi communication will be used even when there is PLC available.

[V2G20-1964] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "True" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" in AC_ChargeLoopRes, the EVCC shall initiate a ServiceRenegotiation as defined by [V2G20-1969] within the number of seconds provided in NotificationMaxDelay.

[V2G20-1965] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "False" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" in AC_ChargeLoopRes, the EVC shall not initiate a ServiceRenegotiation.