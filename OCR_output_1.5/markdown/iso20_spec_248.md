[V2G20-1825] The EV shall adjust its energy transfer behavior to the new setpoints, that have been communicated by the EVSETargetActivePower and/or the EVSETargetReactive elements, as fast as technically feasible.

###### 8.3.5.2.2 Rules related to asymmetric polyphaser values

In order to support asymmetric polyphase energy transfers many elements which are related to power in the context of AC messages are provided in sets with phase specific variants. The following requirements apply to all such element sets unless explicitly stated otherwise in different requirements.

[V2G20-1814] For AC power phase specific element sets the line names L1, L2 and L3 shall identify the associated pins on the charging connector (e.g. as defined in IEC 62196).

NOTE This document only controls the energy exchange between the EV and the EVSE. In that context L1, L2 and L3 are clearly defined by the connector. A mapping to the associated lines at the grid connection point is only possible in the context of a specific installation within the premises and therefore out of the scope for this document.

[V2G20-1815] In the context of AC services with the connector choice SinglePhase only the power phase specific base elements (e.g. EVMaximumChargePower) shall be used. Elements with the suffix "L2" and "L3" shall not be used.

[V2G20-1816] In the context of AC services with the connector choice ThreePhase power phase specific elements with the suffix "L2" and "L3" shall be allowed.

[V2G20-1817] In the context of AC services with the connector choice ThreePhase the power phase specific base elements (e.g. EVMaximumChargePower) shall represent the sum of all three lines if neither the element sets peer with the suffix "L2" nor "L3" is present in the same message. If a sum value is communicated an even distribution across all three power phases shall be applied.

[V2G20-1818] In the context of AC services with the connector choice ThreePhase the power phase specific base elements (e.g. EVMaximumChargePower) shall identify the value associated with the L1 line if either the element sets peer with the suffix "L2" or "L3" is present in the same message.

[V2G20-1819] All requirements which apply to the base element (e.g. EVMaximumChargePower) of a power phase specific element set shall also apply to the peers with the suffix "L2" or "L3" in an equivalent way.

###### 8.3.5.2.3 Rules related to EV energy request values

The EV energy request parameters defined below are used by the EV to inform the EVSE of its energy demands and limitations. They are instantaneous values that will change over time during the energy transfer loops. They are calculated, updated and sent during the energy transfer loop by the EV and they form the foundation for the DynamicControlMode.

The EV shall ensure that at any time: EV Minimum Energy Level ≤ EV Target Energy Level ≤ EV Maximum Energy Level and therefore the resulting energy requests satisfy the following relationship: EVMinimumEnergyRequest ≤ EVTargetEnergyRequest ≤ EVMaximumEnergyRequest.

[V2G20-2191] In dynamic control mode the objective of the energy transfer plan shall be that at the end of the service session the EVTargetEnergyRequest will be less than or equal to zero.