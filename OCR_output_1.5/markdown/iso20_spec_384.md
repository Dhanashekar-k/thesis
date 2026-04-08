[V2G20-437] The EVCC shall wait for the response message corresponding to the request message sent before.

[V2G20-438] The EVCC shall stop waiting for the response message and stop monitoring the V2G_EVCC_Msg_Timer when V2G_EVCC_Msg_Timer is equal or larger than V2G_EVCC_Msg_Timeout(MessageType) and no response message was received. It shall then apply the error handling as defined in 8.6.

NOTE 2 In this document receiving a response message is described by A-DATA.confirmation.

[V2G20-439] The EVCC shall stop waiting for the response message and stop monitoring the V2G_EVCC_Msg_Timer when V2G_EVCC_Msg_Timer is smaller than V2G_EVCC_Msg_Timeout(MessageType) and it received a response message. It shall then process the response message as defined in 8.6.

NOTE 3 In this document receiving a response message is described by A-Data.confirmation.

8.5.4.1.2 SECC timing for response-request message sequence

[V2G20-440] The EVCC shall ignore any message that is not a valid response message.

[V2G20-441] The SECC shall set the timeout V2G_SECC_Sequence_Timeout to the value as defined in Table 215, reset the V2G_SECC_Sequence_Timer and start monitoring the V2G_SECC_Sequence_Timer when it sends a response message.

NOTE 4 In this document sending a response message is described by A-Data.response.

[V2G20-442] The SECC shall wait for a request message.

[V2G20-443] The SECC shall stop waiting for a request message and stop monitoring the V2G_SECC_Sequence_Timer when V2G_SECC_Sequence_Timer is equal or larger than V2G_SECC_Sequence_Timeout and no request message was received. It shall then stop the V2G communication session.

NOTE 5 In this document receiving a request message is described by A-Data.indication. A-Data.indication (A_Msg="message name") signalizes the successful reception of a valid request message for the V2G message that is given by A_Msg where "Valid message" means that all mandatory elements are filled in so that it can be deserialized.

[V2G20-444] The SECC shall stop waiting for a request message and stop monitoring the V2G_SECC_Sequence_Timer when V2G_SECC_Sequence_Timer is smaller than V2G_SECC_Sequence_Timeout and it received a request message. It shall then process the response message as defined in 8.6.

NOTE 6 In this document receiving a request message is described by A-Data.indication.

[V2G20-445] The SECC shall ignore any message that is not a valid request message.

8.5.4.2 AC specific message sequence and session timing

[V2G20-1499] The EVCC shall implement the EVCC specific AC timeouts and performance times defined in Table 216.

[V2G20-1500] The SECC shall implement the SECC specific AC timeouts and performance times defined in Table 216.