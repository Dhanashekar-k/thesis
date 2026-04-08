the private SECC in the "ServerHello" message shall be based on profiles as defined in B.9.1.

NOTE 18 In these cases, the OCSP responses are signed using signature algorithm based on curves as defined by [V2G20-2674].

## [V2G20-2393]

If the EVCC offers and the private SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2319] (as per the configurable mechanism as defined by [V2G20-2320]), the OCSP certificate chain(s) provided by the private SECC in the "ServerHello" message shall be based on profiles as defined in B.9.2.

NOTE 19 In these cases, the OCSP responses are signed using signature algorithm based on curves as defined by [V2G20-2319].

[V2G20-1021] The validity period of the OCSP response provided by the SECC shall be limited to one week.

NOTE 20 If cached, each OCSP response can be updated at least once a week.

The validity period is left to the discretion of the OCSP responder. The OCSP response validity cannot be longer than as specified by [V2G20-1021], but it can be shorter than specified by [V2G20-1021].

In the case where the OCSP response for a certificate was not signed by the issuing CA of the certificate (V2G root CA, CSO sub-CA1, CSO sub-CA2 or any cross-certified CA), each OCSP response shall contain the associated OCSP responder's certificate chain including any necessary cross-certificates and each certificate in the chain (except the OCSP signer certificate) shall include the AuthorityInfoAccess extension field.

NOTE 21 As defined in IETF RFC (as updated by IETF RFC 8954), an OCSP responder might either be the sub-CA itself, or it might be an entity which is directly signed by the corresponding sub-CA/root CA using a key pair with a special extended key usage flag in the certificate.

[V2G20-2394] Each of the OCSP responses provided by the public SECC in the "ServerHello" message shall be signed by a certificate derived from one of the V2G root CA certificates supported by the EVCC (EVCC provided a list of the V2G certificates via [V2G20-1006]).

[V2G20-2395] Each of the OCSP responses provided by the private SECC in the "ServerHello" message shall be signed by a certificate derived from one of the PE private root CA certificates supported by the EVCC (EVCC provided a list of the V2G certificates via [V2G20-1006] or it received from the private SECC via [V2G20-2385]).

[V2G20-2396] If the OCSP response for a particular certificate is not available from an OCSP responder that has a certificate derived from one of the V2G root CA certificates supported by the EVCC (EVCC provided a list of the V2G certificates via [V2G20-1006]), the public SECC shall omit providing OCSP response for that certificate in the "ServerHello" message.

[V2G20-2397] If the OCSP response for a particular certificate is not available from an OCSP responder that has a certificate derived from one of the PE private root CA certificates supported by the EVCC (EVCC provided a list of the V2G certificates via [V2G20-1006] or it received from the private SECC via [V2G20-2385]), private SECC shall omit providing OCSP response for that certificate in the "ServerHello" message.