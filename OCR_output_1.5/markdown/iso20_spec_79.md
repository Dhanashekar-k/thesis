<div style="text-align: center;">NOTE 24 The configurable mechanism as defined by [V2G20-2320] indicates EVCC preference.</div>


<div style="text-align: center;">Table 8 — Supported signature algorithms</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Signature algorithms</td><td style='text-align: center; word-wrap: break-word;'>Standards</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ecDSA_secp521r1_sha512</td><td style='text-align: center; word-wrap: break-word;'>ANSI X9.62</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ed448</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8032</td></tr></table>

NOTE 25 Multiple signature algorithms are integrated to allow for cryptographic agility. Implementers can provide a configuration mechanism to securely prevent the usage of a particular signature algorithm, e.g. in case a security flaw was found in the preferred signature algorithm. The design and implementation of that configuration mechanism is beyond the scope of this document. It is important that the implementers are careful that this mechanism cannot be used nefariously to downgrade to an insecure signature algorithm.

NOTE 26 The configurable mechanism as defined by [V2G20-2320] can be used for this purpose.

V2G communication sessions can be paused and resumed with no need for re-authentication and/or re-authorization by using the same V2G session credentials used in the previously paused V2G session. 8.3.1 provides further details on pausing and resuming V2G sessions. To ensure a seamless resumption of the V2G communication session, the TLS session should be handled in a similar fashion. A renewal of TLS authentication should not be required, and the credentials (session ticket, pre-shared key, etc.) of the previously established session should be used. Refer to 7.7.3.7 for further details of TLS session resumption.

[V2G20-1672] The SECC shall support all pre-shared key exchange modes defined in Table 9.

[V2G20-1673] The SECC shall include pre-shared key exchange modes in the order as they appear in Table 9.

NOTE 27 Pre-shared key exchange modes listed in Table 9 are cataloged in the order of preference with the most preferred pre-shared key exchange mode first.

NOTE 28 The configurable mechanism as defined by [V2G20-2320] indicates SECC's preference.

[V2G20-1674] When selecting the pre-shared key exchange mode from the list of pre-shared key exchange modes received in the "psk_key_exchange_modes" extension field of the received "ClientHello" message, the SECC shall give preference to the most preferred pre-shared key exchange mode that the SECC supports.

NOTE 29 Pre-shared key exchange modes are listed in the "psk_key_exchange_modes" extension field in the order of preference with the most preferred pre-shared key exchange mode first.

NOTE 30 The configurable mechanism as defined by [V2G20-2320] indicates SECC's preference.

[V2G20-1675] The EVCC shall support all pre-shared key exchange modes defined in Table 9.

[V2G20-1676] The EVCC shall include pre-shared key exchange modes in the order as they appear in Table 9.

NOTE 31 Pre-shared key exchange modes listed in Table 9 are cataloged in the order of preference with the most preferred pre-shared key exchange mode first.

[V2G20-1677] When transmitting the list of supported pre-shared key exchange modes in the "psk_key_exchange_modes" extension field of the "ClientHello" message, the EVCC shall list the pre-shared key exchange modes that the EVCC supports in the order of preference of the EVCC.

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.