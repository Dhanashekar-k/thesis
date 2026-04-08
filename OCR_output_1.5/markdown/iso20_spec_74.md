NOTE 56 It is up to the discretion of the PE operator whether a private SECC that does not support PnC can check the revocation status of any certificate in vehicle certificate chain or not. This document does not mandate this check.

[V2G20-2442] If the EVCC has provided a certificate chain that does not trace up to a root certificate that is trusted by the SECC, the SECC shall only accept such a certificate, if it successfully validated the certificate chain using an out of band validation mechanism (e.g. server based certificate validation protocol, SCVP, according to IETF RFC 5055). If the validation using such a service is not done, gives a negative result or fails (e.g. due to missing connectivity), the SECC shall consider that the received vehicle certificate chain has failed validation.

NOTE 57 It is not in the scope of this document to specify the methodology for an out-of-band certificate validation mechanism.

[V2G20-2443] If the SECC is unable to validate received vehicle certificate chain successfully, the SECC shall abort the TLS session setup process and apply [V2G20-1805].

NOTE 58 This requirement applies regardless of why the vehicle certificate chain validation failed. For example, the validation could have failed due to missing OCSP response or because one of the certificates in the vehicle certificate chain was revoked, etc.

[V2G20-2444] If the private SECC is in CPM4PE and it successfully validated the received certificate chain and the received chain contains a root CA certificate, the private SECC shall store the received root CA certificate as an OEM/V2G root CA certificate that it trusts for TLS session setup only. Refer to H.2.2.3 for details of CPM4PE.

[V2G20-2445] The CPM4PE shall expire on the private SECC after the OEM/V2G root CA certificate has been installed per [V2G20-2444].

[V2G20-2446] The SECC shall support maximum fragment length negotiation according to IETF RFC 6066.

[V2G20-2447] The SECC shall be able to support, but not be limited to, a maximum fragment length of  $ 2^{9} $ bytes according to IETF RFC 6066.

###### 7.7.3.3.1 Vehicle certificate revocation check via OCSP

[V2G20-2448] The validity period of the OCSP response provided for a vehicle certificate shall not be longer than one week.

NOTE 1 Each OCSP response can be updated at least once every one week.

The validity period is left to the discretion of the OCSP responder. The OCSP response validity cannot be longer than specified by [V2G20-2448], but it can be shorter than specified by [V2G20-2448].

[V2G20-2449] In the case where the OCSP response for a certificate was not signed by the issuing CA of the certificate (V2G root CA, OEM root CA, OEM sub-CA1, OEM sub-CA2 or any corresponding cross-certified CA), each OCSP response shall contain the associated OCSP responder's certificate chain up to, but not including, the corresponding root. If a cross-certificate is used, the OCSP responder's certificate chain shall including any necessary cross-certificates. Each certificate in the OCSP signer certificate chain (except the OCSP signer certificate itself and the root certificate) shall include the AuthorityInfoAccess extension.