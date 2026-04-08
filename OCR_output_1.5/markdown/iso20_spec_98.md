[V2G20-766] Each message that needs the XML signature framework shall use the value "http://www.w3.org/TR/canonical-exi/" as algorithm attribute within the transform element.

[V2G20-767] The maximum number of Transforms is limited to one (1) (i.e. per referenced element where a signature is to be transmitted for, just one single Transform algorithm can be indicated).

[V2G20-1449] The parts which are signed in the XML-based messages shall be encoded as EXI schema-informed fragment. To encode the signature header, the XML signature schema shall be used as entry point, instead of the schema defined by this document.

[V2G20-2473] Each message, that needs the XML signature framework shall use the value "http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha512" as algorithm attribute within the SignatureMethod element, if the algorithm defined in [V2G20-2674] shall be used according to the configuration in [V2G20-2320]. The certificate whose private key is used for signing the message shall be based on the algorithm defined in [V2G20-2674].

[V2G20-2474] Each message, that needs the XML signature framework shall use the value "urn:iso:std:iso:15118:-20:Security:xmldsig#Ed448" as Algorithm attribute within the SignatureMethod element, if the algorithm defined in [V2G20-2319] shall be used according to the configuration in [V2G20-2320]. The certificate whose private key is used for signing the message shall be based on the algorithm defined in [V2G20-2319].

[V2G20-2475] Each message, that needs the XML signature framework shall use the value "http://www.w3.org/2001/04/xmlenc#sha512" as algorithm attribute within the DigestMethod element, if the algorithm defined in [V2G20-2674] shall be used according to the configuration in [V2G20-2320].

[V2G20-2476] Each message, that needs the XML signature framework shall use the value "urn:iso:std:iso:15118:-20:Security:xmlenc#SHAKE256" as algorithm attribute within the DigestMethod element, if the algorithm defined in [V2G20-2318] shall be used according to the configuration in [V2G20-2320].

[V2G20-771] The following message elements of the XML signature framework shall not be used when transmitting signatures in the header of the V2G message:

- Id (attribute in SignedInfo)

- ##any in SignedInfo - CanonicalizationMethod

– HMACOutputLength in SignedInfo – SignatureMethod

- ##other in SignedInfo - SignatureMethod

– Type (attribute in SignedInfo-Reference)

- ##other in SignedInfo - Reference - Transforms - Transform

- XPath in SignedInfo - Reference - Transforms - Transform

- ##other in SignedInfo - Reference - DigestMethod

- Id (attribute in SignatureValue)

- Object (in Signature)

- KeyInfo

<div style="text-align: center;">NOTE 2 This allows to determine an upper bound for the size of the signature header.</div>
