
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEElectricalChargingDeviceStatus</td><td style='text-align: center; word-wrap: break-word;'>simpleType:electricalChargingDeviceStatusTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>This element provides the information if the conductive connection between the EV and EVSE is in state &quot;connected&quot; (CP State = B, C or D) or &quot;disconnected&quot; (CP State = A).</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMechanicalChargingDeviceStatus</td><td style='text-align: center; word-wrap: break-word;'>simpleType:mechanicalChargingDeviceStatusTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>This element provides the information if the ACDP status of the EVSE is in home, or end position or if it is in a moving state.</td></tr></table>

###### 8.3.4.7.8 ACDP_SystemStatusReq/Res

####### 8.3.4.7.8.1 ACDP_SystemStatusReq/Res handling

This message pattern is used to get current status information of involved charging equipment. The ACDP_SystemStatus message pair provides important diagnostic information as well.

The ACDP_SystemStatus messages have a separate payload type thus they execute in parallel and independent to the V2G messages.

NOTE 1 Safety relevant control with respect to the charging equipment and charging process is not in the scope of this document.

NOTE 2 The V2G communication is kept until the end of the charging session as well in the case of an error until the system is in a safe status after the ACDP has been moved into the home position.

The intended application of ACDP\_SystemStatus is:

- first time after successfully processing of SessionSetupRes;

– at any time within the V2G communication process, asynchronous of the primary communication;

– in case of any relevant internal EV status change;

– in case of any EV error after processing of the last EVSE response message with “ResponseCode = OK”;

– in case of any EVSE error indicated by “ResponseCode = FAILED”, or “FAILED_xxx”;

– ACDP_SystemStatus may possibly be omitted in loop messages with “ResponseCode = OK”.

NOTE 3 The ACDP_SystemStatus message pair can also be applied in a synchronous manner in between the charging control V2G messages.

For the usage of ACDP_SystemStatus in error cases see 8.3.4.7.8.5 and 8.3.4.7.8.7.

####### 8.3.4.7.8.2 ACDP\_SystemStatusReq

[V2G20-4010] The EVCC and the SECC shall implement the message elements as defined in Figure 90 and Table 87.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.