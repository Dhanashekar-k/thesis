##### 7.6.3.1 General

This subclause specifies how an EVCC retrieves valid IP addresses to communicate over an IP-based network. The following addresses are considered for the purpose of this document:

- link local IP address of EVCC;

global IP address of EVCC, if router is present in local link;

– IP address of SECC.

NOTE An IPv6 host can have multiple IP addresses assigned to one physical network interface, e.g. link-local and global address.

##### 7.6.3.2 Stateless auto address configuration (SLAAC)

[V2G20-050] Each V2G entity shall support the configuration of a link-local IPv6 unicast address as specified in IETF RFC 4291.

NOTE 1 IETF RFC 4291 has been updated by IETF RFC 5952, IETF RFC 6052, IETF RFC 7136, IETF RFC 7346, IETF RFC 7371 and IETF RFC 8064. These updates are considered to be included in this document.

[V2G20-051] The interface ID of the link-local address of a V2G entity shall be generated from its IEEE 48 bit MAC identifier according to the definition in IETF RFC 4291.

[V2G20-052] The EVCC shall support auto configuration of IPv6 addresses as described in IETF RFC 4862.

NOTE 2 IETF RFC 4862 has been updated by IETF RFC 7527. These updates are considered to be included in this document.

##### 7.6.3.3 Address selection

[V2G20-1263] If multiple IPv6 addresses are supported, the IPv6 default address selection shall be performed according to IETF RFC 6724.

### 7.7 Transport layer

This subclause, and all subclauses provide specific and separate requirements for the private SECC and the SECC. Thus, unless otherwise specified for this subclause or any subclause within it, private SECC and SECC are not considered interchangeable.

#### 7.7.1 Transmission control protocol (TCP)

##### 7.7.1.1 Overview

The transmission control protocol (TCP) allows applications of V2G entities to establish a reliable data connection to other entities in order to exchange data in a reliable way and in-order. Additionally, TCP provides flow control and congestion control and also provides for various algorithms to handle congestion and influence flow control.

##### 7.7.1.2 Applicable RFCs, limitations and protocol parameter settings

[V2G20-055] Each V2G entity shall implement TCP as specified in IETF RFC 793.

## 54 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.