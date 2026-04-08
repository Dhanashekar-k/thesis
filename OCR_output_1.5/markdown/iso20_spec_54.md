1 App layer communication protocol

2 IEEE 802.1X communication protocol

### Figure 10 — IEEE 802.1X example with backend authentication for WPT

RADIUS is not just limited to WPT, it can be used in other wireless communication use cases like ACDP or AC / DC wireless charging.

1. EV's WLAN STA (see ISO 15118-8 for details) uses WPA3-Enterprise or WPA2-Enterprise to build up a physical connection to a central access point (AP) (see ISO 15118-8 for details) of the infrastructure.

2. The AP forwards the connection request to the authorization server (AS) of the infrastructure via EAP (IEEE 802.1X with EAP pass-through-authentication).

3. After successful mutual authentication via RADIUS, the AP forwards the further establishment of the IP and service discovery protocol (SDP) connection of the EVCC to the central service discovery service. In the SDP request, the EVCC specifies the desired parameters of the electrical system. The central identification service sends back the transport address of the corresponding V2G application via SDP.

4. EVCC and SECC authenticate each other via transport layer security (TLS). The following assignment activity on the V2G application layer checks whether the EVSE can actually operate the EV with its electrical parameters or not.

5. EV now positions itself on the EVSE, uses the pairing and positioning device (PPD) to align itself with the energy transmission device and couples to the EVSE via SECC. After pairing, the EVCC causes the SECC to charge its EV battery.

In summary, it can be stated that RADIUS enables the establishment of an authenticated and encrypted channel on the data link layer, which guarantees the integrity and confidentiality between the EV and the infrastructure. This means that all protocols that use such a protected data connection are equally protected.

##### 7.5.1.3 Secure WLAN connection setup

[V2G20-2247] When the EVCC uses a wireless medium to establish a physical connection to an AP (see ISO 15118-8 for details), the EV's WLAN STA (see ISO 15118-8 for details) shall use WPA3-Enterprise or WPA2-Enterprise according to IEEE 802.1X.

[V2G20-2248] When the CSO offers a wireless medium to establish a physical connection to an AP (see ISO 15118-8 for details), the CSO shall use WPA3-Enterprise or WPA2-Enterprise according to IEEE802.1X.

NOTE 1 The AP is not required to support both WPA3-Enterprise and WPA2-Enterprise.

[V2G20-2249] If the EVCC uses WPA3-Enterprise, its STA device shall set protected management frames (PMF) to required. Refer to WPA3 specifications for details.

[V2G20-2250] If the CSO uses WPA3-Enterprise, its AP shall set protected management frames (PMF) to be required. Refer to WPA3 specifications for details.

[V2G20-2251] If the EVCC uses WPA3-Enterprise, its WLAN STA shall not support WPA3-Enterprise transition mode. Refer to WPA3 specifications for details.