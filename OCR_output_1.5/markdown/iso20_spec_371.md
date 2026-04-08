
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>MobilityNeedsMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Mobility needs provided by EVCC2: Mobility needs provided by SECC allowed</td><td style='text-align: center; word-wrap: break-word;'>Indicate who can provide mobility needs information.Value 2 indicates that not only EVCC but also SECC can provide mobility-needs information (however, the EVCC shall always provide an initial mobility-needs information including DepartureTime). Value 2 can be selected only if Dynamic ControlMode was selected.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Pricing</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0: No pricing1: Absolute Pricing2: Price Levels</td><td style='text-align: center; word-wrap: break-word;'>Providing information about which pricing structure will be used in the offered schedules.</td></tr></table>

NOTE 1 Each ParameterSetID includes all parameters for a specific setup.

NOTE 2 In case a pricing method is offered that will not be used by the EVCC, the EVCC can ignore the provided information.

[V2G20-2651] In case the AC service was selected, unless otherwise stated, anytime an element is prefixed with AC (e.g. AC_CPDReqEnergyTransferMode), it shall be used.

[V2G20-2663] The SECC shall only offer MobilityNeedsMode equal to "2" when ControlMode is set to "2" (Dynamic).

8.4.3.2.2.1 AC BPT

[V2G20-1361] The EVCC and the SECC shall implement the ServiceParameterList for AC bidirectional power transfer services as defined Table 206.

<div style="text-align: center;">Table 206 — Configuration parameters for AC BPT service</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterName</td><td style='text-align: center; word-wrap: break-word;'>ParameterType</td><td style='text-align: center; word-wrap: break-word;'>Values</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Connector</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: SinglePhase2: ThreePhase</td><td style='text-align: center; word-wrap: break-word;'>Usage of the connector.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ControlMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Scheduled2: Dynamic</td><td style='text-align: center; word-wrap: break-word;'>Selection of which party (SECC or EVCC) is responsible to fulfill the mobility needs of this service session.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSENominalVoltage</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0 to 500</td><td style='text-align: center; word-wrap: break-word;'>Line voltage supported by the EVSE.This is the voltage measured between one phase and neutral. If the EVSE supports multiple phase energy transfer the EV might easily calculate the voltage between phases.This parameter is also used as reference for calculating the corresponding maximum charging current out of the power values in the schedule entities.</td></tr></table>