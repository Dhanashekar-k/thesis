4 OCSP response

5 certificate

6 optional certificate

SalesTariff is not a certificate. The black arrow does not depict a certificate signing or certificate derivation/origination. SalesTariff is data that is signed by the eMSP using the private key of the eMSP sub-CA2. This is unusual. Mostly data is signed using keys from a leaf certificate, not a CA certificate. To reduced the need for another leaf certificate in the vehicle, SalesTariff is signed by the eMSP using the private key of the eMSP sub-CA2 certificate. Since, in a PnC use case, the EVCC always contains the eMSP sub-CA2 as part of its contract certificate chain, the EVCC always has the associated public key for eMSP sub-CA2 that it can use to verify the signatures on SalesTariff that were applied by the said eMSP. SalesTariff is not signed in EIM.

### Figure H.6 — Example 2 of a certificate structure with cross signing

Example 2 in Figure H.6 shows two separate vehicle sub-CA1 certificates; one is signed by the OEM root CA certificate while the other is signed by the V2G root CA certificate. Both of them have the same exact public/private key pair.

When a SECC requests the EVCC to send its vehicle certificate for TLS session setup, the SECC provides the lists of root CA certificate that it supports. The EVCC provides the appropriate vehicle certificate chain that the SECC can validate using the root CA certificates available to it.

In some cases that would mean EVCC providing the vehicle sub-CA1 certificate signed by OEM root CA certificate while in others it would provide the vehicle sub-CA1 certificate signed by V2G root CA certificate.

Example 3 as shown in Figure H.7 shows another example certificate structure. In this example, the SECC certificate chain originates from the V2G root CA certificate. Additionally, the OEM utilizes V2G root CA certificate chain to generate the vehicle certificate chain. All other main actors like the eMSP and the OEM utilize their own root certificates for the leaf certificates like the contract certificate, OEM provisioning certificate, etc. In this example, none of the certificates are cross signed. This means that the SECC needs the V2G root CA certificate to validate the vehicle certificate during TLS session setup.

It is worth noting that normally the OEM would not prefer to utilize the certificate chains originating from 2 different root CA certificates. Usually either the OEM would use OEM root CA certificate for signing both the vehicle certificate chain and the OEM provisioning certificate chain or the OEM will use V2G root CA certificate to sign both the vehicle certificate chain and the OEM provisioning certificate chain.

Nevertheless, Example 3 shows that these kinds of certificate structures are possible and not prohibited by this document.