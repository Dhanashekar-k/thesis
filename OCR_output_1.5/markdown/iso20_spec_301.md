[V2G20-1920] The SECC and the EVCC shall implement this type as defined in Figure 163 and Table 154.

<div style="text-align: center;"><img src="imgs/img_in_image_box_362_244_756_334.jpg" alt="Image" width="33%" /></div>


<div style="text-align: center;">Figure 163 — Schema diagram — Detailed TaxType</div>


The elements of this message are used according to Table 154.

<div style="text-align: center;">Table 154 — Semantics and type definition for Detailed TaxType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>TaxRuleID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:numericIDTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>ID of the tax rule</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Amount</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTypeRefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Amount of the tax cost</td></tr></table>

###### 8.3.5.3.61 Detailed Cost Type

This type is used to indicate how much a transaction cost.

The SECC and the EVCC shall implement this type as defined in Table 155 and Figure 164.

<div style="text-align: center;"><img src="imgs/img_in_image_box_345_949_777_1041.jpg" alt="Image" width="36%" /></div>


<div style="text-align: center;">Figure 164 — Schema diagram — Detailed Cost Type</div>


The elements of this message are used according to Table 155.

<div style="text-align: center;">Table 155 — Semantics and type definition for Detailed Cost Type</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Amount</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTypeRefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>How much the single transaction costs.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CostPerUnit</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTypeRefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>What the cost was on a per-unit basis.</td></tr></table>

###### 8.3.5.3.62 PriceLevelScheduleType

[V2G20-1922]

The SECC and the EVCC shall implement this type as defined in Figure 165 and Table 156.

