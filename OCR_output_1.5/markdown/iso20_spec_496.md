2G20-2602] If cross certificate contains both CRLDistributionPoints and AuthorityInfoAccess extensions, the relying party may process just one or both as per the local policy of the relying party. The relying party, though, shall process at least one of these extensions.

NOTE 3 Table B.15 and Table B.16 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are required and critical to indicate that at least one of them is included and that whichever one is included is processed. [V2G20-2602] clarifies that if the issuer desires to include both of these, it is up to the relying party to decide which one to process. However, the relying party processes at least one.

NOTE 4 Per ITU-T X.509 and IETF RFC 5280, if any of these extensions are present and critical, they are processed during certificate validation.

NOTE 5 IETF 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-2603]

The cross certificate extensions in Table B.15 and Table B.16 shall use the definition of "SubjectInfoAccess" as defined in IETF 5280, 4.2.2.2, to indicate that the particular certificate is cross certified. As mentioned in IETF RFC 5280, the field "accessMethod" indicates the type $ ^{4} $ of information and the field "accessLocation" indicates either the information itself or a storage location for the information.



NOTE 6 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

The relying party is not required to take any action based on the cross certificate extension "SubjectInfoAccess". It is simply provided for informational purposes.

[V2G20-2604]

The issuer of the certificate shall describe the information with three additional access descriptions for "AccessDescription". Here are the definitions in ASN.1 notation:



ISO15118-Extensions { iso(1) standard(0) 15118 part20(20) extensions(0) }
DEFINITIONS :=
BEGIN

id-15118-20-ad    OBJECT IDENTIFIER := { iso(1) standard(0) 15118 part20(20) extensions(0) }

-- Indication that this certificate is a cross-certificate
id-crossCertIndication    OBJECT IDENTIFIER := { id-15118-20-ad    crossCertIndication(6) }

END

NOTE 7 Refer to ITU-T X.680 for details of ASN.1 notation.

Refer to H.1.5 and its subclauses for further details on cross-signing.

### B.10 Private environment certificate profiles

B.10.1 Based on curves as defined by [V2G20-2674]

Table B.17 outlines certificates for a private environment based on curves as defined by [V2G20-2674].

Table B.17 — Certificates for a private environment based on curves as defined by [V2G20-2674]