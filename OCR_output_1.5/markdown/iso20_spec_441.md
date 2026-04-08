[V2G20-2317] After receiving the ScheduleExchangeRes with EVSEProcessing set to "Finished", the EVCC shall send a PowerDeliveryReq on V2GTP payload type ScheduleRenegotiationPayloadID with EVPowerProfile based on the ScheduleList in the response received from SECC.

[V2G20-1049] To exit the schedule renegotiation process, the SECC shall send a PowerDeliveryRes on V2GTP payload type ScheduleRenegotiationPayloadID with ResponseCode = OK.

NOTE 1 After the PowerDeliveryRes on V2GTP payload type ScheduleRenegotiationPayloadID with ResponseCode = OK, no further message exchange on V2GTP payload type ScheduleRenegotiationPayloadID is expected for this schedule renegotiation session.

[V2G20-1050] The new EVPowerProfile as a result from the schedule renegotiation session shall be applied in the next ChargeLoopReq on the mainstream communication channel.

NOTE 2 During schedule renegotiation, the SECC can use EVSETargetActivePower (phase specific if necessary) in the ChargeLoopRes on the mainstream communication channel to limit the power drawn by the EVCC temporarily.

[V2G20-1051] During schedule renegotiation according to [V2G20-1045] the EVCC shall maintain the charging behavior based on [V2G20-1825].

The following requirements apply to SECC triggered schedule renegotiation.

[V2G20-1845] When the SECC wants to trigger a schedule renegotiation, it shall set the parameter EVSENotification to ScheduleRenegotiation in ChargeLoopRes on the mainstream communication channel.

[V2G20-1052] When the EVCC received a message where the EVSENotification is set to ScheduleRenegotiation, it shall send a ChargeParameterDiscoveryReq within the number of seconds provided in NotificationMaxDelay with updated parameters based on the current situation on V2GTP payload type ScheduleRenegotiationPayloadID.

[V2G20-2235] If a schedule renegotiation has not completed successfully within the ScheduleRenegotiationPayloadID sidestream, then the SECC shall decide if it wants to abort or retry the schedule renegotiation. If the SECC wants to retry the schedule renegotiation it shall restart the process according to [V2G20-1845] and set the ResponseCode of the ChargeLoopRes to WARNING_ScheduleRenegotiationFailed. If the following schedule renegotiation fails to complete again, then the SECC is allowed to escalate by setting the ResponseCode of the ChargeLoopRes to FAILED_ScheduleRenegotiation and to terminate the charging session (see 8.8.2 on general FAILED behavior).

[V2G20-1053] Requirements [V2G20-1047], [V2G20-1048], [V2G20-1049] and [V2G20-1050] shall apply as subsequent steps.

##### 8.6.5.2 Metering confirmation

For more information, see at 8.3.4.3.11.1.

##### 8.6.5.3 Parking status

Parking status is applied to the EV arriving to the parking area or leaving from there. It will be used by an EV to inform the EVSE either about its arrival and exchange necessary information for guidance to a

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.