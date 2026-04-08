The SA shall use the same (elliptic curve) EC to generate the contract certificate key pair and to encrypt the contract certificate private key as the one used in the EVCC's OEM provisioning certificate, except for the case when the SA's configuration parameter according to [V2G20-2320] does not allow to use this curve.

NOTE 1 In case the SA's configuration parameter according to [V2G20-2320] does not allow to use the (elliptic curve) EC as used in the EVCC's OEM provisioning certificate [V2G20-2709] will apply.

NOTE 2 At the time of CertificateInstallationReq, if the SA intends to provide multiple different contract certificates based on different curves as defined by [V2G20-2674] and [V2G20-2319], the SA will need to send multiple different SignedInstallationData containers to the SECC and the EVCC can, at its/user's discretion, utilize the looping mechanism for CertificateInstallationReq to get and install all different contract certificates.

[V2G20-2709]

In case SA's configuration parameter as defined by [V2G20-2320] does not allow the SA to use the elliptic curve from the EVCC's OEM provisioning certificate, i.e. SA considers this curve insecure, the SA shall not provide a contract certificate.



NOTE 3 The CertificateInstallationReq message is signed using the OEM provisioning certificate that is contained within the CertificateInstallationReq message itself. The signatures on CertificateInstallationReq message are validated using the public key contained in the OEM provisioning certificate. Before the OEM provisioning certificates public key can be used to validate the signatures on CertificateInstallationReq message, the OEM provisioning certificate is validated. If this OEM provisioning certificate validation fails, the SECC sends the appropriate ResponseCode starting with "WARNING_" as defined in 8.6 and its subclauses.

NOTE 4 If this OEM provisioning certificate validation fails because the SECC/SA cannot process the curves in OEM provisioning certificate (due to changes to configuration parameter as defined by [V2G20-2320]), the SECC sends the ResponseCode "WARNING_CertificateValidationError" as defined in 8.6 and its subclauses.

NOTE 5 Communication between the SECC and the SA is not in the scope of this document. As such the exact error message sent by SA in cases described above is not defined by this document. This document simply provides the ResponseCode that the SECC is supposed to use in these circumstances.

20-2487] If the SA uses the elliptic curve corresponding to signature algorithm specified by [V2G20-2674 for contract certificate private key encryption key generation via ECDHE as specified in 7.9.2.5.4, it shall set ECDHCurve parameter in SignedInstallationDataType element of CertificateInstallationRes message to "SECP521".

[V2G20-2488] If the SA uses the elliptic curve corresponding to signature algorithm specified by [V2G20-2319] for contract certificate private key encryption key generation via ECDHE as specified in 7.9.2.5.4, it shall set ECDHCurve parameter in SignedInstallationDataType element of CertificateInstallationRes message to "X448".

[V2G20-2489] The ephemeral public key used in requirement [V2G20-2497] shall be contained in the XML element "DHPublicKey" encoded in its uncompressed form as "Subject Public Key" as defined in IETF RFC 5480.

NOTE 6 DHPublicKey is maximum 133 bytes long. The first byte has the fixed value 0x04 indicating the uncompressed form.

NOTE 7 When ECDHCurve is set to "SECP521", the DHPublicKey is 133 bytes long. When ECDHCurve is set to "X448", the DHPublicKey is 57 bytes long.

NOTE 8 IETF RFC 5480 has been updated by IETF RFC 8813. These updates are considered to be included in this document.