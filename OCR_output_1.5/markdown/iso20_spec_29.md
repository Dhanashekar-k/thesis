NOTE 14 As mentioned in Annex B, there are many mandatory and optional parameters in a certificate. Some parameters have well defined fixed lengths while others are variable length parameters. The certificate issuer can experiment with different optional parameters, different parameter data for variable length parameters, etc. to stay within the bounds of [V2G20-1234]. For example, if the OCSP responder address is too long, the certificate issuer can use methodologies to shorten the address to keep the certificate length within the bounds of [V2G20-1234].

[V2G20-1004] Certificates shall be issued and signed by the CA within the validity of its own certificate.

[V2G20-911] If only one sub-CA layer is used, i.e. a sub-CA signed by a root CA directly signs leaf certificates, the profile of sub-CA2 shall apply for that sub-CA.

[V2G20-1003] All certificate chains (except where a cross certificate is used) shall have a maximum length of 3.

NOTE 15 The certificate chain includes the leaf certificate. The certificate chain does not include the root certificate.

NOTE 16 This means, at most two sub-CA levels can be used.

[V2G20-1005] All certificate chains, including a cross certificate, shall have a maximum length of 4.

NOTE 17 The certificate chain includes the leaf certificate and the cross certificate. The certificate chain does not include the root certificate.

NOTE 18 A cross certificate adds one more level.

[V2G20-1002] When cross-certification is used, the certificate chain sent shall include the cross-certificate.

NOTE 19 The profile of a cross certificate differs from that of other CA certificates by the validity period and the use of Subject Information Access extension. See Annex B for further details.

[V2G20-1853] A cross-certificate shall not be valid beyond the validity period of the cross-certified CA's certificate and cross-certifying CA's certificate.

[V2G20-1001] All certificate validations shall be carried out in conformance with IETF RFC 5280 and ITU-T X.509. During certificate validation, each certificate shall be checked for conformance with the appropriate profile in Annex B. All requirements from Annex B shall be met for the appropriate certificate profile. The EVCC and the SECC shall cache certificate validation results during one service session.

NOTE 20 The certificate validation includes checking the following.

a) The content of a leaf certificate has not been altered after issue. This means it is possible to check and confirm the signature up to the trust anchor level and thus the integrity of the signed content.

b) The signature up to the trust anchor level is not compromised (none of the certificates have been revoked). Certificate revocation is checked via the OCSP response (or CRL, if allowed for that particular certificate) as detailed in 7.7.3.1 and 7.7.3.3.

c) The validity period of each certificate in the chain up to the trust anchor has not yet elapsed.

d) Each certificate in the certificate chain matches the appropriate certificate profile as defined in Annex B. This includes checking the following:

- the key length of each certificate in the certificate chain matches the key length specified by that certificate’s profile in Annex B;

- every critical KeyUsage attribute is set to the appropriate value (i.e. 0 or 1) as defined for that certificate's profile in Annex B;

## 24 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.