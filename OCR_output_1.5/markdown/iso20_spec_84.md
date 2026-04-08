the EVCC shall securely cache/store the data in the received "NewSessionTicket" message.

NOTE 17 It is not in the scope of this document to define the requirements on how the data received in "NewSessionTicket" message(s) is stored and how the data coherency is maintained.

When the EVCC wants to resume a TLS session, it needs to check if there is (are) any valid TLS session ticket(s) stored in the EVCC. Each TLS session ticket comes with a "ticket_lifetime". According to IETF RFC 8446:2018, 4.2.11.1, the EVCC checks if the ticket age is less than the ticket lifetime before using the ticket to resume the TLS session. It is up to the OEM to define how TLS session ticket expiration/age is calculated using the "ticket_lifetime".

[V2G20-2039]

The EVCC shall include only one (1) "PskIdentity" in the "OfferedPsks" field of "PreSharedKeyExtension" value of "pre_shared_key" extension field of the "ClientHello" message it sends to set up a resumed TLS session.



The EVCC will include the data from the "ticket" field from one of the securely stored/cached "NewSessionTicket" message in the "identity" field of "PskIdentity" field of the "OfferedPsks" field of "PreSharedKeyExtension" value of "pre_shared_key" extension field of the "ClientHello" message it sends to set up a resumed TLS session. Refer to IETF RFC 8446:2018, 4.2.11 for further details.

[V2G20-2040]

Once a TLS session ticket has been used to try to resume a TLS session, that particular TLS session ticket shall be discarded by the EVCC.



NOTE 18 Each TLS session ticket is used only once. This is done regardless if the EVCC was actually able to successfully resume the TLS session using the said TLS session ticket. This prevents EVCC tracking. Refer to IETF RFC 8446:2018, Annex C.4 for further details of the security risks.

Upon receiving the "pre_shared_key" extension in the "ClientHello" message, the SECC will authenticate the EVCC via the credentials provided in "pre_shared_key" extension of the "ClientHello" message. Refer to IETF RFC 8446 for further details of this authentication process.

[V2G20-2042] During the authentication of the EVCC using the credentials provided in "pre_shared_key" extension of the "ClientHello" message, the SECC shall simply fail to set up a TLS session if it is unable to successfully validate the PSK identity provided by the EVCC in the "pre_shared_key" extension of the "ClientHello" message.

[V2G20-2043] During the authentication of the EVCC using the credentials provided in "pre_shared_key" extension of the "ClientHello" message, the SECC shall simply fail to set up a TLS session if it is unable to successfully validate the binder provided by the EVCC in the "pre_shared_key" extension of the "ClientHello" message.

[V2G20-2044] If a TLS session is already active between the SECC and the EVCC, after processing a "ClientHello" message with a "pre_shared_key" extension, the SECC shall send a "NewSessionTicket" message (as described in IETF RFC 8446) as long as [V2G20-2028] is not violated.

[V2G20-2045] If no TLS for V2G session is active between the EVCC and SECC, the "pre_shared_key" extension in a "ClientHello" message shall be ignored and a full-handshake TLS shall be established.

7.7.3.8 TLS session termination

A TLS session is terminated when the V2G session is paused or terminated due to any reason (charging process completed, cable disconnected, etc.), the VAS session is terminated, etc.