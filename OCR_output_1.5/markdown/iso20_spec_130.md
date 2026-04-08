[V2G20-2285] For wireless communication an SDP client shall send the payload in the order as shown in Figure 3. A byte with a lower number shall be sent before a byte with a higher number.

[V2G20-2286] For wireless communication the SDP client shall send the SECC discovery request message with the payload type value SDPRequestWirelessPayloadID as defined in Table 14, Figure 3 and Figure 4.

[V2G20-2287] The SDP client shall stop sending SECC discovery request messages after a valid SECC discovery response message has been received with "DiagStatus" = "finished with EVSEID" or "finished without EVSEID".

[V2G20-2288] For wireless communication the SDP client shall wait at least 250 ms before sending the next SECC discovery request message after an SECC discovery response message has been received with the payload parameter "DiagStatus" = "ongoing".

[V2G20-2289] For wireless communication the SDP client shall set the timeout V2G_EVCC_CommunicationSetup_Timeout to the value as defined in Table 221, reset the V2G_EVCC_CommunicationSetup_Timer and start monitoring the V2G_EVCC_CommunicationSetup_Timer when a successful TCP/TLS connection is established.

NOTE 2 Valid SECC discovery response message means that the EV was able to establish a functioning IP communication to the SECC using the IP address and port sent by the SECC discovery response message.

7.10.1.9 SECC discovery response message for communication according to ISO 15118-8

The SDP server uses the SDP response message to respond to an SDP request message and provide the IP-address and the port of the SECC to the client.

For an SDP server for wireless communication the requirements [V2G20-143], [V2G20-146], [V2G20-149], [V2G20-150] and [V2G20-151] shall apply.

[V2G20-2290] A SDP server for wireless communication in a single SECC architecture shall reply to any SECC discovery request message with an SECC discovery response message.

Table 26 contains further information for the response message for wireless communication.

Information regarding SECC discovery response message payload for wireless communication can be found below in Table 27.

<div style="text-align: center;">Table 26 — SECC Discovery response message for wireless communication</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Byte No.</td><td style='text-align: center; word-wrap: break-word;'>1-16</td><td style='text-align: center; word-wrap: break-word;'>17-18</td><td style='text-align: center; word-wrap: break-word;'>19</td><td style='text-align: center; word-wrap: break-word;'>20</td><td style='text-align: center; word-wrap: break-word;'>21</td><td style='text-align: center; word-wrap: break-word;'>22</td><td style='text-align: center; word-wrap: break-word;'>23-59</td></tr></table>


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td colspan="2">SECC IP address</td></tr><tr><td colspan="2">SECC Port</td></tr><tr><td colspan="2">Security</td></tr><tr><td colspan="2">Transport protocol</td></tr><tr><td colspan="2">DiagStatus</td></tr><tr><td colspan="2">CouplingType</td></tr><tr><td colspan="2">EVSEID</td></tr></table>