[V2G20-4039] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a "ACDP_DisconnectReq" when "ResponseCode ≠ OK" of "ACDP_ConnectRes".

[V2G20-4040] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a "ACDP_DisconnectReq" when "ResponseCode ≠ OK" of "CableCheckRes".

[V2G20-4041] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a "ACDP_DisconnectReq" when "ResponseCode ≠ OK" of "PreChargeRes".

[V2G20-4042] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a "ACDP_DisconnectReq" when "ResponseCode ≠ OK" of "PowerDeliveryRes".

[V2G20-4043] If EVCC is using ServiceName = DC_ACDP in Table 204, the EVCC shall send a ACDP_DisconnectReq when "ResponseCode = FAILED" of "DC_ChargeLoopRes".

[V2G20-4044] If EVCC is using ServiceName = DC_ACDP in Table 204, after receiving the ACDP_DisconnectRes with "ResponseCode ≠ OK", the EVCC shall send a SessionStopReq.

###### 8.6.4.5.3 Message Flow

####### 8.6.4.5.3.1 Common message flow

[V2G20-1746] The EVCC shall send a supported App Protocol Req after the fulfilment of [V2G20-024].

[V2G20-1747] After receiving the supportedAppProtocolRes with "ResponseCode = OK_SuccessfulNegotiation", the EVCC shall send a SessionSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1089] The SECC shall not send ResponseCode set to OK_SuccessfulNegotiationWithMinorDeviation in supportedAppProtocolRes, since deviations are not supported by ISO 15118-20 (this document).

[V2G20-1090] In case the EVCC receives a supportedAppProtocolRes with ResponseCode set to OK_SuccessfulNegotiationWithMinorDeviation, the EVCC shall treat it the same as when the SECC would have sent OK_SuccessfulNegotiation.

[V2G20-1749] If the EVCC is using PLC, after receiving the SessionSetupRes with "ResponseCode = OK", the EVCC shall send an AuthorizationSetupReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1576] If the EVCC intends to install or update a contract certificate after receiving the AuthorizationSetupRes with "ResponseCode = OK" and CertificateInstallationService set to "True", the EVCC shall send a CertificateInstallationReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1577] After receiving the AuthorizationSetupRes with "ResponseCode = OK" and CertificateInstallationService set to "False", the EVCC shall send an AuthorizationReq within V2G EVCC Sequence Performance Timeout according to Table 215.

[V2G20-1578] After receiving the CertificateInstallationRes with "ResponseCode = OK" and the EVSEProcessing set to "Ongoing", the EVCC shall send another unaltered CertificateInstallationReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.