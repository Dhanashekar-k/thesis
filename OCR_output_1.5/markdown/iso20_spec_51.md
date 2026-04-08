### 7.5 Data link layer

The definitions in this document assume the data link layer to support the transport of IP packets as defined in the requirements. ISO 15118-3 and ISO 15118-8 define additional details on data link layer to be covered.

[V2G20-035]

If a V2G entity communicates by PLC, the V2G entity shall comply with ISO 15118-3



[V2G20-1015]

If a V2G entity communicates by WLAN, the V2G entity shall comply with ISO 15118-8.



#### 7.5.1 Data link layer security for WLAN

All wireless communication between the EVSE and the EV is inherently insecure unless specific security protocols are implemented. The reason is that the underlying physical layer protocol does not require authentication between the two parties trying to communicate with each other using WLAN. Additionally, all data sent over the WLAN is in plain text unless specific encryption protocols are implemented. This allows an adversary to not only access the WLAN network, but also to sniff and spoof the data being sent on the unprotected WLAN channel.

Although this document mandates TLS for most communications, SDP is sent before TLS is established. As such SDP is vulnerable to sniffing, spoofing, etc. In addition, since WLAN connection is established before TLS tunnel is setup, current specifications do not offer any way to authenticate the clients (EVs) trying to join a WLAN or the wireless access points offering ISO 15118 communication. For example, for an EV driving down the road, there is no way to identify whether the wireless access point that offers ISO 15118 communication is a legitimate EVSE or an attacker trying to establish a connection to the EV to try and compromise it.

Even if EV were to reject all messages/requests unless a TLS session is established, there are vulnerabilities that can be leveraged to scan the EV for other open vulnerabilities, etc. The same can be said for the EVSEs as well.

Currently the ISO 15118 series does not mandate any particular security or encryption methods on WLAN channels. Although security of wireless networks is optional in this document, it is highly recommended to use it. Unprotected wireless connections expose particularly high risks.

This subclause (and its subclauses) offers security on WLAN data link layer by allowing optional use of IEEE 802.1X. Usage of IEEE 802.1X allows establishment of an authenticated channel between the EV's WLAN STA device and the CSO's WLAN AP. Refer to ISO 15118-8 for details of WLAN, AP and STA.

It should be noted that EV's WLAN STA can be same as or different than EVCC. Similarly, CSO's WLAN AP could be same as or different than the SECC.

In addition to authentication, IEEE 802.1X allows optional encryption as well. This document takes advantage of this optional feature of IEEE 802.1X to provide integrity protection and ensure confidentiality of the data exchange between the WLAN access point(s) and the client(s) (EVs) trying to join the network. It also protects the EV by ensuring that the EV is joining a legitimate and secure WLAN network associated with charging infrastructure.

## [V2G20-2237]

If the CSO desires to secure access to their WLAN for EV-EVSE charging communications, the WLAN AP (see ISO 15118-8 for details) operated by that CSO shall implement all specifications in this subclause and the subclauses within.

NOTE 1 It is not mandatory for CSO to support these security mechanisms.