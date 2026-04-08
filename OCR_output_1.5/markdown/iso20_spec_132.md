Table 14 if the element "CouplingType" of the SDP request message matches with the "CouplingType" type of the EVSE. Otherwise the SDP server shall not respond.

[V2G20-2293] For wireless communication the SDP server shall send the SECC discovery response message with the payload as defined in Table 26 and Table 27.

[V2G20-2294] For wireless communication an SDP server shall send the payload in the order as shown in Table 26 and Table 27. A byte with a lower number shall be sent before a byte with a higher number. The payload starts with byte 1 and ends with byte 59.

##### 7.10.1.10 SDP for wireless communication application for ACDP

WLAN communication according to ISO 15118-8 is deployed for, for example, ACDP with infrastructure mounted pantograph and uses the multiple SECC communication architecture. Each EVSE has its own pairing and positioning device (PPD) that provides information about the EVID when an EV is in close proximity to the ACDP. The EVCC uses the EVID information provided by the PPD within the SDP response message to initiate the correct associated communication between the EVCC and the related EVSE. For this the PPD will use the same EVID which is sent in the SDP request message.

Furthermore, the PPD may provide relative position information between the EV and the ACDP. This position information can be used to guide the driver to the correct EV x and y charging position within the mechanical tolerances of the ACDP. Only within these tolerances the EVSE is allowed to initiate the activation of the ACDP and to start the charging procedure.

The pairing and positioning device (PPD) provides a spatial selective orthogonal communication channel to the WLAN communication when the EV is in close proximity to the ACDP in order to resolve the undetermined association of the EV communication to the ACDP's EVSE. The PPD consists of a marker located on the EV and a receiver located in the ACDP infrastructure. The pairing and positioning identification method is not in the scope of this document. A possible design of a PPD is presented in Annex D.

For pairing and positioning device support the SDP client shall send SECC discovery request messages with the element EVID set the element PPD/P2PS to "PPD on infrastructure" according to Table 24 and leave the element EVSEID free.

NOTE 1 EVID can be set to a random number for privacy purposes. If no privacy is required, the EVID can be a readable string, e.g. as on an EV number plate.

[V2G20-4101] For pairing and positioning device support the SDP client shall reset the counter for sent SECC discovery request messages after a valid SECC discovery response message has been received with the payload parameter "DiagStatus = Ongoing".

[V2G20-4102] For wireless communication an SDP server shall send the SECC discovery response message with the payload parameter "DiagStatus = Ongoing" as long as no EVID is detected by the pairing and positioning device when the element PPD/P2PS of the SDP request was set to value "PPD on infrastructure" according to Table 24. The parameter EVSEID may be sent optionally.

NOTE 2 In case of "DiagStatus = Ongoing" the parameter EVSEID can be used in the EV to inform the driver about the available charging points.

[V2G20-4103] For wireless communication an SDP server shall send the payload parameters SECC IP address and port number and DiagStatus set to "Finished with EVSEID" or "Finished without EVSEID" as soon as the EVID has been detected by the pairing and positioning device.