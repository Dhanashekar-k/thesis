For the application of XMLDisig, any element which should be signed is addressable. In this document, this is achieved by a URI referencing the ID attribute of such an element. Therefore, any message element that is signed carries an ID attribute. If a specific element is to be signed in all use cases, the ID attribute is marked mandatory in the XSD. Otherwise, if it is signed in only some use cases, the ID attribute is marked optional and can be omitted when not needed.

NOTE 3 Presence of an ID attribute does not necessarily indicate that a signature is used, i.e. if no signature is used, an ID can be present nevertheless.

NOTE 4 Refer IETF RFC 3986 as updated by IETF RFC 6874 and IETF RFC 7320 for details of URI.

###### 7.9.2.4.3 Application of security mechanisms to XML message

In general, two pairs of security mechanisms are supported.

– Authenticity and integrity: signature generation → signature verification; XML based signature is applied. The entity creates the XML message and signs certain or all fields of an XML message. The receiver verifies the signature.

– Confidentiality: encryption → secretion; encryption is applied. The entity creates the message and encrypts a single binary field of the XML message. The receiver decrypts that binary field.

Table 17 and Table 18 provide an overview of the applied security mechanisms.

The public/private key pair associated with the "subjectPublicKeyInfo" parameter of the appropriate certificate is used for the purposes of XML signatures.

<div style="text-align: center;">Table 17 — Overview of applied XML based signatures</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>XML message</td><td style='text-align: center; word-wrap: break-word;'>Protected fields</td><td style='text-align: center; word-wrap: break-word;'>Signing entity (sender)</td><td style='text-align: center; word-wrap: break-word;'>Verifying entity (receiver)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>AuthorizationReq</td><td style='text-align: center; word-wrap: break-word;'>PnC_AReqIdentificationMode</td><td style='text-align: center; word-wrap: break-word;'>EVCC; signed with private key associated with the contract certificate provided within PnC_AReqIdentificationMode</td><td style='text-align: center; word-wrap: break-word;'>SECC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CertificateInstallationReq</td><td style='text-align: center; word-wrap: break-word;'>message body/all fields</td><td style='text-align: center; word-wrap: break-word;'>EVCC; signed with private key associated with OEM provision certificate (transmitted in message body element)</td><td style='text-align: center; word-wrap: break-word;'>secondary actor</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CertificateInstallationRes</td><td style='text-align: center; word-wrap: break-word;'>SignedInstallationData</td><td style='text-align: center; word-wrap: break-word;'>secondary actor; signed with the private key associated with the leaf certificate of the certificate provisioning service</td><td style='text-align: center; word-wrap: break-word;'>EVCC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>MeteringConfirmationReq</td><td style='text-align: center; word-wrap: break-word;'>message body / all fields</td><td style='text-align: center; word-wrap: break-word;'>EVCC; signed with private key associated with the contract certificate (certificate is transmitted in AuthorizationReq message)</td><td style='text-align: center; word-wrap: break-word;'>SECC</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ChargeParameterDiscoveryRes</td><td style='text-align: center; word-wrap: break-word;'>AbsolutePriceSchedule (if present, signature required for PnC)</td><td style='text-align: center; word-wrap: break-word;'>secondary actor; signed with the private key associated with the eMSP sub-CA2 certificate</td><td style='text-align: center; word-wrap: break-word;'>EVCC</td></tr></table>

<div style="text-align: center;">Table 18 — Overview of applied encryption</div>


## 94 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.