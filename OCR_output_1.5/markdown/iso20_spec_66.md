message is empty), a private SECC not in CPM4PE shall send in the "ServerHello" message its own certificate chain (PE certificate chain) including any necessary cross-certificates up to a root (excluding the root certificate itself) of its own choosing.

[V2G20-2385] A private SECC in CPM4PE shall disregard [V2G20-2383] and send the "ServerHello" message containing its own certificate chain (PE certificate chain) including any necessary cross-certificates and its PE private root CA certificate. Refer to H.2.2.3 for details of CPM4PE.

[V2G20-2386] If the EVCC offers and private SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2674] (as per the configurable mechanism as defined by [V2G20-2320]), the PE certificate chain provided by the private SECC in the "ServerHello" message shall be based on profiles as defined in B.10.1.

[V2G20-2387] If the EVCC offers and private SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2319] (as per the configurable mechanism as defined by [V2G20-2320]), the PE certificate chain provided by the private SECC in the "ServerHello" message shall be based on profiles as defined in B.10.2.

[V2G20-2388] Since the EVCC used the "status_request" extension to request OCSP response for the certificate chain sent by the public SECC, it shall include an OCSP response for each certificate in the certificate chain sent by the public SECC in the "ServerHello" message. Refer to IETF RFC 6960 (as updated by IETF RFC 8954) and IETF RFC 8446 for further details.

NOTE 15 If the public SECC is deployed in a stand-alone application without internet connection or is operating in a semi-online manner without internet connection, the public SECC will not be able to provide the OCSP response.

[V2G20-2389] If the EVCC offers and the public SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2674] (as per the configurable mechanism as defined by [V2G20-2320]), the OCSP certificate chain(s) provided by the public SECC in the "ServerHello" message shall be based on profiles as defined in B.9.1.

NOTE 16 In these cases, the OCSP responses are signed using signature algorithm based on curves as defined by [V2G20-2674].

[V2G20-2390] If the EVCC offers and the public SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2319] (as per the configurable mechanism as defined by [V2G20-2320]), the OCSP certificate chain(s) provided by the public SECC in the "ServerHello" message shall be based on profiles as defined in B.9.2.

NOTE 17 In these cases, the OCSP responses are signed using signature algorithm based on curves as defined by [V2G20-2319].

[V2G20-2391] Since the EVCC used the "status_request" extension to request OCSP response for the certificate chain sent by private SECC, if the private SECC supports PnC, it shall include an OCSP response for each certificate in the certificate chain sent by the private SECC in the "ServerHello" message. Refer to IETF RFC 6960 (as updated by IETF RFC 8954) and IETF RFC 8446 for further adetails.

[V2G20-2392] If the EVCC offers and the private SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2674] (as per the configurable mechanism as defined by [V2G20-2320]), the OCSP certificate chain(s) provided by