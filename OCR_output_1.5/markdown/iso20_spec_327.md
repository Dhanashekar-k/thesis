
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumDischargePower_L2</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Any target power on phase L2 between this level and zero may, for technical reasons, result in a drop of the actual power to zero watts.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumDischargePower_L3</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>OptionalAny target power on phase L3 between this level and zero may, for technical reasons, result in a drop of the actual power to zero watts.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMaximumV2XEnergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:rationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Energy which may be charged until the PresentSOC has left the range dedicated for cycling activity. A negative value indicates that PresentSOC is above the V2X range.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumV2XEnergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:rationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Energy which needs to be charged until the PresentSOC enters the range dedicated for cycling activity. A positive value indicates that PresentSOC is below the V2X range.</td></tr></table>

NOTE If the EVCC sends the parameters EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest, it is indicating a preferred operational V2X range (i.e. for bidirectional cycling) and the SECC can attempt to stay within these limits as long as possible.

[V2G20-2124] If EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest are sent by the EVCC, they always need to be sent together.

[V2G20-2125] If the EVCC provides EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest, they shall follow the following mathematical relationship:

EVMinimumEnergyRequest ≤ EVMinimumV2XEnergyRequest ≤ EVMaximumV2XEnergyRequest ≤ EVMaximumEnergyRequest

####### 8.3.5.4.7.4 BPT_Scheduled_AC_CLReqControlModeType

This type contains all elements of the AC_ChargeLoopReq message that are only required in case the control mode Scheduled is chosen.

[V2G20-1766] The SECC and the EVCC shall implement this type as defined in Figure 177 and Table 168.