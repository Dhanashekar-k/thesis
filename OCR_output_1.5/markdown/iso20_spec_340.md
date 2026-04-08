
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumChargePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Minimum charge power allowed by the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMaximumChargeCurrent</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Maximum charge current allowed by the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMaximumVoltage</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Maximum voltage allowed by the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumVoltage</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Minimum voltage allowed by the EV.</td></tr></table>

[V2G20-2183] In a DC_ChargeLoopReq the EVCC shall either provide a EVTargetVoltage or EVTargetCurrent value. The EVCC shall never provide both values in the same message.

[V2G20-2184] If the EVCC provides an EVTargetVoltage value, the EVTargetVoltage shall be defined in such a way, that it is logically consistent with the reported EVPresentVoltage. The target is reached if EVPresentVoltage is equal to EVTargetVoltage.

[V2G20-2185] The SECC shall adjust the voltage on the EVSE side in such a way, that the reported EVPresentVoltage matches the requested EVTargetVoltage as rapidly and closely as technically possible.

[V2G20-2186] If the EVCC provides an EVTargetCurrent value, the EVTargetCurrent shall be defined in such a way, that it is logically consistent with the reported EVSEPresentCurrent. The target is reached if EVSEPresentCurrent is equal to EVTargetCurrent.

[V2G20-2187] The SECC shall adjust the current on the EVSE side in such a way, that the reported EVSEPresentCurrent matches the requested EVTargetCurrent as rapidly and closely as technically possible.

[V2G20-2188] In its attempt to reach an EVTargetVoltage or EVTargetCurrent setpoint, the SECC shall never initiate an EVSE behavior which would violate any of the communicated and applicable limits (maximum and minimum values; for example, see [V2G20-2181] and [V2G20-2182]).

NOTE 1 Implementers can be aware that EVTargetVoltage and EVTargetCurrent will not necessarily be defining a simple CC/CV (constant current constant voltage) energy transfer strategy. For example, in the case of dynamic grid services the resulting power levels could change very rapidly. For this reason EVTargetVoltage and EVTargetCurrent can be interpreted as real targets and not as a replacement for upper limitation. Limits are communicated in other elements.

NOTE 2 In contrast to high voltage charging systems, where the EVPresentVoltage and EVSEPresentVoltage values might be almost identical, in very low voltage DC charging there might be a considerable voltage drop on the charging cable. For this reason it is important that [V2G20-2185] is implemented dutifully.

###### 8.3.5.5.5 Dynamic DC CLRes Control Mode Type

This type contains all elements of the DC_ChargeLoopRes message that are only required in case the control mode "Dynamic" is chosen.