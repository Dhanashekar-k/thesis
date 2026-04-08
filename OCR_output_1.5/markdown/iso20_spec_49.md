[V2G20-721] After indication of a successful Data-Link establishment (D-LINK_READY.indication(DLINKSTATUS=Link established)), the SECC shall initiate the address assignment mechanism.

[V2G20-026] The SECC shall configure an IP address (static or dynamic) by any appropriate mechanism.

NOTE 1 To enable the integration of an SECC in different communication infrastructures, the definition of the address assignment for the SECC is not in the scope of this document. This enables the operator to assign an appropriate mechanism. For example, the operator can choose any existing mechanism providing a valid IP address like, for example, a static IP or the mechanism described in 7.6.3.2 and 7.6.3.3.

[V2G20-027] After the IP address is assigned, the SECC shall start the SDP server as defined in 7.10.1.

NOTE 2 It is not required that the SECC discovery service is implemented in the SECC directly. It is also possible to have a separate unit providing the SECC discovery service.

[V2G20-723] The SECC may stop the SDP server when SECC_CommunicationSetup_Timer is equal or larger than V2G_SECC_CommunicationSetup_Performance_Time.

[V2G20-029] The SECC may stop the IP address assignment mechanism when V2G\_SECC\_CommunicationSetup\_Timer is equal or larger than V2G\_SECC\_CommunicationSetup\_Performance\_Time.

[V2G20-030] After the SDP server is started successfully, the SECC shall wait for a TLS connection initialization depending on the SDP response message as defined in 7.10.1.6.

[V2G20-031] The SECC shall wait until the TLS connection is established.

[V2G20-032] The SECC shall stop waiting for establishing the TLS connection when V2G\_SECC\_CommunicationSetup\_Timer is equal or larger than V2G\_SECC\_CommunicationSetup\_Performance\_Time.

[V2G20-033] After the TLS connection is established, the SECC shall wait for the initialization of the V2G communication session as defined in Clause 8.

[V2G20-722] If [V2G20-033] applies the SECC may stop the SDP server after successful establishment of a TLS connection.

[V2G20-034] The SECC shall terminate the TLS connection after stopping the V2G communication session.

[V2G20-1776] If the SECC received the message SessionStopReq with parameter ChargingSession equal to "Terminate" it shall terminate the Data-Link (D-LINK_TERMINATE.request()) 2 s after sending the message SessionStopRes.

[V2G20-1777] If the SECC received the message SessionStopReq with parameter ChargingSession equal to "Pause" it shall pause the Data-Link (D-LINK_PAUSE.request()) after sending the message SessionStopRes with ResponseCode set to "OK" and follow the sleep and wake-up requirements defined in ISO 15118-3:2015, 7.6.

[V2G20-726] Whenever the SECC receives the indication for a missing Data-Link (D-LINK_READY.indication(DLINKSTATUS=No link)), the SECC shall continue with [V2G20-721].

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.