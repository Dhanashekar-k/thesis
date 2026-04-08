## Annex J (informative)

# Absolute pricing examples

### J.1 Overview

Absolute pricing provides a means for the EV to figure out exactly how much the charging session will cost the driver. Absolute Pricing allows for the CSO to set prices for power, occupancy, overstay, taxes, and other extra selected services (e.g. valet, carwash).

### J.2 Simple examples

#### J.2.1 Parking fee only

The simplest example is where the CSO only charges the driver for parking the car in the charging spot. This example charges 5 € for 24 h of parking (all times are in seconds).

<?xml version="1.0" encoding="UTF-8"?>
<AbsolutePriceSchedule xmlns="urn:iso:std:iso:15118:-20:CommonMessages" xmlns:v2gci_ct="urn:iso:std:iso:15118:-20:CommonTypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:15118:-20:CommonMessages./V2G_CI_Common_Messages.xsd">
    <TimeAnchor>1582842864000000</TimeAnchor>
    <PriceScheduleID>1</PriceScheduleID>
    <PriceScheduleDescription>Day_of_Parking</PriceScheduleDescription>
    <Currency>EUR</Currency>
    <Language>FRA</Language>
    <PriceAlgorithm>urn:iso:std:iso:15118:-20:PriceAlgorithm:1-Power</PriceAlgorithm>
    <PriceRuleStacks>
        <PriceRuleStack>
            <Duration>86400</Duration>
            <PriceRule>
                <EnergyFee>
                    <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                    <v2gci_ct:Value>0</v2gci_ct:Value>
                </EnergyFee>
                <ParkingFee>
                    <v2gci_ct:Exponent>0</Exponent>
                    <v2gci_ct:Value>5</Value>
                </ParkingFee>
                <ParkingFeePeriod>86400</n1:ParkingFeePeriod>
                <PowerRangeStart>
                    <v2gci_ct:Exponent>0</v2gci_ct:Exponent>
                    <v2gci_ct:Value>0</v2gci_ct:Value>
                </PowerRangeStart>
                </PriceRule>
            </PriceRuleStack>
        </PriceRuleStacks>
    </AbsolutePriceSchedule>

#### J.2.2 Energy fee only

This example illustrates billing by the kWh. This example charges $0.11 per kWh.

<?xml version="1.0" encoding="UTF-8"?>
<AbsolutePriceSchedule xmlns="urn:iso:std:iso:15118:-20:CommonMessages"
xmlns:v2gci_ct="urn:iso:std:iso:15118:-20:CommonTypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:15118:-20:CommonMessages./V2G_CI_Common_Messages.xsd">
<TimeAnchor>1582842864000000</TimeAnchor>
<PriceScheduleID>1</PriceScheduleID>
<PriceScheduleDescription>Fee_for_energy</PriceScheduleDescription>
<Currency>USD</Currency>
<Language>ENG</Language>
<PriceAlgorithm>urn:iso:std:iso:15118:-20:PriceAlgorithm:1-Power</PriceAlgorithm>

© ISO 2022 – All rights reserved.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program.

Copying not permitted. ©ISO. All rights reserved.