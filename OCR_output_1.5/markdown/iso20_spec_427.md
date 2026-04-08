A typical reason for losing the association status is when the driver was closely approaching an ACDP and decides to head for another ACDP afterwards. In this case the EV to EVSE association will be established according to the ACDP which the EV approached first. As soon as the EV leaves the PPD detection zone the association will quit. This is then a loss of association event. Then the SDP process will restart from the beginning.

[V2G20-4063] For early association support the association status between EV and EVSE shall be considered as being correctly associated as long as the continuously updated PPD information provides the same EVID as received by the SDP request when the element PPD/P2PS of the SDP request was set to value "PPD on infrastructure" according to Table 23.

[V2G20-4064] For early association support the association status between EV and EVSE shall be continuously supervised by the SECC when the element PPD/P2PS of the SDP request was set to value "PPD on infrastructure" according to Table 23.

[V2G20-4065] For early association support the SECC shall respond the latest V2G message request with the ResponseCode= FAILED_AssociationError when EV and EVSE are not correctly associated and then wait for a new SDP request when the element PPD/P2PS of the SDP request was set to value "PPD on infrastructure" according to Table 23.

[V2G20-4066] For early association support the SECC shall stop the supervision of the association status after the ACDP_VehiclePositioning has been finished with ResponseCode = OK and EVSEProcessing=Finished when the element PPD/P2PS of the SDP request was set to value "PPD on infrastructure" according to Table 23.

###### 8.6.4.6.3 Message flow

####### 8.6.4.6.3.1 Common message flow

[V2G20-1483] The SECC shall wait for supportedAppProtocolReq, set the timeout V2G_SECC_Sequence_Timeout to the value MessageType as defined in Table 215, reset the V2G_SECC_Sequence_Timer and start monitoring the V2G_SECC_Sequence_Timer.

NOTE 1 Before the first message, the SECC did not send any response message. Therefore, the SECC starts its sequence timer when starting to wait for the first message.

[V2G20-1484] After receiving a supportedAppProtocolReq, the SECC shall respond with a supportedAppProtocolRes within V2G_SECC_Msg_Performance_Time according to Table 215. The allowed next request shall be SessionSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1486] After receiving a SessionSetupReq, the SECC shall respond with a SessionSetupRes within V2G_SECC_Msg_Performance_Time according to Table 215. If the SECC is using "PLC", the allowed next request shall be AuthorizationSetupReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1970] After receiving the AuthorizationSetupReq, the SECC shall respond with an AuthorizationSetupRes within V2G_SECC_Msg_Performance_Time according to Table 215. If the AuthorizationSetupRes is sent with CertificateInstallationService set to "True", the next allowed request shall be CertificateInstallationReq or AuthorizationReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.