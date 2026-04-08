[V2G20-2046] When a TLS session is terminated due to a VAS session being terminated, the EVCC shall irretrievably erase/delete/destroy all cryptographic data calculated for that particular TLS session. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, etc.

[V2G20-2047] When a TLS session is terminated due to a V2G session being paused, the EVCC shall irretrievably erase/delete/destroy all cryptographic data calculated for that particular TLS session. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, etc.

[V2G20-2049] When a V2G session is terminated due to any reason (charging process completed, user cancelled charging, cable disconnected, etc.), the EVCC shall terminate all TLS sessions associated with that V2G session. This includes terminating any TLS sessions associated with any VAS associated with that V2G session. The EVCC shall irretrievably erase/delete/destroy all cryptographic data calculated for all TLS sessions being terminated. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, any TLS session tickets that may have been stored, data stored for "Session Binding", etc.

[V2G20-2050] When a TLS session is terminated due to a VAS session being terminated, the SECC shall irretrievably erase/delete/destroy all cryptographic data calculated for that particular TLS session. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, etc.

NOTE 1 All other active TLS session(s) tied to the same V2G session can be completely unaffected under these circumstances.

[V2G20-2051] When a TLS session is terminated due to a V2G session being paused, the SECC shall irretrievably erase/delete/destroy all cryptographic data calculated for that particular TLS session. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, etc.

[V2G20-2053] When a V2G session is terminated due to any reason (charging process completed, user cancelled charging, cable disconnected, etc.), the SECC shall terminate all TLS sessions associated with that V2G session. This includes terminating any TLS sessions associated with any VAS associated with that V2G session. SECC shall irretrievably erase/delete/destroy all cryptographic data calculated for all TLS sessions being terminated. This includes all keys calculated for TLS encryption, any data calculated for certificate validation, any TLS session tickets that may have been stored, data stored for "Session Binding", etc.

NOTE 2 This is different than pausing of the V2G session.

##### 7.7.3.9 General TLS security comments

IETF RFC 8446:2018, Annex E provides some security risks associated with TLS 1.3 and suggests a few mitigation techniques. The implementers should be cognizant of these and should carefully consider pros and cons of each mitigation technique before incorporating it in the solution.

At the discretion of CSO, the SECC may cache OCSP responses for vehicle certificate for later use. The next time the SECC receives the vehicle certificates for the same EVCC, it may use the cached OCSP responses, if still valid, for revocation status thereby saving time. The methodology to achieve this is not in the scope of this document. It should be noted, though, that relying on the cached OCSP response here will mean that latest updates to that certificate's status could be missed. Refer to 7.3.1 when implementing OCSP response caching.

## 80 

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.