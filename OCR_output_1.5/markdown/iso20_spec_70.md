[V2G20-2411] If the OCSP status of any certificate in SECC certificate chain is not provided by the public SECC in the "ServerHello", the EVCC may contact the OCSP server listed in the said certificate for the OCSP status of that certificate.

NOTE 35 The EVCC can determine that the received certificate chain is linked to a V2G root CA certificate. In that case, the received certificate is a SECC certificate and the EVCC is connected to a public SECC.

NOTE 36 It is not in the scope of this document to specify the methodology for the EVCC to contact the OCSP server directly.

If the private SECC provided OCSP status of at least one but not all of the certificates in the PE certificate chain in the "ServerHello", the EVCC may contact the OCSP server listed in the said certificate for the OCSP status of that certificate.

NOTE 37 The EVCC can determine that the received certificate chain is linked to a PE private root CA certificate. In that case, the received certificate is a PE certificate and the EVCC is connected to a private SECC in a private environment.

NOTE 38 It is not in the scope of this document to specify the methodology for the EVCC to contact the OCSP server directly.

[V2G20-2413] Per IETF RFC 6960 (as updated by IETF RFC 8954), the EVCC will verify the OCSP responder certificate before accepting the OCSP response. If the EVCC is unable to successfully verify the OCSP responder certificate (e.g. when the OCSP responder's certificate is derived from a root not trusted by the EVCC) for any of the OCSP responses, the EVCC shall consider the entire SECC/PE certificate chain to have failed validation.

[V2G20-2414] Per IETF RFC 6960 (as updated by IETF RFC 8954), the EVCC will verify the signature on the received OCSP response. If the EVCC is unable to successfully verify the signature on the OCSP response (e.g. when the signature on the response does not match the signature calculated by the EVCC using the OCSP responder's certificate) for any of the OCSP responses, the EVCC shall consider the entire SECC/PE certificate chain to have failed validation.

[V2G20-2415] If the certificate status of any certificate in the received SECC/PE certificate chain is not "good", the EVCC shall consider the entire SECC/PE certificate chain to have failed validation.

NOTE 39 Refer to IETF RFC 6960 (as updated by IETF RFC 8954) for further details of the certificate status as provided by OCSP server.

[V2G20-2416] If the revocation status of any certificate in the received SECC certificate chain from the SECC is not available or cannot be determined, the EVCC shall consider the entire SECC certificate chain to have failed validation.

NOTE 40 The EVCC can determine that the received certificate chain is linked to a V2G root CA certificate. In that case, the received certificate is an SECC certificate and the EVCC is connected to a public SECC.

[V2G20-2417] If the revocation status of at least one certificate of the received PE certificate chain from the private SECC is available, but the revocation status of all other certificates of the received PE certificate chain from the private SECC is not available or cannot be determined, the EVCC shall consider the entire PE certificate chain to have failed validation.