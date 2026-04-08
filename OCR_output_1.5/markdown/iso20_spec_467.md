the name of the EVSE Operator shall be encoded in the field Organization (O) using a unique identifier chosen by the EVSE Operator, to identify this EVSE Operator;

- the X.500 distinguished name in the subject field shall not contain any further values.

### B.5 Certificate provisioning service certificate profiles

#### B.5.1 Based on curves as defined by [V2G20-2674]

Table B.7 outlines the certificate installation (provisioning) service certificates based on curves as defined by [V2G20-2674].

<div style="text-align: center;">Table B.7 — Certificate installation (provisioning) service certificates based on curves as defined by [V2G20-2674]</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td colspan="3">ISO 15118-20 certificate profiles</td><td style='text-align: center; word-wrap: break-word;'>CPS sub-CA1 Sub</td><td style='text-align: center; word-wrap: break-word;'>Certificate provisioning service
CPS sub-CA2 Sub</td><td style='text-align: center; word-wrap: break-word;'>CPS leaf certificate
Leaf</td></tr><tr><td rowspan="24">TbsCertificate</td><td colspan="2">Version</td><td style='text-align: center; word-wrap: break-word;'>2
(&quot;2&quot; indicates X.509v3)</td><td style='text-align: center; word-wrap: break-word;'>2
(&quot;2&quot; indicates X.509v3)</td><td style='text-align: center; word-wrap: break-word;'>2
(&quot;2&quot; indicates X.509v3)</td></tr><tr><td colspan="2">SerialNumber</td><td style='text-align: center; word-wrap: break-word;'>(Positive integer)</td><td style='text-align: center; word-wrap: break-word;'>(Positive integer)</td><td style='text-align: center; word-wrap: break-word;'>(Positive integer)</td></tr><tr><td rowspan="3">Signature</td><td style='text-align: center; word-wrap: break-word;'>AlgorithmIdentifier</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>algorithm</td><td style='text-align: center; word-wrap: break-word;'>x
ecdsa-with-SHA512</td><td style='text-align: center; word-wrap: break-word;'>x
ecdsa-with-SHA512</td><td style='text-align: center; word-wrap: break-word;'>x
ecdsa-with-SHA512</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>parameters</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td></tr><tr><td rowspan="5">Issuer</td><td style='text-align: center; word-wrap: break-word;'>Country</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization unit</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Common name</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Domain component</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Validity</td><td style='text-align: center; word-wrap: break-word;'>Validity</td><td style='text-align: center; word-wrap: break-word;'>x
[up to CPS]</td><td style='text-align: center; word-wrap: break-word;'>x
[up to CPS]</td><td style='text-align: center; word-wrap: break-word;'>x
[up to CPS]</td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>notBefore</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>time</td><td style='text-align: center; word-wrap: break-word;'>time</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>notAfter</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>time</td><td style='text-align: center; word-wrap: break-word;'>time</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td><td style='text-align: center; word-wrap: break-word;'>(GeneralizedTime expressed in Greenwich Mean Time (Zulu) with format
YYYYMMDDHHMMSSZ)
[Actual time is CA discretionary]</td></tr><tr><td rowspan="5">Subject</td><td style='text-align: center; word-wrap: break-word;'>Country</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Organization unit</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Common name</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Domain component</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x)</td><td style='text-align: center; word-wrap: break-word;'>(x) &amp; &quot;CPS&quot;</td></tr><tr><td rowspan="4">SubjectPublic KeyInfo</td><td style='text-align: center; word-wrap: break-word;'>AlgorithmIdentifier</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>algorithm</td><td style='text-align: center; word-wrap: break-word;'>x
id-ecPublicKey</td><td style='text-align: center; word-wrap: break-word;'>x
id-ecPublicKey</td><td style='text-align: center; word-wrap: break-word;'>x
id-ecPublicKey</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>parameters</td><td style='text-align: center; word-wrap: break-word;'>x
ECParameters</td><td style='text-align: center; word-wrap: break-word;'>x
ECParameters</td><td style='text-align: center; word-wrap: break-word;'>x
ECParameters</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>namedCurve</td><td style='text-align: center; word-wrap: break-word;'>x
secp521r1</td><td style='text-align: center; word-wrap: break-word;'>x
secp521r1</td><td style='text-align: center; word-wrap: break-word;'>x
secp521r1</td></tr></table>

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.