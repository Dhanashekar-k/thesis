"Finished" and ResponseCode per [V2G20-2218] within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has completed successfully but the received contract certificate will expire in 14 days or fewer. The next allowed request shall be one (1) of the following:

– ServiceDiscoveryReq within the V2G_SECC_Sequence_Timeout according to Table 215;

CertificateInstallationReq within the V2G_SECC_Sequence_Timeout according to Table 215, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "True".

NOTE 9 This allows EVCC to install a new contract certificate if it so chooses.

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2218] within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has completed successfully but the received contract certificate will expire in 14 days or fewer. The next allowed request shall be ServiceDiscoveryReq, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "False". The V2G_SECC_Sequence_Timeout shall be according to Table 215.

[V2G20-2230] After receiving the AuthorizationReq with SelectedAuthorizationService set to "EIM", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2219] within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has failed due to any reason. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following:

– another AuthorizationReq with SelectedAuthorizationService set to "PnC", if "PnC" was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215;

– CertificateInstallationReq within the V2G_SECC_Sequence_Timeout according to Table 215, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "True".

NOTE 10 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.

[V2G20-2231]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "EIM", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2219] within V2G_SECC_Msg_Performance_Time according to Table 215, when authorization has failed due to any reason. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be another AuthorizationReq with SelectedAuthorizationService set to "PnC", if "PnC" was offered via AuthorizationServices of AuthorizationSetupRes and the AuthorizationSetupRes was sent with CertificateInstallationService set to "False". The V2G_SECC_Sequence_Timeout shall be according to Table 215.



<div style="text-align: center;">NOTE 11 This allows SECC to ensure that it can terminate connection with an EVCC can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.</div>
