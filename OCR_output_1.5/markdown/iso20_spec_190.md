
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BPT_Scheduled_AC_CLResControlMode</td><td style='text-align: center; word-wrap: break-word;'>complexType:BPT_Scheduled_AC_CLResControlModeTyperefer to 8.3.5.4.7.5</td><td style='text-align: center; word-wrap: break-word;'>This element is used by the SECC for offering and setting parameters for scheduled control mode charging and discharging.</td></tr></table>

[V2G20-1555] The SECC shall send EVSETargetFrequency values only in situations when the EVSENominalFrequency is no longer the desired equilibrium point.

NOTE 1 This might be necessary in situations like the reconnection of residential power island to the main power grid.

The SECC shall not terminate the charging session only for the reason that an EVSETargetFrequency has not been achieved, as the frequency cannot be attributed to the EV's behavior.

NOTE 2 In AC power grids the frequency is the result of the collective behavior of all connected devices. The frequency is always drifting unless perfect equilibrium has been reached. The grid is typically never running at exactly the EVSENominalFrequency. The EVSENominalFrequency only defines a theoretical target frequency and provides a reference point for the definition of technical requirements which define the detection of and the reaction to abnormal situations. However, in some situations (power grid emergencies, small power islands, etc.) the desired frequency for the equilibrium point intentionally gets pushed outside the normal operating bandwidth. Only in those situations the EVSETargetFrequency can be used. The goal of the EVSETargetFrequency is to communicate the equilibrium point and to enable the EV's power inverter to operate in a robust way under extreme circumstances.

[V2G20-1558] In case EVCC selects the dynamic control mode with the service parameter MobilityNeedsMode set to "2", the SECC shall send a departure time in AC_ChargeLoopRes if it intends to update the DepartureTime sent in the latest ScheduleExchangeRes message.

[V2G20-2179] In dynamic control mode the SECC shall provide the target setpoints for the power transfer by the means of EVSETargetActivePower and EVSETargetReactivePower in AC_ChargeLoopRes.

##### 8.3.4.5 DC messages

###### 8.3.4.5.1 Overview

Messages defined as DC-Messages belong to the DC message set(s).

###### 8.3.4.5.2 DC_ChargeParameterDiscoveryReq/Res

####### 8.3.4.5.2.1 DC_ChargeParameterDiscoveryReq/Res handling

After being authorized for charging at the EVSE (SECC) the EVCC and the SECC negotiate the energy transfer parameters with the DC_ChargeParameterDiscovery message pair.

Concepts treated for an optimal supply of energy that corresponds to the customer needs.

When using scheduled control mode, the energy transfer parameters negotiation that precedes the delivery of energy or may be engaged during the energy delivery phase is destined to ensure that the user