[V2G20-1279] The EVCC and the SECC shall implement the message elements as defined in Table 60 and Figure 64.

<div style="text-align: center;"><img src="imgs/img_in_image_box_276_242_823_349.jpg" alt="Image" width="45%" /></div>


<div style="text-align: center;">Figure 64 — Schema diagram - DC_CableCheckReq</div>


The element of this message is used according to Table 60.

<div style="text-align: center;">Table 60 — Semantics and type definition for DC_CableCheckReq</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTyperefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr></table>

NOTE DC_CableCheckReq contains no elements

####### 8.3.4.5.3.3 DC CableCheckRes

After receiving the DC_CableCheckReq from the EVCC the SECC sends the DC_CableCheckRes informing the EVCC about the result of the cable check and EVSE status.

[V2G20-1280]

The EVCC and the SECC shall implement the message elements as defined in Table 61 and Figure 65.



<div style="text-align: center;"><img src="imgs/img_in_image_box_258_908_813_1115.jpg" alt="Image" width="46%" /></div>


<div style="text-align: center;">Figure 65 — Schema diagram - DC_CableCheckRes</div>


The elements of this message are used according to Table 61.

<div style="text-align: center;">Table 61 — Semantics and type definition for DC_CableCheckRes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTyperefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ResponseCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType:responseCodeTypeenumerationrefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>ResponseCode indicating the acknowledgment status of any of the V2G messages received by the SECC.</td></tr></table>