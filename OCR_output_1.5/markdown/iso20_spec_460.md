certification path. This means the "certificatePolicies" extension shall appear in all certificates in the certificate chain except the root certificate. Certificate policy is provided in the certificates using the OIDs. Hence, the certificate policy OID provided in a leaf certificate shall also appear in the sub-CA1 (if present) and sub-CA2 certificates to be valid for the entire certification path.

For example, if the "certificatePolicies" extension is missing from sub-CA1 certificate, no explicit certificate policies are allowed below that CA certificate.

"certificatePolicies" extension should not appear in root certificates as "certificatePolicies" is implicitly set to "anyPolicy" in the root certificate. If the "certificatePolicies" extension were to be present in a root certificate, any updates/changes/modification to the policies would require generating a new root certificate.

If "CRLDistributionPoints" is present, "distributionPoint", "reasons" and "cRLIssuer" that are part of "CRLDistributionPoints" may or may not be present while "CRLDistributionPoints" is present.

Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), if "AuthorityInfoAccess" is present, "accessMethod" and "accessLocation" that are part of "AuthorityInfoAccess" are also present. If "accessMethod" and "accessLocation" are not present while "AuthorityInfoAccess" is present, the relying party will reject the certificate.

Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), if "SubjectInfoAccess" is present, "accessMethod" and "accessLocation" that are part of "SubjectInfoAccess" are also present. If "accessMethod" and "accessLocation" are not present while "SubjectInfoAccess" is present, the relying party will reject the certificate.

### B.3 V2G root CA certificate profiles

#### B.3.1 Based on curves as defined by [V2G20-2674]

Table B.3 outlines the V2G root CA certificate based on curves as defined by [V2G20-2674].

<div style="text-align: center;">Table B.3 — V2G root CA certificate based on curves as defined by [V2G20-2674]</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td colspan="3">ISO 15118-20 certificate profiles</td><td style='text-align: center; word-wrap: break-word;'>V2G root V2G</td></tr><tr><td rowspan="13">TbsCertificate</td><td colspan="2">Version</td><td style='text-align: center; word-wrap: break-word;'>2 (X.509v3)</td></tr><tr><td colspan="2">SerialNumber</td><td style='text-align: center; word-wrap: break-word;'>Integer</td></tr><tr><td rowspan="2">Signature</td><td style='text-align: center; word-wrap: break-word;'>AlgorithmIdentifier</td><td style='text-align: center; word-wrap: break-word;'>x / c</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>algorithm</td><td style='text-align: center; word-wrap: break-word;'>x / c\necdsa-with-SHA512</td></tr><tr><td rowspan="5">Issuer</td><td style='text-align: center; word-wrap: break-word;'>Country</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization unit</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Common name</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Domain component</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td rowspan="4">Validity</td><td style='text-align: center; word-wrap: break-word;'>Validity</td><td style='text-align: center; word-wrap: break-word;'>x\n(25 years)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>notBefore</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td rowspan="2">time</td><td style='text-align: center; word-wrap: break-word;'>x\n(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format YYYYMMDDHHMMSSZ)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>[Actual time is CA discretionary]</td></tr></table>