[V2G20-1579] After receiving the CertificateInstallationRes with "ResponseCode = OK" and the EVSEProcessing set to "Finished", and RemainingContractCertificateChains set to a value higher than "0", the EVCC shall send another unaltered CertificateInstallationReq to continue the installation or shall send a AuthorizationReq to abort the installation of remaining certificates within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1581] After receiving the CertificateInstallationRes with "ResponseCode = OK", EVSEProcessing set to "Finished" and RemainingContractCertificateChains set to "0", the EVCC shall send an AuthorizationReq within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1580] After receiving the CertificateInstallationRes with EVSEProcessing set to "Finished" and ResponseCode starting with "WARNING", the EVCC shall ignore all other parameters of the response message and shall do one (1) of the following.

– If the ResponseCode from the SECC was "WARNING_eMSPUnknown", send another CertificateInstallationReq without including the PrioritizedEMAIDs list. Refer to 8.3.4.3.9 and its subclauses for further details of CertificateInstallationReq.

OR

Send an AuthorizationReq to authorize at the EVSE (using EIM) within V2G_EVCC_Sequence_Performance_Timeout according to Table 215. Refer to 8.3.4.3.3 and its subclauses for further details of AuthorizationReq.

OR

Stop the V2G communication according to requirements defined 7.4.

NOTE 1 Even if no contract certificate was installed in the current service session, it is possible the EVCC has already installed contractcertificates or it can select to use EIM for authorization (if it was offered by the SECC).

[V2G20-1582] After receiving the AuthorizationRes with "ResponseCode = OK" and the EVSEProcessing set to "Ongoing", the EVCC shall send another unaltered AuthorizationReq (with the exception of TimeStamp) within V2G_EVCC_Sequence_Performance_Timeout according to Table 215.

[V2G20-1583] After receiving the AuthorizationRes with the EVSEProcessing set to "Finished" and ResponseCode starting with "WARNING", the EVCC shall ignore all other parameters of the response message and shall do one (1) of the following.

– Send an AuthorizationReq with a different ContractCertificateChain (and corresponding GenChallenge) within V2G_EVCC_Sequence_Performance_Timeout according to Table 215. Refer to 8.3.4.3.3 and its subclauses for further details of AuthorizationReq.

## OR

– If previously the SelectedAuthorizationService was set to "PnC" and the SECC additionally offered "EIM", send an AuthorizationReq with SelectedAuthorizationService set to "EIM" within V2G_EVCC_Sequence_Performance_Timeout according to Table 215. Refer to 8.3.4.3.3 and its subclauses for further details of AuthorizationReq.

## OR

– If previously the SelectedAuthorizationService was set to "EIM" and the SECC additionally offered "PnC", send an AuthorizationReq with SelectedAuthorizationService set to "PnC" within