NOTE 7 In this case the EVCC will follow [V2G20-2097], [V2G20-2098] or [V2G20-5046], depending on the energy transfer mode selected. Authorization from previous V2G communication session is used. As such the EVCC will bypass the authorization messages.

[V2G20-2623] If [V2G20-2622] applies, the SECC shall provide confirmation of continuation of the charging session by sending a SessionSetupRes message including the SessionID it received in the SessionSetupReq message (stored SessionID value) and indicating the resumed V2G communication session with the ResponseCode set to "OK_OldSessionJoined" (refer also to [V2G20-463] for selecting the appropriate response code).

[V2G20-2539] If the EVCC received SessionSetupRes message with the ResponseCode set to "OK_OldSessionJoined" and the SessionID set to the same value that it sent in SessionSetupReq message to resume the previously paused V2G communication session, the EVCC shall check that it is still connected to the same SECC with which it had initially setup this particular V2G communication session. The exact methodology for this check is left up to the OEM.

NOTE 8 An example of this methodology is provided in 8.3.4.1.1.

[V2G20-1032] After resuming a previously paused V2G communication session, following a SessionSetupReq, the SECC shall respond with a SessionSetupRes within V2G_SECC_Msg_Performance_Time according to Table 215. The allowed next request shall be ChargeParameterDiscoveryReq within the V2G_SECC_Sequence_Timeout according to Table 215.

NOTE 9 In case of a resumed session, the AuthorizationReq/Res messages are not required as authorization details of the previous communication session are valid for the whole service session, see [V2G20-1844].

[V2G20-2628] If a new SessionID was assigned per [V2G20-2627] or [V2G20-2547], the SECC shall consider this as a new V2G session. The SECC shall not apply any previously stored authorizations to this new V2G session. The SECC shall expect and require the EVCC to follow normal steps to setup a new V2G session with new authorizations.

NOTE 10 In this case the EVCC will follow [V2G20-1484] and [V2G20-1486].

####### 8.3.4.1.4.1 V2G session resumed successfully

[V2G20-2540] If the check as described by [V2G20-2539] succeeds, i.e. the V2G communication session has been resumed with the same SECC with which the EVCC had initially setup this same communication session, the EVCC shall continue with V2G session resumption

NOTE 1 In this case the EVCC will follow [V2G20-2097], [V2G20-2098] or [V2G20-5046], depending on the energy transfer mode selected. Authorization from previous V2G communication session is used. As such the EVCC will bypass the authorization messages.

[V2G20-1844] When a previously paused V2G communication session is successfully resumed by the EVCC (i.e. [V2G20-2540] applies), the authorization from the previously paused V2G communication session shall be considered as valid.

NOTE 2 An EV can resume a previously paused session by applying the wake up procedure as specified in ISO 15118-3:2015, 7.6.2.1.

[V2G20-1847] When a previously paused V2G communication session is resumed by the SECC, the authorization from the previous session shall be considered valid.