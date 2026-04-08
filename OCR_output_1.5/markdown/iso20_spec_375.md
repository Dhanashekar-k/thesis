[V2G20-1933] In case of bidirectional power transfer where parameter BPTChannel was set to "2" (Separated), both SECC and EVCC shall include 0 kW steps when switching from charging to discharging or vice versa.

[V2G20-2665] The SECC shall only offer MobilityNeedsMode equal to "2" when ControlMode is set to "2" (Dynamic).

###### 8.4.3.2.4 WPT service

An EV and an EVSE that can employ WPT as an energy transfer mode, will support all WPT related services as listed in Table 204 indicated by their corresponding ServiceIDs. For each service, extra information can be exchanged and validated for compatibility during the ServiceDetailReq/Res messaging.

####### 8.4.3.2.4.1 WPT Charging

For ServiceName "WPT" different service configurations can be supported. The SECC provides the supported configurations in a list of parameters as defined in Table 209.

[V2G20-5059] The SECC shall implement the ServiceParameterList for WPT service as defined in Table 209.

<div style="text-align: center;">Table 209 — Configuration parameters for WPT service</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterName</td><td style='text-align: center; word-wrap: break-word;'>ParameterType</td><td style='text-align: center; word-wrap: break-word;'>Values</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ControlMode</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Scheduled2: Dynamic</td><td style='text-align: center; word-wrap: break-word;'>Selection of which party (SECC or EVCC) is responsible to fulfill the mobility needs of this service session</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Pricing</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>0: No pricing1: Absolute Pricing2: Price Levels</td><td style='text-align: center; word-wrap: break-word;'>Providing information about which pricing structure will be used in the offered schedules.</td></tr></table>

The following applies if the EVCC enters a standby period while using WPT:

[V2G20-5023] After receiving a WPT\_AlignmentCheckRes, the EVCC shall not send a PowerDeliveryReq with ChargeProgress set to "Standby".

[V2G20-5060] When the EVCC wants to enter a standby period, after having received WPT_ChargeLoopRes, the EVCC shall send a PowerDeliveryReq with parameter ChargeProgress set to "Standby", while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-5064] After receiving the PowerDeliveryRes with ResponseCode equal to "OK" as a response to a previous PowerDeliveryReq message with ChargeProgress equal to "Standby", the EVCC shall send a WPT_ChargeLoopReq with PowerRequest set to zero, while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

[V2G20-5068] When the EVCC wants to exit a standby period, after having received WPT_ChargeLoopRes, the EVCC shall send a PowerDeliveryReq with ChargeProgress set to "Start", "Stop" or "ScheduleRenegotiation" while V2G_EVCC_Sequence_Timer is smaller than V2G_EVCC_Sequence_Performance_Time.

###### 8.4.3.2.5 ACDP service