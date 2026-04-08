NOTE 2 As defined in IETF RFC 6960 (as updated by IETF RFC 8954), an OCSP responder can either be the sub-CA itself, or it can be an entity which is directly signed by the corresponding sub-CA/root CA using a key pair with a special extended key usage flag in the certificate.

[V2G20-2450] Each of the OCSP responses received by the SECC should be signed by a certificate derived from one of the root certificates supported by the SECC.

NOTE 3 It is not in the scope of this document to define the methodology used by the SECC to indicate to the OCSP responder the roots that are trusted by the SECC. Refer to IETF RFC 6960 (as updated by IETF RFC 8954) for further details.

[V2G20-2451] Per IETF RFC 6960 (as updated by IETF RFC 8954), the SECC will verify the OCSP responder certificate before accepting the OCSP response. If the SECC is unable to successfully authenticate the OCSP responder certificate (e.g. when the OCSP responder's certificate is derived from a root not trusted by the SECC), the SECC shall consider the received vehicle certificate chain to have failed validation.

[V2G20-2452] Per IETF RFC 6960 (as updated by IETF RFC 8954), the SECC will verify the signature on the received OCSP response. If the SECC is unable to successfully verify the signature on the OCSP response (e.g. when the signature on the response does not match the signature calculated by the SECC using the OCSP responder's certificate), the SECC shall consider the received vehicle certificate chain to have failed validation.

###### 7.7.3.3.2 Vehicle certificate revocation check via CRL

[V2G20-2453] The validity period of the CRL provided for a vehicle certificate shall not be longer than 1 week.

NOTE 1 Each CRL can be updated at least once every one week. The validity period is left to the discretion of the CRL issuer. The CRL validity cannot be longer than as specified by [V2G20-2453], but it can be shorter than specified by [V2G20-2453].

[V2G20-2454] In the case where the CRL for a certificate was not signed by the issuing CA of the certificate (V2G root CA, OEM root CA, OEM sub-CA1, OEM sub-CA1, OEM sub-CA2 or any corresponding cross-certified CA), each CRL shall contain the associated CRL issuer's certificate chain up to, but not including, the corresponding root. If a cross-certificate is used, the CRL issuer's certificate chain shall including any necessary cross-certificates. Each certificate in the CRL certificate chain (except the CRL certificate itself and the root certificate) shall include the CRLDistributionPoints extension.

NOTE 2 As defined in IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), a CRL issuer can either be the sub-CA itself, or it can be an entity which is directly signed by the corresponding sub-CA/root CA using a key pair with a special extended key usage flag in the certificate.

[V2G20-2455] Each of the CRL received by the SECC should be signed by a certificate derived from one of the root certificates supported by the SECC.

NOTE 3 It is not in the scope of this document to define the methodology used by the SECC to indicate to the CRL issuer the roots that are trusted by the SECC. Refer to IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399) for further details.

[V2G20-2456] Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), the SECC will verify the CRL issuer certificate before accepting the CRL. If the SECC is unable to successfully authenticate the CRL issuer certificate (e.g. when the CRL issuer's certificate is derived from a root not trusted by the SECC), the SECC shall consider the received vehicle certificate chain to have failed validation.

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.