[V2G20-2664] The SECC shall only offer MobilityNeedsMode equal to "2" when ControlMode is set to "2" (dynamic).

8.4.3.2.3 DC service

[V2G20-1357] The EVCC and the SECC shall implement the ServiceParameterList for DC charging as defined in Table 207.

<div style="text-align: center;">Table 207 — Configuration parameters for DC_Charging</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterName</td><td style='text-align: center; word-wrap: break-word;'>ParameterType</td><td style='text-align: center; word-wrap: break-word;'>Values</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Connector</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Core2: Extended3: Dual24: Dual4</td><td style='text-align: center; word-wrap: break-word;'>Usage of the connector.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ControlMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Scheduled2: Dynamic</td><td style='text-align: center; word-wrap: break-word;'>Selection of which party (SECC or EVCC) is responsible to fulfill the mobility needs of this service session.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>MobilityNeedsMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Mobility needs provided by EVCC2: Mobility needs provided by SECC allowed</td><td style='text-align: center; word-wrap: break-word;'>Indicate who can provide mobility needs information. Value 2 indicates that not only EVCC but also SECC can provide mobility-needs information (however, the EVCC shall always provide an initial mobility-needs information including DepartureTime). Value 2 can be selected only if DynamicControlMode was selected.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Pricing</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0: No pricing1: Absolute Pricing2: Price Levels</td><td style='text-align: center; word-wrap: break-word;'>Providing information about which pricing structure will be used in the offered schedules.</td></tr></table>

NOTE 1 Each ParameterSetID includes all parameters for a specific setup.

NOTE 2 In case a pricing method is offered that will not be used by the EVCC, the EVCC can ignore the provided information.

[V2G20-2653] In case the DC service was selected, unless otherwise stated, anytime an element is prefixed with DC (e.g. DC_CPDReqEnergyTransferMode), it shall be used.

[V2G20-2666] The SECC shall only offer MobilityNeedsMode equal to "2" when ControlMode is set to "2" (Dynamic).

8.4.3.2.3.1 DC BPT

If the EVCC requires DC BPT service, the SECC provides relevant service parameter list.

[V2G20-1360] The EVCC and the SECC shall implement the ServiceParameterList for DC bidirectional power transfer services as defined in Table 208.

Table 208 — Configuration parameters for DC BPT service

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.