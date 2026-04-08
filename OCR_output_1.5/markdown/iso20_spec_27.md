<div style="text-align: center;">Table 2 — Certificate extension examples</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Certificate extensions</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Key usage</td><td style='text-align: center; word-wrap: break-word;'>Usage of the corresponding private key (e.g. Digital Signature, non-repudiation, key encipherment,...)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Extended Key Usage</td><td style='text-align: center; word-wrap: break-word;'>Further specification of key usage using OIDs, e.g.: - server authentication (1.3.6.1.5.5.7.3.1); - client authentication (1.3.6.1.5.5.7.3.2). NOTE Sometimes the following values are encoded here: - Microsoft SGC (1.3.6.1.4.1.311.10.3.3) - Netscape SGC (2.16.840.1.113730.4.1) SGC stands for server gated crypto and indicates that the server can also use strong cryptography for the connection with the client&#x27;s browser. This extension was used at the time of strong crypto export control to enable financial web site to provide appropriate protection of the data transfer.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CRL distribution point</td><td style='text-align: center; word-wrap: break-word;'>Location to retrieve certificate revocation lists</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>OCSP</td><td style='text-align: center; word-wrap: break-word;'>Location to retrieve OCSP. Refer to IETF RFC 6960 as updated by IETF RFC 8954 for details.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Authority information</td><td style='text-align: center; word-wrap: break-word;'>Additional authorization information</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Subject alternative name</td><td style='text-align: center; word-wrap: break-word;'>Alternative names of the entity</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Basic constraint = CA</td><td style='text-align: center; word-wrap: break-word;'>True if the certificate is a root certificate or a sub-CA certificate.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>subjectAltPublicKeyInfo</td><td style='text-align: center; word-wrap: break-word;'>Alternative/secondary certificate key data. This contains the alternative key algorithm and the alternative key generated using the said algorithm. Refer to ITU-T X.509 for further details.</td></tr></table>

<div style="text-align: center;">NOTE 3 For those not familiar with OIDs, e.g. 1.3.6.1.5.5.7.3.1, refer to the Object Identifier (OID) Repository.</div>


[V2G20-2673] Each V2G entity shall support Hash-operation SHA-512 (signature process) according to NIST FIPS PUB 180-4 (for ISO 15118-1, use case element ID: F1).

[V2G20-2318] Each V2G entity shall support SHAKE256 according to NIST FIPS PUB 202 (for ISO 15118-1, use case element ID: F1).

[V2G20-2674] Each V2G entity shall support signature operations using ECC based elliptic curve (secp521r1[SECG notation]) with signature algorithm ECDSA (for ISO 15118-1, use case element ID: F1).

[V2G20-2319] Each V2G entity shall additionally support signature operations with ECC algorithm Ed448 (for ISO 15118-1, use case element ID: F1), i.e. signature algorithm EdDSA using elliptic curve Curve448 (or Curve448-Goldilocks) in Edwards form, see IETF RFC 7748 and IETF RFC 8032.

NOTE 4 In case V2G entity chooses to use Curve448-based signature algorithm, it also uses ECC-based DH algorithm X448 defined for this curve (see IETF RFC 7405), in addition to the algorithms specified by NIST Special Publication 800-56A. See also [V2G20-2710] and [V2G20-2711].

[V2G20-2320]

Multiple algorithms are integrated to allow for cryptographic agility. Each V2G entity shall implement a secure configurable mechanism to securely switch usage of (elliptic curve) EC from that defined in [V2G20-2674] to the one defined by [V2G20-2319] and prevent the usage of a particular algorithm, e.g. in case a security flaw was found in the preferred ECC algorithm.



Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.