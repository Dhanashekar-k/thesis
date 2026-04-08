the SECC, then the SECC returns the corresponding response message. All messages exchanged between EVCC and SECC are described with their syntax and their semantics in 8.2 and 8.3. The entire XML schema definition describing V2G message set is included in Annex A.

8.3.4 defines the V2G message and respective message elements required to be supported for a certain set of use case elements described in ISO 15118-1.

8.5 defines message timing and error handling for the V2G communication message exchange.

Message sequences are shown in 8.6.

V2G communication consists of two different message types:

- V2G application layer protocol handshake messages (refer to 8.2),

V2G application layer messages (refer to 8.3).

[V2G20-809] When transmitting application layer messages the big-endian byte order rule shall be applied: the most significant byte is sent first, the least significant byte is sent last.

### 8.2 Protocol handshake definition

[V2G20-2129] If in the supportedAppProtocolReq, an energy transfer mode is offered based on ISO 15118-20, all features implemented for this energy transfer mode in older generations of the document still need to be supported for ISO 15118-20.

NOTE The impact of [V2G20-2129] is described by the following examples:

An EVCC currently supports DIN SPEC 70121 and now wants to support ISO 15118-20 (this document) as well. Since DIN SPEC 70121 only offers the minimum feature set, implementing even the most minimal feature set of ISO 15118-20 for DC will suffice.

An EVCC currently supports DIN SPEC 70121 DC & PnC according to ISO 15118-2. It now wants to support BPT/DC according to ISO 15118-20 (this document). Based on [V2G20-2129], the EVCC also supports PnC for this document, as otherwise a feature would only be supported with ISO 15118-2 and not with this document, potentially forcing the usage of ISO 15118-2 even when both sides support this document.

An EVCC currently supports AC & PnC according to ISO 15118-2 and now wants to support BPT/DC according to ISO 15118-20 (this document). The EVCC will transmit a supportedAppProtocolReq with two entries. One entry uses the namespace "urn:iso:15118:2:2013:MsgDef" while the other one uses "urn:iso:std:iso:15118:-20:DC". Since it becomes clear to the SECC from the namespace "urn:iso:std:iso:15118:-20:DC" that the EVCC only supports DC according to (this document), an AC SECC will select ISO 15118-2, while a DC SECC will select this document.

#### 8.2.1 Handshake sequence

[V2G20-165] Before starting the application layer message exchange, an appropriate application layer protocol including its version shall be negotiated between the EVCC and the SECC.

In order to negotiate the protocol between the EVCC and the SECC the following application layer protocol handshake is performed.

## [V2G20-166]

The EVCC shall initiate the handshake by sending a supportedAppProtocolReq message as depicted in Figure 32 to the SECC. This request message provides a list of charging protocols supported by the EVCC.