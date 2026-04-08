used for EAP-TLS. In case a security flaw was found in the preferred cipher suite, the WLAN STA can be configured to switch to the backup cipher suite as listed in Table 6.

[V2G20-2266] The CSO shall utilize the (elliptic curve) ECs as specified by Table 7 for EAP.

NOTE 6 Table 7 lists multiple curves in the order of preference. Based on the configuration of the CSO's AP, only one of these curves will be used for EAP-TLS. In general, the preferred curve will be used for EAP-TLS. In case a security flaw was found in the preferred curve, the AP can be configured to switch to the backup curve as listed in Table 7.

[V2G20-2267] The EVCC shall utilize the (elliptic curve) ECs as specified by Table 7 for EAP-TLS.

NOTE 7 Table 7 lists multiple curves in the order of preference. Based on the configuration of the EV's WLAN STA, only one of these curves will be used for EAP. In general, the preferred curve will be used for EAP. In case a security flaw was found in the preferred curve, the WLAN STA can be configured to switch to the backup curve as listed in Table 7.

[V2G20-2268] The CSO shall utilize ECDHE for EAP.

[V2G20-2269] The EVCC shall utilize ECDHE for EAP.

[V2G20-2270] The CSO shall utilize the signature algorithm as specified by Table 8 for EAP.

NOTE 8 Table 8 lists multiple signature algorithms in the order of preference. Based on the configuration of the CSO's AP, only one of these signature algorithms will be used for EAP. In general, the preferred signature algorithm will be used for EAP. In case a security flaw was found in the preferred signature algorithm, the AP can be configured to switch to the backup signature algorithm as listed in Table 8.

[V2G20-2271] The EVCC shall utilize the signature algorithm as specified by Table 8 for EAP.

NOTE 9 Table 8 lists multiple signature algorithms in the order of preference. Based on the configuration of the EV's WLAN STA, only one of these signature algorithms will be used for EAP. In general, the preferred signature algorithm will be used for EAP. In case a security flaw was found in the preferred signature algorithm, the WLAN STA can be configured to switch to the backup signature algorithm as listed in Table 8.

Since the SECC and the CSO's authentication server are two separate entities, the SECC certificate provided by the CSO's authentication server during IEEE 802.1X will likely not be the same as the SECC certificate provided by the SECC to setup the TLS session between the EVCC and the SECC. Similarly, the EVCC and the EV WLAN STA may be two separate entities, resulting in a different vehicle certificate for IEEE 802.1X communication compared to the certificate used during TLS session setup between the EVCC and the SECC. This should not result in any issues though as the WPA3-Enterprise (or WPA2-Enterprise) protected wireless communication is only between the EV's WLAN STA and the CSO's wireless AP while the TLS session protects the communication between the EVCC and the SECC involved in the energy transfer process.

### 7.6 Network link layer

#### 7.6.1 General

The protocol specified in this document is based on the internet protocol standard known as IPv6 (see IETF RFC 8200).

#### 7.6.2 Applicable RFCs, limitations and protocol parameter settings

7.6.2.1 IPv6

[V2G20-1244] A V2G entity shall support IPv6 as defined in IETF RFC 8200.