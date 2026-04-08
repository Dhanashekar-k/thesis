[V2G20-1835] The currency which is used within one ScheduleTupleType with one ScheduleTupleID in the charge and the discharge schedule shall be the same.

###### 8.3.5.3.17 ScheduleTupleType

[V2G20-1319] The SECC and the EVCC shall implement this type as defined in Table 111 and Figure 114.

<div style="text-align: center;"><img src="imgs/img_in_image_box_305_367_818_510.jpg" alt="Image" width="43%" /></div>


<div style="text-align: center;">Figure 114 — Schema diagram - ScheduleTupleType</div>


The elements of this message are used according to Table 111.

<div style="text-align: center;">Table 111 — Semantics and type definition for ScheduleTupleType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ScheduleTupleID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:numericIDTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Mandatory for scheduled control mode, not applicable for dynamic control mode:Unique identifier within an energy transfer session for a ScheduleTuple element.An SAID remains a unique identifier for one schedule throughout an energy transfer session.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ChargingSchedule</td><td style='text-align: center; word-wrap: break-word;'>complexType:ChargingScheduleTyperefer to 8.3.5.3.40</td><td style='text-align: center; word-wrap: break-word;'>Encapsulating element describing all relevant details for the charging schedule.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DischargingSchedule</td><td style='text-align: center; word-wrap: break-word;'>complexType:ChargingScheduleTyperefer to 8.3.5.3.40</td><td style='text-align: center; word-wrap: break-word;'>Optional:Encapsulating element describing all relevant details for the discharging schedule.</td></tr></table>

NOTE 1 A ScheduleTuple contains different elements, two schedules (ChargingSchedule, DischargingSchedule) which all can originate from different secondary actors and therefore can communicate contradicting incentives. While the EV is required to operate within the given physical limits it is free to choose which incentive it wants to follow when deciding on the planned EVPowerProfile.

[V2G20-773] The SECC shall use the values 1 to 255 for the parameter ScheduleTupleID.

[V2G20-1560] The ScheduleTupleID element shall be unique for each ScheduleTuple during the entire charging session.

[V2G20-1561] The SECC shall provide a PowerSchedule element based upon the limits of the local installation if no secondary actor provides a PowerSchedule.

[V2G20-1011] If a secondary actor provided a PowerSchedule, the SECC shall ensure that no power value within the PowerSchedule exceeds the matching EVSEMaximumChargePower limit.