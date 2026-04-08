identifier used for pairing fails it shall respond with a WPT_PairingRes message with the parameter ResponseCode equal to FAILED or WARNING_WPT.

NOTE 1 It is up to the implementation whether to give a response code FAILED or WARNING_WPT. In case of FAILED, the communication is terminated. In case of WARNING_WPT, the system allows to repeat the positioning and pairing procedure.

[V2G20-5065] If the SECC has received the WPT_PairingReq message with the parameter EVResultCode set to "EVResultFailed", then the SECC shall respond with a WPT_PairingRes message with the parameter ResponseCode equal to FAILED or WARNING_WPT.

[V2G20-5017] If the SECC has received the WPT_PairingReq message with the parameter ObservedIDCode set to a pairing identification code and the validation of the ObservedIDCode succeeds it shall respond with a WPT_PairingRes message with the parameter ResponseCode equal to "OK".

[V2G20-5018] If the SECC has identified a pairing code it shall respond to a WPT_PairingReq with a WPT_PairingRes message with the parameter ObservedIDCode set to the pairing identification code and the EVSEProcessing parameter set to "Finished".

[V2G20-5053] If [V2G20-5016] applies or the EVCC sent a WPT_PairingReq with the parameter EVResultCode set to "EVResultFailed, then the SECC should include AlternativeSECCList parameter in the PairingRes message when such information is available.

NOTE 2 The AlternativeSECCList provides a list of SECCs that the EVCC is recommended to connect to, in the order of priority, when the pairing process with the current SECC fails. Given the list, the EVCC can connect to those SECCs in the given order. For example, the EVCC connects to the wireless network with the provided SSID and start SDP protocol, or connect to the SECC by provided IP address and port number directly. How the list of alternative SECCs is obtained by the current SECC is not in the scope of this document.

###### 8.3.4.6.5 WPT_ChargeParameterDiscoveryReq/Res

The WPT_ChargeParameterDiscoveryReq and WPT_ChargeParameterDiscoveryRes messages are used to exchange information about the technical characteristics of the power transfer devices in order to tune the system components, accordingly.

By exchanging this information the final compatibility check of EV device and the supply device is performed (see IEC 61980-2).

####### 8.3.4.6.5.1 WPT_ChargeParameterDiscoveryReq/Res handling

After being authorized for charging at the EVSE (SECC) the EVCC and the SECC negotiate the energy transfer parameters with the WPT_ChargeParameterDiscovery message pair.

Concepts treated for an optimal supply of energy that corresponds to the customer needs below.

When using scheduled control mode, the energy transfer parameters negotiation that precedes the delivery of energy or may be engaged during the energy delivery phase is destined to ensure that the user will be satisfied while at the same time ensuring that the energy will effectively be available and fall within the capacity of power supply grid at the local level (private network) and at the regional level (public network). This required negotiation will become more and more necessary as the number of EVs increase, as well as an increase in volatility of local renewable energy production.