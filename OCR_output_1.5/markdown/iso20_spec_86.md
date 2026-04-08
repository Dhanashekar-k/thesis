##### 7.7.3.10 TLS backwards compatibility

Implementations of this document may be interoperable with earlier versions of th ISO 15118 series (i.e. various editions of ISO 15118-2). To enable an EVCC implementing this document to connect to an SECC implementing a previous revision of 15118 (i.e. various editions of ISO 15118-2), the ClientHello message needs to comply with a specific set of requirements.

Similarly, to enable an SECC implementing this document to accept a connection from an EVCC implementing a previous revision of the ISO 15118 series (i.e. various editions of ISO 15118-2), the interpretation of a received ClientHello message needs to comply with a specific set of requirements.

Therefore, the following requirements should only be implemented, if an implementation of this document should be backwards compatible. Otherwise the following requirements should be ignored.

[V2G20-2054] If the EVCC is required to be backwards compatible to ISO 15118-2, the requirements in 7.7.3.10 shall be implemented.

[V2G20-2055] If the SECC is required to be backwards compatible to ISO 15118-2, the requirements in 7.7.3.10 shall be implemented.

[V2G20-2056] If the EVCC is required to be backwards compatible to ISO 15118-2, it shall additionally support the certificate profiles defined in ISO 15118-2.

[V2G20-2057] If the SECC is required to be backwards compatible to ISO 15118-2, it shall additionally support the certificate profiles defined in ISO 15118-2.

[V2G20-2058] If the EVCC is required to be backwards compatible to ISO 15118-2, it shall include the cipher suites of the ISO 15118-2 in the cipher_suites field of the ClientHello message after the TLS 1.3 cipher suites in the same order as they appear in ISO 15118-2.

NOTE 1 Cipher suites are listed in the cipher_suites field in the order of preference with the most preferred cipher suite first.

[V2G20-2059] If the SECC is required to be backwards compatible to ISO 15118-2, it shall additionally support the cipher suites of the ISO 15118-2 in the cipher_suites field of the ClientHello message.

[V2G20-2060] If the EVCC is required to be backwards compatible to ISO 15118-2, it shall include the necessary extensions, as required by the ISO 15118-2, in the ClientHello message.

NOTE 2 All extensions, as specified in 7.7.3.10 can be included/supported to perform a TLS 1.2 handshake in case an implementation of this document encounters a legacy V2G entity.

[V2G20-2061] If the SECC is required to be backwards compatible to ISO 15118-2, it shall additionally support the necessary extensions, as required by the ISO 15118-2, in the ClientHello message.

NOTE 3 All extensions, as specified in 7.7.3.10 can be included/supported to perform a TLS 1.2 handshake in case an implementation of this document encounters a legacy V2G entity.

If the EVCC is required to be backwards compatible to ISO 15118-2, it shall include the version 0x0303 for TLS 1.2 in the supported_versions extension.

NOTE 4 This allows the SECC to setup a TLS 1.3 or TLS 1.2 session with the EVCC.