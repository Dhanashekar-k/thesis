<div style="text-align: center;">Table 36 — Semantics and type definition for AuthorizationReq</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Header</td><td style='text-align: center; word-wrap: break-word;'>complexType:MessageHeaderTypeRefer to 8.3.3</td><td style='text-align: center; word-wrap: break-word;'>Contains general information, used for all messages.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SelectedAuthorizationService</td><td style='text-align: center; word-wrap: break-word;'>simple Type:authorizationTypeenumerationrefer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>A parameter that indicates which Authorization Service, which was provided by the EVSE, is chosen by the EV.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EIM_AReqAuthorizationMode</td><td style='text-align: center; word-wrap: break-word;'>complexType:EIM_AReqAuthorizationModeTyperefer to 8.3.5.3.31</td><td style='text-align: center; word-wrap: break-word;'>Element to be sent when EIM is chosen as Authorization Method.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>PnC_AReqAuthorizationMode</td><td style='text-align: center; word-wrap: break-word;'>complexType:PnC_AReqAuthorizationModeTyperefer to 8.3.5.3.32</td><td style='text-align: center; word-wrap: break-word;'>This element contains both the challenge sent by the SECC in AuthorizationSetupRes and the EVCC&#x27;s contract certificate</td></tr></table>

In case the EVCC has at least one (1) contract certificate and the EVCC wishes to utilize PnC, the EVCC can use SupportedProviders received as part of AuthorizationSetupRes message to identify and select the contract certificate to be provided for that particular session.

SupportedProviders contains the list of providers (eMSPs) supported by the SECC. Each SupportedProvider in SupportedProviders contains data that the EVCC can compare with the data in EMAID of each contract certificate it contains to identify at least one contract certificate that can be utilized at that particular EVSE.

It should be noted that, although not desirable, SupportedProviders may not be exhaustive. That means there might be eMSPs outside of this list that may be supported by the SECC.

In case none of the contract certificates that the EVCC possesses match any of the supported providers in SupportedProviders, the EVCC, at its discretion (or user's discretion, depending upon the OEM implementation), may either choose to still send each of its contract certificates one by one to see if any of them may be accepted or it may switch to EIM.

Similarly, it should be noted that SupportedProviders may be quite long (refer to 8.3.5.3.35 for the allowed length). EVCC, at its (OEM's) discretion, may only accept part of the list provided by the SECC.

In case EIM was selected as authorization service, unless otherwise stated, anytime an element is prefixed with EIM (e.g. EIM_AReqAuthorizationMode), it shall be used. Anytime an element is prefixed with PnC (e.g. PnC_AReqAuthorizationMode), it shall not be used.

[V2G20-2561] In case PnC was selected as authorization service, unless otherwise stated, anytime an element is prefixed with PnC (e.g. PnC_AReqAuthorizationMode), it shall be used. Anytime an element is prefixed with EIM (e.g. EIM_AReqAuthorizationMode), it shall not be used.

[V2G20-2562] In case EVCC did not receive OCSP responses for any of the certificates in the PE certificate chain, it shall not utilize PnC even if the private SECC supports it.