[V2G20-167] Each entry in the list of supported EVCC protocols shall include the ProtocolNamespace, the VersionNumberMajor and VersionNumberMinor, the unique SchemaID dynamically assigned by the EVCC and the priority of the protocol entry. The priority in the EVCC request message enables the EVCC to announce the preferred application layer protocol where priority equal to "1" indicates the highest priority and priority equal to "20" indicates the lowest priority. The number of protocols included in the request message is limited to 20.

[V2G20-168] The SECC shall respond with the supportedAppProtocolRes message as depicted in Figure 33 indicating the protocol to be used for the subsequent message exchange by both, the EVCC and the SECC.

[V2G20-169] The response message shall include a ResponseCode and the SchemaID of the protocol/schema which is agreed as application protocol for the following V2G communication session. Thereby, the SECC shall select from its own list of supported protocols the protocol with highest priority indicated by the EVCC.

[V2G20-170] The SECC shall confirm (positively respond with ResponseCode "OK_SuccessfulNegotiation") an EVCC supported protocol even if the values of the VersionNumberMinor in EVCC request message does not match with the VersionNumberMinor of an SECC supported protocol where the VersionNumberMajor matches.

NOTE 1 A higher value in the VersionNumberMinor indicates that (in comparison to a lower value) additional data elements is transmitted from either the EVCC or SECC. Implementations only supporting the lower VersionNumberMinor value possibly are not able to process the data and could ignore this data. A difference in the VersionNumberMinor value between EVCC and SECC does not lead to an incompatibility. Refer to 8.2.4 showing examples for successful protocol negotiation.

An EVCC supporting multiple energy transfer modes may therefore add multiple entries for ISO 15118-20 (this document) in the supportedAppProtocolReq. As an example, an EVCC that supports both AC and DC would have two entries for ISO 15118-20, one with the namespace "urn:iso:std:iso:15118:-20:AC" and one with the namespace "urn:iso:std:iso:15118:-20:DC". Another example may be found in 8.2.4.1.

[V2G20-1039] If an EVCC supports the service AC and intends to offer it for this V2G communication session, it shall add an AppProtocol element to the supportedAppProtocolReq with ProtocolNamespace set to "urn:iso:std:iso:15118:-20:AC", VersionNumberMajor set to "1" and VersionNumberMinor set to "0".

[V2G20-2132] If an EVCC supports the service DC and intends to offer it for this V2G communication session, it shall add an AppProtocol element to the supportedAppProtocolReq with ProtocolNamespace set to "urn:iso:std:iso:15118:-20:DC", VersionNumberMajor set to "1" and VersionNumberMinor set to "0".

[V2G20-4107] If an EVCC supports the service ACDP and intends to offer it for this V2G communication session, it shall add an AppProtocol element to the supportedAppProtocolReq with ProtocolNamespace set to "urn:iso:std:iso:15118:20:ACDP", VersionNumberMajor set to "1" and VersionNumberMinor set to "0".

[V2G20-5126] If an EVCC supports the service WPT and intends to offer it for this V2G communication session, it shall add an AppProtocol element to the supportedAppProtocolReq with ProtocolNamespace set to "urn:iso:std:iso:15118:20:WPT", VersionNumberMajor set to "1" and VersionNumberMinor set to "0".