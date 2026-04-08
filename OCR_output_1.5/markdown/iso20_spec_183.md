## Figure 57 — Schema diagram - MeteringConfirmationRes

The elements of this message are used according to Table 53.

<div style="text-align: center;">Table 53 — Semantics and type definition for MeteringConfirmationRes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTypeRefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ResponseCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType:responseCodeTypeenumerationrefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>ResponseCode indicating the acknowledgment status of any of the V2G messages received by the SECC.</td></tr></table>

##### 8.3.4.4 AC messages

###### 8.3.4.4.1 Overview

Messages defined as AC messages belong to the AC message set(s).

###### 8.3.4.4.2 AC_ChargeParameterDiscoveryReq/Res

####### 8.3.4.4.2.1 AC_ChargeParameterDiscoveryReq/Res handling

After being authorized for charging at the EVSE (SECC) the EVCC and the SECC negotiate the energy transfer parameters with the AC_ChargeParameterDiscovery message pair.

Concepts treated for an optimal supply of energy that corresponds to the customer needs:

When using scheduled control mode, the energy transfer parameters negotiation that precedes the delivery of energy or may be engaged during the energy delivery phase is destined to ensure that the user will be satisfied while at the same time ensuring that the energy will effectively be available and fall within the capacity of power supply grid at the local level (private network) and at the regional level (public network). This required negotiation will become more and more necessary as the number of EVs increase, as well as an increase in volatility of local renewable energy production.

When using the dynamic control mode, the energy transfer parameters can be changed dynamically while in the charging loop, depending on the need of the EVSE.

####### 8.3.4.4.2.2 AC_ChargeParameterDiscoveryReq

By sending the AC_ChargeParameterDiscoveryReq message the EVCC provides its energy transfer parameters to the SECC. This message provides status information about the EV, i.e. the capabilities of the EV charging system.

[V2G20-1258]

The EVCC and the SECC shall implement the message elements as defined in Table 54 and Figure 58.

