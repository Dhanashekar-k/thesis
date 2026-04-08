<?xml version="1.0" encoding="UTF-8"?>
<n1:supportedAppProtocolRes xmlns:n1="urn:iso:15118:2:2010:AppProtocol"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
<|LOC_870|><|LOC_870|><|LOC_1000|><|LOC_870|><|LOC_1000|><|LOC_937|><|LOC_870|><|LOC_937|>
<ns:schemaLocation="urn:iso:15118:2:2010:AppProtocol
..\\V2G_CI_AppProtocol.xsd">
<ResponseCode>OK_SuccessfulNegotiation</ResponseCode>
<SchemaID>2</SchemaID>
</ns:supportedAppProtocolRes>

### 8.3 V2G message definition

#### 8.3.1 Overview

A V2G communication session in this document is defined as the exchange of V2G messages between two V2G entities in a predefined sequence (see 8.6) for managing the energy transfer process. A V2G communication session always starts with the SessionSetup message pair and always ends with the SessionStop message pair.

All messages of a V2G communication session carry a SessionID that allows to manage the V2G communication sessions between V2G entities on application level. The SessionID is negotiated by the EVCC and the SECC in the SessionSetup message pair. All V2G messages of a V2G communication session except the SessionSetupReq message use the same SessionID.

The SessionID enables pausing and resuming communication by the EVCC during a single service session using multiple V2G communication sessions. For this, the EVCC and the SECC apply the same SessionID in all V2G communication sessions during a service session. Applying multiple V2G communication sessions enables the EVCC to initiate a stop and, when resuming, to restart all layers while keeping the same application context and energy transfer process management data. This for example allows the EV and the EVSE to switch off the ISO 15118 communication module completely during pause to save energy.

In this document a V2G communication session pause is controlled by the parameter ChargingSession in SessionStopReq with its value set to "Pause". For the scheduled control mode the parameter should be used in conjunction with the EVPowerProfile. This means that an EVCC can initiate a pause at any time after sending PowerDeliveryReq with ChargeProgress equal to "Stop", but it needs to be ensured that this pause period is also reflected as a zero power phase in the previously agreed EVPowerProfile.

Instead of "Pause", an EVCC can alternatively enter a "Standby" period during a V2G communication session when no power transfer is needed but the V2G communication needs to be maintained. For example, the EVCC may choose standby over pause when pause and resuming of communication for a short duration is more costly than beneficial. Also, an EVCC may want to receive value added services while no power is transferred, requiring an active V2G communication session. In contrast to pause, standby allows for performing a schedule renegotiation with multiplexed communication. standby is applicable to all energy transfer modes.

In this document a standby period starts by a PowerDeliveryReq with ChargeProgress set to "Standby" and ends by a PowerDeliveryReq with ChargeProgress set to "Start" or "Stop".

EVSE may choose not to allow a standby period by replying with a PowerDeliveryRes with response code set to "WARNING_StandbyNotAllowed". In this case, the EV is expected to follow the initially agreed power profile or to trigger a schedule renegotiation.

An EV may use pause at its discretion in scheduled control mode. For example, EV may enter a pause period when battery depletion is expected during a zero power period due to its battery consumption for the communication. In dynamic control mode the EV is not expected to initiate a pause as this can pose a conflict with the grid side charging/discharging plan. Instead, the SECC can request the EVCC to pause in dynamic control mode.