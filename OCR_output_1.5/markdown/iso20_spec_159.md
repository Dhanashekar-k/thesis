[V2G20-2563] In case of EIM, the SECC shall complete the authorization at the SECC and provide appropriate response to the EVCC via AuthorizationRes. Refer to 8.6 and its subclauses for details of the response codes.

NOTE 1 It is not in the scope of this document to define how to perform authorization in EIM mode.

[V2G20-2564] In case of PnC, the SECC shall verify the received signature of the AuthorizationReq message by using the provided contract certificate. The SECC shall validate the contract certificate in AuthorizationReq according to [V2G20-1001], [V2G20-2323] and [V2G20-2324]. If any of the aforementioned verifications and validations fail, the SECC shall consider the contract certificate as invalid, and shall not use said contract certificate any further – see [V2G20-2212], [V2G20-2213], [V2G20-2214] and [V2G20-2215].

NOTE 2 The SECC can use a secondary actor for signature verification and for contract certificate validation. It is possible that the certificate failed due to a lack of communication between the SECC and the CSO. It can validate the certificate later. It is up to the CSO's discretion to decide whether to provide services or request authorization using other means.

[V2G20-2565] In case of PnC, the SECC shall verify, that the received GenChallenge matches the GenChallenge that was previously sent by the SECC. If this verification fails, the SECC shall consider the signature as invalid. See [V2G20-2216] and [V2G20-2564]. The SECC may use a secondary actor for signature verification.

[V2G20-1200] In case of EIM, the SECC shall send AuthorizationRes with ResponseCode = "OK" and EVSEProcessing = "Finished" once the external authorization has been successfully completed.

Refer to [V2G20-1583] for details of what options are available to the EVCC after receiving AuthorizationRes message indicating an issue with the contract certificate provided via the previous AuthorizationReq message.

###### 8.3.4.3.4 ServiceDiscoveryReq/Res

####### 8.3.4.3.4.1 ServiceDiscoveryReq/Res handling

The service discovery enables the EVCC to find all services provided by the SECC. This document only describes relevant aspects of the interface between EVCC and SECC with regards to charging/discharging the EV. Nevertheless, the basis for discovery of future value added services is already considered and offers means for extensibility. Therefore, the service discovery differentiates between various service types and scopes.

####### 8.3.4.3.4.2 ServiceDiscoveryReq

By sending the ServiceDiscoveryReq message the EVCC triggers the SECC to send information about all services offered by the SECC. Furthermore, the EVCC can limit for particular services by sending a list of supported service IDs.

## [V2G20-1248]

The EVCC and the SECC shall implement the message elements as defined in Table 38 and Figure 42.