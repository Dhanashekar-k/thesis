
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>XML message</td><td style='text-align: center; word-wrap: break-word;'>Protected fields</td><td style='text-align: center; word-wrap: break-word;'>Encrypting entity (sender)</td><td style='text-align: center; word-wrap: break-word;'>Decrypting entity (receiver)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CertificateInstallationRes</td><td style='text-align: center; word-wrap: break-word;'>SECP521_EncryptedPrivateKey</td><td style='text-align: center; word-wrap: break-word;'>secondary actor</td><td style='text-align: center; word-wrap: break-word;'>EVCC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CertificateInstallationRes</td><td style='text-align: center; word-wrap: break-word;'>X448_EncryptedPrivateKey</td><td style='text-align: center; word-wrap: break-word;'>secondary actor</td><td style='text-align: center; word-wrap: break-word;'>EVCC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CertificateInstallationRes</td><td style='text-align: center; word-wrap: break-word;'>TPM_EncryptedPrivateKey</td><td style='text-align: center; word-wrap: break-word;'>secondary actor</td><td style='text-align: center; word-wrap: break-word;'>EVCC</td></tr></table>

[V2G20-2312] Each V2G entity shall be able to generate XML signatures as specified in Table 17.

[V2G20-2313] Each V2G entity shall be able to verify XML signatures as specified in Table 17.

[V2G20-2477] Each V2G entity generating XML signatures shall utilize the private key associated with the "subjectKeyInfo" parameter of the appropriate certificate, as specified in Table 17, to generate the XML signatures.

[V2G20-2478] Each V2G entity verifying XML signatures shall utilize the public key included in the "subjectPublicKeyInfo" parameter of the appropriate certificate, as specified in Table 17, to verify the XML signatures.

[V2G20-2479] The SA receiving a CertificateInstallationReq indicating the SignatureMethod as defined by [V2G20-2474] shall use the public key in "subjectPublicKeyInfo" of the OEM provisioning certificate contained in CertificateInstallationReq message to verify the signature.

NOTE 1 The key in the extension "subjectAltKey" is encoded for use only in ECDH algorithm. It cannot be used to verify signatures using the Ed448 algorithm.

[V2G20-2699] When generating or verifying the XML signatures, each V2G entity shall utilize the public/private key associated with the appropriate certificate (as specified in Table 17) that uses the algorithm as indicated by the configuration in [V2G20-2320].

NOTE 2 This means that when the configuration in [V2G20-2320] indicates usage of algorithm defined in [V2G20-2674], the V2G entity can use keys from appropriate certificate (as specified in Table 17) based on algorithm defined in [V2G20-2674]. Similarly, when the configuration in [V2G20-2320] indicates usage of algorithm defined in [V2G20-2319], the V2G entity can use keys from appropriate certificate (as specified in Table 17) based on algorithm defined in [V2G20-2319].

[V2G20-2700]

When generating the XML signatures, if the V2G entity does not possess appropriate certificate (as specified in Table 17) that uses the algorithm as indicated by the configuration in [V2G20-2320], it shall fail to generate the necessary XML signatures and take steps as defined for the particular message sequence.



NOTE 3 For example, if the contract certificates contained in the EVCC are based on algorithm defined in [V2G20-2674] but the EVCC's configuration in [V2G20-2320] indicates usage of algorithm defined in [V2G20-2319], the EVCC does not utilize those contract certificates in AuthorizationReq message(s) it sends.

NOTE 4 The example above is possible in cases where the EVCC was recently switched over from algorithm defined in [V2G20-2674] to algorithm defined in [V2G20-2319] (via changes to the configuration defined in [V2G20-2320]) while leaving the existing certificates intact in the EVCC.

[V2G20-2701]

When verifying the XML signatures, if the V2G entity does not possess appropriate certificate (as specified in Table 17) that uses the algorithm as indicated by the configuration in [V2G20-2320], it shall fail to verify the necessary XML signatures and take steps as defined for the particular message sequence.

