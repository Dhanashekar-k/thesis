
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPowerProfile</td><td style='text-align: center; word-wrap: break-word;'>complexType: EVPowerProfileType refer to 8.3.5.3.9</td><td style='text-align: center; word-wrap: break-word;'>Optional: Used by the EV to announce and reserve a specific energy transfer profile for the current charging session. In dynamic control mode it describes a simulation from the EVs perspective on the fastest charging profile in order to reach the EVMaximumEnergyRequest under the constraint of the minimum of the EVSEMaximumChargePower and EVMaximumChargePower as communicated during the charge parameter discovery.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BPT_ChannelSelection</td><td style='text-align: center; word-wrap: break-word;'>simpleType: channelSelectionType refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional: Information Parameter from EV to show if &quot;Charging&quot; or &quot;Discharging&quot; is planned.</td></tr></table>

<div style="text-align: center;">NOTE 2 In dynamic control mode the purpose of the EVPowerProfile is to allow the EVSE to come up with a best effort prediction about the future EVs energy transfer limitations. It by no means defines the real energy transfer profile that will be applied by the EVSE. As the EVPowerProfile is an EV prediction based on the available data at the start of the session, the EVSE can consider the profile as an orientation which is subject to tolerance due to changing energy transfer and boundary conditions.</div>


[V2G20-1069]

In scheduled control mode, the SECC shall only communicate the parameter PowerTolerance in ScheduleExchangeRes if it intends to enforce a power transfer behavior which needs to stay within a PowerTolerance band (as defined in [V2G20-1870]), relative to the EVPowerProfile provided by the EVCC during the PowerDeliveryReq. This PowerTolerance band does not apply for time intervals when the power value defined by the EVPowerProfile is "zero". In this case the power and respective current flow shall be as close to zero as technically feasible.



[V2G20-1546] In all control modes the parameter EVPowerProfile, and in scheduled control mode also the parameter ScheduleTupleID, shall be sent if the parameter ChargeProgress in PowerDeliveryReq message is set to "Start", "Standby", "Stop" or "Pause".

####### 8.3.4.3.8.3 PowerDeliveryRes

After receiving the PowerDeliveryReq message of the EVCC the SECC sends the PowerDeliveryRes message including information if power will be available.

[V2G20-1262]

The EVCC and the SECC shall implement the message elements as defined in Table 47 and Figure 51.

