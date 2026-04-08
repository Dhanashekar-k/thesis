If the optional field/parameter/attribute/data type is included in a certificate, then all sub-fields/sub-parameters/sub-attributes/sub-data types (within the optional field/parameter/attribute/data type) marked as mandatory/required in the certificate profile shall also be included in the certificate conforming to the particular certificate profile.

[V2G20-2693] If the optional field/parameter/attribute/data type is included in a certificate, then any sub-fields/sub-parameters/sub-attributes/sub-data types (within the optional field/parameter/attribute/data type) marked as optional in the certificate profile may or may not be included, at the CA's discretion (unless specified otherwise by the requirements in this document), in the certificate conforming to the particular certificate profile.

If a certificate requester needs any of these optional sub-fields/sub-parameters/sub-attributes/sub-data types to be included, the requester will need to work with its CA to include those sub-fields/sub-parameters/sub-attributes/sub-data types in the certificate chain. It is out of the scope of this document to define the methodologies for the certificate requester to indicate to the CA whether a particular optional sub-field/sub-parameter/sub-attribute/sub-data type should be included or not.

A sub-field/sub-parameter/sub-attribute/sub-data type in the certificate could contain sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types. These sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types are indented within the sub-field/sub-parameter/sub-attribute/sub-data type in the certificate profiles defined below.

Above requirements and methodology also extends to any sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types contained in a sub-field/sub-parameter/sub-attribute/sub-data type.

Although some fields/parameters/attributes/data types are marked as optional, requirements in this document may specify that CA uses them or one of them under certain conditions. If that is the case, the requirements will clearly identify which optional fields/parameters/attributes/data types are included by the CA. All relying parties should be cognizant of these requirements when validating the certificate against a given certificate profile.

#### B.2.2 Critical versus non-critical

Per ITU-T X.509 and IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), extensions in a x.509v3 certificate can be indicated as critical or non-critical. The designation of critical or non-critical only applies to extensions. Other fields/parameters/attributes/data types cannot be marked as critical or non-critical.

The certificate profiles defined below mark some extensions as critical while other extensions in that same certificate profile are marked as non-critical. Table B.1 provides the definition of critical and non-critical parameters.

If a relying party can interpret/process an extension then it should be able to interpret/process all subfields/sub-parameters/sub-attributes/sub-data types within that extension. Similarly, if a relying party cannot interpret/process an extension then it should not be able to interpret/process any sub-field/sub-parameter/sub-attribute/sub-data type within that extension.

As such only the extensions are required to be indicated as critical/non-critical within a certificate. All sub-fields/sub-parameters/sub-attributes/sub-data types within that extension are assumed to inherit the critical/non-critical designation.

Combining optional vs mandatory and critical vs non-critical designation of the extensions lead to following possible scenarios in Table B.2: