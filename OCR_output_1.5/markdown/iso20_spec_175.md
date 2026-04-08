[V2G20-1548] The EVCC shall sign the body element of CertificateInstallationReq using the private key associated with the "subjectKey" of its OEM provisioning certificate.

NOTE 2 The secondary actor providing the contract certificate will validate the OEM provisioning certificate according to [V2G20-1001], [V2G20-2324] and [V2G20-2325] and verify the signature of the body element of the CertificateInstallationReq using the public key (from "subjectPublicKey") of OEM provisioning certificate included in OEMProvisioningCertChain parameter of CertificateInstallationReq message.

NOTE 3 If necessary, the secondary actor will obtain all of the parent certificates in order to validate the OEM provisioning certificate.

NOTE 4 Refer to B.7 for details of "subjectKey" of OEM provisioning certificate.

## [V2G20-2708]

In the CertificateInstallationReq message, the EVCC shall use the OEM provisioning certificate in accordance with the configuration mechanism defined in [V2G20-2320]. In case EVCC supports multiple curves, it may send multiple CertificateInstallationReq messages, using the OEM provisioning certificate corresponding to the respective curve.

NOTE 5 SA is expected to generate and encrypt the contract certificate credentials using the same curve as the provided OEM provisioning certificate does. In case SA considers the curve or ECC algorithm used in the provided OEM provisioning certificate insecure, i.e. the SA's configuration parameter from [V2G20-2320] does not match the one of the EVCC, the SA will not be able to provide a contract certificate.

## [V2G20-1550]

Upon receiving a CertificateInstallationRes, the EVCC shall send another CertificateInstallationReq if the parameter RemainingContractCertificateChains of the CertificateInstallationRes is greater than 0 and the maximum number of contract certificates that can be installed, as indicated by the parameter MaximumContractCertificateChains in CertificateInstallationReq, has not yet been reached.

[V2G20-2571] The EVCC shall stop sending CertificateInstallationReq if the maximum number of contract certificates that can be installed, as indicated by the parameter MaximumContractCertificateChains in CertificateInstallationReq, has been reached while the parameter RemainingContractCertificateChains of the CertificateInstallationRes is greater than zero.

[V2G20-1551] The number of entries of the parameter PrioritizedEMAIDs shall not exceed the value given by MaximumContractCertificateChains.

####### 8.3.4.3.9.3 CertificateInstallationRes

After receiving the CertificateInstallationReq from the EVCC, the SECC sends the CertificateInstallationRes which may include one of the requested certificates. If CertificateInstallationRes includes a certificate, the EVCC installs this certificate as a contract certificate and requests transmission of the other contract certificates, if more are available and EV would prefer to install them all.

## [V2G20-1266]

The EVCC and the SECC shall implement the message elements as defined in Table 49 and Figure 53.