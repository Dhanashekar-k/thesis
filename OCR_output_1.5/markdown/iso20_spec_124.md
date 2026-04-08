An SDP server shall support the port V2G_UDP_SDP_SERVER as defined in Table 20 for receiving and sending SDP messages.

NOTE 3 Depending on the implementation of the EVCC, the dynamically assigned V2G\_UDP\_SDP\_CLIENT port is assigned once during or before the first transmission of a UDP packet to an SECC or can be dynamically re-assigned for each individual UDP request message and response. Also depending on whether messages are repeatedly sent, response messages can arrive asynchronously and cannot be associated to the exact corresponding request anymore.

[V2G20-126] The SDP client shall be able to handle asynchronously arriving SECC discovery response messages.

##### 7.10.1.4 Protocol data unit

###### 7.10.1.4.1 Structure

An SDP message is based on the V2GTP message format as defined in 7.8.3.1.

[V2G20-127] An SDP client shall support the definitions in 7.8.3.1.

[V2G20-128] An SDP client shall use a separate UDP packet for each request message.

[V2G20-129] An SDP client shall locate the first byte of the request message header as defined in Table 12 and Table 13 in the first byte of the UDP packet payload.

[V2G20-130] An SDP server shall support the definitions in 7.8.3.1.

[V2G20-131] An SDP Server shall use a separate UDP packet for each response.

[V2G20-132] An SDP server shall locate the first byte of the response message header as defined in Table 12 and Table 13 in the first byte of the UDP packet payload.

###### 7.10.1.4.2 Header processing

An SDP header processing is based on the V2GTP message header processing as defined in 7.8.3.2.

[V2G20-133] An SDP client shall apply to the header processing as defined in 7.8.3.2.

[V2G20-134] An SDP server shall apply to the header processing as defined in 7.8.3.2.

7.10.1.5 SECC discovery request message for communication according to ISO 15118-3

The SDP client uses the SECC discovery request message to request the IP address and the port number of the SECC.

[V2G20-135] Only an SDP client shall send SECC discovery request messages.

[V2G20-136] An SDP client shall send SECC discovery request messages with the source IP address on which it expects the SECC discovery response message.

[V2G20-137] An SDP client shall send SDP request messages to destination port V2G\_UDP\_SDP\_SERVER as defined in Table 20.

[V2G20-138] An SDP client shall send SDP request messages with source port V2G\_UDP\_SDP\_CLIENT as defined in Table 20 on which it expects the SECC discovery response message.