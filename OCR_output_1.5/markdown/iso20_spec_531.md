When a SECC requests the EVCC to send its vehicle certificate for TLS session setup, the SECC provides the lists of root CA certificate that it supports. The EVCC provides the appropriate vehicle certificate chain that the SECC can validate using the root CA certificates available to it.

In some cases that would mean EVCC providing the vehicle sub-CA2 certificate signed by OEM root CA certificate chain while in others it would provide the vehicle sub-CA2 certificate signed by V2G root CA certificate.

Example 5 as shown in Figure H.9 shows Example 3 certificate structure but with the vehicle certificate chain cross signed by the OEM root CA certificate. This allows the SECC to validate the vehicle certificate using the OEM root CA certificate during TLS session setup. The SECC does not need V2G root CA certificate to validate the vehicle certificate.

In this example of cross signing (Example 5 as shown in Figure H.9), there are 2 separate vehicle sub-CA2 certificates:

— one that is signed by the OEM root CA certificate;

- another that is signed by the V2G root CA certificate chain.

Both of the vehicle sub-CA2 certificates have the same exact public/private key pair.

When an SECC requests the EVCC to send its vehicle certificate for TLS session setup, the SECC provides the list of root CA certificates that it supports. The EVCC provides the appropriate vehicle certificate chain that the SECC can validate using the root CA certificates available to it.

In some cases that would mean EVCC providing the vehicle sub-CA2 certificate signed by OEM root CA certificate while in others it would provide the vehicle sub-CA2 certificate signed by V2G root CA certificate chain.

Similarly, each of those vehicle sub-CA2 certificate may refer to the same exact OCSP server though the OCSP server certificate used in each case will be signed by the appropriate root CA certificate.

It should be noted that there are other examples and methodologies for cross signing. Refer to H.1.5 and its subclauses for further details and examples of cross signing.