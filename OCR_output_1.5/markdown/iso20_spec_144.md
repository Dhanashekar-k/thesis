[V2G20-747] The header of any message sent by the EVCC during an active V2G communication session shall include the SessionID value returned by the SECC in the response to the SessionSetupReq initiating the currently active V2G communication session.

[V2G20-751] The SessionID value returned by the SECC in the SessionSetupRes message shall not change as long as the V2G communication session is not terminated (i.e. value of parameter ChargingSession of SessionStopReq has not been set to "Terminate" at any time).

[V2G20-752] The header of any message sent by the SECC during an active V2G communication session shall include the SessionID value returned by the SECC in the response to the SessionSetupReq initiating the currently active V2G communication session.

[V2G20-2541] If the EVCC detects that there has been no communication associated with a particular V2G session for 648 000 s (7,5 days), the EVCC shall immediately terminate/close that V2G session.

NOTE 1 If there is no communication for 7,5 days for a particular V2G session, it is assumed that the V2G session has been abandoned/orphaned and as such can be terminated/closed.

[V2G20-2620] If the SECC detects that there has been no communication associated with a particular V2G session for 648 000 s (7.5 days), the SECC shall immediately terminate/close that V2G session.

NOTE 2 If there is no communication for 7,5 days for a particular V2G session, it is assumed that the V2G session has been abandoned/orphaned and as such can be terminated/closed.

###### 8.3.4.1.2 Initial V2G session setup

[V2G20-1243] When sending the first SessionSetupReq message for the initiated service session (i.e. when the EVCC is not trying to resume a previously paused V2G communication session), the EVCC shall only transmit zeroes in the parameter SessionID in the message header.

[V2G20-2106] When receiving the SessionSetupReq with the parameter SessionID equal to zero, the SECC shall generate a new (not stored) SessionID value different from zero and return this value in the SessionSetupRes message header.

NOTE 3 In this case the EVCC will follow [V2G20-1484] and [V2G20-1486].

[V2G20-2621] When generating a new SessionID, the SECC shall ensure that the generated SessionID is 64-bit long once with a minimum of 58 bits of entropy. Refer to 7.3.7 for further details.

[V2G20-2618] If the EVCC sent the SessionSetupReq message with a SessionID consisting only of zeroes and received the SessionSetupRes message with the ResponseCode set to "OK_NewSessionEstablished" as well as the SessionID set to a value other than zero, the EVCC shall consider this as a new V2G communication session.

[V2G20-2619] If [V2G20-2618] applies, the EVCC shall follow normal steps to setup a new V2G session with new authorizations.

NOTE 4 In this case the EVCC will follow [V2G20-1484] and [V2G20-1486].

[V2G20-1059] The EVCC and SECC shall cache the relevant authorization data for the duration of the V2G communication session.