
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMaximumEnergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Maximum acceptable energy level of the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumEnergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>The energy request of the EV it needs to fulfil the minimum SOC as specified by the owner.NOTE This value is not to be understood as a guaranteed minimal amount of energy that is to be consumed by or factured to the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMaximumV2XEnergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Energy which may be charged until the PresentSOC has left the range dedicated for cycling activity. A negative value indicates that PresentSOC is above the V2X range.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVMinimumV2XenergyRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Energy which needs to be charged until the PresentSOC enters the range dedicated for cycling activity. A positive value indicates that PresentSOC is below the V2X range.</td></tr></table>

NOTE If the EVCC sends the parameters EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest, it is indicating a preferred operational V2X range (i.e. for bidirectional cycling) and the SECC can attempt to stay within these limits as long as possible.

[V2G20-2103] Unless defined otherwise DepartureTime in all messages shall always be larger than zero.

[V2G20-2104] Unless defined otherwise DepartureTime in all messages shall express the offset in seconds from the point in time of sending this message, which is marked in the TimeStamp element of the common V2G message header.

[V2G20-2681] If EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest are sent by the EVCC, they always need to be sent together.

[V2G20-2682] If the EVCC provides EVMaximumV2XEnergyRequest and EVMinimumV2XEnergyRequest, EVMinimumEnergyRequest shall be less than or equal to EVMinimumV2XEnergyRequest, which shall be less than or equal to EVMaximumV2XEnergyRequest, which shall be less than or equal to EVMaximumEnergyRequest.

###### 8.3.5.3.14 Scheduled_SEReqControlModeType

This type contains all elements of the ScheduleExchangeReq message that are only required in case the control mode Scheduled is chosen.

[V2G20-1753] The SECC and the EVCC shall implement this type as defined in Table 108 and Figure 111.