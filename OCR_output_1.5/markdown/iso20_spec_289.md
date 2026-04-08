
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td rowspan="3">AdditionalSelectedServices</td><td style='text-align: center; word-wrap: break-word;'>complexType</td><td style='text-align: center; word-wrap: break-word;'>Optional:</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>AdditionalServicesListType</td><td rowspan="2">A set of price rules for optional services (e.g. valet, carwash)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>refer to 8.3.5.3.57</td></tr></table>

[V2G20-1888] Only one currency shall be used for all AbsolutePriceSchedules.

NOTE 1 It is possible that the currency in EVAbsolutePriceSchedules can be different from the currency in AbsolutePriceSchedule.

NOTE 2 It is up to the SECC and EVCC to decide on how to handle currencies that are unexpected.

[V2G20-1889] The number of PriceRules shall not exceed the value of MaximumSupportingPoints.

[V2G20-1890] If MaximumCost is specified, then the element defines the maximum that may be billed.

[V2G20-1891] If MinimumCost is specified, then the element defines the minimum that may be billed.

[V2G20-2640] AdditionalSelectedServices shall not be included in the calculation of MaximumCost or MinimumCost.

[V2G20-1892] Each PriceScheduleID shall be unique.

[V2G20-1893] When a fee parameter is not sent, it shall mean this fee does not apply.

NOTE 3 This applies to all fee parameters: Maximum Cost, Minimum Cost, Energy Fee, Parking Fee and Service Fee.

####### 8.3.5.3.49.1 PriceAlgorithm identifiers

This document defines three identifiers for the PriceAlgorithm element:

urn:iso:std:iso:15118:-20:PriceAlgorithm:1-Power;

urn:iso:std:iso:15118:-20:PriceAlgorithm:2-PeakPower;

urn:iso:std:iso:15118:-20:PriceAlgorithm:3-StackedEnergy.

Their definition is based on the following, generic observations, which are illustrated in Figure 147, Figure 148 and Figure 149. In Figure 147, the example is for a set of PriceRule elements and their associated EnergyFee definitions. In the first hour after midnight (00:00) a PowerSchedule limit of 15 kW is in place and only one PriceRule exists. In the next hour (01:00 to 02:00) the PowerSchedule limit has increased to 30 kW and there are three different PriceRule entries, which are stacked based on their PowerRangeStart value. The pictured EnergyFee values are just examples and not relevant for the definition of the PriceAlgorithm choices.