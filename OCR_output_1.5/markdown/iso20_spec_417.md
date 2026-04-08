V2G_EVCC_Sequence_Performance_Timeout according to Table 215. Refer to 8.3.4.3.3 and its subclauses for further details of AuthorizationReq.

– If the AuthorizationSetupRes was sent with CertificateInstallationService set to "True", send a CertificateInstallationReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215 to install a new contract certificate. Refer to 8.3.4.3.9 and its subclauses for further details of CertificateInstallationReq.

— Stop the V2G communication according to requirements defined in 7.4.

NOTE 2 It is necessary for EVCC to "remember" the SelectedAuthorizationService service and ContractCertificateChain (if applicable) it has already used during the current service session. Without that the EVCC can be stuck in a continuous loop. The implementers are advised to be careful about such implementation issues.

NOTE 3 If the EVCC previously sent CertificateInstallationReq which resulted in CertificateInstallationRes message with ResponseCode starting with "WARNING", sending another CertificateInstallationReq after the EVCC received AuthorizationRes message with ResponseCode starting with "WARNING" can send EVCC and SECC into an error loop. The implementers are advised to be careful about such implementation issues.

NOTE 4 Although this allows looping behavior and going back and forth between the EIM and PnC based authorization the requirements are written to allow jumping to a different authorization method if the initially selected authorization method fails. Unrestricted looping between different authorization methods can result in the EVCC and SECC being stuck in a loop. The implementers are advised to be careful about such implementation issues.

[V2G20-2221] After receiving the AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2218], the EVCC shall do one (1) of the following.

– Send a ServiceDiscoveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

– If the AuthorizationSetupRes was sent with CertificateInstallationService set to "True", send a CertificateInstallationReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215 to install a new contract certificate. Refer to 8.3.4.3.9 and its subclauses for further details of CertificateInstallationReq.

[V2G20-1584] After receiving the AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode set to "OK", the EVCC shall send a ServiceDiscoveryReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1585] After receiving the ServiceDiscoveryRes with "ResponseCode = OK", the EVCC shall send a ServiceDetailReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1586] After receiving the ServiceDetailRes with "ResponseCode = OK", if further ServiceDetailReq are necessary to retrieve detailed information from the SECC, the EVCC shall send another ServiceDetailReq, within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1587] After receiving the ServiceDetailRes with "ResponseCode = OK", if the EVCC does not require to retrieve more detail about any service from the SECC, the EVCC shall send

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.