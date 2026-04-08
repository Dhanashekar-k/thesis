[V2G20-045] The EVCC shall implement NDP as defined in IETF RFC 4861.

NOTE 1 IETF RFC 4861 has been updated by IETF RFC 5942, IETF RFC 6980, IETF RFC 7048, IETF RFC 7527, IETF RFC 7559, IETF RFC 8028, IETF RFC 8319 and IETF RFC 8425. These updates are considered to be included in this document.

[V2G20-046] The EVCC shall comply with IETF RFC 4429 allowing assignment of IP addresses before duplicate address detection is finished.

NOTE 2 IETF RFC 4429 has been by IETF RFC 7527. These updates are considered to be included in this document.

##### 7.6.2.4 Internet control message protocol (ICMP)

The internet control message protocol (ICMP) is used to send error messages (e.g. a requested service is not available, a host could not be reached).

[V2G20-047] Each V2G entity shall implement ICMPv6 as specified in IETF RFC 4443.

NOTE 3 IETF RFC 4443 has been updated by IETF RFC 4884 which has been updated by IETF RFC 8335. These updates are considered to be included in this document.

[V2G20-049] Each V2G entity shall implement the RFCs referred to in column "Reference" of Table 4 describing the implementation details for the respective ICMP message type.

<div style="text-align: center;">Table 4 — Mandatory ICMP message set</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ICMP message type</td><td style='text-align: center; word-wrap: break-word;'>ICMP message name</td><td style='text-align: center; word-wrap: break-word;'>Reference</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>Destination unreachable</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4443</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>Packet too big</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8335</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>Time exceeded</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4443</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>Parameter problem</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8335</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>128</td><td style='text-align: center; word-wrap: break-word;'>Echo request</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4443</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>129</td><td style='text-align: center; word-wrap: break-word;'>Echo reply</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 8335</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>133</td><td style='text-align: center; word-wrap: break-word;'>Router solicitation</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4861</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>134</td><td style='text-align: center; word-wrap: break-word;'>Router advertisement</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4861</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>135</td><td style='text-align: center; word-wrap: break-word;'>Neighbor solicitation</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4861</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>136</td><td style='text-align: center; word-wrap: break-word;'>Neighbor advertisement</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4861</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>137</td><td style='text-align: center; word-wrap: break-word;'>Redirect message</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 4861</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>141</td><td style='text-align: center; word-wrap: break-word;'>Inverse neighbor discovery solicitation message</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 3122</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>142</td><td style='text-align: center; word-wrap: break-word;'>Inverse neighbor discovery advertisement message</td><td style='text-align: center; word-wrap: break-word;'>IETF RFC 3122</td></tr></table>

NOTE 4 IETF RFC 4443 has been updated by IETF RFC 4884 which has been updated by IETF RFC 8335. These updates are considered to be included in this document.

NOTE 5 IETF RFC 4861 has been updated by IETF RFC 5942, IETF RFC 6980, IETF RFC 7048, IETF RFC 7527, IETF RFC 7559, IETF RFC 8028, IETF RFC 8319 and IETF RFC 8425. These updates are considered to be included in this document.

#### 7.6.3 IP addressing