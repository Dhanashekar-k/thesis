eMSP sub-CA1 certificate, eMSP sub-CA2 certificate and contract certificate shall contain at least one or both of CRLDistributionPoints or/and AuthorityInfoAccess extensions.

NOTE 1 Table B.9 and Table B.10 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that either one of them are included and processed. [V2G20-2590] clarifies that including at least one of them is mandatory while including both of them is not mandatory.

NOTE 2 [V2G20-2590] does not specify which one of these extensions can be included. It is left up to the eMSP to decide which certificate revocation method works best for it. In some cases CRLs will work better as they allow the relying party to download the entire CRL once and have it available for local checking of revocation status of the next contract certificate without a need for a live connection to the CRL server while in other cases OCSP will provide better results as it provides current revocation status and requires less storage and searching on part of the relying party.

If eMSP sub-CA1 certificate or eMSP sub-CA2 certificate or contract certificate contains both CRLDistributionPoints and AuthorityInfoAccess extensions, the relying party may process just one or both as per the local policy of the relying party.

NOTE 3 Table B.9 and Table B.10 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that at least one of them are included and that whichever one is included is processed. [V2G20-2591] clarifies that if the issuer desires to include both of these, it is up to the relying party to decide which one to process. However, the relying party processes at least one.

NOTE 4 Per ITU-T X.509 and IETF RFC 5280, if any of these extensions are present and critical, they are processed during certificate validation.

NOTE 5 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-1225] The contract certificate extensions in Table B.9 and Table B.10 shall use the definition of "SubjectInfoAccess" as defined IETF RFC 5280:2008, 4.2.2.2, so that the issuer of a contract certificate can provide the applicant with additional information and services. As mentioned in IETF RFC 5280, the field "accessMethod" indicates the type $ ^{2} $ of information and the field "accessLocation" indicates either the information itself or a storage location for the information.

NOTE 6 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-1226] The issuer of the certificate shall describe the information with three additional access descriptions for "AccessDescription". Here are the definitions in ASN.1 notation: