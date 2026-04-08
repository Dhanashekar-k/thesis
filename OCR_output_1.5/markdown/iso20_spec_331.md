[V2G20-1769]

The SECC and the EVCC shall implement this type as defined in Figure 178 and Table 169.



<div style="text-align: center;"><img src="imgs/img_in_image_box_170_247_931_941.jpg" alt="Image" width="63%" /></div>


<div style="text-align: center;">Figure 178 — Schema diagram - BPT_Dynamic_AC_CLResControlModeType The elements of this message are used according to Table 169.</div>


<div style="text-align: center;">Table 169 — Semantics and type definition for BPT_Dynamic_AC_CLResControlModeType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DepartureTime</td><td style='text-align: center; word-wrap: break-word;'>simpleType:xs:unsignedInt</td><td style='text-align: center; word-wrap: break-word;'>Optional:This element is used to indicate when the EV intends to finish the charging process.Only used when service parameter MobilityNeedsMode was set to 2The value is encoded in seconds since the TimeStamp of the message header (see [V2G20-2104]).</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>MinimumSOC</td><td style='text-align: center; word-wrap: break-word;'>simpleType:percentValueTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional:New MinimumSOC value updated by the user from EVSE&#x27;s sideOnly used when service parameter MobilityNeedsMode was set to 2.</td></tr></table>