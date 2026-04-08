#### 8.6.2 Basic definitions for error handling

The basic error handling for a request-response-message pair and a request-response message sequence is based on the ResponseCode included in the response message of the SECC. Depending on the value in the ResponseCode the EVCC decides if it can proceed with the standard request-response message sequence or if it handles an error.

In this document, the ResponseCode as defined in Annex A is interpreted by the EVCC as follows.

- OK:

Any value starting with "OK" or "OK_" indicates a positive response. Detailed information may be provided by OK_<additional info>. This information may be used to differentiate the reaction on the positive response.

- FAILED:

Any value starting with "FAILED" or "FAILED_" indicates a negative response. Detailed information may be provided by FAILED_<additional info>. This information may be used to differentiate the reaction on the negative response. This response is considered a fatal error. The SECC and EVCC will terminate the communication session after sending/receiving this response code.

WARNING:

Any value starting with "WARNING_" indicates a response that requires an adjustment or reaction by the EVCC, otherwise a subsequent negative response is to be expected in the next message pair. Detailed information is to be provided by WARNING_<additional info>. This information is to be used to differentiate the reaction on the response. This response is not considered a fatal error. The SECC and EVCC will not terminate the communication session after sending/receiving this response. They can continue the communication if proper remedial actions (as defined for that particular response) are taken by the EVCC.

The processing of the remaining parameters in a response message in the EVCC depends on the parameter ResponseCode. If the ResponseCode contains a value starting with OK indicating that no error was detected, the EVCC can process other parameters of the response message mandatorily or optionally as defined in 8.3.5.7.1. If the ResponseCode contains a value starting with FAILED indicating that an error was detected, the EVCC is expected to ignore other parameters of the response message. If the ResponseCode contains a value starting with WARNING indicating that something is not as expected, the EVCC may either process the parameters or ignore them depending on the specifications defined for that particular message.

As long as the message content of the received request message is valid and the request message is accepted in the current SECC state (sequencing), the ResponseCode is set to OK. This is also true for response messages with EVSEProcessing set to Ongoing. With the ResponseCode set to OK the SECC indicates that the request message is accepted and valid, but cannot be finally answered at this moment and more time is needed to send the valid values in the response message. When the valid values are sent in the response message, the SECC indicates this with the parameter EVSEProcessing (set to Finished) and the EVCC can proceed with the sequence as expected for the first request message before receiving the parameter EVSEProcessing (set to Ongoing). If the SECC sets the ResponseCode to FAILED it identified an error in processing or an invalid message and the standard error handling applies.

#### 8.6.3 ResponseCode handling

##### 8.6.3.1 Common requirements