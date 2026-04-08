
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SelectedScheduleTupleID</td><td style='text-align: center; word-wrap: break-word;'>simpleType:numericIDTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>This element includes the ScheduleTupleID the EV chose for this session.</td></tr></table>

<div style="text-align: center;">8.3.5.3.39 SignedInstallationDataType</div>


<div style="text-align: center;">[V2G20-1878]</div>


The SECC and the EVCC shall implement this type as defined in Figure 136 and Table 133.

<div style="text-align: center;"><img src="imgs/img_in_image_box_247_470_1008_861.jpg" alt="Image" width="63%" /></div>


<div style="text-align: center;">Figure 136 — Schema diagram - SignedInstallationDataType</div>


The elements of this message are used according to Table 133.

<div style="text-align: center;">Table 133 — Semantics and type definition for SignedInstallationDataType</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ContractCertificateChain</td><td style='text-align: center; word-wrap: break-word;'>complexType:ContractCertificateChainTyperefer 8.3.5.3.5</td><td style='text-align: center; word-wrap: break-word;'>The certificate chain to be used for authorization of the service(s) being utilized at the EVSE.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ECDHCurve</td><td style='text-align: center; word-wrap: break-word;'>simpleType:ECDHCurveTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Parameter indicating which (elliptic curve) EC the eMSP wants to use for generating the session key (seed) used to encrypt the contract certificate private key.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>DHPublicKey</td><td style='text-align: center; word-wrap: break-word;'>simpleType:dhKeyTyperefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Diffie Hellman public key from the SA for generating the session key at the EVCC in order to encrypt the contract signature private key at the SA and decrypt it a the EVCC. Refer to 7.9.2.5.4 for details.</td></tr></table>