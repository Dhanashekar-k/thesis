[V2G20-1665] The SECC shall include the selected named group in the "server_share" field of the "KeyShareServerHello" value of the "key_share" extension in the "ServerHello" message.

NOTE 16 The configurable mechanism as defined by [V2G20-2320] indicates SECC's preference.

[V2G20-1666] The SECC shall support all signature algorithms defined in Table 8.

[V2G20-1667] The SECC shall include the signature algorithms in the order as they appear in Table 8.

[V2G20-1668] When selecting the signature algorithm from the list of signature algorithms received in the "signature_algorithms" and/or "signature_algorithms_cert" extension field(s) of the received "ClientHello" message (per IETF RFC 8446, extension "signature_algorithms_cert" is optional), the SECC shall give preference to the most preferred signature algorithm that the SECC supports. The SECC's/private SECC's preference shall be determined by Table 8 and the configurable mechanism as defined by [V2G20-2320].

NOTE 17 Signature algorithms are listed in the "signature_algorithms" and/or "signature_algorithms_cert" extension field(s) in the order of preference of the EVCC with the most preferred signature algorithm first.

NOTE 18 Signature algorithms listed in Table 8 are cataloged in the order of preference with the most preferred signature algorithm first.

NOTE 19 When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2674] needs to be used, signature algorithm "ecdsa_secp521r1_sha512" is given preference. When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2319] needs to be used, signature algorithm "ed448" is given preference.

[V2G20-2461] The signature algorithm selected by the SECC shall be compatible with the selected named group.

NOTE 20 For example, the SECC can decide not select signature algorithm based on curve as defined by [V2G20-2674] while selecting named group based on curve as defined by [V2G20-2319].

[V2G20-1669] The EVCC shall support all signature algorithms defined in Table 8.

[V2G20-1670] The EVCC shall include the signature algorithms in the order as they appear in Table 8.

NOTE 21 Signature algorithms listed in Table 8 are catalogued in the order of preference with the most preferred signature algorithm first.

NOTE 22 When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2674] needs to be used, signature algorithm "ecdsa_secp521r1_sha512" is given preference. When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2319] needs to be used, signature algorithm "ed448" is given preference.

[V2G20-1671]

When transmitting the list of supported signature algorithms in the "signature_algorithms" and/or "signature_algorithms_cert" extension field(s) of the "ClientHello" message (per IETF RFC 8446, extension signature_algorithms_cert is optional), the EVCC shall list the signature algorithms that the EVCC supports in the order of preference of the EVCC.



NOTE 23 Signature algorithms are listed in the "signature_algorithms" and/or "signature_algorithms_cert" extension field(s) in the order of preference with the most preferred signature algorithm first.