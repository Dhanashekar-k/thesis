<PriceScheduleDescription>power_levels_plus_reverse</PriceScheduleDescription>
<Currency>EUR</Currency>
<Language>DEU</Language>
<PriceAlgorithm>urn:iso:std:iso:15118:-20:PriceAlgorithm:1-Power</PriceAlgorithm>
<PriceRuleStacks>
<PriceRuleStack>
<Duration>86400</Duration>
<PriceRule>
<EnergyFee>
<v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
<v2gci_ct:Value>20</v2gci_ct:Value>
</EnergyFee>
<PowerRangeStart>
<v2gci_ct:Exponent>0</v2gci_ct:Exponent>
<v2gci_ct:Value>0</v2gci_ct:Value>
</PowerRangeStart>
</PriceRule>
<PriceRule>
<EnergyFee>
<v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
<v2gci_ct:Value>10</v2gci_ct:Value>
</EnergyFee>
<PowerRangeStart>
<v2gci_ct:Exponent>4</v2gci_ct:Exponent>
<v2gci_ct:Value>1</v2gci_ct:Value>
</PowerRangeStart>
</PriceRule>
<PriceRule>
<EnergyFee>
<v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
<v2gci_ct:Value>-15</v2gci_ct:Value>
</EnergyFee>
<PowerRangeStart>
<v2gci_ct:Exponent>0</v2gci_ct:Exponent>
<v2gci_ct:Value>-1</v2gci_ct:Value>
</PowerRangeStart>
</PriceRule>
</PriceRuleStack>
</PriceRuleStacks>
</AbsolutePriceSchedule>

#### J.3.4 Overstay after charging finished

This example is about how to discourage overstays.

This example charges overstay rates after charging is finished. Initial parking fee is $4,00 with energy rate at $0,20/kWh. After charging is finished (power goes below 200 W), the overstay starts in an hour later with an additional $4,00/h. Three hours after charging is finished, the overstay changes to $8,00/h (overriding the rule "first"). Four hours after charging is finished, the overstay changes to $16/h.

The overstay fee is added to the normal parking and energy fees.
<?xml version="1.0" encoding="UTF-8"?>
<AbsolutePriceSchedule xmlns="urn:iso:std:iso:15118-20:CommonMessages"
                   xmlns:v2gci_ct="urn:iso:std:iso:15118-20:CommonTypes"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="urn:iso:std:iso:15118-20:CommonMessages./V2G_CI_Common_Messages.xsd">
    <TimeAnchor>1582842864000000</TimeAnchor>
    <PriceScheduleID>1</PriceScheduleID>
    <PriceScheduleDescription>parking_plus_overstay</PriceScheduleDescription>
    <Currency>USD</Currency>
    <Language>ENG</Language>
    <PriceAlgorithm>urn:iso:std:iso:15118-20:PriceAlgorithm:2-PeakPower</PriceAlgorithm>
    <PriceRuleStacks>
        <PriceRuleStack>
            <Duration>86400</Duration>
            <PriceRule>
                <EnergyFee>
                    <v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
                    <v2gci_ct:Value>20</v2gci_ct:Value>
                </EnergyFee>
                <ParkingFee>
                    <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                </EnergyFee>
                    <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                </EnergyFee>
            </EnergyFee>
        </EnergyFee>
    </EnergyFee>
    </EnergyFee>
</PriceScheduleID>

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program.

Copying not permitted. ©ISO. All rights reserved.