An EVCC uses the SECC discovery protocol (SDP) to get the IP address and port number of the SECC. The SDP client sends out SECC discovery request messages to the local link (multicast) expecting any SDP server to answer its request with an SECC discovery response message containing this information.

After the EVCC received the IP address and the port number of the SECC, it can establish a transport layer connection to the SECC (refer to 7.3.4).

Depending on the physical communication layer different messages are used for the SECC discovery.

[V2G20-2273] If PLC communication according to ISO 15118-3 is applied, the SDP client in the EVCC shall use SECC discovery message with the payload type SDPRequestPayloadID (see Table 14).

[V2G20-2274] If PLC communication according to ISO 15118-3 is applied, the SDP client in the EVCC shall only accept SDP response messages with the payload type SDPResponsePayloadID (see Table 14).

[V2G20-2275] If the SDP server shall handle charging services with PLC (according to ISO 15118-3), the SDP server shall accept SECC discovery request messages with payload type SDPRequestPayloadID (see Table 14).

[V2G20-2276] An SDP server which is used for PLC communication according to ISO 15118-3 shall use SECC discovery response message for PLC with payload type SDPResponsePayloadID (see Table 14).

[V2G20-2277] If wireless communication according to ISO 15118-8 is applied the SDP client in the EVCC shall use SECC discovery message for wireless communication with the payload type SDPRequestWirelessPayloadID (see Table 14).

[V2G20-2278] If wireless communication according to ISO 15118-8 is applied, the SDP client in the EVCC shall only accept SDP response messages with the payload type SDPResponseWirelessPayloadID (see Table 14).

[V2G20-2279] If the SDP server shall handle charging services with wireless communication (according to ISO 15118-8), the SDP server shall accept SECC discovery request messages with payload type SDPRequestWirelessPayloadID (see Table 14).

[V2G20-2280] An SDP server which is used for wireless communication according to ISO 15118-8 shall use SECC discovery response message for wireless communication with payload type SDPResponseWirelessPayloadID (see Table 14).

7.10.1.2 Communication architectures

###### 7.10.1.2.1 Single SECC communication architecture

Within a single SECC communication architecture, multiple EVSEs share one common SECC. The SECC has a WLAN AP with an individual SSID. See Figure 28.