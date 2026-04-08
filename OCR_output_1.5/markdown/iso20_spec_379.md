To enable error handling for a V2G communication session setup the EVCC monitors the time between reception of SECC discovery response, SessionSetupRes and PowerDeliveryRes, respectively. This allows the EVCC to decide about a successful or failed charging session after the defined timeouts.

The monitoring of a V2G communication session is based on the following timing concepts:

– message timing: monitors the timing between the request and the response of a Request-Response-Pair. This allows, for example, the EVCC application to initiate the error handling if no response is sent;

– sequence timing: monitors the timing of subsequent request-response-pairs. This allows, for example, the SECC application to initiate the error handling if an expected next request message was not sent;

- ongoing timing: monitors the timing in case of sending a request-response-pair repeatedly based on the parameter EVSEProcessing equal to "Ongoing". This allows, for example, the EVCC to initiate the error handling in case the SECC exceeds the processing time;

- communication setup timing: monitors the time from the moment of an established data link until the session setup message. It allows deciding if the communication setup was successful within a defined time.

The timers are compared to predefined time values as decision criterion. The EVCC and the SECC distinguish between two categories:

- timeout: if the specified time is exceeded the related error handling is initiated:

- performance time: if the specified time is exceeded the performance requirement is not fulfilled.

NOTE 1 While exceeding a timeout always causes an error handling, the performance time does not necessarily cause error handling if not defined differently by requirements. Depending on the system behavior (e.g. transmission time) no error can occur if the corresponding communication partner does not detect a timeout but the probability for causing a timeout is high.

NOTE 2 Timeouts are observed at the application layer where they are also enforced (according to requirement [V2G20-1966] for example). It is important for each sending party to keep in mind that all processing (e.g. TLS encryption) and transmission delays between both application layer sides will be part of the observed timing on the receiving side. See Figure 212 for a detailed illustration.

NOTE 3 This document supports PLC and WiFi communication. Both technologies come with different average and worst case latencies as well as congestion and retransmissions characteristics. For example, in WiFi networks real world round trip latencies can reach up to 25 ms to 100 ms or even more. As mentioned before it is important that those latencies are taken into account when deciding on the implementation of a message timing strategy in the application layer of the sending side. The timing requirements of Table 215 have been defined with the assumption that round-trip end-to-end transmission delays will never exceed 250 ms.

#### 8.5.3 DC service

The monitoring of a DC V2G communication session includes the following timing concepts:

- DC_CableCheck timing: The monitoring of the cable check is carried out by the EV using the V2G_EVCC_DC_CableCheck_Timer. It is started when the EV requests the EVSE to start the Cable Check, and ends when the EVSE has finished the cable check, or when the V2G EVCC DC CableCheck Timer expires:

- DC_PreCharge timing: The monitoring of the pre charge is carried out by the EV using the V2G_EVCC_DC_PreCharge_Timer. It is started when the EV starts the pre charging by sending the first DC_PreChargeReq message, and ends when the pre charging has finished, indicated by the EV determining that the EVSE output voltage, as measured inside the EV, has sufficiently been adjusted to the EV RESS voltage, or when the V2G_EVCC_DC_PreCharge_Timer expires.

#### 8.5.4 Message sequence and communication session

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.