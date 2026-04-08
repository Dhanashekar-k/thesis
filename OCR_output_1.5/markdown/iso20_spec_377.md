###### 8.4.3.2.6 Internet service

Internet service is an optional value added service (VAS). This subclause provides some details of the parameters necessary to implement this service.

[V2G20-1362]

The EVCC and the SECC shall implement the ServiceParameterList for internet service as defined in Table 212.



NOTE 1 This subclause simply provides some of the parameters necessary for implementing this service. It is up to the SA/CSO and OEM to define the security mechanisms necessary to secure this service.

<div style="text-align: center;">Table 212 — ServiceParameterList for internet service</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>ParameterSetID (unsignedshort)</td><td style='text-align: center; word-wrap: break-word;'>ParameterName = Protocol</td><td style='text-align: center; word-wrap: break-word;'>ParameterName = Port</td><td style='text-align: center; word-wrap: break-word;'>Description</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>Reserved by ISO.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>stringValue = ftp</td><td style='text-align: center; word-wrap: break-word;'>intValue = 20</td><td style='text-align: center; word-wrap: break-word;'>Service to use internet access using FTP protocol via port 20.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>stringValue = ftp</td><td style='text-align: center; word-wrap: break-word;'>intValue = 21</td><td style='text-align: center; word-wrap: break-word;'>Service to use internet access using FTP protocol via port 21.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>stringValue = http</td><td style='text-align: center; word-wrap: break-word;'>intValue = 80</td><td style='text-align: center; word-wrap: break-word;'>Service to use internet access using HTTP protocol via port 80.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>stringValue = https</td><td style='text-align: center; word-wrap: break-word;'>intValue = 443</td><td style='text-align: center; word-wrap: break-word;'>Service to use internet access using HTTPS protocol via port 443.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>5 - 65535</td><td style='text-align: center; word-wrap: break-word;'>service name according to IANA Service &amp; Port Registry</td><td style='text-align: center; word-wrap: break-word;'>port number according to IANA Service &amp; Port Registry</td><td style='text-align: center; word-wrap: break-word;'>Additional protocol port combinations which are supported by the SECC for internet access.</td></tr></table>

[V2G20-430]

If the SECC supports additional protocol / port combinations beyond the definitions in Table 212, it shall use the service names and the assigned port numbers according according to IANA Service & Port Registry (i.e. the service name defined in IANA Service & Port Registry is transmitted as the "Protocol" and the port number defined in IANA Service & Port Registry is transmitted as "Port").

<div style="text-align: center;">NOTE 2 It is assumed if an IANA Service & Port Registry defined service name and port number combination is applicable for both transport protocols, TCP and UDP, the SECC supports connections on TCP or UDP or on both for the respective combination.</div>


###### 8.4.3.2.7 Parking status service

Parking status is a VAS, applied in case that the EV is approaching a parking lot or leaving from it. It requires wireless communication for the reason that both use cases cannot have charging cable be connected. This use case covers separate sessions between parking status and charging with a couple of hours.

As for vehicle check in, one of main two objects is notification the completion of EV locating to EVSE and another is measured position exchange in order to help the EV locate the collect position.

Locating policy has two type variations, one is EV lead, measuring by EV with some of optical or other type of sensors, only inform the result to the EVSE. Another is EVSE lead, measuring by EVSE with similar