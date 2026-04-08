<div style="text-align: center;">Figure 139 — Schema diagram - EVPowerScheduleType</div>


The elements of this message are used according to Table 136.

<div style="text-align: center;">Table 136 — Semantics and type definition for EVPowerScheduleType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>TimeAnchor</td><td style='text-align: center; word-wrap: break-word;'>simpleType:xs:unsignedLong</td><td style='text-align: center; word-wrap: break-word;'>The time that defines the starting point for the EVEnergyOffer.The value is encoded at microseconds resolution in SECC time, a concept that is defined in 8.3.3.3.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPowerScheduleEntries</td><td style='text-align: center; word-wrap: break-word;'>complexType:EVPowerScheduleEntryListTyperefer to 8.3.5.3.43</td><td style='text-align: center; word-wrap: break-word;'>List of EVPowerScheduleEntry elements.The number of EVPowerScheduleEntry elements is limited by the parameter MaximumSupportingPoints (according to [V2G20-1056]).</td></tr></table>

[V2G20-2138] The TimeAnchor of an EVPowerScheduleType element shall define the point in time when the first EVPowerScheduleEntry element starts to be active.

###### 8.3.5.3.43 EVPowerScheduleEntryListType

[V2G20-1883] The SECC and the EVCC shall implement this type as defined in Figure 140 and Table 137.

<div style="text-align: center;"><img src="imgs/img_in_image_box_257_796_861_865.jpg" alt="Image" width="50%" /></div>


<div style="text-align: center;">Figure 140 — Schema diagram - EVPowerScheduleEntryListType</div>


The elements of this message are used according to Table 137.

<div style="text-align: center;">Table 137 — Semantics and type definition for EVPowerScheduleEntryListType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVPowerScheduleEntry</td><td style='text-align: center; word-wrap: break-word;'>complexType:EVPowerScheduleEntryTyperefer to 8.3.5.3.44</td><td style='text-align: center; word-wrap: break-word;'>List of EVPowerScheduleEntry elements.The number of EVPowerScheduleEntry elements is limited by the parameterMaximumSupportingPoints (according to [V2G20-1056]).</td></tr></table>

###### 8.3.5.3.44 EVPowerScheduleEntryType

[V2G20-1884] The SECC and the EVCC shall implement this type as defined in Figure 141 and Table 138.

<div style="text-align: center;"><img src="imgs/img_in_image_box_328_1336_802_1425.jpg" alt="Image" width="39%" /></div>


<div style="text-align: center;">Figure 141 — Schema diagram - EVPowerScheduleEntryType</div>


The elements of this message are used according to Table 138.

## Table 138 — Semantics and type definition for EVPowerScheduleEntryType

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.