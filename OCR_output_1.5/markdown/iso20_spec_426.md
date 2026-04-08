[V2G20-1481] At any stage of the V2G communication session, the SECC shall stop the V2G communication according to the requirements defined 7.4 when V2G_SECC_Sequence_Timer is equal or larger than V2G_SECC_Sequence_Timeout according to Table 215.

[V2G20-538] The SECC shall respond with the corresponding response message containing a "ResponseCode = FAILED_SequenceError" within V2G_SECC_Msg_Performance_Time according to Table 215, if request message was received that the SECC does not expect in the wait state.

[V2G20-1482] After sending a message containing a "ResponseCode = FAILED_SequenceError", the SECC shall behave according to the requirements defined in 7.4.

[V2G20-2222] After the SECC sent a ResponseCode starting with ‘FAILED’ or ‘FAILED_’ it shall terminate the communication by applying [V2G20-034].

8.6.4.6.2.1 ACDP error handling

[V2G20-4057] If SECC is using ServiceName = DC_ACDP, [V2G20-1482] does not apply.

[V2G20-4058] In case of any exception handling the SECC shall continue the communication to the EVCC until the last message pair of the exception handling procedure has been executed.

NOTE 1 The EVSE initiates an emergency shut down by ramping down the charging current, open its DC contactors and setting the CP signal to state E (0V). The EVSE will then raise the pantograph. Then the EVCC issues the SessionStop message to end the process. The ACDP_SystemStatus reflects the EVSE causing the emergency shut down. As described in IEC 61851-23.

[V2G20-4059] When SECC experiences an emergency situation, and EVCC is using ServiceName = DC_ACDP in Table 204 the EVSE shall set CP state to E.

NOTE 2 In case high level communication is disturbed or the ACDP is actually blocked from reaching the predefined safe position a procedure can be agreed upon to mobilize the EV in a safe way. A visual confirmation by the driver that the pantograph is actually in a safe position, after which he can manually get the EV in a mobilized state.

[V2G20-4060] If SECC is using ServiceName = DC_ACDP in Table 204, the SECC shall allow a SessionStopReq in case no ACDP_ConnectReq has been received.

[V2G20-4061] If SECC is using ServiceName = DC_ACDP in Table 204, the SECC shall allow receiving a ACDP_DisconnectReq after sending ACDP_ConnectDeviceRes, CableCheckRes, DC_ChargeLoopRes or PowerDeliveryRes.

[V2G20-4062] If SECC is using ServiceName = DC_ACDP in Table 204, after sending a message containing a "ResponseCode = FAILED" in SessionSetupRes or SupportedAppProtocolRes, the SECC shall behave according to the requirements defined in 7.4.

####### 8.6.4.6.2.2 ACDP exception handling in case of association loss

After the SDP process has been completed successfully the EV and the EVSE are associated correctly and the high-level communication starts. EV and EVSE are in the state "Associated". The association status of EVCC and SECC/EVSE shall continuously be supervised by the consistency of the received EVID by the PPD until the ACDP is activated successfully.