
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td colspan="3">ISO 15118-20 certificate profiles</td><td style='text-align: center; word-wrap: break-word;'>eMSP root CA Root</td><td style='text-align: center; word-wrap: break-word;'>eMSP sub-CA1 Sub</td><td style='text-align: center; word-wrap: break-word;'>eMSP sub-CA2 Sub/leaf</td><td style='text-align: center; word-wrap: break-word;'>Contract certificate Leaf</td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>accessLocation</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>x (A URL to a distribution point of current (daily) additional information to the contract. Syntax: An alphanumeric string with a maximum length of 255 characters)</td></tr><tr><td rowspan="3">SignatureAlgorithm</td><td colspan="2">AlgorithmIdentifier</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td colspan="2">algorithm</td><td style='text-align: center; word-wrap: break-word;'>x id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>x id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>x id-Ed448</td><td style='text-align: center; word-wrap: break-word;'>x id-Ed448</td></tr><tr><td colspan="2">parameters</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>-</td></tr><tr><td colspan="3">SignatureValue</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td><td style='text-align: center; word-wrap: break-word;'>(Raw BIT STRING)</td></tr></table>

NOTE IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

#### B.6.3 Common requirements for e-mobility service provider certificate profiles

eMSP sub-CA2 has two purposes:

- it certifies contract certificates;

– it signs tariff information destined for the owners of those contract certificates.

The ID of the provisioning certificate (PCID) is used by the eMSP to identify the contract that belongs to this EV. This is possible because the customer has given the PCID (CN and O, see L.4 and its subclauses for details) to the eMSP when creating the contract. For this purpose, PCID is supposed to be a short string that is unique to the OEM that created the provisioning certificate and to the vehicle which is requesting the contract certificate(s). Furthermore, it is contained in the provisioning certificate.

As mentioned in Table B.9 and Table B.10, it is optional to include the "certificatePolicies" extension in any of the e-Mobility service provider certificates. If the "certificatePolicies" extension is included, it can be marked as non-critical so that the relying party can ignore this extension if it cannot process it. This is done to improve the interoperability.

It should be noted that the EVCC does not validate the contract certificate or any other certificates included in that chain. Usually, the SECC also does not validate the contract certificate or any other certificates included in that chain. Usually, the EVCC provides the contract certificate chain to the eMSP during AuthorizationReq. customarily, it is up to the eMSP to validate the contract certificate chain and ensure that it meets the requirements. In rare instances, the SECC itself may validate the contract certificate chain for authorization purposes.

[V2G20-2588] EMAID shall be created per C.1.

[V2G20-2589] EMAID shall be contained in the subject field of the contract certificate as follows:

- the EMAID itself (see [V2G20-2588]) shall be the value of the Common Name (CN) of the Distinguished Name (DN);

- the name of the eMSP shall be encoded in the field Organization (O) using a unique identifier chosen by the eMSP, to identify this eMSP;

- the X.500 distinguished name in the subject field shall not contain any further values.