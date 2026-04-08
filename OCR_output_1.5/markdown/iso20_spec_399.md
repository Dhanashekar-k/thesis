[V2G20-4023] If [V2G20-4022] applies and no error has been identified, the EV shall not change the CP State until [V2G20-913] applies.

The following requirements apply for the SECC.

[V2G20-4024] The EVSE shall apply a CP duty cycle of 100 % from start of Data Link Setup until end of V2G communication session as defined in IEC 61851-23-1.

NOTE 1 For ACDP noise robustness CP line uses only a DC signal. PWM is not allowed.

NOTE 2 The following DC specific requirements apply: [V2G20-917].

8.5.7 V2G message synchronization with IEC 61980-2 signalling for WPT

8.5.7.1 Overview

In general, the ISO 15118 series is based on the requirements as defined in IEC 61851-1.

[V2G20-5071] An ISO 15118-enabled EV shall conform to IEC 61980-2 and ISO 19363:2020.

[V2G20-5072] During HLC-C, the EV shall apply all energy transfer limits as negotiated by the ISO 15118 series in addition to the limits defined by IEC 61980-2.

[V2G20-5073] ISO 15118-enabled EVSE shall conform to IEC 61980-2.

### 8.6 Message sequencing and error handling

#### 8.6.1 Overview

In a V2G communication session the EVCC and the SECC exchange request-response message pairs based on a predefined sequence. In this document this is referenced as request-response message sequence. These request-response message sequences allow both sides to synchronize the process in any situation and to control the communication between two V2G entities.

The basic error handling concept is based on application level timers for request-response message sequences. This enables a V2G entity to manage any processing error and communication error on application level after waiting for the expected behavior until a specified timeout. Therefore, a V2G entity can decide on a successful processing after waiting for the positive result until a timeout. In case there is no error in the communication layers below the application layer, the application has the option to terminate the TCP communication in case of application error. A terminated TCP connection before a SessionStopRes is always interpreted as an error by the EVCC or the SECC.

Besides the timeout concept defined in this document, it does not limit additional error detection mechanisms as long as such mechanisms do not lead to incompatibility.

Within a charging session, an EVCC can establish a new V2G communication session after an error by applying the V2G communication state processing as described in 7.4. In this case, the EVCC and the SECC start the communication in the same way as for the first V2G session setup.

In general, the processing time of a request message in an SECC is limited by the performance requirements defined in 8.5.4. If an SECC requires more processing time it may apply the parameter EVSEProcessing (set to Ongoing) to avoid a timeout at the EVCC by explicitly indicating that the processing is not finished yet and the EVCC waits for finishing the processing before proceeding with the message sequence. The EVCC will then repeat the request message periodically until the EVSE signals the finishing of the processing by the parameter EVSEProcessing (set to finished).