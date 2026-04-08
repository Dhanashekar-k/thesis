[V2G20-4000] If EVCC is using ServiceName = DC_ACDP, the following requirements are not applicable: [V2G20-1540], [V2G20-2301], [V2G20-2624] and [V2G20-1028].

NOTE 1 To enable pause when using ServiceName = DC_ACDP the common requirements [V2G20-1227], [V2G20-1541], [V2G20-1839], [V2G20-1840], [V2G20-1841], [V2G20-1842], [V2G20-1843] and [V2G20-1844] apply.

[V2G20-4001] If EVCC is using ServiceName = DC_ACDP, an EVCC shall pause a V2G communication session with the parameter ChargingSession set to value "Pause" in message SessionStopReq after receiving ACDP_DisconnectRes with parameter "EVSEProcessing" set to "Finished".

NOTE 2 To enable pause when using ServiceName = DC_ACDP the common requirements [V2G20-1058], [V2G20-1613], [V2G20-2545], [V2G20-1614], [V2G20-2623], [V2G20-1847], [V2G20-1061] and [V2G20-1032] apply.

[V2G20-1541] When the EVCC wants to resume the previously paused V2G communication session, the EVCC shall send the SessionID of the previously paused V2G communication session it is trying to resume.

NOTE 3 The EVCC received this SessionID in the SessionSetupRes message before the EVCC paused the V2G communication session. The EVCC will send this SessionID in the SessionSetupReq message to resume the previously paused V2G communication session.

[V2G20-1613] If an EVCC chooses to resume an energy transfer session by sending a SessionSetupReq with a message header including the SessionID value from the previously paused V2G communication session, the SECC shall compare this value to the value stored from the preceding V2G communication session.

[V2G20-2545] If the SessionID value received in the current SessionSetupReq is equal to a SessionID value stored from a preceding V2G communication session that has not been terminated yet, the SECC shall check that this V2G communication session resumption request came from the same EVCC with which the SECC had setup this particular V2G communication session. The exact methodology for this check is left up to the CSO and/or the manufacturer of the SECC.

NOTE 4 Since authorization from the preceding V2G communication session is reused in a resumed V2G communication session, it is important for the SECC to ensure that it does not resume a paused V2G session with a wrong EVCC. An example is provided in NOTE 2 below.

NOTE 5 For example, when two EVCCs are connected to the same SECC and both pause their respective V2G communication session, one EV can try to restart the V2G communication session using the SessionID of the other EV. If the SECC does not ensure that the EV trying to reuse someone else's V2G communication session is not denied that privilege, the EV trying to reuse the other EV's V2G communication session will not only be able to reuse other EV's V2G communication session, it will also be able to utilize other EV's charging/service authorization regardless if that authorization was based on PnC or EIM.

NOTE 6 An example of a methodology to check that this V2G communication session resumption request came from the same EVCC with which the SECC had setup this particular V2G communication session is provided in 8.3.4.1.1.

[V2G20-2622] If the check as described by [V2G20-2545] succeeds, i.e. this V2G communication session resumption request came from the same EVCC with which the SECC had setup this particular V2G communication session, the SECC shall continue with V2G session resumption.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.