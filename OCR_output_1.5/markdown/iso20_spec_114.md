######## 7.9.2.5.3.2 OEM provisioning certificate for EVCC with TPM 2.0

[V2G20-2512] The OEM provisioning key pair shall be generated using the provisioning key profile from Table 19 for the default ECC algorithm (see [V2G20-2674]) or a separately defined TPM key profile for an alternative ECC algorithm (see [V2G20-2319]).

NOTE 1 The OEM can generate the OEM provisioning key pair in a secure environment. Key generation can be done in a secure fashion and can follow the necessary security guidelines. OEM can achieve this by generating the key pair in the EVCC's TPM using the protected functionality of the EVCC's TPM, which fulfils the respective security requirements (CC EAL4+).

NOTE 2 In case of a TPM-equipped EVCC, the OEM provisioning key pair can be generated in the EVCC's TPM and never leave this TPM. This ensures that only the intended EVCC has access to the OEM provisioning certificate private key and that this key cannot be copied to and used by any other system, e.g. to request contract certificates (identity theft). These guarantees are especially critical for this credential due to its long lifetime.

NOTE 3 After generating the OEM provisioning key pair in the EVCC's TPM, the OEM reads out the public portion of the OEM provisioning key pair in order to generate the OEM provisioning certificate.

[V2G20-2513] If the OEM provisioning key pair is generated outside the TPM, the parameters "fixedTPM" and "fixedParent" in the "objectAttributes" field of the public area shall be set to 0. If the OEM provisioning key pair is generated within the TPM, the parameters "fixedTPM" and "fixedParent" in the "objectAttributes" field shall be set to 1.

[V2G20-2514] The OEM provisioning key pair shall be stored in the EVCC's TPM underneath the storage key corresponding to the ECC algorithm used to generate this key (see [V2G20-2320]).

NOTE 4 The OEM can store the OEM provisioning key pair in the EVCC's TPM in a secure environment using secure mechanisms.

[V2G20-2515] If the OEM provisioning key pair in the EVCC's TPM is desired to be sealed to an OEM specific policy, this policy shall be provided in the "authPolicy" of the key (see Table 19).

NOTE 5 Policies are part of the TPM’s enhanced authorization capability. A policy is a set of assertions that can be validated before authorizing key usage and can be used to, e.g. ensure that the EVCC booted into a trusted software state before authorizing the usage of the OEM provisioning key. Policies are calculated using the "nameAlg" of the key (see Table 19). The actual content of the sealing policy for the OEM provisioning key is up to the OEM.

[V2G20-2516] The OEM provisioning certificate for an OEM provisioning public key shall include the public key of its parent storage key pair in the EVCC's TPM to be used in ECDHE into the "TPMStorageKey" extension of the OEM provisioning certificate as defined in [V2G20-2594] and [V2G20-1226]. The uncompressed form is to be used exclusively.

NOTE 6 This allows the OEM to indicate that the EVCC is equipped with a TPM 2.0 and to provide the necessary information regarding the EVCC's TPM to the eMSP (or other SAs) in a cryptographically secure fashion.

NOTE 7 According to [V2G20-2595] this extension indicates that an SA/eMSP can use the method described in 7.9.2.5.3 (and its subclauses) to encrypt the private contract certificate key for this EVCC.

[V2G20-2517] If the contract certificate keys are supposed to be sealed to a policy, the digest of the EVCC's TPM policy shall be included in the "TPMPPolicyDigest" extension of the OEM provisioning certificate as defined in [V2G20-2594] and [V2G20-1226]. The big-endian byte order rule shall be applied.