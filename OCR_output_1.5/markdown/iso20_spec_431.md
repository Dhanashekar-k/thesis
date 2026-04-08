- another AuthorizationReq with SelectedAuthorizationService set to "EIM", if "EIM" was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215.

NOTE 6 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.

[V2G20-2228]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC" if the challenge response contained in the AuthorizationReq message (in attribute GenChallenge) is not valid versus the GenChallenge provided in AuthorizationSetupRes, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2216] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following:



– another AuthorizationReq with a different ContractCertificateChain (and corresponding GenChallenge). The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR

– another AuthorizationReq with SelectedAuthorizationService set to "EIM", if "EIM" was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR

– CertificateInstallationReq within the V2G_SECC_Sequence_Timeout according to Table 215, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "True".



NOTE 7 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.

[V2G20-2229]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC" if the challenge response contained in the AuthorizationReq message (in attribute GenChallenge) is not valid versus the GenChallenge provided in AuthorizationSetupRes, the SECC shall respond with an AuthorizationRes with EVSEProcessing set to "Finished" and ResponseCode per [V2G20-2216] within V2G_SECC_Msg_Performance_Time according to Table 215. All mandatory parameters shall be filled in with arbitrary XSD conform values. All values shall be chosen in a way that results in a minimal size of the response message. The next allowed request shall be one (1) of the following, if the AuthorizationSetupRes was sent with CertificateInstallationService set to "False":



– another AuthorizationReq with a different ContractCertificateChain (and corresponding GenChallenge). The V2G_SECC_Sequence_Timeout shall be according to Table 215;

OR

– another AuthorizationReq with SelectedAuthorizationService set to "EIM", if "EIM" was offered via AuthorizationServices of AuthorizationSetupRes. The V2G_SECC_Sequence_Timeout shall be according to Table 215.

NOTE 8 This allows SECC to ensure that it can terminate connection with an EVCC that can be stuck sending the same AuthorizationReq with the same invalid ContractCertificateChain.

[V2G20-2232]

After receiving the AuthorizationReq with SelectedAuthorizationService set to "PnC", the SECC shall respond with an AuthorizationRes with EVSEProcessing set to

