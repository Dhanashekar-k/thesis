[V2G20-2252] If the CSO uses WPA3-Enterprise, its AP shall not support WPA3-Enterprise transition mode. Refer to WPA3 specifications for details.

[V2G20-2253] Regardless of WPA3-Enterprise is used or WPA2-Enterprise is used, the EV's WLAN STA (see ISO 15118-8 for details) shall implement MAC address randomization. Refer to WPA3 specifications for details.

[V2G20-2254] Regardless of WPA3-Enterprise is used or WPA2-Enterprise is used, the EV's WLAN STA (see ISO 15118-8 for details) shall implement "server certificate validation" to ensure that the AP that the EVCC connects to is a valid and trustworthy WLAN AP.

[V2G20-2256] The EVCC shall disable user override of server certificate (UOSC). Refer to WPA3 specifications for further details.

NOTE 2 This means TOD-STRICT (trust override disable strict) applies. This requirement applies to both WPA3-Enterprise and WPA2-Enterprise.

[V2G20-2255] The CSO shall provide an SECC certificate, as defined in Annex B, to the EVCC so that the EVCC can authenticate the CSO's authentication server.

[V2G20-2257] The EVCC shall authenticate CSO's authentication server with the certificate provided by the CSO's authentication server.

[V2G20-2258] The EVCC shall validate the provided certificate per [V2G20-1001] (with the SECC certificate profile as defined in Annex B).

NOTE 3 The EV can use its STA or the EVCC or another entity to perform this certificate validation.

[V2G20-2259] If the EVCC is unable to successfully authenticate the CSO’s authentication server, it shall decline to establish a wireless connection with the CSO’s access point.

[V2G20-2260] When the CSO’s authentication server requests EVCC to present its certificate to authenticate itself, the EVCC shall provide its vehicle certificate.

[V2G20-2261] The CSO’s authentication server shall authenticate the EVCC using the certificate provided by the EVCC.

[V2G20-2262] The CSO’s authentication server shall validate the provided certificate per [V2G20-1001] (with the vehicle certificate profile as defined in Annex B).

[V2G20-2263] If the CSO’s authentication server is unable to successfully authenticate the EV, it shall decline establishing a wireless connection with the EV. The CSO’s access point forwards the data traffic to the SECC only after CSO’s authentication server indicates successful mutual authentication via IEEE 802.1X.

[V2G20-2264] The CSO shall utilize the cipher suites as specified by Table 6 for EAP-TLS.

NOTE 4 Table 6 lists multiple cipher suites in the order of preference. Based on the configuration of the CSO's AP, only one of these cipher suites will be used for EAP-TLS. In general, the preferred cipher suite will be used for EAP-TLS. In case a security flaw was found in the preferred cipher suite, the AP can be configured to switch to the backup cipher suite as listed in Table 6.

[V2G20-2265] The EVCC shall utilize the cipher suite as specified by Table 6 for EAP-TLS.

NOTE 5 Table 6 lists multiple cipher suites in the order of preference. Based on the configuration of the EV's WLAN STA, only one of these cipher suites will be used for EAP-TLS. In general, the preferred cipher suite will be

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.