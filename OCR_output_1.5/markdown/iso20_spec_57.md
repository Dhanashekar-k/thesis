[V2G20-1017] A V2G entity shall fulfil the IPv6 node requirements specified in IETF RFC 8504.

[V2G20-1245] A V2G entity shall not use IPsec as defined by IETF RFC 8200 for the V2G communication.

NOTE 1 In case of ISO 15118-20 communication, TLS 1.3 is used to secure the communication between EVCC and SECC. To secure VAS, TLS 1.3 can also be used.

The IANA allocation guidelines for the routing type field in the IPv6 routing header are described in IETF RFC 5871. It is recommended to adhere to these guidelines.

[V2G20-1241] A V2G entity shall implement path MTU discovery according to IETF RFC 8201.

[V2G20-041] A V2G entity shall support handling of overlapping IP fragments according to IETF RFC 5722.

NOTE 2 IETF RFC 5722 has been updated by IETF RFC 6946. These updates are considered to be included in this document.

A V2G entity should comply with the specification in IETF RFC 5220, which extends IETF RFC 8200.

[V2G20-042] When sending an IPv6 packet from EVCC to SECC or from SECC to EVCC, no IP fragmentation shall be used.

It is recommended to use TCP segmentation to transmit a V2G message larger than the MTU.

The communication between EVCC and secondary actors as well as SECC and secondary actors is not in the scope of this document and may or may not use IP fragmentation.

[V2G20-1518] When sending an IPv6 packet containing energy transfer related communication from EVCC to SECC or from SECC to EVCC, the Traffic Class field in the IPv6 header shall be set to a value between 192 and 255.

[V2G20-1519] When sending an IPv6 packet containing non-energy transfer related value added service communication from EVCC to SECC or from SECC to EVCC, the Traffic Class field in the IPv6 header shall be set to a value between 0 and 127.

##### 7.6.2.2 Dynamic host control protocol (DHCPV6)

Data link requirements are described in ISO 15118-3 and ISO 15118-8. The EVCC starts the address assignment triggered by the Data-Link when a Data-Link connection is established. This is done according to 7.6.3.2 using SLAAC (Stateless auto address configuration), which is mandatory according to this document. DHCPv6 might be implemented as an optional IP configuration method.

[V2G20-1242] If an EVCC chooses to implement a DHCPv6 client, it shall implement it according to IETF RFC 8415.

[V2G20-1239] If the infrastructure chooses to implement a DHCPv6 server on an EVSE, it shall implement it according to IETF RFC 8415.

7.6.2.3 Neighbor discovery (ND)

The EVCC uses IPv6 SLAAC for generating addresses for its interface. All interfaces have a link-local address. To ensure unique addresses and to support global addresses, the neighbour discovery protocol (NDP) is used.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.