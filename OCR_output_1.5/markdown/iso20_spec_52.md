[V2G20-2238] If the OEM wants their EVs to access CSO's secure WLAN for EV-EVSE charging communications, the WLAN STA (see ISO 15118-8 for details) in the OEM's EV shall implement all specifications in this subclause and the subclauses within.

NOTE 2 It is not mandatory for the OEM to support these security mechanisms.

[V2G20-2239] It is up to the CSOs discretion whether to allow an EV that does not support the required security for WLAN to access the CSO's secure WLAN for EV-EVSE charging communications.

NOTE 3 The CSO is free to decline access to such EVs to access the CSO’s WLAN.

NOTE 4 If the CSO goes through the effort of securing their WLAN for EV-EVSE charging communications, the CSO will likely not accept insecure connections to its WLAN.

[V2G20-2240] It is up to the OEM's discretion whether to allow an EV that supports security for WLAN to access a CSO's unsecured WLAN for EV-EVSE charging communications.

NOTE 5 The OEM (EV) is free to decline connections to insecure WLAN.

##### 7.5.1.1 Applicable RFCs

The security on the data link layer is ensured through the use of IEEE 802.1X. It is part of the IEEE 802.11-2020 group of network protocols. IEEE 802.1X defines the encapsulation of the extensible authentication protocol (EAP) via IEEE 802.11-2020. EAP is an authentication framework that supports multiple authentication methods. EAP works directly over data link layers (IEEE 802) without the need for IP. EAP encapsulation can be used for both wired and wireless media. This document strongly recommends the use of IEEE 802.1X for connections utilizing wireless media.

[V2G20-2241] A V2G entity shall implement IEEE 802.1X.

NOTE 1 These requirements are normally not implemented in the SECC or EVCC. The OEM would normally implement these requirements in the WLAN STA. The CSO/PE operator would normally implement these requirements in the WLAN AP.

[V2G20-2242] IETF RFC 3748 shall be used as the encapsulation of IEEE 802.1X.

NOTE 2 IETF RFC 3748 has been updated by IETF RFC 5247 and IETF RFC 7057. IETF RFC 5247 has been updated by IETF RFC 8940. All these updates are considered to be included in this document.

[V2G20-2243] Remote authentication dial-in user service (RADIUS) as specified by IETF RFC 3579 shall be used as "pass-through peer" implementation of IETF RFC 3748 by the CSO/PE operator.

NOTE 3 IETF RFC 3579 has been updated by IETF RFC 5080. These updates are considered to be included in this document.

[V2G20-2244] The V2G entity shall use EAP extension EAP-TLS, as specified by IETF RFC 5216. TLS 1.3 shall be used for EAP-TLS.

NOTE 4 At the time of writing, an update of RFC 5216 for EAP-TLS with TLS 1.3 was still in progress. Once it has been released, this update will become applicable according to [V2G20-2244].

###### 7.5.1.1.1 Applicable RFCs for RADIUS