[V2G20-2433] The private SECC shall validate, according to [V2G20-1001], [V2G20-2324] and [V2G20-2325], the certificate chain that was provided by the EVCC during the TLS handshake. During the vehicle certificate chain validation, a private SECC not supporting PnC is not mandated to check revocation status of the certificates in the EVCC's certificate chain.

[V2G20-2434] The private SECC shall validate, according to [V2G20-1001], [V2G20-2324] and [V2G20-2325], the certificate chain that was provided by the EVCC during the TLS handshake. During the vehicle certificate chain validation, a private SECC supporting PnC shall check revocation status of the certificates in the EVCC's certificate chain.

[V2G20-2437] Depending on whether the OEM supports OCSP services or CRL or both for the certificates in vehicle certificate chain, the SECC is free to utilize either OCSP or CRL or both for vehicle certificate revocation check.

NOTE 49 If the vehicle certificate chain contains AuthorityInfoAccess, the SECC can check the revocation status of the certificates in the EVCC's certificate chain via an OCSP response according to IETF RFC 8446. Refer to 7.7.3.3.1 for further details.

NOTE 50 If the vehicle certificate chain contains CRLDistributionPoints, the SECC can check the revocation status of the certificates in the EVCC's certificate chain via a CRL according to IETF RFC 5280, as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. Refer to 7.7.3.3.2 for further details.

NOTE 51 The SECC can receive the revocation status of the vehicle certificate chain from SA or can contact the referenced CRL distribution point/OCSP responder for this status. It is not in the scope of this document to specify the methodology for the SECC to contact the CRL distribution point/OCSP server directly or the SA.

NOTE 52 It is not in the scope of this document to specify the methodology for the SECC to indicate to CRL distribution point/OCSP server/another SA of the named group and signature algorithm that the SECC would like to use. The named group and signature algorithm used for this purpose can be same as those selected for the TLS session (as per the configurable mechanism as defined by [V2G20-2320]).

NOTE 53  It is not advisable to check both OCSP response and CRL for certificate revocation check. If the SECC does want to check both then the response of both can be "good" to consider the said certificate valid. If either of the responses does not indicate "good" then the said certificate can be considered invalid.

[V2G20-2438] If the certificate status of any certificate in vehicle certificate chain is not "good", the SECC shall consider that the received vehicle certificate chain has failed validation.

NOTE 54 Refer to IETF RFC 6960 (as updated by IETF RFC 8954) for further details of the certificate status as provided by OCSP server.

[V2G20-2439] If the revocation status of any certificate in vehicle certificate chain is not available or cannot be determined, the public SECC shall consider that the received vehicle certificate chain has failed validation.

[V2G20-2440] If the revocation status of any certificate in vehicle certificate chain is not available or cannot be determined, the private SECC supporting PnC shall consider that the received vehicle certificate chain has failed validation.

NOTE 55 This requirement does not apply to a private SECC that does not support PnC.

[V2G20-2441] If the revocation status of any certificate in vehicle certificate chain is not available or cannot be determined, per [V2G20-2433], the private SECC not supporting PnC can continue validation of the received vehicle certificate chain.