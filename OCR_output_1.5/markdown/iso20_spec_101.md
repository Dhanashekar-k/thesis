NOTE 5 For example, if the EVCC sends a CertificateInstallationReq containing OEM provisioning certificate based on algorithm defined in [V2G20-2674] but the SA's configuration in [V2G20-2320] indicates usage of algorithm defined in [V2G20-2319], the SA fails to verify the signatures received in CertificateInstallationReq message.

[V2G20-1000]

Both, the r- and the s-values shall always be transferred with their maximum length. If any of these values is shorter, it shall be filled up with leading zeros. The receiver shall assign the first half of the bytes to r and the second half of the bytes to s. This encoding is described in IETF RFC 4050:2005, 3.3.



NOTE 6 The r- and s-values are the output of the ECDSA or EdDSA and consist of a pair of integers.

##### 7.9.2.5 Certificate provisioning

In this document, the contract certificates are created and then distributed from an SA to the EVCC. In order to minimize roundtrips and communication processing time, and ease organizational processes, it was decided, that the SA (and not the EVCC) generates the key pair for the certificate, uses the key pair to then generate the corresponding certificate itself, and finally distributes the certificate and the corresponding private key to the EVCC. Since the private key is kept confidential, appropriate security mechanisms should be used for secure transmission of the contract certificate private key.

The eMSP creates credentials (SignedInstallationData) for the EVCC, consisting of a contract certificate including the encrypted contract certificate private key (the key is encrypted specifically for that EVCC). The contract certificate and the encrypted private key can then be distributed to the EVCC via an online installation service through the EVSE.

The contract certificate and the associated private key can also be distributed to the EVCC via offline/out-of-band installation. This document does not mandate offline or online contract certificate installation. Refer to H.5 for further details of offline contract certificate installation.

For online installation via the EVSE, the eMSP then forwards the credentials to the certificate provisioning service (CPS). The CPS asserts the correctness and authenticity of the credentials with a signature and relays the signed message fragment to the SECC, who compiles a CertificateInstallationRes message and transmits that to the EVCC. The certificate provisioning service is considered trustworthy. It is therefore not required that the EVCC is able to verify the contract certificate it has received via the CertificateInstallationRes.

The role "certificate provisioning service" can be assumed, for example, by the eMSP itself, the EVSE operator or a completely stand-alone service.

Figure 15, Figure 25 and Figure 26 illustrate operations performed by all involved actors to ensure a secure delivery of the contract certificate data to the intended EVCC without and with the usage of TPM 2.0, respectively. In order to inform a SA that an EVCC is equipped with a TPM and that the contract certificate private key should be encrypted for this TPM, the information about the EVCC's TPM is included by the OEM in a non-critical (optional) extension of the OEM provisioning certificate (see Figure 25). In case of a TPM-equipped EVCC, as signaled by the respective extension in the OEM provisioning certificate, the SA/eMSP should encrypt the private contract key for the EVCC's TPM according to 7.9.2.5.3 and its subclauses.

###### 7.9.2.5.1 Common requirements for contract certificate installation in EVCC

[V2G20-2480] Unless specified otherwise, the SA (eMSP) shall use big-endian order for all bit strings and calculations specified by this subclause and the subclauses within.

[V2G20-2481] Unless specified otherwise, the EVCC shall use big-endian order for all bit strings and calculations specified by this subclause and the subclauses within.

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.