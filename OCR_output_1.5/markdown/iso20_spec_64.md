– "Organization Unit" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or PE private root CA certificate;

– "Common Name" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or PE private root CA certificate;

– "CertificateSerialNumber" sub-field from "TBSCertificate" field of the V2G root CA certificate or PE private root CA certificate.

NOTE 8 As specified by IETF RFC 8446, if a particular field/sub-field/sub-sub-field is not available in a particular V2G root CA certificate or PE private root CA certificate that RDN can be included, but left empty in the DistinguishedName (DN).

[V2G20-2369] If no V2G root CA certificate(s) and PE private root CA certificate(s) are available in the EVCC, "authorities" element of "certificate_authorities" extension in the "ClientHello" message shall be left empty.

[V2G20-2370] While the EVCC is in CPM4PE, it shall send an empty "authorities" element of "certificate_authorities" extension in the "ClientHello" message as defined in IETF RFC 8446 regardless if the EVCC has any V2G root CA certificate(s) and PE private root CA certificate(s) or not. Refer to H.2.2.3 for details of CPM4PE.

[V2G20-2371] The EVCC shall not include "oid_filters" extension in the "CertificateRequest" message it sends to the SECC.

[V2G20-2372] The EVCC shall include the extension "status_request" in the "ClientHello" message as defined in IETF RFC 8446.

[V2G20-2373] The EVCC shall include a zero-length "responder_id_list" sequence in the "ResponderID" field of "OCSPStatusRequest".

NOTE 9 "OCSPStatusRequest" is a field in "CertificateStatusRequest". "CertificateStatusRequest" makes up the "extension_data" field of "status_request" extension.

[V2G20-2374] The SECC shall always act as the TLS server component.

NOTE 10 Per IETF RFC 8446, since SECC acts as the server, the SECC will respond to the TLS session requests ("ClientHello") by sending the "ServerHello" message.

[V2G20-2375] The SECC shall not transmit any application data until the TLS handshake is complete.

NOTE 11 Refer to IETF RFC 8446 for the definition of TLS handshake and when it is considered to be complete.

[V2G20-2610] The "nonce" sent by the SECC in the "ServerHello" message shall have a minimum of 231 bits of entropy. Refer to 7.3.7 for details. Additional details can be found in IETF RFC 8446:2018, Annex C.1.

[V2G20-2376] If a private SECC supports CPM4PE, the private SECC shall provide a methodology for authorized users to securely place the private SECC in CPM4PE. Refer to H.2.2.3 for details of CPM4PE.

NOTE 12 It is not in the scope of this document to define who the authorized user(s) of the private SECC are or how to recognize them.

NOTE 13 Similarly, it is not in the scope of this document to define the methodology for securely placing the private SECC in CPM4PE. In some cases it could be as simple as a button press while in others more sophisticated