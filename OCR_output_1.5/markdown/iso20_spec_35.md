SalesTariff is not a certificate. The black arrow does not depict a certificate signing or certificate derivation/origination. SalesTariff is data that is signed by the eMSP using the private key of the eMSP sub-CA2. Since, in a PnC use case, the EVCC always contains the eMSP sub-CA2 as part of its contract certificate chain, the EVCC always has the associated public key for eMSP sub-CA2 that it can use to verify the signatures on SalesTariff.

Direct certification — The use of sub-CA1 is optional.

d Optional direct certification — If the sub-CA1 is present, it signs the sub-CA2 certificates.

Upon eMSP's discretion the contract certificate chain may originate from V2G root CA certificate. This type of arrow shows when the sub-CA1 is signed by the V2G root CA.

Upon eMSP's discretion the contract certificate chain may originate from V2G root CA certificate. This type of arrow shows when the sub-CA1 is not used and sub-CA2 is signed by the V2G root CA.

## Figure 6 — Contract certificate structure

## [V2G20-2331]

A vehicle certificate shall be generated using a certificate chain that uses either an OEM root CA certificate or a V2G root CA certificate as the trust anchor. Refer to Figure 7 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 7 In case the vehicle certificate is generated using a certificate chain that uses an OEM root CA certificate as the trust anchor, the issuer can consider to cross-sign the vehicle certificate chain (one of the sub-CAs in the vehicle certificate chain or the OEM root CA) by a V2G root CA certificate. This will improve availability of communications as specified in this document and allow the EV to utilize communications as specified in this document on any EVSE that supports the said V2G root CA regardless if the EVSE trusts the specific OEM root CA (i.e. has access to the specific OEM root CA certificate) or not.

NOTE 8 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the OEM's discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use (if any) as the trust anchor for their vehicle certificates.

## [V2G20-2332]

The OCSP signer certificate used to sign the OCSP response for vehicle certificate status shall be generated using a certificate chain that uses either an OEM root CA certificate or a V2G root CA certificate as the trust anchor. Refer to Figure 7 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 9 As in case of vehicle certificate, if the OCSP signer certificate that signs the OCSP response for the vehicle certificates is generated using a certificate chain that uses an OEM root CA as the trust anchor, the issuer can consider to cross-sign the OCSP signer certificate chain (one of the sub-CAs in the OCSP signer certificate chain or the OEM root CA) by a V2G root CA certificate. This will improve availability of communications as specified in this document and allow the EV to utilize communications as specified in this document on any EVSE that supports the said V2G root CA regardless if the EVSE trusts the specific OEM root CA (i.e. has access to the specific OEM root CA certificate) or not.

NOTE 10 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the OEM's discretion (while being aware of the applicable local/regional/state/federal/international rules/regulations/laws) to decide which V2G root CA they use (if any) as the trust anchor for the OCSP signer certificate that signs the OCSP response for their vehicle certificates.

## [V2G20-2333]

An OEM provisioning certificate shall be generated using a certificate chain that uses either an OEM root CA certificate or a V2G root CA certificate as the trust anchor. Refer to Figure 7 for a pictorial representation. Refer to Annex H for further details. Refer to H.1.6 for examples of certificate structure. Refer to Annex B for details of the certificate profile.

NOTE 11 This document does not mandate usage of a particular V2G root CA. In case multiple V2G root CAs are available in a region, it is up to the OEM's discretion (while being aware of the applicable