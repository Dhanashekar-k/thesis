Depending on the selected control mode, dynamic or sheduled, different elements may be mandatory or not used.

[V2G20-1214] In case dynamic control mode was selected, unless otherwise stated, anytime an element is prefixed with dynamic (e.g. Dynamic_SEReqControlMode), it shall be used. Anytime an element is prefixed with scheduled (e.g. Scheduled_SEReqControlMode), it shall not be used.

[V2G20-1215] In case scheduled control mode was selected, unless otherwise stated, anytime an element is prefixed with Scheduled (e.g. Scheduled_SEReqControlMode), it shall be used. Anytime an element is prefixed with dynamic (e.g. Dynamic_SEReqControlMode), it shall not be used.

As dynamic control mode delegate the energy transfer control to an off-board system, one could argue that this control mode is not necessary in DC. However, it is required to keep both control modes because the processes and information exchanges differ.

##### 8.4.2.2 Generator modes

The "GeneratorMode" parameter indicates if the system consisting of EV and EVSE operates as a grid following generator (only injecting active and reactive power) or as a grid forming generator.

GridForming: The system is able to control the voltage and frequency of the network and to power wires that would not be powered otherwise ("bootstrap" the network). The GridForming generator mode should be selected, for example, if the system consisting of EV and EVSE is powering up a remote load or the microgrid of a house.

GridFollowing: This mode should be used in situations when the system consisting of EV and EVSE is connected to the upstream distribution network, and would not act as one of the main grid forming generators of the network.

In DC energy transfer mode, one could argue that the GeneratorMode parameter might not be necessary, as the power electronic unit is located in the EVSE. However, the charging / discharging patterns will be different depending on the generator mode (ramps, depth of discharge, etc.) so the EV should still be informed at the beginning of the charging session in which mode it will be operating, and should still be able to refuse one mode.

#### 8.4.3 Selection of service and service parameters

##### 8.4.3.1 Overview

This subclause defines the reserved ServiceID ranges and the relevant services. These are exchanged and negotiated between the EVCC and the SECC by exchanging service discovery and service detail request response messages.

[V2G20-1355] The EVCC and the SECC shall implement the ServiceIDs as defined in Table 204.

NOTE 1 It is not mandatory for the EVCC or SECC to implement all these services. Table 204 simply defines the ServiceIDs to be used for the respective service if supported by the EVCC or SECC.

<div style="text-align: center;">Table 204 — Definition of ServiceID, ServiceName and ServiceCategory</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ServiceID (unsignedShort)</td><td style='text-align: center; word-wrap: break-word;'>ServiceName</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>Reserved by this document</td></tr></table>