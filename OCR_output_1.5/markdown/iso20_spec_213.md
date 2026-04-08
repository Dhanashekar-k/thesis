
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Element Name</td><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Semantics</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ResponseCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType: responseCodeType enumeration refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>ResponseCode indicating the acknowledgment status of any of the V2G messages received by the SECC.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EVSEProcessing</td><td style='text-align: center; word-wrap: break-word;'>simpleType: processingType enumeration refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Parameter indicating that the EVSE has finished the processing that was initiated after the WPT_PairingReq or if the EVSE is still processing at the time, the response message was sent.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ObservedIDCode</td><td style='text-align: center; word-wrap: break-word;'>simpleType: numericIDType refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional: The identifier observed by the supply device through P2PS signaling according to the pairing method applied (omitted if not required for the pairing method).</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>AlternativeSECCList</td><td style='text-align: center; word-wrap: break-word;'>complexType: AlternativeSECCListType refer to 8.3.5.6.1</td><td style='text-align: center; word-wrap: break-word;'>Optional: List of connection information to alternative SECCs in the order of highest probability in case the pairing failed.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>VendorSpecificDataContainer</td><td style='text-align: center; word-wrap: break-word;'>simpleType: WPT_DataContainerType refer to Annex A for the type definition</td><td style='text-align: center; word-wrap: break-word;'>Optional: Data container for additional vendor specific information.</td></tr></table>

####### 8.3.4.6.4.4 General WPT_Pairing Requirements

[V2G20-5007] Both EVCC and SECC shall support the set of WPT pairing messages as described in 8.3.4.6.4, which are required to process the WPT pairing.

######## 8.3.4.6.4.4.1 Requirements for EVCC

[V2G20-5008] To start the pairing process the EVCC shall send a WPT_PairingReq message.

[V2G20-5012] If the EVCC has identified a pairing code it shall send a WPT_PairingReq message with the parameter ObservedIDCode set to the pairing identification code and the EVProcessing parameter set to "Finished".

[V2G20-5049] As long as the EVProcessing Element in WPT_PairingReq is "Ongoing" the EVResultCode shall be set to "EVResultUnknown".

[V2G20-5050] If the EVProcessing element in WPT_PairingReq is set to "Finished" the EVResultCode shall not be set to "EVResultUnknown".

######## 8.3.4.6.4.4.2 Requirements for SECC

[V2G20-5016] If the SECC has received the WPT_PairingReq message with the parameter ObservedIDCode set to a pairing identification code and the validation of the

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.