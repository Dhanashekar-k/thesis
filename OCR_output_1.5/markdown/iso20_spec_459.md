As such, these fields (basic certificate fields "TbsCertificate", "SignatureAlgorithm" and "SignatureValue") are not marked as mandatory or critical in the certificate profiles below.

[V2G20-2694]

The relying party shall reject a certificate that does not contain either "TbsCertificate", "SignatureAlgorithm" or "SignatureValue".



Per ITU-T X.509 and IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), "TbsCertificate" field will always contain sub-fields "Version", "SerialNumber", "Signature", "Issuer", "Validity", "Subject" and "SubjectPublicKeyInfo". If any of these fields are not present in the certificate or if the relying party/validating entity is unable to process any of these sub-fields, the relying party will reject the certificate.

As such, these parameters ("Version", "SerialNumber", "Signature", "Issuer", "Validity", "Subject" and "SubjectPublicKeyInfo") are not marked as mandatory or critical in the certificate profiles below.

[V2G20-2695] The relying party shall reject a certificate that does not contain either "Version", "SerialNumber", "Signature", "Issuer", "Validity", "Subject" or "SubjectPublicKeyInfo" in "TbsCertificate" field.

[V2G20-2696] Each relying party shall be capable of interpreting/processing "AuthorityKeyIdentifier", "SubjectKeyIdentifier", "ExtendedKeyUsage", "CRLDistributionPoints", "AuthorityInfoAccess" and "SubjectInfoAccess" extensions.

This document does not require relying party to be capable of interpreting/processing CertificatePolicies extension. It is left to the local policy of the relying party whether it needs to process the CertificatePolicies extension.

[V2G20-1851]

keyIdentifier in "AuthorityKeyIdentifier" shall be calculated as in IETF RFC 5280:2008, 4.2.1.2, method 2 using the public key of the issuer and shall be included as OCTET STRING in the certificate.



NOTE 1 IETF RFC5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399) and ITU-T X.509, it is optional to include "authorityCertIssuer" and "authorityCertSerialNumber" in "AuthorityKeyIdentifier". But if "authorityCertIssuer" or "authorityCertSerialNumber" is present, then it is mandatory to include the corresponding "authorityCertSerialNumber"/"authorityCertIssuer" in the order shown. If "authorityCertIssuer" is present while "authorityCertSerialNumber" is not present or if "authorityCertSerialNumber" is present while "authorityCertIssuer" is not present, the relying party will reject the certificate.

[V2G20-1852]

keyIdentifier in "SubjectKeyIdentifier" shall be calculated as IETF RFC 5280:2008, 4.2.1.2, method 2 using the public key of its own certificate and shall be included as OCTET STRING in the certificate.



NOTE 2 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-2582] Any URIs in the certificates (for example OCSP address, etc.) shall conform to IETF RFC 3986 as updated by IETF RFC 6874 and IETF RFC 7320.

[V2G20-1224] The distinguished name shall be represented as a string that complies with IETF RFC 4514, Clause 3. Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), any certificate policy shall be valid for entire

## 454 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.