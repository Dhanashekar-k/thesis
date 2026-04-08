received message as invalid, and discard the message. Otherwise, the EVCC shall continue processing the data received in SignedInstallationData.

## [V2G20-2706]

When the EVCC receives the parameter ECDHCurve (in SignedInstallationData) set to the default ECC algorithm according to [V2G20-2674], it shall check that the configuration parameter defined in [V2G20-2320] is also set to this algorithm. If these parameters do not match, the EVCC shall regard the received message as invalid, and discard the message. Otherwise, the EVCC shall continue processing the data received in SignedInstallationData.

NOTE 3 This allows to protect EVCC against downgrade attacks, in case weaknesses in the default curve are discovered.

[V2G20-2707] Upon reception of SignedInstallationData, the EVCC shall check that the received encrypted contract key uses the ECC algorithm in accordance with the configuration parameter [V2G20-2320] or with the OEM provisioning certificate the EVCC provided in the CertificateInstallationReq, otherwise, the EVCC shall regard the received message as invalid, and discard the message.

NOTE 4 This means that if EVCC not equipped with a TPM uses an alternative curve and receives a SECP521_EncryptedPrivateKey, the EVCC will not process the SignedInstallationData.

[V2G20-2578] If all previous checks pass, the EVCC shall store the contract certificate chain and associated private key after having applied requirements as specified in 7.9.2.5 and its subclauses to decrypt the encrypted contract certificate private key and store it securely in the EVCC. Refer to 7.3.6 and its subclauses for secure storage of contract certificate private key.

NOTE 5 An EVCC with a TPM will store/install the contract certificate private key in TPM and follow the requirements for decryption of the private key for EVCCs with TPM. Similarly, an EVCC without a TPM will store/install the contract certificate private key in HSM (or whatever other mechanisms it is using to securely store the private keys) and follow the requirements for decryption of the private key for EVCCs without TPM.

[V2G20-2579] The ContractCertificateChain received by the EVCC in the CertificateInstallationRes Message shall be stored persistently in such a way, that it can be applied later on for the purpose of verifying PriceSchedules. The eMSP sub-CA2 certificate is required to verify PriceSchedules.

NOTE 6 It is not required that the EVCC is able to verify the certificate it has received. It is the task of the certificate provisioning service to provide only valid certificates.

###### 8.3.4.3.10 SessionStopReq/Res

####### 8.3.4.3.10.1 SessionStopReq/Res handling

This V2G message pair shall be used for terminating a V2G communication session initiated by preceding SessionSetupReq message.

####### 8.3.4.3.10.2 SessionStopReq

By sending the SessionStopReq the EVCC requests termination of the energy transfer process.

[V2G20-1271] The EVCC and the SECC shall implement the message elements as defined in Table 50 and Figure 54.