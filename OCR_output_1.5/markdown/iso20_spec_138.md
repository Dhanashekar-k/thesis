<div style="text-align: center;">Table 30 — Semantics and type definition for supportedAppProtocolRes message elements</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element/Attribute Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SchemaID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:idTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional:This message element is used by the SECC to reference one of the EVCC supported protocols received in the request message.Always mandatory, only not used in case ResponseCode is equal to FAILED_NoNegotiation</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ResponseCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType:responseCodeTypeenumerationrefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>This message element is used by the SECC for indicating whether the list of protocols received from the EVCC includes at least one protocol matching with the protocols supported by the SECC.</td></tr></table>

#### 8.2.4 Message examples

##### 8.2.4.1 Protocol negotiation

Examples below illustrate the exchange of supportedAppProtocol messages between the EVCC and the SECC. In the request message, the EVCC sends a prioritized list of supported application layer protocols to the SECC. The Priority element indicates to the SECC which protocol is preferred by the EVCC. The SchemaID is simply a running counter, enabling the SECC to refer to a specific entry. In the response message the SECC confirms "urn:iso:std:iso:15118:-20:DC" by setting the SchemaID element to "2" and using a ResponseCode equal to "OK_SuccessfulNegotiation".

The following is V2G message example 1 – supportedAppProtocolReq: protocol negotiation.

<?xml version="1.0" encoding="UTF-8"?>
<n1:supportedAppProtocolReq xmlns:n1="urn:iso:15118:2:2010:AppProtocol"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="urn:iso:15118:2:2010:AppProtocol V2G_CI_AppProtocol.xsd">
    <AppProtocol>
        <ProtocolNamespace>urn:iso:std:iso:15118:-20:AC</ProtocolNamespace>
        <VersionNumberMajor>1</VersionNumberMajor>
        <VersionNumberMinor>0</VersionNumberMinor>
        <SchemaID>1</SchemaID>
        <Priority>2</Priority>
    </AppProtocol>
    <AppProtocol>
        <ProtocolNamespace>urn:iso:std:iso:15118:-20:DC</ProtocolNamespace>
        <VersionNumberMajor>1</VersionNumberMajor>
        <VersionNumberMinor>0</VersionNumberMinor>
        <SchemaID>2</SchemaID>
        <Priority>1</Priority>
    </AppProtocol>
    <AppProtocol>
        <ProtocolNamespace>urn:iso:15118:2:2013:MsgDef</ProtocolNamespace>
        <VersionNumberMajor>2</VersionNumberMajor>
        <VersionNumberMinor>0</VersionNumberMinor>
        <SchemaID>3</SchemaID>
        <Priority>3</Priority>
    </AppProtocol>
</n1:supportedAppProtocolReq>

The following is V2G message example 2 – supportedAppProtocolRes: protocol negotiation.