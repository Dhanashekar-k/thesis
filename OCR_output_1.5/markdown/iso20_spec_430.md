parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be another AuthorizationReq with a SelectedAuthorizationService that was offered via AuthorizationServices of AuthorizationSetupRes, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "False". The V2G_SECC_Sequence_Timeout shall be according to Table 215.

NOTE 4 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid SelectedAuthorizationService.

## [V2G20-1978]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC" when an issue is detected (either by SECC or by SA) with the provided contract certificate chain, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode starting with "WARNING", specifying the detected issue with the provided contractcertificate (refer to [V2G20-2210], [V2G20-2211], [V2G20-2212], [V2G20-2213], [V2G20-2214] and [V2G20-2215] for further details of the ResponseCode to be provided) within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following:

- another AuthorizationReq with a different ContractCertificateChain (and corresponding GenChallenge). The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR

- another AuthorizationReq with SelectedAuthorizationService set to "EIM", if "EIM" was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR

CertificateInstallationReq within the V2G_SECC_Sequence_Timeout according to Table 215, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "True".

NOTE 5 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.

## [V2G20-2131]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC" when an issue is detected (either by SECC or by SA) with the provided contractcertificate chain, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode starting with "WARNING", specifying the detected issue with the provided contractcertificate (refer to [V2G20-2210], [V2G20-2211], [V2G20-2212], [V2G20-2213], [V2G20-2214] and [V2G20-2215] for further details of the ResponseCode to be provided) within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "False":

- another AuthorizationReq with a different ContractCertificateChain (and corresponding GenChallenge). The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR