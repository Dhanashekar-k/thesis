##### 7.7.2.1 Overview

The user datagram protocol (UDP) is a connectionless protocol. UDP does not provide the reliability and ordering guarantees that TCP provides. Packets may arrive out of order or may be lost without notification to the sender or receiver. However, UDP is faster and more efficient for many lightweight or time-sensitive purposes. UDP is located on the transport layer of the OSI layered architecture model.

Optional security mechanisms are provided in 7.5.1 to secure UDP over WLAN. Currently there is no PLC based use case utilizing UDP, for which security mechanisms on UDP would be required (refer to ISO 15118-1 for details on security use cases).

##### 7.7.2.2 Applicable RFC, limitations and protocol parameter settings

[V2G20-065] Each V2G entity shall implement user datagram protocol according to IETF RFC 768.

#### 7.7.3 Transport layer security (TLS)

##### 7.7.3.1 Overview

Security on transport layer is being provided by using TLS. This allows establishment of an authenticated and encrypted channel between the EVCC and the SECC. TLS allows for unilateral or mutual authentication (ensures integrity protection and confidentiality protection). For security in the ISO 15118 series mutual authentication is used (the EVCC authenticates the SECC and the SECC authenticates the EVCC).

For transport layer security, the EVCC authenticates a public SECC using SECC certificate. This is being achieved by a public SECC having a private key corresponding to the SECC certificate and the EVCC verifying the certificate chain from the V2G root CA certificate to the SECC certificate. The revocation status check of sub-CA certificates and the SECC leaf certificate in the certificate chain is performed via the OCSP response received during TLS handshake (for details refer to IETF RFC 6066 as updated by IETF RFC 8446 and IETF RFC 8449).

The public SECC provides a certificate chain comprising its own SECC certificate and CPO sub-CA certificate(s) whose corresponding root certificate is possessed by the EVCC. Together with this certificate chain, the public SECC also sends the OCSP response for each certificate in the SECC certificate chain it sends to the EVCC.

Similarly, the EVCC authenticates private SECC using PE certificate. This is achieved by private SECC having a private key corresponding to the PE certificate and the EVCC verifying the certificate chain from the PE private root CA certificate to the PE certificate. The revocation status is usually not checked.

In this case, the private SECC provides a certificate chain comprising its own PE certificate and PE sub-CA certificate(s) whose corresponding root certificate is possessed by the EVCC.

In instances where the private SECC wants to provide PnC services (via usage of contract certificate(s)), the private SECC additionally provides OCSP responses for all certificates in its PE certificate chain, except for the PE private root CA certificate. EVCC performs the revocation status check of sub-CA certificates and the PE certificate in the certificate chain by utilizing the OCSP responses it received during the TLS handshake (for details refer to IETF RFC 6066 as updated by IETF RFC 8446 and IETF RFC 8449).

Likewise, the SECC authenticates EVCC using vehicle certificate. This is achieved by EVCC having a private key corresponding to the vehicle certificate and SECC verifying the certificate chain from the root certificate to the vehicle certificate. The public SECC checks the revocation status of the vehicle certificate chain while the private SECC typically does not check the revocation status of the vehicle certificate chain. The revocation status check of sub-CA certificates and the vehicle certificate in the certificate chain is performed via the OCSP responses (for details refer to IETF RFC 6066 as updated by IETF RFC 8446 and