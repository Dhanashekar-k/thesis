separated and process V2G messages efficiently. V2GTP is the standard transfer protocol between the EVCC and SECC but may also be used for communication with other V2G entities that support the V2GTP protocol.

#### 7.8.2 Supported ports

V2GTP is based on TLS+TCP. TLS+TCP uses a pair of IP addresses (source address and destination address) and a pair of port numbers (source port and destination port) to establish and identify a connection for bidirectional exchange of byte streams. The connection is established from the source address and source port to the destination address and destination port. The ports listed in Table 10 are used by V2GTP entities.

<div style="text-align: center;">Table 10 — Supported TCP ports for V2GTP</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Name</td><td style='text-align: center; word-wrap: break-word;'>Protocol</td><td style='text-align: center; word-wrap: break-word;'>Port number</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_SRC_TCP_DATA</td><td style='text-align: center; word-wrap: break-word;'>TCP(unicast)</td><td style='text-align: center; word-wrap: break-word;'>Port number in the range of Dynamic Ports (49152-65535) as defined in IETF RFC 6335.</td><td style='text-align: center; word-wrap: break-word;'>V2GTP source port at a Primary Actor (e.g. EVCC) that implements the V2GTP protocol.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>V2G_DST_TCP_DATA</td><td style='text-align: center; word-wrap: break-word;'>TCP (unicast)</td><td style='text-align: center; word-wrap: break-word;'>Port number at V2GTP entity providing a V2GTP destination port number in the range of Dynamic Ports (49152-65535) as defined in IETF RFC 6335. For an SECC it will be dynamically assigned by the SDP mechanism (see 7.10.1)</td><td style='text-align: center; word-wrap: break-word;'>V2GTP destination port at a Primary Actor (e.g. SECC)</td></tr></table>

For V2GTP entities implementing the V2GTP the following general requirements apply.

[V2G20-073] A V2GTP entity providing a destination port shall support at least one connection on the local port V2G_DST_TCP_DATA as defined in Table 10.

NOTE 1 A V2GTP entity providing a destination port can support multiple simultaneous connections on the local port V2G_DST_TCP_DATA as defined by Table 10.

[V2G20-075] A V2GTP entity using a source port shall support at least one connection on the local port V2G_SRC_TCP_DATA as defined in Table 10.

NOTE 2 A V2GTP entity using a source port can support multiple connections on the local port V2G_SRC_TCP_DATA as defined in Table 10.

Especially, for an EVCC and an SECC the following applies.

[V2G20-077] The EVCC shall use a source port V2G_SRC_TCP_DATA as defined in Table 10.

[V2G20-078] The SECC shall provide a destination port V2G_DST_TCP_DATA as defined in Table 10.

[V2G20-079] The EVCC shall support at least one connection for a V2G communication session on port V2G_SRC_TCP_DATA.

[V2G20-080] The SECC shall support at least one connection for a V2G communication session on port V2G_DST_TCP_DATA.

[V2G20-081] The EVCC shall use the port V2G_DST_TCP_DATA returned in the last SECC discovery response message (refer to 7.10.1.6) for connecting the SECC.