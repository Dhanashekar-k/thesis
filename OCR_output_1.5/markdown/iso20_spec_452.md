The OID repository [99] also refers to id-tpmStorageKey as tpmStorageKey(4) (see NOTE 1 in this subclause providing the OID value for id-tpmStorageKey).

The OID repository [99] also refers to id-tpmPolicyDigest as tpmPolicyDigest(5) (see NOTE 1 in this subclause providing the OID value for id-tpmPolicyDigest).

The OID repository  $ [99] $ also refers to id-crossCertIndication as crossCertIndication(6) (see NOTE 1 in this subclause providing the OID value for id-crossCertIndication).

GeneralizedTime in Greenwich Mean Time (GMT) is utilized for certificate validity purposes as some of the certificates can have expiration date beyond year 2049 as, per ITU-T X.509 [and IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399)], Coordinated Universal Time (UTC) based time can only be used in certificates that expire before year 2050.

It should be noted that although the certificate validity of each certificate type will be as per the definition in this annex, the certificate validity remaining at the time of V2G entity production or deployment may be less than the requirements as specified in this annex. This is because the certificate may have been generated long before the V2G entity was produced and/or deployed.

Furthermore, the certificate validity is not directly related to the date of issuance of a certificate, but is rather tied to "notBefore" and "notAfter" fields of the certificate.

For example, if a V2G root CA certificate has a "notBefore" field of 20100301180000Z (March 1 18:00:00 2010 GMT) and a "notAfter" field of 20350301175959Z (March 1 17:59:59 2035 GMT), this results in a validity of 25 years. If a vehicle manufactured in March 2020 uses that V2G root CA certificate, that root certificate will only have 15 more years of validity left before the certificate expires.

### B.2 General

This subclause applies to all certificate types and profiles.

[V2G20-2685]

Any extension or field/parameter/attribute/data type (or sub-field/sub-parameter/sub-attribute/sub-data type or sub-sub-field/sub-sub-parameter/sub-sub-attribute/sub-sub-data type or etc.) not defined in the certificate profiles defined by this document shall not be included in any certificate conforming to this document.



Per ITU-T X.509 and IETF RFC 5280 as updated by updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), some fields/parameters/attributes/data types (or sub-fields/sub-parameters/sub-attributes/sub-data types or sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.) can take multiple sub-fields/sub-parameters/sub-attributes/sub-data types (or sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.). Certificate profiles defined by this annex limit the number of sub-fields/sub-parameters/sub-attributes/sub-data types (or sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.) to as defined by this document.

Per ITU-T X.509 and IETF RFC 5280 (as updated by updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399), some fields/parameters/attributes/data types (or sub-fields/sub-parameters/sub-attributes/sub-data types or sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.) can take a sequence of sub-fields/sub-parameters/sub-attributes/sub-data types (or a sequence of sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.). Certificate profiles defined by this annex limit the number of sequences of sub-fields/sub-parameters/sub-attributes/sub-data types (or sub-sub-fields/sub-sub-parameters/sub-sub-attributes/sub-sub-data types or etc.) to as defined by this document.