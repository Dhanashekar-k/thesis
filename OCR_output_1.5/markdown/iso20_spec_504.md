<PCID> = <WMI> <S> <ID Type> <S> <OEM's own unique ID> <S>
<Check Digit>
<WMI> = 3 (ALPHA / DIGIT)
; Three alphanumeric characters for the World
Manufacturer Identifier (WMI) code, as per ISO
3780
<ID Type> = "P"
; one character "P" indicating that this ID
represents a reference to a PCID
<OEM's own unique ID> = Minimum 13 (ALPHA / DIGIT)
Maximum 250 (ALPHA / DIGIT)
; OEM's own unique ID for clearly identifying
a single vehicle made by the manufacturer
<Check Digit> = *1 (ALPHA / DIGIT)
; Used to verify valid PCID, see sub-clause
C.6 for its computation
ALPHA = %x41-5A / %x61-7A
; according to IETF RFC 5234 (7-Bit ASCII), case-
insensitive (IETF RFC 7405)
DIGIT = %x30-39
; according to IETF RFC 5234 (7-Bit ASCII)
<S> = *1 ("-" )
; optional separator, but advised not to use it between
IT systems and only for visibility purposes

#### C.2.2 PCID semantics

## [V2G20-2081]

The <PCID> shall be interpreted as case-insensitive, i.e. "DE8-P-AA00003C4D58Y-2" is exactly the same ID as "de8-P-aA00003C4d58y-2".

The hyphen ("-") is simply used as a separator between the elements <WMI>, <ID Type>, <OEM's own unique ID> and <Check Digit>.

### C.3 Supply equipment communications controller identifier (SECCID)

[V2G20-2082]

The CSO/SA operating the SECC shall ensure that the SECCID does not change during an ISO 15118-20 communication session.



NOTE Since SECCID is included in the SECC certificate, the only way to change the SECCID is to update the SECC certificate. The CSO/SA operating the SECC can update the SECC certificate in the SECC with a new one. At its discretion, the CSO/SA operating the SECC can choose to use a different SECCID in this new SECC certificate. Changing the certificate while it is in use can result in unforeseen issues.

#### C.3.1 SECCID syntax