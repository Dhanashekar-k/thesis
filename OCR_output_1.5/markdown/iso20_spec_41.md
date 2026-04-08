and as such may install the PE private root CA certificate for that particular PE in the EVCC of the EVs in that fleet but may choose not to install any PE private root CA certificate in EVCC in any other EVs it manufactures.

If the communication should work, some root CA certificates are installed in each SECC and EVCC. Depending on the use case of the EV and/or EVSE, the OEMs/CSOs will need to figure out which root CA certificates they should install in their EVCC/SECC so as to enable that particular use case.

[V2G20-1806] Each EVCC shall provide storage space for at least two V2G root CA certificates.

Storing two V2G root CA certificates is required by [V2G20-1806] to be able to store the currently valid V2G root CA certificate of a specific V2G root CA and additionally the new V2G root CA certificate of that V2G root CA that will be valid after the previous V2G root CA certificate has expired.

[V2G20-2352] Each SECC shall provide storage space for at least two V2G root CA certificates.

NOTE 1 It is not mandatory for SECC to support any V2G root CA certificates. A CSO can decide to only offer ISO 15118-20 communications to those EVs whose vehicle certificate is signed (or cross-signed) by an OEM root CA certificate supported by the CSO's SECC.

Storing two V2G root CA certificates is required by [V2G20-2352] to be able to store the currently valid V2G root CA certificate of a specific V2G root CA and additionally the new V2G root CA certificate of that V2G root CA that will be valid after the previous V2G root CA certificate has expired.

NOTE 2 This requirement does not apply to a private SECC.

There can be multiple V2G root CAs in a given market. [V2G20-1806] and [V2G20-2352] define the minimum number of V2G root CA certificates that need to be supported by EVCC and SECC respectively. Regulatory and market conditions may require EVCC and/or SECC to support more than the minimum number of V2G root CA certificates. For example, it is strongly advised, but not mandated, that the EVCC and SECC support all local/regional V2G root CA certificates. This will improve availability of ISO 15118-20 communications and allow the EV to utilize ISO 15118-20 based communications on any local/regional EVSE.

It is not in the scope of this document to define the maximum number of V2G root CA certificates to be supported by the EVCC and/or SECC. It is left up to the OEM to decide on the maximum number of V2G root CA certificates to be supported by the EVCC. Similarly, it is left up to the CSO to decide on the maximum number of V2G root CA certificates to be supported by the SECC.

Additionally, if the EV drives to a different region, it would need V2G root CA certificates for that region. It is not in the scope of this document to define how the OEM manages that situation. But the OEM is advised to take that into account when designing the EVs.

[V2G20-2353] Each public SECC shall provide storage space for at least two OEM root CA certificates.

NOTE 3 It is not mandatory for a public SECC to support any OEM root CA certificates. A CSO can decide to only offer ISO 15118-20 communications to those EVs whose vehicle certificate is signed (or cross-signed) by a V2G root CA certificate supported by the CSO's SECC.

Storing two OEM root CA certificates is required by [V2G20-2353] to be able to store the currently valid OEM root CA certificate of a specific OEM and additionally the new OEM root CA certificate of that OEM that will be valid after the previous V2G root CA certificate has expired.

[V2G20-2354] Each private SECC shall provide storage space for at least one OEM root CA certificate or V2G root CA certificate.

NOTE 4 A private SECC can contain more than one OEM root CA certificates and/or V2G root CA certificates.

## 36 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.