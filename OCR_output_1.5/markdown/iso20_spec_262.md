TargetSOC or MinimumSOC as new Mobility Need information, the EVCC shall send updated DepartureTime, TargetSOC or MinimumSOC in the subsequent ChargeLoopReq.

[V2G20-1649] If the EVCC selected the service parameter MobilityNeedsMode set to 2 and the EVCC receives a ScheduleExchangeRes with DepartureTime, TargetSOC or MinimumSOC in Dynamic_SEResControlMode, and if the EV cannot accept this DepartureTime, TargetSOC or MinimumSOC, e.g. for internal reasons, the EVCC shall send different values in the subsequent ChargeLoopReq than the values in the ScheduleExchangeRes.

NOTE 1 In this case, the behavior of the SECC is not in scope.

NOTE 2 Both EVCC and SECC are expected to adapt the respective valid parameter and, if applicable, update their system, user interface, etc. with the information that is used for the session to ensure a high level of transparency and to avoid conflicting information to be displayed.

###### 8.3.5.3.16 Scheduled_SEResControlModeType

[V2G20-1318] The SECC and the EVCC shall implement this type as defined in Table 110 and Figure 113.

<div style="text-align: center;"><img src="imgs/img_in_image_box_345_712_911_778.jpg" alt="Image" width="47%" /></div>


<div style="text-align: center;">Figure 113 — Schema diagram - Scheduled_SEResControlModeType</div>


The elements of this message are used according to Table 110.

<div style="text-align: center;">Table 110 — Semantics and type definition for Scheduled_SEResControlModeType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ScheduleTuple</td><td style='text-align: center; word-wrap: break-word;'>complexType:ScheduleTupleTyperefer to 8.3.5.3.17</td><td style='text-align: center; word-wrap: break-word;'>Includes several tuples of schedules from secondary actors. The number of ScheduleTuple elements is limited to 3.If this element includes discharging service, relevant parameter especially power in PowerSchedule will be used with negative value.</td></tr></table>

NOTE 1 The EVCC can implement a mechanism to compare different ScheduleTuple elements in order to optimize the charge schedule considering any given kind of cost.

[V2G20-297] The first ScheduleTuple element shall be defined as the default schedule.

[V2G20-298] If the EVCC is not capable of comparing different ScheduleTuple elements or comparison fails, the EVCC shall choose the default ScheduleTuple according to [V2G20-297].

NOTE 2 If the SECC (or a secondary actor) is interested in the energy offered by the EVCC, it can use the information provided in the EVEnergyOffer and integrate it into one of the provided ScheduleTuples.

NOTE 3 The schedule to which an EVCC refers to via the ScheduleTupleID in the PowerDeliveryReq, always originates from the SECC.