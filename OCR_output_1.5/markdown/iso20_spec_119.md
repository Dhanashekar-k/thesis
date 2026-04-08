NOTE 7 Refer to B.7.1 for the OEM provisioning certificate profile associated with the algorithm specified by [V2G20-2674].

NOTE 8 If EVCC is equipped with TPM 2.0, the EVCC will perform the direct TPM import and apply requirement [V2G20-2523] instead.

[V2G20-2534] If the EVCC receives the parameter ECDHCurve set to "X448", it shall use the private key associated with the "Alternate Subject Public Key" of the OEM provisioning certificate along with the public key calculated from [V2G20-2532] for calculation of the session key as defined by [V2G20-2535].

NOTE 9 Refer to B.7.2 for the OEM provisioning certificate profile associated with the algorithm specified by [V2G20-2319] and [V2G20-2674].

NOTE 10 If EVCC is equipped with TPM 2.0, the EVCC will perform the direct TPM import and apply requirement [V2G20-2523] instead.

2G20-2535] For session key agreement, the ephemeral-static ECDHE protocol "6.2.2.2 One-Pass Diffie-Hellman, C(1, 1, ECC CDH)" as defined in NIST Special Publication 800-56A shall be used. The KDF shall be the "concatenation key derivation function", where the hash function shall be SHA512. In case the curve corresponding to ECC signature algorithm specified by [V2G20-2319] is chosen, the input parameters for KDF including the shared secret shall be derived according to IETF RFC 7748. The SA shall act as party U (as defined in said NIST document) and the EVCC shall act as party V. The protocol shall use elliptic curves as defined in Annex B. The algorithm ID shall be one character 0x01. The sender name ID U shall be one character "U" = 0x55, the receiver name ID V shall be one character "V" = 0x56. A symmetric encryption key of exactly 256 bits shall be derived.

NOTE 11 The authenticity of the transmission is ensured by the surrounding signature. The authenticity check is vital for the security of the ECDHE protocol.

NOTE 12 For a more detailed explanation please refer to Figure 27.

V2G20-822] A certificate whose key pair is used for ECDHE shall have its key Agreement flag set. This applies to all OEM provisioning certificates and shall be enforced by all participating parties.