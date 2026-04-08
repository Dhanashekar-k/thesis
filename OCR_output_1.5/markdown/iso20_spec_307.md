<div style="text-align: center;"><img src="imgs/img_in_image_box_82_168_806_746.jpg" alt="Image" width="60%" /></div>


<div style="text-align: center;">Figure 169 — Schema diagram - AC_CPDResEnergyTransferModeType</div>


<div style="text-align: center;">The elements of this message are used according to Table 160.</div>


<div style="text-align: center;">Table 160 — Semantics and type definition for AC_CPDResEnergyTransferModeType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumChargePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Maximum power allowed by the EVSE</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumChargePower_L2</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Maximum power allowed by the EVSE on phase L2 (as defined in 8.3.5.2.2)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMaximumChargePower_L3</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Maximum power allowed by the EVSE on phase L3 (as defined in 8.3.5.2.2)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMinimumChargePower</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Any target power between this level and zero may, for technical reasons, result in a drop of the actual power to zero watts</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEMinimumChargePower_L2</td><td style='text-align: center; word-wrap: break-word;'>complexType:RationalNumberTyperefer to 8.3.5.3.8</td><td style='text-align: center; word-wrap: break-word;'>Optional:Any target power on phase L2 between this level and zero may, for technical reasons, result in a drop of the actual power to zero watts.</td></tr></table>