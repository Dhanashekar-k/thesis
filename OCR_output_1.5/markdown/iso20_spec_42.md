There can be multiple OEMs in a given market. [V2G20-2353] defines the minimum number of OEM root CA certificates that need to be supported by the public SECC. [V2G20-2354] defines the minimum number of OEM root CA certificates that need to be supported by the private SECC. Regulatory and market conditions may require the SECC to support more than the minimum number of OEM root CA certificates. For example, it is strongly advised, but not mandated, that the SECC support all local/regional OEM root CA certificates. This will improve availability of ISO 15118-20 communications and allow the EV to utilize ISO 15118-20 based communications on any local/regional EVSE.

It is not in the scope of this document to define the maximum number of OEM root CA certificates to be supported by the SECC. It is left up to the CSO to decide on the maximum number of OEM root CA certificates to be supported by the SECC.

Additionally, as new EV OEMs startup, there would be a need to add OEM root CA certificates for those new OEMs to the SECCs. It is not in the scope of this document to define how the CSO/PE operator manages that. But the CSO/PE operator is advised to take that into account when designing their systems.

[V2G20-2355] Each EVCC should provide storage space for at least one PE private root CA certificate.

NOTE 5 It is not mandatory for the EV to support private environment.

[V2G20-867] Except in private environment (PE), a root CA shall not issue a leaf certificate.

NOTE 6 Leaf certificates can only be issued by a sub-CA.

NOTE 7 This applies to all root CAs including V2G root CA, OEM root CA, eMSP root CA, etc. except PE private root CA. A PE private root CA can issue a leaf certificate. Refer to 7.3.4 for further details of PE security.

#### 7.3.4 Support and application of TLS

According to 7.3.2 and 7.3.3, this document requires the following TLS:

1) the certificate management defined in 7.3.2;

2) the key management defined in 7.3.2;

3) the certificate chain structure defined in 7.3.2 and 7.3.3;

4) the certificate validity period defined in 7.3.2 and 7.3.3.

[V2G20-1238] In the SDP handshake, when the SECC intends to offer ISO 15118-20 communication, it shall respond to a TLS request by the EVCC with TLS.

[V2G20-1235] V2G-CI-TLS shall always be applied for both the EVCC and SECC, if the chosen ProtocolNamespace is equal to "urn:iso:std:iso:15118:-20".

[V2G20-2646] After the message exchange of supportedAppProtocolReq/Res, usage of V2G-CI-TLS shall be confirmed.

[V2G20-1237] If the established connection between EVCC and SECC is TLS 1.2 (or lower) or TCP without TLS the EVCC shall not offer ISO 15118-20 communication in SupportedAppProtocolReq message (see Table 5).

[V2G20-2356] If the established connection between EVCC and SECC is TLS 1.2 (or lower) or TCP without TLS the SECC shall not select ISO 15118-20 communication from SupportedAppProtocolReq message (see Table 5).

Private environment is considered to be a power transfer service for a closed user group. This user group is defined and managed by the eMSP of the power transfer service itself. The security of the field is