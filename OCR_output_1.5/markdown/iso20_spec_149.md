NOTE 3 An EVSE can resume a previously paused session by applying the wake up procedure as specified in ISO 15118-3:2015, 7.6.2.2.

[V2G20-1843] In case EVCC successfully resumes a previously paused V2G communication session (i.e. [V2G20-2540] applies), the EVCC shall apply the message sequence according to [V2G20-2097], [V2G20-2098] and [V2G20-5046].

[V2G20-2301] If [V2G20-1540] applies and a connection based on ISO 15118-3 has been established, the EVCC shall take care that [V2G20-1541] is fulfilled as long as no CP state E or F was detected in the EVCC as defined in IEC 61851-1.

[V2G20-1027] If [V2G20-1540] applies and a connection based on ISO 15118-8 has been established, the EVCC shall take care that [V2G20-1541] is fulfilled as long as no alignment failure has been reported by the SECC.

[V2G20-1028] If [V2G20-2623] applies and a connection based on ISO 15118-8 has been established, the SECC shall take care that [V2G20-1058] is fulfilled as long as no alignment failure was detected in the SECC.

[V2G20-2624] If [V2G20-2623] applies and a connection based on ISO 15118-3 has been established, the SECC shall take care that [V2G20-1058] is fulfilled as long as no CP State A, E, or F was detected in the SECC as in IEC 61851-1.

[V2G20-1058] If the V2G communication session is resumed according to [V2G20-2623] the SECC shall ensure that if a ScheduleTuple is offered with the same ScheduleTupleID that was offered previously, this ScheduleTuple shall not differ from the previously offered ScheduleTuple.

NOTE 4 This allows the EVCC to continue/reuse an EVPowerProfile that was calculated before the pause based on a ScheduleTuple that is still offered by the SECC.

[V2G20-1840] If an EVCC successfully resumes a previously paused V2G communication session (i.e. [V2G20-2540] applies) it shall reduce the time elapsed during the pause period for the ScheduleTuple selected in the previous V2G communication session.

[V2G20-1841] If an EVCC successfully resumes a previously paused V2G communication session (i.e. [V2G20-2540] applies) and the time elapsed is greater than the time covered by the ScheduleTuple whose ID was selected in the previous V2G communication session the EVCC shall trigger an instant schedule renegotiation.

[V2G20-1765] If the EVCC wants to change the energy transfer parameters, it shall use the schedule renegotiation mechanism defined in this document.

[V2G20-2625] If the V2G communication session is resumed according to [V2G20-2623] and if the SECC wants to change the energy transfer parameters listed in [V2G20-1058] it shall use the schedule renegotiation mechanism defined in this document.

[V2G20-2546] If the V2G communication session is resumed according to [V2G20-2545] and if the SECC wants to change the energy transfer parameters listed in [V2G20-1058], it shall use the schedule renegotiation mechanism defined in this document.

[V2G20-1614] If the EVCC or SECC want to change the energy transfer parameters, the EVCC or SECC shall use the schedule renegotiation mechanism defined in this document.

8.3.4.1.4.2 V2G session resumption failed

## 144 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.