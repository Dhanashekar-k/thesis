<div style="text-align: center;"><img src="imgs/img_in_image_box_277_174_976_467.jpg" alt="Image" width="58%" /></div>


<div style="text-align: center;">Figure 89 — Schema diagram - ACDP_DisconnectRes</div>


The elements of this message are used according to Table 86.

<div style="text-align: center;">Table 86 — Semantics and type definition for ACDP_DisconnectRes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTyperefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ResponseCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType:responseCodeTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>ResponseCode indicating the acknowledgment status of any of the V2G Messages received by the SECC.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEProcessing</td><td style='text-align: center; word-wrap: break-word;'>simpleType:processingTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Parameter indicating that the EVSE has finished the processing that was initiated after the ACDP_ConnectReq or if the EVSE is still processing at the time, the response message was sent.</td></tr></table>