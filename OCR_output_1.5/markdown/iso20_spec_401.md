Besides the requirements for request-response message pairs and request-response message sequences as defined in 8.6.4 the EVCC and the SECC shall conform to the following requirements.

[V2G20-734] If the ResponseCode contains a value starting with OK, the EVCC shall process the other parameters of the response message as defined in 8.6.

[V2G20-735] If the ResponseCode contains a value starting with FAILED, the EVCC shall ignore the other parameters of the response message.

[V2G20-736] If the SECC sends a ResponseCode containing a value starting with FAILED all mandatory parameters shall be filled in with arbitrary XSD conform values. Additionally, all values shall be chosen in a way that results in a minimal size of the response message.

[V2G20-2201] If the ResponseCode contains a value starting with WARNING, the EVCC shall take appropriate actions as defined for that particular WARNING response for that particular message.

NOTE 1 Each WARNING ResponseCode can have different reaction requirements for the EVCC. In some cases the EVCC can be required to ignore the other parameters of the response message and take a pre-defined action while in other cases the EVCC can be required to take an action based on the parameters received in the message but act in a different way than when it receives OK ResponseCode for the same message.

[V2G20-2202] If the SECC sends a ResponseCode containing a value starting with WARNING all mandatory parameters shall be filled as defined for that particular WARNING response for that particular message.

NOTE 2 Each WARNING ResponseCode can have a different requirements for the parameters. In some cases the SECC can be required to send default/arbitrary XSD conform values while in others the SECC can be required to send some specific values so that the EVCC can take an action based on the parameters received in the message.

In general each response message can contain two types of ResponseCode values "OK" or "FAILED". In addition some response messages can further contain the ResponseCode value "WARNING_ (see Table 224).

[V2G20-457] A response message shall contain the ResponseCode "OK" in the "ResponseCode" attribute if the processing of the request message was successful. If later on a specific positive "ResponseCode" is defined for a dedicated situation, this ResponseCode shall be used.

[V2G20-458] A response message shall contain the ResponseCode "FAILED" in the "ResponseCode" attribute if the processing of the request message was not successful and no specific "ResponseCodeType" is defined for the concrete error case.

[V2G20-459] The response message shall contain the ResponseCode "FAILED_SequenceError" if the SECC has received an unexpected request message.

[V2G20-460] The response message shall contain the ResponseCode "FAILED_UnknownSession" if the SessionID in any request message except SessionSetupReq is not equal to the SessionID value stored for the currently active V2G communication session.

[V2G20-461] The response message shall contain the ResponseCode "FAILED_SignatureError" if the validation of the Security element in the message header failed.

[V2G20-462] The message "SessionSetupRes" shall contain the specific ResponseCode "OK_NewSessionEstablished" if processing of the SessionSetupReq message was