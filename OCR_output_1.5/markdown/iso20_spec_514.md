# Annex F (informative)

# Message sequencing for renegotiation

### F.1 Overview

This annex gives message sequence examples to make the comprehension of the schedule renegotiation mechanism easier.

In this document, the schedule renegotiation mechanism is used to change the target settings and EVPowerProfile during a charging loop without interruption of the ongoing charging message exchange. The schedule renegotiation message exchange is performed on a parallel side stream with V2GTP payload type ScheduleRenegotiationPayloadID V2G Messages. A schedule renegotiation can be initiated either by the EVCC or SECC.

To initiate a schedule renegotiation by the SECC, the SECC shall set the parameter EVSENotification to ScheduleRenegotiation in ChargeLoopRes. If so, the EVCC shall initiate a schedule renegotiation in a limited time (see also [V2G20-1845]).

To initiate a schedule renegotiation by the EVCC, the EVCC can decide to perform a schedule renegotiation by sending ChargeParameterDiscoveryReq on V2GTP payload type ScheduleRenegotiationPayloadID only after having sent at least one ChargeLoopReq message depending on the selected energy transfer services. (See also [V2G20-1846]).

In addition to the schedule renegotiation, this document also provides a ServiceRenegotiation. In comparison to the ScheduleRenegotiation, the ServiceRenegotiation is not intended to change certain target settings within a selected service (i.e. EVPowerProfile in AC scheduled control mode) but to enable the change or addition of the service selection (i.e. changing from unidirectional to bidirectional power flow or from scheduled into dynamic control mode, or adding a value-added service) within a service session. Unlike a schedule renegotiation, the ServiceRenegotiation is to be handled in sequence (V2GTP payload type Part20MainstreamPayloadID EXI encoded messages), therefore it is not multiplexed and cannot take place while energy transfer is in progress.

Depending on the operator's policy or the grid situation, the SECC can allow or disallow ServiceRenegotiation by setting the ServiceRenegotiationSupported parameter to "True" or "False", respectively, in the first ServiceDiscoveryRes message. This condition is valid until the end of the service session.

To initiate a ServiceRenegotiation by the SECC, the SECC shall set the parameter EVSENotification to "ServiceRenegotiation" in ChargeLoopRes. If triggered, the EVCC is expected to initiate a ServiceRenegotiation within the specified time (see [V2G20-1964], [V2G20-1969], [V2G20-1651], [V2G20-1661] and [V2G20-5080]).

To initiate a ServiceRenegotiation by the EVCC, the EVCC shall set the parameter "ChargeProgress" in PowerDeliveryReq to "Stop" and, depending on the currently selected energy transfer service, the corresponding message sequence to the SessionStopReq will be followed. In SessionStopReq the ServiceRenegotiation will be indicated by the parameter "ChargingSession" set to "ServiceRenegotiation". After having received a SessionStopRes message with ResponseCode set to "OK", the EVCC shall send a ServiceDiscoveryReq and renegotiate the service. (see [V2G20-1969], [V2G20-1661], [V2G20-1476] and [V2G20-1477]).