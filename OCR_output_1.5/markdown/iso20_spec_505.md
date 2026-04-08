[V2G20-2127] SECCID shall be an alphanumeric string with a length of minimum 39 and maximum 255 characters (i.e. A..Z, a..z, 0..9), including a check digit at the end.

[V2G20-2128] Characters restricted for usage in WMI by ISO 3780 shall not be used in SECCID.

NOTE This enhances the user readability of the SECCID.

[V2G20-2083] The SECCID shall match the following structure (the notation corresponds to the augmented Backus-Naur Form (ABNF) as defined in IETF RFC 5234 and IETF RFC 7405):

<SECCID> = <Country Code> <S> <EVSE Operator ID> <S> <ID Type>
<S> <ControllerID> <S> <Check Digit>

<Country Code> = 2 ALPHA

; two character country code according to ISO 3166-1 (Alpha-2-Code)

<EVSE Operator ID> = 3 (ALPHA / DIGIT)

; three alphanumeric characters, referring to the EVSE Operator

<ID Type> = "S"

; one character "S" indicating that this ID represents a reference to a "Supply Equipment"

<ControllerID> = Minimum 32 (ALPHA / DIGIT)
Maximum 248 (ALPHA / DIGIT)

; Alphanumeric characters referring to the specific communication controller

<Check Digit> = *1 (ALPHA / DIGIT)

; Used to verify valid SECCID, see sub-clause C.6 for its computation

ALPHA = %x41-5A / %x61-7A

; according to IETF RFC 5234 (7-Bit ASCII), case-insensitive (IETF RFC 7405)

DIGIT = %x30-39

; according to IETF RFC 5234 (7-Bit ASCII)

<S> = *1 ("-" )

; optional separator, but advised not to use it between IT systems and only for visibility purposes

#### C.3.2 SECCID semantics

© ISO 2022 – All rights reserved
Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program.
Copying not permitted. ©ISO. All rights reserved.