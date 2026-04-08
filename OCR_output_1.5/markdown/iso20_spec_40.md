Certificate governance and lifecycle management is a major aspect of any PKI system to secure the PKI, build trust and provide the necessary assurance. However, these aspects of the PKI system are outside the scope of this document.

A certificate, in and of itself, does not provide assurance on how the certificate holder ensures that the private key associated with the certificate is not compromised, what is the guarantee that the holder of the certificate is actually who they say they are, steps the CA will take when a private key is compromised, etc. That assurance and trust in the certificates comes through a certificate policy, certification practice statement, etc. certificate policy (CP) and certification practice statement (CPS) contain the topics as defined IETF RFC 3647.

X.509 defines a CP as "a named set of rules that indicates the applicability of a certificate to a particular community and/or class of application with common security requirements".

Per IETF RFC 3647, "When a certification authority (CA) issues a certificate, it is providing a statement to a certificate user (i.e. relying party) that a particular public key is bound to a particular entity (i.e. certificate subject). The extent to which the certificate user should rely on that statement needs to be assessed by the certificate user." The certificate policy provides the information that can be used by a certificate user to decide whether or not to trust a certificate.

Certificate policies are also used to establish trust relationships between CAs (i.e. cross certification). When CAs issue cross certificates, one CA assesses and recognizes one or more certificate policies of the other CA.

Mostly the CAs post the CP, CPS, audit results, etc. publicly so that the certificate users can see how the CA ensures the security of the keys, identity of the certificate holders, manages the certificate lifecycle, etc. and develop trust in the CA.

[V2G20-2349] Any certificates originating from, or cross-signed by, a V2G root CA certificate chain or eMSP root CA certificate chain or OEM root CA certificate chain shall follow a well-established certificate governance structure, including but not limited to CP, CPS, etc.

[V2G20-2350] Any certificates originating from a PE private root CA certificate chain are not required to follow [V2G20-2349] if the private SECC using them is not scheduled to support PnC.

NOTE This does not mean that a governance structure cannot be used in PE. This just says it is not mandated.

[V2G20-2351] Any certificates originating from a PE private root CA certificate chain are required to follow [V2G20-2349] if the private SECC using them is scheduled to support PnC utilizing contract certificates.

This document does not provide any certificate governance structure. With many industry participants, this document leaves it to those participants, the CAs, PKI implementers, etc. to define the certificate governance structure that best suits their use cases. It is envisioned that the industry will automatically gravitate towards robust and secure CAs who have strong CP/CPS and provide periodic audit results along with verifiable data proving that they actually adhere to their CP/CPS.

#### 7.3.3 Number of root certificates and root validity

This subclause defines requirements for storage space for number of various types of root CA certificates for the SECC and EVCC. This subclause does not mandate actual installation of these various root CA certificates in the SECC or EVCC. It is up to the discretion of the CSOs to decide which root CA certificates they want to install in their SECCs and to the OEMs to decide which root CA certificates they want to install in their EVCCs. For example, an OEM may want to support a specific PE for a certain fleet of vehicles.