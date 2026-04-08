<div style="text-align: center;">Table 185 — Semantics and type definition for WPT_EVPCPowerControlParameterType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPCOilCurrentRequest</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>EVPC wants the primary device to set a specific (preferred) coil current value in amperes.NOTE The EVPC PowerRequest element is overriding the value given here in case of mismatch.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPCOilCurrentInformation</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Information about secondary device coil current (AC) in amperes</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPCCurrentOutputInformation</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Information about DC current supplied to the EV in amperes</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPCVoltageOutputInformation</td><td style='text-align: center; word-wrap: break-word;'>complexTypeRationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Information about DC bus or battery voltage in volts</td></tr></table>

####### 8.3.5.6.3.2 WPT_SPCPowerControlParameterType

[V2G20-5105] The EVCC and the SECC shall implement this type as defined in Figure 195 and Table 186.

<div style="text-align: center;"><img src="imgs/img_in_image_box_269_847_993_883.jpg" alt="Image" width="60%" /></div>


Figure 195 — Schema diagram - WPT_SPCPowerControlParameterType

The elements of this message are used according to Table 186.

<div style="text-align: center;">Table 186 — Semantics and type definition for WPT_SPCPowerControlParameterType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCPrimaryDeviceCoilCurrentInformation</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Information about the primary device coil current (AC) in amperes</td></tr></table>

###### 8.3.5.6.4 Data types related to fine positioning

The following complex data types are used in messages related to fine positioning. Refer to IEC 61980-2 for detailed information of the individual data and their application.

####### 8.3.5.6.4.1 WPT_LF_SystemSetupDataType

This data type contains information exchanged during the fine positioning setup. It relates to fine positioning methods LF_TxEV or LF_TxPrimaryDevice.

[V2G20-5106]

The EVCC and the SECC shall implement this type as defined in Figure 196 and Table 187.

