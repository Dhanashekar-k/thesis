allowed request shall be AuthorizationReq or another CertificateInstallationReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

.0] After receiving the CertificateInstallationReq, if no contract certificate chain for the provided PCID could be found, the SECC shall respond with a CertificateInstallationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2206] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be AuthorizationReq and the V2G SECC_Sequence_Timeout is set according to Table 215.

## [V2G20-2225]

[V2G20-2225] After receiving the CertificateInstallationReq, if the new contract certificate cannot be retrieved from secondary actor within V2G_SECC_Msg_Performance_Time (according to Table 215), the SECC shall respond with a CertificateInstallationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2207] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be AuthorizationReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

[V2G20-1977] After receiving the AuthorizationReq, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Ongoing" within V2G_SECC_Msg_Performance_Time according to Table 215, while the authorization is still ongoing. The next allowed request shall be another unaltered AuthorizationReq and the V2G_SECC_Sequence_Timeout is set according to Table 215.

NOTE 2 This applies to both EIM and PnC authorization modes.

[V2G20-2226] After receiving the AuthorizationReq with SelectedAuthorizationService set to a value that was not part of the offered AuthorizationServices of AuthorizationSetupRes message, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2209] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following.

– Another AuthorizationReq with a SelectedAuthorizationService that was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215.

OR

CertificateInstallationReq within the V2G_SECC_Sequence_Timeout according to Table 215, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "True".

NOTE 3 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid SelectedAuthorizationService.

## [V2G20-2227]

After receiving the AuthorizationReq with SelectedAuthorizationService set to a value that was not part of the offered AuthorizationServices of AuthorizationSetupRes message, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2209] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory

## 424 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.