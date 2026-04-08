
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td rowspan="3">EVPCNaturalFrequency</td><td style='text-align: center; word-wrap: break-word;'>complexType</td><td rowspan="3">Self-resonance frequency of the EV device under fully loaded condition (primary device not present)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>RationalNumberType</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>refer to 8.3.5.3.8</td></tr><tr><td rowspan="2">EVPCDeviceLocalControl</td><td style='text-align: center; word-wrap: break-word;'>simpleType:</td><td rowspan="2">True, if EV device has a local control loop, which modifies reactance or power, false otherwise.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>xs:boolean</td></tr><tr><td rowspan="3">VendorSpecificDataContainer</td><td style='text-align: center; word-wrap: break-word;'>simpleType:</td><td style='text-align: center; word-wrap: break-word;'>Optional:</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>WPT_DataContainerType</td><td rowspan="2">Manufacturer specific data container, containing, e.g. manufacturer ID and Model ID</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>refer to Annex A for the type definition</td></tr></table>

NOTE The parameters related to current, power and voltage provided in WPT_ChargeParameterDiscovery message pair can be considered as physical limitations, meaning that they are related to the physical abilities of the system under rated operating conditions. Later during the charging process, depending on the external and environmental conditions (SOC, temperatures, etc.), the values of these limitations can change into more conservative values.

####### 8.3.4.6.5.3 WPT_ChargeParameterDiscoveryRes

With the WPT_ChargeParameterDiscoveryRes message the SECC provides applicable charge parameters from the grid's perspective.

[V2G20-5021] The SECC shall respond with a WPT_ChargeParameterDiscoveryRes with the ResponseCode = OK when the element values received from the EVCC allow a system setup for successful power transfer at the supply device.

[V2G20-5022] The SECC shall respond with a WPT_ChargeParameterDiscoveryRes with the ResponseCode = FAILED when the element values received from the EVCC do not allow a system setup for any power transfer at the supply device.

[V2G20-5066] The SECC shall respond with a WPT_ChargeParameterDiscoveryRes with the ResponseCode = WARNING_WPT when the element values received from the EVCC only allow a system setup for limited (significantly lower) power transfer at the supply device.

NOTE It is up to the implementation of the SECC when to response with WARNING_WPT or FAILED based on the system behavior.

[V2G20-5127] The EVCC and the SECC shall implement the message elements as defined in Figure 79 and Table 75.