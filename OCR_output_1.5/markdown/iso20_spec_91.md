
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Payload type value</td><td style='text-align: center; word-wrap: break-word;'>Payload type identifier</td><td style='text-align: center; word-wrap: break-word;'>Explanation</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x8104</td><td style='text-align: center; word-wrap: break-word;'>ParkingStatusPayloadID</td><td style='text-align: center; word-wrap: break-word;'>EXI encoded V2G message on a multiplexed side stream for the purpose of delivering Parking Status information (see 8.6.5.3 and 8.3.4.8.1)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x8105 - 0x8FFF</td><td style='text-align: center; word-wrap: break-word;'>Not applicable</td><td style='text-align: center; word-wrap: break-word;'>Reserved for future use</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x9000</td><td style='text-align: center; word-wrap: break-word;'>SDPRequestPayloadID</td><td style='text-align: center; word-wrap: break-word;'>SDP request message (see 7.10.1.5)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x9001</td><td style='text-align: center; word-wrap: break-word;'>SDPResponsePayloadID</td><td style='text-align: center; word-wrap: break-word;'>SDP response message (see 7.10.1.6)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x9002</td><td style='text-align: center; word-wrap: break-word;'>SDPRequestWirelessPayloadID</td><td style='text-align: center; word-wrap: break-word;'>SDP request message for wireless communication (see 7.10.1.8)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x9003</td><td style='text-align: center; word-wrap: break-word;'>SDPResponseWirelessPayloadID</td><td style='text-align: center; word-wrap: break-word;'>SDP response message for wireless communication (see 7.10.1.9)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0x9004 - 0x9FFF</td><td style='text-align: center; word-wrap: break-word;'>Not applicable</td><td style='text-align: center; word-wrap: break-word;'>Reserved for future use</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0xA000 - 0xFFFF</td><td style='text-align: center; word-wrap: break-word;'>Not applicable</td><td style='text-align: center; word-wrap: break-word;'>Available for manufacturer specific use. Uniqueness of those identifiers is not guaranteed by this document.</td></tr></table>

NOTE 1 Only the payload type value numbers are technically used by the protocol. However, the requirements of this document reference those values by the associated identifier with the PayloadID suffix.

[V2G20-086] A V2GTP entity shall use the V2GTP message structure as shown in Figure 8 to send V2G messages as defined in Clause 8.

[V2G20-2307] A V2GTP entity shall use the definitions as defined in Table 13 and Table 14.

[V2G20-1229] For EXI encoded V2G messages (payload 0x8001 up to and including 0x8FFF) a V2GTP entity shall use a separate V2GTP message for each V2G message.

NOTE 2 Requirement [V2G20-1229] implies that the payload field can include neither a part of a message nor multiple messages.

##### 7.8.3.2 Header processing

For the processing of the payload the V2GTP entity processes the header first. For this, a V2GTP entity that receives a V2GTP message checks the header field step by step. The header processing as defined below is illustrated in Figure 11.

[V2G20-089] A V2GTP entity shall process the V2GTP header as defined in Table 13 before processing the payload as defined in Table 14.

[V2G20-090] A V2GTP entity shall check the protocol version and inverse protocol version fields (synchronization pattern) before any other header fields.

[V2G20-092] A V2GTP entity shall check the payload type after the successful check of the version and inverse version field.

[V2G20-094] A V2GTP entity shall check the payload length after the successful check of the payload type.

[V2G20-096] If the header processing was successful the V2GTP entity shall process the payload.