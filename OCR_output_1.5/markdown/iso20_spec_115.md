NOTE 8 The policy digest is part of the TPM key profile (see "authPolicy") and is created using the "nameAlg" algorithm of the key. In case of the default ECC algorithm as defined by [V2G20-2674], the EVCC's TPM policy digest uses SHA-512 and is 64 byte long (see Table 19).

NOTE 9 The actual content of the contract key sealing policy is up to the OEM.

####### 7.9.2.5.3.3 Contract certificate private key encryption mechanism for EVCC with TPM

2.0

[V2G20-2518] In order to enable a direct import of the encrypted contract certificate private key into the EVCC's TPM, the contract certificate private key shall be encrypted with the TPM storage key of the EVCC's TPM from the OEM provisioning certificate extension (in contrast to [V2G20-2529] and [V2G20-2530]). This encryption shall comply with ISO/IEC 11889-1:2015, 23.3.2 and only use the outer duplication wrapper. This encryption shall use the values from Table 19 for the default ECC algorithm (see [V2G20-2674]) or a separately defined TPM key profile for an alternative ECC algorithm (see [V2G20-2319]), whereby the contract certificate public key is inserted into the buffers of the contract key profile's "unique" field. If a policy digest is provided in the OEM provisioning certificate of this EVCC, the value of the policy digest shall be included in the encryption of the contract certificate private key via the "authPolicy" field of the contract key profile.

NOTE 1 The high-level overview of the contract certificate private key encryption for direct import into the EVCC's TPM is shown in Figure 26.

NOTE 2 The values from Table 19 are necessary to calculate the "Name" (see ISO/IEC 11889-1:2015, Clause 16) of the asymmetric contract key in TPM 2.0 or when parameter selection is based on the "new parent" (in this context the new parent would be the storage key). Table 19 also shows the values for the key profile in the case that the OEM chooses to not seal the contract key to a policy, i.e. for the case that the optional policyDigest field of the custom TPM certificate extension in the OEM provisioning certificate is omitted.

[V2G20-2519] The encryption, as specified by [V2G20-2518], requires the generation of a new seed (session key). The seed shall be generated using the method defined in 7.9.2.5.3., with the "TPM storage key" from the OEM provisioning certificate extension used as static public key for calculation of the session key as defined by [V2G20-2535]. Also refer to ISO/IEC 11889-3:2015, B.5.1 for further details with respect to TPM 2.0.

NOTE 3 The seed is used to derive HMAC and encryption keys (see Figure 26).

[V2G20-2520] The ephemeral public key of the eMSP (SA) shall be transmitted using the method defined in [V2G20-2489].

[V2G20-2521] The encrypted contract certificate private key shall be transmitted within TPM_EncryptedPrivateKey in the message CertificateInstallationRes if the private contract key was encrypted with the public storage key from the OEM provisioning certificate extension carrying TPM Information. The SA shall not add any padding to the encrypted key to increase its size to the maximum size of 206 bytes.

NOTE 4 At the time of CertificateInstallationReq, if the SA intends to provide multiple different contract certificates based on different curves as defined by [V2G20-2674] and [V2G20-2319], the SA will need to send multiple different SignedInstallationData containers to the SECC and the EVCC can, at its/user's discretion, utilize the looping mechanism for CertificateInstallationReq to get and install all different contract certificates.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.