transmission security and transport protocol for the port provided in the same payload as the security and transport protocol bytes.

##### 7.10.1.7 Timing and error handling

The process of SECC discovery is based on the application time out definitions as described in 7.10.1. This subclause describes additional timing and error handling for the SECC discovery protocol.

[V2G20-157] The SDP client shall count the number of SECC discovery request messages until a valid SECC discovery response message has been received.

[V2G20-158] The SDP client shall reset the counter for sent SECC discovery request messages after a valid SECC discovery response message has been received.

NOTE Valid means that a valid IP address was received and communication setup procedure can continue.

[V2G20-159] After sending an SECC discovery request message, the SDP client shall wait for an SECC discovery response message for at least 250 ms.

[V2G20-160] After unsuccessfully waiting for an SECC discovery response message the SDP client shall send a new SECC discovery request message and increment the counter for sent SECC discovery request messages.

[V2G20-161] If the SDP client has not received any valid SECC discovery response message after sending in maximum 50 consecutive SECC discovery request messages it shall stop the SECC discovery.

[V2G20-162] After unsuccessfully stopping the SECC discovery, the SDP client shall go to the same state as defined for a timeout (refer to Figure 8).

7.10.1.8 SECC discovery request message for communication according to ISO 15118-8

For the SDP clients for wireless communication, the requirements [V2G20-135], [V2G20-136], [V2G20-137], [V2G20-138], [V2G20-139] shall apply. Table 22 contains further information for the request message for wireless communication.

Information regarding P2PS/PPD and CouplingType value settings in the SDP request can be found below in Table 23.

<div style="text-align: center;">Table 22 — SECC Discovery request message for wireless communication</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Byte No.</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>Security</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>Transport protocol</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>3 - 4</td><td style='text-align: center; word-wrap: break-word;'>P2PS/PPD</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>5</td><td style='text-align: center; word-wrap: break-word;'>CouplingType</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>6 - 25</td><td style='text-align: center; word-wrap: break-word;'>EVID</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>26 - 62</td><td style='text-align: center; word-wrap: break-word;'>EVSEID</td></tr></table>