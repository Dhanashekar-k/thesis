RemainingContractCertificateChains to the minimum of the number of contract certificates available at the SECC minus one and the value given by MaximumContractCertificateChains in CertificateInstallationReq minus one.

[V2G20-1553] If the SECC receives more contract certificates from the secondary actor than indicated by the parameter MaximumContractCertificateChains in CertificateInstallationReq and the parameter PrioritizedEMAIDs is set, then the SECC needs to filter the installation of contract certificates based on PrioritizedEMAIDs.

The SECC shall send a request to a secondary actor upon the first CertificateInstallationReq to download all available contract certificates associated with the PCID of the OEM provisioning certificate that is sent within the CertificateInstallationReq.

[V2G20-2580] If contract certificates for both available (elliptic curve) ECs need to be provided for the same contract, the SECC will need to send multiple CertificateInstallationRes messages according to [V2G20-1550].

NOTE 1 It is up to the eMSP whether it wants to deploy certificates for both curves or only for the currently preferred curve.

[V2G20-1077] The certificate provisioning service shall sign the SignedInstallationData element of the CertificateInstallationRes using the private key associated with the CPS leaf certificate. It shall include the certificate chain for verification of this signature in the field CPSCertificateChain.

NOTE 2 The certificate provisioning service will verify that the data, which is covered by the signature, is received from the preceding secondary actor in an authentic manner.

[V2G20-1078] The EVCC shall verify the signature of the CertificateInstallationRes Message using the signer certificate chain CPSCertificateChain, validate said chain according to [V2G20-1001], [V2G20-2324] and [V2G20-2325] while leaving out the revocation check, and ensure that it traces back to a trusted root certificate.

[V2G20-2648] The EVCC shall ensure that the signature covers the SignedInstallationData element.

[V2G20-2649] If any of the aforementioned fails, the EVCC shall regard the received message as invalid, and discard the message. Otherwise, the EVCC shall continue processing the data received in SignedInstallationData.

[V2G20-2572] The EVCC shall check that the most significant byte (1 $ ^{st} $ byte from left) of DHPublicKey in SignedInstallationData is set to 0x04. If the most significant byte of DHPublicKey is not set to 0x04, the EVCC shall regard the received message as invalid, and discard the message. Otherwise, the EVCC shall continue processing the data received in SignedInstallationData.

[V2G20-2573] When the EVCC receives the parameter ECDHCurve (in SignedInstallationData) set to "SECP521", it shall check that the received DHPublicKey (in SignedInstallationData) is 133 bytes. If the received DHPublicKey is not 133 bytes, the EVCC shall regard the received message as invalid, and discard the message. Otherwise, the EVCC shall continue processing the data received in SignedInstallationData.

[V2G20-2574] When the EVCC receives the parameter ECDHCurve (in SignedInstallationData) set to "X448", it shall check that the received DHPublicKey (in SignedInstallationData) is 57 bytes. If the received DHPublicKey is not 57 bytes, the EVCC shall regard the