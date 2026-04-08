## [V2G20-2326]

An SECC certificate shall be generated using a certificate chain that uses a V2G root CA certificate as the trust anchor. Refer to Figure 5 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of a certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 2 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the CSO's discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use as the trust anchor for the SECC certificate in their SECCs.

## [V2G20-2327]

An OCSP signer certificate used to sign the OCSP response for SECC certificate status shall be generated using a certificate chain that uses a V2G root CA certificate as the trust anchor. Refer to Figure 5 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of a certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 3 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the CSO's discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use as the trust anchor for the OCSP signer certificate that signs the OCSP response for their SECC certificates.

## [V2G20-2328]

A CPS leaf certificate shall be generated using a certificate chain that uses a V2G root CA certificate as the trust anchor. Refer to Figure 5 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of a certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 4 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the CPS' discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use as the trust anchor for their CPS leaf certificate.