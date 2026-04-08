## NOTE

IETF RFC 793 has been updated by IETF RFC 1122, IETF RFC 3168, IETF RFC 6093 and IETF RFC 6528. Additionally:

– IETF RFC 1122 has been updated by IETF RFC 2474, IETF RFC 5884, IETF RFC 6093, IETF RFC 6298, IETF RFC 6633, IETF RFC 6864 and IETF RFC 6;

– IETF RFC 3168 has been updated by IETF RFC 4301, IETF RFC 6040 and IETF RFC 8311;

– IETF RFC 2474 has been updated by IETF RFC 3186, IETF RFC 3260 and IETF RFC 8436;

– IETF RFC 8029 has been updated by IETF RFC 8611;

– IETF RFC 8584 has been updated by IETF RFC 7726;

– IETF RFC 4301 has been updated by IETF RFC 6040 and IETF RFC 7619.

All these updates are considered to be included in this document.

##### 7.7.1.3 TCP performance and checksum requirements

The following requirements define TCP implementation details relative to congestion control, retransmission, timing, initial window size and Selective Acknowledgement for the purpose of improving the overall performance of TCP.

It is recommended to use the following congestion control and retransmission algorithms in addition to the standard TCP methods:

[V2G20-057] Each V2G entity should implement TCP congestion control according to IETF RFC 5681.

[V2G20-059] Each V2G entity should compute TCP's retransmission timer according to IETF RFC 6298.

[V2G20-2134] Whenever a TCP retransmission timeout (RTO) is computed in a V2G entity, the RTO shall be lower than 400 ms.

[V2G20-2135] Whenever a TCP retransmission timeout (RTO) is computed in a V2G entity, the RTO should be in the range of 50 ms (lower bound) and 110 ms (upper bound).

NOTE While [V2G20-2134] defines the maximum upper bound allowed in this document, [V2G20-2135] provides a recommendation.

[V2G20-060] To increase TCP's performance each V2G entity should implement TCP extensions for high performance according to IETF RFC 7323.

[V2G20-062] Each V2G entity should implement the user timeout option according to IETF RFC 5482.

[V2G20-063] The urgent pointer for TCP should not be used by any V2G entity.

It is recommended to use the following checksum algorithm:

[V2G20-064] The checksum fields required in TCP headers should be implemented according to IETF RFC 1624.

[V2G20-2358] To improve packet loss handling, each V2G entity should implement selective acknowledgment (SACK) and selective repeat retransmission according to IETF RFC 2018.

#### 7.7.2 User datagram protocol (UDP)