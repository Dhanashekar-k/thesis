[V2G20-2084] The <SECCID> shall be interpreted as case-insensitive, i.e. "DE-8AA-S-00003C4D557878675645330967543476-2" is exactly the same ID as "de-8aA-S-00003C4d557878675645330967543476-2".

The hyphen ("-") is simply used as a separator between the elements <Country Code>, <EVSE Operator ID>, <ID Type>, <ControllerID> and <Check Digit>.

Country codes as defined in ISO 3166-1 typically map to one country. However, ISO 3166-1 does not provide well defined "user-assigned" country codes: AA, QM to QZ, XA to XZ, and ZZ.

[V2G20-2085] Within 15118-20 the following country codes have a fixed meaning:

- ZZ-0-... = Any <SECCID> starting with this prefix is reserved and shall be considered as zero or as "undefined".

### C.4 Electric vehicle supply equipment ID (EVSEID)

[V2G20-2086] The CSO shall ensure that the EVSEID does not change during an ISO 15118-20 communication session.

#### C.4.1 EVSEID syntax

[V2G20-2087] The EVSEID shall match the requirements as specified in IEC 63119-2.

[V2G20-2088] The maximum length of EVSEID shall be 255 characters.

### C.5 Electric vehicle communication controller ID (EVCCID)

[V2G20-2092] The OEM shall ensure that the EVCCID does not change during an ISO 15118-20 communication session.

NOTE Since EVCCID is included in the vehicle certificate, the only way to change the EVCCID is to update the vehicle certificate. An OEM could need to update the vehicle certificate in the EV with a new one. At its discretion, the OEM can choose to use a different EVCCID in this new vehicle certificate. Changing the certificate while it is in use can result in unforeseen issues.

#### C.5.1 EVCCID syntax

[V2G20-2089] EVCCID shall be an alphanumeric string with a length of minimum 20 and maximum 255 characters (i.e. A..Z, a..z, 0..9), including a check digit at the end.

[V2G20-2090] Characters restricted for usage in WMI by ISO 3780 shall not be used in EVCCID.

NOTE This enhances the user readability of the EVCCID.

[V2G20-2093] The EVCCID shall match the following structure (the notation corresponds to the augmented Backus-Naur Form (ABNF) as defined in IETF RFC 5234 and IETF RFC 7405):