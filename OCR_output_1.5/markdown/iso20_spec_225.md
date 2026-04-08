The wireless communication for ACDP with infrastructure mounted pantograph requires early association of the EVCC with the associated SECC before the V2G communication can be started. This is needed to be able to control the EV positioning and ACDP activation processes correctly. For this the early association provides the required information as the EVID and EV position information.

For ACDP the multi SECC communication architecture according Figure 29 applies for multiple SECC architecture as described in 7.10.1.2.2.

For ACDP a pairing and positioning device (PPD) mounted on the infrastructure applies as described in EN 50696:2021, A.2 and A.3.

NOTE 1 An architecture using a single AP with single SECC, and single PPD can be viewed as a special version of the Multiple SECC architecture and is therefore also a permitted communication architecture.

NOTE 2 For ACDP mounted pantograph on the infrastructure the pairing and positioning device can be located on the infrastructure side. The identification object which holds the EVID is located on the EVs ACDP counterpart side. In this case the PPD can be able to read an identification mark positioned on or in the EV. The PPD identification method is used to ensure that the EV's EVID is detected only in close proximity of the EV to the EVSE so crosstalk to another EV is not possible (Partitioning). RFID identification tags are recommended to be present on the EV to ensure a basic level of interoperability. These tags are specified in Annex E.2.

NOTE 3 The EVID can be any unique identifier number or string. For electric bus applications it can comprise a readable name or, e.g. the EV number plate. For any other application it can be any random number which is unique at that time, thus privacy is not concerned.

The ACDP V2G communication consists of the following messages:

common messages;

- DC messages;

– ACDP specific messages.

####### 8.3.4.7.2.1 ACDP terminology

There are three distinct roles for the pairing and positioning device:

## Pairing

The EV connects to the right supply equipment communication controller (SECC) using the wireless SDP protocol in installations where there are several ACDP EVSEs in close proximity. This is a required role.

## Partitioning

The area around the ACDP is partitioned into a properly sized acceptance zone, outside which a charging session cannot be started. The zone should not be so small as to restrict the positioning leeway, but small enough that a nearby EV cannot inadvertently start a session and lower the ACDP such that a dangerous situation as a collision between the ACDP and another EV can occur. This is a required role for safety.

## Positioning

The driver can position the bus with enough precision that the ACDP contacts will connect with the ACDP counterpart contacts on the EV correctly so that correct charging is assured. This is an optional role for operational efficiency.

The pairing and positioning device provides a spatial selective orthogonal communication channel to the WLAN communication when the EV is in close proximity to the ACDP in order to resolve the undetermined association of the EV communication to the ACDP's EVSE. The PPD consists of a marker located on the EV and a receiver located in the ACDP infrastructure.

## 220 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.