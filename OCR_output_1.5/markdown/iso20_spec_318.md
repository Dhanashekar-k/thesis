
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSETargetReactivePower_L3</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Target reactive power requested by the EVSE on phase L3 (as defined in 8.3.5.2.2)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEPresentActivePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Active power as presently measured by the EVSE. This value is based on the actual voltage and not the EVSENominalVoltage.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEPresentActivePower_L2</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Active power as presently measured by the EVSE on phase L2 (as defined in 8.3.5.2.2). This value is based on the actual voltage and not the EVSENominalVoltage.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEPresentActivePower_L3</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Active power as presently measured by the EVSE on phase L3 (as defined in 8.3.5.2.2). This value is based on the actual voltage and not the EVSENominalVoltage.</td></tr></table>

###### 8.3.5.4.7 AC BPT

[V2G20-1213] Parameters used for discharging the EV battery shall be set with a negative value, parameters used for charging shall be set with positive value. The following shall also apply for DC BPT (refer to 8.3.5.5.7).

Additionally, a typical reverse power transfer system can be equipped with new functionalities. This induces the need to add optional parameters to existing messages which, for example, indicate the direction of the energy transfer.

The technical characteristics of reverse power transfer systems can be defined with the help of two groups of parameters.

BPT Channel (Single channel or Dual Channel):

This parameter describes the usage of one or two channels, i.e. current line paths, for the use of transmitting Power for Charging and/or Discharging. In the single Channel Configuration the Power Transfer Channel is shared between charging and discharging. With the dual Channel Configuration there are two separate power transfer channels, one for the charging and one for discharging.

– Generator Mode (GridFollowing or GridForming):

The GeneratorMode parameter indicates if the system  $ \{EV + EVSE\} $ operates as a grid following generator (only injecting active and reactive power) or as a grid forming generator, which is able to control the voltage and frequency of the network. For more details see 8.4.2.

####### 8.3.5.4.7.1 BPT_AC_CPDReqEnergyTransferModeType

[V2G20-1456] The EVCC and the SECC shall implement this type as defined in Table 165 and Figure 174.