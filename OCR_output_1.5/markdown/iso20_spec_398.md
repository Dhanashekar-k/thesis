[V2G20-917] The SECC shall respond with DC_CableCheckRes containing "ResponseCode = OK" within V2G_SECC_Msg_Performance_Time according to Table 215, if the SECC measures a CP State C or D.

[V2G20-918] The SECC shall respond with DC_CableCheckRes containing "ResponseCode = "FAILED" within V2G_SECC_Msg_Performance_Time according to Table 215, if the SECC measures no CP State C or D.

[V2G20-919] After sending a PowerDeliveryRes message with parameter ResponseCode set to "OK" in response to a PowerDeliveryReq with parameter ChargeProgress set to "Stop", the SECC shall try to measure CP state B.

[V2G20-920] After receiving a DC_WeldingDetectionReq message or a SessionStopReq message, the SECC shall wait for a maximum of V2G_SECC_Msg_Performance_Time to measure CP state B.

[V2G20-921] After receiving a DC_WeldingDetectionReq message or a SessionStopReq message, the SECC shall send the corresponding response message with parameter ResponseCode set to "OK" within V2G_SECC_Msg_Performance_Time according to Table 103, if CP State B was measured.

[V2G20-922] After receiving a DC_WeldingDetectionReq message or a SessionStopReq message, the SECC shall send the corresponding response message with parameter ResponseCode set to "FAILED" within V2G_SECC_Msg_Performance_Time according to Table 103, if CP State B was not measured.

##### 8.5.6.5 AC and DC reverse power transfer specific requirements

###### 8.5.6.5.1 General

In the discharging services, EVCC and SECC shall align to IEC 61851-1 signalling in the same way as in the charging services. Until the discharging service is added in IEC 61851-1, it is defined as an extension within this document. Basic status definitions between charging and discharging are similar, but trigger conditions for charging and discharging loops are defined for reverse power transfer system. It shall be given by HLC control under the condition of IEC 61851-1 signalling agreement.

###### 8.5.6.5.2 Common BPT specific requirements for AC and DC

Most of common requirements defined in 8.5.6.2 shall be applied with following exceptions.

[V2G20-1138] ISO 15118 enabled EVCC shall confirm to IEC 61851-1 in case of charging. Also ISO 15118 enabled EVCC shall similarly work as defined in IEC 61851-1 in case of discharging.

[V2G20-1409] ISO 15118 enabled SECC shall confirm to IEC 61851-1 in case of charging. Also ISO 15118 enabled SECC shall similarly work as the EVSE defined in IEC 61851-1 in case of discharging.

##### 8.5.6.6 ACDP specific requirements

The following requirements apply for the EVCC.

[V2G20-4022] After receiving a ACDP_ConnectRes message with "ResponseCode = OK" and before sending a DC_CableCheckReq message, the EVCC shall change to CP State C or State D as defined in IEC 61851-1.