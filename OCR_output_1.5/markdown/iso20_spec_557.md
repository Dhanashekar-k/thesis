<PriceRuleStack>
    <Duration>86400</Duration>
    <PriceRule>
        <EnergyFee>
            <v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
            <v2gci_ct:Value>11</v2gci_ct:Value>
        </EnergyFee>
        <PowerRangeStart>
            <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
            <v2gci_ct:Value>0</v2gci_ct:Value>
        </PowerRangeStart>
    </PriceRule>
</PriceRuleStack>
</AbsolutePriceSchedule>

#### J.3.2 Different rates for different power levels

This example shows how to have different rates for different power levels. This example charges a higher rate for slow charging (0,20 €/kWh) and a lower rate for fast charging (0,10 €/kWh).

<px="urn:iso:std:iso:15118:-20:CommonMessages"

#### J.3.3 Different rates for different power levels including reverse power

This example shows how to have different rates for different power levels. This example charges a higher rate for slow charging (0,20 €/kWh) and a lower rate for fast charging (0,10 €/kWh), and a different rate for reverse power.

Note that the fee is negative for when the power is flowing from the EV.

<?xml version="1.0" encoding="UTF-8"?>
<AbsolutePriceSchedule xmlns="urn:iso:std:iso:15118:-20:CommonMessages"
xmlns:v2gci_ct="urn:iso:std:iso:15118:-20:CommonTypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
<TimeAnchor>1582842864000000</TimeAnchor>
<PriceScheduleID>1</PriceScheduleID>

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.