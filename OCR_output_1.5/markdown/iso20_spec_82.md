The "NewSessionTicket" message is also (and interchangeably/commonly) referred to as "TLS session ticket" in this document.

## [V2G20-2023]

If the SECC supports VAS services and it allows EVCC to use TLS resumption for VAS, it may send up to the same number of separate/unique "NewSessionTicket" messages (as described in IETF RFC 8446) as the number of VAS supported by the SECC.

NOTE 2 "NewSessionTicket" message sets up the PSK for TLS session resumption.

NOTE 3 Each value added service uses a separate TLS session which are all tied to the same V2G session. Each "NewSessionTicket" message provides a unique PSK that can be used to set up a separate, though parallel, resumed TLS session.

NOTE 4 8.3.4.3.4.3 limits the number of value added services supported by SECC to be eight (8). Hence, at most, additional eight (8) "NewSessionTicket" messages are sent out by the SECC to support each separate value added service.

[V2G20-2611] The SECC shall follow [V2G20-2023] for every "Full Handshake".

NOTE 5 "Full Handshake" can occur multiple times during the same V2G session whenever the V2G session is resumed after a pause.

[V2G20-2612] The "ticket_nonce" sent by the SECC in the "NewSessionTicket" message shall have minimum 7 bits of entropy. Refer to 7.3.7 for details. Additional details can be found in IETF RFC 8446:2018, Annex C.1.

[V2G20-2024] The SECC shall set "ticket_lifetime" in "NewSessionTicket" message to be greater than or equal to Minimum_TLS_SessionTicket_Lifetime and less than or equal to Maximum_TLS_SessionTicket_Lifetime. Refer to IETF RFC 8446 for further details of "ticket_lifetime".

[V2G20-2025] Minimum_TLS_SessionTicket_Lifetime shall be 20 s.

NOTE 6 This can give both the SECC and the EVCC enough time to transmit/receive and process all the "NewSessionTicket" messages. For example, including one for the V2G session, there could be a maximum of 8 "NewSessionTicket" messages exchanged between the SECC and the EVCC. This is to ensure that the SECC does not keep sending new tickets per [V2G20-2027]. The ticket lifetime can also be long enough for the EVCC to initiate a VAS communication when needed during the V2G session.

[V2G20-2026] Maximum_TLS_SessionTicket_Lifetime shall be 86 400 s (24 h).

NOTE 7 Although IETF RFC 8446 supports ticket lifetimes up to 7 days, longer session ticket lifetimes can lead to security issues. Most nominal use cases of TLS session resumption in the context of this document would not need tickets valid longer than a few hours. As such, ticket lifetimes longer than 24 h are not allowed for implementations defined in this document.

## [V2G20-2029]

It is up to the discretion of the CSO/PE operator whether to support TLS resumption for VAS. If the SECC does not support TLS resumption, the SECC shall not send "NewSessionTicket" messages to EVCC.

NOTE 8 Lack of support for TLS session resumption eliminates security concerns related to TLS session resumption (refer to [V2G20-2024] for examples of the security concerns).

The "ticket_lifetime" according to IETF RFC 8446 shall be less than Minimum_TLS_SessionTicket_Lifetime and greater than Maximum_TLS_SessionTicket_Lifetime.