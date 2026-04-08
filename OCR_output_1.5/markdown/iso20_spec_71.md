NOTE 41 The EVCC can determine that the received certificate chain is linked to a PE private root CA certificate. In that case, the received certificate is a PE certificate and the EVCC is connected to a private SECC in a private environment.

If the EVCC determines that the certificate chain it received during TLS session setup process is a PE certificate chain and the private SECC did not provide OCSP response for any of the certificates in the PE certificate chain, the EVCC shall ignore the fact that the private SECC has not sent OCSP responses. The EVCC shall continue with the PE certificate chain validation without the certificate revocation check as specified by [V2G20-1001].

NOTE 42 The EVCC can determine that the received certificate chain is linked to a PE private root CA certificate. In that case, the received certificate is a PE certificate and the EVCC is connected to a private SECC in a private environment.

[V2G20-2419] If the EVCC is in CPM4PE and it successfully validated the received certificate chain and the received chain contains a root CA certificate, the EV shall assume that the certificate it received during TLS session setup process is a PE certificate chain from the private SECC and the EVCC shall store the received root CA certificate as a PE private root CA certificate that it trusts for TLS session setup only. Refer to H.2.2.3 for details of CPM4PE.

NOTE 43 Refer to H.2 and its subclauses for details of PE and risks with PE certificate chains. Also refer to 7.3.2.2 for further details of risks with PE certificate chains.

[V2G20-2420] The CPM4PE shall expire on the EVCC after the PE private root CA certificate has been installed per [V2G20-2419].

[V2G20-2421] If the SECC has provided a certificate chain that does not trace up to a V2G root CA certificate or a PE private root CA certificate that the EVCC contains/possesses, the EVCC shall only accept such a certificate, if it successfully validated the certificate chain using an out of band validation mechanism (e.g. server based certificate validation protocol, SCVP, according to IETF RFC 5055). If the validation using such a service is not done, gives a negative result or fails (e.g. due to missing connectivity), the EVCC shall treat the SECC/PE certificate chain as failed validation.

NOTE 44 It is not in the scope of this document to specify the methodology for an out-of-band certificate validation mechanism.

[V2G20-2422] If the EVCC is unable to validate SECC/PE certificate chain successfully, the EVCC shall abort the TLS session setup process and apply [V2G20-1805].

NOTE 45 This requirement applies regardless of why the SECC/PE certificate chain validation failed. For example, the validation could have failed due to missing OCSP response or because one of the certificates in the SECC certificate chain was revoked, etc.

[V2G20-2423] When the EVCC receives a "CertificateRequest" message, the EVCC shall check that extension "status_request" is not present in the "CertificateRequest" message. If extension "status_request" is present in the "CertificateRequest" message, the EVCC shall disregard this extension and continue with the TLS handshake as if the "CertificateRequest" message did not contain those extension(s).

[V2G20-2424] In response to a "CertificateRequest" message, the EVCC shall send a "Certificate" message containing its own certificate chain (vehicle certificate chain) including any necessary cross-certificates up to the corresponding root (excluding the root

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.