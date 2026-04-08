IETF RFC 8449) or via CRLs (for details refer to IETF RFC 5280 as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399).

The EVCC provides a certificate chain comprising its own vehicle certificate and corresponding sub-CA certificate(s). The EVCC does not provide revocation status with the certificate chain it sends. The public SECC contacts the OCSP responder or CRL provider for revocation status of each certificate it received in the vehicle certificate chain from the EVCC. Similarly, if the private SECC offers PnC, the private SECC will contact the OCSP responder or CRL provider for revocation status of each certificate it received in the vehicle certificate chain from the EVCC.

##### 7.7.3.2 Applicable RFCs

[V2G20-1264] For the considered use cases mutual authentication with TLS version 1.3 according to IETF RFC 8446 shall be supported by each V2G entity.

[V2G20-1521] TLS versions higher than 1.3 may also be supported.

[V2G20-2359] The EVCC or SECC may support TLS version 1.2 as specified in ISO 15118-2 for backwards compatibility.

NOTE 1 [V2G20-2356] applies if TLS 1.2 is negotiated.

NOTE 2 Refer to 7.7.3.10 for TLS 1.2 support.

NOTE 3 Table 5 describes which version of ISO spec is supported by what TLS mechanisms.

<div style="text-align: center;">Table 5 — Supported communication protocols</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>TLS version</td><td style='text-align: center; word-wrap: break-word;'>Communication protocols supported</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1.3</td><td style='text-align: center; word-wrap: break-word;'>- This document- ISO 15118-2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1.2</td><td style='text-align: center; word-wrap: break-word;'>- ISO 15118-2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1.1 or earlier</td><td style='text-align: center; word-wrap: break-word;'>- ISO 15118-2 EIM only</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>No TLS</td><td style='text-align: center; word-wrap: break-word;'>- ISO 15118-2 EIM only- Communication specified in DIN SPEC 70121</td></tr></table>

[V2G20-2360] Random numbers used during TLS session setup shall follow requirements as specified by 7.3.7 and its subclauses.

[V2G20-2361] Session key(s) generated and used during TLS session shall be protected per the requirements as specified by 7.3.6 and its subclauses.

7.7.3.3 Transport layer security usage

[V2G20-2362] The EVCC shall always act as the TLS client component.

NOTE 1 Per IETF RFC 8446, since EVCC acts as the client, the EVCC will initiate the TLS session by sending the "ClientHello" message.

[V2G20-2363] The EVCC shall not request any application data until the TLS handshake is complete.

NOTE 2 Refer to IETF RFC 8446 for the definition of TLS handshake and when it is considered to be complete.