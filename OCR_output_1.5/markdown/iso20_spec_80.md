<div style="text-align: center;">NOTE 32 Pre-shared key exchange modes are listed in the "psk_key_exchange_modes" extension field in the order of preference with the most preferred pre-shared key exchange mode first.</div>


<div style="text-align: center;">Table 9 — Supported pre-shared key exchange modes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Pre-shared key exchange modes</td><td style='text-align: center; word-wrap: break-word;'>Standards</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>psk_dhe_ke</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8446</td></tr></table>

[V2G20-1678] The SECC shall accept a PSK handshake only to resume a TLS session.

[V2G20-1679] The EVCC shall utilize a PSK handshake only to resume a TLS session.

[V2G20-1680] Regardless if a previous TLS session is being resumed or a new TLS session is being initiated, the SECC shall not accept the "early_data" extension in the received "ClientHello" message as described in IETF RFC 8446.

[V2G20-1612] Regardless if a previous TLS session is being resumed or a new TLS session is being initiated, the EVCC shall not send the "early_data" extension in the transmitted "ClientHello" message as described in IETF RFC 8446.

7.7.3.5 TLS session setup

There can be multiple TLS handshakes between the EVCC and SECC during the same V2G session. For the purposes of this document, "Initial Handshake" is defined as the first successful TLS handshake between the EVCC and SECC during the given V2G session.

Similarly, for the purposes of this document, "Full Handshake" is defined as the TLS handshake where client (EVCC)/server (SECC) authentication is performed via client (vehicle)/server (SECC) certificate validation. This is same as "Full Handshake" as defined in IETF RFC 8446. "Full Handshake" does not include "pre_shared_key" in the "ClientHello" and "ServerHello" messages. Refer to IETF RFC 8446 for further details. An "Initial Handshake" is always a "Full Handshake".

[V2G20-2677] Only full-handshake TLS shall be used for V2G communication between EVCC and SECC, whether initial or resumed, except for VAS communication.

[V2G20-2462] The SECC shall follow the requirements defined in 7.7.3.3 and IETF RFC 8446 to setup the TLS 1.3 session.

[V2G20-2465] The EVCC shall follow the requirements defined in 7.7.3.3 and IETF RFC 8446 to setup the TLS 1.3 session.

[V2G20-2468] The CPM4PE, if active, shall expire on the EVCC after the TLS session has been established and PE private root CA certificate was not received in the PE certificate chain.

[V2G20-2469] The CPM4PE, if active, shall expire on the private SECC after the TLS session has been established and OEM root CA certificate was not received in the vehicle certificate chain.

7.7.3.6 Enabling of VAS communication

[V2G20-1523] Each VAS shall be offered via a dedicated port at SECC.