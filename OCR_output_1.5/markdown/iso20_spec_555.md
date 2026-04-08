<PriceRuleStacks>
    <PriceRuleStack>
        <Duration>86400</Duration>
        <PriceRule>
            <EnergyFee>
                <v2gci_ct:Exponent>-2</v2gci_ct:Exponent>
                <v2gci_ct:Value>1</v2gci_ct:Value>
            </EnergyFee>
            <PowerRangeStart>
                <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                <v2gci_ct:Value>0</v2gci_ct:Value>
            </PowerRangeStart>
        </PriceRule>
    </PriceRuleStack>
</PriceRuleStacks>
</AbsolutePriceSchedule>

#### J.2.3 Energy and taxes

This example illustrates billing by the kWh, and now includes the taxes. Note that taxes are expressed in percent. This example charges $0.11 per kWh, and provides federal and state taxes.

<AbsolutePriceSchedule
    xmlns="urn:iso:std:iso:15118:-20:CommonMessages"
    xmlns:v2gci_ct="urn:iso:std:iso:15118:-20:CommonTypes"       xmlns:xsi="http://www.w3.org/2001/XMLSchema"
    instance" xsi:schemaLocation="urn:iso:std:iso:15118:-20:CommonMessages./V2G_CI_Common_Messages.xsd"
    <TimeAnchor>1582842864000000</TimeAnchor>
    <PriceScheduleID>1</PriceScheduleID>
    <PriceScheduleDescription>Fee_and_Tax_for_energy</PriceScheduleDescription>
    <Currency>USD</Currency>
    <Language>ENG</Language>
    <TaxRules>
        <TaxRule>
            <TaxRuleID>1</TaxRuleID>
            <TaxRuleName>Federal</TaxRuleName>
            <TaxRate>
                <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                <v2gci_ct:Value>5</v2gci_ct:Value>
            </TaxRate>
            <AppliesToEnergyFee>true</AppliesToEnergyFee>
            <AppliesToParkingFee>true</AppliesToParkingFee>
            <AppliesToOverstayFee>true</AppliesToOverstayFee>
            <AppliesMinimumMaximumCost>true</AppliesMinimumMaximumCost>
        </TaxRule>
        <TaxRule>
            <TaxRuleID>2</TaxRuleID>
            <TaxRuleName>State</TaxRuleName>
            <TaxRate>
                <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                <v2gci_ct:Value>1</v2gci_ct:Value>
            </TaxRate>
            <AppliesToEnergyFee>true</AppliesToEnergyFee>
            <AppliesToParkingFee>true</AppliesToParkingFee>
            <AppliesToOverstayFee>true</AppliesToOverstayFee>
            <AppliesMinimumMaximumCost>true</AppliesMinimumMaximumCost>
        </TaxRule>
    </TaxRules>
    <PriceAlgorithm>urn:iso:std:iso:15118:-20:PriceAlgorithm:1-Power</PriceAlgorithm>
    <PriceRuleStacks>
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
    </PriceRuleStacks>
</AbsolutePriceSchedule>

© ISO 2022 – All rights reserved
Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.