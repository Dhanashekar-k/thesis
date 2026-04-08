#### 7.8.3 Protocol data unit

##### 7.8.3.1 Structure

The V2GTP PDU consists of a header and a body section as shown in Table 11.

<div style="text-align: center;">Table 11 — V2GTP message structure</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>Payload</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>8 Bytes</td><td style='text-align: center; word-wrap: break-word;'>4294967295 Bytes</td></tr></table>

The payload contains the application data (e.g. a V2G message). The header separates the payloads (i.e. individual V2GTP messages) within a byte stream and gives information for the payload processing.

The V2GTP message header structure is shown in Table 12 and described in Table 13. The supported payload types are described in Table 14.

<div style="text-align: center;">Table 12 — V2GTP message header structure</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Byte No.</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>5</td><td style='text-align: center; word-wrap: break-word;'>6</td><td style='text-align: center; word-wrap: break-word;'>7</td><td style='text-align: center; word-wrap: break-word;'>8</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header field</td><td style='text-align: center; word-wrap: break-word;'>Protocol version</td><td style='text-align: center; word-wrap: break-word;'>Inverse protocol version</td><td colspan="2">Payload type</td><td colspan="4">Payload length</td></tr></table>

'2G20-082] A V2GTP entity shall use the header structure as shown in Table 12.

[V2G20-083] A V2GTP entity shall send the 8 bytes of the V2GTP header in the order as shown in Table 12.

[V2G20-084] A byte with a lower number shall be sent before a byte with a higher number. The header starts with byte 1 and ends with byte 8.

[V2G20-085] A V2GTP entity shall send the fields "payload type" and "payload length" in big-endian format: The most significant byte is sent first, the least significant byte is sent last.

<div style="text-align: center;">Table 13 — Generic V2GTP header structure</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Header field</td><td style='text-align: center; word-wrap: break-word;'>Header field description</td><td style='text-align: center; word-wrap: break-word;'>Header field values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Protocol Version</td><td style='text-align: center; word-wrap: break-word;'>Identifies the protocol version of V2GTP messages.</td><td style='text-align: center; word-wrap: break-word;'>0x01: V2GTP version 10x00, 0x02-0xFF: reserved by document</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Inverse Protocol Version</td><td style='text-align: center; word-wrap: break-word;'>Contains the bit-wise inverse value of the protocol version which is used in conjunction with the V2GTP protocol version as a protocol verification pattern to ensure that a correctly formatted V2GTP message is received.Equals the &lt;Protocol_Version&gt; XOR 0xFF</td><td style='text-align: center; word-wrap: break-word;'>0xFE: V2GTP Version 10xFF, 0xFD-0x00: reserved by document</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Payload Type</td><td style='text-align: center; word-wrap: break-word;'>Contains information about how to decode the payload following the V2GTP header.</td><td style='text-align: center; word-wrap: break-word;'>Refer to Table 14 for a complete list of payload type values.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Payload Length</td><td style='text-align: center; word-wrap: break-word;'>Contains the length of the V2GTP message payload in bytes (i.e. excluding the generic V2GTP header bytes).</td><td style='text-align: center; word-wrap: break-word;'>0...4294967295</td></tr></table>

<div style="text-align: center;">Table 14 — V2GTP payload types</div>


Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.