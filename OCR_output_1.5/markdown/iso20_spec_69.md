NOTE 28 As specified by IETF RFC 8446, if a particular field/sub-field/sub-sub-field is not available in a particular V2G root CA certificate or OEM root CA certificate that RDN can be included but left empty in the DistinguishedName (DN).

[V2G20-2404] If no V2G root CA certificate and OEM root CA certificate is/are available in the public SECC or private SECC not in CPM4PE, the "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message shall be left empty.

[V2G20-2405] A private SECC in CPM4PE shall send an empty "authorities" element of "certificate_authorities" extension in the "CertificateRequest" message as defined in IETF RFC 8446. Refer to H.2.2.3 for details of CPM4PE.

[V2G20-2406] SECC shall not include "oid_filters" extension in the "CertificateRequest" message it sends to the EVCC.

[V2G20-2407] SECC shall not include "status_request" extension in the "CertificateRequest" message it sends to the EVCC.

NOTE 29 "status_request" extension requires EVCC to provide OCSP response for its certificate.

[V2G20-2408] Although a valid time in the EVCC is not mandatory, the EVCC should implement a mechanism to discard outdated certificates from the SECC.

NOTE 30 It is not in the scope of this document how errors with EVCC time are handled. It is up to the OEM how these errors are handled.

[V2G20-2409] The EVCC shall validate, according to [V2G20-1001], [V2G20-2324] and [V2G20-2325], the certificate chain that was provided by the SECC during the TLS handshake.

[V2G20-1240] When the EVCC receives the certificate chain in TLS handshake, it validates it per [V2G20-2409]. During this certificate validation, the EVCC shall check the revocation status of the certificates it received in the certificate chain from the public SECC. This revocation check shall be performed via an OCSP response according to IETF RFC 6960 (as updated by IETF RFC 8446).

NOTE 31 In most cases the EVCC will receive the OCSP response from the SECC in the "ServerHello" message.

NOTE 32 The EVCC can determine that the received certificate chain is linked to a V2G root CA certificate. In that case, the received certificate is an SECC certificate and the EVCC is connected to a public SECC.

[V2G20-2410]

When the EVCC receives the certificate chain in TLS handshake, it validates it per [V2G20-2409]. During this certificate validation, if the EVCC received OCSP response for any of the certificates in the certificate chain it received from the private SECC, the EVCC shall check the revocation status of the certificates it received in the certificate chain from the private SECC. This revocation check shall be performed via an OCSP response according to IETF RFC 6960 (as updated by IETF RFC 8954) and IETF RFC 8446.



NOTE 33 The EVCC can determine that the received certificate chain is linked to a PE private root CA certificate. In that case, the received certificate is a PE certificate and the EVCC is connected to a private SECC in a private environment.

NOTE 34 A private SECC can provide OCSP responses or choose not to. If the private SECC did provide OCSP response for any one of the certificates in the PE certificate chain, then the revocation status can be checked for each certificate in the PE certificate chain.

## 64 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.