
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Message/Action</td><td style='text-align: center; word-wrap: break-word;'>Abbr</td><td style='text-align: center; word-wrap: break-word;'>Com</td><td style='text-align: center; word-wrap: break-word;'>DC</td><td style='text-align: center; word-wrap: break-word;'>ACDP</td><td style='text-align: center; word-wrap: break-word;'>Msg Looped</td><td style='text-align: center; word-wrap: break-word;'>Next message(s) on success</td><td style='text-align: center; word-wrap: break-word;'>Exception handling on app level failure</td><td style='text-align: center; word-wrap: break-word;'>Exception handling on msg timeout</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>SessionStop</td><td style='text-align: center; word-wrap: break-word;'>SSP</td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>N</td><td style='text-align: center; word-wrap: break-word;'>SSP</td><td style='text-align: center; word-wrap: break-word;'>SDP-Restart</td><td style='text-align: center; word-wrap: break-word;'>ESDW</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Wait for new session</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>SDP-Restart</td><td style='text-align: center; word-wrap: break-word;'>SDP-Restart</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td colspan="9">Multiplexed communication</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>MeteringConfirmation</td><td style='text-align: center; word-wrap: break-word;'>MCON</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>N</td><td style='text-align: center; word-wrap: break-word;'>MCON</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>ESDW</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ACDP_SystemStatus</td><td style='text-align: center; word-wrap: break-word;'>SYSS</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>x</td><td style='text-align: center; word-wrap: break-word;'>Y</td><td style='text-align: center; word-wrap: break-word;'>SYSS</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>SDP-Restart</td></tr></table>

NOTE 1 Emergency shut down (ESDW) according to IEC 61851-23:2014, Annex CC.5 and wait for change of control pilot to State A.

NOTE 2 ACDP\_SystemStatus has a separate payload type, see Table 14.

###### 8.3.4.7.4 SDP parameters for ACDP

For ACDP use case the SDP client needs to select the appropriate configuration compliant with the following requirement:

[V2G20-4003]

For ACDP an SDP client shall send the SDP request message with the elements "PPD/P2PS" (Bit 0) set to 1 and "Coupling Type" (Bit 0/1) set to 1 accordingly.



###### 8.3.4.7.5 ACDP_VehiclePositioning

####### 8.3.4.7.5.1 ACDP_VehiclePositioningReq/Res handling

During the EV approaching process the ACDP_VehiclePositioningReq/Res messages may be used to guide the EV to the ACDP infrastructure charging area with defined x and y tolerances of the contact interface according to EN 50696.

The definition of the coordinate system for ACDP for infrastructure mounted pantograph is based on ISO 4130:1978, Annex D.

For ACDP the actual position of the EV contact interface in relation to the ACDP contact interface is determined by the pairing and positioning device.

The position information provided during the EV approaching process as well as the effective tolerance dimensions can be communicated via the ACDP_VehiclePositioningRes message. This information may be forwarded to the EV driver as guiding information.

There are three cases for positioning support between EV and EVSE. Either both the EV and the EVSE support positioning support, the EV does not, or the EV does and the EVSE does not. The sequence is slightly different in these three cases.

## Case 1:

Positioning support from both sides. The EVCC will start sending ACDP_VehiclePositioningReq with EVPositioningSupport=True, and EVMobilityStatus=Mobilized since it is asking the SECC to help it position the EV. The SECC will reply ACDP_VehiclePositioningRes with EVSEPositioningSupport=True and EVSEProcessing=Ongoing and provide positioning information to assist the EV in moving to the correct charging position. When the EVCC receives this information,

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.