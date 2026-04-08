[V2G20-1246] The EVCC and the SECC shall implement the message elements as defined in Table 32 and Figure 36.

<div style="text-align: center;"><img src="imgs/img_in_image_box_268_244_800_407.jpg" alt="Image" width="44%" /></div>


<div style="text-align: center;">Figure 36 — Schema diagram - SessionSetupReq</div>


The element of this message is used according to Table 32.

<div style="text-align: center;">Table 32 — Semantics and type definition for SessionSetupReq</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTypeRefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVCCID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:identifierTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Specifies the EVCC&#x27;s unique identifier.</td></tr></table>

[V2G20-1062] The EVCC shall transmit an EVCCID with the first 3 bytes containing the WMI as defined in ISO 3780:2009.

####### 8.3.4.3.1.2 SessionSetupRes

By using the SessionSetupRes the SECC responds to a SessionSetupReq. With the SessionSetupRes the SECC notifies the EVCC with an enclosed ResponseCode, whether establishing a new session or joining a previous communication session was successful or not.

7] The EVCC and the SECC shall implement the message elements as defined in Table 33 and Figure 37.

<div style="text-align: center;"><img src="imgs/img_in_image_box_267_1118_807_1328.jpg" alt="Image" width="45%" /></div>


<div style="text-align: center;">Figure 37 — Schema diagram - SessionSetupRes</div>


The elements of this message are used according to Table 33.

<div style="text-align: center;">Table 33 — Semantics and type definition for SessionSetupRes</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr></table>

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.