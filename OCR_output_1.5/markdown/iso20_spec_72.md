certificate itself), which shall be one of those roots previously indicated by the SECC as being present in the SECC.

## [V2G20-2426]

If the SECC provides a list of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message is not empty), the EVCC shall follow IETF RFC 5280, 7.1, as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399, to utilize the received "DistinguishedNames" (see [V2G20-2401]) to choose a vehicle certificate chain originating from one of the received "DistinguishedNames" and provide it to the SECC in "CertificateRequest" message as defined in IETF RFC 8446.

[V2G20-2427] If the public SECC did not provide any indication of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message is empty), the EVCC shall send a "Certificate" message containing its own certificate chain (vehicle certificate chain) including any necessary cross-certificates up to the corresponding root (excluding the root certificate itself) of its own choosing.

NOTE 46 The EVCC can determine that the received certificate chain is linked to a V2G root CA certificate. In that case, the received certificate is an SECC certificate and the EVCC is connected to a public SECC.

2G20-2428] If the private SECC did not provide any indication of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message is empty), an EVCC not in CPM4PE shall send a "Certificate" message containing its own certificate chain (vehicle certificate chain) including any necessary cross-certificates up to the corresponding root (excluding the root certificate itself) of its own choosing.

NOTE 47 The EVCC can determine that the received certificate chain is linked to a PE private root CA certificate. In that case, the received certificate is a PE certificate and the EVCC is connected to a private SECC in a private environment.

[V2G20-2429] If the EVCC cannot provide a certificate with a chain up to one of the roots, which the SECC signaled as being present in the SECC, the EVCC shall provide within the TLS handshake a valid certificate including a chain to a root certificate (the root certificate itself shall not be transmitted).

NOTE 48 It is assumed that the EVCC is not in CPM4PE.

[V2G20-2430] If the named group and signature algorithm selected for the TLS session are based on curves as defined by [V2G20-2674] (as per the configurable mechanism as defined by [V2G20-2320]), the vehicle certificate chain provided by the EVCC in the "Certificate" message shall be based on profiles as defined in B.8.1.

[V2G20-2431] If the named group and signature algorithm selected for the TLS session are based on curves as defined by [V2G20-2319] (as per the configurable mechanism as defined by [V2G20-2320]), the vehicle certificate chain provided by the EVCC in the "Certificate" message shall be based on profiles as defined in B.8.2.

[V2G20-2432] The public SECC shall validate, according to according to [V2G20-1001], [V2G20-2324] and [V2G20-2325], the certificate chain that was provided by the EVCC during the TLS handshake. During the EVCC certificate chain validation the public SECC shall check revocation status of the certificates in the EVCC's certificate chain.