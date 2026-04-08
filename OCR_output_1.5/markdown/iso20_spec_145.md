NOTE 5 From first authorization until termination of the V2G communication session or physical plug out - CP state changes B to A for conductive charging

NOTE 6 For EIM the relevant authorization data of the SECC is the authorization status. For PnC the relevant authorization data of an EVCC includes the credentials of the TLS sessions including VAS, and the relevant authorization data of an SECC includes the credentials of the TLS sessions including VAS, the certificate chains received from the EV, validation and revocation check results of those certificates, and the authorization status.

###### 8.3.4.1.3 V2G session pausing

[V2G20-1540] If an EVCC wants to pause an active V2G communication session, it shall do so by sending PowerDeliveryReq with ChargeProgress set to "Stop" followed by SessionStopReq message with the parameter ChargingSession set to value "Pause".

[V2G20-1839] In scheduled control mode, any pause period initiated by the EVCC shall be indicated as zero power period in the currently applied EVPowerProfile, sent in the latest PowerDeliveryReq with ChargeProgress set to "Start", "Standby", "Stop" or "Pause".

A "zero power" period in an EVPowerProfile does not require a standby to be initiated. Only if a standby is requested by the EVCC shall the applied EVPowerProfile indicate this accordingly.

[V2G20-1197] At the point in time when entering pause by SessionStopReq with ChargingSession=Pause in Scheduled control mode, the EVCC shall ensure that the applied EVPowerProfileEntry is equal to 0kW.

[V2G20-1061] In scheduled control mode, any pause period initiated by the SECC shall be indicated as zero power period in the currently applied EVPowerProfile, sent in the latest PowerDeliveryReq with Charge progress set to "Start", "Standby", "Stop" or "Pause".

A "zero power" period in an EVPowerProfile does not require a pause to be initiated. Only if a pause is requested by the SECC shall the applied EVPowerProfile indicate this accordingly.

It is not recommended for the SECC to request a pause for short time periods of zero power transfer. In case the SECC requests the EVCC to enter a pause, the EVCC can alternatively enter a StandbyPeriod according to [V2G20-1850].

[V2G20-1198] At the point in time when requesting pause by setting the parameter EVSENotification to Pause in scheduled control mode, the SECC shall ensure that the applied EVPowerProfileEntry is equal to 0kW.

[V2G20-1842] In dynamic control mode, the EVCC shall only request a pause period if triggered by the SECC according to [V2G20-1850].

NOTE 1 In dynamic control mode the SECC needs to dynamically adjust the power profile based on grid demands, etc. A pause initiated by the EVCC contradicts the intent of dynamic control mode where the SECC controls the power profile, not the EVCC.

[V2G20-4002] If SECC is using ServiceName = DC_ACDP, in the case the SECC wants to perform a pause period, it shall trigger the EVCC via EVSEStatus Parameter EVSENotification set to "Pause". The EVCC shall then initiate a pause period according to [V2G20-4001].

[V2G20-2071] After pausing the V2G session, the EVCC shall terminate the TLS connection associated with the V2G session.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.