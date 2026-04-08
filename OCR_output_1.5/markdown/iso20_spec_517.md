# Annex H (informative)

# Application of certificates

### H.1 General information

This clause and its subclauses provides specific and separate requirements for the private SECC and the SECC. Thus, unless otherwise specified, private SECC and SECC are not considered interchangeable.

NOTE Only certain parts of this annex (H.1.5 and its subclauses, H.1.6, H.2 and its subclauses, H.6 and H.7) have been fully reviewed and updated in this document. The rest (H.1 and its subclauses not listed previously, H.3, H.4 and H.5 and its subclauses) will be improved upon in the next edition. It is important for the implementers to be careful when reading and designing systems relying on information mentioned in those clauses that have not been reviewed and updated in this document.

#### H.1.1 Overview

This annex provides an overview about the application of the certificates and the demands which need to be fulfilled by the certificate concept implemented in this document. It also explains the certificate parameters like validity, size, chain length and others.

## Informative Information:

In the charge protocol, the following types of certificates are used.

V2G root CA certificates: These are globally valid (top level) root certificates of the PKI (public key infrastructure). They are used to check the authenticity of certificates. The corresponding private keys are in possession of the respective root CAs.

– eMSP root CA certificate: This kind of certificate is used to sign (via a chain of sub-CAS) contract certificates.

– Contract certificate: This kind of certificate is used in the PnC use case (i.e. contract-based charging) to represent a contract between an EV and a secondary actor (the eMSP). It is stored in an EVCC along with the corresponding private key. The EVCC uses it to prove the existence of the corresponding contract to the EVSE. Contract certificates are derived from an eMSP root CA certificate.

– SECC certificate: This kind of certificate is used to authenticate the SECC to the EVCC. The corresponding private key is in possession of the SECC. SECC certificates are derived from the V2G root CA certificates mentioned above.

– PE private root CA certificate: A PE private root CA certificate is very similar to an eMSP root CA certificate. The only difference is that it is organizationally handled differently (described in H.1.2). Its purpose is to facilitate setting up private charging infrastructure for cars that are under immediate control of the infrastructure owner.

– PE certificate: This kind of certificate is used to authenticate the private SECC to the EVCC. The corresponding private key is in possession of the private SECC. PE certificates are derived from the PE private root CA certificates mentioned above.

OEM provisioning certificate: This kind of certificate is individual for each EVCC (installed, e.g. at EV production) and used to verify the identity of an EVCC at the beginning of the contract