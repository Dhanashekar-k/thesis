###### 7.10.1.10.1 Option for large number of SECC

The following optional requirements may be optional implemented in order to avoid a message avalanche of SDP response messages, when there is a very large number of SECCs in a depot in the same network.

[V2G20-4104] For early association support an SDP server shall wait a random number of milliseconds that is smaller than 100 ms before sending the SECC discovery response message with the payload parameter "DiagStatus = Finished with EVSEID" or "DiagStatus = Finished without EVSEID" as long as no EVID has been received by the pairing and positioning device that matches with the EVID of the SDP request. The parameter EVSEID may be sent optionally.

[V2G20-4105] For early association support and when [V2G20-4104] applies an SDP server may abort a pending SDP response message related to an SDP request with EVID when recognizing an SDP response message of another SDP server containing the same EVID.

###### 7.10.1.10.2 Loss of association PPD exception handling

After the SDP process has been completed successfully the EV and the EVSE are associated correctly and the high-level communication starts. The association status of EV and EVSE shall continuously be supervised by the consistency of the received EVID of the PPD until the ACDP is activated successfully. If the detected EVID changes or disappears the V2G process aborts.

A typical reason for losing the association status is when the driver was closely approaching an ACDP and decides to head for another ACDP afterwards. In such a case the association will first be established with the first ACDP. As soon as the EV leaves the PPD detection zone the existing association will quit. This is then a loss of association event. In case of a loss of association event the ACDP_VehiclePositioningRes will have the response code "FAILED_AssociationError".

##### 7.10.1.11 SDP for wireless communication application for WPT

By setting the CouplingType in the SDP request message to "WPT" the EV indicates that in intends to use wireless power transfer. As a consequence the P2PS/PPD parameter of the SDP request should be coded according to the P2PS options of the EV, which are featured for WPT.

Setting no bit typically indicates that the EV has no additional P2PS means and thus would apply WPT defaults or proprietary means. Since PPD is not used in combination with WPT, an error response of the SDP server can be expected if the P2PS/PPD parameter is coded for PPD support. Refer to IEC 61980-2 for P2PS specification and usage.

## 8 Application layer messages

### 8.1 General information and definitions

The vehicle to grid (V2G) application layer message definition describes the client-server based message exchange between EVCC and SECC for the purpose of initializing and configuring the energy transfer process from or to an EV. The message set is designed to cover the use cases defined in ISO 15118-1. The messages and the required message flow (i.e. communication protocol) represent the application layer according to the OSI layered architecture model.

A V2G message uses the EXI-based Presentation Layer as described in 7.9.1. The communication between EVCC and SECC at application layer level is based on client/server architecture. The EVCC always acts as a client (service requester) during the entire charging process, whereas the SECC always acts as a server (service responder). Hence the EVCC always initiates communication by sending a request message to