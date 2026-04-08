NOTE 3 See Figure 16 for a pictorial reference.

<div style="text-align: center;"><img src="imgs/img_in_image_box_289_217_832_329.jpg" alt="Image" width="45%" /></div>


<div style="text-align: center;">Figure 16 — AAD calculation</div>


######## 7.9.2.5.2.2 Contract certificate private key encryption mechanism for EVCC without TPM 2.0

######### 7.9.2.5.2.2.1 Common requirements for encryption of 521-bit and 448-bit contract certificate private keys for EVCC without TPM 2.0

V2G20-2493] The private key corresponding to the contract certificate shall be transmitted only in encrypted format within SECP521_EncryptedPrivateKey or X448_EncryptedPrivateKey element in the SignedInstallationData parameter of the CertificateInstallationRes message.

NOTE 1 SECP521_EncryptedPrivateKey is used when the contract certificate provided in SignedInstallationData is based on curve as defined by [V2G20-2674]. X448_EncryptedPrivateKey is used when the contract certificate provided in SignedInstallationData is based on curve as defined by [V2G20-2319].

NOTE 2 At the time of CertificateInstallationReq, if the SA intends to provide multiple different contract certificates based on different curves as defined by [V2G20-2674] and [V2G20-2319], the SA will need to send multiple different SignedInstallationData containers to the SECC and the EVCC can, at its/user's discretion, utilize the looping mechanism for CertificateInstallationReq to get and install all different contract certificates.

[V2G20-2494] The sender shall ensure that the authenticated encryption function used to encrypt data produces an authentication tag (also known as "tag" for short) of 128 bits. Refer to 5.2.1.2 of NIST Special Publication 800-38D for further details.

[V2G20-2495] When using 448-bit ephemeral public key in requirement [V2G20-2497], the sender shall not include any extra filler/padding bytes to reach DHPublicKey size of 133 bytes.

[V2G20-2496] Once the sender sends the data to the certificate provisioning service (CPS) for verification and signature generation, the sender shall irretrievably erase/delete/destroy the contract certificate private key, ECDHE private key and the session key as generated in 7.9.2.5.4, and the ciphertext.

NOTE 3 This ensures that the contract certificate private key cannot be compromised through a compromised SA. It also ensures that the ECDHE private key or session key are not reused. It further ensures that the same ciphertext is not sent out again to the receiver.

NOTE 4 This requirement is simply referring to unencrypted contract certificate private keys, ciphertext, session keys, etc. It does not refer to the SignedInstallationData that the eMSP gets back from the CPS which includes the CPS certificates and the CPS signature on the entire data. It also does not refer to the ECDH public key that the eMSP sends to the EVCC in DHPublicKey parameter.

######### 7.9.2.5.2.2.2 Encryption of 521-bit contract certificate private key for EVCC without TPM 2.0

The 521-bit private key corresponding to the contract certificate shall be encrypted by the sender (the SA (eMSP)) using the session key derived in the ECDHE protocol (see 7.9.2.5.4). The sender shall apply the algorithm AES-GCM-256 according to NIST

## 100 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.