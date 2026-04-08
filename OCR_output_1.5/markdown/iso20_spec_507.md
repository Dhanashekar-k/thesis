<EVCCID> = <WMI> <S> <ID Type> <S> <OEM's own unique ID> <S>
<Check Digit>
<WMI> = 3 (ALPHA / DIGIT)
; Three alphanumeric characters for the World
Manufacturer Identifier (WMI) code, as per
ISO 3780
<ID Type> = "V"
; one character "V" indicating that this ID
represents a reference to an EVCCID
<OEM's own unique ID> = Minimum 15 (ALPHA / DIGIT)
Maximum 250 (ALPHA / DIGIT)
; OEM's own unique ID for clearly identifying
a single vehicle made by the manufacturer
<Check Digit> = *1 (ALPHA / DIGIT)
; Used to verify valid EVCCID, see sub-clause
C.6 for its computation
ALPHA = %x41-5A / %x61-7A
; according to IETF RFC 5234 (7-Bit ASCII), case-
insensitive (IETF RFC 7405)
DIGIT = %x30-39
; according to IETF RFC 5234 (7-Bit ASCII)
<S> = *1 ("-" )
; optional separator, but advised not to use it between
IT systems and only for visibility purposes

#### C.5.2 EVCCID semantics

The <EVCCID> shall be interpreted as case-insensitive, i.e. "DE8-V-AA0000453C4D58Y-2" is exactly the same ID as "de8-V-aA0000453C4d58y-2".

The hyphen ("-") is simply used as a separator between the elements <WMI>, <ID Type>, <OEM's own unique ID> and <Check Digit>.

### C.6 Calculation of the check digit

A check digit is a unique value calculated for an alphanumeric character sequence, as used in the EMAID, PCID, SECCID and EVCCID. The <Check Digit> is placed at the last position of the corresponding ID.

The <Check Digit> is calculated on the entire ID (excluding the check digit itself).

[V2G20-2095]

Calculation of the <Check Digit> shall be performed according to the following algorithm:



Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.