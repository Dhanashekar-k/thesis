local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use (if any) as the trust anchor for their OEM provisioning certificates.

[V2G20-2334]

The OCSP signer certificate used to sign the OCSP response for OEM provisioning certificate status shall be generated using a certificate chain that uses either an OEM root CA certificate or a V2G root CA certificate as the trust anchor. Refer to Figure 7 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of certificate structure. Refer to Annex B for details of the certificate profile.



NOTE 12 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the OEM's discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use (if any) as the trust anchor for the OCSP signer certificate that signs the OCSP response for their OEM provisioning certificates.