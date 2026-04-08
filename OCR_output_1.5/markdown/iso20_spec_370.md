[V2G20-1931] To indicate that SECC is capable of a ServiceRenegotiation, the SECC shall set the parameter ServiceRenegotiationSupported to "True" in the first ServiceDiscoveryRes message of the service session. To indicate that the SECC is not capable of ServiceRenegotiation, the SECC shall set the parameter ServiceRenegotiationSupported to "False" in the first ServiceDiscoveryRes message of the service session.

[V2G20-1932] The SECC shall send the identical value for the parameter ServiceRenegotiationSupported for all ServiceDiscoveryRes messages throughout a service session.

##### 8.4.3.2 Service parameters for selected services

###### 8.4.3.2.1 General

This subclause defines the service parameter list tables sent in ServiceDetailRes for each of the defined services.

[V2G20-2712] Whenever an EVCC or SECC intends to use one of the services listed below, the requirements defined for the service that is intended to be used shall be supported. In case a service is not used, the respective clauses may be ignored.

###### 8.4.3.2.2 AC service

[V2G20-1356] The EVCC and the SECC shall implement the ServiceParameterList for AC charging as defined in Table 205.

<div style="text-align: center;">Table 205 — Configuration parameters for AC_Charging</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterName</td><td style='text-align: center; word-wrap: break-word;'>ParameterType</td><td style='text-align: center; word-wrap: break-word;'>Values</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Connector</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: SinglePhase2: ThreePhase</td><td style='text-align: center; word-wrap: break-word;'>Usage of the connector.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ControlMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Scheduled2: Dynamic</td><td style='text-align: center; word-wrap: break-word;'>Selection of which party (SECC or EVCC) is responsible to fulfill the mobility needs of this service session.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSENominalVoltage</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0 to 500</td><td style='text-align: center; word-wrap: break-word;'>Line voltage supported by the EVSE.This is the voltage measured between one phase and neutral. If the EVSE supports multiple phase energy transfer the EV might easily calculate the voltage between phases.This parameter is also used as reference for calculating the corresponding maximum charging current out of the Power values in the Schedule entities.</td></tr></table>