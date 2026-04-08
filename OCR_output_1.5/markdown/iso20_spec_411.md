<div style="text-align: center;">Table 228 — Overview on application of ACDP ResponseCodes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2">ResponseCode (Enumeration)</td><td colspan="4">V2G application layer messages</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_VehiclePositioningRes</td><td style='text-align: center; word-wrap: break-word;'>ACDP_ConnectRes</td><td style='text-align: center; word-wrap: break-word;'>ACDP_DisconnectRes</td><td style='text-align: center; word-wrap: break-word;'>ACDP_SystemStatusRes</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>OK</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>FAILED</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>FAILED_SequenceError</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>FAILED_UnknownSession</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>FAILED_AssociationError</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

#### 8.6.4 Request-response message sequence requirements

NOTE In this document the sequence of the requirements is output driven.

##### 8.6.4.1 General requirements

The EVCC behavior defining all valid request-response message sequences for WLAN and PLC based communication is shown in 8.6.6. The messages shown in the diagram do not contain the multiplexed messages. If message names are used, they always reference the payload type Part20MainstreamPayloadID, unless noted otherwise.

[V2G20-1413] If the EVCC sends a valid parameter EVPowerProfile (as defined in [V2G20-1070]) in the message PowerDeliveryReq the SECC shall ensure that the power envelope defined by the PowerSchedule in the ChargingSchedule as well as, if present, the DischargingSchedule, can be utilized for the entire time span which they cover.

[V2G20-1009] As soon as the SECC becomes aware of the fact that [V2G20-1413] can no longer be satisfied it shall trigger a proper schedule renegotiation procedure.

[V2G20-1402] When the SECC wants to trigger a termination of the session, it shall set the parameter EVSENotification to "Terminate" and send the parameter until the awaited action has been processed by the EV.

[V2G20-1414] If the EVCC sends PowerDeliveryReq with ChargeProgress=Renegotiate it shall not send an EVPowerProfile.

NOTE 1 [V2G20-1414] is only relevant after leaving the standby phase.

[V2G20-1416] If the parameter EVSENotification in EVSEStatus is equal to Terminate, the EVCC shall stop charging within the number of seconds provided in NotificationMaxDelay.

NOTE 2 After indication of a terminate the SECC can stop the charging from EVSE side, e.g. by turning-off the pilot signal or opening the main contactors after the duration of NotificationMaxDelay.