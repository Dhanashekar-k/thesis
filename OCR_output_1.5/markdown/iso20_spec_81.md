[V2G20-1524] The firewall running on the SECC shall be configured to allow access to this (these) dedicated VAS port(s).

[V2G20-1525] Either full-handshake TLS or resumed TLS can be used to open an additional communication channel for a VAS. The resumption shall be based on the TLS context (i.e. ticket) exchanged in the V2G session. TLS session resumption shall be performed using the mechanism described in 7.7.3.7.

[V2G20-1527] If the SECC allows TLS resumption for VAS, the SECC shall issue the EVCC a separate TLS session ticket for each offered VAS.

The SECC can provide TCP-level forwarding. This forwarding can be mapped to a fixed external URI or a Proxy server or localhost for local VAS. For an end-to-end secured communication via the proxy server, the proxy server should offer the HTTP CONNECT method as specified in IETF RFC 2817. If UDP based VAS are desired, the approach using session resumption can also be used in conjunction with OpenVPN. For end-to-end secured communication over fixed external URI, the EVCC and the target VAS server should negotiate a separate security association, e.g. a separate TLS session. The specific security for VAS is not in the scope of this document.

NOTE 1 For detailed information on the realization, please refer to Annex G.

NOTE 2 IETF RFC 2817 has been updated by IETF RFC 7230 (which is updated by IETF RFC 8615) and IETF RFC 7231. These updates are considered to be included in this document.

[V2G20-2470] If the SECC does not support TLS session resumption, the EVCC shall setup a distinct TLS session for each value added service supported/provided by the SECC.

NOTE 3 For methods of associating a VAS session with a V2G session, see Annex G.

##### 7.7.3.7 TLS session resumption

TLS session cannot be paused, but it can be closed (terminated). Refer to 7.7.3.8 for details of TLS session termination.

A closed TLS session can be restarted/resumed if the server (SECC) provided the client (EVCC) with the necessary information to resume the TLS session. The resumed TLS session, as described by IETF RFC 8446 is cryptographically bound to the initial TLS session without the need for re-authentication of the server/client certificates saving valuable time in time-critical applications.

A TLS session resumption requires usage of "Session Tickets". The session ticket, in IETF RFC 8446, ensures that the client has access to the session credentials negotiated in the TLS handshake.

In the application of ISO 15118-20, TLS session resumption can be used to ensure that the value added service can be securely related to an already established V2G session. TLS session resumption cannot be used for V2G session resumption. Only full-handshake TLS can be used for V2G session resumption. Both TLS resumption and TLS full-handshake can be used for opening a VAS communication.

[V2G20-2021] 0-RTT shall not be used for TLS session resumption.

NOTE 1 0-RTT can lead to replay attacks.

TLS session resumption in this document is performed via the "PSK Handshake" as defined in IETF RFC 8446 using "pre_shared_key" in the "ClientHello" and "ServerHello" messages. Refer to IETF RFC 8446 for further details.