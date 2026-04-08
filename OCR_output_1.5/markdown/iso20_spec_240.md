– EVSEEmergencyShutdown = False;

– EVSEMalfunction = False;

– EVInChargePosition = True;

EVAssociationStatus = True.

In the usual case of a normal shut down due to the driver’s-initiated end of the charging by releasing the hand brake the EVTechnicalStatus will look like:

– EVReadyToCharge = False;

– EVImmobilizationRequest = False;

- EVWLANStrength = -66 dBm;

— EVCPStatus  

— EVCPStatus  

— = C;

– EVSOC = 74%;

– EVErrorCode = 0;

In this case the status of the element EVImmobilizationRequest = False indicates that the release of the hand brake was the cause to end the charging process.

####### 8.3.4.7.8.6 ACDP\_SystemStatus EVSE requirements

[V2G20-4016] After receiving the SessionSetupRes with parameter "ResponseCode = OK" the EVCC shall start to send ACDP_SystemStatusReq messages.

[V2G20-4017] The SECC shall respond to ACDP_SystemStatusReq message with “ResponseCode = OK” when it is able to represent the current EVSE status with the assigned parameters.

[V2G20-4018] The SECC shall respond to ACDP_SystemStatusReq message with “ResponseCode = FAILED” when it is not able to represent the current EVSE status with the assigned parameters.

[V2G20-4019] In case the SECC receives a ACDP_SystemStatusReq message with Parameter "EV_Status_ReadyToCharge = FALSE" it shall respond with ACDP_SystemStatusRes with "ResponseCode = OK" and all other EVSE ACDP_SystemStatus parameters representing the current EVSE status.

The timeout for System_Status_EndTime is defined in Table 89.

NOTE The System_Status service is stopped after a SessionStopRes with parameter ResponseCode = OK was received.

<div style="text-align: center;">Table 89 — System_Status service timer timeout value</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Value[S]</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>System_Status_EndTimer</td><td style='text-align: center; word-wrap: break-word;'>System_Status_End_Timeout</td><td style='text-align: center; word-wrap: break-word;'>Duration of system status service</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>System_Status_End_Timeout</td><td style='text-align: center; word-wrap: break-word;'>60</td><td style='text-align: center; word-wrap: break-word;'>Timeout value of system status duration</td></tr></table>

####### 8.3.4.7.8.7 Usage of ACDP\_SystemStatusReq/Res on EVSE error