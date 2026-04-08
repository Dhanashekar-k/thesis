certificate because the SECC/SA cannot process the curves in the OEM provisioning certificate (due to changes to configuration parameter as defined by [V2G20-2320]), the SECC will send the ResponseCode "WARNING_CertificateValidationError".

[V2G20-2206] The message "CertificateInstallationRes" shall contain the ResponseCode "WARNING_NoContractMatchingPCIDFound" if the SA(s) indicate to the SECC that after a complete search, no contract could be found for the PCID contained in the OEM provisioning certificate received in the OEMProvisioningCertificate chain contained in the CertificateInstallationReq message.

[V2G20-2207] The message "CertificateInstallationRes" shall contain the ResponseCode "WARNING_NoCertificateAvailable" if a new contract certificate cannot be retrieved from secondary actor within V2G_SECC_Msg_Performance_Time according to Table 215.

NOTE 4 This response code indicates a timeout. The timeout could be due to many reasons including communication errors, taking longer than the timeout allows to retrieve the contract certificate from the secondary actor, etc.

[V2G20-2208] The message CertificateInstallationRes shall contain the ResponseCode "WARNING_eMSPUnknown" if the SECC does not recognize any one (or more) of the eMSPs indicated by the EMAID included in the PrioritizedEMAIDs list it received in CertificateInstallationReq message.

[V2G20-2209] The message "AuthorizationRes" shall contain the ResponseCode "WARNING_AuthorizationSelectionInvalid" if the SelectedAuthorizationService contained in the AuthorizationReq message was not part of the offered AuthorizationServices of AuthorizationSetupRes message.

[V2G20-2210] The message AuthorizationRes shall contain the ResponseCode "WARNING_ContractCancelled" if the SECC received the information (potentially from SA; it is not in the scope of this document to define how the SECC received this information) that the contract associated with the ContractCertificate it received in AuthorizationReq message, in attribute ContractSignatureCertChain, has been cancelled.

NOTE 5 This response code is related to the actual customer contract between the SA and the customer. It is not related to the contract certificate itself. For example, the contract certificate can still be valid while the customer possibly cancelled the actual contract with the eMSP. In that case, at the SA's discretion, this response code is expected to be utilized.

[V2G20-2211] The message AuthorizationRes shall contain the ResponseCode "WARNING_eMSPUnknown" if the SECC does not recognize the eMSP indicated by the EMAID included in the ContractCertificate it received in AuthorizationReq message, in attribute ContractSignatureCertChain.

[V2G20-2212] The message "AuthorizationRes" shall contain the ResponseCode "WARNING_CertificateExpired" if the SECC (or SA) deduces that one (or more) of the certificates in the ContractCertificate chain it received in the AuthorizationReq message, in attribute ContractSignatureCertChain, is expired. This includes any cross certificates (if applicable).

[V2G20-2213] The message "AuthorizationRes" shall contain the ResponseCode "WARNING_CertificateNotYetValid" if the SECC (or SA) deduces that one (or more) of the certificates in the ContractCertificate chain it received in the AuthorizationReq

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.