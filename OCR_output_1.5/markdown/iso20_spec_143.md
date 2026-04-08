[V2G20-1534] The value of the TimeStamp element of the common MessageHeaderType shall always be in SECC time and encoded at microseconds resolution.

NOTE 1 The use of microseconds in a 64 bit unsigned long integer has the benefit of preventing the year 2038 problem, allowing for precise synchronization with other high resolution clocks (e.g. as used in smart meters) and allowing precise calculations of clock drift and data transmission or processing latencies in cases where this might be helpful to trace down technical problems.

NOTE 2 While even the EVCC is required to use TimeStamps in SECC time this does not require that it changes its internal hardware clock. The EVCC will only need to calculate its clock offset to SECC time and always apply this delta appropriately. Due to the nature of clock drift that delta can change over time and the EVCC monitors its delta and adjust it continuously.

## [V2G20-1535]

The value of the TimeStamp element of the common MessageHeaderType sent by the EVCC during the initial SessionSetupReq message shall be its best effort guess of the present SECC time stamp, assuming the SECC time is synchronized to UTC. If the EVCC has no knowledge of the present UTC time than it shall indicate this by sending "zero" as the initial TimeStamp.

NOTE 3 In cases where the SECC does not have any means to synchronize its clock to external sources (e.g. due to lack of internet connectivity, etc.), the above requirement allows the SECC to decide if it wants to join the EVCC's world view of time.

## [V2G20-1536]

The value of the TimeStamp element of the common MessageHeaderType sent by the SECC during the SessionSetupRes message shall define the initial SECC time stamp, which serves as the reference for all future message exchanges.

NOTE 4 The EVCC might not have any means to synchronize its clock to external sources. [V2G20-1533] discourages the use of SECC time for security related purposes. If the EVCC, in lack of better options, wants to utilize SECC time as a source for the synchronization of its internal real time clock, it can try to ensure that the conditions of [V2G20-1531] are met, where UTC time alignment is assured.

[V2G20-1537] The value of the TimeStamp element of the common MessageHeaderType sent by the SECC or the EVCC shall always increase with each message and according to the progress of time.

[V2G20-1538] The previous requirement [V2G20-1537] shall not apply to the first (SessionSetupReq) and the second (ServiceDiscoveryReq) message which is being sent by the EVCC within a newly established charging session.

NOTE 5 The always increasing time stamps allow "ordering" of messages (linearization) which can be helpful in situations where multiple multiplexed sequences are taking place and where internal processing queue prioritization can result in out of order processing that might need detection in some applications.

#### 8.3.4 Request and response definitions

##### 8.3.4.1 V2G session handling

Messages defined as common messages in the following clause and its subclauses can be applied to the message sequence in any charging mode.

Additionally, this subclause and the subclauses within it, will provide specific and separate requirements for the private SECC and the SECC. Thus, unless otherwise specified for this subclause or any subclause within it, private SECC and SECC are not considered interchangeable.

###### 8.3.4.1.1 General

## 138 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.