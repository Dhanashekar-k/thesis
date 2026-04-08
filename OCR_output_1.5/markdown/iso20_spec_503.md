# Annex C (normative)

# Specification of identifiers

### C.1 e-Mobility authentication identifier (EMAID)

#### C.1.1 EMAID syntax

The e-Mobility authentication identifier substitutes the "e-Mobility account identifier" from ISO 15118-2 and the "Contract ID" from ISO 15118-1.

[V2G20-2702] Once a V2G communication session has been authorized using a contract certificate, the EMAID and the contract certificate provided in AuthorizationReq shall not change until the said V2G communication session has been terminated.

[V2G20-2076] The EMAID shall match the requirements as specified in IEC 63119-2.

[V2G20-2126] The maximum length of EMAID shall be 255 characters.

### C.2 Provisioning certificate identifier (PCID)

[V2G20-2078] The OEM shall ensure that the PCID does not change during an ISO 15118-20 communication session.

NOTE 1 Since PCID is included in the OEM provisioning certificate, the only way to change the PCID is to update the OEM provisioning certificate. An OEM can update the OEM provisioning certificate in the EV with a new one. At its discretion, the OEM can choose to use a different PCID in this new OEM provisioning certificate. Changing the certificate while it is in use can result in unforeseen issues.

NOTE 2 Since the contracts are tied to the PCID and PCID is used in CertificateInstallationReq/CertificateInstallationRes to automatically install contract certificates, any change to PCID can be communicated to the EMSP so that automatic contract certificate installation can continue. It is out of the scope of this document to specify how a change to PCID is communicated to the EMSP.

#### C.2.1 PCID syntax

[V2G20-2079] PCID shall be an alphanumeric string with a length of minimum 18 and maximum 255 characters (i.e. A..Z, a..z, 0..9), including a check digit at the end.

NOTE 1 Since the user needs to read the PCID and provide it to the eMSP at the time of signing the contract, a larger PCID can be more error prone for registering with the eMSP.

[V2G20-2077] Characters restricted for usage in WMI according to ISO 3780 shall not be used in PCID.

NOTE 2 This enhances the user readability of the PCID.

[V2G20-2080] The PCID shall match the following structure (the notation corresponds to the augmented Backus-Naur Form (ABNF) as defined in IETF RFC 5234 and IETF RFC 7405):

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.