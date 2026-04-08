<div style="text-align: center;"><img src="imgs/img_in_image_box_370_166_747_234.jpg" alt="Image" width="31%" /></div>


<div style="text-align: center;">Figure 126 — Schema diagram - ServiceIDListType</div>


The elements of this message are used according to Table 123.

<div style="text-align: center;">Table 123 — Semantics and type definition for ServiceIDListType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ServiceID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:serviceIDTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>This element identifies a service which has been offered by the SECC in the ServiceDiscoveryRes message.</td></tr></table>

###### 8.3.5.3.30 EMAIDListType

[V2G20-1588] The SECC and the EVCC shall implement this type as defined in Figure 127 and Table 124.

<div style="text-align: center;"><img src="imgs/img_in_image_box_388_758_730_825.jpg" alt="Image" width="28%" /></div>


<div style="text-align: center;">Figure 127 — Schema diagram - EMAIDListType</div>


The elements of this message are used according to Table 124.

<div style="text-align: center;">Table 124 — Semantics and type definition for EMAIDListType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EMAID</td><td style='text-align: center; word-wrap: break-word;'>simpleType identifierType refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Contains the EMAID as defined in C.1.</td></tr></table>

###### 8.3.5.3.31 EIM_AReqAuthorizationModeType

This type contains all elements of the AuthorizationReq message that are only required in case the authorization mode EIM is chosen.

[V2G20-1875]

The SECC and the EVCC shall implement this type as defined in Table 125 and Figure 128.



EIM\_AReqAuthorizationModeType

<div style="text-align: center;">Figure 128 — Schema diagram - EIM_AReqAuthorizationModeType</div>


<div style="text-align: center;">Table 125 — Semantics and type definition for EIM_AReqAuthorizationModeType</div>
