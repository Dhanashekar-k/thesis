[V2G20-2686] The relying party shall reject any certificate that contains an extension or field/parameter/attribute/data type not defined in the certificate profile for that certificate type in this document.

#### B.2.1 Mandatory versus optional

The certificate profiles defined below mark some fields/parameters/attributes/data types as optional while other fields/parameters/attributes/data types in that certificate profile are marked as mandatory/required to be supported.

[V2G20-2687] All mandatory/required fields/parameters/attributes/data types shall be included in a certificate conforming to a particular certificate profile.

[V2G20-2688] Any optional fields/parameters/attributes/data types may or may not be included in the certificate at the CA's discretion, unless specified otherwise by the requirements in this document.

If a certificate requester needs any of these optional fields/parameters/attributes/data types to be included, the requester will need to work with its CA to include those fields/parameters/attributes/data types in the certificate chain. It is out of the scope of this document to define the methodologies for the certificate requester to indicate to the CA whether a particular optional field/parameter/attribute/data type should be included or not.

A field/parameter/attribute/data type in the certificate could contain sub-fields/sub-parameters/sub-attributes/sub-data types. These sub-fields/sub-parameters/sub-attributes/sub-data types are indented within the field/parameter/attribute/data type in the certificate profiles defined below.

[9] All mandatory/required sub-fields/sub-parameters/sub-attributes/sub-data types shall be included in a mandatory/required field/parameter/attribute/data type within a certificate conforming to a particular certificate profile.

90] Unless specified otherwise by the requirements in this document, at the CA's discretion, any optional sub-fields/sub-parameters/sub-attributes/sub-data types may or may not be included in a mandatory/required field/parameter/attribute/data type within a certificate conforming to a particular certificate profile.

If a certificate requester needs any of these optional sub-fields/sub-parameters/sub-attributes/sub-data types to be included, the requester will need to work with its CA to include those sub-fields/sub-parameters/sub-attributes/sub-data types in the certificate chain. It is out of the scope of this document to define the methodologies for the certificate requester to indicate to the CA whether a particular optional sub-field/sub-parameter/sub-attribute/sub-data type should be included or not.

Some of the optional fields/parameters/attributes/data types contain sub-fields/sub-parameters/sub-attributes/sub-data types which may then be individually marked as mandatory/required to be supported in that certificate profile while other sub-fields/sub-parameters/sub-attributes/sub-data types contained within that field/parameter/attribute/data type may be marked as optional to be supported in that certificate profile.

## [V2G20-2691]

If the optional field/parameter/attribute/data type is omitted, then all subfields/sub-parameters/sub-attributes/sub-data types included in that field/parameter/attribute/data type shall also be omitted from the certificate conforming to that particular certificate profile. This shall be done whether a particular sub-field/sub-parameter/sub-attribute/sub-data type is indicated as mandatory or optional in the certificate profile.

## 448 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.