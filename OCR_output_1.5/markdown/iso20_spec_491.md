– the EVCCID itself (see [V2G20-2597]) shall be the value of the Common Name (CN) of the Distinguished Name (DN);

- the name of the OEM shall be encoded in the field Organization (O) using a unique identifier chosen by the OEM, to identify this OEM;

- the X.500 distinguished name in the subject field shall not contain any further values.

G20-2599] Vehicle sub-CA1 certificate, vehicle sub-CA2 certificate and vehicle certificate shall contain at least one or both of CRLDistributionPoints or/and AuthorityInfoAccess extensions.

NOTE 1 Table B.13 and Table B.14 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that one of them is included and processed. [V2G20-2599] clarifies that including at least one of them is mandatory while including both of them is not mandatory.

NOTE 2 [V2G20-2599] does not specify which one of these extensions can be included. It is left up to the OEM to decide which certificate revocation method works best for it. In some cases CRLs will work better as they allow the relying party to download the entire CRL once and have it available for local checking of revocation status of the next contract certificate without a need for a live connection to the CRL server while in other cases OCSP will provide better results as it provides current revocation status and requires less storage and searching on part of the relying party.

## [V2G20-2600]

If vehicle sub-CA1 certificate, vehicle sub-CA2 certificate and vehicle certificate contains both CRLDistributionPoints and AuthorityInfoAccess extensions, the relying party may process just one or both as per the local policy of the relying party. The relying party, though, shall process at least one of these extensions.

NOTE 3 Table B.13 and Table B.14 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that at least one of them is included and that whichever one is included is processed. [V2G20-2600] clarifies that if the issuer desires to include both of these, it is up to the relying party to decide which one to process. However, the relying party processes at least one.

NOTE 4 Per ITU-T X.509 and IETF RFC 5289, if any of these extensions are present and critical, they are processed during certificate validation.

NOTE 5 IETF RF5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

There may be use cases allowing usage of vehicle certificate for both client and server authentication. As such, the vehicle certificate profile provides for the possibility of allowing the vehicle certificate to be used for both. Since these use cases are not fully defined yet, it is left up to the OEM's discretion whether to generate vehicle certificates that can be used for both client and server authentication or those that can only be used for client authentication.

To allow widest acceptance of the vehicle certificate, vehicle certificates should be derived from a chain originating from a V2G root CA certificate. This allows the SECC to validate the vehicle certificate using a V2G root that it may possess. If the vehicle certificates cannot be derived from a chain originating from a V2G root CA certificate, the vehicle certificate chain may be cross signed by a V2G root CA certificate. Refer to H.1.5 and its subclauses for further details on cross-signing.

### B.9 Cross certificate & OCSP signer certificate profiles

#### B.9.1 Based on curves as defined by [V2G20-2674]

Table B.15 outlines the cross certificate and OSCP signer certificates based on curves as defined by [V2G20-2674].

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.