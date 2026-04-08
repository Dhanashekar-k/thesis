[V2G20-2626] If the check as described by [V2G20-2545] fails, i.e. this V2G communication session resumption request came from a different EVCC than the one with which the SECC had setup this particular V2G communication session, the SECC shall consider this as an attempt to start a new V2G session.

[V2G20-2627] If [V2G20-2626] applies, the SECC shall send a SessionID value in the SessionSetupRes message that is unequal to zero and unequal to the SessionID value received in SessionSetupReq message. The new SessionID shall meet [V2G20-2621]. The SECC shall indicate the setup of new V2G communication session with the ResponseCode in the SessionSetupRes message set to "OK_NewSessionEstablished" (refer also to [V2G20-462] for applicability of this response code).

NOTE 1 Refer to 8.6.3 for additional requirements of response codes applicable to the SessionSetupRes message.

[V2G20-2547] If the SECC receives a SessionSetupReq including a SessionID value which is not equal to zero and not equal to the SessionID value stored from the preceding V2G communication session, it shall send a SessionID value in the SessionSetupRes message that is unequal to zero and unequal to the SessionID value stored from the preceding V2G communication session and indicate the new V2G communication session with the ResponseCode set to "OK_NewSessionEstablished" (refer also to [V2G20-462] for applicability of this response code).

NOTE 2 Refer to 8.6.3 for additional requirements of response codes applicable to the SessionSetupRes message.

[V2G20-2613] If the check as described by [V2G20-2539] fails, i.e. the V2G communication session has not been resumed with the same SECC with which the EVCC had initially setup this same V2G communication session, the EVCC shall consider this as a new V2G communication session.

[V2G20-2614] If [V2G20-2613] applies, the EVCC shall purge all data associated with the paused V2G communication session and terminate that V2G communication session.

NOTE 3 Something went wrong if the V2G communication session has not been resumed with the same SECC with which the EVCC had initially setup this same V2G communication session. As such the safest course of action is to terminate this V2G communication session.

[V2G20-2615] If the EVCC received SessionSetupRes message with the ResponseCode set to "OK_NewSessionEstablished" and the SessionID set to a value different than the value that it sent in SessionSetupReq message to resume the previously paused V2G communication session, the EVCC shall consider this as a new V2G communication session.

[V2G20-2616] If [V2G20-2615] applies, the EVCC shall purge all data (including any authorizations) associated with the paused V2G communication session that the EVCC was trying to resume.

[V2G20-2617] If [V2G20-2615] applies, the EVCC shall follow normal steps to setup a new V2G session with new authorizations.

NOTE 4 In this case the EVCC will follow [V2G20-1484] and [V2G20-1486].

####### 8.3.4.1.4.3 Example of V2G session to vehicle/SECC certificate binding

This is just an example. It is not mandated to follow this methodology. The OEM, CSO, SECC manufacturer may decide to use another methodology.