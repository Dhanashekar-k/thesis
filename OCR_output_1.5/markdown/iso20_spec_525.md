It adds burden on the entity that cross signs other entities certificates to take an action in case the other entity's certificate is compromised. In the above example, when the organization B's certificate(s) are compromised, organization A will need to take an action to mark the associated cross certificate as revoked to help ensure that the relying parties do not falsely assume that organization B's certificate(s) are still valid since they are cross signed by organization A whose certificates are not compromised and are still valid.

– Use of cross certification may require more resources on the device such as memory for storing cross-certificates, and take longer for the verification of certificate chains with cross-certificates. For example, if an OEM wants to support cross-certification for vehicle certificate validation, their EV stores necessary cross certificates, each signed by different V2G root CA within its storage.

PKI operators are recommended to examine all these issues and weigh against advantages before employing cross-certification.

##### H.1.5.5 Risk mitigation of cross certification

One way to mitigate risks of cross certification is to ensure that the entities that cross sign each other's CA(s) belong to same governance structure. An example of governance structure for web browsers is CA/B Forum $ ^{5} $. This forum has defined a strict set of requirements that need to be followed to consider a PKI to be under the governance standards as specified by CA/B.

Since any CA that provides CA certificates under CA/B governance standards follows the same requirements, it is likely that these CAs have similar level of security. As such cross signing root CA certificates under these conditions may be acceptable if the certificate policies, certification practice statements, etc. for the 2 root CAs are compatible.

It should be noted that this helps reduce the risks but it does not completely eliminate the risks associated with cross-signing.

#### H.1.6 Examples of the resulting certificate structure

As mentioned in 7.3.2.1, this document does not mandate any particular certificate structure. It simply sets some minimum constraints that enable the PKI necessary for TLS, PnC and other features described and/or specified by this document.

Figure H.5, Figure H.6, Figure H.7, Figure H.8, Figure H.9 and Figure H.10 provide a few visual examples of the possible certificate structure.

CSOs/eMSPs/OEMs are allowed to independently choose any certificate structure between (and including) Figure H.5 and Figure H.10. This means that OEM may choose to skip OEM sub-CA1 without any negative/interoperability issues with any of the other entities relying on the OEM certificates.

The OEM provisioning certificates are independent from the PKI of the secondary actors below the (global) root certificates (V2G root CA certificate). The root certificate of an OEM provisioning certificate is created by the OEM itself. Therefore, there is no need to have a (longer) certificate chain. (For an explanation of the usage of the OEM root CA certificate and the OEM provisioning certificate refer to H.2). It is, however, allowed to reuse a V2G root as an eMSP root CA certificate or an OEM root CA certificate or to cross sign one of the sub-CAs in contract certificate chain or OEM provisioning certificate chain.

All certificate chains have a maximum length of 3; i.e. including the root certificate 4 certificates are involved. This does not include the cross certificate which will increase the length by 1.