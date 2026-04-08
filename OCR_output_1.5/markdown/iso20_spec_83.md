[V2G20-2027] If TLS resumption is supported, the SECC shall send a new TLS session ticket(s) with updated information Minimum_TLS_SessionTicket_Lifetime before the TLS session ticket(s) are set to expire while the TLS session is still active, i.e. it has not been terminated yet.

NOTE 9 This helps ensure that EVCC has valid session tickets at any given time while the TLS session is still active. It also enables the SECC to set "ticket_lifetime" to short values reducing some of the security risks inherent with TLS session resumption.

NOTE 10 This requires SECC to maintain the knowledge of how long the session tickets it sent are still valid for.

[V2G20-2028] The SECC shall stop sending new TLS session tickets (per [V2G20-2027]) as soon as it has been 604 800 s (7 days) since the last "Full Handshake" during the currently active V2G session.

NOTE 11 This ensures that the existing TLS session is not extended indefinitely. Indefinite TLS session extension can lead to security risks like TLS session continuation long (604 800 s (7 days)) after certificate expiration or revocation, etc.

NOTE 12 This requires SECC to maintain the knowledge of how long it has been since the "Full Handshake".

[V2G20-2031] The SECC shall not send the "early_data" extension in the transmitted "NewSessionTicket" message (as described in IETF RFC 8446).

[V2G20-2032] The SECC shall securely cache/store the data transmitted in "NewSessionTicket" message(s).

NOTE 13 It is not in the scope of this document to define the requirements on how the data transmitted in "NewSessionTicket" message(s) is stored and how the data coherency is maintained.

[V2G20-2033] The SECC shall discard all data associated with TLS session tickets that have expired.

NOTE 14 This requires SECC to periodically check if any of the stored/cached TLS session tickets have expired or otherwise fail to meet the requirements in this document. This document leaves the periodicity of such checks to the discretion of the implementers.

Upon reception of a "NewSessionTicket" message, the EVCC shall ensure that the "ticket_lifetime" in the received "NewSessionTicket" message is greater than or equal to Minimum_TLS_SessionTicket_Lifetime and less than or equal to Maximum_TLS_SessionTicket_Lifetime. Any "NewSessionTicket" messages not meeting this criterion shall be discarded. Refer to IETF RFC 8446 for further details of "ticket_lifetime".

[V2G20-2035] The EVCC shall reject any "NewSessionTicket" messages if they are received 604 800 s (7 days) or more after the "Full Handshake".

NOTE 15 This ensures that the existing TLS session is not extended indefinitely. Indefinite TLS session extension can lead to security risks like TLS session continuation long (604 800 s (7 days)) after certificate expiration or revocation, etc.

NOTE 16 This requires EVCC to maintain the knowledge of how long it has been since the "Full Handshake".

[V2G20-2036] The EVCC shall reject any "NewSessionTicket" message with "early_data" extension (as described in IETF RFC 8446.

[V2G20-2037] After verifying the "NewSessionTicket" message to be valid and contain a TLS session ticket that meets requirements [V2G20-2034], [V2G20-2035], and [V2G20-2036],

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.