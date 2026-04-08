[V2G20-2457] Per IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), the SECC will verify the signature on the received CRL. If the SECC is unable to successfully verify the signature on the CRL (e.g. when the signature on the response does not match the signature calculated by the SECC using the CRL issuer's certificate), the SECC shall consider the received vehicle certificate chain to have failed validation.

7.7.3.4 Transport layer security credentials and cipher suites

[V2G20-2458] The SECC shall support all cipher suites defined in Table 6.

[V2G20-1856] The SECC shall include the cipher suites in the order as they appear in Table 6.

NOTE 1 Cipher suites listed in Table 6 are cataloged in the order of preference with the most preferred cipher suite first.

[V2G20-1857] When selecting the cipher suite from the list of cipher suites received in the "cipher_suites" field of the received "ClientHello" message, the SECC shall give preference to the most preferred cipher suite that the SECC supports.

NOTE 2 Cipher suites are listed in the "cipher_suites" field in the order of preference with the most preferred cipher suite first.

[V2G20-2459] The EVCC shall support all cipher suites defined in Table 6.

[V2G20-1858] The EVCC shall include the cipher suites in the order as they appear in Table 6.

NOTE 3 Cipher suites listed in Table 6 are cataloged in the order of preference with the most preferred cipher suite first.

[V2G20-1860] When transmitting the list of supported cipher suites in the "cipher_suites" field of the "ClientHello" message, the EVCC shall list the cipher suites that the EVCC supports in the order of preference of the EVCC.

NOTE 4 Cipher suites are listed in the "cipher_suites" field in the order of preference with the most preferred cipher suite first.

<div style="text-align: center;">Table 6 — Supported cipher suites</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Cipher suite</td><td style='text-align: center; word-wrap: break-word;'>RFC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>TLS_AES_256_GCM_SHA384</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 5116</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>TLS_CHACHA20_POLY1305_SHA256</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8439</td></tr></table>

NOTE 5 Multiple algorithms are integrated to allow for cryptographic agility. Implementers can provide a configuration mechanism to securely prevent the usage of a particular algorithm, e.g. in case a security flaw was found in the preferred cipher suite. The design and implementation of that configuration mechanism is not in the scope of this document.

[V2G20-1634] The SECC shall support all named groups defined in Table 7.

[V2G20-2460] When selecting the named group from the list of named groups received in the "supported_groups" extension field of the received "ClientHello" message, the SECC shall give preference to the most preferred named group that the SECC supports. The SECC's/private SECC's preference shall be determined by Table 7 and the configurable mechanism as defined by [V2G20-2320].