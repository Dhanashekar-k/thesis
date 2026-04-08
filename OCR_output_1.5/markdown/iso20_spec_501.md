
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2" colspan="2">ISO 15118-2 certificate profiles</td><td colspan="4">Private SECC/private environment</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>PE private root CA Root</td><td style='text-align: center; word-wrap: break-word;'>PE sub-CA1 Sub (optional)</td><td style='text-align: center; word-wrap: break-word;'>PE sub-CA2 Sub (optional)</td><td style='text-align: center; word-wrap: break-word;'>PE certification Leaf</td></tr><tr><td rowspan="3">SignatureAlg orithm</td><td style='text-align: center; word-wrap: break-word;'>AlgorithmIdentifier</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>algorithm</td><td style='text-align: center; word-wrap: break-word;'>✗ id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>✗ id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>✗ id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>✗ id-Ed448</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>parameters</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td></tr><tr><td colspan="2">SignatureValue</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td></tr></table>

<div style="text-align: center;">B.10.3 Common requirements for private environment certificate profiles</div>


As mentioned in Table B.17 and Table B.18, it is optional to include the "certificatePolicies" extension in any of the PE certificates. If the "certificatePolicies" extension is included, it can be marked as non-critical so that the relying party can ignore this extension if it cannot process it. This is done to improve the interoperability.

[V2G20-2697] PEID shall be an alpha-numeric string with maximum length of 255 bytes that can be used to uniquely identify a private SECC in a particular private environment.

Uniqueness of PEID is only required between private SECCs in a single private environment. Uniqueness of PEID is not required between private SECCs in different/distinct private environments. Uniqueness of subject name is required between private SECCs in different/distinct private environments.

[V2G20-2605] In case the private SECC supports only EIM, PE sub-CA1 certificate, PE sub-CA2 certificate and PE certificate may contain at least one or both of CRLDistributionPoints or/and AuthorityInfoAccess extensions.

[V2G20-2715] In case the private SECC supports PnC, PE sub-CA1 certificate, PE sub-CA2 certificate and PE certificate shall contain at least one or both of CRLDistributionPoints or/and AuthorityInfoAccess extensions.

NOTE 1 Table B.17 and Table B.18 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that either of them may be included or neither of them may be included. But if they are included, the relying party of these certificates processes them. [V2G20-2605] clarifies that if the issuer desires to include both of these, it is up to the relying party to decide which one to process.

NOTE 2 [V2G20-2605] does not specify which one of these extensions can be included. It is left up to the CA to decide which certificate revocation method works best for it. In some cases CRLs will work better as they allow the relying party to download the entire CRL once and have it available for local checking of revocation status of the next contract certificate without a need for a live connection to the CRL server while in other cases OCSP will provide better results as it provides current revocation status and requires less storage and searching on part of the relying party.

[V2G20-2606]

If PE sub-CA1 certificate or PE sub-CA2 certificate or PE certificate contains both CRLDistributionPoints and AuthorityInfoAccess extensions, the relying party may process just one or both as per the local policy of the relying party. The relying party, though, shall process at least one of these extensions.



NOTE 3 Table B.17 and Table B.18 specify that both CRLDistributionPoints and AuthorityInfoAccess extensions are optional but critical to indicate that either of them may be included or neither of them may be included. But if they are included, the relying party of these certificates processes them. [V2G20-2606] clarifies that if the issuer desires to include both of these, it is up to the relying party to decide which one to process. However, the relying party processes at least one.

NOTE 4 Per ITU-T X.509 and IETF RFC 5280, if any of these extensions are present and critical, they are processed during certificate validation.