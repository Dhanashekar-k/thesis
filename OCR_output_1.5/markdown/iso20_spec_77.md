NOTE 6 Named groups are listed in the "supported_groups" extension field in the order of preference of the EVCC with the most preferred named group first.

NOTE 7 Named groups listed in Table 7 are cataloged in the order of preference with the most preferred named group first.

NOTE 8 When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2674] needs to be used, named group "secp521r1" is given preference. When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2319] needs to be used, named group "x448" is given preference.

[V2G20-1637] The EVCC shall support all named groups defined in Table 7.

[V2G20-1638] The EVCC shall include the named groups in the order as they appear in Table 7 or as per the configurable mechanism as defined by [V2G20-2320].

NOTE 9 Named groups listed in Table 7 are cataloged in the order of preference with the most preferred named group first.

NOTE 10 When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2674] needs to be used, named group "secp521r1" is given preference. When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2319] needs to be used, named group "x448" is given preference.

[V2G20-1639] When transmitting the list of supported named groups in the "supported_groups" extension field of the "ClientHello" message, the EVCC shall list the named groups that the EVCC supports in the order of preference of the EVCC.

NOTE 11 Named groups are listed in the "supported_groups" extension field in the order of preference with the most preferred named group first.

NOTE 12 The configurable mechanism as defined by [V2G20-2320] indicates EVCC's preference.

<div style="text-align: center;">Table 7 — Supported named groups</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Named group</td><td style='text-align: center; word-wrap: break-word;'>Standards</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>secp521r1</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8446</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>x448</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8446</td></tr></table>

NOTE 13 Multiple named groups are integrated to allow for cryptographic agility. Implementers can provide a configuration mechanism to securely prevent the usage of a particular named group, e.g. in case a security flaw was found in the preferred named group. The design and implementation of that configuration mechanism is beyond the scope of this document. It is important that the implementers are careful that this mechanism cannot be used nefariously to downgrade to an insecure named group.

NOTE 14 The configurable mechanism as defined by [V2G20-2320] can be used for this purpose.

[V2G20-1663] The EVCC shall also include the list of supported named groups in the "client_shares" field of the "KeyShareClientHello" value of the "key_share" extension in the "ClientHello" message.

[V2G20-1664] The supported named groups included in the "client_shares" field of the "KeyShareClientHello" value of the "key_share" extension in the "ClientHello" message shall be in the order of preference of the EVCC.

NOTE 15 The configurable mechanism as defined by [V2G20-2320] indicates EVCC's preference.