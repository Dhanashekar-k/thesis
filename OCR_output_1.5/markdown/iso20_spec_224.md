
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCMaxOutputPowerLimit</td><td style='text-align: center; word-wrap: break-word;'>complexTypeRationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Time varying maximum transmittable power of the supply power circuit given in Watt. The EVCC should not request more than this amount of power</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCMinOutputPowerLimit</td><td style='text-align: center; word-wrap: break-word;'>complexTypeRationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Time varying minimum transmittable power of the supply power circuit given in Watt. The EVCC should not request less than this amount of power, unless it will request 0 watts.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCChargeDiagnostics</td><td style='text-align: center; word-wrap: break-word;'>simpleType:WPT_SPCChargeDiagnosticsTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Diagnostics information, can have the following values: - NoIssue - FODDetected - LOPDetected - SPCTempOverheatDetected - SPCPowerTransferAnomalyDetected - SPCAnomalyDetected</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCOoperatingFrequency</td><td style='text-align: center; word-wrap: break-word;'>complexTypeRationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:SPC actual MF-WPT operating frequency in Hz</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SPCPowerControlParameter</td><td style='text-align: center; word-wrap: break-word;'>simpleType:WPT_SPCPowerControlParameterTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional:Additional parameters for the applied wireless power transfer method:Primary device coil current information</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ManufacturerSpecificDataContainer</td><td style='text-align: center; word-wrap: break-word;'>simpleType:WPT_DataContainerTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional:Manufacturer specific parameters:additional field for proprietary manufacturer specific information during power transfer (vendor specific information)</td></tr></table>

##### 8.3.4.7 ACDP messages

###### 8.3.4.7.1 Introduction and scope

The scope of the following subclause relates to ACDP for infrastructure mounted pantograph used for high power charging of electric busses or other commercial vehicles:

– ACDP with infrastructure mounted pantograph as specified in EN 50696:2021, A.2 and A.3;

- WLAN communication according to this document;

- WLAN communication layer according to ISO 15118-8;

– Electrical safety according to IEC 61851-23-1.

###### 8.3.4.7.2 Overview

The following clause describes the requirements for the WLAN based communication for an infrastructure mounted ACDP according to EN 50696:2021, Annex A using direct current.