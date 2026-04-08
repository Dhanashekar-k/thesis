[V2G20-2063] If the EVCC wants/prefers to setup and utilize ISO 15118-2 communications, it shall omit sending supported_versions extension.

NOTE 5 This either forces the SECC to setup a TLS 1.2 session with EVCC or fails to setup any TLS session at all.

[V2G20-2064] The EVCC shall continue a TLS 1.2 handshake, as described in ISO 15118-2, if the SECC selected TLS 1.2 and EVCC supports TLS 1.2.

[V2G20-2065] The SECC shall perform a TLS 1.2 handshake, as specified in ISO 15118-2, if supported_versions extension is not present in (i.e. missing from) the received ClientHello and the SECC supports TLS 1.2.

[V2G20-2066] The SECC shall perform a TLS 1.2 handshake, as specified in ISO 15118-2, if supported_versions extension in the received ClientHello is set to 0x0303 (i.e. no other versions are listed in the supported_versions extension) and the SECC supports TLS 1.2.

NOTE 6 [V2G20-2356] applies, if a TLS 1.2 handshake is negotiated.

NOTE 7 A SECC that does not support TLS 1.3 sends a ServerHello without the supported_versions extension, since implementations are required to ignore unknown extensions. In contrast, a server that does support TLS 1.3 sends a supported_version extension containing the selected version (see IETF RFC 8446).

NOTE 8 The TLS 1.2 and TLS 1.3 ClientHello messages are compatible on the network binary level; i.e. all mandatory fields are present and have the same size in both revisions. TLS 1.3 is specified using extensions to the ClientHello message. Since both TLS 1.2 and TLS 1.3 implementations are required to ignore unknown extensions, a TLS 1.2 implementation can safely ignore any TLS 1.3 mandatory extension. If a TLS 1.3 peer is willing to negotiate TLS 1.2, it can accept the legacy ClientHello and respond with a legacy ServerHello or respectively accept a legacy ServerHello. Refer to IETF RFC 8446:2018, Annex D for further details.

[V2G20-2067] An SECC trying to establish legacy ISO 15118-2 communication shall not request EVCC to send the EVCC's certificate via "CertificateRequest" message.

NOTE 9 This ensures backwards compatibility with ISO 15118-2 utilizing unilateral authentication.

[V2G20-2068] The EVCC shall abort the handshake, if a downgrade is detected in the server's random value according to IETF RFC 8446.

[V2G20-2069] If the EVCC and SECC do not support the same TLS versions, TLS session setup will fail. For example, if the EVCC only supports TLS 1.3 while SECC only supports TLS 1.2, a TLS session setup request will fail. If TLS session setup process fails due to incompatible TLS versions, the EVCC shall abort the TLS setup process and apply [V2G20-1805].

[V2G20-2070] If the EVCC and SECC do not support the same TLS versions, TLS session setup will fail. For example, if the EVCC only supports TLS 1.3 while SECC only supports TLS 1.2, a TLS session setup request will fail. If TLS session setup process fails due to incompatible TLS versions, the SECC shall abort the TLS setup process and apply [V2G20-035].

### 7.8 V2G transfer protocol

#### 7.8.1 General information

The V2G transfer protocol (V2GTP) is a compact communication protocol to transfer V2G messages between two V2GTP entities. It mainly consists of a header and payload definition that allow to be