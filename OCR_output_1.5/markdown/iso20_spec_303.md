[V2G20-2162] If more than one ScheduleTuple containing PriceLevelSchedule is sent to the EVCC, they shall have the same NumberOfPriceLevels and priceLevels inside different ScheduleTupleless shall correspond to the same energy price.

[V2G20-2163] The TimeAnchor of a PriceLevelScheduleType element shall define a time that either is the present or some point in the near past.

[V2G20-2164] The NumberOfPriceLevels element shall be defined as the overall number of distinct PriceLevel elements used across all PriceLevelSchedules under the ScheduleTupleType elements.

EXAMPLE 1 If a PriceLevelSchedule is provided as part of the corresponding ScheduleTupleType element, where three different price levels for, for example, off-peak 0,5 € kWh ~ price level 1/3, for mid-peak 0,55 € kWh ~ price level 2/3, and for on-peak 1 € kWh ~ price level 3/3, are defined, the resulting value for NumberOfPriceLevels element is set to 3.

EXAMPLE 2 If only one flat rate PriceLevelSchedule is provided as part of the corresponding ScheduleTupleType element, with one price level at all times, the resulting value for the NumberOfPriceLevels element is set to 1.

EXAMPLE 3 If two PriceLevelSchedule are provided as part of the ScheduleTuple element, where the first PriceLevelSchedule S1 has three different price levels and the second PriceLevelSchedule S2 has another two differing price levels, the corresponding NumberOfPriceLevels element shall be set to 5.

[V2G20-2165] Both, EVCC and SECC shall support up to 100 price levels for the element NumberOfPriceLevels.

[V2G20-2166] In case the value of NumberOfPriceLevels is equal to "0", the value of PriceLevel shall be "0".

NOTE 1 The elements PriceLevel and NumEPriceLevels are set to "0" in case the secondary actor is not providing any price indication information for this schedule.

[V2G20-2167] A PriceLevelSchedule that is communicated as part of a ChargingScheduleType shall only present the price levels for power values that are equal to, or greater than 0 kW.

NOTE 2 For the PowerScheduleEntryType positive power values are to be used for charging of the EV.

[V2G20-2168] A PriceLevelSchedule that is communicated as part of a DischargingSchedule shall only present the price levels for all power levels that are less than 0 kW.

NOTE 3 For the PowerScheduleEntryType negative power values are to be used for discharging of the EV.

NOTE 4 A PriceLevel communicated as part of a DischargingSchedule is to be understood as indication of refund for the energy (power over duration) that is transferred from the EV into the grid.

8.3.5.3.63 PriceLevelScheduleEntryListType

The SECC and the EVCC shall implement this type as defined in Table 157 and Figure 166.

<div style="text-align: center;"><img src="imgs/img_in_image_box_253_1393_871_1442.jpg" alt="Image" width="51%" /></div>


## Figure 166 — Schema diagram — PriceLevelScheduleEntryListType

The elements of this message are used according to Table 157.

298 © ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.