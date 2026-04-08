This type contains all elements of the EVPowerProfile that are only required in case the control mode "Dynamic" is chosen.

[V2G20-1875]

The SECC and the EVCC shall implement this type as defined in Table 105 and Figure 108.



Dynamic EVPPT Control Mode Type

<div style="text-align: center;">Figure 108 — Schema diagram - Dynamic EVPPT Control Mode Type</div>


<div style="text-align: center;">Table 105 — Semantics and type definition for Dynamic_EVPPTControlModeType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>n/a</td><td style='text-align: center; word-wrap: break-word;'>n/a</td><td style='text-align: center; word-wrap: break-word;'>n/a</td></tr></table>

NOTE This parameter does not contain any elements.

###### 8.3.5.3.12 Scheduled EVPPT Control Mode Type

This type contains all elements of the EVPowerProfile that are only required in case the control mode "Scheduled" is chosen.

[V2G20-1782]

The SECC and the EVCC shall implement this type as defined in Table 106 and Figure 109.



<div style="text-align: center;"><img src="imgs/img_in_image_box_221_777_897_871.jpg" alt="Image" width="56%" /></div>


<div style="text-align: center;">Figure 109 — Schema diagram - Scheduled_EVPPTControlModeType</div>


The elements of this message are used according to Table 106.

<div style="text-align: center;">Table 106 — Semantics and type definition for Scheduled_EVPPTControlModeType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SelectedScheduleTupleID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:numericIDTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Unique identifier of the selectedScheduleTuple</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>PowerToleranceAcceptance</td><td style='text-align: center; word-wrap: break-word;'>simpleType:powerToleranceAcceptanceTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional:This value is used to indicate if the EVCC acknowledges the PowerTolerance(s) sent by the SECC in ScheduleExchangeRes that was selected by the EVCC with the SelectedScheduleTupleID.This value can be set to &quot;PowerToleranceConfirmed&quot; for a positive reply or set to &quot;PowerToleranceNotConfirmed&quot; for a negative reply. This Element shall always be sent if a PowerTolerance has been provided by the SECC in the latest ScheduleExchangeRes.</td></tr></table>