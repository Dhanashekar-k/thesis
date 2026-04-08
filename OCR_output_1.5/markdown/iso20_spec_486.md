If OEM sub-CA1 certificate or OEM sub-CA2 certificate or OEM provisioning certificate contains both CRLDistributionPoints and AuthorityInfoAccess extensions, the relying party may process just one or both as per the local policy of the relying party. The relying party, though, shall process at least one of these extensions.

NOTE 3 Table B.11 and Table B.12 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that at least one of them is included and that whichever one is included is processed. [V2G20-2593] clarifies that if the issuer desires to include both of these, its up to the relying party to decide which one to process. However, the relying party processes at least one.

NOTE 4 Per IETF RFC 5280, if any of these extensions are present and critical, they are processed during certificate validation.

NOTE 5 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-2594]

The OEM provisioning certificate extensions in Table B.11 and Table B.12 shall use the definition of "SubjectInfoAccess" as defined in IETF 5280, 4.2.2.2, so that the issuer of an OEM provisioning certificate can indicate to the eMSP that the EVCC contains a TPM and provide the necessary information to the eMSP to process the contract certificates for TPM. As mentioned in IETF RFC 5280, the field "accessMethod" indicates the type $ ^{3} $ of information and the field "accessLocation" indicates either the information itself or a storage location for the information.



NOTE 6 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-2595] In case the OEM provisioning certificate provided by/for the EVCC contains the non-critical extension "TPMStorageKey" and/or "TpmPolicyDigest", the SA/eMSP shall use the method described in 7.9.2.5.3 to encrypt the private contract certificate key for this EVCC.

[V2G20-2596] The issuer of the certificate shall describe the information with three additional access descriptions for "AccessDescription". Here are the definitions in ASN.1 notation:

ISO15118-Extensions { iso(1) standard(0) 15118 part20(20) extensions(0) }
DEFINITIONS :=
BEGIN
id-15118-20-ad    OBJECT IDENTIFIER := { iso(1) standard(0) 15118 part20(20) extensions(0) }
-- Public Storage Key of EVCC's TPM
id-tpmStorageKey    OBJECT IDENTIFIER := { id-15118-20-ad tpmStorageKey(4) }
-- Policy Digest for EVCC's TPM Contract Keys
id-tpmPolicyDigest    OBJECT IDENTIFIER := { id-15118-20-ad tpmPolicyDigest(5) }
END

NOTE 7 Refer to ITU-T X.680 for details of ASN.1 notation.

### B.8 Vehicle certificate profiles