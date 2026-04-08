Key
1 direct certification
2 cross certification
3 OCSP response
4 certificate

SalesTariff is not a certificate. The black arrow does not depict a certificate signing or certificate derivation/origination. SalesTariff is data that is signed by the eMSP using the private key of the eMSP sub-CA2. This is unusual. Mostly data is signed using keys from a leaf certificate, not a CA certificate. To reduced the need for another leaf certificate in the vehicle, SalesTariff is signed by the eMSP using the private key of the eMSP sub-CA2 certificate. Since, in a PnC use case, the EVCC always contains the eMSP sub-CA2 as part of its contract certificate chain, the EVCC always has the associated public key for eMSP sub-CA2 that it can use to verify the signatures on SalesTariff that were applied by the said eMSP. SalesTariff is not signed in EIM.

### Figure H.10 — Example of an alternative (simplified) certificate structure

In the example of cross signing shown in Figure H.10, there are 2 separate vehicle sub-CA2 certificates; one is signed by the OEM root CA certificate while the other is signed by the V2G root CA certificate. Both of them have the same exact public/private key pair.

When a SECC requests the EVCC to send its vehicle certificate for TLS session setup, the SECC provides the lists of root CA certificate that it supports. The EVCC provides the appropriate vehicle certificate chain that the SECC can validate using the root CA certificates available to it.

In some cases that would mean EVCC providing the vehicle sub-CA2 certificate signed by OEM root CA certificate while in others it would provide the vehicle sub-CA2 certificate signed by V2G root CA certificate.

As mentioned earlier, the certificate structures depicted here are simply examples. All entities are allowed to choose any structure that works for their implementations. Any certificate structure chosen by the various entities should abide by the constraints set up by this document. For example, a CPS certificate is not allowed to be signed by the OEM root CA certificate.

H.2.1 provides an example of simplified certificate management in private environments.

### H.2 Simplified certificate management in private environment

#### H.2.1 Overview

The main use cases of this document imply that the EVSE is public. However, the EVSE can also be private (PE EVSE).

Decentralizing the charging infrastructure and operating it in a PE is an essential element of this document. Whether the implementation of this document is also worthwhile in a PE depends on whether the production and operating costs are lower than those for public are.

In contrast to public infrastructure, it is assumed that the charging infrastructure is operated in a location that is not freely accessible and is therefore private. A PE could include a private plot of land, a private garage, a private parking space or a privately operated multi-story car park. A PE EVSE owner can be a natural person or a smaller company that does not act publicly. As a rule, the PE EVSE is not freely accessible in a PE, so that access to the private infrastructure is only granted to a restricted group of users who have been authorized by the PE EVSE owner. Authorized in this context means that the PE EVSE owner grants the EVs the right to charge by giving access to the PE EVSE and, if necessary, giving the user the option of preparing their EV for charging at this PE EVSE.