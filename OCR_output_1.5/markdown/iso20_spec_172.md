When the EVCC does not possess a valid contract certificate or the contract certificate is due to expire soon or the EVCC needs a new contract certificate (for example when the existing contract certificate is not accepted at the particular EVSE where the EV is currently charging, etc.) or EV wants to simply check if a new contract certificate is available, the EVCC can trigger an installation of a new contract certificate into the EVCC. In this use case the EVCC requests available contract certificates from the SECC to be installed into the EVCC. This procedure typically happens before PnC charging since PnC charging with authorization can only be started if a valid contract certificate is available in the EVCC. The SECC may request the certificate from a SA.

The installation of multiple contract certificates is realized with a loop of CertificateInstallation message pairs. Depending on SECC and SA implementations, the SECC may, however, only need to send the first CertificateInstallationReq to the SA in order to retrieve all available contract certificates associated with the OEM provisioning certificate's PCID. Each CertificateInstallationReq/Res message pair between the EVCC and the SECC is used to install exactly one of the available contract certificate chains (including the related sub-CA certificates) and the encrypted private key.

In contrast to ISO 15118-2, both the installation and update of a contract certificate are performed with the CertificateInstallationReq/Res message pair. The CertificateUpdateReq/Res message pair has been removed from this version. The initial installation and later update of one or more contract certificates may take up to several minutes depending on the existing communication link between the SECC and the secondary actors and the number of contract certificates to be installed into the EV. Therefore, it is recommended to not initiate a certificate installation process during each charging session. This avoids unnecessary traffic to the backend as, in most cases, there will not be a new certificate available yet.

The OEM may want to apprise the driver that in cases where contract certificate installation is needed before entering a charging loop, it might take more time than usual for the charging process to start.

The implementation of the CertificationInstallationReq/Res is optional for both EV and EVSE. If the EV does support CertificationInstallationReq/Res messages, the OEM is required to install an OEM provisioning certificate in the EVCC. In such cases, the procedure described here can be used for the installation of the contract certificate.

If no OEM provisioning certificate is available in the EVCC, the procedure described in 8.3.4.3.3.2 (and its sub clauses) cannot be used for contract certificate installation. In these cases the contract certificate should be installed into the EVCC by other means. Mechanisms other than using an OEM provisioning certificate for installing the contract certificate are out of the scope of this document.

For details on OEM provisioning certificates refer to H.4.

NOTE 1 The SECC can request the signed contract data at a secondary actor, if it has online capabilities.

NOTE 2 If the SECC is not able to deliver the requested certificates an appropriate error handling should be performed. If an EVSE is not able to support this function in general, it is supposed to be marked for instance as "offline EVSE" (e.g. by a label at the EVSE). If the EVCC does not possess a valid contract certificate associated with a legal contract, it is not able to use PnC until a certificate installation process is performed successfully.

NOTE 3 For a more detailed explanation of the certificate installation process, see 7.9.2.5 and its subclauses.

####### 8.3.4.3.9.2 CertificateInstallationReq

By sending the CertificateInstallationReq, the EVCC requests the SECC to deliver the certificates that belong to the currently valid contracts of the EV user.

[V2G20-2684]

The EVCC shall possess a certificate and corresponding private key usable for signature and key agreement to support the decryption of encrypted information.

