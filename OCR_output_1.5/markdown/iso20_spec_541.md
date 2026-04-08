maintain other trust anchors used in PE. This will remove some of the disadvantages/challenges associated with each of these challenges.

When possible EVs could use their knowledge of a GPS coordinate to implement plausibility checks based on "geolocation fencing" algorithms to check if a presented PE private root CA certificates is plausible in a given location and ask for confirmation from the driver in uncertain cases.

##### H.2.2.4 Charging in a private environment

From the perspective of the EV, charging in a private environment is exactly the same as in a non-private environment. This is important, in case that the EV does not know where it is currently located. In a private environment, the private SECC transmits its PE certificate chain to the EVCC. The EVCC checks (as always) whether the certificate is still valid and whether it is derived from one of the root certificates stored in the EV. Thereby, V2G root CA certificates as well as PE private root CA certificates are recognized.

##### H.2.2.5 Compromised certificate of a private SECC

A PE certificate of a private SECC can get compromised; e.g. when it was stolen. Each EVCC that belongs to this private environment (i.e. possessing the corresponding PE private root CA certificate) can be attacked with this stolen leaf certificate by a man in the middle attack (all EVs that do not belong to this private environment are still safe). This attack is possible at each EVSE, even outside of the private environment. Therefore, in that case, it is the responsibility of the owner of the private environment to disable the PE private root CA certificate in all EVs of that particular private environment. To reinstate the charging functionality, the operator will then deploy a completely new certificate structure starting from a new PE private root CA certificate.

As the description of the process shows, two aspects are crucial in this scenario:

– the PE certificates in the private SECCs are either secured safely or their theft is detected reliably;

AND

– the effort that results in case of a theft from exchanging the PE private root CA certificates of all EVCCs and all private SECCs of this environment is acceptable.

Therefore, the described solution is only suitable for closed and small environments; i.e. a small number of EVs and a small number of EVSEs in a private environment or an environment of a small organizational unit.

#### H.2.3 Security considerations of using private environment credentials

Since the whole idea behind PE is to simplify the certificate chain with increased validity period, it sacrifices some of the security offered by the certificate chains in the public certificates like the certificates arising from V2G root CA. CAs acting as V2G root CAs or CAs operating below the V2G root CAs follow more stringent security and governance structure for their certificates.

For example, a CA operating in public environment will ensure the identity of the entity to which the certificate is being issued while the CA operating in private environment is not required to do so. Similarly, the CA operating in public environment will ensure that the entity to whom the certificate is being issued follows best practices to keep the private keys secure while the CA operating in private environment is not required to do so.

End-entities in public environment are required to protect the leaf certificate private key against loss/theft of the said private key. End entities in private environment are not required to do so.