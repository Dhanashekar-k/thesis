[V2G20-2609] The "nonce" sent by the EVCC in the "ClientHello" message shall have a minimum of 231 bits of entropy. Refer to 7.3.7 for details. Additional details can be found in IETF RFC 8446:2018, Annex C.1.

[V2G20-2364] The EVCC shall include the supported versions extension described in IETF RFC 8446 as an extension in the "ClientHello" message.

[V2G20-2365] The EVCC shall include the version "0x0304" for TLS 1.3 in the supported_versions extension.

IETF RFC 8446 requires the "legacy_version" field to be mandatorily included in the "ClientHello" message. It also requires the "legacy_version" field to be mandatorily set to "0x0303".

[V2G20-2366] If an EVCC supports CPM4PE, the EV shall provide a methodology for authorized users to securely place the EVCC in CPM4PE. Refer to H.2.2.3 for details of CPM4PE.

NOTE 3 It is not in the scope of this document to define who the authorized user(s) of the EV are or how to recognize them.

NOTE 4 Similarly, it is not in the scope of this document to define the methodology for securely placing the EVCC in CPM4PE. In some cases it could be as simple as a button press while in others more sophisticated authorization methods could be required. Regardless of the methodology used, CPM4PE on EVCC can only be activated by explicit user interaction.

[V2G20-2367] The CPM4PE shall expire on the EVCC at least 120 s after the user activates the mode. Refer to H.2.2.3 for details of CPM4PE.

NOTE 5 Longer times are allowed but can result in user experience issues. For example, if the user does not actually want to perform the pairing between the particular EV and the particular private SECC, the user could still need to wait for the timeout period defined here before CPM4PE mode expires on the vehicle. Increasing the time the EV and the private SECC can pair, will also result in increased wait time in this example.

[V2G20-1006]

While the EVCC is not in CPM4PE, it shall send a list of all the V2G root CA certificate(s) and PE private root CA certificate(s) it possesses via an extension of type "certificate_authorities" in the "ClientHello" message as defined in IETF RFC 8446. Refer to H.2.2.3 for details of CPM4PE.



NOTE 6 If the EVCC has V2G root CA certificate(s) and/or PE private root CA certificate(s) based on curves as defined by [V2G20-2674] and [V2G20-2319], it will include both in the "certificate_authorities" extension in the "ClientHello" message.

NOTE 7 The "authorities" element contains "DistinguishedName" of the V2G root CA certificate(s) and PE private root CA certificate(s) supported by the EVCC.

[V2G20-2368]

The "DistinguishedName" (DN) of the V2G root CA certificate(s) and PE private root CA certificate(s) provided by the EVCC in "authorities" element of "certificate_authorities" extension in the "ClientHello" message shall include the following relative distinguished name (RDN) fields in the order specified below for each V2G root CA certificate and PE private root CA certificate supported by the EVCC and shall follow X501 and X509 for distinguished names:



– "Country" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or PE private root CA certificate;

– "Organization" sub-sub-field from "Issuer" sub-field from "TBSCertificate" field of the V2G root CA certificate or PE private root CA certificate;