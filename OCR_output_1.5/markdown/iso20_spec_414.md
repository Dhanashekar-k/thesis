In case of any exception handling the EVCC shall continue the communication to the SECC until the last message pair of the exception handling procedure has been executed.

NOTE 2 The EV initiates an emergency shut down by changing the CP state from C/D to B. The EVSE ramps down the charging current rapidly, opens the DC contactors and raises the pantograph. The EVCC issues the ACDP_Disconnect message then in order to determine the status of the pantograph. After the ACDP_Disconnect response indicates the pantograph being in home position the EVCC issues the SessionStop message to end the process. The ACDP_SystemStatus messages meanwhile unveils the EV causing the emergency shut down, as described in IEC 61851-23.

[V2G20-4027] When EVCC experiences an emergency situation, and EVCC is using ServiceName = DC_ACDP as defined in Table 204 the EVCC shall set CP state to B and start sending ACDP_DisconnectReq.

If the EV detects a situation that requires an emergency termination of the charging process, the EV will use other means to indicate that an emergency shutdown is required, change to CP State B in accordance with IEC 61851-1.

NOTE 3 If the EVSE detects a CP state C to CP state B change, it will execute an emergency shutdown according to IEC 61851-23-1. It can keep communication open to allow the disconnection of the ACDP and to give status information about the ACDP to the EV.

[V2G20-4028] If EVCC is using ServiceName = DC_ACDP in Table 204 and the EVCC measures CP State change from C/D to E or F it shall start sending ACDP_DisconnectReq.

[V2G20-4030] The EVCC shall stop the V2G communication session when "ResponseCode ≠ OK" of "SessionSetupRes".

[V2G20-4031] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send SessionStopReq when the "ResponseCode ≠ OK" of "ACDP_VehiclePositioningRes".

[V2G20-4032] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "ServiceDiscoveryRes".

[V2G20-4033] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "ServiceDetailRes".

[V2G20-4034] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "ServiceSelectionRes".

[V2G20-4035] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "AuthorizationSetupRes".

[V2G20-4036] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq "ResponseCode ≠ OK" of "AuthorizationRes".

[V2G20-4037] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "CertificateInstallationRes".

[V2G20-4038] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of "DC_ChargeParameterDiscoveryRes".

[V2G20-4079] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a SessionStopReq when "ResponseCode ≠ OK" of ScheduleExchangeRes".