
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>AckMaxDelay</td><td style='text-align: center; word-wrap: break-word;'>simpleType:xs:unsignedShort</td><td style='text-align: center; word-wrap: break-word;'>Optional:This value indicates the maximum delay in seconds that SECC expects the EVCC to apply new mobility needs (DepartureTime or TargetSOC or MinimumSOC) and send updated values in a Charge Loop message since the reception of the message stating the AckMaxDelay.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumChargePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Maximum power the EVSE can deliver.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMinimumChargePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Any target power between this level and zero may, for technical reasons, result in a drop of the actual power to zero watts.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumChargeCurrent</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Maximum current the EVSE can deliver.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumVoltage</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Maximum voltage the EVSE can deliver.</td></tr></table>

[V2G20-1290] The SECC shall only send MinimumSOC that is less than or equal to TargetSOC.

[V2G20-1291] If the EVCC selected the service parameter "MobilityNeedsMode" set to 2 and the SECC received new values for departure time, target SOC or minimum SOC from a secondary actor, the SECC shall include those updated values in DepartureTime, TargetSOC or MinimumSOC, respectively. If TargetSOC or MinimumSOC are included, then the SECC shall also include AckMaxDelay.

[V2G20-1292] If the EVCC selected the service parameter MobilityNeedsMode set to 2 and receives a DC_ChargeLoopRes message with DepartureTime, TargetSOC or MinimumSOC, and if the EVCC accepts this DepartureTime, TargetSOC or MinimumSOC, then the EVCC shall send updated values in a DC_ChargeLoopReq within the number of seconds stated in AckMaxDelay of DC_ChargeLoopRes.

[V2G20-1294] If the EVCC selected the service parameter MobilityNeedsMode set to 2 and EVCC receives a DC_ChargeLoopRes message with DepartureTime, TargetSOC or MinimumSOC, and if the EVCC cannot accept this DepartureTime, TargetSOC or MinimumSOC, e.g. for internal reasons, then the EVCC shall send different values in a DC_ChargeLoopReq than the values in DC_ChargeLoopRes within the number of seconds stated in AckMaxDelay of the DC_ChargeLoopRes.

NOTE In this case, the behavior of the SECC is not in the scope.

###### 8.3.5.5.6 Scheduled_DC_CLResControlModeType

This type contains all elements of the DC_ChargeLoopRes message that are only required in case the control mode "Scheduled" is chosen.

[V2G20-1761]

The SECC and the EVCC shall implement this type as defined in Table 176 and Figure 185.

