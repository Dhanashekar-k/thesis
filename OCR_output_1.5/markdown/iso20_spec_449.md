# Annex B (normative)

## Certificate profiles

### B.1 Overview

Certificate profiles are presented in tables, divided into several thematic clusters each containing profiles for specific certificate types. Certificate profiles are based on ITU-T X.509 and IETF RFC 5280 (as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399).

Tables B.x (like Table B.3, Table B.5, Table B.7, Table B.9, Table B.11, Table B.13, Table B.15 or Table B.17) provide certificate profiles for certificates based on the curve as defined by [V2G20-2674].

Tables B.y (like Table B.4, Table B.6, Table B.8, Table B.10, Table B.12, Table B.14, Table B.16 or Table B.18) provide certificate profiles for certificates based on the curve as defined by [V2G20-2319].

A cell's content in the certificate profiles in Table B.1 have the following meaning.

<div style="text-align: center;">Table B.1 — Certificate profile cell content meaning</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Cell content</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>Required/mandatory - Issuing CA ensures that this extension is present. - Certificate validating entity ensures that this extension is present.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>Optional - It is up to the discretion of the issuing CA and/or certificate requester to either include or omit this extension. - Certificate validating entity ignores the absence of this extension.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>Should not be present - Issuing CA ensures that this extension is not present. - Certificate validating entity ensures that this extension is not present.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>c</td><td style='text-align: center; word-wrap: break-word;'>This extension is critical see IETF RFC 5280 - If this extension is present, the certificate validating entity processes it. If an implementation recognizes that a &quot;critical&quot; extension is present, but the implementation cannot interpret the extension, the implementation rejects the certificate. Quote from IETF RFC 5280: &quot;A certificate-using system rejects the certificate if it encounters a critical extension it does not recognize or a critical extension that contains information that it cannot process.&quot; NOTE IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>nc</td><td style='text-align: center; word-wrap: break-word;'>This extension is non-critical, see IETF RFC 5280 - If this extension is present, the certificate validating entity may ignore it if the entity is unable to process the extension. If an implementation recognizes that a &quot;non-critical&quot; extension is present, but the implementation cannot interpret the extension, the extension can be ignored. Quote from IETF RFC 5280: &quot;A non-critical extension MAY be ignored if it is not recognized, but is processed if it is recognized.&quot; NOTE IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>()</td><td style='text-align: center; word-wrap: break-word;'>For &quot;(x)&quot;: - See above For cases other than &quot;(x)&quot;: Details of the parameter</td></tr></table>

## 444 

© ISO 2022 – All rights reserved

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.