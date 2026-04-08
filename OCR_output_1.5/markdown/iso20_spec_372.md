
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>MobilityNeedsMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Mobility needs provided by EVCC2: Mobility needs provided by SECC allowed</td><td style='text-align: center; word-wrap: break-word;'>Indicate who can provide mobility needs information. Value 2 indicates that not only EVCC but also SECC can provide mobility-needs information (however, the EVCC shall always provide an initial mobility-needs information including DepartureTime). Value 2 can be selected only if DynamicControlMode was selected.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Pricing</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0: No pricing1: Absolute Pricing2: Price Levels</td><td style='text-align: center; word-wrap: break-word;'>Providing information about which pricing structure will be used in the offered schedules.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BPTChannel</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Unified2: Separated</td><td style='text-align: center; word-wrap: break-word;'>Type of installed power transfer channel.Unified: Single channelSeparated: Dual channel</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>GeneratorMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: GridFollowing2: GridForming</td><td style='text-align: center; word-wrap: break-word;'>Power converter behavior. For details see the IEC/TS 62898 series.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>GridCodeIslandingDetectionMethod</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1. ActiveDetection2. PassiveDetection</td><td style='text-align: center; word-wrap: break-word;'>Parameter to determine what method is used to detect landing.</td></tr></table>

NOTE 1 Each ParameterSetID includes all parameters for a specific setup.

<div style="text-align: center;">NOTE 2 The EV can maintain islanding situation, until the EVSE shuts it down.</div>


## [V2G20-2652]

In case the AC BPT service was selected, unless otherwise stated, anytime an element is prefixed with BPT or AC (e.g. BPT_AC_CPDReqEnergyTransferMode), it shall be used. In case both elements are available exclusively, BPT takes precedence.

The BPT channel parameter is used to make a distinction between single and dual channel architectures. In the former one, one single meter is used for the energy flows. In the later one, two separate meters are used for the two opposite energy flows. As a consequence, two switches are used and turned on / off depending on the current flow direction. The BPT channel parameter is used in both AC and DC charging services.

The following requirements apply in case of AC_BPT channel is equal to "separated" (e.g. dual channel) and the energy transfer needs to move from a charging phase to a discharging phase (or vice-versa):

## [V2G20-1468]

In case a service was selected where parameter BPTChannel was set to "2" (Separated), the SECC shall apply a power of 0 kW until contactors position are ready for the new phase.

In AC energy transfer mode, one could argue that the BPT Channel parameter might not be necessary, as the switch control operation is performed by the SECC. However, in case of a negotiated power profile (scheduled control mode), the EVCC should take into account the physical architecture (e.g. by planning 0 kW steps between charging and discharging phases).

## [V2G20-1469]

In case of bidirectional power transfer where parameter BPTChannel was set to "2" (Separated), both SECC and EVCC shall include 0 kW steps when switching from charging to discharging or vice versa.