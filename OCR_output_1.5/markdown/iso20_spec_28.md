NOTE 5 The design and implementation of this configuration mechanism is not in the scope of this document.

NOTE 6 secp521r1 is a very common ECC algorithm supported by NIST. Curve Ed448 is not as widely used at the time of the publication of this document. Although there are quite a few implementations supporting curve Ed448, secp521r1 is used as the main curve due to its ubiquity. In case flaw(s) are found in the secp521r1, availability of the alternative curves allows implementers to quickly switch to a parallel algorithm without the need for implementation and validation of a new cryptographic algorithm. This ensures that the implementers/operators can quickly respond to any reported vulnerabilities in secp521r1.

[V2G20-2321]

As long as no issues or flaws are identified in the (elliptic curve) EC as specified by [V2G20-2674], the (elliptic curve) EC as specified by [V2G20-2674] shall be considered the preferred ECC algorithm. The mechanism defined by [V2G20-2320] shall only be updated to usage of (elliptic curve) EC as defined by [V2G20-2319] when there are issues/flaws identified with the (elliptic curve) EC as specified by [V2G20-2674].



NOTE 7 By default the mechanism defined by [V2G20-2320] can be set to use (elliptic curve) EC as specified by [V2G20-2674].

[V2G20-2675] Each V2G entity shall support a key length of 521 bits for ECC based asymmetric cryptography.

NOTE 8 Additionally, key length of 448 bits is used with certain curves in the application of this document. If a V2G entity can manage and utilize 521 bit keys, it can be capable of managing and utilizing 448 bit keys as well.

[V2G20-2322] Each certificate shall meet all requirements as specified for that certificate in this subclause (and any of its subclauses), 7.3.3 (and any of its subclauses) and in Annex B.

NOTE 9 Annex B provides the certificate profiles.

[V2G20-926] The certificate extensions mentioned in Annex B shall be supported.

NOTE 10 Where necessary, deviations have been specified.

[V2G20-2323] Certificates used in this document shall not contain any extensions other than those specified in Annex B.

NOTE 11 If an extension is mentioned as allowed for a certificate profile in Annex B, regardless whether it is marked as mandatory or optional, a certificate generated to meet that certificate profile is permitted to utilize that extension. If the extension is not mentioned as allowed in the corresponding certificate profile, that extension cannot be present in the corresponding certificate. For example, "CertificatePolicies" extension is marked as optional in most profiles. That means whether the "CertificatePolicies" extension is included is up to the certificate issuer's and certificate requester's discretion. On the other hand, since the "subjectDirectoryAttributes" extension is not specified as a mandatory or optional extension by Annex B, the "subjectDirectoryAttributes" extension cannot be included in any certificate used in this document.

NOTE 12 This ensures that incompatible extensions do not result in unforeseen issues or result in interoperability concerns.

[V2G20-1234]

Each certificate in a certificate chain shall be DER encoded and the size of each certificate in DER encoded form shall be limited to a maximum of 1 600 bytes. Refer to ITU-T X.509 for details of DER encoding.



NOTE 13 A certificate chain is made up of multiple certificates. [V2G20-1234] applies to each certificate in the certificate chain, not the entire certificate chain itself. If a certificate chain is made up of four certificates, that chain will be a maximum of 6 400 bytes in DER format.