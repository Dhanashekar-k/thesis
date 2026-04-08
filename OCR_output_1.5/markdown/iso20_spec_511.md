# Annex E (informative)

# Basic PPD for interoperability

### E.1 Overview

For ACDP the multi SECC communication architecture Figure 29 applies for multiple SECC architecture as described in 7.10.1.2.2. Also, ACDP requires wireless communication, and therefore wireless early SDP association also applies. In turn, the wireless SDP requires sufficient position information to correctly pair an EV and EVSE. Since there is only one access point in the multiple SECC architecture, this position information should come from an infrastructure mounted pairing and positioning device (PPD).

Since many different PPD technologies are available, this can present an interoperability obstacle. For example, if an EV arrives at an EVSE which does not support the same PPD technology as the EV, the early association SDP process will never complete, and the EV will not be able to charge. Therefore, a simple and low cost RFID PPD (vehicle portion) is defined in this clause to provide a basic level of PPD interoperability. It is not intended to preclude the addition of more sophisticated PPD systems for positioning and guidance.

The recommended way to implement a PPD is the RFID implementation. It shall be implemented as described in E.2. An alternative method is allowed but this can cause interoperability issues as EVSE and EV might not share the same PPD.

[V2G20-2716] A PPD is required. If there is only one ACDP EVSE, it can still be the case that a vehicle that is not in the right position can still communicate with the EVSE.

[V2G20-2717] The chosen PPD can be sufficiently accurate for the application it is used for, for example, directional WiFi can only be used in locations where vehicles have dedicated sufficiently separated lanes for charging.

### E.2 RFID implementation (recommended)

#### E.2.1 Functional description

The basic configuration of the RFID function is depicted in Figure E.1 and consists of four passive RFID tags on the EV roof and an active RFID reader fixed on the ACDP inverted pantograph. The reader head is fixed and not moving. The detection area of the RFID beam is adjusted to be a cone that is about the dimension of the bus roof thus it is larger than the contact interface but does not reach to a neighboring vehicle. The goal of the RFID system is to reliably read the EVID of the bus only when the vehicle is positioned in close proximity to the contact interface of the pantograph. This position may be at the edge or even outside of the contact field tolerances. Therefore, the RFID system cannot serve for position verification (positioning), but is sufficient for partitioning.