[V2G20-2523]

If the contract certificate private key was transmitted within the TPM_EncryptedPrivateKey field in the message CertificateInstallationRes and the EVCC with TPM 2.0 fully supports the respective curve, the EVCC shall directly import the encrypted contract key into its TPM underneath the storage key using the values from Table 19 for the curve P-521/secp521r1 or a separate TPM key profile for the curve Ed448.



NOTE 1 The direct import of encrypted contract keys into the TPM is done using the TPM2_Import() command with the storage key as new parent. Refer to ISO/IEC 11889-3:2015 for further details of TPM2_Import() command.

NOTE 2 The direct import of the encrypted contract certificate private key requires the EVCC to provide both the public and the encrypted private part of the contract key object as input to the TPM. The public part of the contract key object in TPM 2.0 consists of the contract key profile values from Table 19 (for the default ECC algorithm) with the contract certificate public key from the received contract certificate inserted into the "unique" field of this key profile.

NOTE 3 TPM_EncryptedPrivateKey can contain secp521 (see [V2G20-2674]) or Curve448 (see [V2G20-2319]) based encrypted contract private key. Assuming SA chooses the ECDHCurve parameter based on the ECC algorithm of the EVCC's OEM provisioning certificate, when the EVCC receives the parameter ECDHCurve set to "SECP521", TPM_EncryptedPrivateKey is expected to be 206 bytes long (see Figure 26). The respective value for an alternative ECC algorithm can be derived using TPM Key Profile for this algorithm.

###### 7.9.2.5.4 Encryption/decryption (session) key generation for the distribution of secret keys

ISO 15118 communication uses an ephemeral-static Diffie-Hellman key exchange protocol to derive a session key where the receiver's keys are static. The SA (eMSP) uses this session key to transmit the private key in encrypted form to the EVCC.

In the ephemeral-static variant of the Diffie-Hellman protocol, the public key of the receiver (EVCC) does not change, i.e. is static, and is already known to the sender (eMSP). The sender, however, still uses an ephemeral public key that is transmitted to the receiver. In this manner, both sender and receiver can derive the same session key without a reply message from the receiver.

Since the SA uses ephemeral keys, the derived session keys will be different for each instance (distribution) of the secret keys (private key).

NOTE 1 The ephemeral-static Diffie-Hellman protocol does not provide perfect forward secrecy, i.e. if the static private key of the EVCC (OEM provisioning certificate) is leaked to an adversary, then this adversary can derive the respective session key(s) and decrypt any past and future communication between the eMSP and EVCC that relies on the private key of OEM provisioning certificate (or a key derived from the private key of OEM provisioning certificate) for secrecy. The same is true for the ephemeral private key of the eMSP (in case eMSP reuses this key, all transfers will be affected). In addition, the EVCC leaking the OEM provisioning private key allows an adversary to impersonate this EVCC and generate signatures as if the adversary is/was the EVCC, as the basic key used for signatures is the same as the basic key used for encryption, i.e. the private key of the OEM provisioning certificate.

[V2G20-2710]

If SA uses the elliptic curve corresponding to signature algorithm specified by [V2G20-2319], the SA (eMSP) shall additionally support X448 as specified by IETF RFC 7748 for calculation of the ECDHE secret and key-derivation for the encryption of private keys.



[V2G20-2711] If EVCC uses the elliptic curve corresponding to signature algorithm specified by [V2G20-2319], the EVCC shall additionally support X448 as specified by IETF RFC 7748 for calculation of the ECDHE secret and key-derivation for the decryption of encrypted information like private keys.