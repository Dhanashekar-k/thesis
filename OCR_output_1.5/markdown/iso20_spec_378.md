way as EV lead. This case requires communication session exchange measured position in form of difference from target.

Also locating control within an EV has two varieties, one is manual driving by customer with indication of difference information from target position, and another is auto parking function. Target position consists of device position within a parking lot and install offset within vehicle frame. Vehicle frame is defined as enveloping square to vehicle outline. These values are exchanged as ones of service parameter lists. Usually these requires calibration with registration to EVSEs in advance.

As for vehicle check out, main object is to inform EVSE of EV departure and vacant parking lot. It seems to be considered necessary for the EVSE detect vacation of EV without dedicated devices for it. Recently such devices have become more popular, so that this service is confirmed by them in some cases.

[V2G20-1365]

The EVCC and the SECC shall implement the ServiceParameterList for parking status as defined in Table 213.



<div style="text-align: center;">Table 213 — Configuration parameters for parking status</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterName</td><td style='text-align: center; word-wrap: break-word;'>ParameterType</td><td style='text-align: center; word-wrap: break-word;'>Values</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>IntendedService</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: VehicleCheckIn2: VehicleCheckOut</td><td style='text-align: center; word-wrap: break-word;'>intended service during parking status session</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ParkingStatusType</td><td style='text-align: center; word-wrap: break-word;'>intValue</td><td style='text-align: center; word-wrap: break-word;'>1: Auto/Internal2: Auto/External3: Manual/Internal4: Manual/External</td><td style='text-align: center; word-wrap: break-word;'>Type parking status;Auto: auto parkingManual: manual parkingInternal: information exchange inside ISO 15118External: information exchange outside ISO 15118</td></tr></table>

[V2G20-2136] If the EVCC and the SECC agree to select "VehicleCheckIn" with setting value of 1 to "IntendedService", "VehicleCheckIn" request and response shall apply to selected "ParkingStatusService" as unique type of message exchange set.

[V2G20-2137] If the EVCC and the SECC agree to select "VehicleCheckOut" with setting value of 2 to "IntendedService", "VehicleCheckOut" request and response shall apply to selected "ParkingStatusService" as unique type of message exchange set.

### 8.5 V2G communication timing

#### 8.5.1 Overview

This subclause describes the timing and error handling for the V2G communication session with EXI encoded messages of V2GTP payload type in the range of 0x8001 up to 0x81FF. The error handling is based on timers enabling the EVCC and the SECC to monitor the V2G message exchange. For the detection of missing or delayed messages the EVCC and the SECC use predefined timeout values as error criteria. Whenever a timer is equal or larger than the related timeout the related error handling is processed.

The monitoring of a V2G communication message exchange is based on two timer categories:

– message timer: monitors the exchange of a request message and the corresponding response message (request-response-pair);

– sequence timer: monitors the exchange of multiple request-response-pairs.

#### 8.5.2 Common