This subclause defines the selection method with respect to service and applied message set. The respective service will be selected through service discovery, service detail and service selection message exchanges.

Each request and response message exchange will select relevant service. These are summarized as follows.

- Service discovery:

The EVCC will request the available services from the SECC. The EVCC may pre-filter by sending the respective service IDs to only ask the SECC for services it is interested in. The SECC will answer with an appropriate list of supported services it can offer the EVCC. These may include user specific services.

- Service detail:

The EVCC will select the services it intends to use and sends the service IDs to the SECC for more detailed information. The SECC will answer with the parameter list of the chosen Service. This happens in a loop, for each Service the EVCC wants information it will send one service detail with one ServiceID.

- Service selection:

The EVCC will select the services by sending the selected ServiceID and the respective ParameterSetID to the SECC.

Charge parameter discovery:

EVCC and SECC exchange the physical limitations under rated operating conditions for the chosen energy transfer service.

EVCC and SECC will select and negotiate the service operation applied to the established service session through this message exchange. After the service operation is selected, the applied message set will be decided uniquely. A message set consists of multiple mandatory or optional messages with parameters, and it may cover multiple operation modes.

#### 8.4.2 General description of configuration parameters

##### 8.4.2.1 Control modes

Two control modes are available. Basically, a distinction is made between two main situations: (a) the EVCC is in charge of ensuring the mobility needs (scheduled control mode), or (b) ensuring the mobility needs is delegated to an off-board system (dynamic control mode).

- Scheduled: In the scheduled control mode, the SECC and the EVCC negotiate a power profile based on the information exchanged in the ScheduleList element. In this control mode, the EVCC is responsible for computing an EVPowerProfile compliant with the user's mobility needs.

Dynamic: In the dynamic control mode, the control is fully delegated to an off-board system. There are no negotiations needed in this mode. The EVCC sends parameters which describe the boundaries of the EV battery for energy usage to the SECC. The SECC then sends single power setpoints to the EVCC, which the EV should abide to. The off-board system in charge of the control is responsible for ensuring that the user's mobility needs will be satisfied. This control mode is particularly adapted to fast responding grid services.

2G20-1460] EVCC shall support dynamic and scheduled control mode for all supported energy transfer services.

[V2G20-1464] SECC shall support dynamic and scheduled control mode for all supported energy transfer services.

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.