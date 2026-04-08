[V2G20-2398] A private SECC not supporting PnC can ignore the "status_request" extension, and continue as if the EVCC never sent that request. Refer IETF RFC 8446 for further details.

NOTE 22 A private SECC not supporting PnC is allowed to function in an offline mode where it cannot provide OCSP response for its PE certificate chain.

A private SECC supporting PnC is required to provide OCSP response for its PE certificate chain.

[V2G20-2399] If the public SECC cannot provide a certificate with a chain up to one of the roots, which the EVCC signaled as being present in the EVCC, the public SECC shall provide within the TLS handshake a valid certificate including a chain to a root certificate (the root certificate itself shall not be transmitted).

[V2G20-2400] The SECC shall request EVCC to send the EVCC's certificate via "CertificateRequest" message.

NOTE 23 This allows setting up a mutually authenticated TLS session where both the EVCC and SECC verify the authenticity of each other.

[V2G20-2401] A public SECC shall send a list of all V2G root CA certificate(s) and/or OEM root CA certificate(s) it possesses via the "certificate_authorities" extension in the "CertificateRequest" message it sends to the EVCC.

NOTE 24 Refer to IETF RFC 8446.

NOTE 25 The "authorities" element contains "DistinguishedName" of the V2G root CA certificate(s) and/or OEM root CA certificate(s) supported by the SECC.

V2G20-2402] A private SECC not in CPM4PE shall send a list of all V2G root CA certificate(s) and/or OEM root CA certificate(s) it possesses via the "certificate_authorities" extension in the "CertificateRequest" message it sends to the EVCC.

NOTE 26 Refer to IETF RFC 8446.

NOTE 27 The "authorities" element contains "DistinguishedName" of the V2G root CA certificate(s) and/or OEM root CA certificate(s) supported by the private SECC.

The "DistinguishedName" (DN) of the V2G root CA certificate(s) and/or OEM root CA certificate(s) provided by the public SECC or private SECC not in CPM4PE in the "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message shall include the following relative distinguished name (RDN) fields in the order specified below for each V2G root CA certificate and OEM root CA certificate supported by the public SECC or private SECC not in CPM4PE and shall follow X501 and X509 for distinguished names:

– "Country" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or OEM root CA certificate;

– "Organization" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or OEM root CA certificate;

– "Organization Unit" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or OEM root CA certificate;

– "Common Name" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or OEM root CA certificate;

– "CertificateSerialNumber" sub-field from "TBSCertificate" field of the V2G root CA certificate or OEM root CA certificate.