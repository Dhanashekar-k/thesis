##### 8.6.4.3 DC Requirements

[V2G20-1650] For DC charging with WiFi communication only WiFi communication will be used even when there is PLC available.

[V2G20-1651] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "True" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" in DC_ChargeLoopRes, the EVCC shall initiate a ServiceRenegotiation as defined by [V2G20-1661] within the number of seconds provided in NotificationMaxDelay.

[V2G20-1652] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "False" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" in DC_ChargeLoopRes, the EVC shall not initiate a ServiceRenegotiation.

##### 8.6.4.4 WPT Requirements

[V2G20-5080] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "True" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" WPT_ChargeLoopRes, the EVCC shall initiate a ServiceRenegotiation as defined by [V2G20-1661] within the number of seconds provided in NotificationMaxDelay.

[V2G20-5081] If the first ServiceDiscoveryRes message of the service session had the parameter ServiceRenegotiationSupported set to "False" and if the parameter EVSENotification in EVSEStatus is equal to "ServiceRenegotiation" in WPT_ChargeLoopRes, the EVC shall not initiate a ServiceRenegotiation.

8.6.4.5 EVCC

###### 8.6.4.5.1 General

The EVCC behavior defining all valid request-response message sequence.

###### 8.6.4.5.2 Error handling

[V2G20-1966] For all messages, the EVCC shall stop the V2G communication according to 7.4 after V2G_EVCC_Msg_Timeout according to Table 215.

[V2G20-1967] After receiving a response message with "ResponseCode = FAILED", the EVCC shall stop the V2G communication according to requirements defined 7.4.

[V2G20-1968] After receiving any message with "ResponseCode = FAILED_SequenceError", the EVCC shall react according to 7.4.

[V2G20-2220] After the EVCC receives a ResponseCode starting with 'FAILED' or 'FAILED_' it shall terminate the communication by applying [V2G20-728].

####### 8.6.4.5.2.1 ACDP error handling

NOTE 1 ACDP deploys the same basic error handling concept for DC charging with the following exception. In case of an application error when there is no error in the communication layers below the application layer the communication can be continued until the last message pair of the exception handling procedure has been executed.

[V2G20-4025] If EVCC is using ServiceName = DC_ACDP, [V2G20-1967] does not apply.

## 408 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.